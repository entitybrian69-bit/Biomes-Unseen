"""
pixelart/creature_maps.py -- Hand-authored 64x64 GeckoLib UV atlases.

Every mob in Biomes Unseen uses a real GeckoLib `.geo.json` (Golden Rule #2:
no CubeListBuilder, no ModelPart). This file is the matching artwork: an
authored 64x32 texture atlas whose cells line up 1:1 with the boxes declared
in `resources/assets/biomesunseen/geo/entity/*.geo.json`.

ATLAS LAYOUT (u = column, v = row). All boxes are UV-aligned to 8px cells so
no cell ever straddles two body parts:

    HEAD box (8w x 7h x 8d), geo uv(0,0)
        u0..7    v0..5    head right   (-x)
        u8..15   v0..5    head front   (+z)  <- eyes, muzzle
        u16..23  v0..5    head left    (+x)
        u24..31  v0..5    head back    (-z)
        u8..15   v6..13   head top     (+y)  <- crown, ears, mane parting
        u16..23  v6..13   head bottom  (-y)  <- jaw, deep occlusion

    TORSO box (8w x 12h x 16d), geo uv(0,14)
        u32..47  v0..7    torso right  (-x)
        u48..63  v0..7    torso front  (+z)  <- chest, lighter belly
        u32..47  v8..15   torso back   (-z)  <- spine, mane
        u48..63  v8..15   torso top    (+y)  <- shoulder line, key light

    LIMBS (4w x 10h x 4d)
        front_left  geo uv(0,26)  -> u0..15   v16..29
        front_right geo uv(20,26) -> u16..31  v16..29
        back_left   geo uv(36,26) -> u32..47  v16..29
        back_right  geo uv(52,26) -> u48..63  v16..29
        per limb: u+0..3 right, u+4..7 front, u+8..11 left, u+12..15 back
        v16..25 the 10px leg, v26..29 occluded root / unused

    TAIL (3w x 12h x 3d), composed at u0..11 / v34..45 in its own band
        u0..2  right (-x) | u3..5 front (+z) | u6..8 left (+x) | u9..11 back (-z)
        The atlas is 64 rows tall so this band is free: at 32 rows the tail had
        to overwrite the front-right and back-left limb cells.

Rows are composed from named region segments (constants of an exact width)
concatenated left to right. The composition order is asserted at import time
via _seg(), so a mis-counted region fails loudly instead of silently shifting
art onto the wrong body part.

Glyph vocabulary
----------------
    H  specular highlight        L  key light (top-left)
    M  mid hide / fur / chitin   D  form shadow
    S  ambient occlusion         O  1px outline
    A  accent (mane, markings)   a  accent shadow
    E  eye sclera/lens           e  pupil / emissive eye
    B  bone, horn, tusk          b  bone shadow
    G  bioluminescent marking    g  glow falloff
    T  membrane / translucent    W  wet or slick specular
    .  transparent (only in rows 30..31 and outside silhouettes)
"""

from __future__ import annotations

from typing import Dict, List

ATLAS_W = 64
# 64 rows rather than 32. At 32 the atlas was fully subscribed -- head and torso
# occupied v0..15, the four limb cells v16..25 and their occlusion roots v26..29,
# leaving only two spare rows -- so the tail had nowhere to live and was patched
# over the front-right and back-left limb cells at u24..35, corrupting two legs
# to gain one tail. The extra band v32..63 is tail space and nothing else.
ATLAS_H = 64

# Where the tail is composed: four 3-column faces side by side, 12 rows tall.
TAIL_U = 0
TAIL_V = 34


def _seg(text: str, width: int, label: str) -> str:
    """Width guard so a hand-authored region can never shift the atlas."""
    if len(text) != width:
        raise ValueError(f"creature atlas segment {label}: expected {width} glyphs, got {len(text)} :: {text}")
    return text


# Region widths (columns)
HW_R, HW_F, HW_L, HW_B = 8, 8, 8, 8            # head sides: 32 cols
TT_R, TT_F, TT_L, TT_B = 16, 16, 16, 16        # torso: 32 + 32 cols
LEG = 16                                        # one limb block
TAIL_W = 12                                     # tail: 3+3+3+3
GAP2, GAP3 = 2, 3                               # column gutters


def _atlas(
    name: str,
    head_side_r: List[str], head_side_f: List[str],
    head_side_l: List[str], head_side_b: List[str],
    head_top: List[str], head_bottom: List[str],
    torso_r: List[str], torso_f: List[str],
    torso_b: List[str], torso_t: List[str],
    limb_fl: List[str], limb_fr: List[str],
    limb_bl: List[str], limb_br: List[str],
    tail_r: List[str], tail_f: List[str],
    tail_l: List[str], tail_b: List[str],
) -> List[str]:
    """
    Assemble the 64x32 atlas from authored region blocks.

    Every region is a list of authored strings of the documented width. This
    function only concatenates and pads -- it never invents a pixel.
    """
    rows: List[str] = []

    # ---- v0..v7 : head sides (32 cols) + torso right (16) + torso front (16)
    for i in range(8):
        rows.append(
            _seg(head_side_r[i], HW_R, f"{name}.head_right[{i}]")
            + _seg(head_side_f[i], HW_F, f"{name}.head_front[{i}]")
            + _seg(head_side_l[i], HW_L, f"{name}.head_left[{i}]")
            + _seg(head_side_b[i], HW_B, f"{name}.head_back[{i}]")
            + _seg(torso_r[i], TT_R, f"{name}.torso_right[{i}]")
            + _seg(torso_f[i], TT_F, f"{name}.torso_front[{i}]")
        )

    # ---- v8..v13 : head top (16) + head bottom (16) + torso back (16) + torso top (16)
    for i in range(6):
        rows.append(
            _seg(head_top[i], HW_F + HW_L, f"{name}.head_top[{i}]")
            + _seg(head_bottom[i], HW_B + HW_R, f"{name}.head_bottom[{i}]")
            + _seg(torso_b[i], TT_R, f"{name}.torso_back[{i}]")
            + _seg(torso_t[i], TT_F, f"{name}.torso_top[{i}]")
        )
    # ---- v14..v15 : head top/bottom rows 6..7 + torso back/top rows 6..7 + tail root
    for i in range(2):
        rows.append(
            _seg(head_top[6 + i], HW_F + HW_L, f"{name}.head_top[{6+i}]")
            + _seg(head_bottom[6 + i], HW_B + HW_R, f"{name}.head_bottom[{6+i}]")
            + _seg(torso_b[6 + i], TT_R, f"{name}.torso_back[{6+i}]")
            + _seg(torso_t[6 + i], TT_F, f"{name}.torso_top[{6+i}]")
        )

    # ---- v16..v25 : four limbs (16 cols each) = 64
    for i in range(10):
        rows.append(
            _seg(limb_fl[i], LEG, f"{name}.limb_fl[{i}]")
            + _seg(limb_fr[i], LEG, f"{name}.limb_fr[{i}]")
            + _seg(limb_bl[i], LEG, f"{name}.limb_bl[{i}]")
            + _seg(limb_br[i], LEG, f"{name}.limb_br[{i}]")
        )

    # ---- v26..v29 : limb root occlusion rows
    for i in range(4):
        rows.append(
            _seg(limb_fl[10 + i], LEG, f"{name}.limb_fl_root[{i}]")
            + _seg(limb_fr[10 + i], LEG, f"{name}.limb_fr_root[{i}]")
            + _seg(limb_bl[10 + i], LEG, f"{name}.limb_bl_root[{i}]")
            + _seg(limb_br[10 + i], LEG, f"{name}.limb_br_root[{i}]")
        )

    # ---- v30..v63 : tail band, then unused (kept transparent so mipmapping
    #                 never bleeds into the rows above)
    while len(rows) < ATLAS_H:
        rows.append("." * ATLAS_W)

    # Compose the tail into its own band. Each of the four faces is authored 3
    # columns by 12 rows, laid side by side with no gutter, which matches the
    # geometry the tail bone declares -- so no face is stretched and no other
    # body part's artwork is overwritten.
    tail_blocks = (tail_r, tail_f, tail_l, tail_b)
    out = [list(r) for r in rows]
    for v in range(12):
        for bi, block in enumerate(tail_blocks):
            for c in range(3):
                glyph = block[v][c]
                if glyph == ".":
                    continue
                col = TAIL_U + bi * 3 + c
                out[TAIL_V + v][col] = glyph
    final = ["".join(r) for r in out]

    for i, r in enumerate(final):
        if len(r) != ATLAS_W:
            raise ValueError(f"{name}: atlas row {i} is {len(r)} wide, expected {ATLAS_W}")
    if len(final) != ATLAS_H:
        raise ValueError(f"{name}: atlas is {len(final)} rows tall, expected {ATLAS_H}")
    return final


def _limb_block(right: List[str], front: List[str], left: List[str], back: List[str],
                root: List[str] | None = None) -> List[str]:
    """
    Compose the 16-column limb cell from four authored 4-column faces.

    A GeckoLib limb box is 4w x 10h x 4d, so each face unwraps to exactly 4
    columns and the cell holds four faces with NO gutter:
        u+0..3 right (-x) | u+4..7 front (+z) | u+8..11 left (+x) | u+12..15 back (-z)

    `root` supplies the four v26..v29 rows of occlusion where the limb meets
    the torso; if omitted, a hand-authored default occlusion band is used.
    """
    for label, face in (("right", right), ("front", front), ("left", left), ("back", back)):
        if len(face) != 10:
            raise ValueError(f"limb {label}: expected 10 authored rows, got {len(face)}")
        for i, r in enumerate(face):
            if len(r) != 4:
                raise ValueError(f"limb {label} row {i}: expected 4 glyphs, got {len(r)} :: {r}")
    rows = [right[i] + front[i] + left[i] + back[i] for i in range(10)]
    if root is None:
        root = [
            "OSSSSSSSSSSSSSSO",
            "OSDDDDDDDDDDDDSO",
            "OOSSSSSSSSSSSSOO",
            "OOOOOOOOOOOOOOOO",
        ]
    if len(root) != 4:
        raise ValueError(f"limb root: expected 4 rows, got {len(root)}")
    for i, r in enumerate(root):
        if len(r) != 16:
            raise ValueError(f"limb root row {i}: expected 16 glyphs, got {len(r)} :: {r}")
    rows += list(root)
    return rows


DEFAULT_LIMB_ROOT = [
    "OSSSSSSSSSSSSSSO",
    "OSDDDDDDDDDDDDSO",
    "OOSSSSSSSSSSSSOO",
    "OOOOOOOOOOOOOOOO",
]


# ===========================================================================
#  FAMILY 1 -- QUADRUPED  (prowlers, stags, herds: fur, mane, hooves/claws)
# ===========================================================================

_QUAD_HEAD_R = [
    "OOOOOOOO",
    "OHHLLLLL",
    "OHLLLLLM",
    "OHMLMMMM",
    "OMMMMDDD",
    "OMMDDDDD",
    "OSSSSSSS",
    "OOOOOOOO",
]
_QUAD_HEAD_F = [
    "OOOOOOOO",
    "OHHHHLLO",
    "OHEeEeLO",
    "OHLLMLLO",
    "OMMMBMMO",
    "OMMBBMMO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_QUAD_HEAD_L = [
    "OOOOOOOO",
    "LLLLLHHO",
    "MLLLLLOH",
    "MMMMMLMO",
    "DDDDMMMM",
    "DDDDDDMM",
    "SSSSSSSS",
    "OOOOOOOO",
]
_QUAD_HEAD_B = [
    "OOOOOOOO",
    "OAAHHHHO",
    "OAALLLLO",
    "OAALLLLO",
    "ODDLLLLO",
    "ODDDDLLO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_QUAD_HEAD_TOP = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHHO",
    "OAHLLLLLLLLLLLAO",
    "OAALLLLLLLLLLAAO",
    "ODLLMMMMMMMMMLOO",
    "ODDMMMMMMMMMMDSO",
    "ODSSSSSSSSSSSSOO",
    "OOOOOOOOOOOOOOOO",
]
_QUAD_HEAD_BOT = [
    "OOOOOOOOOOOOOOOO",
    "OSSSSSSSSSSSSSSO",
    "OSSDDDDDDDDDDSSO",
    "OSDDDDDDDDDDDDSO",
    "OSDDBBBBBBBBDDSO",
    "OSSDBBBBBBBDSSSO",
    "OOSSSSSSSSSSSSOO",
    "OOOOOOOOOOOOOOOO",
]
_QUAD_TORSO_R = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHDO",
    "OALLLLLLLLLLLLDO",
    "OALMMMMMMMMMMMDO",
    "OAMMMMMMMMMMMMDO",
    "ODMMMMMMMMMMMDDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]
_QUAD_TORSO_F = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHDO",
    "OALLWWWWWWWWLLDO",
    "OALMWWWWWWWWMDDO",
    "OMMMWWWWWWWWMMDO",
    "ODMMWWWWWWWWMMDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]
_QUAD_TORSO_B = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAADO",
    "OALLLLLLLLLLLLDO",
    "OALLMMMMMMMMMLDO",
    "ODLMMMMMMMMMMDDO",
    "ODDMMMMMMMMMDDDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]
_QUAD_TORSO_T = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHDO",
    "OAHHLLLLLLLLLLDO",
    "OAHLLLLLLLLLLLDO",
    "ODLLLLLLLLLLLLDO",
    "ODDLLLLLLLLLLDDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]


def _quad_limb(light_left: bool) -> List[str]:
    """
    Quadruped leg (4w x 10h x 4d). Darker at the root -- ambient occlusion
    where the leg meets the belly -- and a bone-coloured hoof at the tip.
    `light_left` flips the key light for the animal's left-hand side.
    """
    if light_left:
        right = ["OOOO", "OHHL", "OHLL", "OLLL", "OMLM", "OMMM", "OMDM", "ODDM", "OBBO", "OOOO"]
        left  = ["OOOO", "OLLH", "OLLH", "LLLH", "MLMO", "MMMO", "MDMO", "DDDO", "OBBO", "OOOO"]
    else:
        right = ["OOOO", "OLLH", "OLLH", "LLLH", "MLMO", "MMMO", "MDMO", "DDDO", "OBBO", "OOOO"]
        left  = ["OOOO", "OHHL", "OHLL", "OLLL", "OMLM", "OMMM", "OMDM", "ODDM", "OBBO", "OOOO"]
    front = ["OOOO", "OHLL", "OHLL", "OOLL", "MMLM", "MMMM", "MDMM", "DDDM", "OBBO", "OOOO"]
    back  = ["OOOO", "OSDD", "OSSD", "OSSD", "SDDM", "SDDD", "SDDD", "SSDD", "OSBO", "OOOO"]
    return _limb_block(right, front, left, back)



_QUAD_TAIL_R = [
    "OOO", "OAO", "OAO", "OAO", "OAO", "OAO",
    "OMO", "OMO", "OMM", "OMM", "OHO", "OOO",
]
_QUAD_TAIL_F = [
    "OOO", "OAO", "OAO", "OAO", "OAO", "OAO",
    "OMO", "OMO", "OMM", "OMM", "OHO", "OOO",
]
_QUAD_TAIL_L = [
    "OOO", "OAO", "OAO", "OAO", "OAO", "OAO",
    "OMO", "OMO", "OMM", "OMM", "OHO", "OOO",
]
_QUAD_TAIL_B = [
    "OOO", "OaO", "OaO", "OaO", "OaO", "OaO",
    "ODO", "ODO", "ODD", "ODD", "OHO", "OOO",
]


# ===========================================================================
#  FAMILY 2 -- ARTHROPOD  (chitin plates, segmented abdomen, many legs)
# ===========================================================================

_ARTHRO_HEAD_R = [
    "OOOOOOOO",
    "OHHHDDDO",
    "OHHDDDDO",
    "OHDDDDDO",
    "ODDDDDDO",
    "ODDDDDDO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_ARTHRO_HEAD_F = [
    "OOOOOOOO",
    "OHHHHLLO",
    "OHEeEeLO",
    "OHHLLHLO",
    "OBBOOBBO",
    "OBBOOBBO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_ARTHRO_HEAD_L = [
    "OOOOOOOO",
    "DDDHHHDO",
    "DDDDHHDO",
    "DDDDDHDO",
    "DDDDDDDO",
    "DDDDDDDO",
    "SSSSSSSO",
    "OOOOOOOO",
]
_ARTHRO_HEAD_B = [
    "OOOOOOOO",
    "OHHHHHHO",
    "OHDDDDHO",
    "ODDDDDDO",
    "ODDDDDDO",
    "ODDDDDDO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_ARTHRO_HEAD_TOP = [
    "OOOOOOOOOOOOOOOO",
    "OHHHHHHHHHHHHHHO",
    "OHHDDDDDDDDDDHHO",
    "OHDHHHHHHHHHHDHO",
    "OHDHHHHHHHHHHDHO",
    "OHDHHHHHHHHHHDHO",
    "ODDDDDDDDDDDDDDO",
    "OSSSSSSSSSSSSSSO",
]
_ARTHRO_HEAD_BOT = [
    "OOOOOOOOOOOOOOOO",
    "OSSSSSSSSSSSSSSO",
    "OSDDDDDDDDDDDDSO",
    "OSDBBBBBBBBBBDSO",
    "OSDBBBBBBBBBBDSO",
    "OSDDDDDDDDDDDDSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_ARTHRO_TORSO_R = [
    "OOOOOOOOOOOOOOOO",
    "OHHHHOOOHHHHOOOO",
    "OHHDDOOOHHDDOOOO",
    "OHDDDOOOHDDDOOOO",
    "ODDDDOOODDDDOOOO",
    "ODDDDOOODDDDOOOO",
    "OSSSSOOOSSSSOOOO",
    "OOOOOOOOOOOOOOOO",
]
_ARTHRO_TORSO_F = [
    "OOOOOOOOOOOOOOOO",
    "OHHHHHHHHHHHHHDO",
    "OHDDDDDDDDDDDDDO",
    "OHDGGDDDDDDGGDHO",
    "ODGGGDDDDDDGGGDO",
    "ODGGGDDDDDDGGGDO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_ARTHRO_TORSO_B = [
    "OOOOOOOOOOOOOOOO",
    "OHHHHHHHHHHHHHDO",
    "OHDDDDDDDDDDDDDO",
    "OHDDDDDDDDDDDDDO",
    "ODDDDDDDDDDDDDDO",
    "ODDDDDDDDDDDDDDO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_ARTHRO_TORSO_T = [
    "OOOOOOOOOOOOOOOO",
    "OHHHHHHHHHHHHHHO",
    "OHDDDDDDDDDDDDHO",
    "OHDHHHHHHHHHHDHO",
    "OHDHHHHHHHHHHDHO",
    "ODDDDDDDDDDDDDDO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]


def _arthro_limb() -> List[str]:
    """Spined arthropod leg: dark joint at the root, chitin highlight, tarsus."""
    face  = ["OOOO", "OSSO", "ODDO", "OHDO", "OHDO", "ODOO", "ODOO", "ODDO", "OSSO", "OOOO"]
    front = ["OOOO", "OSSO", "ODDO", "OHHO", "OHHO", "OHOO", "OHOO", "OHDO", "OSSO", "OOOO"]
    back  = ["OOOO", "OSSO", "OSDO", "OSDO", "OSDO", "OSDO", "OSDO", "OSSO", "OSSO", "OOOO"]
    return _limb_block(face, front, face, back)



_ARTHRO_TAIL_R = ["OOO", "ODO", "ODO", "ODO", "OHO", "OHO", "OMO", "OMO", "OMM", "OSS", "OSO", "OOO"]
_ARTHRO_TAIL_F = ["OOO", "ODO", "OHO", "OHO", "OHO", "OMO", "OMO", "OMM", "OMM", "OSS", "OSO", "OOO"]
_ARTHRO_TAIL_L = ["OOO", "ODO", "ODO", "OHO", "OHO", "OMO", "OMO", "OMM", "OMM", "OSS", "OSO", "OOO"]
_ARTHRO_TAIL_B = ["OOO", "ODO", "ODO", "ODO", "OHO", "OHO", "OMO", "OMO", "OMM", "OSS", "OSO", "OOO"]


# ===========================================================================
#  FAMILY 3 -- BIPED  (humanoid wardens, cultists, golems)
# ===========================================================================

_BIPED_HEAD_R = [
    "OOOOOOOO",
    "OHHLLLLL",
    "OHLLLLLM",
    "OHMLMMMM",
    "OMMMMDDD",
    "OMMDDDDD",
    "OSSSSSSS",
    "OOOOOOOO",
]
_BIPED_HEAD_F = [
    "OOOOOOOO",
    "OAHHHHAO",
    "OAHEeEAO",
    "OAHLHLAO",
    "OMMMMMMO",
    "OMMBBMMO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_BIPED_HEAD_L = [
    "OOOOOOOO",
    "LLLLLHHO",
    "MLLLLLOH",
    "MMMMMLMO",
    "DDDDMMMM",
    "DDDDDDMM",
    "SSSSSSSS",
    "OOOOOOOO",
]
_BIPED_HEAD_B = [
    "OOOOOOOO",
    "OAHHHHAO",
    "OALLLLAO",
    "OALLLLAO",
    "ODDDDDDO",
    "ODDDDDDO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_BIPED_HEAD_TOP = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAAO",
    "OAAHHHHHHHHHHAAO",
    "OAHLLLLLLLLLLHAO",
    "OAHLMMMMMMMMLHAO",
    "ODHMMMMMMMMMMHDO",
    "ODSSSSSSSSSSSSDO",
    "OOOOOOOOOOOOOOOO",
]
_BIPED_HEAD_BOT = [
    "OOOOOOOOOOOOOOOO",
    "OSSSSSSSSSSSSSSO",
    "OSDDDDDDDDDDDDSO",
    "OSDBBBBBBBBBBDSO",
    "OSDBBBBBBBBBBDSO",
    "OSDDDDDDDDDDDDSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_BIPED_TORSO_R = [
    "OOOOOOOOOOOOOOOO",
    "OHHHHHHHHHHHHHDO",
    "OHLLLLLLLLLLLLDO",
    "OHLLMMMMMMMMMLDO",
    "OHMMMMMMMMMMMMDO",
    "ODMMMMMMMMMMMDDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]
_BIPED_TORSO_F = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHAO",
    "OALLLLLLLLLLLLAO",
    "OALGGGGGGGGGGLAO",
    "OAMGGGGGGGGGGMAO",
    "ODMGGGGGGGGGGMDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]
_BIPED_TORSO_B = [
    "OOOOOOOOOOOOOOOO",
    "OHHHHHHHHHHHHHDO",
    "OHAAAAAAAAAAAADO",
    "OHALLLLLLLLLLADO",
    "ODALLLLLLLLLLADO",
    "ODDAAAAAAAAAADDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]
_BIPED_TORSO_T = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHAO",
    "OAHHHHHHHHHHHHAO",
    "OAALLLLLLLLLLAAO",
    "ODALLLLLLLLLLADO",
    "ODDAAAAAAAAAADDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]


def _biped_limb(arm: bool) -> List[str]:
    """Humanoid limb: an arm carries a pauldron cap, a leg ends in a foot."""
    if arm:
        right = ["OOOO", "OBBO", "OHHL", "OHLL", "OLLL", "OMLM", "OMMM", "ODDM", "OBBO", "OOOO"]
        front = ["OOOO", "OBBO", "OHLL", "OHLL", "OLLM", "MLMM", "MMMM", "MDMM", "OBBO", "OOOO"]
        left  = right
    else:
        right = ["OOOO", "OHHL", "OHLL", "OLLL", "OMLM", "OMMM", "OMDM", "ODDM", "OBBO", "OOOO"]
        front = ["OOOO", "OHLL", "OHLL", "OOLL", "MMLM", "MMMM", "MDMM", "DDDM", "OBBO", "OOOO"]
        left  = right
    back = ["OOOO", "OSBO", "OSDL", "OSSD", "OSSD", "SDDM", "SDDD", "SSDD", "OSBO", "OOOO"]
    return _limb_block(right, front, left, back)



_BIPED_TAIL_R = ["OOO"] * 12
_BIPED_TAIL_F = ["OOO"] * 12
_BIPED_TAIL_L = ["OOO"] * 12
_BIPED_TAIL_B = ["OOO"] * 12


# ===========================================================================
#  FAMILY 4 -- SERPENT  (coiled body, no limbs: limb cells carry body coils)
# ===========================================================================

_SERP_HEAD_R = [
    "OOOOOOOO",
    "OHHHDDDO",
    "OHHLDDDO",
    "OHLLDDDO",
    "OLLLDDDO",
    "OMMMDDDO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_SERP_HEAD_F = [
    "OOOOOOOO",
    "OAHHHHAO",
    "OEeHHeO.",
    "OAHLHLAO",
    "OBBBBBBO",
    "OBbBbBbO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_SERP_HEAD_L = [
    "OOOOOOOO",
    "DDDHHHHO",
    "DDDHLHHO",
    "DDDHLHHO",
    "DDDLLLLO",
    "DDDMMMLO",
    "SSSSSSSO",
    "OOOOOOOO",
]
_SERP_HEAD_B = [
    "OOOOOOOO",
    "OAHHHHAO",
    "OALLLLAO",
    "OALLLLAO",
    "ODDDDDDO",
    "ODDDDDDO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_SERP_HEAD_TOP = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHHO",
    "OAHHLLLLLLLLLAHO",
    "OAHLLLLLLLLLLHAO",
    "OAHLMMMMMMMMLHAO",
    "ODHMMMMMMMMMMHDO",
    "ODDSSSSSSSSSSDDO",
    "OOOOOOOOOOOOOOOO",
]
_SERP_HEAD_BOT = [
    "OOOOOOOOOOOOOOOO",
    "OSSSSSSSSSSSSSSO",
    "OSDDDDDDDDDDDDSO",
    "OSDBBBBBBBBBBDSO",
    "OSDBbBbBbBbBbDSO",
    "OSDDDDDDDDDDDDSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_SERP_TORSO_R = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHAO",
    "OALLLLLLLLLLLLAO",
    "OALLMMMMMMMMMLAO",
    "ODLMMMMMMMMMMDDO",
    "ODDMMMMMMMMMDDDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]
_SERP_TORSO_F = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHAO",
    "OAGGLLLLLLLLGGAO",
    "OAGGLMMMMMMGGGAO",
    "ODGGLMMMMMMGGGDO",
    "ODDDMMMMMMMDDDDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]
_SERP_TORSO_B = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAADO",
    "OALLLLLLLLLLLLDO",
    "OALLMMMMMMMMMLDO",
    "ODLMMMMMMMMMMDDO",
    "ODDMMMMMMMMMDDDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]
_SERP_TORSO_T = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHDO",
    "OAHHLLLLLLLLLLDO",
    "OAHHLLLLLLLLLLDO",
    "ODHHLLLLLLLLLLDO",
    "ODDLLLLLLLLLLDDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]


def _serp_coil() -> List[str]:
    """
    Serpents have no limbs, so the four limb cells carry coiled body rings
    (the geo chains them parent->child to build the segmented spine). Each
    ring is a scaled band with a belly plate and occlusion where it meets the
    previous ring.
    """
    face  = ["OOOO", "OSSO", "OHHL", "OHLL", "OOLL", "OMLM", "OMMM", "ODDM", "OSSO", "OOOO"]
    front = ["OOOO", "OSSO", "OBBO", "OBBO", "OBBO", "OBBO", "OMMO", "ODDO", "OSSO", "OOOO"]
    back  = ["OOOO", "OSSO", "OSDO", "OSDO", "OSDO", "SDDO", "SDDO", "SSDO", "OSSO", "OOOO"]
    return _limb_block(face, front, face, back)



_SERP_TAIL_R = ["OOO", "OAO", "OAO", "OAO", "OMO", "OMO", "OMO", "OMM", "OMM", "OHO", "OHO", "OOO"]
_SERP_TAIL_F = ["OOO", "OAO", "OAO", "OAO", "OMO", "OMO", "OMO", "OMM", "OMM", "OHO", "OHO", "OOO"]
_SERP_TAIL_L = ["OOO", "OAO", "OAO", "OAO", "OMO", "OMO", "OMO", "OMM", "OMM", "OHO", "OHO", "OOO"]
_SERP_TAIL_B = ["OOO", "OaO", "OaO", "OaO", "ODO", "ODO", "ODO", "ODD", "ODD", "OHO", "OHO", "OOO"]


# ===========================================================================
#  FAMILY 5 -- AVIAN  (wing cells replace the rear limbs)
# ===========================================================================

_AVIAN_HEAD_R = [
    "OOOOOOOO",
    "OAHHHHHO",
    "OAHLLLLO",
    "OAHHLLLO",
    "OHLLLLLO",
    "OMLLLLDO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_AVIAN_HEAD_F = [
    "OOOOOOOO",
    "OAHHHHAO",
    "OHEeEeHO",
    "OAHHHHAO",
    "OBBBBBBO",
    "OBbBbBbO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_AVIAN_HEAD_L = [
    "OOOOOOOO",
    "OHHHHHAO",
    "OLLLLLAO",
    "OLLHHHAO",
    "OLLLLLHO",
    "ODLLLLMO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_AVIAN_HEAD_B = [
    "OOOOOOOO",
    "OAHHHHAO",
    "OALLLLAO",
    "OALLLLAO",
    "ODDDDDDO",
    "ODDDDDDO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_AVIAN_HEAD_TOP = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHHO",
    "OAHHHHHHHHHHHHHO",
    "OAHLLLLLLLLLLHAO",
    "OAHLMMMMMMMMLHAO",
    "ODHMMMMMMMMMMHDO",
    "ODDSSSSSSSSSSDDO",
    "OOOOOOOOOOOOOOOO",
]
_AVIAN_HEAD_BOT = [
    "OOOOOOOOOOOOOOOO",
    "OSSSSSSSSSSSSSSO",
    "OSDDDDDDDDDDDDSO",
    "OSDBBBBBBBBBBDSO",
    "OSDBBBBBBBBBBDSO",
    "OSDDDDDDDDDDDDSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_AVIAN_TORSO_R = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHAO",
    "OATTTTTTTTTTTTAO",
    "OATTTTTTTTTTTTAO",
    "ODTTTTTTTTTTTDDO",
    "ODDTTTTTTTTTDDDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]
_AVIAN_TORSO_F = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHAO",
    "OALLLLLLLLLLLLAO",
    "OALLWWWWWWWLLLAO",
    "ODLLWWWWWWWLLLLO",
    "ODDLLWWWWWLLLLDD",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]
_AVIAN_TORSO_B = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAADO",
    "OATTTTTTTTTTTADO",
    "OATTTTTTTTTTTADO",
    "ODTTTTTTTTTTTDDO",
    "ODDTTTTTTTTTDDDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]
_AVIAN_TORSO_T = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHAO",
    "OATTTTTTTTTTTTAO",
    "OATTTTTTTTTTTTAO",
    "ODTTTTTTTTTTTDDO",
    "ODDTTTTTTTTTDDDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]


def _avian_leg() -> List[str]:
    """Bird leg: thin, scaly, three-toed foot at the base."""
    face  = ["OOOO", "OSSO", "OHBO", "OHBO", "OBBO", "OBBO", "OBbO", "OBbO", "OBBO", "OOOO"]
    front = ["OOOO", "OSSO", "OHBO", "OBBO", "OBBO", "OBbO", "OBbO", "OBbO", "OBBO", "OOOO"]
    back  = ["OOOO", "OSSO", "OSBO", "OSBO", "OSBO", "OSBO", "OSBO", "OSBO", "OSBO", "OOOO"]
    return _limb_block(face, front, face, back)



def _avian_wing() -> List[str]:
    """
    Folded wing: primary feathers run down the outer face with a specular
    leading edge (top-left key light) and deep occlusion between the vanes.
    """
    face  = ["OOOO", "OAHO", "OAHO", "OAHO", "OTHO", "OTHO", "OTDO", "OTDO", "OTDO", "OOOO"]
    front = ["OOOO", "OAHO", "OAHO", "OOTO", "OOTO", "OODO", "OODO", "OODO", "OSSO", "OOOO"]
    back  = ["OOOO", "OSSO", "OSSO", "OSSO", "OSSO", "OSDO", "OSDO", "OSDO", "OSSO", "OOOO"]
    return _limb_block(face, front, face, back)



_AVIAN_TAIL_R = ["OOO", "OAO", "OAO", "OTO", "OTO", "OTO", "OTO", "OTO", "ODO", "ODO", "ODO", "OOO"]
_AVIAN_TAIL_F = ["OOO", "OAO", "OTO", "OTO", "OTO", "OTO", "OTO", "OTO", "ODO", "ODO", "ODO", "OOO"]
_AVIAN_TAIL_L = ["OOO", "OAO", "OAO", "OTO", "OTO", "OTO", "OTO", "OTO", "ODO", "ODO", "ODO", "OOO"]
_AVIAN_TAIL_B = ["OOO", "OaO", "OaO", "OTO", "OTO", "OTO", "OTO", "OTO", "ODO", "ODO", "ODO", "OOO"]


# ===========================================================================
#  FAMILY 6 -- FUNGAL / ELEMENTAL  (soft cap body, emissive gills, no bones)
# ===========================================================================

_FUNG_HEAD_R = [
    "OOOOOOOO",
    "OHHHDDDO",
    "OHHHDDDO",
    "OHGGDDDO",
    "OGGGDDDO",
    "OGGGDDDO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_FUNG_HEAD_F = [
    "OOOOOOOO",
    "OHHHHHHO",
    "OHGGGGHO",
    "OHEeEeHO",
    "OGGGGGGO",
    "OGgGgGgO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_FUNG_HEAD_L = [
    "OOOOOOOO",
    "DDDHHHHO",
    "DDDGHHHO",
    "DDDGHHHO",
    "DDDGGGGO",
    "DDDGGGGO",
    "SSSSSSSO",
    "OOOOOOOO",
]
_FUNG_HEAD_B = [
    "OOOOOOOO",
    "OHHHHHHO",
    "OHGGGGHO",
    "OGGGGGGO",
    "OGGGGGGO",
    "OGgGgGgO",
    "OSSSSSSO",
    "OOOOOOOO",
]
_FUNG_HEAD_TOP = [
    "OOOOOOOOOOOOOOOO",
    "OHHHHHHHHHHHHHHO",
    "OHHHHGGGGGGHHHHO",
    "OHHHGGGGGGGGHHHO",
    "OHGGGGGGGGGGGGHO",
    "OHGGGgGGGGgGGGHO",
    "ODSSSSSSSSSSSSDO",
    "OOOOOOOOOOOOOOOO",
]
_FUNG_HEAD_BOT = [
    "OOOOOOOOOOOOOOOO",
    "OSSSSSSSSSSSSSSO",
    "OSGGGGGGGGGGGGSO",
    "OSGgGgGgGgGgGgSO",
    "OSGGGGGGGGGGGGSO",
    "OSGgGgGgGgGgGgSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_FUNG_TORSO_R = [
    "OOOOOOOOOOOOOOOO",
    "OHHHHHHHHHHHHHDO",
    "OHHHGGGGGGGGHHDO",
    "OHGGGGGGGGGGGHDO",
    "OGGGGgGGGGgGGGDO",
    "ODGGGGGGGGGGGDDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]
_FUNG_TORSO_F = [
    "OOOOOOOOOOOOOOOO",
    "OHHHHHHHHHHHHHHO",
    "OHHGGGGGGGGGGHHO",
    "OHGGGGGGGGGGGGHO",
    "OGGGgGGGGGGgGGGO",
    "ODGGGGGGGGGGGGDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]
_FUNG_TORSO_B = [
    "OOOOOOOOOOOOOOOO",
    "OHHHHHHHHHHHHHDO",
    "OHHHGGGGGGGGHHDO",
    "OHGGGGGGGGGGGHDO",
    "OGGGGGGGGGGGGGDO",
    "ODGGGGGGGGGGGDDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]
_FUNG_TORSO_T = [
    "OOOOOOOOOOOOOOOO",
    "OHHHHHHHHHHHHHHO",
    "OHHHGGGGGGGGHHHO",
    "OHGGGGGGGGGGGGHO",
    "OGGGGGGGGGGGGGGO",
    "ODGGGGGGGGGGGGDO",
    "ODDSSSSSSSSSDDDO",
    "OOOOOOOOOOOOOOOO",
]


def _fungal_limb() -> List[str]:
    """Soft stalk limb: no bone, glowing gill band, occluded root."""
    face  = ["OOOO", "OHGO", "OHGO", "OGGO", "OGGO", "OGgO", "OGgO", "ODDO", "OSSO", "OOOO"]
    front = ["OOOO", "OHGO", "OGGO", "OGGO", "OGgO", "OGgO", "OGgO", "ODDO", "OSSO", "OOOO"]
    back  = ["OOOO", "OSGO", "OSDO", "OSDO", "OSDO", "OSDO", "OSDO", "OSSO", "OSSO", "OOOO"]
    return _limb_block(face, front, face, back)



_FUNG_TAIL_R = ["OOO", "OGO", "OGO", "OGg", "OGg", "OGg", "ODg", "ODg", "ODD", "ODD", "OSS", "OOO"]
_FUNG_TAIL_F = ["OOO", "OGO", "OGg", "OGg", "OGg", "ODg", "ODg", "ODD", "ODD", "OSS", "OSS", "OOO"]
_FUNG_TAIL_L = ["OOO", "OGO", "OGO", "OGg", "OGg", "OGg", "ODg", "ODg", "ODD", "ODD", "OSS", "OOO"]
_FUNG_TAIL_B = ["OOO", "OGO", "OGO", "OGg", "OGg", "OGg", "ODg", "ODg", "ODD", "ODD", "OSS", "OOO"]


# ===========================================================================
#  FAMILY REGISTRY
#  Six authored atlas families. The 55 species in content/mobs.py each pick a
#  family, a curated palette (palettes.creature_ramp) and zero or more
#  hand-placed OVERLAYS below -- that is what makes a Gloomstag read as a
#  Gloomstag and not as a recoloured Prowler.
# ===========================================================================

FAMILIES: Dict[str, Dict[str, object]] = {
    "quadruped": {
        "head_side_r": _QUAD_HEAD_R, "head_side_f": _QUAD_HEAD_F,
        "head_side_l": _QUAD_HEAD_L, "head_side_b": _QUAD_HEAD_B,
        "head_top": _QUAD_HEAD_TOP, "head_bottom": _QUAD_HEAD_BOT,
        "torso_r": _QUAD_TORSO_R, "torso_f": _QUAD_TORSO_F,
        "torso_b": _QUAD_TORSO_B, "torso_t": _QUAD_TORSO_T,
        "limb_fl": _quad_limb(True), "limb_fr": _quad_limb(False),
        "limb_bl": _quad_limb(True), "limb_br": _quad_limb(False),
        "tail_r": _QUAD_TAIL_R, "tail_f": _QUAD_TAIL_F,
        "tail_l": _QUAD_TAIL_L, "tail_b": _QUAD_TAIL_B,
    },
    "arthropod": {
        "head_side_r": _ARTHRO_HEAD_R, "head_side_f": _ARTHRO_HEAD_F,
        "head_side_l": _ARTHRO_HEAD_L, "head_side_b": _ARTHRO_HEAD_B,
        "head_top": _ARTHRO_HEAD_TOP, "head_bottom": _ARTHRO_HEAD_BOT,
        "torso_r": _ARTHRO_TORSO_R, "torso_f": _ARTHRO_TORSO_F,
        "torso_b": _ARTHRO_TORSO_B, "torso_t": _ARTHRO_TORSO_T,
        "limb_fl": _arthro_limb(), "limb_fr": _arthro_limb(),
        "limb_bl": _arthro_limb(), "limb_br": _arthro_limb(),
        "tail_r": _ARTHRO_TAIL_R, "tail_f": _ARTHRO_TAIL_F,
        "tail_l": _ARTHRO_TAIL_L, "tail_b": _ARTHRO_TAIL_B,
    },
    "biped": {
        "head_side_r": _BIPED_HEAD_R, "head_side_f": _BIPED_HEAD_F,
        "head_side_l": _BIPED_HEAD_L, "head_side_b": _BIPED_HEAD_B,
        "head_top": _BIPED_HEAD_TOP, "head_bottom": _BIPED_HEAD_BOT,
        "torso_r": _BIPED_TORSO_R, "torso_f": _BIPED_TORSO_F,
        "torso_b": _BIPED_TORSO_B, "torso_t": _BIPED_TORSO_T,
        "limb_fl": _biped_limb(True), "limb_fr": _biped_limb(True),
        "limb_bl": _biped_limb(False), "limb_br": _biped_limb(False),
        "tail_r": _BIPED_TAIL_R, "tail_f": _BIPED_TAIL_F,
        "tail_l": _BIPED_TAIL_L, "tail_b": _BIPED_TAIL_B,
    },
    "serpent": {
        "head_side_r": _SERP_HEAD_R, "head_side_f": _SERP_HEAD_F,
        "head_side_l": _SERP_HEAD_L, "head_side_b": _SERP_HEAD_B,
        "head_top": _SERP_HEAD_TOP, "head_bottom": _SERP_HEAD_BOT,
        "torso_r": _SERP_TORSO_R, "torso_f": _SERP_TORSO_F,
        "torso_b": _SERP_TORSO_B, "torso_t": _SERP_TORSO_T,
        "limb_fl": _serp_coil(), "limb_fr": _serp_coil(),
        "limb_bl": _serp_coil(), "limb_br": _serp_coil(),
        "tail_r": _SERP_TAIL_R, "tail_f": _SERP_TAIL_F,
        "tail_l": _SERP_TAIL_L, "tail_b": _SERP_TAIL_B,
    },
    "avian": {
        "head_side_r": _AVIAN_HEAD_R, "head_side_f": _AVIAN_HEAD_F,
        "head_side_l": _AVIAN_HEAD_L, "head_side_b": _AVIAN_HEAD_B,
        "head_top": _AVIAN_HEAD_TOP, "head_bottom": _AVIAN_HEAD_BOT,
        "torso_r": _AVIAN_TORSO_R, "torso_f": _AVIAN_TORSO_F,
        "torso_b": _AVIAN_TORSO_B, "torso_t": _AVIAN_TORSO_T,
        "limb_fl": _avian_wing(), "limb_fr": _avian_wing(),
        "limb_bl": _avian_leg(), "limb_br": _avian_leg(),
        "tail_r": _AVIAN_TAIL_R, "tail_f": _AVIAN_TAIL_F,
        "tail_l": _AVIAN_TAIL_L, "tail_b": _AVIAN_TAIL_B,
    },
    "fungal": {
        "head_side_r": _FUNG_HEAD_R, "head_side_f": _FUNG_HEAD_F,
        "head_side_l": _FUNG_HEAD_L, "head_side_b": _FUNG_HEAD_B,
        "head_top": _FUNG_HEAD_TOP, "head_bottom": _FUNG_HEAD_BOT,
        "torso_r": _FUNG_TORSO_R, "torso_f": _FUNG_TORSO_F,
        "torso_b": _FUNG_TORSO_B, "torso_t": _FUNG_TORSO_T,
        "limb_fl": _fungal_limb(), "limb_fr": _fungal_limb(),
        "limb_bl": _fungal_limb(), "limb_br": _fungal_limb(),
        "tail_r": _FUNG_TAIL_R, "tail_f": _FUNG_TAIL_F,
        "tail_l": _FUNG_TAIL_L, "tail_b": _FUNG_TAIL_B,
    },
}


def build_family_atlas(family: str) -> List[str]:
    """Return the authored 64x32 character atlas for a creature family."""
    if family not in FAMILIES:
        raise KeyError(f"unknown creature family {family!r}; have {sorted(FAMILIES)}")
    f = FAMILIES[family]
    return _atlas(family, **{k: f[k] for k in f})


# ===========================================================================
#  SPECIES OVERLAYS
#  Small, hand-placed detail patches applied at explicit atlas coordinates.
#  These are the marks that separate one species from another: horns, crests,
#  fin fans, eye counts, bioluminescent freckles, mane stripes, carapace
#  ridges. Every glyph below was placed by hand -- nothing is generated.
# ===========================================================================

OVERLAYS: Dict[str, Dict[str, object]] = {
    # (dx, dy) is the top-left corner of the patch on the 64x32 atlas.
    "antlers": {"at": (8, 0), "rows": [
        "BOOOOOOB",
        "BOO..OOB",
        "BO....OB",
    ]},
    "horns_curved": {"at": (8, 0), "rows": [
        "bBOOOOBb",
        ".BOOOOB.",
        "..bOOb..",
    ]},
    "crest": {"at": (9, 0), "rows": [
        ".AOOOOA.",
        "AAOOOOAA",
        ".AOOOOA.",
    ]},
    "single_horn": {"at": (11, 0), "rows": [
        "..BBO...",
        ".BbBO...",
        ".BbBO...",
    ]},
    "fin_fan": {"at": (8, 0), "rows": [
        "TTOOOOTT",
        "gTOOOOTg",
        ".TOOOOT.",
    ]},
    "eyes_three": {"at": (9, 2), "rows": [
        "EeEeEeEe",
        "eEeEeEeE",
    ]},
    "eyes_glowing": {"at": (9, 2), "rows": [
        "GgGgGgGg",
        "gGgGgGgG",
    ]},
    "eyes_void": {"at": (10, 2), "rows": [
        "eOOOOe",
        "OeOOeO",
    ]},
    "mane_stripe": {"at": (8, 0), "rows": [
        "AAAAAAAA",
        "AaAaAaAa",
    ]},
    "carapace_ridge": {"at": (8, 1), "rows": [
        "ODOODOOD",
        "DOODOODO",
        "ODOODOOD",
    ]},
    "bioluminescent_freckles": {"at": (8, 3), "rows": [
        "G.H.G.H.",
        ".G.H.G.H",
        "H.G.H.G.",
    ]},
    "gills": {"at": (0, 3), "rows": [
        "SSSSSSSS",
        "SgSgSgSg",
        "SSSSSSSS",
    ]},
    "tusks": {"at": (10, 4), "rows": [
        "B....B",
        "Bb..bB",
    ]},
    "beak_hooked": {"at": (11, 4), "rows": [
        "BBBB",
        "BbbB",
        ".BB.",
    ]},
    "mushroom_cap": {"at": (8, 0), "rows": [
        "GggggggG",
        "gGGGGGGg",
        "GggggggG",
    ]},
    "spore_vents": {"at": (32, 3), "rows": [
        "g.GG.GG.g.GG.GG.",
    ]},
    "runes_glowing": {"at": (48, 3), "rows": [
        "G.GG.GG.GG.GG.GG",
        ".GG.GG.GG.GG.GG.",
    ]},
    "scar": {"at": (16, 2), "rows": [
        "S.S.S.",
        ".S.S.S",
    ]},
    "saddle": {"at": (48, 2), "rows": [
        "WWWWWWWWWWWWWWWW",
        "WwwwwwwwwwwwwwwW",
    ]},
    "barding": {"at": (32, 2), "rows": [
        "BBBBBBBBBBBBBBBB",
        "BbBbBbBbBbBbBbBb",
    ]},
    "claws_long": {"at": (0, 24), "rows": [
        "B..OB..OB..OB..O",
    ]},
    "hooves_cloven": {"at": (0, 24), "rows": [
        "BBOBBBOBBBOBBBOB",
    ]},
    "wing_membrane": {"at": (0, 17), "rows": [
        "TTTTTTTTTTTTTTTT",
        "gTgTgTgTgTgTgTgT",
    ]},
    "segment_bands": {"at": (32, 1), "rows": [
        "OOOOOOOOOOOOOOOO",
        "SSSSSSSSSSSSSSSS",
        "OOOOOOOOOOOOOOOO",
    ]},
    "crown_shards": {"at": (8, 0), "rows": [
        "B.OB.OB.",
        "BBOBBBOB",
    ]},
    "void_fractures": {"at": (48, 4), "rows": [
        "A.AA.AA.",
        ".AA.AA.A",
        "A.AA.AA.",
    ]},
    "moss_growth": {"at": (32, 5), "rows": [
        "G.GG.GG.GG.GG.GG",
        ".GG.GG.GG.GG.GG.",
    ]},
    "crystal_spurs": {"at": (0, 16), "rows": [
        "H..OH..OH..OH..O",
        "LHOLHOLHOLHOLHO.",
    ]},
    "root_heart_glow": {"at": (32, 3), "rows": [
        "G.CCG.G.CCG.G.CC",
        ".CCG.G.CCG.G.CCG",
        "G.CCG.G.CCG.G.CC",
    ]},
    "bark_plates": {"at": (0, 2), "rows": [
        "A.AA.AA.AA.AA.AA",
        ".AA.AA.AA.AA.AA.",
        "a.aa.aa.aa.aa.aa",
    ]},
    "gilded_trim": {"at": (48, 1), "rows": [
        "AAAAAAAAAAAAAAAA",
        "aAaAaAaAaAaAaAaA",
    ]},
    "phase_scars": {"at": (16, 3), "rows": [
        "X.Y.X.Y.X.Y.X.Y.",
        ".Z.Z.Z.Z.Z.Z.Z.Z",
    ]},
    "no_marking": {"at": (0, 0), "rows": ["."]},
}
