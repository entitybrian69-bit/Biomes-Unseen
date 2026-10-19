#!/usr/bin/env python3
"""
Biomes Unseen -- asset & data resource generator.

Emits every JSON the mod needs around its Java registries, driven entirely by
tools/registry.py (which is itself driven by tools/content/*). Nothing here is
hand-written per-block: adding a biome, ore or mob to the content tables makes
its blockstate, models, loot table, recipes, tags and lang entries appear on
the next run.

Outputs
-------
assets/biomesunseen/
    blockstates/<block>.json          264
    models/block/<block>.json         per block kind
    models/item/<item>.json           every item + block-item
    lang/en_us.json                   every display name + lore
data/biomesunseen/
    loot_tables/blocks/<block>.json
    loot_tables/entities/<mob>.json
    loot_tables/chests/<structure>.json
    recipes/*.json
    tags/**.json
src/main/resources/
    pack.mcmeta
    META-INF/mods.toml
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import sys
from typing import Dict, Iterable, List, Optional, Set, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import content.biomes as BIOMES        # noqa: E402
import content.bosses as BOSSES        # noqa: E402
import content.gear as GEAR            # noqa: E402
import content.mobs as MOBS            # noqa: E402
import content.ores as ORES            # noqa: E402
import content.structures as STRUCTS   # noqa: E402
import registry as REG                 # noqa: E402

MODID = REG.MODID
R = REG.REGISTRY

RES = os.path.join(ROOT, "src", "main", "resources")
ASSETS = os.path.join(RES, "assets", MODID)
DATA = os.path.join(RES, "data", MODID)

PACK_FORMAT = 15          # Minecraft 1.20.1
FORGE_VERSION = "47.2.20"
MC_VERSION = "1.20.1"

TOOL_SET_BY_ID: Dict[str, object] = {t.id: t for t in GEAR.TOOL_SETS}
ARMOR_SET_BY_ID: Dict[str, object] = {a.id: a for a in GEAR.ARMOR_SETS}
ORE_BY_BLOCK: Dict[str, object] = {}
for _o in ORES.ALL_ORES:
    ORE_BY_BLOCK[_o.ore_block] = _o
    if _o.deepslate_ore_block:
        ORE_BY_BLOCK[_o.deepslate_ore_block] = _o
MOB_BY_ID: Dict[str, object] = {m.id: m for m in MOBS.ALL_MOBS}
BOSS_BY_ID: Dict[str, object] = {b.id: b for b in BOSSES.ALL_BOSSES}
STRUCT_BY_ID: Dict[str, object] = {s.id: s for s in STRUCTS.ALL_STRUCTURES}


class Writer:
    """Writes JSON files, tracking what changed so runs are reviewable."""

    def __init__(self, check_only: bool = False) -> None:
        self.check_only = check_only
        self.written: List[str] = []
        self.changed: List[str] = []
        self.problems: List[str] = []

    def json(self, path: str, obj: object) -> None:
        text = json.dumps(obj, indent=2, sort_keys=False) + "\n"
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        self.written.append(rel)
        if self.check_only:
            return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        old = None
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fh:
                old = fh.read()
        if old != text:
            self.changed.append(rel)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)

    def text(self, path: str, text: str) -> None:
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        self.written.append(rel)
        if self.check_only:
            return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        old = None
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fh:
                old = fh.read()
        if old != text:
            self.changed.append(rel)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)


def bpath(*parts: str) -> str:
    return os.path.join(ASSETS, *parts)


def dpath(*parts: str) -> str:
    return os.path.join(DATA, *parts)


def rid(path: str) -> str:
    """
    Qualify a registry path with our namespace.

    An id that already carries a namespace ('minecraft:paper', 'forge:ingots')
    is passed through untouched: re-prefixing it would emit the malformed
    'biomesunseen:minecraft:paper', which Forge rejects at datapack load and
    which silently breaks every recipe that mixes vanilla and mod ingredients.
    """
    return path if ":" in path else f"{MODID}:{path}"


# --------------------------------------------------------------------------- #
#  Block models + blockstates
# --------------------------------------------------------------------------- #

def grass_filler(block: str) -> str:
    """The dirt/loam a grass block drops and shows on its underside."""
    for biome in BIOMES.ALL_BIOMES:
        top = biome.surface_top.split(":")[-1]
        fill = biome.surface_filler.split(":")[-1]
        if top == block and fill in R.block_set:
            return fill
    return block.replace("grass_block", "dirt")


def block_model(block: str) -> Optional[dict]:
    """Model JSON for a block, or None when the block has no baked model."""
    kind = R.block_kind(block)
    tex = f"{MODID}:block/{block}"

    if kind == REG.BlockKind.GRASS:
        filler = grass_filler(block)
        side = f"{MODID}:block/{block}_side" if R.has_face(block, "side") else tex
        return {
            "parent": "minecraft:block/cube_bottom_top",
            "textures": {
                "bottom": f"{MODID}:block/{filler}",
                "top": tex,
                "side": side,
                "particle": side,
            },
        }

    if kind == REG.BlockKind.LOG:
        end = f"{MODID}:block/{block}_top" if R.has_face(block, "top") else tex
        return {
            "parent": "minecraft:block/cube_column",
            "textures": {"end": end, "side": tex, "particle": tex},
        }

    if kind == REG.BlockKind.ALTAR:
        end = f"{MODID}:block/{block}_top" if R.has_face(block, "top") else tex
        return {
            "parent": "minecraft:block/cube_column",
            "textures": {"end": end, "side": tex, "particle": tex},
        }

    if kind == REG.BlockKind.CROSS:
        # Cutout so the authored silhouette keeps its transparent corners.
        return {
            "parent": "minecraft:block/cross",
            "render_type": "minecraft:cutout",
            "textures": {"cross": tex, "particle": tex},
        }

    if kind == REG.BlockKind.PORTAL:
        return {
            "parent": "minecraft:block/cube_all",
            "render_type": "minecraft:translucent",
            "textures": {"all": tex, "particle": tex},
        }

    if kind == REG.BlockKind.LANTERN:
        return {
            "parent": "minecraft:block/cube_all",
            "render_type": "minecraft:cutout",
            "textures": {"all": tex, "particle": tex},
        }

    if kind == REG.BlockKind.FLUID:
        return None

    return {
        "parent": "minecraft:block/cube_all",
        "textures": {"all": tex, "particle": tex},
    }


def blockstate(block: str) -> dict:
    """Blockstate JSON. Fluids carry an empty variant map, as vanilla does."""
    kind = R.block_kind(block)
    if kind == REG.BlockKind.FLUID:
        return {"variants": {}}
    if kind == REG.BlockKind.LOG:
        return {
            "variants": {
                "axis=x": {"model": rid(f"block/{block}"), "x": 90, "y": 90},
                "axis=y": {"model": rid(f"block/{block}")},
                "axis=z": {"model": rid(f"block/{block}"), "x": 90},
            }
        }
    if kind == REG.BlockKind.ALTAR:
        return {
            "variants": {
                "axis=x": {"model": rid(f"block/{block}"), "x": 90, "y": 90},
                "axis=y": {"model": rid(f"block/{block}")},
                "axis=z": {"model": rid(f"block/{block}"), "x": 90},
            }
        }
    return {"variants": {"": {"model": rid(f"block/{block}")}}}


# --------------------------------------------------------------------------- #
#  Item models
# --------------------------------------------------------------------------- #

TOOL_SUFFIXES = ("sword", "pickaxe", "axe", "shovel", "hoe")
ARMOR_SUFFIXES = ("helmet", "chestplate", "leggings", "boots")


def is_tool(item: str) -> bool:
    return item.endswith(TOOL_SUFFIXES) and item in all_tool_items()


def all_tool_items() -> Set[str]:
    out: Set[str] = set()
    for ts in GEAR.TOOL_SETS:
        for tool in ts.tools:
            out.add(f"{ts.id}_{tool}")
        if ts.has_bow:
            out.add(f"{ts.id}_bow")
        if ts.has_shield:
            out.add(f"{ts.id}_shield")
    out.update(GEAR.ARTEFACT_WEAPONS.values())
    return out


def item_model(item: str) -> dict:
    """Item model JSON, including bow pull overrides."""
    # Spawn eggs use the authored per-species mote texture rather than the
    # vanilla tinted template, so every species is visually distinct.
    if item.endswith("_spawn_egg"):
        return {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": f"{MODID}:item/{item}"},
        }

    if item.endswith("_bow"):
        overrides = []
        for state in sorted(R.bow_states.get(item, [])):
            suffix = state.rsplit("_", 1)[-1]
            overrides.append({
                "predicate": {"minecraft:pulling": 1, "minecraft:pull": 0.0},
                "model": rid(f"item/{state}"),
            })
        model = {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": f"{MODID}:item/{item}"},
        }
        if overrides:
            model["overrides"] = overrides
        return model

    if item in R.bow_states or "_pulling_" in item:
        return {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": f"{MODID}:item/{item}"},
        }

    if item in all_tool_items():
        # handheld gives tools the correct tilted grip transform.
        return {
            "parent": "minecraft:item/handheld",
            "textures": {"layer0": f"{MODID}:item/{item}"},
        }

    # Block items reference their block model so the inventory icon matches.
    if item in R.block_set:
        kind = R.block_kind(item)
        if kind in (REG.BlockKind.CROSS, REG.BlockKind.PORTAL,
                    REG.BlockKind.LANTERN):
            folder = "block"
            return {
                "parent": "minecraft:item/generated",
                "textures": {"layer0": f"{MODID}:{folder}/{item}"},
            }
        if kind == REG.BlockKind.FLUID:
            # Fluids are bucketed, not held; the bucket uses its own texture.
            return {
                "parent": "minecraft:item/generated",
                "textures": {"layer0": f"minecraft:item/water_bucket"},
            }
        return {"parent": rid(f"block/{item}")}

    return {
        "parent": "minecraft:item/generated",
        "textures": {"layer0": f"{MODID}:item/{item}"},
    }


# --------------------------------------------------------------------------- #
#  Loot tables
# --------------------------------------------------------------------------- #

def self_drop(block: str, lo: int = 1, hi: int = 1) -> dict:
    entry: dict = {
        "type": "minecraft:item",
        "name": rid(block),
    }
    if lo != 1 or hi != 1:
        entry["functions"] = [{
            "function": "minecraft:set_count",
            "count": {"type": "minecraft:uniform", "min": lo, "max": hi},
            "add": False,
        }]
    return {
        "type": "minecraft:block",
        "pools": [{
            "rolls": 1.0,
            "bonus_rolls": 0.0,
            "entries": [entry],
            "conditions": [{"condition": "minecraft:survives_explosion"}],
        }],
    }


def drop_item(item: str, lo: int, hi: int, fortune: bool = True) -> dict:
    funcs: List[dict] = []
    if lo != 1 or hi != 1:
        funcs.append({
            "function": "minecraft:set_count",
            "count": {"type": "minecraft:uniform", "min": lo, "max": hi},
            "add": False,
        })
    if fortune:
        funcs.append({
            "function": "minecraft:apply_bonus",
            "enchantment": "minecraft:fortune",
            "formula": "minecraft:ore_drops",
        })
    funcs.append({"function": "minecraft:explosion_decay"})
    entry: dict = {"type": "minecraft:item", "name": rid(item)}
    if funcs:
        entry["functions"] = funcs
    return {
        "type": "minecraft:block",
        "pools": [{"rolls": 1.0, "bonus_rolls": 0.0, "entries": [entry]}],
    }


def empty_loot() -> dict:
    return {"type": "minecraft:block", "pools": []}


def silk_touch_alternative(block: str, alt_pool: dict) -> dict:
    """Drop the block itself under Silk Touch, otherwise the alternative."""
    return {
        "type": "minecraft:block",
        "pools": [{
            "rolls": 1.0,
            "bonus_rolls": 0.0,
            "entries": [{
                "type": "minecraft:alternatives",
                "children": [
                    {
                        "type": "minecraft:item",
                        "name": rid(block),
                        "conditions": [{
                            "condition": "minecraft:match_tool",
                            "predicate": {
                                "enchantments": [{
                                    "enchantment": "minecraft:silk_touch",
                                    "levels": {"min": 1},
                                }],
                            },
                        }],
                    },
                    alt_pool["pools"][0]["entries"][0],
                ],
            }],
        }],
    }


def block_loot(block: str) -> dict:
    kind = R.block_kind(block)

    if kind == REG.BlockKind.FLUID or kind == REG.BlockKind.PORTAL:
        return empty_loot()

    if kind == REG.BlockKind.GRASS:
        # Grass blocks drop their substrate, exactly like vanilla grass.
        return self_drop(grass_filler(block))

    if kind == REG.BlockKind.ORE:
        ore = ORE_BY_BLOCK.get(block)
        if ore is None:
            return self_drop(block)
        drop = ore.drop or f"{ore.base_name}_raw"
        if drop not in R.item_set:
            return self_drop(block)
        lo, hi = (ore.drop_count if isinstance(ore.drop_count, tuple)
                  else (1, 1))
        return silk_touch_alternative(block, drop_item(drop, lo, hi))

    if kind == REG.BlockKind.CROSS:
        return self_drop(block)

    return self_drop(block)


def entity_loot(mob: object) -> dict:
    """Mob drops, from the authored drop tuples plus experience."""
    pools: List[dict] = []
    for drop in getattr(mob, "drops", ()):
        ident, lo, hi, chance = drop[0], drop[1], drop[2], drop[3]
        if ":" in ident and not ident.startswith(f"{MODID}:"):
            name = ident
        else:
            bare = ident.split(":")[-1]
            if bare not in R.item_set:
                continue
            name = rid(bare)
        entry: dict = {"type": "minecraft:item", "name": name}
        funcs: List[dict] = [{
            "function": "minecraft:set_count",
            "count": {"type": "minecraft:uniform", "min": lo, "max": hi},
            "add": False,
        }, {
            "function": "minecraft:looting_enchant",
            "count": {"type": "minecraft:uniform", "min": 0.0, "max": 1.0},
        }]
        entry["functions"] = funcs
        pool: dict = {"rolls": 1.0, "bonus_rolls": 0.0, "entries": [entry]}
        if chance < 1.0:
            pool["conditions"] = [{
                "condition": "minecraft:random_chance_with_looting",
                "chance": chance,
                "looting_multiplier": 0.02,
            }]
        pools.append(pool)
    return {"type": "minecraft:entity", "pools": pools}


def boss_loot(boss: object) -> dict:
    """Boss loot: guaranteed artefact pieces plus the lore book."""
    pools: List[dict] = []
    struct = STRUCT_BY_ID.get(boss.arena_structure.split(":")[-1])
    lore = getattr(struct, "lore_book", None) if struct else None
    for item, lo, hi in _boss_drops(boss):
        if item not in R.item_set:
            continue
        pools.append({
            "rolls": 1.0,
            "bonus_rolls": 0.0,
            "entries": [{
                "type": "minecraft:item",
                "name": rid(item),
                "functions": [{
                    "function": "minecraft:set_count",
                    "count": {"type": "minecraft:uniform", "min": lo, "max": hi},
                    "add": False,
                }],
            }],
        })
    if lore and lore.split(":")[-1] in R.item_set:
        pools.append({
            "rolls": 1.0, "bonus_rolls": 0.0,
            "entries": [{"type": "minecraft:item",
                         "name": rid(lore.split(":")[-1])}],
        })
    return {"type": "minecraft:entity", "pools": pools}


def _boss_drops(boss: object) -> List[Tuple[str, int, int]]:
    """Authored boss drops, read from the structure/boss table."""
    out: List[Tuple[str, int, int]] = []
    raw = getattr(boss, "drops", ())
    for entry in raw:
        if isinstance(entry, tuple) and len(entry) >= 3:
            out.append((str(entry[0]).split(":")[-1], int(entry[1]), int(entry[2])))
        elif isinstance(entry, str):
            out.append((entry.split(":")[-1], 1, 1))
    return out


def chest_loot(struct: object) -> dict:
    """Structure chest loot: themed junk plus the mandatory lore book."""
    pools: List[dict] = []
    entries: List[dict] = []
    for loot_ref in getattr(struct, "loot_tables", ()):
        # The authored value is already a fully qualified loot-table path
        # ('biomesunseen:chests/lore/grove'). Prefixing it again would produce
        # 'chests/chests/lore/grove' and a dangling reference at load time.
        entries.append({
            "type": "minecraft:loot_table",
            "name": loot_ref,
            "weight": 1,
        })
    # Guarantee at least some content so the chest is never empty.
    filler = [i for i in R.items if i.endswith(("_shard", "_gem", "_ingot",
                                                "_crystal", "_chunk"))]
    for item in sorted(filler)[:12]:
        entries.append({
            "type": "minecraft:item",
            "name": rid(item),
            "weight": 6,
            "functions": [{
                "function": "minecraft:set_count",
                "count": {"type": "minecraft:uniform", "min": 1, "max": 4},
                "add": False,
            }],
        })
    if entries:
        pools.append({
            "rolls": {"type": "minecraft:uniform", "min": 3.0, "max": 7.0},
            "bonus_rolls": 0.0,
            "entries": entries,
        })
    lore = getattr(struct, "lore_book", None)
    if lore:
        bare = lore.split(":")[-1]
        if bare in R.item_set:
            pools.append({
                "rolls": 1.0, "bonus_rolls": 0.0,
                "entries": [{"type": "minecraft:item", "name": rid(bare)}],
            })
    return {"type": "minecraft:chest", "pools": pools}


# --------------------------------------------------------------------------- #
#  Recipes
# --------------------------------------------------------------------------- #

def smelting(result: str, ingredient: str, xp: float, time: int) -> dict:
    return {
        "type": "minecraft:smelting",
        "category": "misc",
        "ingredient": {"item": rid(ingredient)},
        "result": rid(result),
        "experience": xp,
        "cookingtime": time,
    }


def blasting(result: str, ingredient: str, xp: float) -> dict:
    return {
        "type": "minecraft:blasting",
        "category": "misc",
        "ingredient": {"item": rid(ingredient)},
        "result": rid(result),
        "experience": xp,
        "cookingtime": 100,
    }


def shaped(result: str, count: int, pattern: List[str], key: Dict[str, str]) -> dict:
    return {
        "type": "minecraft:crafting_shaped",
        "category": "equipment",
        "pattern": pattern,
        "key": {k: {"item": rid(v)} for k, v in key.items()},
        "result": {"item": rid(result), "count": count},
    }


def shapeless(result: str, count: int, ingredients: List[str]) -> dict:
    return {
        "type": "minecraft:crafting_shapeless",
        "category": "misc",
        "ingredients": [{"item": rid(i)} for i in ingredients],
        "result": {"item": rid(result), "count": count},
    }


TOOL_PATTERNS: Dict[str, Tuple[List[str], Dict[str, str]]] = {
    "sword": (["M", "M", "S"], {"M": "material", "S": "stick"}),
    "pickaxe": (["MMM", " S ", " S "], {"M": "material", "S": "stick"}),
    "axe": (["MM", "MS", " S"], {"M": "material", "S": "stick"}),
    "shovel": (["M", "S", "S"], {"M": "material", "S": "stick"}),
    "hoe": (["MM", " S", " S"], {"M": "material", "S": "stick"}),
}
ARMOR_PATTERNS: Dict[str, List[str]] = {
    "helmet": ["MMM", "M M"],
    "chestplate": ["M M", "MMM", "MMM"],
    "leggings": ["MMM", "M M", "M M"],
    "boots": ["M M", "M M"],
}


# --------------------------------------------------------------------------- #
#  Referenced nested loot tables
# --------------------------------------------------------------------------- #

# Vanilla staples that always make a chest feel stocked. They are real vanilla
# ids, so they need no texture of our own.
VANILLA_STAPLES: Tuple[str, ...] = (
    "minecraft:bread", "minecraft:torch", "minecraft:iron_ingot",
    "minecraft:gold_ingot", "minecraft:emerald", "minecraft:bone",
    "minecraft:string", "minecraft:paper", "minecraft:book",
    "minecraft:coal", "minecraft:redstone", "minecraft:glowstone_dust",
    "minecraft:golden_carrot", "minecraft:arrow", "minecraft:experience_bottle",
)

# Materials a portal chest should hand the player, so a found portal is usable.
PORTAL_KITS: Dict[str, Tuple[str, ...]] = {
    "hollow_deep": ("portal_igniter", "hollowite_gem", "gloomite_shard"),
    "aetherfall": ("portal_igniter", "aetherium_refined", "dawnshard"),
    "void_between": ("portal_igniter", "voidsteel_ingot", "nullite_shard"),
}


def _stable_seed(text: str) -> int:
    """Deterministic per-path seed so chest contents never churn between runs."""
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:8], 16)


def dimension_materials(dimension: str) -> List[str]:
    """Refined materials sourced from ores belonging to one dimension."""
    out: List[str] = []
    for ore in ORES.ALL_ORES:
        if ore.dimension != dimension:
            continue
        drop = (ore.drop or f"{ore.base_name}_raw").split(":")[-1]
        if drop in R.item_set:
            out.append(drop)
        ts = TOOL_SET_BY_ID.get(ore.base_name)
        if ts and ts.repair_item.startswith(f"{MODID}:"):
            refined = ts.repair_item.split(":")[-1]
            if refined in R.item_set:
                out.append(refined)
    return sorted(set(out)) or sorted(
        i for i in R.items if i.endswith(("_shard", "_gem", "_ingot"))
    )


def themed_chest(path: str, dimension: str) -> dict:
    """
    Build a themed chest table for a referenced nested loot path.

    The theme comes from the path itself: 'lore/<theme>' chests guarantee lore
    fragments, 'boss_arena/<boss>' chests reward the artefact material, and
    'portal/<dim>' chests hand over an igniter so the portal is actually
    usable. Everything else draws from the dimension's own materials.
    """
    rng = random.Random(_stable_seed(path))
    segment = path.split("/")[-1]
    materials = dimension_materials(dimension)
    entries: List[dict] = []

    def item(name: str, weight: int, lo: int = 1, hi: int = 3) -> None:
        entries.append({
            "type": "minecraft:item",
            "name": name if ":" in name else rid(name),
            "weight": weight,
            "functions": [{
                "function": "minecraft:set_count",
                "count": {"type": "minecraft:uniform", "min": lo, "max": hi},
                "add": False,
            }],
        })

    if "lore" in path:
        if "lore_fragment" in R.item_set:
            item("lore_fragment", 20, 2, 5)
        item("minecraft:book", 14, 1, 2)
        item("minecraft:paper", 16, 2, 6)
        books = sorted(i for i in R.items if i.startswith("lore_book_"))
        if books:
            item(rng.choice(books), 6, 1, 1)
    elif "boss_arena" in path:
        boss_id = next((b.id for b in BOSSES.ALL_BOSSES if b.id in path), None)
        if boss_id:
            for cand in (f"{boss_id}_core", f"{boss_id}_shard",
                         f"{boss_id}_fragment"):
                if cand in R.item_set:
                    item(cand, 20, 1, 2)
            weapon = GEAR.ARTEFACT_WEAPONS.get(boss_id)
            if weapon and weapon in R.item_set:
                item(weapon, 3, 1, 1)
        for mat in materials[:6]:
            item(mat, 10, 2, 6)
    elif "portal" in path:
        for kit in PORTAL_KITS.get(segment, ("portal_igniter",)):
            if kit in R.item_set:
                item(kit, 25, 1, 1)
        for mat in materials[:5]:
            item(mat, 10, 1, 4)
    else:
        for mat in rng.sample(materials, min(6, len(materials))):
            item(mat, 10, 1, 4)

    for staple in rng.sample(VANILLA_STAPLES, 6):
        item(staple, 8, 1, 4)

    # Enchanted book as the rare pull, so every chest has a chase item.
    entries.append({
        "type": "minecraft:item",
        "name": "minecraft:enchanted_book",
        "weight": 2,
        "functions": [{"function": "minecraft:enchant_randomly"}],
    })

    return {
        "type": "minecraft:chest",
        "pools": [{
            "rolls": {"type": "minecraft:uniform", "min": 4.0, "max": 8.0},
            "bonus_rolls": 0.0,
            "entries": entries,
        }],
    }


def emit_referenced_chests(w: Writer) -> None:
    """
    Emit a real file for every nested loot path the structure table references.

    Without this, a structure's chest pool points at a loot table that does not
    exist and the chest loads empty.
    """
    owner: Dict[str, str] = {}
    for struct in STRUCTS.ALL_STRUCTURES:
        for loot_ref in getattr(struct, "loot_tables", ()):
            path = loot_ref.split(":")[-1]
            owner.setdefault(path, struct.dimension)
    for path, dimension in sorted(owner.items()):
        # The authored path is a registry path, not a filename: the '.json'
        # suffix has to be added here or the table lands as an extensionless
        # file that the datapack loader never reads.
        dest = dpath("loot_tables", *path.split("/")) + ".json"
        w.json(dest, themed_chest(path, dimension))


def emit_recipes(w: Writer) -> None:
    emitted: Set[str] = set()

    def put(name: str, obj: dict) -> None:
        if name in emitted:
            return
        emitted.add(name)
        w.json(dpath("recipes", f"{name}.json"), obj)

    # --- ore -> refined material ----------------------------------------
    for ore in ORES.ALL_ORES:
        drop = (ore.drop or f"{ore.base_name}_raw").split(":")[-1]
        if drop not in R.item_set:
            continue
        # The refined product is whatever the matching gear set repairs with.
        ts = TOOL_SET_BY_ID.get(ore.base_name)
        target = None
        if ts and ts.repair_item.startswith(f"{MODID}:"):
            cand = ts.repair_item.split(":")[-1]
            if cand in R.item_set:
                target = cand
        if target is None:
            for suffix in ("_ingot", "_refined", "_gem"):
                cand = f"{ore.base_name}{suffix}"
                if cand in R.item_set:
                    target = cand
                    break
        if target is None or target == drop:
            continue
        xp = 0.7 + (ore.tier or 1) * 0.2
        put(f"smelting_{target}_from_{drop}", smelting(target, drop, xp, 200))
        put(f"blasting_{target}_from_{drop}", blasting(target, drop, xp))
        # The ore block itself can be smelted directly (silk-touch route).
        for blk in filter(None, (ore.ore_block, ore.deepslate_ore_block)):
            if blk in R.block_set:
                put(f"smelting_{target}_from_{blk}",
                    smelting(target, blk, xp, 200))

    # --- mineral block <-> 9 material -----------------------------------
    for ore in ORES.ALL_ORES:
        ts = TOOL_SET_BY_ID.get(ore.base_name)
        material = None
        if ts and ts.repair_item.startswith(f"{MODID}:"):
            cand = ts.repair_item.split(":")[-1]
            if cand in R.item_set:
                material = cand
        if material is None:
            continue
        blk = ore.mineral_block
        if blk not in R.block_set:
            continue
        put(f"{material}_from_{blk}", shapeless(material, 9, [blk]))
        put(blk, shaped(blk, 1, ["MMM", "MMM", "MMM"], {"M": material}))

    # --- logs -> planks, planks -> sticks --------------------------------
    for block in R.blocks_of_kind(REG.BlockKind.LOG):
        base = block[:-4] if block.endswith("_log") else block
        planks = f"{base}_planks"
        if planks in R.block_set:
            put(f"{planks}_from_{block}", shapeless(planks, 4, [block]))

    # --- tools and armor -------------------------------------------------
    for ts in GEAR.TOOL_SETS:
        material = ts.repair_item.split(":")[-1] if ts.repair_item else None
        if not material or material not in R.item_set:
            continue
        stick = "minecraft:stick"
        for tool in ts.tools:
            item = f"{ts.id}_{tool}"
            if item not in R.item_set or tool not in TOOL_PATTERNS:
                continue
            pattern, key = TOOL_PATTERNS[tool]
            concrete = {k: (material if v == "material" else stick)
                        for k, v in key.items()}
            obj = shaped(item, 1, pattern, concrete)
            put(item, obj)
        if ts.has_shield:
            item = f"{ts.id}_shield"
            if item in R.item_set:
                obj = shaped(item, 1, ["MWM", "MMM", " M "],
                             {"M": material, "W": "shield_wood"})
                obj["key"]["W"] = {"tag": "minecraft:planks"}
                put(item, obj)

    for aset in GEAR.ARMOR_SETS:
        material = aset.repair_item.split(":")[-1] if aset.repair_item else None
        if not material or material not in R.item_set:
            continue
        for piece in aset.pieces:
            item = f"{aset.id}_{piece}"
            if item not in R.item_set or piece not in ARMOR_PATTERNS:
                continue
            put(item, shaped(item, 1, ARMOR_PATTERNS[piece], {"M": material}))

    # --- boss artefacts --------------------------------------------------
    for boss_id, weapon in GEAR.ARTEFACT_WEAPONS.items():
        if weapon not in R.item_set:
            continue
        core = f"{boss_id}_core"
        if core not in R.item_set:
            core = next((i for i in R.items
                         if i.startswith(boss_id.split("_")[0]) and
                         i.endswith(("_core", "_shard", "_fragment"))), None)
        if not core:
            continue
        put(weapon, shaped(weapon, 1, [" C ", " S ", " S "],
                           {"C": core, "S": "minecraft:stick"}))

    # --- lore books: fragment + paper ------------------------------------
    if "lore_fragment" in R.item_set:
        for book in [i for i in R.items if i.startswith("lore_book")]:
            put(book, shapeless(book, 1, ["lore_fragment", "minecraft:paper",
                                          "minecraft:book"]))

    # --- portal igniter --------------------------------------------------
    if "portal_igniter" in R.item_set:
        mats = [i for i in ("lumenite_shard", "voidsteel_ingot")
                if i in R.item_set] + ["minecraft:blaze_rod"]
        put("portal_igniter", shapeless("portal_igniter", 1, mats[:3]))


# --------------------------------------------------------------------------- #
#  Tags
# --------------------------------------------------------------------------- #

def tag_list(values: Iterable[str]) -> dict:
    return {"replace": False, "values": sorted(set(values))}


def emit_tags(w: Writer) -> None:
    mc_blocks = os.path.join(RES, "data", "minecraft", "tags", "blocks")
    mc_items = os.path.join(RES, "data", "minecraft", "tags", "items")
    forge_blocks = os.path.join(RES, "data", "forge", "tags", "blocks")
    forge_items = os.path.join(RES, "data", "forge", "tags", "items")

    pickaxe, axe, shovel, hoe = [], [], [], []
    stone_tool, iron_tool, diamond_tool = [], [], []

    for block in R.blocks:
        kind = R.block_kind(block)
        ident = rid(block)
        if kind in (REG.BlockKind.FLUID, REG.BlockKind.PORTAL,
                    REG.BlockKind.CROSS):
            continue
        if kind == REG.BlockKind.LOG or block.endswith("_planks"):
            axe.append(ident)
        elif kind == REG.BlockKind.GRASS or block.endswith(
                ("_dirt", "_loam", "_sand", "_silt", "_mud", "_grit",
                 "_gravel", "_hardpan", "_crust", "_chalk")):
            shovel.append(ident)
        else:
            pickaxe.append(ident)
        ore = ORE_BY_BLOCK.get(block)
        tier = (ore.tier if ore else None) or _default_tier(block, kind)
        if tier >= 4:
            diamond_tool.append(ident)
        elif tier >= 3:
            iron_tool.append(ident)
        elif tier >= 1:
            stone_tool.append(ident)

    w.json(os.path.join(mc_blocks, "mineable", "pickaxe.json"), tag_list(pickaxe))
    w.json(os.path.join(mc_blocks, "mineable", "axe.json"), tag_list(axe))
    w.json(os.path.join(mc_blocks, "mineable", "shovel.json"), tag_list(shovel))
    w.json(os.path.join(mc_blocks, "mineable", "hoe.json"), tag_list(hoe))
    w.json(os.path.join(mc_blocks, "needs_stone_tool.json"), tag_list(stone_tool))
    w.json(os.path.join(mc_blocks, "needs_iron_tool.json"), tag_list(iron_tool))
    w.json(os.path.join(mc_blocks, "needs_diamond_tool.json"), tag_list(diamond_tool))

    # --- vanilla block categories ---------------------------------------
    logs = [rid(b) for b in R.blocks_of_kind(REG.BlockKind.LOG)]
    planks = [rid(b) for b in R.blocks if b.endswith("_planks")]
    leaves = [rid(b) for b in R.blocks if b.endswith("_leaves")]
    saplings = [rid(b) for b in R.blocks if b.endswith("_sapling")]
    w.json(os.path.join(mc_blocks, "logs.json"), tag_list(logs))
    w.json(os.path.join(mc_blocks, "logs_that_burn.json"), tag_list(logs))
    w.json(os.path.join(mc_blocks, "planks.json"), tag_list(planks))
    w.json(os.path.join(mc_blocks, "leaves.json"), tag_list(leaves))
    w.json(os.path.join(mc_blocks, "saplings.json"), tag_list(saplings))
    w.json(os.path.join(mc_items, "logs.json"), tag_list(logs))
    w.json(os.path.join(mc_items, "logs_that_burn.json"), tag_list(logs))
    w.json(os.path.join(mc_items, "planks.json"), tag_list(planks))
    w.json(os.path.join(mc_items, "leaves.json"), tag_list(leaves))
    w.json(os.path.join(mc_items, "saplings.json"), tag_list(saplings))

    # --- forge ore / storage-block conventions ---------------------------
    ores = [rid(o.ore_block) for o in ORES.ALL_ORES if o.ore_block in R.block_set]
    ores += [rid(o.deepslate_ore_block) for o in ORES.ALL_ORES
             if o.deepslate_ore_block and o.deepslate_ore_block in R.block_set]
    storage = [rid(o.mineral_block) for o in ORES.ALL_ORES
               if o.mineral_block in R.block_set]
    w.json(os.path.join(forge_blocks, "ores.json"), tag_list(ores))
    w.json(os.path.join(forge_items, "ores.json"), tag_list(ores))
    w.json(os.path.join(forge_blocks, "storage_blocks.json"), tag_list(storage))
    w.json(os.path.join(forge_items, "storage_blocks.json"), tag_list(storage))

    ingots = [rid(i) for i in R.items if i.endswith(("_ingot", "_refined"))]
    gems = [rid(i) for i in R.items
            if i.endswith(("_gem", "_shard", "_crystal", "_chunk", "_polish"))]
    w.json(os.path.join(forge_items, "ingots.json"), tag_list(ingots))
    w.json(os.path.join(forge_items, "gems.json"), tag_list(gems))

    # --- entity type tags for spawn control ------------------------------
    monsters = [rid(m.id) for m in MOBS.ALL_MOBS if m.hostile]
    creatures = [rid(m.id) for m in MOBS.ALL_MOBS if not m.hostile]
    ent_dir = os.path.join(RES, "data", "minecraft", "tags", "entity_types")
    w.json(os.path.join(ent_dir, "skeletons.json"), tag_list([]))
    w.json(os.path.join(ent_dir, "powder_snow_walkable_mobs.json"), tag_list([]))
    w.json(dpath("tags", "entity_types", "hostile.json"), tag_list(monsters))
    w.json(dpath("tags", "entity_types", "passive.json"), tag_list(creatures))
    w.json(dpath("tags", "entity_types", "bosses.json"),
           tag_list([rid(b.id) for b in BOSSES.ALL_BOSSES]))


def _default_tier(block: str, kind: str) -> int:
    """Mining tier for non-ore blocks, derived from the block family."""
    if kind == REG.BlockKind.MINERAL_BLOCK:
        return 3
    if block.endswith("_planks") or kind == REG.BlockKind.LOG:
        return 0
    if kind == REG.BlockKind.GRASS:
        return 0
    return 1


# --------------------------------------------------------------------------- #
#  Lang
# --------------------------------------------------------------------------- #

def titleize(ident: str) -> str:
    return " ".join(p.capitalize() for p in ident.replace(":", "_").split("_"))


def emit_lang(w: Writer) -> None:
    lang: Dict[str, str] = {}

    lang[f"itemGroup.{MODID}"] = "Biomes Unseen"
    lang[f"itemGroup.{MODID}.blocks"] = "Biomes Unseen: Blocks"
    lang[f"itemGroup.{MODID}.gear"] = "Biomes Unseen: Gear"
    lang[f"itemGroup.{MODID}.nature"] = "Biomes Unseen: Nature"

    for block in R.blocks:
        name = None
        ore = ORE_BY_BLOCK.get(block)
        if ore:
            if block == ore.ore_block:
                name = ore.name
            elif block == ore.deepslate_ore_block:
                name = f"Deepslate {ore.name}"
            elif block == ore.mineral_block:
                name = f"Block of {ore.base_name.replace('_', ' ').title()}"
        if name is None:
            for biome in BIOMES.ALL_BIOMES:
                pass
        lang[f"block.{MODID}.{block}"] = name or titleize(block)

    for item in R.items:
        if item.endswith("_spawn_egg"):
            ent = item[: -len("_spawn_egg")]
            mob = MOB_BY_ID.get(ent) or BOSS_BY_ID.get(ent)
            base = mob.name if mob else titleize(ent)
            lang[f"item.{MODID}.{item}"] = f"{base} Spawn Egg"
            continue
        if item in R.block_set:
            continue  # block items inherit the block translation key
        lang[f"item.{MODID}.{item}"] = _item_name(item)

    for biome in BIOMES.ALL_BIOMES:
        lang[f"biome.{MODID}.{biome.id}"] = biome.name

    for mob in MOBS.ALL_MOBS:
        lang[f"entity.{MODID}.{mob.id}"] = mob.name

    for boss in BOSSES.ALL_BOSSES:
        lang[f"entity.{MODID}.{boss.id}"] = boss.name
        lang[f"{MODID}.boss.{boss.id}.music"] = boss.name
        for phase in boss.phases:
            lang[f"{MODID}.boss.{boss.id}.phase.{phase.index}"] = phase.name
            lang[f"{MODID}.boss.{boss.id}.phase.{phase.index}.desc"] = phase.description

    for struct in STRUCTS.ALL_STRUCTURES:
        lang[f"structure.{MODID}.{struct.id}"] = struct.name

    for ts in GEAR.TOOL_SETS:
        lang[f"{MODID}.gear.{ts.id}.lore"] = ts.lore
    for aset in GEAR.ARMOR_SETS:
        lang[f"{MODID}.armor.{aset.id}.bonus"] = titleize(aset.set_bonus)
        lang[f"{MODID}.armor.{aset.id}.lore"] = aset.lore

    # Biome and structure lore, surfaced through the lore books.
    for biome in BIOMES.ALL_BIOMES:
        if biome.lore:
            lang[f"{MODID}.lore.biome.{biome.id}"] = biome.lore
    for struct in STRUCTS.ALL_STRUCTURES:
        if struct.lore:
            lang[f"{MODID}.lore.structure.{struct.id}"] = struct.lore
    for mob in MOBS.ALL_MOBS:
        if mob.lore:
            lang[f"{MODID}.lore.mob.{mob.id}"] = mob.lore

    lang[f"{MODID}.subtitle.music.hollow_deep"] = "Hollow Deep ambience"
    for boss in BOSSES.ALL_BOSSES:
        lang[f"{MODID}.subtitle.music.{boss.id}"] = f"{boss.name} theme"
    lang[f"{MODID}.message.portal.unlit"] = "The frame sleeps. Strike it with an igniter."
    lang[f"{MODID}.message.boss.summon"] = "Something ancient notices you."

    w.json(bpath("lang", "en_us.json"), lang)


def _item_name(item: str) -> str:
    for ts in GEAR.TOOL_SETS:
        if item.startswith(f"{ts.id}_"):
            piece = item[len(ts.id) + 1:]
            return f"{ts.name} {titleize(piece)}"
    for aset in GEAR.ARMOR_SETS:
        if item.startswith(f"{aset.id}_"):
            piece = item[len(aset.id) + 1:]
            return f"{aset.name} {titleize(piece)}"
    for boss_id, weapon in GEAR.ARTEFACT_WEAPONS.items():
        if item == weapon:
            boss = BOSS_BY_ID.get(boss_id)
            return f"{boss.name if boss else titleize(boss_id)} Artefact"
    if item.startswith("lore_book"):
        return f"Lore Book ({titleize(item[len('lore_book'):].strip('_'))})"
    return titleize(item)


# --------------------------------------------------------------------------- #
#  pack.mcmeta + mods.toml
# --------------------------------------------------------------------------- #

def emit_meta(w: Writer) -> None:
    w.json(os.path.join(RES, "pack.mcmeta"), {
        "pack": {
            "description": "Biomes Unseen resources",
            "pack_format": PACK_FORMAT,
        }
    })

    mods_toml = f'''modLoader = "javafml"
loaderVersion = "[47,)"
license = "All Rights Reserved"
issueTrackerURL = "https://github.com/entitybrian69-bit/Biomes-Unseen/issues"

[[mods]]
modId = "{MODID}"
version = "${{file.jarVersion}}"
displayName = "Biomes Unseen"
updateJSONURL = "https://raw.githubusercontent.com/entitybrian69-bit/Biomes-Unseen/main/update.json"
displayURL = "https://github.com/entitybrian69-bit/Biomes-Unseen"
logoFile = "logo.png"
credits = "Built as a total-conversion worldgen expansion."
authors = "Biomes Unseen Team"
description = \'\'\'
Biomes Unseen is a total-conversion exploration mod: 140 hand-authored biomes
across five Overworld categories, three new dimensions, 44 ores with real uses,
ten gear families with set bonuses, 80 creatures, 34 jigsaw structures and five
multi-phase bosses.

Every texture is hand-authored pixel art. Every creature is a fully articulated
GeckoLib model. Every hostile has real targeting and melee AI.
\'\'\'

[[dependencies.{MODID}]]
    modId = "forge"
    mandatory = true
    versionRange = "[{FORGE_VERSION},)"
    ordering = "NONE"
    side = "BOTH"

[[dependencies.{MODID}]]
    modId = "minecraft"
    mandatory = true
    versionRange = "[{MC_VERSION},1.21)"
    ordering = "NONE"
    side = "BOTH"

[[dependencies.{MODID}]]
    modId = "geckolib"
    mandatory = true
    versionRange = "[4.4.7,)"
    ordering = "AFTER"
    side = "BOTH"
'''
    w.text(os.path.join(RES, "META-INF", "mods.toml"), mods_toml)


# --------------------------------------------------------------------------- #

def emit_all(w: Writer) -> None:
    # --- blockstates + block models --------------------------------------
    for block in R.blocks:
        w.json(bpath("blockstates", f"{block}.json"), blockstate(block))
        model = block_model(block)
        if model is not None:
            w.json(bpath("models", "block", f"{block}.json"), model)

    # --- item models ------------------------------------------------------
    for item in R.items:
        w.json(bpath("models", "item", f"{item}.json"), item_model(item))
    # Every solid block gets a BlockItem, so it needs an item model too even
    # though no separate item texture exists: the model parents the block model.
    # Skipping these would leave 263 blocks rendering as missing-model cubes in
    # the inventory and the creative tab.
    for block in R.block_items:
        if block in R.item_set:
            continue
        w.json(bpath("models", "item", f"{block}.json"), item_model(block))
    # Bow pull states are referenced by overrides, so they need models too.
    for states in R.bow_states.values():
        for state in states:
            w.json(bpath("models", "item", f"{state}.json"), item_model(state))

    # --- loot tables ------------------------------------------------------
    for block in R.blocks:
        w.json(dpath("loot_tables", "blocks", f"{block}.json"), block_loot(block))
    for mob in MOBS.ALL_MOBS:
        w.json(dpath("loot_tables", "entities", f"{mob.id}.json"), entity_loot(mob))
    for boss in BOSSES.ALL_BOSSES:
        w.json(dpath("loot_tables", "entities", f"{boss.id}.json"), boss_loot(boss))
    for struct in STRUCTS.ALL_STRUCTURES:
        w.json(dpath("loot_tables", "chests", f"{struct.id}.json"), chest_loot(struct))

    emit_referenced_chests(w)
    emit_recipes(w)
    emit_tags(w)
    emit_lang(w)
    emit_meta(w)


def main(argv: Optional[List[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    check = "--check" in argv
    w = Writer(check_only=check)
    if R.problems:
        print("registry has unresolved problems; fix those first:")
        for p in R.problems[:40]:
            print("   ! " + p)
        return 1
    emit_all(w)
    print(f"[res] emitted {len(w.written)} resource files"
          + (" (check only)" if check else ""))
    if not check and w.changed:
        print(f"[res] wrote/updated {len(w.changed)} files")
        for c in w.changed[:12]:
            print("      + " + c)
        if len(w.changed) > 12:
            print(f"      ... and {len(w.changed) - 12} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
