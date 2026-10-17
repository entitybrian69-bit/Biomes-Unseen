# -*- coding: utf-8 -*-
"""Emits datapack data trees per API style: biomes, features, structures,
loot, recipes, tags, advancements, spawn data, structure NBTs and the
overworld multi-noise parameter list."""

import json
import os

from content import (BIOME_ROWS, BIOME_GROUPS, ORE_ROWS, DECOR_ROWS, PLANT_ROWS,
                     MOB_ROWS, BOSS_ROWS, STRUCTURE_ROWS, ADVANCEMENT_ROWS)
from lines import LINES, MC_TO_LINE
import nbt


def _stable_salt(sid):
    """Deterministic structure-set salt.

    Python's hash() is salted per process, so using it here rewrote every
    structure_set JSON on each run.  A stable digest keeps the generated tree
    byte-identical between builds.
    """
    import hashlib
    digest = hashlib.sha256(("biomesunseen:" + sid).encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % 100000


def _w(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text if text.endswith("\n") else text + "\n")


def _wj(root, rel, obj):
    _w(root, rel, json.dumps(obj, indent=2))


# ---------------------------------------------------------------------------
# Style key: (features, structures, dirs, biome_json)
# ---------------------------------------------------------------------------

def style_key(F):
    return (F["features"], F["structures"], F["data_dirs"], F["biome_json"])


STYLE_DIRS = {
    ("legacy", "legacy", "plural", "old"): "data-legacy",
    ("placed", "legacy", "plural", "old"): "data-1181",
    ("placed", "sets", "plural", "old"): "data-noise-old",
    ("placed", "sets", "plural", "new"): "data-noise-new",
    ("placed", "sets", "flat", "new"): "data-1.21",
    ("placed", "sets", "flat", "list"): "data-1.21.2",
    ("placed", "sets", "flat", "attrs"): "data-26",
}

_HAS_DEEP_DARK = True

ANIMATED_BLOCKS = ("crystal_shard_block", "glowcap_block", "nullglass")

class _Ore(object):
    def __init__(self, t):
        (self.id, self.display, self.color, self.particleColor, self.minY,
         self.maxY, self.veinSize, self.veinsPerChunk, self.rarity,
         self.biomeGroup, self.stoneTag, self.glows, self.tool,
         self.potionEffect, self.machineTier) = t


ORES = [_Ore(t) for t in ORE_ROWS]




def _palette_for(group):
    base = {
        "crystal": ["biomesunseen:crystal_shard_block", "biomesunseen:nullglass",
                    "minecraft:quartz_block", "minecraft:amethyst_block"],
        "ember": ["biomesunseen:ember_rock", "biomesunseen:sunstone_bricks",
                  "minecraft:blackstone", "minecraft:magma_block"],
        "verdant": ["biomesunseen:living_heartwood", "biomesunseen:verdant_soils",
                    "minecraft:mossy_cobblestone", "minecraft:dark_oak_planks"],
        "frost": ["biomesunseen:frostbloom_ice", "minecraft:packed_ice",
                  "minecraft:blue_ice", "minecraft:quartz_block"],
        "storm": ["biomesunseen:storm_shale", "biomesunseen:skystone_bricks",
                  "minecraft:stone_bricks", "minecraft:lightning_rod"],
        "mire": ["biomesunseen:mire_muck", "minecraft:mud_bricks",
                 "minecraft:mossy_stone_bricks", "minecraft:dark_oak_planks"],
        "sky": ["biomesunseen:skystone_bricks", "minecraft:cut_copper",
                "minecraft:quartz_pillar", "minecraft:glass"],
        "void": ["biomesunseen:void_veined_stone", "biomesunseen:nullglass",
                 "minecraft:deepslate_bricks", "minecraft:crying_obsidian"],
    }
    return base[group]


def emit_structure_nbt(root):
    """Shared structure templates (same .nbt works on every line)."""
    for row in STRUCTURE_ROWS:
        (sid, display, group, category, spacing, sep, rarity, maxd, hasboss,
         bossid, pool, bg, tier, lore) = row
        palette = _palette_for(group)
        if category == "boss_arena":
            size, npal, blocks = nbt.build_room(9, 7, 9, 0, 1, 2, 3)
        elif category == "tower":
            size, npal, blocks = nbt.build_room(5, 8, 5, 0, 1, 2, 3)
        elif category in ("fortress", "palace", "pyramid"):
            size, npal, blocks = nbt.build_room(7, 5, 7, 0, 1, 2, 3)
        else:
            size, npal, blocks = nbt.build_room(5, 4, 5, 0, 1, 2, 3)
        for nbt_dir in ("structures", "structure"):
            path = os.path.join(root, "common/src/main/resources/data/biomesunseen",
                                nbt_dir, sid, "start.nbt")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            nbt.write_structure_nbt(path, size, palette[:npal], blocks)


def _spawn_attrs(entries):
    out = []
    for e in entries:
        out.append({
            "type": e["type"],
            "weight": e["weight"],
            "count": {"type": "minecraft:uniform",
                      "min_inclusive": e["minCount"],
                      "max_inclusive": e["maxCount"]},
        })
    return out


def _biome_json(def_row, style, feature_ids, monster_spawns, creature_spawns):
    (bid, display, group, depth, scale, temp, downfall, rarity, weather) = def_row
    g = BIOME_GROUPS[group]
    water_fog = (g["water"] >> 1) & 0x7F7F7F
    effects = {
        "grass_color": g["grass"],
        "foliage_color": g["foliage"],
        "water_color": g["water"],
        "water_fog_color": water_fog,
        "sky_color": g["sky"],
        "fog_color": g["fog"],
        "mood_sound": {
            "sound": "biomesunseen:" + g["ambient"],
            "tick_delay": 400,
            "block_search_extent": 8,
            "offset": 2.0,
        },
    }
    if weather == "snow":
        precipitation = "snow"
    elif weather in ("rain", "thunder"):
        precipitation = "rain"
    else:
        precipitation = "none"
    biome = {}
    if style in ("old", "new"):
        # depth/scale/category left the codec in 1.18/1.19; on those versions
        # the extra keys are ignored, on 1.16/1.17 they are required.
        biome["category"] = g["category"]
        biome["depth"] = depth
        biome["scale"] = scale
    biome["temperature"] = temp
    biome["downfall"] = downfall
    if style == "old":
        biome["precipitation"] = precipitation
        biome["surface_builder"] = "minecraft:default"
    elif style == "new":
        # 1.19.3 still decodes "precipitation"; 1.19.4 (23w03a) renamed it to
        # "has_precipitation". Unknown keys are ignored, so ship both.
        biome["precipitation"] = precipitation
        biome["has_precipitation"] = precipitation != "none"
    else:
        biome["has_precipitation"] = precipitation != "none"
    biome["effects"] = effects
    if style in ("old", "new"):
        # carver-type map form until 1.21.2 (24w33a) replaced it with a list
        biome["carvers"] = {"air": []}
    else:
        biome["carvers"] = []
    # 10 generation steps on 1.16/1.17, 11 once FLUID_SPRINGS exists; list
    # length is lenient and index 6 is UNDERGROUND_ORES in both layouts.
    steps = [[] for _ in range(10 if style == "old" else 11)]
    steps[6] = feature_ids
    biome["features"] = steps
    if style == "attrs":
        # 26.x moved mob spawns and sky colour into biome attributes.
        def hexcol(c):
            return "#%06x" % (c & 0xFFFFFF)
        biome["attributes"] = {
            "minecraft:gameplay/natural_mob_spawns": {
                "argument": {
                    "spawn_costs": {},
                    "spawns_by_category": {
                        "monster": _spawn_attrs(monster_spawns),
                        "creature": _spawn_attrs(creature_spawns),
                    },
                },
            },
            "minecraft:visual/sky_color": hexcol(g["sky"]),
        }
    else:
        # only category keys that exist on every target of the style: unknown
        # MobCategory keys fail the spawners map codec outright.
        biome["spawners"] = {
            "monster": monster_spawns,
            "creature": creature_spawns,
            "ambient": [],
            "water_creature": [],
            "water_ambient": [],
            "misc": [],
        }
        biome["spawn_costs"] = {}
    return biome


def _ore_feature_legacy(ore):
    return {
        "type": "minecraft:ore",
        "config": {
            "size": ore.veinSize,
            "discard_chance_on_air_exposure": 0.0,
            "targets": [
                {"target": {"predicate_type": "minecraft:tag_match",
                            "tag": "minecraft:stone_ore_replaceables"},
                 "state": {"Name": "biomesunseen:%s_ore" % ore.id}},
                {"target": {"predicate_type": "minecraft:tag_match",
                            "tag": "minecraft:deepslate_ore_replaceables"},
                 "state": {"Name": "biomesunseen:%s_ore" % ore.id}},
            ],
        },
    }


def _ore_placed(ore):
    return {
        "feature": "biomesunseen:%s_ore" % ore.id,
        "placement": [
            {"type": "minecraft:count", "count": ore.veinsPerChunk},
            {"type": "minecraft:in_square"},
            {"type": "minecraft:height_range",
             "height": {"type": "minecraft:uniform",
                        "min_inclusive": {"absolute": ore.minY},
                        "max_inclusive": {"absolute": ore.maxY}}},
            {"type": "minecraft:biome"},
        ],
    }


def _legacy_configured_structure(def_row):
    (sid, display, group, category, spacing, sep, rarity, maxd, hasboss,
     bossid, pool, bg, tier, lore) = def_row
    # jigsaw codec: max_distance_from_center is intRange(1, 128)
    maxd = max(1, min(128, maxd))
    biome_keys = []
    for brow in BIOME_ROWS:
        if brow[2] in bg:
            biome_keys.append("biomesunseen:" + brow[0])
    return {
        "type": "minecraft:jigsaw",
        "config": {
            "start_pool": "biomesunseen:%s" % pool,
            "size": 3 if category != "boss_arena" else 5,
            "start_height": {"absolute": 0},
            "project_start_to_heightmap": "WORLD_SURFACE_WG",
            "max_distance_from_center": maxd,
            "use_expansion_hack": False,
        },
        "biomes": biome_keys,
        "adapt_noise": False,
        "spawn_overrides": {},
    }


def _modern_structure(def_row):
    (sid, display, group, category, spacing, sep, rarity, maxd, hasboss,
     bossid, pool, bg, tier, lore) = def_row
    # jigsaw codec: max_distance_from_center is intRange(1, 128)
    maxd = max(1, min(128, maxd))
    biome_keys = []
    for brow in BIOME_ROWS:
        if brow[2] in bg:
            biome_keys.append("biomesunseen:" + brow[0])
    # Flat jigsaw shape (fields sit next to "type"), valid 1.18.2 through 26.x.
    return {
        "type": "minecraft:jigsaw",
        "biomes": biome_keys,
        "step": "surface_structures",
        "spawn_overrides": {},
        "terrain_adaptation": "none",
        "start_pool": "biomesunseen:%s" % pool,
        "size": 3 if category != "boss_arena" else 5,
        "start_height": {"absolute": 0},
        "project_start_to_heightmap": "WORLD_SURFACE_WG",
        "max_distance_from_center": maxd,
        "use_expansion_hack": True,
    }


def _template_pool(sid):
    return {
        "fallback": "minecraft:empty",
        "elements": [
            {
                "weight": 1,
                "element": {
                    "element_type": "minecraft:legacy_single_pool_element",
                    "location": "biomesunseen:%s/start" % sid,
                    "projection": "rigid",
                    "processors": "minecraft:empty",
                },
            }
        ],
    }


def _overworld_parameter_list():
    """Complete overworld multi-noise parameter list: vanilla climates plus
    every Biomes Unseen biome in its own temperature/humidity band."""
    entries = []

    def clamp(v):
        # Climate.Parameter codec = intervalCodec(floatRange(-2, 2)): values
        # outside [-2.0, 2.0] fail world_preset/dimension decoding and abort
        # world creation ("Missing overworld dimension").
        return max(-2.0, min(2.0, float(v)))

    def entry(biome, t, h, c, w, d, e):
        return {
            "biome": biome,
            "parameters": {
                "temperature": clamp(t), "humidity": clamp(h),
                "continentalness": clamp(c), "erosion": clamp(w),
                "depth": clamp(d), "weirdness": clamp(e),
                "offset": 0.0,
            },
        }

    # A compact but complete vanilla set (all overworld vanilla biomes).
    vanilla = [
        ("minecraft:plains", 0, 0, 0), ("minecraft:sunflower_plains", 0, 0, 0.1),
        ("minecraft:desert", 2, -1, 0), ("minecraft:swamp", 0, 1, 0),
        ("minecraft:forest", 0, 0, -0.1), ("minecraft:flower_forest", 0, 0, 0.2),
        ("minecraft:birch_forest", 0, 0, -0.2), ("minecraft:dark_forest", -0.1, 0, -0.2),
        ("minecraft:old_growth_birch_forest", 0, 0, -0.3),
        ("minecraft:old_growth_pine_taiga", -0.4, 0, -0.2),
        ("minecraft:old_growth_spruce_taiga", -0.5, 0, -0.1),
        ("minecraft:taiga", -0.5, 0, 0), ("minecraft:snowy_taiga", -1, 0, 0),
        ("minecraft:savanna", 1.2, -0.5, 0), ("minecraft:savanna_plateau", 1.2, -0.5, 0.4),
        ("minecraft:windswept_hills", 0, 0, 0.5), ("minecraft:windswept_gravelly_hills", 0, 0, 0.7),
        ("minecraft:windswept_forest", 0, 0, 0.3), ("minecraft:windswept_savanna", 1.2, -0.5, 0.6),
        ("minecraft:jungle", 0.9, 0.8, -0.2), ("minecraft:sparse_jungle", 0.9, 0.5, -0.1),
        ("minecraft:bamboo_jungle", 0.9, 0.9, -0.3),
        ("minecraft:badlands", 2, -1, 0.2), ("minecraft:eroded_badlands", 2, -1, 0.5),
        ("minecraft:wooded_badlands", 2, -1, 0.1),
        ("minecraft:meadow", 0.2, 0, 0.6), ("minecraft:grove", -0.4, 0, 0.7),
        ("minecraft:snowy_slopes", -0.9, 0, 0.8), ("minecraft:jagged_peaks", -0.9, 0, 1),
        ("minecraft:frozen_peaks", -1, 0, 1), ("minecraft:stony_peaks", 0.8, 0, 1),
        ("minecraft:river", 0, 0, -0.6), ("minecraft:frozen_river", -1, 0, -0.6),
        ("minecraft:beach", 0, 0, -0.9), ("minecraft:snowy_beach", -1, 0, -0.9),
        ("minecraft:stony_shore", 0, 0, -0.9),
        ("minecraft:ocean", 0, 0, -1), ("minecraft:deep_ocean", 0, 0, -1.2),
        ("minecraft:warm_ocean", 1, 0, -1), ("minecraft:lukewarm_ocean", 0.6, 0, -1),
        ("minecraft:cold_ocean", -0.6, 0, -1), ("minecraft:frozen_ocean", -1, 0, -1),
        ("minecraft:deep_lukewarm_ocean", 0.6, 0, -1.2),
        ("minecraft:deep_cold_ocean", -0.6, 0, -1.2),
        ("minecraft:deep_frozen_ocean", -1, 0, -1.2),
        ("minecraft:mushroom_fields", 0, 1, -0.8),
        ("minecraft:lush_caves", 0, 0.6, -1.4), ("minecraft:dripstone_caves", 0, -0.4, -1.4),
        ("minecraft:deep_dark", -0.5, -0.5, -1.6),
    ]
    for biome, t, h, d in vanilla:
        if biome == "minecraft:deep_dark" and not _HAS_DEEP_DARK:
            continue
        entries.append(entry(biome, t, h, 0, 0, d, 0))

    # Biomes Unseen entries: each biome gets a distinct climate point derived
    # from its temperature/downfall with jitter from its id hash.
    for idx, (bid, display, group, depth, scale, temp, downfall, rarity, weather) in enumerate(BIOME_ROWS):
        t = round((temp - 0.7) * 1.6, 2)
        h = round((downfall - 0.5) * 1.8, 2)
        c = round(-0.1 + (idx % 7) * 0.05, 2)
        e = round(((idx * 37) % 11 - 5) / 10.0, 2)
        wd = round(((idx * 17) % 9 - 4) / 12.0, 2)
        dpt = round(depth / 3.0, 2)
        entries.append(entry("biomesunseen:" + bid, t, h, c, e, dpt, wd))

    return {"biomes": entries}


def _dimension_overworld(biomes):
    return {
        "type": "minecraft:overworld",
        "generator": {
            "type": "minecraft:noise",
            "settings": "minecraft:overworld",
            "biome_source": {"type": "minecraft:multi_noise", "biomes": biomes},
        },
    }


def _world_preset(biomes, settings):
    return {
        "dimensions": {
            "minecraft:overworld": {
                "type": "minecraft:overworld",
                "generator": {
                    "type": "minecraft:noise",
                    "biome_source": {"type": "minecraft:multi_noise",
                                     "biomes": biomes},
                    "settings": "minecraft:%s" % settings,
                },
            },
            "minecraft:the_end": {
                "type": "minecraft:the_end",
                "generator": {
                    "type": "minecraft:noise",
                    "biome_source": {"type": "minecraft:the_end"},
                    "settings": "minecraft:end",
                },
            },
            "minecraft:the_nether": {
                "type": "minecraft:the_nether",
                "generator": {
                    "type": "minecraft:noise",
                    "biome_source": {"type": "minecraft:multi_noise",
                                     "preset": "minecraft:nether"},
                    "settings": "minecraft:nether",
                },
            },
        },
    }


def emit_tree(root, style_name, style):
    """Emit one complete data tree."""
    features, structures, dirs, biome_json = style
    base = "common/src/%s/resources" % style_name
    ns = "data/biomesunseen"

    loot_dir = "loot_table" if dirs == "flat" else "loot_tables"
    recipe_dir = "recipe" if dirs == "flat" else "recipes"
    adv_dir = "advancement" if dirs == "flat" else "advancements"
    block_tag_dir = "tags/block" if dirs == "flat" else "tags/blocks"
    item_tag_dir = "tags/item" if dirs == "flat" else "tags/items"
    entity_tag_dir = "tags/entity_type" if dirs == "flat" else "tags/entity_types"

    # ---------------- worldgen features ----------------
    for ore in ORES:
        _wj(root, "%s/%s/worldgen/configured_feature/%s_ore.json"
            % (base, ns, ore.id), _ore_feature_legacy(ore))
        if features == "placed":
            _wj(root, "%s/%s/worldgen/placed_feature/%s_ore.json"
                % (base, ns, ore.id), _ore_placed(ore))

    # ---------------- biomes ----------------
    feature_names = ["biomesunseen:%s_ore" % o.id for o in ORES]
    for brow in BIOME_ROWS:
        (bid, display, group, depth, scale, temp, downfall, rarity, weather) = brow
        # features for this biome group
        feats = ["biomesunseen:%s_ore" % o.id for o in ORES
                 if o.biomeGroup is None or o.biomeGroup == group]
        if features == "placed":
            # placed-feature references
            pass
        monsters = []
        creatures = []
        for mrow in MOB_ROWS:
            (mid, mdisplay, cat, hp, spd, atk, defn, w, h, behaviors, tame, trade,
             pack, herd, flees, terrain, bg, weight, night, anims, color, glow) = mrow
            if group not in bg:
                continue
            entry = {"type": "biomesunseen:" + mid, "weight": weight,
                     "minCount": 1, "maxCount": 4 if pack else 2}
            if cat == "monster":
                monsters.append(entry)
            else:
                creatures.append(entry)
        bjson = _biome_json(brow, biome_json, feats, monsters, creatures)
        if biome_json == "old":
            # effects.mood_sound sound name: use our own event ids
            bjson["effects"]["mood_sound"]["sound"] = "biomesunseen:" + BIOME_GROUPS[group]["ambient"]
        _wj(root, "%s/%s/worldgen/biome/%s.json" % (base, ns, bid), bjson)

    # ---------------- structures ----------------
    if structures == "sets":
        for row in STRUCTURE_ROWS:
            (sid, display, group, category, spacing, sep, rarity, maxd, hasboss,
             bossid, pool, bg, tier, lore) = row
            _wj(root, "%s/%s/worldgen/structure/%s.json" % (base, ns, sid),
                _modern_structure(row))
            _wj(root, "%s/%s/worldgen/structure_set/%s.json" % (base, ns, sid),
                {
                    "structures": [{"structure": "biomesunseen:%s" % sid,
                                    "weight": max(1, int(round(rarity * 10)))}],
                    "placement": {
                        "type": "minecraft:random_spread",
                        "salt": _stable_salt(sid),
                        "spacing": spacing,
                        "separation": sep,
                        "spread_type": "linear",
                    },
                })
            _wj(root, "%s/%s/worldgen/template_pool/%s.json" % (base, ns, pool),
                _template_pool(sid))
    else:
        for row in STRUCTURE_ROWS:
            (sid, display, group, category, spacing, sep, rarity, maxd, hasboss,
             bossid, pool, bg, tier, lore) = row
            _wj(root, "%s/%s/worldgen/configured_structure_feature/%s.json"
                % (base, ns, sid), _legacy_configured_structure(row))
            _wj(root, "%s/%s/worldgen/template_pool/%s.json" % (base, ns, pool),
                _template_pool(sid))

    # ---------------- overworld biome injection ----------------
    # The old multi_noise_biome_source_parameter_list/overworld.json override
    # was invalid: that registry only accepts {"preset": ...} aliases and its
    # codec crashed world creation on the custom "biomes" list.  Instead we
    # replace the overworld dimension (Default world type) and the vanilla
    # world presets (when a preset is selected) with a multi-noise biome
    # source that includes every Biomes Unseen biome.
    if structures == "sets":
        global _HAS_DEEP_DARK
        _HAS_DEEP_DARK = biome_json != "old"
        biomes = _overworld_parameter_list()["biomes"]
        _wj(root, "%s/data/minecraft/dimension/overworld.json" % base,
            _dimension_overworld(biomes))
        for preset_id, settings in (("normal", "overworld"),
                                    ("amplified", "amplified"),
                                    ("large_biomes", "large_biomes")):
            _wj(root, "%s/data/minecraft/worldgen/world_preset/%s.json"
                % (base, preset_id), _world_preset(biomes, settings))

    # ---------------- loot tables ----------------
    for ore in ORES:
        _wj(root, "%s/%s/%s/blocks/%s_ore.json" % (base, ns, loot_dir, ore.id),
            {"type": "minecraft:block",
             "pools": [{"rolls": 1,
                        "entries": [{"type": "minecraft:item",
                                     "name": "biomesunseen:%s" % ore.id}],
                        "conditions": [{"condition": "minecraft:survives_explosion"}]}]})
    for did, display, color, sound, material in DECOR_ROWS:
        _wj(root, "%s/%s/%s/blocks/%s.json" % (base, ns, loot_dir, did),
            {"type": "minecraft:block",
             "pools": [{"rolls": 1,
                        "entries": [{"type": "minecraft:item",
                                     "name": "biomesunseen:%s" % did}],
                        "conditions": [{"condition": "minecraft:survives_explosion"}]}]})
    for pid, display, color, height, pottable, flower in PLANT_ROWS:
        _wj(root, "%s/%s/%s/blocks/%s.json" % (base, ns, loot_dir, pid),
            {"type": "minecraft:block",
             "pools": [{"rolls": 1,
                        "entries": [{"type": "minecraft:item",
                                     "name": "biomesunseen:%s" % pid}]}]})
    for mrow in MOB_ROWS:
        mid = mrow[0]
        _wj(root, "%s/%s/%s/entities/%s.json" % (base, ns, loot_dir, mid),
            {"type": "minecraft:entity",
             "pools": [{"rolls": 1,
                        "entries": [{"type": "minecraft:item",
                                     "name": "biomesunseen:%s_trophy" % mid,
                                     "functions": [{"function": "minecraft:set_count",
                                                    "count": {"type": "minecraft:uniform",
                                                              "min": 0, "max": 2}}]}]}]})
    for brow in BOSS_ROWS:
        bid = brow[0]
        _wj(root, "%s/%s/%s/entities/%s.json" % (base, ns, loot_dir, bid),
            {"type": "minecraft:entity",
             "pools": [
                 {"rolls": 1,
                  "entries": [{"type": "minecraft:item",
                               "name": "biomesunseen:unseen_sigil"}]},
                 {"rolls": {"type": "minecraft:uniform", "min": 3, "max": 6},
                  "entries": [{"type": "minecraft:item",
                               "name": "biomesunseen:%s" % brow[10].split("/")[-1]
                               if False else "biomesunseen:voidshard"}]},
                 {"rolls": 1,
                  "entries": [{"type": "minecraft:item",
                               "name": "biomesunseen:%s_trophy" % ("brambleback" if bid == "heart_of_the_forest" else "star_whale")}]}
             ]})

    # ---------------- recipes ----------------
    for ore in ORES:
        _wj(root, "%s/%s/%s/%s_from_smelting.json" % (base, ns, recipe_dir, ore.id),
            {"type": "minecraft:smelting",
             "ingredient": {"item": "biomesunseen:%s_ore" % ore.id},
             "result": "biomesunseen:%s" % ore.id,
             "experience": 0.7, "cookingtime": 200})
        _wj(root, "%s/%s/%s/%s_from_blasting.json" % (base, ns, recipe_dir, ore.id),
            {"type": "minecraft:blasting",
             "ingredient": {"item": "biomesunseen:%s_ore" % ore.id},
             "result": "biomesunseen:%s" % ore.id,
             "experience": 0.7, "cookingtime": 100})
        _wj(root, "%s/%s/%s/%s_pickaxe.json" % (base, ns, recipe_dir, ore.id),
            {"type": "minecraft:crafting_shaped",
             "pattern": ["MMM", " S ", " S "],
             "key": {"M": {"item": "biomesunseen:%s" % ore.id},
                     "S": {"item": "minecraft:stick"}},
             "result": {"item": "biomesunseen:%s_pickaxe" % ore.id}})
        _wj(root, "%s/%s/%s/%s_sword.json" % (base, ns, recipe_dir, ore.id),
            {"type": "minecraft:crafting_shaped",
             "pattern": ["M", "M", "S"],
             "key": {"M": {"item": "biomesunseen:%s" % ore.id},
                     "S": {"item": "minecraft:stick"}},
             "result": {"item": "biomesunseen:%s_sword" % ore.id}})
        _wj(root, "%s/%s/%s/%s_tonic.json" % (base, ns, recipe_dir, ore.id),
            {"type": "minecraft:crafting_shapeless",
             "ingredients": [{"item": "biomesunseen:%s" % ore.id},
                             {"item": "minecraft:glass_bottle"}],
             "result": {"item": "biomesunseen:%s_tonic" % ore.id}})
    for tier in range(1, 5):
        ore = ORES[min(len(ORES) - 1, tier * 4)]
        _wj(root, "%s/%s/%s/machine_core_t%d.json" % (base, ns, recipe_dir, tier),
            {"type": "minecraft:crafting_shaped",
             "pattern": ["MMM", "MCM", "MMM"],
             "key": {"M": {"item": "biomesunseen:%s" % ore.id},
                     "C": {"item": "minecraft:redstone"}},
             "result": {"item": "biomesunseen:machine_core_t%d" % tier}})

    # ---------------- tags ----------------
    ore_ores = ["biomesunseen:%s_ore" % o.id for o in ORES]
    _wj(root, "%s/%s/%s/ores.json" % (base, "data/c", block_tag_dir),
        {"replace": False, "values": ore_ores})
    _wj(root, "%s/%s/%s/ores.json" % (base, "data/c", item_tag_dir),
        {"replace": False, "values": ore_ores})
    _wj(root, "%s/%s/%s/ores.json" % (base, ns, block_tag_dir),
        {"replace": False, "values": ore_ores})
    _wj(root, "%s/%s/%s/ores.json" % (base, ns, item_tag_dir),
        {"replace": False, "values": ["biomesunseen:%s" % o.id for o in ORES]})
    _wj(root, "%s/%s/%s/plants.json" % (base, ns, block_tag_dir),
        {"replace": False, "values": ["biomesunseen:%s" % p[0] for p in PLANT_ROWS]})
    _wj(root, "%s/%s/%s/terrain.json" % (base, ns, block_tag_dir),
        {"replace": False, "values": ["biomesunseen:%s" % d[0] for d in DECOR_ROWS]})
    _wj(root, "%s/%s/%s/mobs.json" % (base, ns, entity_tag_dir),
        {"replace": False, "values": ["biomesunseen:%s" % m[0] for m in MOB_ROWS]})
    _wj(root, "%s/%s/%s/bosses.json" % (base, ns, entity_tag_dir),
        {"replace": False, "values": ["biomesunseen:%s" % b[0] for b in BOSS_ROWS]})
    _wj(root, "%s/%s/%s/tameable.json" % (base, ns, entity_tag_dir),
        {"replace": False, "values": ["biomesunseen:%s" % m[0] for m in MOB_ROWS if m[10]]})
    _wj(root, "%s/%s/%s/pack_mobs.json" % (base, ns, entity_tag_dir),
        {"replace": False, "values": ["biomesunseen:%s" % m[0] for m in MOB_ROWS if m[12]]})
    _wj(root, "%s/%s/%s/stones.json" % (base, "data/c", block_tag_dir),
        {"replace": False, "values": ["biomesunseen:%s" % d[0] for d in DECOR_ROWS
                                      if d[4] == "stone"]})
    _wj(root, "%s/%s/%s/woods.json" % (base, "data/c", block_tag_dir),
        {"replace": False, "values": ["biomesunseen:living_heartwood"]})

    # ---------------- advancements ----------------
    adv_map = {a[0]: a for a in ADVANCEMENT_ROWS}
    for aid, title, desc, parent in ADVANCEMENT_ROWS:
        doc = {}
        if parent:
            doc["parent"] = "biomesunseen:%s" % parent
        display = {
            "icon": {"item": "biomesunseen:unseen_sigil"},
            "title": title,
            "description": desc,
        }
        if aid == "root":
            display["background"] = "minecraft:textures/block/deepslate_tiles.png"
        if aid in ("heart_of_the_forest", "void_serpent", "boss_hunter"):
            display["frame"] = "challenge"
        doc["display"] = display
        if aid == "root":
            doc["criteria"] = {"entered": {"trigger": "minecraft:location"}}
        elif aid == "heart_of_the_forest":
            doc["criteria"] = {"killed": {"trigger": "minecraft:player_killed_entity",
                                          "conditions": {"entity": {"type": "biomesunseen:heart_of_the_forest"}}}}
        elif aid == "void_serpent":
            doc["criteria"] = {"killed": {"trigger": "minecraft:player_killed_entity",
                                          "conditions": {"entity": {"type": "biomesunseen:void_serpent"}}}}
        else:
            doc["criteria"] = {"tick": {"trigger": "minecraft:tick"}}
        _wj(root, "%s/%s/%s/%s.json" % (base, ns, adv_dir, aid), doc)

    # ---------------- spawn data (extra biome spawn overrides) ----------------
    spawn_doc = {"mobs": []}
    for mrow in MOB_ROWS:
        spawn_doc["mobs"].append({
            "id": "biomesunseen:%s" % mrow[0],
            "weight": mrow[17],
            "categories": [mrow[2]],
            "groups": list(mrow[16]),
        })
    _wj(root, "%s/%s/spawn_data.json" % (base, ns), spawn_doc)


def emit(root):
    emit_structure_nbt(root)
    emitted = set()
    for line_key, F in LINES.items():
        sk = style_key(F)
        style_name = STYLE_DIRS[sk]
        if style_name in emitted:
            continue
        emitted.add(style_name)
        emit_tree(root, style_name, sk)

    # Loader metadata support files shared by all lines
    # (advancement/function naming differences are handled above).
    _w(root, "common/src/main/resources/pack.mcmeta", json.dumps({
        "pack": {
            "pack_format": 15,
            "description": "Biomes Unseen - shared resources",
        }
    }, indent=2))
