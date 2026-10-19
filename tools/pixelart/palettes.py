"""
pixelart/palettes.py -- Curated colour ramps.

Every ramp is art-directed by hand: a deep outline tone, an ambient-occlusion
tone, two to three mid body tones, a key-light tone and a specular highlight.
Key light is always assumed to come from the TOP-LEFT, so the highlight glyphs
are authored into the top-left of every map.

Glyph vocabulary used across the base maps
------------------------------------------
    H  specular highlight          (top-left facets, wet edges)
    L  key light                   (lit faces)
    M  mid / body tone             (majority of the surface)
    D  form shadow                 (turning-away faces)
    S  ambient occlusion           (crevices, under overhangs)
    O  outline                     (1px dark contour, nearly black)
    G  emissive core               (glowstones, eyes, runes)
    g  emissive falloff            (halo around G)
    .  transparent
"""

from __future__ import annotations

from typing import Dict

# ---------------------------------------------------------------------------
#  STONE / ROCK BODY RAMPS  (5 stone types per dimension family)
# ---------------------------------------------------------------------------

STONE_RAMPS: Dict[str, Dict[str, str]] = {
    # --- Overworld --------------------------------------------------------
    "umberstone": {
        "H": "#9C8D7A", "L": "#7E7061", "M": "#655A4E",
        "D": "#4E463D", "S": "#3A342D", "O": "#221E1A",
    },
    "mossy_umberstone": {
        "H": "#8FA06B", "L": "#6E8355", "M": "#5A6B49",
        "D": "#454F3A", "S": "#333A2C", "O": "#1D2119",
    },
    "verdant_stone": {
        "H": "#7FC9A2", "L": "#57A87F", "M": "#418A66",
        "D": "#2F6A4E", "S": "#224E3A", "O": "#132C21",
    },
    "ashen_stone": {
        "H": "#9E9A96", "L": "#7C7873", "M": "#615D59",
        "D": "#494643", "S": "#353330", "O": "#1F1E1C",
    },
    "sunbleached_stone": {
        "H": "#EFE3C6", "L": "#D6C7A6", "M": "#BBA98A",
        "D": "#9A8A6E", "S": "#7A6C55", "O": "#4A4132",
    },
    "petrified_wood": {
        "H": "#B39A78", "L": "#937C5D", "M": "#756049",
        "D": "#5A4836", "S": "#42342686", "O": "#241B12",
    },
    # --- The Hollow Deep (bioluminescent subterranea) ---------------------
    "hollow_stone": {
        "H": "#6FA8B8", "L": "#4E7F92", "M": "#3A6273",
        "D": "#2A4957", "S": "#1D333E", "O": "#0F1B22",
    },
    "mycelial_slimestone": {
        "H": "#8FBF7A", "L": "#6A9A5C", "M": "#4F7746",
        "D": "#3A5A35", "S": "#284026", "O": "#152315",
    },
    "gloomslate": {
        "H": "#5C5A78", "L": "#464460", "M": "#34324A",
        "D": "#252338", "S": "#191828", "O": "#0C0B15",
    },
    "spore_chalk": {
        "H": "#E4E8D2", "L": "#C6CBB2", "M": "#A6AC93",
        "D": "#838873", "S": "#636756", "O": "#3A3D32",
    },
    "basaltic_hollowstone": {
        "H": "#6B6570", "L": "#524C58", "M": "#3E3943",
        "D": "#2C2830", "S": "#1E1B22", "O": "#100E13",
    },
    # --- Aetherfall (celestial twilight) ----------------------------------
    "aetherstone": {
        "H": "#DCE9FF", "L": "#B7CBEE", "M": "#93ABD8",
        "D": "#7189B8", "S": "#556A96", "O": "#31405C",
    },
    "dawn_marble": {
        "H": "#FFEFD9", "L": "#F6D7B0", "M": "#E0BB8E",
        "D": "#BE9A70", "S": "#987956", "O": "#5C4832",
    },
    "cloudstone": {
        "H": "#FFFFFF", "L": "#E8EFFA", "M": "#CBD8EC",
        "D": "#A9BAD6", "S": "#8598BC", "O": "#4F5D7A",
    },
    "twilight_shale": {
        "H": "#9C8FD1", "L": "#7C6FB4", "M": "#5F5394",
        "D": "#473D74", "S": "#322B57", "O": "#1B1733",
    },
    "gilded_aetherstone": {
        "H": "#FFE9A8", "L": "#E8C86F", "M": "#C7A44C",
        "D": "#9E7F38", "S": "#77602A", "O": "#463716",
    },
    # --- The Void Between (fractured reality) -----------------------------
    "voidstone": {
        "H": "#4B2E63", "L": "#39224C", "M": "#291739",
        "D": "#1C0F29", "S": "#120A1C", "O": "#07040D",
    },
    "fracture_shale": {
        "H": "#7A5FA8", "L": "#5D4588", "M": "#452F6B",
        "D": "#31204F", "S": "#211538", "O": "#100A1F",
    },
    "static_stone": {
        "H": "#B9F5E6", "L": "#84D6C4", "M": "#57AFA0",
        "D": "#3C877C", "S": "#296059", "O": "#153430",
    },
    "glitch_concrete": {
        "H": "#FF6FB5", "L": "#E14A97", "M": "#B32F77",
        "D": "#8A2059", "S": "#5F143D", "O": "#330A21",
    },
    "null_basalt": {
        "H": "#3C3C46", "L": "#2E2E37", "M": "#222229",
        "D": "#17171D", "S": "#0F0F14", "O": "#06060A",
    },
}

# ---------------------------------------------------------------------------
#  MINERAL RAMPS  (ore veins: 20 Overworld + 24 dimension ores)
#  Each ramp: C = emissive/specular core, H highlight, L key light,
#             M mid, D form shadow, S ambient occlusion inside the vein.
# ---------------------------------------------------------------------------

MINERAL_RAMPS: Dict[str, Dict[str, str]] = {
    "lumenite":    {"C": "#FFFFFF", "H": "#FFF6C2", "L": "#FFE066", "M": "#E0B12E", "D": "#A87C18", "S": "#6E4F0C"},
    "umbrite":     {"C": "#C7B49A", "H": "#A08B6E", "L": "#7E6B52", "M": "#5D4C39", "D": "#403426", "S": "#262016"},
    "petrichorite":{"C": "#D9F2FF", "H": "#A9DCF5", "L": "#74BEE4", "M": "#4E97C4", "D": "#35709B", "S": "#1F4A6B"},
    "sunscorch":   {"C": "#FFF2B0", "H": "#FFD35C", "L": "#FFA92B", "M": "#E27C12", "D": "#A8520A", "S": "#6E3306"},
    "glimmerleaf": {"C": "#E8FFD0", "H": "#B6F28C", "L": "#7FD95A", "M": "#4FAE37", "D": "#2F7D22", "S": "#1A4F13"},
    "tideglass":   {"C": "#EAFDFF", "H": "#B2EEF7", "L": "#79D6E8", "M": "#4BACC6", "D": "#2E839E", "S": "#1A566B"},
    "emberquartz": {"C": "#FFE2C0", "H": "#FF9E5C", "L": "#F26A28", "M": "#C4421A", "D": "#8E2A0F", "S": "#5A1808"},
    "frostbloom":  {"C": "#FFFFFF", "H": "#DFF4FF", "L": "#AFDCFA", "M": "#7BB8E8", "D": "#4F8CC0", "S": "#2C5F8C"},
    "sporeamber":  {"C": "#FFF0B8", "H": "#F0C86A", "L": "#D09A34", "M": "#A26F1E", "D": "#734C12", "S": "#452C09"},
    "hollowite":   {"C": "#C8FFF4", "H": "#7CF0DC", "L": "#3FCDB4", "M": "#229E8B", "D": "#147164", "S": "#0A463E"},
    "mycelium_ore":{"C": "#E6FFC8", "H": "#BEE894", "L": "#93C863", "M": "#6B9E42", "D": "#48702B", "S": "#294417"},
    "gloomite":    {"C": "#C8B4FF", "H": "#9C82F0", "L": "#7355D1", "M": "#52379F", "D": "#372373", "S": "#1F1248"},
    "deep_pearl":  {"C": "#FFFFFF", "H": "#F2E8FA", "L": "#D8C6EC", "M": "#B49BD1", "D": "#8A72AB", "S": "#5C4A7C"},
    "lumenshade":  {"C": "#FFFBE0", "H": "#EAF3A8", "L": "#C4DE63", "M": "#96B83C", "D": "#6C8B26", "S": "#455E14"},
    "rootiron":    {"C": "#E8C9A8", "H": "#C49A72", "L": "#9C7250", "M": "#74503A", "D": "#4F3527", "S": "#2E1E16"},
    "chronosite":  {"C": "#E8FFFF", "H": "#A8E8E8", "L": "#69C3C9", "M": "#3E96A2", "D": "#266D79", "S": "#13454F"},
    "pyroclast":   {"C": "#FFE0A0", "H": "#FF8A3C", "L": "#E84E18", "M": "#B22A0C", "D": "#7C1806", "S": "#4A0D03"},
    "aetherium":   {"C": "#FFFFFF", "H": "#DCEBFF", "L": "#A9C8FF", "M": "#7399EE", "D": "#4C6DC4", "S": "#2A428C"},
    "voidsteel":   {"C": "#B98CFF", "H": "#8A54D6", "L": "#63349F", "M": "#442073", "D": "#2B114C", "S": "#170729"},
    "nullite":     {"C": "#FFFFFF", "H": "#FF6FD8", "L": "#E0309F", "M": "#A81A73", "D": "#770C4F", "S": "#46052C"},
    "staticite":   {"C": "#EAFFFF", "H": "#9DF7E4", "L": "#54D8BE", "M": "#2CA992", "D": "#177B69", "S": "#0A4C41"},
    "skylead":     {"C": "#F2F7FF", "H": "#C6D6EE", "L": "#93AED6", "M": "#6580AE", "D": "#415A85", "S": "#233859"},
    "dawnshard":   {"C": "#FFF6DC", "H": "#FFE0A0", "L": "#FBC563", "M": "#E29E33", "D": "#B0741C", "S": "#7A4C0D"},
    "wraithsalt":  {"C": "#FFFFFF", "H": "#E4E9F5", "L": "#BFC8DE", "M": "#939FBE", "D": "#69759A", "S": "#414B70"},
    "bloomglass":  {"C": "#FFF0FA", "H": "#FFC4E8", "L": "#F58CCB", "M": "#D25CA6", "D": "#A03A7C", "S": "#6B2152"},
    "graveamber":  {"C": "#F5E0B0", "H": "#D2AE6E", "L": "#A98043", "M": "#7E5A2A", "D": "#573C18", "S": "#33210A"},
    "titanite":    {"C": "#DCE8EE", "H": "#A8BECB", "L": "#7A96A8", "M": "#537084", "D": "#354F61", "S": "#1D3241"},
    "spiritwood":  {"C": "#E8F7D8", "H": "#BFE0A4", "L": "#94C076", "M": "#6B9850", "D": "#466E33", "S": "#26431B"},
    "moonpetal":   {"C": "#F4F0FF", "H": "#D6CCF5", "L": "#AE9EE0", "M": "#8471BE", "D": "#5C4B94", "S": "#352A66"},
    "sunspore":    {"C": "#FFFAD2", "H": "#FFEC8A", "L": "#FFD247", "M": "#E8A81E", "D": "#B47B0F", "S": "#7A5106"},
    "frostvein":   {"C": "#F0FFFF", "H": "#C2EFFF", "L": "#8FD4F5", "M": "#5FA9DC", "D": "#3A7CB0", "S": "#1F5280"},
    "ashen_core":  {"C": "#FFD9A8", "H": "#D98C4E", "L": "#A85C2A", "M": "#7A3C18", "D": "#51240D", "S": "#2E1306"},
    "root_heart":  {"C": "#D8FFC0", "H": "#9EE87E", "L": "#6CC24E", "M": "#459630", "D": "#2A6A1C", "S": "#15400D"},
    "echo_crystal":{"C": "#E0FFFF", "H": "#A0E8F0", "L": "#63C0D4", "M": "#3A90A8", "D": "#216478", "S": "#0F3D4C"},
    "witherite":   {"C": "#C8C0D8", "H": "#948AA8", "L": "#6B6180", "M": "#48405A", "D": "#2C2738", "S": "#15121E"},
    "stormcell":   {"C": "#F2FFFF", "H": "#A8E8FF", "L": "#5FC0F0", "M": "#2E8FCB", "D": "#18649B", "S": "#0A3E6B"},
    "glacierite":  {"C": "#FFFFFF", "H": "#D8F2FF", "L": "#A6DCF5", "M": "#6FB6E0", "D": "#4388B8", "S": "#225C88"},
    "bloodstone":  {"C": "#FFC0B0", "H": "#E06A52", "L": "#B23327", "M": "#851B14", "D": "#5A0E0A", "S": "#330504"},
    "duskite":     {"C": "#F0D8FF", "H": "#C79CE8", "L": "#9A67C8", "M": "#6F439E", "D": "#4A2873", "S": "#291348"},
    "coralite":    {"C": "#FFE8E0", "H": "#FFB0A0", "L": "#F07A6C", "M": "#C74E45", "D": "#952F2B", "S": "#611A18"},
    "kelpstone":   {"C": "#E0FFC8", "H": "#A8E88A", "L": "#71C255", "M": "#489636", "D": "#2B6A20", "S": "#143F0F"},
    "abyssite":    {"C": "#A8C8FF", "H": "#6A8FE0", "L": "#4260B8", "M": "#273F8C", "D": "#152861", "S": "#08163A"},
    "fracture_shale": {"C": "#C8B4E8", "H": "#9A86C4", "L": "#715C9C", "M": "#4E3C74", "D": "#32254F", "S": "#1B1230"},
    "starfall":    {"C": "#FFFFFF", "H": "#FFF0C8", "L": "#FFD98A", "M": "#E8B452", "D": "#B8852C", "S": "#805814"},
    "runeglass":   {"C": "#E8FFFF", "H": "#B0F0E8", "L": "#70D0C8", "M": "#42A5A0", "D": "#257874", "S": "#114C49"},
}

# ---------------------------------------------------------------------------
#  METAL / GEAR RAMPS  (tools + armour: handle, guard, blade/plate, edge)
# ---------------------------------------------------------------------------

GEAR_RAMPS: Dict[str, Dict[str, str]] = {
    # glyph: W = wood/handle highlight, w = handle mid, K = handle shadow
    #        H = metal highlight, L = metal key light, M = metal mid,
    #        D = metal form shadow, S = metal AO, O = outline
    #        E = cutting edge / specular, G = emissive inlay
    "lumenshade": {
        "W": "#D9C48A", "w": "#A88F55", "K": "#6E5B31",
        "H": "#FFFBE0", "L": "#E4EEA0", "M": "#B4CB5E", "D": "#829C38",
        "S": "#5A7022", "O": "#2C3810", "E": "#FFFFFF", "G": "#F6FFB0",
    },
    "voidstone": {
        "W": "#5A3E7A", "w": "#3E2A59", "K": "#241638",
        "H": "#C79CFF", "L": "#9A66E8", "M": "#6C3CB8", "D": "#472285",
        "S": "#2B1257", "O": "#140630", "E": "#E8CFFF", "G": "#B98CFF",
    },
    "aetherium": {
        "W": "#E8E0C8", "w": "#BDB296", "K": "#8A8068",
        "H": "#FFFFFF", "L": "#D8E6FF", "M": "#A2BFF0", "D": "#6F92CC",
        "S": "#47649E", "O": "#233861", "E": "#FFFFFF", "G": "#C8DEFF",
    },
    "chronos": {
        "W": "#8FB8A8", "w": "#648E80", "K": "#3E5D53",
        "H": "#E0FFFF", "L": "#A8E4E0", "M": "#6FBDBB", "D": "#459094",
        "S": "#27656C", "O": "#113B41", "E": "#F2FFFF", "G": "#9DF7E4",
    },
    "pyroclast": {
        "W": "#5C3A24", "w": "#3E2517", "K": "#241409",
        "H": "#FFD9A0", "L": "#FF9A45", "M": "#DE5F1A", "D": "#A83A0B",
        "S": "#722205", "O": "#3A0F02", "E": "#FFF0C0", "G": "#FF7A28",
    },
    "hollowite": {
        "W": "#2F5D63", "w": "#1F4349", "K": "#112B30",
        "H": "#B8FFF0", "L": "#72E8D4", "M": "#39BFAA", "D": "#1F9080",
        "S": "#0F6357", "O": "#053730", "E": "#DFFFF8", "G": "#7CF0DC",
    },
    "rootiron": {
        "W": "#7A5334", "w": "#573A23", "K": "#34210F",
        "H": "#E0BE96", "L": "#B98F63", "M": "#8E6844", "D": "#63452A",
        "S": "#3F2B18", "O": "#1F140A", "E": "#F5DCBB", "G": "#C89A6A",
    },
    "gloomsteel": {
        "W": "#4A3D63", "w": "#332A47", "K": "#1D1729",
        "H": "#9C93C4", "L": "#756AA0", "M": "#544A78", "D": "#383054",
        "S": "#221D38", "O": "#100D1E", "E": "#C0B8E0", "G": "#8A7FD1",
    },
    "nullite": {
        "W": "#3A2440", "w": "#26172B", "K": "#130A17",
        "H": "#FF9FE0", "L": "#E058B8", "M": "#B02C8C", "D": "#7E1862",
        "S": "#4F0B3D", "O": "#260320", "E": "#FFD0F0", "G": "#FF6FD8",
    },
    "starforged": {
        "W": "#C9B48A", "w": "#9C8860", "K": "#6A5A3A",
        "H": "#FFFFFF", "L": "#FFF2C0", "M": "#F0D478", "D": "#C0A044",
        "S": "#8A7026", "O": "#4A3A10", "E": "#FFFFFF", "G": "#FFFAD2",
    },
}

# ---------------------------------------------------------------------------
#  ORGANIC RAMPS  (grass, leaves, logs, flora, fungi)
# ---------------------------------------------------------------------------

ORGANIC_RAMPS: Dict[str, Dict[str, str]] = {
    "lumen_grass":  {"H": "#C8F5A0", "L": "#8FD96A", "M": "#5FB044", "D": "#3D8530", "S": "#245A1D", "O": "#113310"},
    "petrified_grass": {"H": "#C8B48E", "L": "#A08A64", "M": "#7C6844", "D": "#584830", "S": "#382D1D", "O": "#1C160E"},
    "crystal_grass": {"H": "#D8F0FF", "L": "#A8D4F0", "M": "#74AED8", "D": "#4C85AE", "S": "#2C5C80", "O": "#15324A"},
    "spore_grass":  {"H": "#D8E8A0", "L": "#B0C870", "M": "#87A04C", "D": "#5F7832", "S": "#3D5220", "O": "#1E2B10"},
    "hollow_grass": {"H": "#8FE8D0", "L": "#57C0A8", "M": "#339582", "D": "#1E6E5F", "S": "#0F4A40", "O": "#052621"},
    "aether_grass": {"H": "#E0ECFF", "L": "#B4C8EE", "M": "#8AA2D6", "D": "#6179AE", "S": "#3D5183", "O": "#1E2A4C"},
    "void_grass":   {"H": "#8A5FC0", "L": "#66409A", "M": "#472A73", "D": "#2E1A4F", "S": "#1B0E33", "O": "#0C051C"},
    "ash_grass":    {"H": "#B8B0A4", "L": "#928A7E", "M": "#6E665C", "D": "#4C453C", "S": "#2F2A24", "O": "#16130F"},

    "lumen_leaves": {"H": "#B8F08A", "L": "#82CC5C", "M": "#549E3A", "D": "#356F24", "S": "#1C4513", "O": "#0B2509"},
    "petrified_leaves": {"H": "#D0BC96", "L": "#A89270", "M": "#806A4C", "D": "#5A4832", "S": "#382C1D", "O": "#1A130C"},
    "crystal_leaves": {"H": "#CDEBFF", "L": "#9AC8EE", "M": "#6A9FD4", "D": "#4375A8", "S": "#244F7A", "O": "#0F2A47"},
    "hollow_leaves": {"H": "#7AE0C8", "L": "#48B8A0", "M": "#268C79", "D": "#136455", "S": "#084139", "O": "#02211D"},
    "aether_leaves": {"H": "#DCE6FF", "L": "#AFC2F0", "M": "#7E96D8", "D": "#546FB0", "S": "#31498A", "O": "#17264F"},
    "void_leaves": {"H": "#7E4FB8", "L": "#5B3392", "M": "#3D206B", "D": "#26124A", "S": "#150930", "O": "#08031A"},

    "lumen_log":    {"H": "#A88A5C", "L": "#836A42", "M": "#5F4B2D", "D": "#41321D", "S": "#261C10", "O": "#100B05"},
    "petrified_log":{"H": "#B8A484", "L": "#94805F", "M": "#6E5C41", "D": "#4B3D2A", "S": "#2C2317", "O": "#140F09"},
    "hollow_log":   {"H": "#4E7A78", "L": "#385C5B", "M": "#254140", "D": "#152B2B", "S": "#0A1A1A", "O": "#030B0B"},
    "aether_log":   {"H": "#B8C4DC", "L": "#929FBC", "M": "#6C7896", "D": "#495270", "S": "#2B314C", "O": "#141829"},
    "void_log":     {"H": "#4A3168", "L": "#36234D", "M": "#241636", "D": "#150C21", "S": "#0A0513", "O": "#040208"},

    "glowcap":      {"H": "#C8FFF0", "L": "#7CE8D0", "M": "#3CBBA4", "D": "#1F8C7A", "S": "#0E5E52", "O": "#04302A"},
    "sporecap":     {"H": "#F0E0A0", "L": "#D0B868", "M": "#A58C42", "D": "#77622A", "S": "#4B3C16", "O": "#241B08"},
    "bloodcap":     {"H": "#FFB0A0", "L": "#E0685A", "M": "#B0382E", "D": "#7E1F19", "S": "#500E0A", "O": "#260504"},
    "voidcap":      {"H": "#B98CFF", "L": "#8A54D6", "M": "#63349F", "D": "#442073", "S": "#2B114C", "O": "#170729"},
}

# ---------------------------------------------------------------------------
#  MOB SKIN RAMPS  (used by the creature base maps + per-species palettes)
# ---------------------------------------------------------------------------

def creature_ramp(skin: str, hide: str, accent: str, eye: str, bone: str = "#E8DCC0") -> Dict[str, str]:
    """
    Build the glyph set expected by the creature base maps from five
    art-directed colours. The ramp order (H -> O) is a hand-chosen tonal
    progression, not a computed gradient.
    """
    return {
        "H": skin, "L": hide, "M": hide, "D": hide, "S": hide, "O": hide,
        "A": accent, "a": accent, "E": eye, "e": eye, "B": bone,
    }


__all__ = [
    "STONE_RAMPS",
    "MINERAL_RAMPS",
    "GEAR_RAMPS",
    "ORGANIC_RAMPS",
    "creature_ramp",
]
