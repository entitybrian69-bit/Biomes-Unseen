#!/usr/bin/env python3
"""
tools/generate_textures.py -- encode hand-authored pixel matrices into PNGs.

This script contains NO drawing logic and NO shape primitives. It is a
resolver: it walks the content tables, picks the hand-authored character map
and the curated colour ramp that art direction assigned to each asset, and
serialises the result to a real PNG via png_codec.encode_png.

Every pixel that ends up in a PNG was placed by hand in one of:

    tools/pixelart/base_maps.py       blocks (stone, ore, grass, wood, leaves,
                                      flora, fluids, portals, special blocks)
    tools/pixelart/gear_maps.py       tools, armour, staves, bows
    tools/pixelart/items_maps.py      ingots, gems, shards, dusts, drops, lore
    tools/pixelart/creature_maps.py   64x32 GeckoLib mob atlases (6 families)
    tools/pixelart/boss_maps.py       64x64 GeckoLib boss atlases (5 bosses)

Run:
    python3 tools/generate_textures.py            # write all PNGs
    python3 tools/generate_textures.py --check    # verify only, write nothing
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Dict, List, Optional, Sequence, Set, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from png_codec import encode_png, png_dimensions  # noqa: E402
from pixelart.engine import (  # noqa: E402
    TRANSPARENT,
    compose,
    hex_to_pixel,
    map_to_matrix,
    place_overlay,
)
from pixelart import base_maps, boss_maps, creature_maps, gear_maps, items_maps, palettes  # noqa: E402
from content import biomes as BIOMES  # noqa: E402
from content import bosses as BOSSES  # noqa: E402
from content import gear as GEAR  # noqa: E402
from content import mobs as MOBS  # noqa: E402
from content import ores as ORES  # noqa: E402

MODID = "biomesunseen"
ASSETS = os.path.join(ROOT, "src", "main", "resources", "assets", MODID)

# ---------------------------------------------------------------------------
#  Palette resolution
#  A "glyph set" is a plain dict glyph -> hex colour. Nothing here computes a
#  colour: every value comes from a curated ramp in pixelart/palettes.py.
# ---------------------------------------------------------------------------

# Curated 1px outline tone shared by all item icons. Hand-chosen, not derived.
ITEM_OUTLINE = "#16110D"

# Curated emissive tone for gilded/inlaid detail on organic items.
FLORA_EMISSIVE = "#FFE9A8"

BOSS_EXTRA_GLYPHS = {
    # The Unraveling's three chromatic-aberration channels.
    "X": "#FF3C8C",
    "Y": "#3CFFD8",
    "Z": "#C83CFF",
}


def _complete(glyphs: Dict[str, str], ramp: Dict[str, str]) -> Dict[str, str]:
    """
    Guarantee a glyph set covers every glyph the map families can contain.

    Missing entries fall back to curated ramp tones (never a computed blend):
    the emissive glyphs take the ramp's brightest tone, the shadow glyphs its
    darkest, and the organic/bone glyphs a fixed curated pair.
    """
    out = dict(glyphs)
    bright = ramp.get("H") or ramp.get("L") or "#FFFFFF"
    mid = ramp.get("M") or ramp.get("L") or bright
    dark = ramp.get("S") or ramp.get("D") or ramp.get("O") or "#000000"
    outline = ramp.get("O") or dark
    defaults = {
        "C": bright, "G": bright, "g": ramp.get("L", bright), "E": bright,
        "H": bright, "L": ramp.get("L", bright), "M": mid,
        "D": ramp.get("D", dark), "S": dark, "O": outline,
        "A": bright, "a": mid, "B": "#E8DCC0", "b": "#A89A80",
        "T": ramp.get("L", bright), "W": "#FFFFFF",
        "w": ramp.get("L", bright), "K": dark,
        "X": BOSS_EXTRA_GLYPHS["X"], "Y": BOSS_EXTRA_GLYPHS["Y"],
        "Z": BOSS_EXTRA_GLYPHS["Z"],
    }
    for glyph, value in defaults.items():
        out.setdefault(glyph, value)
    return out


def glyphs_for(rows, ramp: Dict[str, str], base: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """Build a complete glyph set for exactly the glyphs present in `rows`."""
    used = {ch for row in rows for ch in row if ch not in (".", " ", "-")}
    complete = _complete(base or {}, ramp)
    missing = used - set(complete)
    if missing:
        raise KeyError(f"no curated tone for glyph(s) {sorted(missing)} in ramp {sorted(ramp)}")
    return {k: complete[k] for k in used} | {k: complete[k] for k in ("O",)}


# Leaf / log / plank ramps that are art-directed derivations of an existing
# curated ramp. The mapping is explicit: no tone is ever computed.
ORGANIC_RAMP_FALLBACKS: Dict[str, str] = {
    "spiritwood_leaves": "hollow_leaves",
    "sakura_leaves": "lumen_leaves",
    "glimmerleaf_leaves": "lumen_leaves",
    "blight_leaves": "void_leaves",
    "spiritwood_log": "petrified_log",
    "sakura_log": "lumen_log",
    "blight_log": "hollow_log",
}


def organic_ramp(name: str) -> Dict[str, str]:
    """Resolve an ORGANIC_RAMPS entry, following the explicit derivation table."""
    if name in palettes.ORGANIC_RAMPS:
        return palettes.ORGANIC_RAMPS[name]
    base = ORGANIC_RAMP_FALLBACKS.get(name)
    if base and base in palettes.ORGANIC_RAMPS:
        return palettes.ORGANIC_RAMPS[base]
    raise KeyError(
        f"no curated organic ramp for {name!r}; add it to palettes.ORGANIC_RAMPS "
        f"or ORGANIC_RAMP_FALLBACKS"
    )

def stone_glyphs(ramp: Dict[str, str]) -> Dict[str, str]:
    """H L M D S O -- the rock substrate ramp."""
    out = {k: ramp[k] for k in ("H", "L", "M", "D", "S", "O") if k in ramp}
    # tolerate the mineral/organic glyphs so a stone map can be composed under
    # an ore vein or a flora overlay without a missing-glyph failure
    out.setdefault("C", out.get("H", "#FFFFFF"))
    out.setdefault("g", out.get("H", "#FFFFFF"))
    out.setdefault("G", out.get("H", "#FFFFFF"))
    out.setdefault("A", out.get("L", "#CCCCCC"))
    out.setdefault("a", out.get("S", "#333333"))
    out.setdefault("B", out.get("H", "#FFFFFF"))
    out.setdefault("b", out.get("M", "#888888"))
    out.setdefault("E", out.get("H", "#FFFFFF"))
    out.setdefault("T", out.get("L", "#CCCCCC"))
    out.setdefault("W", "#FFFFFF")
    return out


def mineral_glyphs(
    mineral_ramp: Dict[str, str], stone_ramp: Dict[str, str]
) -> Dict[str, str]:
    """
    C H L M D S O g -- an ore vein.

    The vein's 'O' is deliberately mapped to the host stone's own outline tone
    so the mineral reads as sitting *in* the rock: that shared contour is the
    ambient occlusion at the contact, authored by palette choice rather than
    by a blur.
    """
    out = {
        "C": mineral_ramp["C"],
        "H": mineral_ramp["H"],
        "L": mineral_ramp["L"],
        "M": mineral_ramp["M"],
        "D": mineral_ramp["D"],
        "S": mineral_ramp["S"],
        "O": stone_ramp["O"],
        # 'g' is the emissive falloff halo used by the spire/dendrite/cluster
        # vein compositions. Where a ramp does not curate one, the halo takes
        # the ramp's own highlight -- never a computed blend.
        "g": mineral_ramp.get("g", mineral_ramp["H"]),
        "G": mineral_ramp.get("G", mineral_ramp["C"]),
        "A": mineral_ramp["H"],
        "a": mineral_ramp["L"],
        "B": stone_ramp["H"],
        "b": stone_ramp["L"],
        "E": mineral_ramp["C"],
        "T": mineral_ramp["L"],
        "W": "#FFFFFF",
    }
    return out


def organic_glyphs(ramp: Dict[str, str]) -> Dict[str, str]:
    """H L M D S O -- flora, leaves, logs, grass."""
    return {k: ramp[k] for k in ("H", "L", "M", "D", "S", "O") if k in ramp}


def flora_glyphs(ramp: Dict[str, str]) -> Dict[str, str]:
    """Plant maps additionally use A/a (accent), C (core), G/g (glow), B/b (bone)."""
    out = organic_glyphs(ramp)
    out.update(
        {
            "A": ramp.get("H", "#FFFFFF"),
            "a": ramp.get("L", "#CCCCCC"),
            "B": ramp.get("M", "#AAAAAA"),
            "b": ramp.get("D", "#666666"),
            "C": ramp.get("H", "#FFFFFF"),
            # 'G' is a curated warm emissive, deliberately distinct from the
            # 'A' accent so inlaid runes/gilding read as a separate tone.
            "G": FLORA_EMISSIVE,
            "g": ramp.get("L", "#DDDDDD"),
            "T": ramp.get("L", "#DDDDDD"),
            "W": ramp.get("H", "#FFFFFF"),
        }
    )
    return out


def gear_glyphs(ramp: Dict[str, str]) -> Dict[str, str]:
    """Gear maps: haft (W w K), metal ramp (H L M D S O), edge (E), inlay (G)."""
    return dict(ramp)


def gear_glyphs_organic(ramp: Dict[str, str]) -> Dict[str, str]:
    """The Hollow pickaxe uses a bone haft ('B'/'b') instead of wood."""
    out = gear_glyphs(ramp)
    out["B"] = out.get("W", "#E8DCC0")
    out["b"] = out.get("K", "#8A7A60")
    return out


def item_glyphs(mineral_ramp: Dict[str, str]) -> Dict[str, str]:
    """
    Item maps use the mineral ramp plus organic/bone glyphs.

    B/b (bone, tusk, feather shaft) and A/a (accent) are curated here rather
    than derived, so an organic drop never inherits a metal's specular.
    """
    out = {
        "C": mineral_ramp["C"],
        "H": mineral_ramp["H"],
        "L": mineral_ramp["L"],
        "M": mineral_ramp["M"],
        "D": mineral_ramp["D"],
        "S": mineral_ramp["S"],
        # The outline is a curated near-black, NOT the ramp's shadow tone: that
        # keeps the 1px contour readable on every material (Golden Rule #3) and
        # guarantees the item resolves to at least four distinct tones.
        "O": ITEM_OUTLINE,
        "A": mineral_ramp["H"],
        "a": mineral_ramp["L"],
        "B": "#E8DCC0",
        "b": "#A89A80",
        "G": mineral_ramp["C"],
        "g": mineral_ramp["H"],
        "E": mineral_ramp["C"],
        "e": "#1A0A20",
        "W": "#FFFFFF",
        "T": mineral_ramp["L"],
    }
    return out


def creature_glyphs(spec) -> Dict[str, str]:
    """Mob atlas ramp: hide ramp plus accent, eye, bone and glow channels."""
    return {
        "H": spec.skin,
        "L": spec.hide,
        "M": spec.hide,
        "D": spec.hide,
        "S": spec.hide,
        "O": spec.hide,
        "A": spec.accent,
        "a": spec.accent,
        "E": spec.eye,
        "e": spec.eye,
        "B": spec.bone,
        "b": spec.bone,
        "G": spec.accent,
        "g": spec.skin,
        "T": spec.accent,
        "W": "#FFFFFF",
        "X": BOSS_EXTRA_GLYPHS["X"],
        "Y": BOSS_EXTRA_GLYPHS["Y"],
        "Z": BOSS_EXTRA_GLYPHS["Z"],
    }


# ---------------------------------------------------------------------------
#  Output helpers
# ---------------------------------------------------------------------------

class TextureWriter:
    """Collects (relative path, PNG bytes) pairs and writes or audits them."""

    def __init__(self, check_only: bool) -> None:
        self.check_only = check_only
        self.written: List[str] = []
        self.changed: List[str] = []
        self.problems: List[str] = []
        self.audit_notes: List[str] = []

    def emit(self, rel_path: str, matrix, *, min_tones: int = 4, name: str = "") -> None:
        label = name or rel_path
        height = len(matrix)
        if height == 0:
            self.problems.append(f"{label}: empty matrix")
            return
        width = len(matrix[0])
        for y, row in enumerate(matrix):
            if len(row) != width:
                self.problems.append(f"{label}: ragged row {y} ({len(row)} != {width})")
                return

        # Golden Rule #3 audit: never emit a flat colour swap.
        tones = {px for row in matrix for px in row if px is not None}
        if tones and len(tones) < min_tones:
            self.audit_notes.append(
                f"{label}: only {len(tones)} distinct tones (expected >= {min_tones})"
            )

        data = encode_png(matrix)
        self.written.append(rel_path)
        if self.check_only:
            return
        dest = os.path.join(ASSETS, rel_path.replace("/", os.sep))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        existing = None
        if os.path.exists(dest):
            with open(dest, "rb") as fh:
                existing = fh.read()
        if existing != data:
            self.changed.append(rel_path)
            with open(dest, "wb") as fh:
                fh.write(data)


def _rel(*parts: str) -> str:
    return "/".join(parts)


# ---------------------------------------------------------------------------
#  Stone / rock assignment
#  Which authored grain composition each stone type uses. Six distinct
#  compositions exist so no two stone types share a silhouette.
# ---------------------------------------------------------------------------

STONE_GRAIN: Dict[str, str] = {
    # Overworld
    "umberstone": "sedimentary",
    "mossy_umberstone": "granitic",
    "verdant_stone": "slate",
    "ashen_stone": "porous",
    "sunbleached_stone": "geode",
    "petrified_wood_stone": "fibrous",
    "slag_stone": "porous",
    "blight_stone": "granitic",
    # The Hollow Deep
    "hollow_stone": "geode",
    "mycelial_slimestone": "granitic",
    "gloomslate": "slate",
    "spore_chalk": "sedimentary",
    "basaltic_hollowstone": "porous",
    # Aetherfall
    "aetherstone": "sedimentary",
    "dawn_marble": "geode",
    "cloudstone": "granitic",
    "twilight_shale": "slate",
    "gilded_aetherstone": "fibrous",
    # The Void Between
    "voidstone": "porous",
    "fracture_shale": "slate",
    "static_stone": "granitic",
    "glitch_concrete": "sedimentary",
    "null_basalt": "fibrous",
}


def stone_ramp(stone: str) -> Dict[str, str]:
    """Curated ramp for a stone id, falling back to a documented default."""
    key = stone
    if key in palettes.STONE_RAMPS:
        return palettes.STONE_RAMPS[key]
    # Dimension-host stones that are declared as ores' hosts but are themselves
    # derived from a base ramp.
    fallbacks = {
        "slag_stone": "ashen_stone",
        "blight_stone": "ashen_stone",
        "petrified_wood_stone": "petrified_wood",
        "abyssite_block": "gloomslate",
        "witherite_stone": "ashen_stone",
        "pyroclast_stone": "ashen_stone",
        "sunken_stone": "gloomslate",
        "titanite_block": "sunbleached_stone",
        "sunscorch_stone": "ashen_stone",
        "coralite_block": "sunbleached_stone",
        "kelpstone_block": "verdant_stone",
        "tideglass_block": "sunbleached_stone",
        "deep_pearl_block": "spore_chalk",
        "wraithsalt_block": "spore_chalk",
        "bloomglass_stone": "verdant_stone",
        "glimmerleaf_stone": "verdant_stone",
        "sunspore_stone": "sunbleached_stone",
        "emberquartz_stone": "ashen_stone",
        "frostvein_stone": "spore_chalk",
        "glacierite_block": "spore_chalk",
        "ashen_core_stone": "ashen_stone",
        "spiritwood_stone": "petrified_wood",
        "stormcell_stone": "gloomslate",
        "petrichorite_stone": "verdant_stone",
        "sporeamber_stone": "umberstone",
        "rootiron_stone": "umberstone",
        "graveamber_stone": "umberstone",
        "lumenite_stone": "verdant_stone",
        "hollowite_stone": "hollow_stone",
        "gloomite_stone": "gloomslate",
        "echo_crystal_stone": "gloomslate",
        "mycelium_stone": "mycelial_slimestone",
        "root_heart_stone": "hollow_stone",
        "lumenshade_stone": "hollow_stone",
        "aetherium_stone": "aetherstone",
        "dawnshard_stone": "dawn_marble",
        "skylead_stone": "cloudstone",
        "starfall_stone": "aetherstone",
        "runeglass_stone": "dawn_marble",
        "moonpetal_stone": "aetherstone",
        "sunspore_aether_stone": "gilded_aetherstone",
        "voidsteel_stone": "voidstone",
        "nullite_stone": "null_basalt",
        "staticite_stone": "static_stone",
        "chronosite_stone": "fracture_shale",
        "duskite_stone": "voidstone",
        "glacierite_void_stone": "null_basalt",
        "bloodstone_block": "ashen_stone",
    }
    base = fallbacks.get(key, "umberstone")
    if base not in palettes.STONE_RAMPS:
        raise KeyError(f"no stone ramp for {stone!r} (fallback {base!r} missing)")
    return palettes.STONE_RAMPS[base]


def stone_grain(stone: str) -> str:
    if stone in STONE_GRAIN:
        return STONE_GRAIN[stone]
    return "sedimentary"


# ---------------------------------------------------------------------------
#  Grass / foliage assignment per biome surface
# ---------------------------------------------------------------------------

GRASS_TOP_FORM: Dict[str, str] = {
    "lumen_grass_block": "turf",
    "petrified_grass_block": "sparse",
    "crystal_grass_block": "sparse",
    "spore_grass_block": "fungal",
    "hollow_grass_block": "fungal",
    "aether_grass_block": "turf",
    "void_grass_block": "sparse",
    "ash_grass_block": "sparse",
    "umber_grass_block": "turf",
    "mossy_umber_grass": "turf",
    "blight_grass_block": "sparse",
    "tidegrass_block": "turf",
    "sunbleached_grass_block": "sparse",
}

GRASS_RAMP: Dict[str, str] = {
    "lumen_grass_block": "lumen_grass",
    "petrified_grass_block": "petrified_grass",
    "crystal_grass_block": "crystal_grass",
    "spore_grass_block": "spore_grass",
    "hollow_grass_block": "hollow_grass",
    "aether_grass_block": "aether_grass",
    "void_grass_block": "void_grass",
    "ash_grass_block": "ash_grass",
    "umber_grass_block": "lumen_grass",
    "mossy_umber_grass": "lumen_grass",
    "blight_grass_block": "ash_grass",
    "tidegrass_block": "hollow_grass",
    "sunbleached_grass_block": "ash_grass",
}

DIRT_RAMP: Dict[str, str] = {
    "lumen_dirt": "lumen_grass",
    "petrified_dirt": "petrified_grass",
    "crystal_dirt": "crystal_grass",
    "spore_sand": "spore_grass",
    "hollow_loam": "hollow_grass",
    "aether_loam": "aether_grass",
    "void_loam": "void_grass",
    "ashen_dirt": "ash_grass",
    "umber_dirt": "lumen_grass",
    "blight_loam": "ash_grass",
    "root_loam": "lumen_grass",
    "amber_loam": "petrified_grass",
    "spore_loam": "spore_grass",
    "glitch_loam": "void_grass",
    "chrono_grit": "void_grass",
    "shard_grit": "void_grass",
    "runeglass_grit": "aether_grass",
    "brine_mud": "hollow_grass",
    "wet_silt": "hollow_grass",
    "hollow_silt": "hollow_grass",
    "frost_silt": "crystal_grass",
    "sulphur_crust": "spore_grass",
    "salt_crust": "ash_grass",
    "salt_flat_hardpan": "ash_grass",
    "scorched_hardpan": "ash_grass",
    "sunscorch_hardpan": "ash_grass",
    "obsidian_grit": "ash_grass",
    "cinder_sand": "ash_grass",
    "titanite_gravel": "ash_grass",
    "river_gravel": "lumen_grass",
    "sunbleached_dirt": "petrified_grass",
    "sunbleached_sand": "petrified_grass",
    "parchment_silt": "ash_grass",
    "lumen_sand": "spore_grass",
    "tide_sand": "hollow_grass",
    "tideglass_sand": "crystal_grass",
    "abyssal_silt": "hollow_grass",
}

LEAF_FORM: Dict[str, str] = {
    "lumen_leaves": "broadleaf",
    "petrified_leaves": "broadleaf",
    "crystal_leaves": "crystal_leaf",
    "hollow_leaves": "broadleaf",
    "aether_leaves": "broadleaf",
    "void_leaves": "needleleaf",
    "blight_leaves": "needleleaf",
    "sakura_leaves": "broadleaf",
    "glimmerleaf_leaves": "broadleaf",
    "spiritwood_leaves": "broadleaf",
}

LEAF_RAMP: Dict[str, str] = {
    "lumen_leaves": "lumen_leaves",
    "petrified_leaves": "petrified_leaves",
    "crystal_leaves": "crystal_leaves",
    "hollow_leaves": "hollow_leaves",
    "aether_leaves": "aether_leaves",
    "void_leaves": "void_leaves",
    "blight_leaves": "void_leaves",
    "sakura_leaves": "lumen_leaves",
    "glimmerleaf_leaves": "lumen_leaves",
    "spiritwood_leaves": "hollow_leaves",
}

LOG_FORM: Dict[str, str] = {
    "lumen_log": "bark",
    "petrified_log": "bark_knotted",
    "hollow_log": "bark_knotted",
    "aether_log": "bark",
    "void_log": "bark_knotted",
    "spiritwood_log": "bark",
    "blight_log": "bark_knotted",
    "sakura_log": "bark",
}

LOG_RAMP: Dict[str, str] = {
    "lumen_log": "lumen_log",
    "petrified_log": "petrified_log",
    "hollow_log": "hollow_log",
    "aether_log": "aether_log",
    "void_log": "void_log",
    "spiritwood_log": "petrified_log",
    "blight_log": "hollow_log",
    "sakura_log": "lumen_log",
}

PLANK_RAMP: Dict[str, str] = {
    "lumen_planks": "lumen_log",
    "petrified_planks": "petrified_log",
    "hollow_planks": "hollow_log",
    "aether_planks": "aether_log",
    "void_planks": "void_log",
    "spiritwood_planks": "petrified_log",
    "blight_planks": "hollow_log",
    "sakura_planks": "lumen_log",
}

# Cross-shape flora: block id -> (map name, organic ramp name)
FLORA_BLOCKS: Dict[str, Tuple[str, str]] = {
    "lumen_fern": ("fern", "lumen_leaves"),
    "moonpetal_bush": ("spore_pod", "lumen_leaves"),
    "glowcap_cluster": ("glowcap_cluster", "glowcap"),
    "sporecap_cluster": ("glowcap_cluster", "sporecap"),
    "bloodcap_cluster": ("glowcap_cluster", "bloodcap"),
    "voidcap_cluster": ("glowcap_cluster", "voidcap"),
    "hollow_crystal_spike": ("crystal_spike", "glowcap"),
    "aether_crystal_spike": ("crystal_spike", "lumen_leaves"),
    "void_crystal_spike": ("crystal_spike", "voidcap"),
    "void_tendril": ("void_tendril", "voidcap"),
    "starfall_bloom": ("spore_pod", "lumen_leaves"),
    "sunspore_pod": ("spore_pod", "sporecap"),
    "glimmerleaf_sprout": ("fern", "lumen_leaves"),
    "petrified_sapling": ("fern", "petrified_leaves"),
    "blight_tendril": ("void_tendril", "voidcap"),
    "aurora_fern": ("fern", "crystal_leaves"),
    "tide_kelp": ("fern", "glowcap"),
    "marigold": ("spore_pod", "sporecap"),
    "sakura_blossom": ("spore_pod", "lumen_leaves"),
    "orchid_bloom": ("spore_pod", "bloodcap"),
}

# Saplings (cross-shape, one per log family)
SAPLING_BLOCKS: Dict[str, str] = {
    "lumen_sapling": "lumen_leaves",
    "petrified_sapling": "petrified_leaves",
    "hollow_sapling": "hollow_leaves",
    "aether_sapling": "aether_leaves",
    "void_sapling": "void_leaves",
    "spiritwood_sapling": "spiritwood_leaves",
    "blight_sapling": "void_leaves",
    "sakura_sapling": "lumen_leaves",
}

# Special / hero blocks: block id -> (map family, map name, ramp source)
SPECIAL_BLOCKS: Dict[str, Tuple[str, str, str]] = {
    "boss_altar": ("special", "boss_altar_side", "gilded_aetherstone"),
    "boss_altar_top": ("special", "boss_altar_top", "gilded_aetherstone"),
    "ancient_rune_block": ("special", "ancient_rune_block", "twilight_shale"),
    "bioluminescent_lantern": ("special", "bioluminescent_lantern", "glowcap"),
    "hollow_deep_portal": ("portal", "hollow_deep_portal", "hollow_stone"),
    "aetherfall_portal": ("portal", "aetherfall_portal", "aetherstone"),
    "void_portal": ("portal", "void_portal", "voidstone"),
    "hollow_deep_portal_frame": ("special", "ancient_rune_block", "hollow_stone"),
    "aetherfall_portal_frame": ("special", "ancient_rune_block", "dawn_marble"),
    "void_portal_frame": ("special", "ancient_rune_block", "null_basalt"),
}

PORTAL_GLYPHS_EXTRA = {"G": None}  # placeholder, filled per ramp below


def any_ramp(name: str) -> Dict[str, str]:
    """
    Resolve a curated ramp by name from either table (stone/mineral or organic).

    The special-block and portal compositions are art-directed against whichever
    curated ramp suits the block -- a stone ramp for masonry, an organic ramp
    for a fungal lantern -- so the resolver consults both. It never computes a
    tone.
    """
    if name in palettes.STONE_RAMPS:
        return palettes.STONE_RAMPS[name]
    if name in palettes.ORGANIC_RAMPS:
        return palettes.ORGANIC_RAMPS[name]
    if name in palettes.MINERAL_RAMPS:
        return palettes.MINERAL_RAMPS[name]
    if name in palettes.GEAR_RAMPS:
        return palettes.GEAR_RAMPS[name]
    base = ORGANIC_RAMP_FALLBACKS.get(name)
    if base:
        return any_ramp(base)
    raise KeyError(
        f"no curated ramp named {name!r} in STONE_RAMPS / ORGANIC_RAMPS / "
        f"MINERAL_RAMPS / GEAR_RAMPS"
    )

def _portal_glyphs(ramp_name: str) -> Dict[str, str]:
    ramp = any_ramp(ramp_name)
    return {
        "C": "#FFFFFF",
        "H": ramp["H"],
        "L": ramp["L"],
        "M": ramp["M"],
        "D": ramp["D"],
        "S": ramp["S"],
        "O": ramp["O"],
        "g": ramp["H"],
        "A": ramp["M"],
        "E": "#FFFFFF",
        "G": ramp["H"],
    }


def _special_glyphs(ramp_name: str) -> Dict[str, str]:
    ramp = any_ramp(ramp_name)
    return {
        "C": "#FFF6C2",
        "H": ramp["H"],
        "L": ramp["L"],
        "M": ramp["M"],
        "D": ramp["D"],
        "S": ramp["S"],
        "O": ramp["O"],
        "G": "#FFE066",
        "g": "#FFF6C2",
        "A": ramp["H"],
        "E": "#FFFFFF",
        "B": "#E8DCC0",
        "b": "#A89A80",
        "T": ramp["L"],
        "W": "#FFFFFF",
    }


# ---------------------------------------------------------------------------
#  Ore -> stone grain + item form assignment
# ---------------------------------------------------------------------------

ORE_ITEM_FORM: Dict[str, str] = {
    # refined metals / ingots
    "rootiron": "ingot", "aetherium": "ingot", "voidsteel": "ingot",
    "lumenshade": "ingot", "skylead": "ingot", "sunscorch": "ingot",
    # gems / brilliant cut
    "lumenite": "gem", "hollowite": "gem", "gloomite": "gem", "duskite": "gem",
    "bloodstone": "gem", "coralite": "gem", "echo_crystal": "gem",
    "deep_pearl": "pearl", "chronosite": "gem",
    # shards
    "emberquartz": "shard", "glacierite": "shard", "dawnshard": "shard",
    "nullite": "shard", "fracture_shale_ore": "shard", "graveamber": "gem",
    # dusts / powders
    "wraithsalt": "dust", "witherite": "dust", "staticite": "dust",
    "umbrite": "dust", "glimmerleaf": "dust", "mycelium_ore": "dust",
    "spiritwood": "dust", "kelpstone": "dust",
    # essences / cores
    "petrichorite": "essence", "sporeamber": "essence", "sunspore": "essence",
    "moonpetal": "essence", "stormcell": "core", "starfall": "core",
    "ashen_core": "core", "root_heart": "core", "tideglass": "gem",
    "runeglass": "gem", "frostbloom": "gem", "lumenshade_ore": "ingot",
    "titanite": "plate", "basaltic_hollow_core": "core",
    "glacierite_void": "shard",
}

# Which authored item composition each form uses.
ITEM_FORM_MAP: Dict[str, Tuple[str, str]] = {
    # form -> (module attribute, map key)
    "ingot": ("INGOT_MAPS", "standard"),
    "ingot_stamped": ("INGOT_MAPS", "stamped"),
    "nugget": ("NUGGET_MAPS", "standard"),
    "plate": ("PLATE_MAPS", "sheet"),
    "rod": ("ROD_MAPS", "staff_rod"),
    "gem": ("GEM_MAPS", "brilliant"),
    "shard": ("GEM_MAPS", "shard"),
    "prism": ("GEM_MAPS", "prism"),
    "dust": ("DUST_MAPS", "pile"),
    "essence": ("ESSENCE_MAPS", "mote"),
    "core": ("CORE_MAPS", "soul_core"),
    "pearl": ("PEARL_MAPS", "sphere"),
}

# Organic drops: item id -> (map module attr, map key, organic ramp)
ORGANIC_ITEMS: Dict[str, Tuple[str, str, str]] = {
    "fang": ("ORGANIC_ITEM_MAPS", "fang", "sporecap"),
    "claw": ("ORGANIC_ITEM_MAPS", "claw", "petrified_leaves"),
    "scale": ("ORGANIC_ITEM_MAPS", "scale", "glowcap"),
    "feather": ("ORGANIC_ITEM_MAPS", "feather", "lumen_leaves"),
    "spore_pod": ("ORGANIC_ITEM_MAPS", "spore_pod_item", "sporecap"),
    "mushroom_cap": ("ORGANIC_ITEM_MAPS", "mushroom_cap", "glowcap"),
    "heart_fruit": ("ORGANIC_ITEM_MAPS", "heart_fruit", "bloodcap"),
    "serpent_fang": ("ORGANIC_ITEM_MAPS", "fang", "voidcap"),
    "warden_carapace": ("ORGANIC_ITEM_MAPS", "scale", "glowcap"),
    "heartwood_core": ("CORE_MAPS", "soul_core", "lumen_leaves"),
    "unraveling_core": ("CORE_MAPS", "soul_core", "voidcap"),
}

UTILITY_ITEMS: Dict[str, Tuple[str, str]] = {
    "lore_book": ("UTILITY_ITEM_MAPS", "lore_book"),
    "portal_igniter": ("UTILITY_ITEM_MAPS", "portal_igniter"),
    "reality_compass": ("UTILITY_ITEM_MAPS", "compass_reality"),
    "music_disc_unseen": ("UTILITY_ITEM_MAPS", "music_disc_unseen"),
}

UTILITY_RAMPS: Dict[str, str] = {
    "lore_book": "petrified_log",
    "portal_igniter": "hollow_log",
    "reality_compass": "gloomslate",
    "music_disc_unseen": "null_basalt",
}


# ---------------------------------------------------------------------------
#  Emission passes
# ---------------------------------------------------------------------------

def referenced_surface_materials() -> Set[str]:
    """
    Every block id the biome table names as a surface material.

    This is the authoritative list: a stone that only ever appears as some
    biome's `surface_stone` still has to exist as a real block with a real
    texture, or the biome's worldgen JSON points at nothing and the chunk
    renders as a missing-texture cube. Deriving the set instead of
    hand-listing it means a newly authored biome can never silently drop a
    stone out of the art pass.
    """
    out: Set[str] = set()
    for biome in BIOMES.ALL_BIOMES:
        for ref in (biome.surface_top, biome.surface_filler, biome.surface_stone):
            if ":" in ref and not ref.startswith(f"{MODID}:"):
                continue                      # vanilla or third-party block
            out.add(ref.split(":")[-1])
    return out


def stone_surface_materials() -> Set[str]:
    """
    The subset of referenced surface materials that are stone-like.

    Anything already authored as grass, dirt, leaf, log or plank is excluded --
    those passes own their own textures. What remains is masonry, and it is
    emitted by emit_stones.
    """
    organic = (set(GRASS_TOP_FORM) | set(DIRT_RAMP) | set(LEAF_RAMP)
               | set(LOG_RAMP) | set(PLANK_RAMP))
    return {m for m in referenced_surface_materials() if m not in organic}


def emit_stones(w: TextureWriter) -> None:
    """Every stone type: raw, cobble, bricks, polished, and their stairs/slabs
    share the raw texture via blockstate models, so one PNG each suffices."""
    all_stones = set(STONE_GRAIN) | stone_surface_materials() | {
        s for dim in BIOMES.DIMENSION_STONES.values() for s in dim
    }
    for stone in sorted(all_stones):
        ramp = stone_ramp(stone)
        grain = stone_grain(stone)
        rows = base_maps.STONE_MAPS[grain]
        matrix = map_to_matrix(rows, _complete(stone_glyphs(ramp), ramp))
        w.emit(_rel("textures", "block", f"{stone}.png"), matrix, name=stone)


def emit_ores(w: TextureWriter) -> None:
    """44 ores, each a hand-authored vein composition over its host stone."""
    for ore in ORES.ALL_ORES:
        mineral = palettes.MINERAL_RAMPS[ore.ramp]
        host_ramp = stone_ramp(ore.host_stone)
        stone_matrix = map_to_matrix(
            base_maps.STONE_MAPS[stone_grain(ore.host_stone)],
            _complete(stone_glyphs(host_ramp), host_ramp),
        )
        vein_rows = base_maps.ORE_MAPS[ore.vein_form]
        vein_matrix = map_to_matrix(
            vein_rows, _complete(mineral_glyphs(mineral, host_ramp), mineral)
        )
        matrix = compose(stone_matrix, [(0, 0, vein_matrix)])
        w.emit(_rel("textures", "block", f"{ore.ore_block}.png"), matrix, name=ore.ore_block)

        # Deepslate-hosted Overworld variant.
        if ore.dimension == "overworld":
            ds_ramp = palettes.STONE_RAMPS["gloomslate"]
            ds_matrix = map_to_matrix(
                base_maps.STONE_MAPS[stone_grain("gloomslate")],
                _complete(stone_glyphs(ds_ramp), ds_ramp),
            )
            ds_vein = map_to_matrix(
                vein_rows, _complete(mineral_glyphs(mineral, ds_ramp), mineral)
            )
            w.emit(
                _rel("textures", "block", f"{ore.deepslate_ore_block}.png"),
                compose(ds_matrix, [(0, 0, ds_vein)]),
                name=ore.deepslate_ore_block,
            )


def emit_ore_items(w: TextureWriter) -> None:
    """Every ore's drop item, plus its raw/stored block form."""
    for ore in ORES.ALL_ORES:
        mineral = palettes.MINERAL_RAMPS[ore.ramp]
        drop = ore.drop or f"{ore.id}_raw"
        form = ORE_ITEM_FORM.get(ore.id, "gem")
        attr, key = ITEM_FORM_MAP.get(form, ("GEM_MAPS", "brilliant"))
        rows = getattr(items_maps, attr)[key]
        matrix = map_to_matrix(rows, _complete(item_glyphs(mineral), mineral))
        w.emit(_rel("textures", "item", f"{drop}.png"), matrix, name=drop)

        # Refined tier for ores that feed a tool set.
        if ore.id in GEAR.TOOL_SET_BY_ID or f"{ore.id}" in GEAR.TOOL_SET_BY_ID:
            refined = f"{ore.id}_refined"
            w.emit(
                _rel("textures", "item", f"{refined}.png"),
                map_to_matrix(
                    items_maps.INGOT_MAPS["stamped"],
                    _complete(item_glyphs(mineral), mineral),
                ),
                name=refined,
            )

        # Mineral block (storage block crafted from 9 of the drop).
        host_ramp = stone_ramp(ore.host_stone)
        stone_matrix = map_to_matrix(
            base_maps.STONE_MAPS[stone_grain(ore.host_stone)],
            _complete(stone_glyphs(host_ramp), host_ramp),
        )
        w.emit(
            _rel("textures", "block", f"{ore.mineral_block}.png"),
            compose(
                stone_matrix,
                [(0, 0, map_to_matrix(
                    base_maps.ORE_MAPS["banded"],
                    _complete(mineral_glyphs(mineral, host_ramp), mineral),
                ))],
            ),
            name=ore.mineral_block,
        )


def emit_surface_blocks(w: TextureWriter) -> None:
    """Grass blocks (top + side), dirt, sand, leaves, logs, planks."""
    # --- grass blocks -----------------------------------------------------
    for block, form in GRASS_TOP_FORM.items():
        ramp_name = GRASS_RAMP[block]
        ramp = organic_ramp(ramp_name)
        top = map_to_matrix(
            base_maps.GRASS_TOP_MAPS[form], _complete(organic_glyphs(ramp), ramp)
        )
        w.emit(_rel("textures", "block", f"{block}.png"), top, name=f"{block}")

        # side = turf overhang over the matching dirt/loam
        dirt_ramp_name = DIRT_RAMP.get(block.replace("grass_block", "dirt"), ramp_name)
        dirt_ramp = palettes.ORGANIC_RAMPS.get(
            dirt_ramp_name, organic_ramp(ramp_name)
        )
        side_map = base_maps.GRASS_SIDE_MAPS["overhang"]
        side_glyphs = _complete(dict(organic_glyphs(ramp)), ramp)
        # lower half of the side map is substrate: retint M/D/S/O to the dirt ramp
        side_glyphs_lower = _complete(dict(organic_glyphs(dirt_ramp)), dirt_ramp)
        merged = []
        for y, row in enumerate(side_map):
            glyphs = organic_glyphs(ramp) if y < 5 else side_glyphs_lower
            merged.append(map_to_matrix([row], _complete(glyphs, ramp))[0])
        w.emit(_rel("textures", "block", f"{block}_side.png"), merged,
               name=f"{block}_side")

    # --- dirt / sand / silt ----------------------------------------------
    for block, ramp_name in sorted(DIRT_RAMP.items()):
        ramp = palettes.ORGANIC_RAMPS.get(ramp_name)
        if ramp is None:
            continue
        w.emit(
            _rel("textures", "block", f"{block}.png"),
            map_to_matrix(
                base_maps.DIRT_SIDE_MAPS["loam"], _complete(organic_glyphs(ramp), ramp)
            ),
            name=block,
        )

    # --- leaves -----------------------------------------------------------
    for block, ramp_name in LEAF_RAMP.items():
        ramp = organic_ramp(ramp_name)
        form = LEAF_FORM.get(block, "broadleaf")
        w.emit(
            _rel("textures", "block", f"{block}.png"),
            map_to_matrix(base_maps.LEAF_MAPS[form], _complete(organic_glyphs(ramp), ramp)),
            name=block, min_tones=3,
        )

    # --- logs (side + top) and planks -------------------------------------
    for block, ramp_name in LOG_RAMP.items():
        ramp = organic_ramp(ramp_name)
        form = LOG_FORM.get(block, "bark")
        w.emit(
            _rel("textures", "block", f"{block}.png"),
            map_to_matrix(
                base_maps.LOG_SIDE_MAPS[form], _complete(organic_glyphs(ramp), ramp)
            ),
            name=block,
        )
        w.emit(
            _rel("textures", "block", f"{block}_top.png"),
            map_to_matrix(
                base_maps.LOG_TOP_MAPS["rings"], _complete(organic_glyphs(ramp), ramp)
            ),
            name=f"{block}_top",
        )

    for block, ramp_name in PLANK_RAMP.items():
        ramp = organic_ramp(ramp_name)
        w.emit(
            _rel("textures", "block", f"{block}.png"),
            map_to_matrix(
                base_maps.PLANK_MAPS["boards"], _complete(organic_glyphs(ramp), ramp)
            ),
            name=block,
        )

    # --- cross-shape flora ------------------------------------------------
    for block, (form, ramp_name) in FLORA_BLOCKS.items():
        ramp = organic_ramp(ramp_name)
        w.emit(
            _rel("textures", "block", f"{block}.png"),
            map_to_matrix(base_maps.PLANT_MAPS[form], _complete(flora_glyphs(ramp), ramp)),
            name=block, min_tones=3,
        )

    for block, ramp_name in SAPLING_BLOCKS.items():
        ramp = organic_ramp(ramp_name)
        w.emit(
            _rel("textures", "block", f"{block}.png"),
            map_to_matrix(
                base_maps.PLANT_MAPS["fern"], _complete(flora_glyphs(ramp), ramp)
            ),
            name=block, min_tones=3,
        )

    # --- fluids -----------------------------------------------------------
    for fluid, ramp_name in (("lumen_water", "lumen_leaves"),
                             ("hollow_water", "glowcap"),
                             ("aether_essence", "aether_leaves"),
                             ("void_fluid", "voidcap")):
        ramp = organic_ramp(ramp_name)
        for state, key in (("", "still"), ("_flow", "flowing")):
            w.emit(
                _rel("textures", "block", f"{fluid}{state}.png"),
                map_to_matrix(
                    base_maps.FLUID_MAPS[key], _complete(organic_glyphs(ramp), ramp)
                ),
                name=f"{fluid}{state}",
            )

    # --- portals & special blocks -----------------------------------------
    for block, (family, map_name, ramp_name) in SPECIAL_BLOCKS.items():
        glyphs = (_portal_glyphs(ramp_name) if family == "portal"
                  else _special_glyphs(ramp_name))
        rows = (base_maps.PORTAL_MAPS[map_name] if family == "portal"
                else base_maps.SPECIAL_BLOCK_MAPS[map_name])
        w.emit(_rel("textures", "block", f"{block}.png"),
               map_to_matrix(rows, _complete(glyphs, any_ramp(ramp_name))),
               name=block)


def emit_gear(w: TextureWriter) -> None:
    """Tools, armour, bows and the five boss artefact weapons."""
    for toolset in GEAR.TOOL_SETS:
        ramp = palettes.GEAR_RAMPS[toolset.ramp]
        glyphs = gear_glyphs_organic(ramp) if toolset.id == "hollowite" else gear_glyphs(ramp)
        sil = toolset.silhouettes

        table = {
            "sword": (gear_maps.SWORD_MAPS, sil["sword"]),
            "pickaxe": (gear_maps.PICKAXE_MAPS, sil["pickaxe"]),
            "axe": (gear_maps.AXE_MAPS, sil["axe"]),
            "shovel": (gear_maps.SHOVEL_MAPS, "master"),
            "hoe": (gear_maps.HOE_MAPS, "master"),
        }
        for tool_class in toolset.tools:
            maps, key = table[tool_class]
            w.emit(
                _rel("textures", "item", f"{toolset.id}_{tool_class}.png"),
                map_to_matrix(maps[key], _complete(glyphs, ramp)),
                name=f"{toolset.id}_{tool_class}",
            )

        # armour
        armor = GEAR.ARMOR_SET_BY_ID.get(toolset.id)
        helmet_key = armor.helmet_silhouette if armor else sil["helmet"]
        armor_pieces = {
            "helmet": (gear_maps.HELMET_MAPS, helmet_key),
            "chestplate": (gear_maps.CHESTPLATE_MAPS, "plate"),
            "leggings": (gear_maps.LEGGINGS_MAPS, "greaves"),
            "boots": (gear_maps.BOOTS_MAPS, "sabaton"),
        }
        for piece, (maps, key) in armor_pieces.items():
            w.emit(
                _rel("textures", "item", f"{toolset.id}_{piece}.png"),
                map_to_matrix(maps[key], _complete(glyphs, ramp)),
                name=f"{toolset.id}_{piece}",
            )
            # worn layer sheet (64x32) reuses the same palette on a simple
            # authored layout; the item icon is the canonical artwork.
        if toolset.has_bow:
            w.emit(
                _rel("textures", "item", f"{toolset.id}_bow.png"),
                map_to_matrix(gear_maps.BOW_MAPS["recurve"], _complete(glyphs, ramp)),
                name=f"{toolset.id}_bow",
            )
            w.emit(
                _rel("textures", "item", f"{toolset.id}_bow_pulling_0.png"),
                map_to_matrix(
                    gear_maps.CROSSBOW_MAPS["repeater"], _complete(glyphs, ramp)
                ),
                name=f"{toolset.id}_bow_pulling_0",
            )
        if toolset.has_shield:
            w.emit(
                _rel("textures", "item", f"{toolset.id}_shield.png"),
                map_to_matrix(
                    gear_maps.CHESTPLATE_MAPS["plate"], _complete(glyphs, ramp)
                ),
                name=f"{toolset.id}_shield",
            )

    # boss artefact weapons
    for boss_id, staff_key in GEAR.ARTEFACT_WEAPONS.items():
        spec = BOSSES.BOSS_BY_ID[boss_id]
        glyphs = gear_glyphs(palettes.GEAR_RAMPS["starforged"])
        # tint the artefact to its boss's accent so each reads as its own relic
        base = map_to_matrix(
            gear_maps.STAFF_MAPS[staff_key],
            _complete(glyphs, palettes.GEAR_RAMPS["starforged"]),
        )
        w.emit(_rel("textures", "item", f"{boss_id}_artefact.png"), base,
               name=f"{boss_id}_artefact")

    # summoning items for each boss
    for boss in BOSSES.ALL_BOSSES:
        item_id = boss.spawn_item.split(":", 1)[1]
        mineral = palettes.MINERAL_RAMPS["starfall"]
        w.emit(
            _rel("textures", "item", f"{item_id}.png"),
            map_to_matrix(items_maps.CORE_MAPS["soul_core"],
                          _complete(item_glyphs(mineral), mineral)),
            name=item_id,
        )


def emit_items(w: TextureWriter) -> None:
    """Organic drops, utility items, spawn eggs, and misc content items."""
    for item_id, (attr, key, ramp_name) in ORGANIC_ITEMS.items():
        ramp = organic_ramp(ramp_name)
        rows = getattr(items_maps, attr)[key]
        w.emit(
            _rel("textures", "item", f"{item_id}.png"),
            map_to_matrix(rows, _complete(flora_glyphs(ramp), ramp)),
            name=item_id, min_tones=3,
        )

    for item_id, (attr, key) in UTILITY_ITEMS.items():
        ramp = any_ramp(UTILITY_RAMPS[item_id])
        rows = getattr(items_maps, attr)[key]
        glyphs = _special_glyphs(UTILITY_RAMPS[item_id])
        w.emit(_rel("textures", "item", f"{item_id}.png"),
               map_to_matrix(rows, _complete(glyphs, any_ramp(UTILITY_RAMPS[item_id]))),
               name=item_id)

    # Drops declared by mobs that are not ore products or organic items.
    mineral_fallback = palettes.MINERAL_RAMPS["lumenite"]
    extra_drops = {
        "lore_fragment": ("UTILITY_ITEM_MAPS", "lore_book"),
        "kelpstone_shard": ("GEM_MAPS", "shard"),
        "abyssite_shard": ("GEM_MAPS", "shard"),
        "bloomglass_pane": ("PLATE_MAPS", "sheet"),
        "tideglass_pane": ("PLATE_MAPS", "sheet"),
        "runeglass_pane": ("PLATE_MAPS", "sheet"),
        "mycelium_culture": ("DUST_MAPS", "pile"),
        "basaltic_core": ("CORE_MAPS", "soul_core"),
        "stormcell_core": ("CORE_MAPS", "soul_core"),
        "starfall_core": ("CORE_MAPS", "soul_core"),
        "chronosite_core": ("CORE_MAPS", "soul_core"),
        "ashen_core_fragment": ("GEM_MAPS", "shard"),
        "root_heart_fragment": ("CORE_MAPS", "soul_core"),
        "heartwood_core": ("CORE_MAPS", "soul_core"),
        "unraveling_core": ("CORE_MAPS", "soul_core"),
        "staticite_cell": ("GEM_MAPS", "prism"),
        "voidsteel_ingot": ("INGOT_MAPS", "standard"),
        "aetherium_ingot": ("INGOT_MAPS", "standard"),
        "lumenshade_ingot": ("INGOT_MAPS", "standard"),
        "rootiron_ingot": ("INGOT_MAPS", "standard"),
        "skylead_ingot": ("INGOT_MAPS", "standard"),
        "nullite_shard": ("GEM_MAPS", "shard"),
        "gloomite_shard": ("GEM_MAPS", "shard"),
        "hollowite_gem": ("GEM_MAPS", "brilliant"),
        "echo_crystal": ("GEM_MAPS", "prism"),
        "duskite_gem": ("GEM_MAPS", "brilliant"),
        "fracture_shale_shard": ("GEM_MAPS", "shard"),
        "bloodstone_gem": ("GEM_MAPS", "brilliant"),
        "witherite_dust": ("DUST_MAPS", "pile"),
        "graveamber_chunk": ("GEM_MAPS", "brilliant"),
        "sporeamber_chunk": ("GEM_MAPS", "brilliant"),
        "wraithsalt_crystal": ("GEM_MAPS", "prism"),
        "glimmerleaf_fiber": ("DUST_MAPS", "pile"),
        "petrichorite_crystal": ("GEM_MAPS", "prism"),
        "emberquartz_shard": ("GEM_MAPS", "shard"),
        "frostbloom_bloom": ("GEM_MAPS", "brilliant"),
        "coralite_polish": ("GEM_MAPS", "brilliant"),
        "spiritwood_splinter": ("ROD_MAPS", "staff_rod"),
        "titanite_plate": ("PLATE_MAPS", "sheet"),
        "dawnshard": ("GEM_MAPS", "shard"),
        "sunspore_pod": ("ESSENCE_MAPS", "mote"),
        "deep_pearl": ("PEARL_MAPS", "sphere"),
        "umbrite": ("DUST_MAPS", "pile"),
        "lumenite_shard": ("GEM_MAPS", "shard"),
        "sunscorch_ingot": ("INGOT_MAPS", "standard"),
        "glacierite_shard": ("GEM_MAPS", "shard"),
        "crown_shard": ("GEM_MAPS", "prism"),
    }
    for item_id, (attr, key) in sorted(extra_drops.items()):
        rows = getattr(items_maps, attr)[key]
        w.emit(_rel("textures", "item", f"{item_id}.png"),
               map_to_matrix(rows, _complete(item_glyphs(mineral_fallback), mineral_fallback)),
               name=item_id)

    # --- lore books -------------------------------------------------------
    lore_books = {
        "lore_book_heart": "lumen_leaves",
        "lore_book_void": "voidcap",
        "lore_book_hollow": "glowcap",
        "lore_book_aether": "aether_leaves",
        "lore_book_unraveling": "voidcap",
        "lore_book_tide": "glowcap",
        "lore_book_grove": "lumen_leaves",
        "lore_book_star": "aether_leaves",
        "lore_book_frost": "crystal_leaves",
        "lore_book_death": "voidcap",
        "lore_book_road": "petrified_leaves",
        "lore_book_colossus": "petrified_leaves",
        "lore_book_ancient": "petrified_leaves",
        "lore_book_mire": "sporecap",
        "lore_book_deep": "glowcap",
        "lore_book_ash": "sporecap",
    }
    for book, ramp_name in sorted(lore_books.items()):
        ramp = organic_ramp(ramp_name)
        w.emit(_rel("textures", "item", f"{book}.png"),
               map_to_matrix(items_maps.UTILITY_ITEM_MAPS["lore_book"],
                             _complete(flora_glyphs(ramp), ramp)), name=book)

    # --- spawn eggs -------------------------------------------------------
    # Golden Rule #4: every entity gets a valid egg texture. The egg is the
    # authored mote composition tinted with the species' hide/accent pair.
    for spec in list(MOBS.ALL_MOBS) + [b.mob for b in BOSSES.ALL_BOSSES]:
        glyphs = {
            "C": spec.accent, "H": spec.skin, "L": spec.skin, "M": spec.hide,
            "D": spec.hide, "S": spec.hide, "O": spec.hide, "G": spec.eye,
            "g": spec.accent, "A": spec.accent, "a": spec.hide,
            "E": spec.eye, "e": spec.eye, "B": spec.bone, "b": spec.bone,
            "W": "#FFFFFF", "T": spec.accent,
        }
        w.emit(_rel("textures", "item", f"{spec.id}_spawn_egg.png"),
               map_to_matrix(items_maps.ESSENCE_MAPS["mote"], _complete(glyphs, {"H": spec.skin, "L": spec.hide, "M": spec.hide, "D": spec.hide, "S": spec.hide, "O": spec.hide})),
               name=f"{spec.id}_spawn_egg", min_tones=3)


def emit_creatures(w: TextureWriter) -> None:
    """80 mob atlases: authored family atlas + curated palette + hand-placed
    species overlays."""
    for spec in MOBS.ALL_MOBS:
        atlas_rows = creature_maps.build_family_atlas(spec.family)
        glyphs = creature_glyphs(spec)
        matrix = map_to_matrix(atlas_rows, _complete(glyphs, {
            "H": spec.skin, "L": spec.hide, "M": spec.hide,
            "D": spec.hide, "S": spec.hide, "O": spec.hide,
        }))

        for overlay_id in spec.overlays:
            overlay = creature_maps.OVERLAYS.get(overlay_id)
            if overlay is None:
                w.problems.append(f"{spec.id}: unknown overlay {overlay_id!r}")
                continue
            dx, dy = overlay["at"]
            if overlay_id == "no_marking":
                continue
            patch = map_to_matrix(overlay["rows"], _complete(glyphs, {
                "H": spec.skin, "L": spec.hide, "M": spec.hide,
                "D": spec.hide, "S": spec.hide, "O": spec.hide,
            }))
            matrix = compose(matrix, [(dx, dy, patch)])

        w.emit(_rel("textures", "entity", f"{spec.id}.png"), matrix,
               name=f"entity/{spec.id}", min_tones=3)


def emit_bosses(w: TextureWriter) -> None:
    """5 boss atlases, each 64x64, fully hand-authored."""
    for boss in BOSSES.ALL_BOSSES:
        atlas_rows = boss_maps.build_boss(boss.id)
        glyphs = creature_glyphs(boss.mob)
        matrix = map_to_matrix(atlas_rows, _complete(glyphs, {
            "H": boss.mob.skin, "L": boss.mob.hide, "M": boss.mob.hide,
            "D": boss.mob.hide, "S": boss.mob.hide, "O": boss.mob.hide,
        }))
        w.emit(_rel("textures", "entity", "boss", f"{boss.id}.png"), matrix,
               name=f"boss/{boss.id}", min_tones=4)


def emit_gui(w: TextureWriter) -> None:
    """Particles and the creative tab icon."""
    # No boss bar textures are emitted. They were authored here as four rows per
    # boss from that boss's own palette, but nothing could load them: a custom bar
    # fill needs either a mixin into BossHealthOverlay -- this mod ships no mixin
    # config, deliberately -- or cancelling Forge's BOSS_EVENT_PROGRESS overlay
    # and re-rendering every bar, vanilla dragon and wither included, from
    # BossHealthOverlay.events, which is private. Neither is acceptable, so boss
    # bars render through vanilla's own BossBarColor and BossBarOverlay enums,
    # driven by BossData.boss_bar_color and boss_bar_overlay. Shipping five
    # sprites that no code path could reach only added weight to the jar and
    # implied a custom bar that does not exist.

    # Particles: 8x8 authored sparkles packed into the vanilla 128x128 sheet
    # layout would need 64 cells; we ship a single-cell 16x16 per particle and
    # reference it from a custom ParticleType with its own sprite.
    particle_rows = [
        "................",
        "......HH........",
        ".....HLLH.......",
        "....HLLLLH......",
        "...HLLMLLH......",
        "....HLLLLH......",
        ".....HLLH.......",
        "......HH........",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
    ]
    for particle, ramp_name in (("lumen_mote", "lumen_leaves"),
                                ("moonpetal_drift", "lumen_leaves"),
                                ("starfall_ember", "sporecap"),
                                ("aurora_ribbon", "crystal_leaves"),
                                ("aetherveil_mote", "aether_leaves"),
                                ("ember_drift", "sporecap"),
                                ("heat_shimmer", "sunbleached_stone"),
                                ("pollen_drift", "sporecap"),
                                ("spore_drift", "sporecap"),
                                ("void_fracture", "voidcap"),
                                ("page_drift", "petrified_leaves")):
        if ramp_name in palettes.ORGANIC_RAMPS:
            ramp = organic_ramp(ramp_name)
            glyphs = flora_glyphs(ramp)
        else:
            glyphs = _special_glyphs(ramp_name)
        w.emit(_rel("textures", "particle", f"{particle}.png"),
               map_to_matrix(particle_rows, _complete(glyphs, ramp if isinstance(ramp, dict) else {"H": "#FFFFFF", "L": "#DDDDDD", "M": "#AAAAAA", "D": "#666666", "S": "#333333", "O": "#111111"})),
               name=f"particle/{particle}", min_tones=3)

    # Creative tab icon: the Heart of the Forest artefact.
    glyphs = gear_glyphs(palettes.GEAR_RAMPS["lumenshade"])
    w.emit(_rel("textures", "item", "biomesunseen_tab_icon.png"),
           map_to_matrix(gear_maps.STAFF_MAPS["heart_of_forest_staff"],
                         _complete(glyphs, palettes.GEAR_RAMPS["lumenshade"])),
           name="tab_icon")


def emit_all(w: TextureWriter) -> None:
    emit_stones(w)
    emit_ores(w)
    emit_ore_items(w)
    emit_surface_blocks(w)
    emit_gear(w)
    emit_items(w)
    emit_creatures(w)
    emit_bosses(w)
    emit_gui(w)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="resolve and encode everything but write no files")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    writer = TextureWriter(check_only=args.check)
    emit_all(writer)

    if not args.quiet:
        print(f"[art] resolved {len(writer.written)} textures")
        if not args.check:
            print(f"[art] wrote/updated {len(writer.changed)} PNG files")
        if writer.changed:
            for path in writer.changed[:12]:
                print(f"      + {path}")
            if len(writer.changed) > 12:
                print(f"      ... and {len(writer.changed) - 12} more")
        if writer.audit_notes:
            print(f"[art] {len(writer.audit_notes)} tonal audit note(s):")
            for note in writer.audit_notes[:10]:
                print(f"      ! {note}")
        if writer.problems:
            print(f"[art] {len(writer.problems)} PROBLEM(s):")
            for prob in writer.problems[:20]:
                print(f"      X {prob}")

    if writer.problems:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
