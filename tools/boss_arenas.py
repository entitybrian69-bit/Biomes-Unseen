#!/usr/bin/env python3
"""
boss_arenas.py -- the five hand-authored boss arena layouts.

Every boss fight in this mod happens in a structure the player walks into, so the
arena is half the encounter: it has to telegraph what the boss does, give the
phases somewhere to happen, and read as a place built for one specific creature
rather than a generic circle with pillars.

These layouts are authored per boss and keyed to that boss's phase machine, which
is the part that makes them more than decoration:

    heart_of_the_forest   summon_roots / explosive_seeds / heart_exposed
        A root-woven clearing. Four great tapered root pillars carry arches, and
        the centre is a raised heart-stump the boss is summoned on -- "heart
        exposed" is a phase about reaching that centre, so the centre is built to
        be reached.

    void_serpent          phase_out / coil_slam / phase_in
        Floating coil platforms over open void. A central disc with four
        satellites at different heights, joined by narrow bridges, because a
        serpent that phases out and slams down wants vertical space and somewhere
        for the player to be stranded.

    warden_of_the_hollow_deep  tremor_slam / spire_rise / burrow
        An enclosed cavern. Thick walls and a ceiling so tremor_slam has
        something to shake, six spires that read as the things spire_rise raises,
        and a floor of broken rubble for burrow to disappear into.

    the_skyward_crown     aerial_dive / crown_split / shard_orbit
        A sky island with no walls at all, tapered to a point underneath. Five
        crown spires in a ring are the shards that orbit, and the open edge is
        what makes aerial_dive dangerous rather than theatrical.

    the_unraveling        form.quadruped / form.serpent / form.humanoid / glitch_burst
        Deliberately asymmetric and broken. Three distinct dais areas, one per
        form it takes, on uneven platforms at odd heights -- an unstable creature
        should not fight in a symmetrical room.

Geometry only lives here. Materials come from the structure's own biome, resolved
by generate_structures.materials_for, so each arena is built out of whatever the
place it generates in is actually made of.

Coordinates are local and centred on the origin; generate_structures normalises
them into the template's own space afterwards.
"""

from __future__ import annotations

import math
from typing import List, Tuple

Cell = Tuple[int, int, int, str]


def _disc(radius: int, y: int, role: str, hollow: bool = False) -> List[Cell]:
    """A horizontal disc, optionally just its rim."""
    cells = []
    for x in range(-radius, radius + 1):
        for z in range(-radius, radius + 1):
            distance = x * x + z * z
            if distance > radius * radius:
                continue
            if hollow and distance < (radius - 1) * (radius - 1):
                continue
            cells.append((x, y, z, role))
    return cells


def _column(x: int, z: int, y0: int, height: int, role: str,
            cap: str = None, finial: str = None) -> List[Cell]:
    """A column with an optional cap and finial, used for pillars and spires."""
    cells = [(x, y0 + dy, z, role) for dy in range(height)]
    top = y0 + height
    if cap:
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                cells.append((x + dx, top, z + dz, cap))
    if finial:
        cells.append((x, top + 1, z, finial))
    return cells


def _tapered_pillar(x: int, z: int, y0: int, height: int, role: str,
                    cap: str = None) -> List[Cell]:
    """
    A pillar that narrows as it rises.

    A straight box reads as masonry; tapering reads as growth, which is what a
    root pillar or a stone spire is doing. The radius steps down at thirds.
    """
    cells = []
    for dy in range(height):
        fraction = dy / max(1, height - 1)
        radius = 2 if fraction < 0.34 else (1 if fraction < 0.72 else 0)
        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                if dx * dx + dz * dz <= radius * radius:
                    cells.append((x + dx, y0 + dy, z + dz, role))
    if cap:
        cells.append((x, y0 + height, z, cap))
    return cells


# --------------------------------------------------------------------------- #
#  Heart of the Forest -- root-woven clearing
# --------------------------------------------------------------------------- #

def heart_of_the_forest(_spec) -> List[Cell]:
    cells: List[Cell] = []

    # Mossy clearing floor with a stone heart at the centre.
    cells += _disc(11, 0, "floor")
    cells += _disc(11, -1, "wall")
    cells += _disc(4, 0, "rubble")

    # Four great root pillars on the cardinal points, tapered so they read as
    # grown rather than built, each carrying a light at the top.
    for angle_index in range(4):
        angle = angle_index * math.pi / 2.0
        x = int(round(8.0 * math.cos(angle)))
        z = int(round(8.0 * math.sin(angle)))
        cells += _tapered_pillar(x, z, 1, 11, "pillar", cap="cap")
        cells.append((x, 12, z, "accent"))

    # Root arches spanning between adjacent pillars, so the canopy reads as
    # enclosed without building a wall the player cannot see through.
    for angle_index in range(4):
        a0 = angle_index * math.pi / 2.0
        a1 = (angle_index + 1) * math.pi / 2.0
        for step in range(1, 6):
            t = step / 6.0
            x = int(round(8.0 * (math.cos(a0) * (1 - t) + math.cos(a1) * t)))
            z = int(round(8.0 * (math.sin(a0) * (1 - t) + math.sin(a1) * t)))
            # The arch rises to its crown midway between the pillars.
            lift = int(round(3.0 * math.sin(t * math.pi)))
            cells.append((x, 10 + lift, z, "pillar"))

    # The heart stump: a raised dais the boss is summoned on. Three tiers so the
    # player climbs it, which is what makes "heart exposed" a positional phase
    # rather than a damage check.
    cells += _disc(3, 1, "pillar")
    cells += _disc(2, 2, "cap")
    cells += _disc(1, 3, "cap")
    cells.append((0, 4, 0, "accent"))

    # Buttress roots radiating from the stump out to the clearing floor.
    for angle_index in range(8):
        angle = angle_index * math.pi / 4.0 + math.pi / 8.0
        for radius in range(2, 8):
            x = int(round(radius * math.cos(angle)))
            z = int(round(radius * math.sin(angle)))
            height = 2 if radius < 5 else 1
            for dy in range(height):
                cells.append((x, 1 + dy, z, "rubble"))

    # A low rim so the clearing has an edge, broken at the four approaches.
    for x in range(-11, 12):
        for z in (-11, 11):
            if abs(x) < 3:
                continue
            cells.append((x, 1, z, "wall"))
    for z in range(-11, 12):
        for x in (-11, 11):
            if abs(z) < 3:
                continue
            cells.append((x, 1, z, "wall"))
    return cells


# --------------------------------------------------------------------------- #
#  Void Serpent -- floating coil platforms over open void
# --------------------------------------------------------------------------- #

def void_serpent(_spec) -> List[Cell]:
    cells: List[Cell] = []

    # The central coil: a disc with a spiral ridge rising out of it, which is the
    # serpent's own body language carried into the architecture.
    cells += _disc(7, 0, "floor")
    cells += _disc(7, -1, "wall")
    for step in range(34):
        angle = step * 0.55
        radius = 1.0 + step * 0.17
        x = int(round(radius * math.cos(angle)))
        z = int(round(radius * math.sin(angle)))
        if x * x + z * z <= 49:
            cells.append((x, 1, z, "pillar"))
            if step % 5 == 0:
                cells.append((x, 2, z, "cap"))
    cells.append((0, 2, 0, "accent"))

    # Four satellite platforms at different heights. Uneven heights are the
    # point: coil_slam wants the player to have somewhere high to be knocked off,
    # and phase_out wants them to have somewhere to lose track of the boss.
    satellites = [(11, 11, 2), (-11, 10, 4), (12, -10, 6), (-12, -11, 3)]
    for sx, sz, sy in satellites:
        cells += _disc(3, sy, "floor")
        cells += _disc(3, sy - 1, "wall")
        cells.append((sx, sy + 1, sz, "accent"))
        # A tapered spur hanging below each platform, so they read as broken
        # fragments of something larger rather than as placed discs.
        for dy in range(1, 4):
            radius = 3 - dy
            for dx in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    if dx * dx + dz * dz <= radius * radius:
                        cells.append((sx + dx, sy - 1 - dy, sz + dz, "rubble"))

    # Narrow bridges from the central coil to each satellite. One block wide, so
    # crossing one during a slam is genuinely a risk rather than a formality.
    for sx, sz, sy in satellites:
        steps = 9
        for step in range(1, steps):
            t = step / steps
            x = int(round(sx * t * 0.62))
            z = int(round(sz * t * 0.62))
            y = int(round(sy * t))
            cells.append((x, y, z, "cap"))
            # A single rail block on the outer side only, so the bridge has a
            # wrong side to be pushed off from.
            if step % 3 == 0:
                cells.append((x, y + 1, z, "pillar"))
    return cells


# --------------------------------------------------------------------------- #
#  Warden of the Hollow Deep -- enclosed cavern
# --------------------------------------------------------------------------- #

def warden_of_the_hollow_deep(_spec) -> List[Cell]:
    cells: List[Cell] = []
    half = 11
    wall_height = 9

    # Floor, ceiling and four thick walls. Enclosure is the design: tremor_slam
    # needs somewhere for the shock to be felt, and a warden that burrows wants a
    # floor to disappear into rather than open sky.
    for x in range(-half, half + 1):
        for z in range(-half, half + 1):
            cells.append((x, 0, z, "floor"))
            cells.append((x, wall_height + 1, z, "cap"))
            if max(abs(x), abs(z)) == half:
                for dy in range(1, wall_height + 1):
                    cells.append((x, dy, z, "wall"))

    # Six spires in an uneven ring -- these are what spire_rise reads against, so
    # they have to be tall enough to matter and few enough to dodge between.
    spires = [(-7, -6, 6), (-2, -8, 5), (5, -6, 7), (7, 3, 5), (1, 7, 6), (-6, 5, 4)]
    for sx, sz, height in spires:
        cells += _tapered_pillar(sx, sz, 1, height, "pillar", cap="cap")

    # A drill-shaped dais at the centre: the warden's own silhouette, stepped so
    # it narrows to a point.
    for tier, radius in enumerate((3, 2, 1)):
        y = 1 + tier
        for x in range(-radius, radius + 1):
            for z in range(-radius, radius + 1):
                if x * x + z * z <= radius * radius:
                    cells.append((x, y, z, "cap" if tier else "pillar"))
    cells.append((0, 4, 0, "accent"))

    # Rubble field, denser toward the walls: the burrow phase wants broken ground
    # to read as somewhere the warden could have gone.
    for x in range(-half + 1, half):
        for z in range(-half + 1, half):
            distance = math.hypot(x, z)
            if distance > 4 and (x * 7 + z * 13) % 5 == 0:
                cells.append((x, 1, z, "rubble"))

    # Two doorways on opposite sides so the arena can be entered and, more
    # importantly, fled.
    for x in range(-1, 2):
        for dy in range(1, 4):
            cells.append((x, dy, -half, "air"))
            cells.append((x, dy, half, "air"))

    # Ceiling lights over the ring, so the cavern is not pitch black.
    for sx, sz, _height in spires:
        cells.append((sx, wall_height, sz, "accent"))
    return cells


# --------------------------------------------------------------------------- #
#  Skyward Crown -- open sky island
# --------------------------------------------------------------------------- #

def the_skyward_crown(_spec) -> List[Cell]:
    cells: List[Cell] = []

    # A flat-topped island with no walls whatsoever. The open edge is the whole
    # design: aerial_dive is only threatening if falling off is possible, and a
    # walled arena would turn the crown's signature move into a damage number.
    cells += _disc(10, 0, "floor")

    # Tapered underside, so the island reads as a broken fragment of the
    # floating landmass around it rather than as a disc placed in the sky.
    for depth in range(1, 8):
        radius = 10 - depth
        if radius < 1:
            break
        for x in range(-radius, radius + 1):
            for z in range(-radius, radius + 1):
                if x * x + z * z <= radius * radius:
                    cells.append((x, -depth, z, "wall" if depth < 3 else "rubble"))

    # Five crown spires in a ring. Five, matching the regalia, and spaced so the
    # player can be forced to move between them during shard_orbit.
    for index in range(5):
        angle = index * 2.0 * math.pi / 5.0 - math.pi / 2.0
        x = int(round(7.0 * math.cos(angle)))
        z = int(round(7.0 * math.sin(angle)))
        height = 9 if index == 0 else 7
        cells += _tapered_pillar(x, z, 1, height, "pillar", cap="cap")
        cells.append((x, height + 2, z, "accent"))

    # A low parapet only on the inward side of each spire, giving cover that
    # faces the centre -- so hiding is possible but never safe, because the boss
    # is always on the other side of it.
    for index in range(5):
        angle = index * 2.0 * math.pi / 5.0 - math.pi / 2.0
        x = int(round(7.0 * math.cos(angle)))
        z = int(round(7.0 * math.sin(angle)))
        inward_x = -1 if x > 0 else 1
        inward_z = -1 if z > 0 else 1
        cells.append((x + inward_x * 2, 1, z + inward_z, "wall"))
        cells.append((x + inward_x, 1, z + inward_z * 2, "wall"))

    # A raised dais at the centre where the crown is summoned.
    cells += _disc(2, 1, "cap")
    cells.append((0, 2, 0, "accent"))

    # Broken stair fragments on three sides, implying the island was once
    # reachable and now is not -- which is why the portal is the way in.
    for angle_index in range(3):
        angle = angle_index * 2.0 * math.pi / 3.0
        for step in range(5):
            x = int(round((10 + step) * math.cos(angle)))
            z = int(round((10 + step) * math.sin(angle)))
            cells.append((x, -step, z, "rubble"))
    return cells


# --------------------------------------------------------------------------- #
#  The Unraveling -- fractured, deliberately asymmetric
# --------------------------------------------------------------------------- #

def the_unraveling(_spec) -> List[Cell]:
    cells: List[Cell] = []

    # Three dais areas, one per form the Unraveling takes, at different heights
    # and on deliberately unequal footings. A shapeshifter fighting in a
    # symmetrical room reads as a bug, so nothing here is mirrored.
    forms = [
        ("quadruped", (-8, -5, 0), 6),
        ("serpent", (7, -7, 2), 5),
        ("humanoid", (2, 8, 1), 4),
    ]
    for _name, (fx, fz, fy), radius in forms:
        # Each platform is an ellipse rather than a disc, and offset, so the three
        # arenas-in-one do not look like the same shape stamped three times.
        for x in range(-radius, radius + 1):
            for z in range(-radius, radius + 1):
                if (x * x) / float(radius * radius) + (z * z) / float(
                        (radius - 1) * (radius - 1)) <= 1.0:
                    cells.append((fx + x, fy, fz + z, "floor"))
                    cells.append((fx + x, fy - 1, fz + z, "wall"))
        cells.append((fx, fy + 1, fz, "accent"))

    # Fractured walkways joining them, each at a different width and slope.
    for index in range(len(forms)):
        _n0, (x0, z0, y0), _r0 = forms[index]
        _n1, (x1, z1, y1), _r1 = forms[(index + 1) % len(forms)]
        steps = 10
        width = 1 + (index % 2)
        for step in range(steps + 1):
            t = step / float(steps)
            x = int(round(x0 + (x1 - x0) * t))
            z = int(round(z0 + (z1 - z0) * t))
            # Deliberately not a straight ramp: the middle sags, so crossing has a
            # visible low point the player has to commit to.
            sag = -1 if 3 <= step <= 7 else 0
            y = int(round(y0 + (y1 - y0) * t)) + sag
            for w in range(width):
                cells.append((x + w, y, z, "cap"))

    # Glitch shards: free-standing fragments at odd angles around the whole space,
    # which is what glitch_burst detonates past. Placed on a fixed but irregular
    # pattern rather than a ring, so they never read as decoration placed by rule.
    shard_offsets = [(-11, 2, 1), (-4, -11, 2), (5, -12, 1), (11, -3, 3),
                     (12, 6, 2), (4, 12, 1), (-6, 11, 2), (-12, -6, 1),
                     (0, 0, 4), (-9, 8, 2), (9, -9, 2)]
    for sx, sz, height in shard_offsets:
        lean = 1 if (sx + sz) % 2 == 0 else -1
        for dy in range(height):
            cells.append((sx + lean * (dy // 2), dy + 1, sz, "pillar"))
        cells.append((sx + lean * (height // 2), height + 1, sz, "accent"))

    # A floor of broken plates under the whole arena, with gaps, so the void shows
    # through in places and the space never feels solid.
    for x in range(-13, 14):
        for z in range(-13, 14):
            if x * x + z * z > 169:
                continue
            if (x * 5 + z * 3) % 11 == 0:
                continue
            cells.append((x, -2, z, "rubble"))
    return cells


# --------------------------------------------------------------------------- #

#: Boss id -> its authored arena layout.
BOSS_ARENAS = {
    "heart_of_the_forest": heart_of_the_forest,
    "void_serpent": void_serpent,
    "warden_of_the_hollow_deep": warden_of_the_hollow_deep,
    "the_skyward_crown": the_skyward_crown,
    "the_unraveling": the_unraveling,
}


def arena_for(boss_id: str):
    """The authored layout for a boss, or None if it has no bespoke arena."""
    return BOSS_ARENAS.get(boss_id)
