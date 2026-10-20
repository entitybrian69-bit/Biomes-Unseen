#!/usr/bin/env python3
"""
generate_structures.py -- author the structure templates every jigsaw pool places.

A jigsaw pool element names a template by location, and the game resolves that to
data/<namespace>/structures/<path>.nbt. Without those binary files the pool has
nothing to place: all 115 structures would be registered, would appear in the
creative structure list, and would simply never generate in a world -- a silent
hole that no compile step and no JSON check can catch.

The template paths are read back from the emitted template_pool JSON rather than
recomputed here, so this generator and generate_worldgen.py cannot disagree about
where a template lives. If a pool is renamed, the template follows.

Layouts are authored as archetypes, not noise. Each structure is built by one of
nine hand-written layout builders chosen from tokens in its own id, and dressed
in the materials of the biome it belongs to -- so a torii in a sakura biome is
sakura wood and a vent field in the Hollow Deep is hollow stone. Boss arenas get
a distinct archetype with a central altar, a pillar ring and the arena's authored
chests, because an arena has to read as a fought-in space rather than a landmark.
"""

from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from content import biomes as B          # noqa: E402
from content import structures as S      # noqa: E402
from nbt_codec import (                  # noqa: E402
    block_state, chest_nbt, structure_template, write_gzip,
)
from boss_arenas import arena_for        # noqa: E402
from registry import REGISTRY as R       # noqa: E402

MODID = "biomesunseen"
DATA = os.path.join(ROOT, "src", "main", "resources", "data")
POOL_DIR = os.path.join(DATA, MODID, "worldgen", "template_pool")

WRITTEN = 0


# --------------------------------------------------------------------------- #
#  Materials
# --------------------------------------------------------------------------- #

class Materials:
    """The block palette one structure is dressed in."""

    def __init__(self, floor: str, wall: str, pillar: str, cap: str,
                 rubble: str, accent: str):
        self.floor = floor
        self.wall = wall
        self.pillar = pillar
        self.cap = cap
        self.rubble = rubble
        self.accent = accent

    def palette(self):
        """Unique block states in a stable order, plus name -> index."""
        order = []
        for name in (self.floor, self.wall, self.pillar, self.cap,
                     self.rubble, self.accent, "minecraft:chest",
                     "minecraft:air"):
            if name not in order:
                order.append(name)
        index = {name: i for i, name in enumerate(order)}
        return [block_state(n) for n in order], index


def has_block(name: str) -> bool:
    """True if a bare registry path is one of our own blocks."""
    return name.split(":")[-1] in R.blocks


def qualify(name: str) -> str:
    """Fully qualify a block id, passing vanilla ids through."""
    return name if ":" in name else f"{MODID}:{name}"


def materials_for(spec) -> Materials:
    """
    Dress a structure in its biome's own materials.

    Taken from the first biome the structure is authored to generate in, so a
    structure looks like it was built where it stands rather than from a generic
    stone kit. Falls back to the dimension's stone list, then to vanilla stone,
    so a structure can never reference a block that does not exist.
    """
    surface_top = surface_filler = surface_stone = None
    for biome_id in list(spec.biomes) or []:
        biome = B.BY_ID.get(biome_id.split(":")[-1])
        if biome is None:
            continue
        surface_top, surface_filler, surface_stone = (
            biome.surface_top, biome.surface_filler, biome.surface_stone)
        break

    stones = [qualify(s) for s in (B.DIMENSION_STONES.get(spec.dimension) or [])]
    stones = [s for s in stones if has_block(s)]

    floor = qualify(surface_top) if surface_top and has_block(surface_top) else (
        stones[0] if stones else "minecraft:stone")
    filler = qualify(surface_filler) if surface_filler and has_block(surface_filler) else (
        stones[1] if len(stones) > 1 else floor)
    stone = qualify(surface_stone) if surface_stone and has_block(surface_stone) else (
        stones[2] if len(stones) > 2 else filler)

    # An accent that actually exists in this dimension: prefer a lantern, then
    # any ore from the same dimension, so a ruin has something worth finding.
    accent = None
    if has_block("bu_lantern"):
        accent = qualify("bu_lantern")
    if accent is None:
        for candidate in R.blocks:
            if candidate.endswith("_lantern"):
                accent = qualify(candidate)
                break
    if accent is None:
        for candidate in R.blocks:
            if candidate.endswith("_ore") and spec.dimension in candidate:
                accent = qualify(candidate)
                break
    if accent is None:
        accent = "minecraft:lantern"

    return Materials(floor=floor, wall=filler, pillar=stone, cap=stone,
                     rubble=filler, accent=accent)


# --------------------------------------------------------------------------- #
#  Layout builders
# --------------------------------------------------------------------------- #
# Each builder returns a list of (x, y, z, material-role) cells in local space.
# Coordinates are normalised to start at 0 afterwards, so a builder can work in
# centred coordinates without caring about the template's final origin.

def _disc(radius: int, y: int, role: str):
    """A filled horizontal disc."""
    cells = []
    for x in range(-radius, radius + 1):
        for z in range(-radius, radius + 1):
            if x * x + z * z <= radius * radius:
                cells.append((x, y, z, role))
    return cells


def _ring(radius: int, y: int, height: int, role: str, cap_role=None):
    """A hollow ring of columns."""
    cells = []
    for x in range(-radius, radius + 1):
        for z in range(-radius, radius + 1):
            distance = x * x + z * z
            if abs(distance - radius * radius) <= radius:
                for dy in range(height):
                    cells.append((x, y + dy, z, role))
                if cap_role:
                    cells.append((x, y + height, z, cap_role))
    return cells


def layout_arena(spec):
    """
    A boss arena: a railed platform, a pillar ring and a raised central altar.

    Deliberately open and circular so a multi-phase fight has room to move and
    the player can circle the boss, and walled at the rim so the fight cannot be
    escaped by running -- which is what makes it an arena rather than a clearing.
    """
    cells = []
    cells += _disc(10, 0, "floor")
    cells += _disc(10, -1, "wall")
    cells += _ring(10, 1, 2, "wall", cap_role="cap")
    for angle_index in range(8):
        angle = angle_index * 3.141592653589793 / 4.0
        x = int(round(7.5 * math.cos(angle)))
        z = int(round(7.5 * math.sin(angle)))
        for dy in range(6):
            cells.append((x, 1 + dy, z, "pillar"))
        cells.append((x, 7, z, "cap"))
        cells.append((x, 8, z, "accent"))
    # The altar the boss is summoned at: raised, capped and lit at the corners.
    cells += _disc(2, 1, "pillar")
    cells += _disc(2, 2, "cap")
    cells.append((0, 3, 0, "accent"))
    for dx, dz in ((-2, -2), (-2, 2), (2, -2), (2, 2)):
        cells.append((dx, 3, dz, "accent"))
    return cells


def layout_shrine(spec):
    """A walled sanctum with corner pillars, a roof and one doorway."""
    cells = []
    cells += _disc(5, 0, "floor")
    for x in range(-5, 6):
        for z in range(-5, 6):
            if max(abs(x), abs(z)) == 5:
                for dy in range(1, 4):
                    # Leave a two-block doorway on the south face.
                    if x in (0, 1) and z == 5 and dy <= 2:
                        continue
                    cells.append((x, dy, z, "wall"))
    for x, z in ((-5, -5), (-5, 5), (5, -5), (5, 5)):
        for dy in range(1, 6):
            cells.append((x, dy, z, "pillar"))
        cells.append((x, 6, z, "cap"))
        cells.append((x, 7, z, "accent"))
    for x in range(-5, 6):
        for z in range(-5, 6):
            cells.append((x, 4, z, "cap"))
    cells.append((0, 1, 0, "accent"))
    cells.append((0, 2, 0, "pillar"))
    return cells


def layout_arch(spec):
    """Two piers and a lintel: a gate or torii."""
    cells = []
    for x in range(-4, 5):
        cells.append((x, 0, 0, "floor"))
        cells.append((x, 0, 1, "floor"))
    for z in (0, 1):
        for dy in range(1, 8):
            cells.append((-4, dy, z, "pillar"))
            cells.append((-3, dy, z, "pillar"))
            cells.append((3, dy, z, "pillar"))
            cells.append((4, dy, z, "pillar"))
    for x in range(-5, 6):
        cells.append((x, 8, 0, "cap"))
        cells.append((x, 8, 1, "cap"))
        cells.append((x, 9, 0, "wall"))
    cells.append((-5, 7, 0, "accent"))
    cells.append((5, 7, 0, "accent"))
    return cells


def layout_spire(spec):
    """A tapered tower: spire, obelisk, pylon or steeple."""
    cells = []
    levels = [(4, 4), (4, 3), (3, 3), (3, 2), (2, 2), (2, 1), (1, 1)]
    y = 0
    for half, height in levels:
        for x in range(-half, half + 1):
            for z in range(-half, half + 1):
                cells.append((x, y, z, "floor" if y == 0 else "pillar"))
        for dy in range(1, height):
            for x in range(-half, half + 1):
                for z in range(-half, half + 1):
                    if max(abs(x), abs(z)) == half:
                        cells.append((x, y + dy, z, "wall"))
                    else:
                        cells.append((x, y + dy, z, "pillar"))
            cells.append((half, y + dy, half, "accent"))
            cells.append((-half, y + dy, -half, "accent"))
        y += height
    cells.append((0, y, 0, "cap"))
    cells.append((0, y + 1, 0, "accent"))
    return cells


def layout_ruin(spec):
    """Broken wall segments, a standing pillar and scattered rubble."""
    cells = []
    for x in range(-6, 7):
        for z in range(-5, 6):
            cells.append((x, 0, z, "floor"))
    # Two intact wall runs and two collapsed ones, so it reads as decayed rather
    # than as a deliberately open-sided building.
    for x in range(-6, 1):
        for dy in range(1, 4):
            cells.append((x, dy, -5, "wall"))
    for x in range(2, 7):
        for dy in range(1, 2):
            cells.append((x, dy, -5, "wall"))
    for z in range(-5, 2):
        for dy in range(1, 4):
            cells.append((-6, dy, z, "wall"))
    for z in range(3, 6):
        cells.append((-6, 1, z, "rubble"))
    for dy in range(1, 7):
        cells.append((6, dy, 5, "pillar"))
    cells.append((6, 7, 5, "cap"))
    for x, z in ((-3, 2), (-2, 3), (1, -2), (3, 1), (4, -3), (-4, -1)):
        cells.append((x, 1, z, "rubble"))
    cells.append((0, 1, 0, "accent"))
    return cells


def layout_span(spec):
    """A linear crossing: bridge, stair, weir or skyway."""
    cells = []
    for x in range(-9, 10):
        for z in range(-1, 2):
            cells.append((x, 0, z, "floor"))
        if x % 4 == 0:
            for dy in range(-3, 0):
                cells.append((x, dy, -1, "pillar"))
                cells.append((x, dy, 1, "pillar"))
    for x in range(-9, 10):
        cells.append((x, 1, -2, "wall"))
        cells.append((x, 1, 2, "wall"))
        if x % 3 == 0:
            cells.append((x, 2, -2, "cap"))
            cells.append((x, 2, 2, "cap"))
    cells.append((-9, 2, 0, "accent"))
    cells.append((9, 2, 0, "accent"))
    return cells


def layout_scatter(spec):
    """A field of small features: vents, crystals, cairns or geysers."""
    cells = []
    for x in range(-7, 8):
        for z in range(-7, 8):
            if (x * x + z * z) <= 49:
                cells.append((x, 0, z, "floor"))
    centres = [(-4, -3), (3, -4), (0, 2), (-2, 5), (5, 3)]
    for index, (cx, cz) in enumerate(centres):
        height = 2 + (index % 3)
        for dy in range(1, height + 1):
            cells.append((cx, dy, cz, "pillar"))
        cells.append((cx, height + 1, cz, "accent"))
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            cells.append((cx + dx, 1, cz + dz, "rubble"))
    return cells


def layout_camp(spec):
    """Huts around a central fire: village, outpost, waystation or caravan."""
    cells = []
    for x in range(-8, 9):
        for z in range(-7, 8):
            cells.append((x, 0, z, "floor"))
    huts = [(-5, -4), (4, -4), (-5, 3), (4, 3)]
    for hx, hz in huts:
        for x in range(hx - 2, hx + 3):
            for z in range(hz - 2, hz + 3):
                cells.append((x, 1, z, "wall"))
                cells.append((x, 2, z, "wall"))
                cells.append((x, 3, z, "cap"))
        # Hollow the interior and cut a door.
        for x in range(hx - 1, hx + 2):
            for z in range(hz - 1, hz + 2):
                cells.append((x, 1, z, "air"))
                cells.append((x, 2, z, "air"))
        cells.append((hx, 1, hz + 2, "air"))
        cells.append((hx, 2, hz + 2, "air"))
        cells.append((hx, 1, hz, "accent"))
    cells.append((0, 1, 0, "accent"))
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        cells.append((dx, 1, dz, "rubble"))
    return cells


def layout_chamber(spec):
    """An underground room with load-bearing columns and a ceiling."""
    cells = []
    for x in range(-6, 7):
        for z in range(-6, 7):
            cells.append((x, 0, z, "floor"))
            cells.append((x, 6, z, "cap"))
    for x in range(-6, 7):
        for z in range(-6, 7):
            if max(abs(x), abs(z)) == 6:
                for dy in range(1, 6):
                    cells.append((x, dy, z, "wall"))
    for cx, cz in ((-3, -3), (-3, 3), (3, -3), (3, 3)):
        for dy in range(1, 6):
            cells.append((cx, dy, cz, "pillar"))
    for x in range(-2, 3):
        for dy in range(1, 4):
            cells.append((x, dy, 6, "air"))
    cells.append((0, 1, 0, "accent"))
    cells.append((0, 2, 0, "pillar"))
    return cells


# Archetype selection by token, ordered so the most specific tokens win. A
# structure whose id matches none of these falls back to a shrine, which is a
# reasonable landmark for anything unclassified.
ARCHETYPES = [
    (("arena", "colosseum", "caldera", "amphitheatre"), layout_arena),
    (("torii", "arch", "gate", "gateway", "portal", "door"), layout_arch),
    (("spire", "obelisk", "pylon", "tower", "steeple", "monolith",
      "column", "needle", "stair", "skyward"), layout_spire),
    (("bridge", "crossing", "weir", "span", "causeway", "viaduct",
      "aqueduct", "span_"), layout_span),
    (("vent", "cluster", "field", "geyser", "scatter", "bloom",
      "grove_marker", "stones", "henge"), layout_scatter),
    (("village", "outpost", "waystation", "caravan", "camp", "hold",
      "settlement", "hamlet"), layout_camp),
    (("ruin", "remains", "cairn", "wreck", "fallen", "shatter",
      "broken", "tomb", "grave"), layout_ruin),
    (("cave", "cavern", "hollow", "chamber", "deep", "underground",
      "vault", "crypt", "cathedral"), layout_chamber),
    (("shrine", "temple", "sanctum", "altar", "citadel", "palace",
      "observatory", "archive", "library"), layout_shrine),
]


def layout_for(spec):
    """Pick the authored archetype that fits this structure's id."""
    haystack = spec.id.lower()

    # A boss arena gets its own hand-authored layout, keyed to that boss's phase
    # machine rather than to a generic circle-and-pillars template. All five were
    # previously built by the same layout_arena, which produced five arenas of
    # identical geometry -- 21x10x21, 923 blocks each -- differing only in which
    # blocks dressed them. The arena is half the encounter, so it is authored per
    # boss: the Skyward Crown's has no walls because aerial_dive is only a threat
    # if falling off is possible, and the Warden's is fully enclosed because
    # tremor_slam needs somewhere for the shock to be felt.
    boss_id = getattr(spec, "boss", None)
    if boss_id:
        bespoke = arena_for(boss_id)
        if bespoke is not None:
            return lambda _spec: bespoke(_spec)
    if spec.is_boss_arena:
        return layout_arena
    for tokens, builder in ARCHETYPES:
        if any(token in haystack for token in tokens):
            return builder
    return layout_shrine


# --------------------------------------------------------------------------- #
#  Assembly
# --------------------------------------------------------------------------- #

def normalise(cells):
    """
    Shift cells so the minimum corner is the origin, later writes winning.

    Builders work in centred coordinates and may overwrite the same cell (a hut
    wall hollowed out by 'air', for example), so the last write for a position is
    the one that stands.
    """
    min_x = min(c[0] for c in cells)
    min_y = min(c[1] for c in cells)
    min_z = min(c[2] for c in cells)
    filled = {}
    for x, y, z, role in cells:
        filled[(x - min_x, y - min_y, z - min_z)] = role
    return filled


def chests_for(spec, occupied) -> list:
    """
    Place the structure's authored chests on free floor cells.

    Chests carry the loot table by reference, so the structure's authored drops
    -- including the lore book the Golden Rules require -- roll on first open.
    Positions are chosen deterministically from the structure's own salt so a
    regenerated template is byte-identical and chests do not drift between runs.
    """
    placements = []
    tables = list(spec.loot_tables or [])
    if not tables:
        return placements

    # Candidate spots are any free cell sitting directly on top of solid
    # masonry, at whatever height that happens to be. Scanning the built
    # structure rather than assuming a floor at y=0 is what lets the floating
    # arenas host chests at all: the Void Serpent's platforms are at y=2..6 with
    # nothing beneath them, so a y=0 probe found one spot and quietly dropped the
    # lore chest -- which is the chest the Golden Rules require every structure
    # to guarantee.
    candidates = []
    for (x, y, z), role in occupied.items():
        if role in ("air", "chest"):
            continue
        above = (x, y + 1, z)
        if above in occupied:
            continue
        candidates.append(above)
    if not candidates:
        raise SystemExit(
            f"structure '{spec.id}' has no free cell above masonry for a chest")
    candidates.sort()

    cursor = spec.salt
    for index, table in enumerate(tables):
        # Walk the candidate list deterministically from the structure's own salt
        # so a regenerated template is byte-identical and chests do not drift
        # between runs, and so two chests never land on the same cell.
        for _attempt in range(len(candidates)):
            cursor = (cursor * 1103515245 + 12345) & 0x7FFFFFFF
            spot = candidates[cursor % len(candidates)]
            if spot in occupied:
                continue
            placements.append((spot[0], spot[1], spot[2], table, index))
            occupied[spot] = "chest"
            break
        else:
            # A dropped loot table is invisible in game -- the structure simply
            # generates without its reward -- so it fails the build instead.
            raise SystemExit(
                f"structure '{spec.id}' could not place loot table '{table}': "
                f"no free cell remained")
    return placements


def template_paths_on_disk():
    """Every (pool file, element location) pair the emitted pools declare."""
    found = []
    if not os.path.isdir(POOL_DIR):
        return found
    for root, _dirs, files in os.walk(POOL_DIR):
        for name in sorted(files):
            path = os.path.join(root, name)
            doc = json.load(open(path, encoding="utf-8"))
            for element in doc.get("elements", []):
                location = element.get("element", {}).get("location")
                if location:
                    found.append((path, location))
    return found


def build(spec, location: str) -> None:
    """Write one structure template."""
    global WRITTEN
    namespace, _, template = location.partition(":")
    dest = os.path.join(DATA, namespace, "structures", template + ".nbt")
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    materials = materials_for(spec)
    palette, index = materials.palette()
    cells = normalise(layout_for(spec)(spec))

    role_to_block = {
        "floor": materials.floor, "wall": materials.wall,
        "pillar": materials.pillar, "cap": materials.cap,
        "rubble": materials.rubble, "accent": materials.accent,
        "air": "minecraft:air", "chest": "minecraft:chest",
    }

    blocks = []
    for (x, y, z), role in sorted(cells.items()):
        if role == "air":
            continue
        blocks.append(((x, y, z), index[role_to_block[role]]))

    # Chests go in after the masonry so they are never overwritten by it, and
    # each carries its authored loot table plus a seed derived from the
    # structure's own salt.
    for x, y, z, table, order in chests_for(spec, cells):
        seed = (spec.salt * 31 + order * 7919) & 0x7FFFFFFFFFFFFFFF
        blocks.append(((x, y, z), index["minecraft:chest"],
                       chest_nbt(table if ":" in table else f"{MODID}:{table}",
                                 seed)))

    # Measured after the chests: a chest placed on top of the highest cell would
    # otherwise fall outside the template's declared size, and a block outside
    # its own template is dropped when the structure places.
    size_x = max(b[0][0] for b in blocks) + 1
    size_y = max(b[0][1] for b in blocks) + 1
    size_z = max(b[0][2] for b in blocks) + 1

    write_gzip(dest, "", structure_template((size_x, size_y, size_z),
                                            palette, blocks))
    WRITTEN += 1


def main() -> None:
    specs_by_pool = {s.start_jigsaw_pool: s for s in S.ALL_STRUCTURES}
    pools = template_paths_on_disk()
    if not pools:
        raise SystemExit(
            "no template pools found; run tools/generate_worldgen.py first")

    unresolved = []
    for _path, location in pools:
        pool_path = location.split(":", 1)[-1]
        # The element location is "<pool>/start"; the pool id is the parent.
        pool_id = pool_path.rsplit("/", 1)[0]
        spec = specs_by_pool.get(pool_id)
        if spec is None:
            # Fall back to matching by the structure's own id, which is the last
            # path segment of the pool for both boss and landmark pools.
            tail = pool_id.rsplit("/", 1)[-1]
            spec = next((s for s in S.ALL_STRUCTURES if s.id == tail), None)
        if spec is None:
            unresolved.append(location)
            continue
        build(spec, location)

    if unresolved:
        raise SystemExit(
            f"{len(unresolved)} template locations map to no structure spec: "
            f"{unresolved[:5]}")
    print(f"[structures] wrote {WRITTEN} templates for {len(S.ALL_STRUCTURES)} structures")


if __name__ == "__main__":
    main()
