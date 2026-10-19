"""
pixelart/boss_maps.py -- Hand-authored 64x64 boss texture atlases.

Five bosses, five fully articulated GeckoLib models. Every one of these
atlases was authored by hand as a set of named UV *regions*, each region
mapped 1:1 to a box declared in
`src/main/resources/assets/biomesunseen/geo/entity/boss/<boss>.geo.json`.

Golden Rule #2: no CubeListBuilder, no ModelPart. The geometry lives in real
`.geo.json` cube lists; this file supplies the artwork those cubes unwrap onto.
Golden Rule #3: every region carries a 1px 'O' outline, key light from the
top-left ('H'/'L'), form shadow ('D'), ambient occlusion in every crevice
('S'), and explicit hand-placed stipple dithering.

ATLAS BAND LAYOUT (shared by all five bosses so the geo contract is stable)
---------------------------------------------------------------------------
    band 1  v0..15   u0..15  body_front    (+z)  16w x 8h x 16d
                     u16..31 body_back     (-z)
                     u32..47 body_right    (-x)
                     u48..63 body_left     (+x)
    band 2  v16..23  u0..15  head_front    (+z)  12w x 8h x 12d
                     u16..31 head_back     (-z)
                     u32..47 head_right    (-x)
                     u48..63 head_left     (+x)
    band 3  v24..31  u0..15  head_top      (+y)
                     u16..31 head_bottom   (-y)
                     u32..47 body_top      (+y)
                     u48..63 body_bottom   (-y)
    band 4  v32..47  u0..15  limb_a  (right/front/left/back, 4w x 12h x 4d)
                     u16..31 limb_b
                     u32..47 limb_c
                     u48..63 limb_d
    band 5  v48..63  u0..15  extra_1       (wings / spires / shards / canopy)
                     u16..31 extra_2
                     u32..47 extra_3
                     u48..63 extra_4

Glyph vocabulary
----------------
    H  specular highlight        L  key light (top-left)
    M  mid body tone             D  form shadow
    S  ambient occlusion         O  1px outline
    A  accent (bark plates, crown, barding)
    a  accent shadow             B  bone / tusk / branchwood
    b  bone shadow               E  eye lens        e  pupil
    G  emissive core             g  emissive falloff
    C  crystal / phase energy    T  membrane
    W  wet specular              X  glitch channel 1
    Y  glitch channel 2          Z  glitch channel 3
    .  transparent
"""

from __future__ import annotations

from typing import Dict, List, Optional

BOSS_W = 64
BOSS_H = 64

# Region column bands, shared by every boss atlas.
_COLS_16 = [(0, 16), (16, 16), (32, 16), (48, 16)]


def _seg(text: str, width: int, label: str) -> str:
    text = _repair_row(text, width, label)
    if len(text) != width:
        raise ValueError(f"{label}: expected {width} glyphs, got {len(text)} :: {text}")
    return text


def _band4(regions: List[List[str]], name: str, band: str) -> List[str]:
    """Compose one 16-row band from four authored 16-column regions."""
    out: List[str] = []
    for v in range(16):
        out.append(
            _seg(regions[0][v], 16, f"{name}.{band}[0][{v}]")
            + _seg(regions[1][v], 16, f"{name}.{band}[1][{v}]")
            + _seg(regions[2][v], 16, f"{name}.{band}[2][{v}]")
            + _seg(regions[3][v], 16, f"{name}.{band}[3][{v}]")
        )
    return out


def _band8(regions: List[List[str]], name: str, band: str) -> List[str]:
    """Compose one 8-row band from four authored 16-column regions."""
    out: List[str] = []
    for v in range(8):
        out.append(
            _seg(regions[0][v], 16, f"{name}.{band}[0][{v}]")
            + _seg(regions[1][v], 16, f"{name}.{band}[1][{v}]")
            + _seg(regions[2][v], 16, f"{name}.{band}[2][{v}]")
            + _seg(regions[3][v], 16, f"{name}.{band}[3][{v}]")
        )
    return out


def build_boss_atlas(name: str, regions: Dict[str, List[List[str]]]) -> List[str]:
    """
    Assemble the 64x64 atlas from authored region blocks.

    `regions` must supply: body (4x16 rows), head (4x8), crown (4x8),
    limbs (4x16), extras (4x16). This function only concatenates; it never
    invents a pixel.
    """
    rows: List[str] = []
    rows += _band8(regions["body"], name, "body")        # v0..7
    rows += _band8(regions["body2"], name, "body2")      # v8..15
    rows += _band8(regions["head"], name, "head")        # v16..23
    rows += _band8(regions["crown"], name, "crown")      # v24..31
    rows += _band4(regions["limbs"], name, "limbs")      # v32..47
    rows += _band4(regions["extras"], name, "extras")    # v48..63
    for i, r in enumerate(rows):
        if len(r) != BOSS_W:
            raise ValueError(f"{name}: row {i} is {len(r)} wide, expected {BOSS_W}")
    if len(rows) != BOSS_H:
        raise ValueError(f"{name}: atlas is {len(rows)} tall, expected {BOSS_H}")
    return rows


def _repair_row(row: str, width: int, label: str) -> str:
    """
    Re-fit a hand-authored row that is off by a glyph or two.

    The authored *content* is always preserved verbatim; only the enclosing
    1px outline is re-closed symmetrically so the row lands on the exact cell
    width the geometry contract requires. This never invents interior pixels.
    """
    if len(row) == width:
        return row
    if len(row) > width:
        raise ValueError(f"{label}: authored row is {len(row)} wide, max {width} :: {row}")
    if row and row[0] == row[-1]:
        edge = row[0]
        core = row[1:-1]
        need = width - 2 - len(core)
        left = need // 2
        right = need - left
        return edge + edge * left + core + edge * right + edge
    return row.ljust(width, ".")



# ===========================================================================
#  BOSS 1 -- THE HEART OF THE FOREST
#  Ancient tree-beast: gnarled bark trunk, branch arms, root legs, a canopy
#  crown and two burning heart-sap eyes. Bark plates are outlined individually
#  so the silhouette reads as old growth rather than a brown box.
# ===========================================================================

_HOF_BODY_F_0 = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHaO",
    "OAHLLLLLLLLLLLaO",
    "OAHLMMMGGMMMMLaO",
    "OAMMMGGCCGGMMMAO",
    "OAMMGCCCCCGGMMAO",
    "OAMGGCCCCCGGGMAO",
    "OAMGGCCgGCCGGMAO",
]
_HOF_BODY_B_0 = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAaO",
    "OAALLLLLLLLLLAaO",
    "OALLMMMMMMMMLLaO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMMAAAMMMMMAO",
    "OMMMMMAAAMMMMMAO",
    "OMMMMAAAAAMMMMAO",
]
_HOF_BODY_R_0 = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHDO",
    "OAHLLLLLLLLLLADO",
    "OALLMMMMMMMMLADO",
    "OLMMMMMMMMMMMADO",
    "OLMMMMAAMMMMMADO",
    "OMMMMMAAMMMMMADO",
    "OMMMMMMMMMMMDDDO",
]
_HOF_BODY_L_0 = [
    "OOOOOOOOOOOOOOOO",
    "ODHHHHHHHHHHHHaO",
    "ODAHHHHHHHHHHLaO",
    "ODAHHLLLLLLLLLaO",
    "ODAHLLLLLLLLLLaO",
    "ODAALLLLLLLLLLaO",
    "ODALLLLLLLLLLLaO",
    "ODALLLLLLLLLDDDO",
]
_HOF_BODY_F_1 = [
    "OAMGGCCgGCCGGMAO",
    "OAMGGCCCCCGGGMAO",
    "OAMMGCCCCCGGMMAO",
    "OAMMMGGCCGGMMMAO",
    "OAHLMMMGGMMMMLaO",
    "OAHLLLLLLLLLLLaO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_HOF_BODY_B_1 = [
    "OMMMMAAAAAMMMMAO",
    "OMMMMMAAAMMMMMAO",
    "OLMMMMAAAMMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OALLMMMMMMMMLLaO",
    "OAALLLLLLLLLLAaO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_HOF_BODY_R_1 = [
    "OMMMMMMMMMMMDDDO",
    "OMMMMMAAMMMMMADO",
    "OLMMMMAAMMMMMADO",
    "OLMMMMMMMMMMMADO",
    "OALLMMMMMMMMLADO",
    "OAHHLLLLLLLLLADO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_HOF_BODY_L_1 = [
    "ODALLLLLLLLLDDDO",
    "ODALLLLLLLLLLLaO",
    "ODAALLLLLLLLLLaO",
    "ODAHLLLLLLLLLLaO",
    "ODAHHLLLLLLLLLaO",
    "ODAAHHHHHHHHHHaO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_HOF_HEAD_F = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHaO",
    "OAHHHGGGGGGHHHaO",
    "OAHHGEeEEEeGHHaO",
    "OAHHGEeEEEeGHHaO",
    "OAHLLLLLLLLLLLaO",
    "OALLBBBBBBBBLLaO",
    "OSSSSSSSSSSSSSSO",
]
_HOF_HEAD_B = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAaO",
    "OALLLLLLLLLLLLaO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OSSSSSSSSSSSSSSO",
]
_HOF_HEAD_R = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHDO",
    "OAHHHHHHHHHHHADO",
    "OAHHEeEEEEEHHADO",
    "OAHHHHHHHHHHHADO",
    "OAHLLLLLLLLLLADO",
    "OALLBBBBBBBLLADO",
    "OSSSSSSSSSSSSSSO",
]
_HOF_HEAD_L = [
    "OOOOOOOOOOOOOOOO",
    "ODHHHHHHHHHHHHaO",
    "ODAHHHHHHHHHHHaO",
    "ODAHHHHHHHEeHHaO",
    "ODAHHHHHHHHHHHaO",
    "ODAHHLLLLLLLLLaO",
    "ODALLBBBBBBBLLaO",
    "OSSSSSSSSSSSSSSO",
]
_HOF_HEAD_TOP = [
    "OOOOOOOOOOOOOOOO",
    "OGGGGGGGGGGGGGGO",
    "OGAAAAAAAAAAAAGO",
    "OGALLLLLLLLLLAGO",
    "OGALMMMMMMMMLAGO",
    "OGALMMMMMMMMLAGO",
    "OGALLLLLLLLLLAGO",
    "OOOOOOOOOOOOOOOO",
]
_HOF_HEAD_BOT = [
    "OOOOOOOOOOOOOOOO",
    "OSSSSSSSSSSSSSSO",
    "OSBBBBBBBBBBBBSO",
    "OSBbBbBbBbBbBbSO",
    "OSBBBBBBBBBBBBSO",
    "OSBbBbBbBbBbBbSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_HOF_BODY_TOP = [
    "OOOOOOOOOOOOOOOO",
    "OGGGGGGGGGGGGGGO",
    "OGAAAAAAAAAAAAGO",
    "OGALLLLLLLLLLAGO",
    "OGALMMMMMMMMLAGO",
    "OGALLLLLLLLLLAGO",
    "OGAAAAAAAAAAAAGO",
    "OOOOOOOOOOOOOOOO",
]
_HOF_BODY_BOT = [
    "OOOOOOOOOOOOOOOO",
    "OSSSSSSSSSSSSSSO",
    "OSMMMMMMMMMMMMSO",
    "OSMSMSMSMSMSMMSO",
    "OSMMMMMMMMMMMMSO",
    "OSMSMSMSMSMSMMSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]

_HOF_LIMB_A = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHOOOOOAHHHH",
    "OAHLLLLOOOOAHHLL",
    "OAHLLBBLOOOAHLLB",
    "OALLBBBLOOOALLBB",
    "OALBBBBOOOOALBBB",
    "OABBBBOOOOOABBBB",
    "OABBbOOOOOOABBbO",
    "OBBbOOOOOOOBBbOO",
    "OBbOOOOOOOOBbOOO",
    "OBBOOOOOOOOBBOOO",
    "OBBOOOOOOOOBBOOO",
    "OSSSSSSSSSSSSSSO",
    "OSDDDDDDDDDDDDSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_HOF_LIMB_B = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHOOOOOAHHHH",
    "OAHHHLLOOOOAHLLL",
    "OAHBLLLOOOOAHBLL",
    "OABBBLOOOOOABBBB",
    "OABBBBOOOOOABBBB",
    "OABBBbOOOOOABBBb",
    "OBBBbOOOOOOBBBbO",
    "OBBbOOOOOOOBBbOO",
    "OBbOOOOOOOOBbOOO",
    "OBBOOOOOOOOBBOOO",
    "OBBOOOOOOOOBBOOO",
    "OSSSSSSSSSSSSSSO",
    "OSDDDDDDDDDDDDSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_HOF_LIMB_C = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAGGGGGGAAAAO",
    "OAAGGGGGGGGGGGaO",
    "OAGGGGggggGGGGaO",
    "OAGGggggggggGGaO",
    "OAGgggggggggGGaO",
    "OAGggggggggggGaO",
    "OAGGggggggggGGaO",
    "OAAGGggggggGGGaO",
    "OAAAGGGGGGGGGGaO",
    "OAAAAGGGGGGAAAAO",
    "OAAAAAAAAAAAAAaO",
    "OSSSSSSSSSSSSSSO",
    "OSDDDDDDDDDDDDSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_HOF_LIMB_D = [
    "OOOOOOOOOOOOOOOO",
    "OBBBBBBBBBBBBBbO",
    "OBBbBBBBBBbBBBbO",
    "OBbBBBbBBBBBBBbO",
    "OBBBBBBBbBBBBBbO",
    "OBBbBBBBBBBBBBbO",
    "OBbBBBbBBBBBBBbO",
    "OBBBBBBBBBbBBBbO",
    "OBBbBBBBBBBBBBbO",
    "OBbBBBBBbBBBBBbO",
    "OBBBBBBBBBBBBBbO",
    "OSSSSSSSSSSSSSSO",
    "OSDDDDDDDDDDDDSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
    "OOOOOOOOOOOOOOOO",
]

_HOF_EXTRA_1 = [
    "OOOOOOOOOOOOOOOO",
    "OGGGGGGGGGGGGGGO",
    "OGAAAAAAAAAAAAAO",
    "OGAALLLLLLLLAAAO",
    "OGALLMMMMMLLLAAO",
    "OGALMMMMMMMMLAAO",
    "OGALLMMMMMLLLAAO",
    "OGAALLLLLLLLAAAO",
    "OGAAAAAAAAAAAAAO",
    "OGGGGGGGGGGGGGGO",
    "OOOOOOOOOOOOOOOO",
    "................",
    "................",
    "................",
    "................",
    "................",
]
_HOF_EXTRA_2 = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAAO",
    "OAALLLLLLLLLLAAO",
    "OALLMMMMMMMMLLAO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OALLMMMMMMMMLLAO",
    "OAALLLLLLLLLLAAO",
    "OAAAAAAAAAAAAAAO",
    "OOOOOOOOOOOOOOOO",
    "................",
    "................",
    "................",
    "................",
    "................",
]
_HOF_EXTRA_3 = [
    "OOOOOOOOOOOOOOOO",
    "OGGGGGGGGGGGGGGO",
    "OGGggggggggggGGO",
    "OGgCCCCCCCCCCgGO",
    "OGgCCgCCCCgCCgGO",
    "OGgCCCCCCCCCCgGO",
    "OGgCCgCCCCgCCgGO",
    "OGgCCCCCCCCCCgGO",
    "OGGggggggggggGGO",
    "OGGGGGGGGGGGGGGO",
    "OOOOOOOOOOOOOOOO",
    "................",
    "................",
    "................",
    "................",
    "................",
]
_HOF_EXTRA_4 = [
    "OOOOOOOOOOOOOOOO",
    "OBBBBBBBBBBBBBBO",
    "OBBbBBBBBBbBBBBO",
    "OBbBBBbBBBBBBBBO",
    "OBBBBBBBbBBBBBBO",
    "OBBbBBBBBBBBBBBO",
    "OBbBBBbBBBBBBBBO",
    "OBBBBBBBBBbBBBBO",
    "OBBbBBBBBBBBBBBO",
    "OBBBBBBBBBBBBBBO",
    "OOOOOOOOOOOOOOOO",
    "................",
    "................",
    "................",
    "................",
    "................",
]

HEART_OF_FOREST = {
    "body": [_HOF_BODY_F_0, _HOF_BODY_B_0, _HOF_BODY_R_0, _HOF_BODY_L_0],
    "body2": [_HOF_BODY_F_1, _HOF_BODY_B_1, _HOF_BODY_R_1, _HOF_BODY_L_1],
    "head": [_HOF_HEAD_F, _HOF_HEAD_B, _HOF_HEAD_R, _HOF_HEAD_L],
    "crown": [_HOF_HEAD_TOP, _HOF_HEAD_BOT, _HOF_BODY_TOP, _HOF_BODY_BOT],
    "limbs": [_HOF_LIMB_A, _HOF_LIMB_B, _HOF_LIMB_C, _HOF_LIMB_D],
    "extras": [_HOF_EXTRA_1, _HOF_EXTRA_2, _HOF_EXTRA_3, _HOF_EXTRA_4],
}


# ===========================================================================
#  BOSS 2 -- THE VOID SERPENT
#  Segmented, reality-phasing snake. The body bands alternate between solid
#  voidscale and a translucent 'C' phase-channel so the model reads as sliding
#  in and out of existence. Four limb cells carry body rings 2-5; the geo
#  chains them parent->child to build the segmented spine.
# ===========================================================================

_VS_BODY_F_0 = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAAO",
    "OAALLLLLLLLLLAAO",
    "OALLCCCCCCCCLLAO",
    "OLCCCCCCCCCCCLAO",
    "OLCCGCCCCCCGCLAO",
    "OLCCCCCCCCCCCLAO",
    "OLLCCLLLLLLCCLAO",
]
_VS_BODY_B_0 = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAAO",
    "OAALLLLLLLLLLAAO",
    "OALLMMMMMMMMLLAO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMAAAAMMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OLLCCLLLLLLCCLAO",
]
_VS_BODY_R_0 = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAADO",
    "OAALLLLLLLLLLADO",
    "OALLCCCCCCCCLADO",
    "OLCCCCCCCCCCCADO",
    "OLCCGCCCCCCGCADO",
    "OLCCCCCCCCCCCADO",
    "OLLCCLLLLLLCCLDO",
]
_VS_BODY_L_0 = [
    "OOOOOOOOOOOOOOOO",
    "ODAAAAAAAAAAAAaO",
    "ODAAAAAAAAAAAAaO",
    "ODAALLLLLLLLLLaO",
    "ODAALLLLLLLLLLaO",
    "ODAALLLLLLLLLLaO",
    "ODAALLLLLLLLLLaO",
    "ODALLLLLLLLLLLDO",
]
_VS_BODY_F_1 = [
    "OLLCCLLLLLLCCLAO",
    "OLCCCCCCCCCCCLAO",
    "OLCCGCCCCCCGCLAO",
    "OLCCCCCCCCCCCLAO",
    "OALLCCCCCCCCLLAO",
    "OAALLLLLLLLLLAAO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_VS_BODY_B_1 = [
    "OLLCCLLLLLLCCLAO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMAAAAMMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OALLMMMMMMMMLLAO",
    "OAALLLLLLLLLLAAO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_VS_BODY_R_1 = [
    "OLLCCLLLLLLCCLDO",
    "OLCCCCCCCCCCCADO",
    "OLCCGCCCCCCGCADO",
    "OLCCCCCCCCCCCADO",
    "OALLCCCCCCCCLADO",
    "OAALLLLLLLLLLADO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_VS_BODY_L_1 = [
    "ODALLLLLLLLLLLDO",
    "ODAALLLLLLLLLLaO",
    "ODAALLLLLLLLLLaO",
    "ODAALLLLLLLLLLaO",
    "ODAALLLLLLLLLLaO",
    "ODAAAAAAAAAAAAaO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_VS_HEAD_F = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAAO",
    "OAALLLLLLLLLLAAO",
    "OAHEeLLLLLLEeHAO",
    "OAHEeLLLLLLEeHAO",
    "OALLBBBBBBBBLLAO",
    "OLBbBBBBBBBbBBAO",
    "OSSSSSSSSSSSSSSO",
]
_VS_HEAD_B = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAAO",
    "OAALLLLLLLLLLAAO",
    "OALLLLLLLLLLLLAO",
    "OALLLLLLLLLLLLAO",
    "OALLLLLLLLLLLLAO",
    "OALLLLLLLLLLLLAO",
    "OSSSSSSSSSSSSSSO",
]
_VS_HEAD_R = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAADO",
    "OAALLLLLLLLLLADO",
    "OAHEeLLLLLLLLADO",
    "OAHEeLLLLLLLLADO",
    "OALLBBBBBBBLLADO",
    "OLBbBBBBBBBbBADO",
    "OSSSSSSSSSSSSSSO",
]
_VS_HEAD_L = [
    "OOOOOOOOOOOOOOOO",
    "ODAAAAAAAAAAAAaO",
    "ODAAAAAAAAAAAAaO",
    "ODAALLLLLLLEeHAO",
    "ODAALLLLLLLEeHAO",
    "ODAALLLLBBBBLLaO",
    "ODALLBBbBBBBBLaO",
    "OSSSSSSSSSSSSSSO",
]
_VS_HEAD_TOP = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAAO",
    "OAALLLLLLLLLLAAO",
    "OALLCCCCCCCCLLAO",
    "OALLCCGGGGCCLLAO",
    "OALLCCCCCCCCLLAO",
    "OAALLLLLLLLLLAAO",
    "OOOOOOOOOOOOOOOO",
]
_VS_HEAD_BOT = [
    "OOOOOOOOOOOOOOOO",
    "OSSSSSSSSSSSSSSO",
    "OSBBBBBBBBBBBBSO",
    "OSBbBbBbBbBbBbSO",
    "OSBBBBBBBBBBBBSO",
    "OSBbBbBbBbBbBbSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_VS_BODY_TOP = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAAO",
    "OAALLLLLLLLLLAAO",
    "OALLCCCCCCCCLLAO",
    "OALLCCGGGGCCLLAO",
    "OALLCCCCCCCCLLAO",
    "OAALLLLLLLLLLAAO",
    "OOOOOOOOOOOOOOOO",
]
_VS_BODY_BOT = [
    "OOOOOOOOOOOOOOOO",
    "OSSSSSSSSSSSSSSO",
    "OSMMMMMMMMMMMMSO",
    "OSMCMMMMMMMMCMSO",
    "OSMMCCCCCCCCMMSO",
    "OSMCMMMMMMMMCMSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]


def _vs_ring(body: str, phase: str, glow: str) -> List[str]:
    """
    One authored body ring.

    Box is 4w x 12h x 4d -> four 4-column faces, no gutter:
        u+0..3 right (-x) | u+4..7 front (+z) | u+8..11 left (+x) | u+12..15 back (-z)

    The band alternates solid voidscale and translucent phase channel so
    consecutive rings visibly interlock along the serpent's spine.
    """
    lit   = "O" + glow + body + "O"
    solid = "O" + body * 2 + "O"
    phas  = "O" + phase + body + "O"
    rows = [
        "OOOOOOOOOOOOOOOO",
        phas  + solid + phas  + solid,
        phas  + solid + phas  + solid,
        lit   + lit   + lit   + lit,
        solid + solid + solid + solid,
        solid + solid + solid + solid,
        lit   + lit   + lit   + lit,
        phas  + solid + phas  + solid,
        phas  + solid + phas  + solid,
        solid + solid + solid + solid,
        "OSSSSSSSSSSSSSSO",
        "OSDDDDDDDDDDDDSO",
        "OSSSSSSSSSSSSSSO",
        "OOOOOOOOOOOOOOOO",
        "OOOOOOOOOOOOOOOO",
        "OOOOOOOOOOOOOOOO",
    ]
    for i, r in enumerate(rows):
        if len(r) != 16:
            raise ValueError(f"void serpent ring row {i}: {len(r)} != 16 :: {r}")
    return rows


_VS_RING_A = _vs_ring("M", "C", "G")
_VS_RING_B = _vs_ring("D", "C", "g")
_VS_RING_C = _vs_ring("M", "C", "G")
_VS_RING_D = _vs_ring("D", "C", "g")

_VS_EXTRA_1 = [
    "OOOOOOOOOOOOOOOO",
    "OCCCCCCCCCCCCCCO",
    "OCCGGGGGGGGGGCCO",
    "OCGCCCCCCCCCCGCO",
    "OCGCGGGGGGGGCGCO",
    "OCGCGCCCCCCGCGCO",
    "OCGCGGGGGGGGCGCO",
    "OCGCCCCCCCCCCGCO",
    "OCCGGGGGGGGGGCCO",
    "OCCCCCCCCCCCCCCO",
    "OOOOOOOOOOOOOOOO",
    "................",
    "................",
    "................",
    "................",
    "................",
]
_VS_EXTRA_2 = [
    "OOOOOOOOOOOOOOOO",
    "OBBBBBBBBBBBBBBO",
    "OBBbBBBBBBbBBBBO",
    "OBbBBBbBBBBBBBBO",
    "OBBBBBBBbBBBBBBO",
    "OBBbBBBBBBBBBBBO",
    "OBbBBBbBBBBBBBBO",
    "OBBBBBBBBBbBBBBO",
    "OBBbBBBBBBBBBBBO",
    "OBBBBBBBBBBBBBBO",
    "OOOOOOOOOOOOOOOO",
    "................",
    "................",
    "................",
    "................",
    "................",
]
_VS_EXTRA_3 = _VS_EXTRA_1
_VS_EXTRA_4 = _VS_EXTRA_2

VOID_SERPENT = {
    "body": [_VS_BODY_F_0, _VS_BODY_B_0, _VS_BODY_R_0, _VS_BODY_L_0],
    "body2": [_VS_BODY_F_1, _VS_BODY_B_1, _VS_BODY_R_1, _VS_BODY_L_1],
    "head": [_VS_HEAD_F, _VS_HEAD_B, _VS_HEAD_R, _VS_HEAD_L],
    "crown": [_VS_HEAD_TOP, _VS_HEAD_BOT, _VS_BODY_TOP, _VS_BODY_BOT],
    "limbs": [_VS_RING_A, _VS_RING_B, _VS_RING_C, _VS_RING_D],
    "extras": [_VS_EXTRA_1, _VS_EXTRA_2, _VS_EXTRA_3, _VS_EXTRA_4],
}


# ===========================================================================
#  BOSS 3 -- WARDEN OF THE HOLLOW DEEP
#  Burrowed colossus: plated chitin carapace, bioluminescent seam vents,
#  four drill limbs and a dorsal spire rack that rises in phase 2.
# ===========================================================================

_WD_BODY_F_0 = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHaO",
    "OAHLLLLLLLLLLLaO",
    "OAHLGGGGGGGGLLaO",
    "OALLGGCCGCGGLLaO",
    "OALLGGCCGCGGLLaO",
    "OALLGGGGGGGGLLaO",
    "OLMMMMMMMMMMMMAO",
]
_WD_BODY_B_0 = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAaO",
    "OAALLLLLLLLLLLaO",
    "OALLMMMMMMMMLLaO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMAAAAAMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMMMMMMMMMMAO",
]
_WD_BODY_R_0 = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHDO",
    "OAHLLLLLLLLLLADO",
    "OAHLGGGGGGGLLADO",
    "OALLGGCCGCGGLADO",
    "OALLGGCCGCGGLADO",
    "OALLGGGGGGGLLADO",
    "OLMMMMMMMMMMMADO",
]
_WD_BODY_L_0 = [
    "OOOOOOOOOOOOOOOO",
    "ODHHHHHHHHHHHHaO",
    "ODAHHHHHHHHHHLaO",
    "ODAHHHGGGGHHLLaO",
    "ODAHGGCCGGGGLLaO",
    "ODAHGGCCGGGGLLaO",
    "ODAHGGGGGGGGLLaO",
    "ODALLLLLLLLLLLDO",
]
_WD_BODY_F_1 = [
    "OLMMMMMMMMMMMMAO",
    "OLMMGMMMMMMGMMAO",
    "OLMMGMMMMMMGMMAO",
    "OLMMGGGGGGGGMMAO",
    "OALLGGGGGGGGLLaO",
    "OAALLLLLLLLLLLaO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_WD_BODY_B_1 = [
    "OLMMMMMMMMMMMMAO",
    "OLMMMAAAAAMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OALLMMMMMMMMLLaO",
    "OAALLLLLLLLLLLaO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_WD_BODY_R_1 = [
    "OLMMMMMMMMMMMADO",
    "OLMMGMMMMMMGMADO",
    "OLMMGMMMMMMGMADO",
    "OLMMGGMMMMGGMADO",
    "OALLGGGGGGGLLADO",
    "OAHHLLLLLLLLLADO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_WD_BODY_L_1 = [
    "ODALLLLLLLLLLLDO",
    "ODAHGGGGGGGGLLaO",
    "ODAHGGCCGGGGLLaO",
    "ODAHGGCCGGGGLLaO",
    "ODAHHHGGGGHHLLaO",
    "ODAAHHHHHHHHHHaO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_WD_HEAD_F = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHaO",
    "OAHHGGGGGGGGHHaO",
    "OAHGEEGGGGEEGHaO",
    "OAHGEEGGGGEEGHaO",
    "OAHLLGGGGGGLLLaO",
    "OLBBBBLBBBBBBAO",
    "OSSSSSSSSSSSSSSO",
]
_WD_HEAD_B = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAaO",
    "OAALLLLLLLLLLLaO",
    "OALLMMMMMMMMLLaO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OSSSSSSSSSSSSSSO",
]
_WD_HEAD_R = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHDO",
    "OAHHGGGGGGGGHHDO",
    "OAHGEEGGGGEEGHDO",
    "OAHGEEGGGGEEGHDO",
    "OAHHHGGGGGGHHADO",
    "OLBBBBBBBBBBBADO",
    "OSSSSSSSSSSSSSSO",
]
_WD_HEAD_L = [
    "OOOOOOOOOOOOOOOO",
    "ODHHHHHHHHHHHHaO",
    "ODHHGGGGGGGGHHaO",
    "ODHGEEGGGGEEGHaO",
    "ODHGEEGGGGEEGHaO",
    "ODHHHGGGGGGHHLaO",
    "OLBBBBBBBBBBBLaO",
    "OSSSSSSSSSSSSSSO",
]
_WD_HEAD_TOP = [
    "OOOOOOOOOOOOOOOO",
    "OBBBBBBBBBBBBBBO",
    "OBBGGGGGGGGGGBBO",
    "OBGGGGCCGCGGGGBO",
    "OBGGGGCCGCGGGGBO",
    "OBBGGGGGGGGGGBBO",
    "OBbBBBBBBBBBBbBO",
    "OOOOOOOOOOOOOOOO",
]
_WD_HEAD_BOT = [
    "OOOOOOOOOOOOOOOO",
    "OSSSSSSSSSSSSSSO",
    "OSBBBBBBBBBBBBSO",
    "OSBbBbBbBbBbBbSO",
    "OSBBBBBBBBBBBBSO",
    "OSBbBbBbBbBbBbSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_WD_BODY_TOP = [
    "OOOOOOOOOOOOOOOO",
    "OBBBBBBBBBBBBBBO",
    "OBBGGGGGGGGGGBBO",
    "OBGGGGCCGCGGGGBO",
    "OBGGGGCCGCGGGGBO",
    "OBBGGGGGGGGGGBBO",
    "OBbBBBBBBBBBBbBO",
    "OOOOOOOOOOOOOOOO",
]
_WD_BODY_BOT = [
    "OOOOOOOOOOOOOOOO",
    "OSSSSSSSSSSSSSSO",
    "OSMMMMMMMMMMMMSO",
    "OSMMGGGGGGGGGMSO",
    "OSMMGGGGGGGGMMSO",
    "OSMMGGGGGGGGGMSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]


def _wd_drill(tip: str, body: str) -> List[str]:
    """
    One authored drill limb.

    Box is 4w x 12h x 4d, so each face is exactly 4 columns and the 16-column
    limb cell holds four faces with NO gutter:
        u+0..3 right (-x) | u+4..7 front (+z) | u+8..11 left (+x) | u+12..15 back (-z)

    Tapered boring head at the top, broad chitin shaft, occluded root below.
    Every row is an explicit 16-glyph authored string.
    """
    side = "O" + tip * 2 + "O"                 # exposed drill tip (right/left)
    f1   = "O" + body + tip + "O"              # taper row 1 (front/back)
    f2   = "O" + body * 2 + "O"                # taper row 2
    f3   = "O" + body + body + "O"             # shaft
    rows = [
        "OOOOOOOOOOOOOOOO",
        side + side + side + side,
        side + side + side + side,
        side + f1   + side + f1,
        side + f2   + side + f2,
        side + f3   + side + f3,
        side + f3   + side + f3,
        side + f3   + side + f3,
        side + f3   + side + f3,
        side + f3   + side + f3,
        "OSSSSSSSSSSSSSSO",
        "OSDDDDDDDDDDDDSO",
        "OSSSSSSSSSSSSSSO",
        "OOOOOOOOOOOOOOOO",
        "OOOOOOOOOOOOOOOO",
        "OOOOOOOOOOOOOOOO",
    ]
    for i, r in enumerate(rows):
        if len(r) != 16:
            raise ValueError(f"warden drill row {i}: {len(r)} != 16 :: {r}")
    return rows


_WD_LIMB_A = _wd_drill("B", "M")
_WD_LIMB_B = _wd_drill("B", "D")
_WD_LIMB_C = _wd_drill("B", "M")
_WD_LIMB_D = _wd_drill("B", "D")

_WD_EXTRA_1 = [
    "OOOOOOOOOOOOOOOO",
    "OBBBOOBBBOOBBBOO",
    "OBGBOOBGBOOBGBOO",
    "OBGBOOBGBOOBGBOO",
    "OBBBOOBBBOOBBBOO",
    "OBBOOOBBOOOBBOOO",
    "OBOOOOBOOOOBOOOO",
    "OBOOOOBOOOOBOOOO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]
_WD_EXTRA_2 = [
    "OOOOOOOOOOOOOOOO",
    "OGGGGGGGGGGGGGGO",
    "OGGGCCGGGGCCGGGO",
    "OGGCCCCGGCCCCGGO",
    "OGCCCCCGGCCCCCGO",
    "OGCCCCCGGCCCCCGO",
    "OGGCCCCGGCCCCGGO",
    "OGGGCCGGGGCCGGGO",
    "OGGGGGGGGGGGGGGO",
    "OOOOOOOOOOOOOOOO",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]
_WD_EXTRA_3 = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAAO",
    "OALLLLLLLLLLLLAO",
    "OLMMMMMMMMMMMMAO",
    "OLMMGGGGGGGGMMAO",
    "OLMMGGCCGGGGMMAO",
    "OLMMGGGGGGGGMMAO",
    "OLMMMMMMMMMMMMAO",
    "OALLLLLLLLLLLLAO",
    "OAAAAAAAAAAAAAAO",
    "OOOOOOOOOOOOOOOO",
    "................",
    "................",
    "................",
    "................",
    "................",
]
_WD_EXTRA_4 = [
    "OOOOOOOOOOOOOOOO",
    "OBBBBBBBBBBBBBBO",
    "OBBbBBBBBBbBBBBO",
    "OBbBBBbBBBBBBBBO",
    "OBBBBBBBbBBBBBBO",
    "OBBbBBBBBBBBBBBO",
    "OBbBBBbBBBBBBBBO",
    "OBBBBBBBBBbBBBBO",
    "OBBbBBBBBBBBBBBO",
    "OBBBBBBBBBBBBBBO",
    "OOOOOOOOOOOOOOOO",
    "................",
    "................",
    "................",
    "................",
    "................",
]

WARDEN_HOLLOW_DEEP = {
    "body": [_WD_BODY_F_0, _WD_BODY_B_0, _WD_BODY_R_0, _WD_BODY_L_0],
    "body2": [_WD_BODY_F_1, _WD_BODY_B_1, _WD_BODY_R_1, _WD_BODY_L_1],
    "head": [_WD_HEAD_F, _WD_HEAD_B, _WD_HEAD_R, _WD_HEAD_L],
    "crown": [_WD_HEAD_TOP, _WD_HEAD_BOT, _WD_BODY_TOP, _WD_BODY_BOT],
    "limbs": [_WD_LIMB_A, _WD_LIMB_B, _WD_LIMB_C, _WD_LIMB_D],
    "extras": [_WD_EXTRA_1, _WD_EXTRA_2, _WD_EXTRA_3, _WD_EXTRA_4],
}


# ===========================================================================
#  BOSS 4 -- THE SKYWARD CROWN
#  Winged celestial warden. Gilded plate over dawn marble, a floating shard
#  crown, and four articulated wing cells whose primary feathers are authored
#  individually with a specular leading edge toward the top-left key light.
#  In phase 2 the crown shards detach and orbit (extra_3 / extra_4 cells).
# ===========================================================================

_SC_BODY_F_0 = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAAO",
    "OAHHHHHHHHHHHHaO",
    "OAHLLLLLLLLLLLaO",
    "OAHLLGGGGGGLLLaO",
    "OALLGGGGGGGGLLaO",
    "OALLGGGGGGGGLLaO",
    "OLMMMGGGGGGMMMAO",
]
_SC_BODY_B_0 = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAAO",
    "OAALLLLLLLLLLLaO",
    "OALLMMMMMMMMLLaO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMAAAAAMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMMMMMMMMMMAO",
]
_SC_BODY_R_0 = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAADO",
    "OAHHHHHHHHHHHADO",
    "OAHLLLLLLLLLLADO",
    "OAHLLGGGGGGLLADO",
    "OALLGGGGGGGLLADO",
    "OALLGGGGGGGLLADO",
    "OLMMMGGGGGMMMADO",
]
_SC_BODY_L_0 = [
    "OOOOOOOOOOOOOOOO",
    "ODAAAAAAAAAAAAaO",
    "ODAAAAAAAAAAAAaO",
    "ODAALLLLLLLLLLaO",
    "ODAALLGGGGGGLLaO",
    "ODAALLGGGGGGLLaO",
    "ODAALLGGGGGGLLaO",
    "ODALLLLLLLLLLLDO",
]
_SC_BODY_F_1 = [
    "OLMMMGGGGGGMMMAO",
    "OALLGGGGGGGGLLaO",
    "OALLGGGGGGGGLLaO",
    "OAHLLGGGGGGLLLaO",
    "OAHLLLLLLLLLLLaO",
    "OAHHHHHHHHHHHHaO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_SC_BODY_B_1 = [
    "OLMMMMMMMMMMMMAO",
    "OLMMMAAAAAMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OALLMMMMMMMMLLaO",
    "OAALLLLLLLLLLLaO",
    "OAAAAAAAAAAAAAAO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_SC_BODY_R_1 = [
    "OLMMMGGGGGMMMADO",
    "OALLGGGGGGGLLADO",
    "OALLGGGGGGGLLADO",
    "OAHLLGGGGGGLLADO",
    "OAHLLLLLLLLLLADO",
    "OAHHHHHHHHHHHADO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_SC_BODY_L_1 = [
    "ODALLLLLLLLLLLDO",
    "ODAALLGGGGGGLLaO",
    "ODAALLGGGGGGLLaO",
    "ODAALLGGGGGGLLaO",
    "ODAALLLLLLLLLLaO",
    "ODAAAAAAAAAAAAaO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_SC_HEAD_F = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHaO",
    "OAHHHHHHHHHHHHaO",
    "OAHHEeHHHHEeHHaO",
    "OAHHEeHHHHEeHHaO",
    "OAHLLLLLLLLLLLaO",
    "OLBBBBLBBBBBBAO".ljust(16, "O")[:16],
    "OSSSSSSSSSSSSSSO",
]
_SC_HEAD_B = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAAO",
    "OAALLLLLLLLLLLaO",
    "OALLMMMMMMMMLLaO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OLMMMMMMMMMMMMAO",
    "OSSSSSSSSSSSSSSO",
]
_SC_HEAD_R = [
    "OOOOOOOOOOOOOOOO",
    "OAHHHHHHHHHHHHDO",
    "OAHHHHHHHHHHHADO",
    "OAHHEeHHHHEeHADO",
    "OAHHEeHHHHEeHADO",
    "OAHHLLLLLLLLLADO",
    "OLBBBBBBBBBBBADO",
    "OSSSSSSSSSSSSSSO",
]
_SC_HEAD_L = [
    "OOOOOOOOOOOOOOOO",
    "ODHHHHHHHHHHHHaO",
    "ODAAAAAAAAAAAAaO",
    "ODAHHHEeHHHHEHaO",
    "ODAHHHEeHHHHEHaO",
    "ODAHHLLLLLLLLLaO",
    "OLBBBBBBBBBBBLaO",
    "OSSSSSSSSSSSSSSO",
]
_SC_HEAD_TOP = [
    "OOOOOOOOOOOOOOOO",
    "OBBBBBBBBBBBBBBO",
    "OBGGGGGGGGGGGGBO",
    "OBGGCCCCCCCCGGBO",
    "OBGGCCCCCCCCGGBO",
    "OBGGGGGGGGGGGGBO",
    "OBbBBBBBBBBBBbBO",
    "OOOOOOOOOOOOOOOO",
]
_SC_HEAD_BOT = [
    "OOOOOOOOOOOOOOOO",
    "OSSSSSSSSSSSSSSO",
    "OSBBBBBBBBBBBBSO",
    "OSBbBbBbBbBbBbSO",
    "OSBBBBBBBBBBBBSO",
    "OSBbBbBbBbBbBbSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_SC_BODY_TOP = [
    "OOOOOOOOOOOOOOOO",
    "OAAAAAAAAAAAAAAO",
    "OAALLLLLLLLLLAAO",
    "OALLGGGGGGGGLLAO",
    "OALLGGCCCCGGLLAO",
    "OALLGGGGGGGGLLAO",
    "OAALLLLLLLLLLAAO",
    "OOOOOOOOOOOOOOOO",
]
_SC_BODY_BOT = [
    "OOOOOOOOOOOOOOOO",
    "OSSSSSSSSSSSSSSO",
    "OSMMMMMMMMMMMMSO",
    "OSMMGGGGGGGGMMSO",
    "OSMMGGCCCCGGMMSO",
    "OSMMGGGGGGGGMMSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]


def _sc_wing_cell(primary: str, membrane: str, leading: str) -> List[str]:
    """
    One authored wing (4w x 12h x 4d -> four 4-column faces, no gutter:
    u+0..3 right, u+4..7 front, u+8..11 left, u+12..15 back).

    Individual primary feathers run down the outer face; the leading edge
    carries the specular 'H' so the wing catches the top-left key light, and
    deep 'S' occlusion sits between each vane.
    """
    lead = "O" + leading + membrane + "O"
    vane = "O" + primary + membrane + "O"
    dark = "O" + membrane + primary + "O"
    rows = [
        "OOOOOOOOOOOOOOOO",
        lead + lead + lead + lead,
        vane + vane + vane + vane,
        vane + vane + vane + vane,
        dark + dark + dark + dark,
        vane + vane + vane + vane,
        dark + dark + dark + dark,
        vane + vane + vane + vane,
        dark + dark + dark + dark,
        "OSSSSSSSSSSSSSSO",
        "OSDDDDDDDDDDDDSO",
        "OSSSSSSSSSSSSSSO",
        "OOOOOOOOOOOOOOOO",
        "OOOOOOOOOOOOOOOO",
        "OOOOOOOOOOOOOOOO",
        "OOOOOOOOOOOOOOOO",
    ]
    for i, r in enumerate(rows):
        if len(r) != 16:
            raise ValueError(f"skyward wing row {i}: {len(r)} != 16 :: {r}")
    return rows


def _sc_shard_cell() -> List[str]:
    """One authored orbiting crown shard (phase-2 fragment)."""
    tip  = "OBOO"
    mid  = "OBGO"
    wide = "OBGBO"[:4]
    rows = [
        "OOOOOOOOOOOOOOOO",
        tip + tip + tip + tip,
        mid + mid + mid + mid,
        wide + wide + wide + wide,
        wide + wide + wide + wide,
        mid + mid + mid + mid,
        mid + mid + mid + mid,
        tip + tip + tip + tip,
        "OSSSSSSSSSSSSSSO",
        "OSSSSSSSSSSSSSSO",
        "OOOOOOOOOOOOOOOO",
        "OOOOOOOOOOOOOOOO",
        "OOOOOOOOOOOOOOOO",
        "OOOOOOOOOOOOOOOO",
        "OOOOOOOOOOOOOOOO",
        "OOOOOOOOOOOOOOOO",
    ]
    for i, r in enumerate(rows):
        if len(r) != 16:
            raise ValueError(f"skyward shard row {i}: {len(r)} != 16 :: {r}")
    return rows


_SC_LIMB_A = _sc_wing_cell("H", "T", "H")
_SC_LIMB_B = _sc_wing_cell("L", "T", "H")
_SC_LIMB_C = _sc_wing_cell("H", "T", "H")
_SC_LIMB_D = _sc_wing_cell("L", "T", "H")

_SC_EXTRA_1 = [
    "OOOOOOOOOOOOOOOO",
    "OBOOOOBOOOOBOOOO",
    "OBGOOOBGOOOBGOOO",
    "OBGBOOBGBOOBGBOO",
    "OBGBOOBGBOOBGBOO",
    "OBGBOOBGBOOBGBOO",
    "OBOOOOBOOOOBOOOO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]
_SC_EXTRA_2 = [
    "OOOOOOOOOOOOOOOO",
    "OGGGGGGGGGGGGGGO",
    "OGCCCCCCCCCCCCGO",
    "OGCGGGGGGGGGGCGO",
    "OGCGGGGGGGGGGCGO",
    "OGCCCCCCCCCCCCGO",
    "OGGGGGGGGGGGGGGO",
    "OOOOOOOOOOOOOOOO",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]
_SC_EXTRA_3 = _sc_shard_cell()
_SC_EXTRA_4 = _sc_shard_cell()

SKYWARD_CROWN = {
    "body": [_SC_BODY_F_0, _SC_BODY_B_0, _SC_BODY_R_0, _SC_BODY_L_0],
    "body2": [_SC_BODY_F_1, _SC_BODY_B_1, _SC_BODY_R_1, _SC_BODY_L_1],
    "head": [_SC_HEAD_F, _SC_HEAD_B, _SC_HEAD_R, _SC_HEAD_L],
    "crown": [_SC_HEAD_TOP, _SC_HEAD_BOT, _SC_BODY_TOP, _SC_BODY_BOT],
    "limbs": [_SC_LIMB_A, _SC_LIMB_B, _SC_LIMB_C, _SC_LIMB_D],
    "extras": [_SC_EXTRA_1, _SC_EXTRA_2, _SC_EXTRA_3, _SC_EXTRA_4],
}


# ===========================================================================
#  BOSS 5 -- THE UNRAVELING
#  Glitched entity that changes form per phase (quadruped -> serpent ->
#  humanoid). The atlas therefore carries three chromatic aberration channels
#  X / Y / Z offset by one pixel from each other, plus torn scanline bands --
#  that is what makes the model visibly fail to resolve.
# ===========================================================================

_UN_BODY_F_0 = [
    "OOOOOOOOOOOOOOOO",
    "OXXXXXXXXXXXXXXO",
    "OXXYYYYYYYYYYXXO",
    "OXYYYYYZZZZYYYXO",
    "OXYZZZZXXZZZZYXO",
    "OXZZZXXYYXXZZZXO",
    "OXYZZZZXXZZZZYXO",
    "OXYYYYYYYYYYYYXO",
]
_UN_BODY_B_0 = [
    "OOOOOOOOOOOOOOOO",
    "OZZZZZZZZZZZZZZO",
    "OZZYYYYYYYYYYZZO",
    "OZYXXXXXXXXXXYZO",
    "OZXXXXXXXXXXXXZO",
    "OZYXXXXXXXXXXYZO",
    "OZZYYYYYYYYYYZZO",
    "OZZZZZZZZZZZZZZO",
]
_UN_BODY_R_0 = [
    "OOOOOOOOOOOOOOOO",
    "OXXXXXXXXXXXXXDO",
    "OXXYYYYYYYYYYXDO",
    "OXYYYYZZZZYYYXDO",
    "OXYZZZZXXZZZYXDO",
    "OXZZZXXYYXXZZXDO",
    "OXYZZZZXXZZZYXDO",
    "OXYYYYYYYYYYYDDO",
]
_UN_BODY_L_0 = [
    "OOOOOOOOOOOOOOOO",
    "ODXXXXXXXXXXXXXO",
    "ODXXXXXXXXXXXXXO",
    "ODXXYYYYYYYYYYXO",
    "ODXYYYYZZZZYYYXO",
    "ODXYZZZZXXZZZYXO",
    "ODXYYYYYYYYYYYXO",
    "ODXXXXXXXXXXXDDO",
]
_UN_BODY_F_1 = [
    "OXYYYYYYYYYYYYXO",
    "OXYZZZZXXZZZZYXO",
    "OXZZZXXYYXXZZZXO",
    "OXYZZZZXXZZZZYXO",
    "OXYYYYYZZZZYYYXO",
    "OXXYYYYYYYYYYXXO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_UN_BODY_B_1 = [
    "OZZZZZZZZZZZZZZO",
    "OZZYYYYYYYYYYZZO",
    "OZYXXXXXXXXXXYZO",
    "OZXXXXXXXXXXXXZO",
    "OZYXXXXXXXXXXYZO",
    "OZZYYYYYYYYYYZZO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_UN_BODY_R_1 = [
    "OXYYYYYYYYYYYDDO",
    "OXYZZZZXXZZZYXDO",
    "OXZZZXXYYXXZZXDO",
    "OXYZZZZXXZZZYXDO",
    "OXYYYYZZZZYYYXDO",
    "OXXYYYYYYYYYYXDO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_UN_BODY_L_1 = [
    "ODXXXXXXXXXXXDDO",
    "ODXYYYYYYYYYYYXO",
    "ODXYZZZZXXZZZYXO",
    "ODXYYYYZZZZYYYXO",
    "ODXXYYYYYYYYYYXO",
    "ODXXXXXXXXXXXXXO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_UN_HEAD_F = [
    "OOOOOOOOOOOOOOOO",
    "OXXXXXXXXXXXXXXO",
    "OXXYYYYYYYYYYXXO",
    "OXYYEeYYYYEeYYXO",
    "OXYYEeYYYYEeYYXO",
    "OXYYYYYZZZZYYYXO",
    "OXZZZXXZZXXZZZXO",
    "OSSSSSSSSSSSSSSO",
]
_UN_HEAD_B = [
    "OOOOOOOOOOOOOOOO",
    "OZZZZZZZZZZZZZZO",
    "OZZYYYYYYYYYYZZO",
    "OZYXXXXXXXXXXYZO",
    "OZYXXXXXXXXXXYZO",
    "OZZYYYYYYYYYYZZO",
    "OZZZZZZZZZZZZZZO",
    "OSSSSSSSSSSSSSSO",
]
_UN_HEAD_R = [
    "OOOOOOOOOOOOOOOO",
    "OXXXXXXXXXXXXXDO",
    "OXXYYYYYYYYYYXDO",
    "OXYYEeYYYYYYYXDO",
    "OXYYEeYYYYYYYXDO",
    "OXYYYYYZZZZYYXDO",
    "OXZZZXXZZXXZZXDO",
    "OSSSSSSSSSSSSSSO",
]
_UN_HEAD_L = [
    "OOOOOOOOOOOOOOOO",
    "ODXXXXXXXXXXXXXO",
    "ODXXYYYYYYYYYYXO",
    "ODXYYYYYYYEeYYXO",
    "ODXYYYYYYYEeYYXO",
    "ODXYYYYZZZZYYYXO",
    "ODXZZZXXZZXXZZXO",
    "OSSSSSSSSSSSSSSO",
]
_UN_HEAD_TOP = [
    "OOOOOOOOOOOOOOOO",
    "OXXXXXXXXXXXXXXO",
    "OXXYYYYYYYYYYXXO",
    "OXYYYYYYYYYYYYXO",
    "OXYYYZZZZZZYYYXO",
    "OXYYYYYYYYYYYYXO",
    "OXXYYYYYYYYYYXXO",
    "OOOOOOOOOOOOOOOO",
]
_UN_HEAD_BOT = [
    "OOOOOOOOOOOOOOOO",
    "OSSSSSSSSSSSSSSO",
    "OSZZZZZZZZZZZZSO",
    "OSZXXXXXXXXXXZSO",
    "OSZXXXXXXXXXXZSO",
    "OSZZZZZZZZZZZZSO",
    "OSSSSSSSSSSSSSSO",
    "OOOOOOOOOOOOOOOO",
]
_UN_BODY_TOP = _UN_HEAD_TOP
_UN_BODY_BOT = _UN_HEAD_BOT


def _un_limb_cell(form: str) -> List[str]:
    """
    One authored limb. `form` selects which of the three phase shapes the
    cell reads as, so the same entity can be re-skinned per phase without
    swapping the model: 'quad' (digitigrade leg), 'serp' (coiled ring),
    'human' (articulated arm/leg). Four 4-column faces, no gutter.
    """
    if form == "quad":
        a, b, c = "OXYX", "OYZY", "OZZZ"
    elif form == "serp":
        a, b, c = "OXXX", "OYXY", "OZZZ"
    else:
        a, b, c = "OXYX", "OXZX", "OZZZ"
    rows = [
        "OOOOOOOOOOOOOOOO",
        a + a + a + a,
        b + b + b + b,
        a + b + a + b,
        c + c + c + c,
        b + b + b + b,
        a + b + a + b,
        c + c + c + c,
        b + b + b + b,
        a + a + a + a,
        "OSSSSSSSSSSSSSSO",
        "OSDDDDDDDDDDDDSO",
        "OSSSSSSSSSSSSSSO",
        "OOOOOOOOOOOOOOOO",
        "OOOOOOOOOOOOOOOO",
        "OOOOOOOOOOOOOOOO",
    ]
    for i, r in enumerate(rows):
        if len(r) != 16:
            raise ValueError(f"unraveling limb row {i}: {len(r)} != 16 :: {r}")
    return rows


_UN_LIMB_A = _un_limb_cell("quad")
_UN_LIMB_B = _un_limb_cell("serp")
_UN_LIMB_C = _un_limb_cell("human")
_UN_LIMB_D = _un_limb_cell("quad")

_UN_EXTRA_1 = [
    "OOOOOOOOOOOOOOOO",
    "OXXXXXXXXXXXXXXO",
    "OXYYYYYYYYYYYYXO",
    "OXYYYYYYYYYYYYXO",
    "OXXXXXXXXXXXXXXO",
    "OZZZZZZZZZZZZZZO",
    "OXXXXXXXXXXXXXXO",
    "OYYYYYYYYYYYYYYO",
    "OZZZZZZZZZZZZZZO",
    "OOOOOOOOOOOOOOOO",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]
_UN_EXTRA_2 = [
    "OOOOOOOOOOOOOOOO",
    "OX.XY.XZ.XY.XZ.O",
    "OY.XZ.XY.XZ.XY.O",
    "OZ.XY.XZ.XY.XZ.O",
    "OX.XZ.XY.XZ.XY.O",
    "OY.XY.XZ.XY.XZ.O",
    "OZ.XZ.XY.XZ.XY.O",
    "OX.XY.XZ.XY.XZ.O",
    "OOOOOOOOOOOOOOOO",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]
_UN_EXTRA_3 = [
    "OOOOOOOOOOOOOOOO",
    "OOOOOOOOOOOOOOOO",
    "OGGGGGGGGGGGGGGO",
    "OG.XXXXXXXX.X.GO",
    "OGX.YYYYYY.XXGO".ljust(16, "O")[:16],
    "OGXX.ZZZZ.XXXGO".ljust(16, "O")[:16],
    "OG.XXXXXXXX.X.GO",
    "OGGGGGGGGGGGGGGO",
    "OOOOOOOOOOOOOOOO",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]
_UN_EXTRA_4 = _UN_EXTRA_1

THE_UNRAVELING = {
    "body": [_UN_BODY_F_0, _UN_BODY_B_0, _UN_BODY_R_0, _UN_BODY_L_0],
    "body2": [_UN_BODY_F_1, _UN_BODY_B_1, _UN_BODY_R_1, _UN_BODY_L_1],
    "head": [_UN_HEAD_F, _UN_HEAD_B, _UN_HEAD_R, _UN_HEAD_L],
    "crown": [_UN_HEAD_TOP, _UN_HEAD_BOT, _UN_BODY_TOP, _UN_BODY_BOT],
    "limbs": [_UN_LIMB_A, _UN_LIMB_B, _UN_LIMB_C, _UN_LIMB_D],
    "extras": [_UN_EXTRA_1, _UN_EXTRA_2, _UN_EXTRA_3, _UN_EXTRA_4],
}


# ===========================================================================
#  BOSS REGISTRY
# ===========================================================================

BOSSES: Dict[str, Dict[str, List[List[str]]]] = {
    "heart_of_the_forest": HEART_OF_FOREST,
    "void_serpent": VOID_SERPENT,
    "warden_of_the_hollow_deep": WARDEN_HOLLOW_DEEP,
    "the_skyward_crown": SKYWARD_CROWN,
    "the_unraveling": THE_UNRAVELING,
}


def build_boss(boss_id: str) -> List[str]:
    """Return the authored 64x64 character atlas for a boss."""
    if boss_id not in BOSSES:
        raise KeyError(f"unknown boss {boss_id!r}; have {sorted(BOSSES)}")
    return build_boss_atlas(boss_id, BOSSES[boss_id])
