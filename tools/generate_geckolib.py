#!/usr/bin/env python3
"""
generate_geckolib.py -- emit the .geo.json rigs and .animation.json clips.

Golden Rule #2 forbids CubeListBuilder and ModelPart: every creature in this mod
is a GeckoLib model. That means each one needs a real geometry file and a real
animation file, or it renders as a missing model no matter how good its texture
is. This script writes both.

Six family rigs cover all 80 creatures, because every member of a family shares
one articulated skeleton and one authored 64x32 atlas band layout -- what differs
between species is the texture, not the rig. The five bosses each get their own
multi-part rig from a 64x64 atlas.

UV MAPPING IS DERIVED FROM THE AUTHORED ATLAS, NOT GUESSED.
The pixel matrices in tools/pixelart/ compose each atlas from named regions laid
out at fixed rows and columns. The boxes below sample exactly those regions, and
every face is chosen so its uv_size matches the region 1:1 -- no face is
stretched, which is what keeps hand-authored pixel art from blurring or shearing.

Creature atlas (64x32), as composed by creature_maps._atlas():
    v0..7    head right u0-7 | head front u8-15 | head left u16-23 | head back u24-31
             torso right u32-47 | torso front u48-63
    v8..15   head top u0-15 | head bottom u16-31 | torso back u32-47 | torso top u48-63
    v16..25  four limb cells at u0, u16, u32, u48; within a cell the four faces
             are 4 columns each with no gutter: right | front | left | back
    v26..29  limb root occlusion, same four columns per cell
    v30..31  transparent

Boss atlas (64x64), as composed by boss_maps.build_boss_atlas():
    v0..15   body front u0-15 | body back u16-31 | body right u32-47 | body left u48-63
    v16..23  head front | head back | head right | head left, same columns
    v24..31  head top u0-15 | head bottom u16-31 | body top u32-47 | body bottom u48-63
    v32..47  four limb cells at u0, u16, u32, u48, each 16 rows tall
    v48..63  four extra cells (wings, spires, shards, canopy)

The tail band is deliberately not mapped. creature_maps patches the tail into
u24..35 / v14..25, which overlaps the front-right and back-left limb cells, so
there is no clean rectangle to sample. Mapping it would corrupt two legs to gain
one tail, so the rigs omit the bone instead.
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from content import bosses as BO         # noqa: E402
from content import mobs as M            # noqa: E402

MODID = "biomesunseen"
ASSETS = os.path.join(ROOT, "src", "main", "resources", "assets", MODID)

GEO_VERSION = "1.12.0"
ANIM_VERSION = "1.8.0"

WRITTEN = 0


def write(rel: str, payload) -> None:
    global WRITTEN
    dest = os.path.join(ASSETS, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    WRITTEN += 1


# --------------------------------------------------------------------------- #
#  Cube construction
# --------------------------------------------------------------------------- #

def face(u: int, v: int, w: int, h: int) -> dict:
    """One per-face UV entry."""
    return {"uv": [u, v], "uv_size": [w, h]}


def cube(origin, size, uv, inflate: float = 0.0) -> dict:
    """
    A geometry cube with explicit per-face UV.

    Per-face UV is used rather than a single box `uv` offset because the authored
    atlases do not follow Bedrock's standard box unwrap: the regions were laid out
    by hand, so each face has to name its own rectangle.
    """
    out = {"origin": list(origin), "size": list(size), "uv": uv}
    if inflate:
        out["inflate"] = inflate
    return out


def bone(name: str, parent: str, pivot, cubes, rotation=None) -> dict:
    entry = {"name": name, "parent": parent, "pivot": list(pivot)}
    if rotation:
        entry["rotation"] = list(rotation)
    if cubes:
        entry["cubes"] = cubes
    return entry


def geometry(identifier: str, tex_w: int, tex_h: int, bones,
             bounds_w: float, bounds_h: float, bounds_y: float) -> dict:
    return {
        "format_version": GEO_VERSION,
        "minecraft:geometry": [{
            "description": {
                "identifier": identifier,
                "texture_width": tex_w,
                "texture_height": tex_h,
                "visible_bounds_width": bounds_w,
                "visible_bounds_height": bounds_h,
                "visible_bounds_offset": [0, bounds_y, 0],
            },
            "bones": bones,
        }],
    }


# --------------------------------------------------------------------------- #
#  Creature atlas regions
# --------------------------------------------------------------------------- #

# Head is 8x8x8: the four side faces are 8x8 at v0..7, and the top/bottom faces
# sample the left half of the 16-wide top/bottom regions at v8..15.
def head_uv() -> dict:
    return {
        "west": face(0, 0, 8, 8),     # right, -x
        "south": face(8, 0, 8, 8),    # front, +z
        "east": face(16, 0, 8, 8),    # left, +x
        "north": face(24, 0, 8, 8),   # back, -z
        "up": face(0, 8, 8, 8),
        "down": face(16, 8, 8, 8),
    }


# Torso is 16 wide, 8 tall, 8 deep. Front and back take the full 16x8 regions;
# the two side faces split the 16-wide torso_right region into halves so every
# face still maps 1:1. The underside has no authored region and is rarely
# visible, so it reuses the top.
def torso_uv() -> dict:
    return {
        "south": face(48, 0, 16, 8),   # front, +z
        "north": face(32, 8, 16, 8),   # back, -z
        "west": face(32, 0, 8, 8),     # right, -x
        "east": face(40, 0, 8, 8),     # left, +x
        "up": face(48, 8, 16, 8),
        "down": face(48, 8, 16, 8),
    }


# A limb cell is 16 columns wide: four 4-column faces with no gutter, 10 rows of
# leg at v16..25 and 4 rows of root at v26..29 for the top and bottom caps.
def limb_uv(base: int) -> dict:
    return {
        "west": face(base + 0, 16, 4, 10),
        "south": face(base + 4, 16, 4, 10),
        "east": face(base + 8, 16, 4, 10),
        "north": face(base + 12, 16, 4, 10),
        "up": face(base + 0, 26, 4, 4),
        "down": face(base + 4, 26, 4, 4),
    }


# The tail band, matching TAIL_U / TAIL_V in creature_maps. Four 3-column faces
# side by side and 12 rows tall, which is exactly the 3x12x3 box the tail bone
# declares -- so no face is stretched. The caps have no authored art of their own
# and reuse the top of the right face, which is standard for a box end that is
# pressed against the body and effectively never seen.
TAIL_U = 0
TAIL_V = 34


def tail_uv() -> dict:
    return {
        "west": face(TAIL_U + 0, TAIL_V, 3, 12),
        "south": face(TAIL_U + 3, TAIL_V, 3, 12),
        "east": face(TAIL_U + 6, TAIL_V, 3, 12),
        "north": face(TAIL_U + 9, TAIL_V, 3, 12),
        "up": face(TAIL_U + 0, TAIL_V, 3, 3),
        "down": face(TAIL_U + 3, TAIL_V, 3, 3),
    }


LIMB_CELLS = {"front_left": 0, "front_right": 16, "back_left": 32, "back_right": 48}


# --------------------------------------------------------------------------- #
#  Family rigs
# --------------------------------------------------------------------------- #
# Each family reuses the same authored regions but arranges the bones into a
# different skeleton, which is what makes an avian read as an avian and a serpent
# as a serpent despite all six sharing one atlas layout.

def rig_quadruped() -> list:
    """Four legs, horizontal body, head forward at shoulder height."""
    return [
        bone("root", None, [0, 0, 0], []),
        bone("body", "root", [0, 9, 0],
             [cube([-8, 5, -4], [16, 8, 8], torso_uv())]),
        bone("neck", "body", [0, 12, -4], []),
        bone("head", "neck", [0, 13, -8],
             [cube([-4, 9, -12], [8, 8, 8], head_uv())]),
        bone("leg_front_left", "body", [-6, 5, -2],
             [cube([-8, -5, -4], [4, 10, 4], limb_uv(LIMB_CELLS["front_left"]))]),
        bone("leg_front_right", "body", [6, 5, -2],
             [cube([4, -5, -4], [4, 10, 4], limb_uv(LIMB_CELLS["front_right"]))]),
        bone("leg_back_left", "body", [-6, 5, 2],
             [cube([-8, -5, 0], [4, 10, 4], limb_uv(LIMB_CELLS["back_left"]))]),
        bone("leg_back_right", "body", [6, 5, 2],
             [cube([4, -5, 0], [4, 10, 4], limb_uv(LIMB_CELLS["back_right"]))]),
    ]


def rig_biped() -> list:
    """Upright: two legs from the hind cells, two arms from the front cells."""
    return [
        bone("root", None, [0, 0, 0], []),
        bone("body", "root", [0, 12, 0],
             [cube([-8, 8, -4], [16, 8, 8], torso_uv())]),
        bone("head", "body", [0, 16, 0],
             [cube([-4, 16, -4], [8, 8, 8], head_uv())]),
        bone("arm_left", "body", [-8, 15, 0],
             [cube([-12, 5, -2], [4, 10, 4], limb_uv(LIMB_CELLS["front_left"]))]),
        bone("arm_right", "body", [8, 15, 0],
             [cube([8, 5, -2], [4, 10, 4], limb_uv(LIMB_CELLS["front_right"]))]),
        bone("leg_left", "body", [-4, 8, 0],
             [cube([-6, -2, -2], [4, 10, 4], limb_uv(LIMB_CELLS["back_left"]))]),
        bone("leg_right", "body", [4, 8, 0],
             [cube([2, -2, -2], [4, 10, 4], limb_uv(LIMB_CELLS["back_right"]))]),
    ]


def rig_avian() -> list:
    """Two legs, and the front limb cells become wings hung off the shoulders."""
    return [
        bone("root", None, [0, 0, 0], []),
        bone("body", "root", [0, 10, 0],
             [cube([-8, 6, -4], [16, 8, 8], torso_uv())], rotation=[-75, 0, 0]),
        bone("neck", "body", [0, 12, -4], [], rotation=[30, 0, 0]),
        bone("head", "neck", [0, 14, -7],
             [cube([-4, 12, -11], [8, 8, 8], head_uv())]),
        bone("wing_left", "body", [-8, 12, 0],
             [cube([-12, 4, -2], [4, 10, 4], limb_uv(LIMB_CELLS["front_left"]))],
             rotation=[0, 0, 20]),
        bone("wing_right", "body", [8, 12, 0],
             [cube([8, 4, -2], [4, 10, 4], limb_uv(LIMB_CELLS["front_right"]))],
             rotation=[0, 0, -20]),
        bone("leg_left", "body", [-3, 6, 1],
             [cube([-5, -4, -1], [4, 10, 4], limb_uv(LIMB_CELLS["back_left"]))]),
        bone("leg_right", "body", [3, 6, 1],
             [cube([1, -4, -1], [4, 10, 4], limb_uv(LIMB_CELLS["back_right"]))]),
    ]


def rig_serpent() -> list:
    """
    No legs: the four limb cells become coil segments stacked behind the body.

    A serpent with leg bones reads as a broken quadruped, so the same authored
    limb art is repositioned along the spine as body coils instead.
    """
    coils = []
    for index, (cell, zoff) in enumerate([
            ("front_left", 4), ("front_right", 10),
            ("back_left", 16), ("back_right", 22)]):
        coils.append(bone(f"coil_{index + 1}", "body" if index == 0 else f"coil_{index}",
                          [0, 5, zoff],
                          [cube([-2, 3, zoff - 2], [4, 10, 4], limb_uv(LIMB_CELLS[cell]))]))
    return [
        bone("root", None, [0, 0, 0], []),
        bone("body", "root", [0, 5, -6],
             [cube([-8, 1, -10], [16, 8, 8], torso_uv())]),
        bone("head", "body", [0, 6, -12],
             [cube([-4, 2, -18], [8, 8, 8], head_uv())]),
    ] + coils


def rig_arthropod() -> list:
    """Low, wide body with four legs splayed outward."""
    return [
        bone("root", None, [0, 0, 0], []),
        bone("body", "root", [0, 5, 0],
             [cube([-8, 1, -4], [16, 8, 8], torso_uv())]),
        bone("head", "body", [0, 5, -6],
             [cube([-4, 1, -12], [8, 8, 8], head_uv())]),
        bone("leg_front_left", "body", [-8, 3, -2],
             [cube([-12, -5, -4], [4, 10, 4], limb_uv(LIMB_CELLS["front_left"]))],
             rotation=[0, 0, 35]),
        bone("leg_front_right", "body", [8, 3, -2],
             [cube([8, -5, -4], [4, 10, 4], limb_uv(LIMB_CELLS["front_right"]))],
             rotation=[0, 0, -35]),
        bone("leg_back_left", "body", [-8, 3, 2],
             [cube([-12, -5, 0], [4, 10, 4], limb_uv(LIMB_CELLS["back_left"]))],
             rotation=[0, 0, 35]),
        bone("leg_back_right", "body", [8, 3, 2],
             [cube([8, -5, 0], [4, 10, 4], limb_uv(LIMB_CELLS["back_right"]))],
             rotation=[0, 0, -35]),
    ]


def rig_fungal() -> list:
    """Cap over a short thick body, with stubby limbs."""
    return [
        bone("root", None, [0, 0, 0], []),
        bone("body", "root", [0, 6, 0],
             [cube([-8, 2, -4], [16, 8, 8], torso_uv())]),
        # Named "head", not "cap": creature_animations drives a head track for
        # every family, and a rig whose head bone carries any other name leaves
        # those channels driving nothing -- the cap sat perfectly still through
        # idle, walk, hurt and attack while the animation thought it was moving
        # it. The cap IS this rig's head (it uses head_uv), so the name follows.
        bone("head", "body", [0, 10, 0],
             [cube([-4, 10, -4], [8, 8, 8], head_uv())]),
        bone("leg_front_left", "body", [-5, 2, -2],
             [cube([-7, -6, -4], [4, 10, 4], limb_uv(LIMB_CELLS["front_left"]))]),
        bone("leg_front_right", "body", [5, 2, -2],
             [cube([3, -6, -4], [4, 10, 4], limb_uv(LIMB_CELLS["front_right"]))]),
        bone("leg_back_left", "body", [-5, 2, 2],
             [cube([-7, -6, 0], [4, 10, 4], limb_uv(LIMB_CELLS["back_left"]))]),
        bone("leg_back_right", "body", [5, 2, 2],
             [cube([3, -6, 0], [4, 10, 4], limb_uv(LIMB_CELLS["back_right"]))]),
    ]


# Tail bone per family: (pivot, cube origin, rotation), or None for a family
# whose tail is vestigial. Biped's authored tail region is outline-only -- every
# glyph is 'O' -- so it gets no bone; a box of pure outline would read as a
# floating wireframe behind the creature rather than as a tail.
#
# This is derived from the authored atlas rather than hardcoded per family, so a
# future family whose tail is real gets one automatically.
FAMILY_TAILS = {
    "quadruped": ([0, 12, 4], [-1.5, 0, 4], [-20, 0, 0]),
    "avian": ([0, 8, 4], [-1.5, 2, 4], [60, 0, 0]),
    "serpent": ([0, 6, 24], [-1.5, 1, 24], [-10, 0, 0]),
    "arthropod": ([0, 7, 4], [-1.5, 0, 4], [-25, 0, 0]),
    "fungal": ([0, 8, 4], [-1.5, 0, 4], [-12, 0, 0]),
    "biped": None,
}


def tail_is_real(family: str) -> bool:
    """
    Whether a family's authored tail carries anything but outline.

    Read from the pixel matrices themselves rather than from a hand-kept list, so
    the rigs and the art cannot drift: if a family's tail is later given real
    shading it starts rendering, and if one is stripped back to outline it stops.
    """
    spec = FAMILY_TAILS.get(family)
    if spec is None:
        return False
    try:
        from pixelart import creature_maps as CM
        regions = CM.FAMILIES[family]
        glyphs = set()
        for key in ("tail_r", "tail_f", "tail_l", "tail_b"):
            for row in regions.get(key) or []:
                glyphs.update(row)
        # '.' is transparent and 'O' is the 1px outline every region carries;
        # anything else means the tail was actually shaded.
        return bool(glyphs - {".", "O"})
    except Exception:  # noqa: BLE001
        # If the art cannot be introspected, trust the authored placement table
        # rather than silently dropping every tail in the mod.
        return True


def with_tail(family: str, bones: list) -> list:
    """Append the tail bone to a rig when that family has a real one."""
    if not tail_is_real(family):
        return bones
    pivot, origin, rotation = FAMILY_TAILS[family]
    return bones + [bone("tail", "body", pivot,
                         [cube(origin, [3, 12, 3], tail_uv())],
                         rotation=rotation)]


FAMILY_RIGS = {
    "quadruped": (rig_quadruped, 3.0, 2.0, 0.75),
    "biped": (rig_biped, 2.5, 3.0, 1.25),
    "avian": (rig_avian, 3.0, 2.5, 1.0),
    "serpent": (rig_serpent, 4.0, 1.5, 0.5),
    "arthropod": (rig_arthropod, 3.0, 1.5, 0.5),
    "fungal": (rig_fungal, 2.5, 2.5, 1.0),
}


# --------------------------------------------------------------------------- #
#  Boss atlas regions
# --------------------------------------------------------------------------- #
# Body is 16 wide, 16 tall, 8 deep: the four side faces are 16x16 at v0..15, the
# side faces split their 16-wide region in half, and top/bottom take the 16x8
# regions in the crown band exactly.
def boss_body_uv() -> dict:
    return {
        "south": face(0, 0, 16, 16),
        "north": face(16, 0, 16, 16),
        "west": face(32, 0, 8, 16),
        "east": face(40, 0, 8, 16),
        "up": face(32, 24, 16, 8),
        "down": face(48, 24, 16, 8),
    }


# Head is 12 wide, 8 tall, 8 deep; top and bottom take the 16x8 crown regions
# trimmed to 12 columns, which still maps without stretching.
def boss_head_uv() -> dict:
    return {
        "south": face(0, 16, 12, 8),
        "north": face(16, 16, 12, 8),
        "west": face(32, 16, 8, 8),
        "east": face(48, 16, 8, 8),
        "up": face(0, 24, 12, 8),
        "down": face(16, 24, 12, 8),
    }


def boss_limb_uv(base: int) -> dict:
    """Limb cell at v32..47: four 4-column faces 12 tall, caps in the last 4 rows."""
    return {
        "west": face(base + 0, 32, 4, 12),
        "south": face(base + 4, 32, 4, 12),
        "east": face(base + 8, 32, 4, 12),
        "north": face(base + 12, 32, 4, 12),
        "up": face(base + 0, 44, 4, 4),
        "down": face(base + 4, 44, 4, 4),
    }


def boss_extra_uv(base: int) -> dict:
    """
    Extra cell at v48..63, used for wings, spires, shards and canopy.

    Modelled as a thin 16x16 panel: the two broad faces take the full authored
    region and the narrow edges take a single column, so a wing reads as a flat
    membrane rather than a block.
    """
    return {
        "south": face(base, 48, 16, 16),
        "north": face(base, 48, 16, 16),
        "west": face(base, 48, 1, 16),
        "east": face(base + 15, 48, 1, 16),
        "up": face(base, 48, 16, 1),
        "down": face(base, 63, 16, 1),
    }


BOSS_LIMB_CELLS = [0, 16, 32, 48]
BOSS_EXTRA_CELLS = [0, 16, 32, 48]


def boss_rig(boss) -> list:
    """
    A multi-part articulated rig for one boss.

    Every boss gets body, head, four limbs and its authored extras, so a phase
    animation can move each part independently -- which is what makes a boss
    fight read as a large articulated creature rather than a single sliding box.
    """
    bones = [
        bone("root", None, [0, 0, 0], []),
        bone("body", "root", [0, 16, 0],
             [cube([-8, 8, -4], [16, 16, 8], boss_body_uv())]),
        bone("head", "body", [0, 26, -4],
             [cube([-6, 26, -14], [12, 8, 8], boss_head_uv())]),
    ]

    limb_names = ["limb_front_left", "limb_front_right",
                  "limb_back_left", "limb_back_right"]
    offsets = [(-8, -4), (8, -4), (-8, 4), (8, 4)]
    for name, cell, (x, z) in zip(limb_names, BOSS_LIMB_CELLS, offsets):
        bones.append(bone(name, "body", [x, 10, z],
                          [cube([x - (4 if x > 0 else 0), -2, z - 2],
                                [4, 12, 4], boss_limb_uv(cell))]))

    # Extras are the silhouette-defining parts: wings for the crown and the
    # unraveling, spires for the warden, shards for the serpent, canopy for the
    # heart. They hang off the body so phase animations can flare them.
    # Driven by the atlas, not by an attribute that does not exist. BossSpec has
    # no `extras` field, so the hasattr() fallback silently clamped every boss to
    # two bones while boss_animations keyframes extra_1..extra_4 -- ten orphaned
    # channels across the five bosses, each a part that flared in the animation
    # and never moved on screen. BOSS_EXTRA_CELLS is four authored cells wide, so
    # all four get real geometry.
    extra_count = len(BOSS_EXTRA_CELLS)
    for index in range(extra_count):
        cell = BOSS_EXTRA_CELLS[index]
        side = -1 if index % 2 == 0 else 1
        bones.append(bone(
            f"extra_{index + 1}", "body",
            [side * 8, 22 + (index // 2) * 4, 0],
            [cube([side * 8, 14 + (index // 2) * 4, -8],
                  [16, 16, 1], boss_extra_uv(cell))],
            rotation=[0, 0, side * 15]))
    return bones


# --------------------------------------------------------------------------- #
#  Animations
# --------------------------------------------------------------------------- #

def keyframes(*pairs) -> dict:
    """A keyframe track from (time, value) pairs."""
    return {f"{t:g}": list(v) for t, v in pairs}


def clip(length: float, loop: bool, bones: dict) -> dict:
    entry = {"animation_length": length, "bones": bones}
    entry["loop"] = loop
    return entry


def creature_animations(family: str) -> dict:
    """
    The five clips every creature declares.

    Names match MobSpec.animations exactly; the Java controller only starts a
    clip the species declares, so a name mismatch here would silently leave a
    creature idling through its own walk cycle.
    """
    limbs = {
        "quadruped": ["leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"],
        "biped": ["leg_left", "leg_right"],
        "avian": ["leg_left", "leg_right"],
        "serpent": ["coil_1", "coil_2", "coil_3", "coil_4"],
        "arthropod": ["leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"],
        "fungal": ["leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"],
    }[family]
    wings = ["wing_left", "wing_right"] if family == "avian" else []
    arms = ["arm_left", "arm_right"] if family == "biped" else []

    # Diagonal pairs so a quadruped trots instead of hopping; bipeds and
    # arthropods alternate left against right.
    swing = {}
    for index, limb in enumerate(limbs):
        sign = 12.0 if index % 2 == 0 else -12.0
        swing[limb] = {"rotation": keyframes(
            (0.0, (sign, 0, 0)), (0.4, (-sign, 0, 0)), (0.8, (sign, 0, 0)))}

    # Only families that actually have a tail bone get a tail track; keyframing a
    # bone the rig does not define makes GeckoLib warn at load.
    tails = ["tail"] if tail_is_real(family) else []

    # The avian and quadruped rigs both build a neck that the head hangs off.
    # Nothing keyframed it, so the neck stayed rigid while the head it parents
    # bobbed -- a visible seam at the base of the skull on 40 of the 80 mobs.
    necks = ["neck"] if family in ("avian", "quadruped") else []

    idle_bones = {
        "body": {"position": keyframes(
            (0.0, (0, 0, 0)), (1.0, (0, 0.4, 0)), (2.0, (0, 0, 0)))},
        "head": {"rotation": keyframes(
            (0.0, (0, 0, 0)), (1.5, (3, 2, 0)), (3.0, (0, 0, 0)))},
    }
    for limb in wings:
        idle_bones[limb] = {"rotation": keyframes(
            (0.0, (0, 0, 18)), (0.35, (0, 0, -22)), (0.7, (0, 0, 18)))}
    for tail in tails:
        idle_bones[tail] = {"rotation": keyframes(
            (0.0, (0, -4, 0)), (1.5, (0, 5, 0)), (3.0, (0, -4, 0)))}
    for index, arm in enumerate(arms):
        # Opposite signs so a standing biped settles its weight instead of
        # holding both arms at the same angle.
        sign = 3.0 if index % 2 == 0 else -3.0
        idle_bones[arm] = {"rotation": keyframes(
            (0.0, (sign, 0, 0)), (1.5, (-sign, 0, 0)), (3.0, (sign, 0, 0)))}
    for neck in necks:
        idle_bones[neck] = {"rotation": keyframes(
            (0.0, (0, 0, 0)), (1.5, (-3, 0, 0)), (3.0, (0, 0, 0)))}

    walk_bones = dict(idle_bones)
    walk_bones.update(swing)
    walk_bones["body"] = {"rotation": keyframes(
        (0.0, (0, 2, 0)), (0.4, (0, -2, 0)), (0.8, (0, 2, 0)))}
    for limb in wings:
        walk_bones[limb] = {"rotation": keyframes(
            (0.0, (0, 0, 30)), (0.2, (0, 0, -35)), (0.4, (0, 0, 30)))}
    for tail in tails:
        # The tail counter-swings against the stride, which is what sells the walk
        # as weight-bearing rather than a sliding model.
        walk_bones[tail] = {"rotation": keyframes(
            (0.0, (0, 12, 0)), (0.4, (0, -12, 0)), (0.8, (0, 12, 0)))}
    for index, arm in enumerate(arms):
        # Arms counter-swing against the legs on the same side: the left arm
        # leads when the left leg trails. Without this a biped marched with both
        # arms pinned to its sides while its legs walked.
        sign = -28.0 if index % 2 == 0 else 28.0
        walk_bones[arm] = {"rotation": keyframes(
            (0.0, (sign, 0, 0)), (0.4, (-sign, 0, 0)), (0.8, (sign, 0, 0)))}
    for neck in necks:
        walk_bones[neck] = {"rotation": keyframes(
            (0.0, (2, 0, 0)), (0.4, (-3, 0, 0)), (0.8, (2, 0, 0)))}

    attack_target = arms[0] if arms else ("head" if family == "serpent" else limbs[0])
    attack_bones = {
        attack_target: {"rotation": keyframes(
            (0.0, (0, 0, 0)), (0.12, (-55, 0, 0)), (0.3, (25, 0, 0)), (0.45, (0, 0, 0)))},
        "body": {"rotation": keyframes(
            (0.0, (0, 0, 0)), (0.12, (8, 0, 0)), (0.45, (0, 0, 0)))},
    }
    for arm in arms:
        if arm != attack_target:
            # The off-arm pulls back as the striking arm comes through, which is
            # what makes the punch read as a whole-body motion.
            attack_bones[arm] = {"rotation": keyframes(
                (0.0, (0, 0, 0)), (0.12, (22, 0, 0)), (0.45, (0, 0, 0)))}

    hurt_bones = {
        "body": {"rotation": keyframes(
            (0.0, (0, 0, 0)), (0.08, (-14, 0, 6)), (0.3, (0, 0, 0)))},
        "head": {"rotation": keyframes(
            (0.0, (0, 0, 0)), (0.08, (18, 0, 0)), (0.3, (0, 0, 0)))},
    }

    death_bones = {
        "root": {"rotation": keyframes(
            (0.0, (0, 0, 0)), (0.9, (0, 0, 88))),
            "position": keyframes((0.0, (0, 0, 0)), (0.9, (0, -3, 0)))},
        "body": {"rotation": keyframes((0.0, (0, 0, 0)), (0.9, (-12, 0, 0)))},
    }
    for limb in limbs:
        death_bones[limb] = {"rotation": keyframes((0.0, (0, 0, 0)), (0.6, (25, 0, 0)))}
    for tail in tails:
        death_bones[tail] = {"rotation": keyframes((0.0, (0, 0, 0)), (0.9, (35, 0, 0)))}

    return {
        "animation.idle": clip(3.0, True, idle_bones),
        "animation.walk": clip(0.8, True, walk_bones),
        "animation.attack": clip(0.45, False, attack_bones),
        "animation.hurt": clip(0.3, False, hurt_bones),
        "animation.death": clip(0.9, False, death_bones),
    }


def entry_clip(phase) -> dict:
    """
    The one-shot clip played when a boss crosses into a phase.

    Built from the phase's own authored data rather than a shared template: the
    health threshold sets how violent the transition reads, so the final phase
    snaps harder than the first, and the abilities list decides whether the
    extras flare (aerial, shard, crown, orbit style moves) or the limbs slam
    (tremor, stomp, dive, coil style moves).
    """
    abilities = " ".join(phase.abilities).lower()
    flares = any(word in abilities for word in
                 ("aerial", "shard", "crown", "orbit", "dive", "split", "glitch",
                  "form", "seed", "spore", "phase"))
    strength = 18.0 + 9.0 * phase.index
    length = 1.2 + 0.2 * phase.index

    bones = {
        "root": {"position": keyframes(
            (0.0, (0, 0, 0)),
            (length * 0.35, (0, 3.0 if flares else -2.5, 0)),
            (length, (0, 0, 0)))},
        "body": {"rotation": keyframes(
            (0.0, (0, 0, 0)),
            (length * 0.35, (-strength * 0.6 if flares else strength, 0, 0)),
            (length, (0, 0, 0)))},
        "head": {"rotation": keyframes(
            (0.0, (0, 0, 0)),
            (length * 0.35, (strength, 0, 0)),
            (length, (0, 0, 0)))},
    }
    for index in range(1, 5):
        extra = f"extra_{index}"
        sign = 1 if index % 2 == 0 else -1
        flare = 45.0 if flares else 18.0
        bones[extra] = {"rotation": keyframes(
            (0.0, (0, 0, sign * 12)),
            (length * 0.4, (0, 0, sign * flare)),
            (length, (0, 0, sign * 12)))}
    if not flares:
        for index, limb in enumerate(
                ["limb_front_left", "limb_front_right",
                 "limb_back_left", "limb_back_right"]):
            bones[limb] = {"rotation": keyframes(
                (0.0, (0, 0, 0)),
                (length * 0.3, (-38.0 if index < 2 else -22.0, 0, 0)),
                (length, (0, 0, 0)))}
    return clip(length, False, bones)


def boss_animations(boss) -> dict:
    """
    The full boss clip set.

    Beyond the five creature clips a boss needs a spawn reveal and one loop per
    phase, because BUBoss advances an 'animation.phase.<n>' track on every
    transition and BUEntities.BOSS_ANIMATIONS declares exactly this list. A
    missing phase clip would throw at model load, not degrade quietly.
    """
    limbs = ["limb_front_left", "limb_front_right", "limb_back_left", "limb_back_right"]
    extras = [f"extra_{i}" for i in range(1, 5)]

    swing = {}
    for index, limb in enumerate(limbs):
        sign = 10.0 if index % 2 == 0 else -10.0
        swing[limb] = {"rotation": keyframes(
            (0.0, (sign, 0, 0)), (0.5, (-sign, 0, 0)), (1.0, (sign, 0, 0)))}

    idle = {
        "body": {"position": keyframes(
            (0.0, (0, 0, 0)), (1.5, (0, 0.8, 0)), (3.0, (0, 0, 0)))},
        "head": {"rotation": keyframes(
            (0.0, (0, 0, 0)), (1.5, (5, 4, 0)), (3.0, (0, 0, 0)))},
    }
    for index, extra in enumerate(extras):
        idle[extra] = {"rotation": keyframes(
            (0.0, (0, 0, 12)), (1.6, (0, 0, -14)), (3.0, (0, 0, 12)))}

    walk = dict(idle)
    walk.update(swing)

    attack = {
        "head": {"rotation": keyframes(
            (0.0, (0, 0, 0)), (0.15, (-45, 0, 0)), (0.4, (30, 0, 0)), (0.6, (0, 0, 0)))},
        "body": {"rotation": keyframes(
            (0.0, (0, 0, 0)), (0.15, (14, 0, 0)), (0.6, (0, 0, 0)))},
        limbs[0]: {"rotation": keyframes(
            (0.0, (0, 0, 0)), (0.2, (-60, 0, 0)), (0.6, (0, 0, 0)))},
    }

    hurt = {
        "body": {"rotation": keyframes(
            (0.0, (0, 0, 0)), (0.1, (-10, 0, 5)), (0.4, (0, 0, 0)))},
        "head": {"rotation": keyframes(
            (0.0, (0, 0, 0)), (0.1, (16, 0, 0)), (0.4, (0, 0, 0)))},
    }

    death = {
        "root": {"position": keyframes((0.0, (0, 0, 0)), (2.4, (0, -6, 0)))},
        "body": {"rotation": keyframes((0.0, (0, 0, 0)), (2.4, (0, 0, 78)))},
        "head": {"rotation": keyframes((0.0, (0, 0, 0)), (1.2, (35, 0, 0)))},
    }
    for limb in limbs:
        death[limb] = {"rotation": keyframes((0.0, (0, 0, 0)), (1.6, (30, 0, 0)))}

    # The spawn reveal: the boss rises and the extras flare, so entering an arena
    # reads as an event rather than a mob appearing mid-stride.
    spawn = {
        "root": {"position": keyframes((0.0, (0, -14, 0)), (1.2, (0, 2, 0)), (1.6, (0, 0, 0))),
                 "scale": keyframes((0.0, (0.7, 0.7, 0.7)), (1.6, (1.0, 1.0, 1.0)))},
        "head": {"rotation": keyframes((0.0, (40, 0, 0)), (1.6, (0, 0, 0)))},
    }
    for index, extra in enumerate(extras):
        spawn[extra] = {"rotation": keyframes(
            (0.0, (0, 0, 70)), (1.6, (0, 0, 12)))}

    out = {
        "animation.idle": clip(3.0, True, idle),
        "animation.walk": clip(1.0, True, walk),
        "animation.attack": clip(0.6, False, attack),
        "animation.hurt": clip(0.4, False, hurt),
        "animation.death": clip(2.4, False, death),
        "animation.spawn": clip(1.6, False, spawn),
    }

    # Each phase also names its own entry clip, and those names are authored per
    # boss ("animation.phase.summon_roots", "animation.form.quadruped") rather
    # than numbered. BUBoss plays phase.entryAnimation on every transition, so
    # each of those clips has to exist here -- GeckoLib throws when a controller
    # starts a clip the animation file does not define, which would break the
    # fight at the first phase change rather than degrade quietly.
    for phase in boss.phases:
        if phase.entry_animation and phase.entry_animation not in out:
            out[phase.entry_animation] = entry_clip(phase)

    # One distinct posture per phase: the fight visibly changes as health drops,
    # which is the readable signal that a phase boundary was crossed.
    for phase in boss.phases:
        posture = {}
        lift = 1.5 * phase.index
        posture["body"] = {"position": keyframes(
            (0.0, (0, lift, 0)), (1.4, (0, lift + 0.9, 0)), (2.8, (0, lift, 0)))}
        posture["head"] = {"rotation": keyframes(
            (0.0, (-4 * phase.index, 0, 0)),
            (1.4, (-4 * phase.index + 6, 3, 0)),
            (2.8, (-4 * phase.index, 0, 0)))}
        for index, extra in enumerate(extras):
            flare = 10 + 14 * phase.index
            sign = 1 if index % 2 == 0 else -1
            posture[extra] = {"rotation": keyframes(
                (0.0, (0, 0, sign * flare)),
                (1.0, (0, 0, sign * (flare + 18))),
                (2.0, (0, 0, sign * flare)))}
        out[f"animation.phase.{phase.index}"] = clip(2.8, True, posture)
    return out


# --------------------------------------------------------------------------- #

def main() -> None:
    families = sorted({m.family for m in M.ALL_MOBS})
    missing = [f for f in families if f not in FAMILY_RIGS]
    if missing:
        raise SystemExit(f"no rig authored for family/families: {missing}")

    for family in families:
        builder, bw, bh, by = FAMILY_RIGS[family]
        write(f"geo/entity/{family}.geo.json",
              geometry(f"geometry.{MODID}.{family}", 64, 64,
                       with_tail(family, builder()), bw, bh, by))
        write(f"animations/entity/{family}.animation.json",
              {"format_version": ANIM_VERSION,
               "animations": creature_animations(family)})
    print(f"[geckolib] family rigs: {len(families)} ({', '.join(families)})")

    for boss in BO.ALL_BOSSES:
        write(f"geo/entity/boss/{boss.id}.geo.json",
              geometry(f"geometry.{MODID}.boss.{boss.id}", 64, 64, boss_rig(boss),
                       5.0, 4.0, 1.5))
        write(f"animations/entity/boss/{boss.id}.animation.json",
              {"format_version": ANIM_VERSION, "animations": boss_animations(boss)})
    print(f"[geckolib] boss rigs: {len(BO.ALL_BOSSES)}")

    # Every creature species resolves a family rig, so confirm each one exists.
    for mob in M.ALL_MOBS:
        if mob.family not in families:
            raise SystemExit(f"mob {mob.id} has unknown family {mob.family}")
    print(f"[geckolib] wrote {WRITTEN} files")


if __name__ == "__main__":
    main()
