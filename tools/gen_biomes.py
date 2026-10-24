#!/usr/bin/env python3
"""Generates all biome data from tools/spec/biomes.py (standard library only).

Hollow Deep (60 biomes): biome JSON, dimension/hollow_deep.json (multi-noise cells),
  worldgen/noise_settings/hollow_deep.json (terrain + one surface rule per theme),
  tags hollow_deep + has_structure/heart_arena, one add_spawns biome modifier per theme.
Overworld (80 biomes): biome JSON, tag overworld_biomes, specs/overworld.json
  (read by the TerraBlender region and surface rules in Java).
Run this before tools/gen_ores.py. Usage: python tools/gen_biomes.py
"""
import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from jsonfmt import write  # noqa: E402
from spec.biomes import DIM_BIOMES, OW_BIOMES, OW_GROUPS, THEMES, VARIANTS, VEG  # noqa: E402
from spec.mobs import MOBS  # noqa: E402

ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "src", "main", "resources", "data", "biomesunseen")
NS = "biomesunseen:"
SPAWN_BY_ARCH = {"blob": (40, 2, 4), "crawler": (35, 1, 3), "quad": (30, 1, 3), "biped": (30, 1, 2),
                 "floater": (20, 1, 2), "serpent": (25, 1, 2), "brute": (8, 1, 1)}
CATEGORIES = ["monster", "creature", "ambient", "axolotls", "underground_water_creature",
              "water_creature", "water_ambient", "misc"]
STANDARD_MONSTERS = [("spider", 100, 4, 4), ("zombie", 95, 4, 4), ("zombie_villager", 5, 1, 1),
                     ("skeleton", 100, 4, 4), ("creeper", 100, 4, 4), ("slime", 100, 4, 4),
                     ("enderman", 10, 1, 4), ("witch", 5, 1, 1)]
ORES_STEP = ["minecraft:ore_dirt", "minecraft:ore_gravel", "minecraft:ore_granite_upper", "minecraft:ore_granite_lower",
             "minecraft:ore_diorite_upper", "minecraft:ore_diorite_lower", "minecraft:ore_andesite_upper",
             "minecraft:ore_andesite_lower", "minecraft:ore_tuff", "minecraft:ore_coal_upper", "minecraft:ore_coal_lower",
             "minecraft:ore_iron_upper", "minecraft:ore_iron_middle", "minecraft:ore_iron_small", "minecraft:ore_gold",
             "minecraft:ore_gold_lower", "minecraft:ore_redstone", "minecraft:ore_redstone_lower", "minecraft:ore_diamond",
             "minecraft:ore_diamond_large", "minecraft:ore_diamond_buried", "minecraft:ore_lapis",
             "minecraft:ore_lapis_buried", "minecraft:ore_copper"]


def shade(color, k):
    r, g, b = (min(255, int(((color >> s) & 255) * k)) for s in (16, 8, 0))
    return (r << 16) | (g << 8) | b


def title(bid):
    small = {"of", "the"}
    return " ".join(w if w in small else w.capitalize() for w in bid.split("_"))


def features(base, extra):
    steps = [[] for _ in range(11)]
    for source in (base, extra):
        for step, ids in source.items():
            for fid in ids:
                if fid not in steps[step]:
                    steps[step].append(fid)
    return steps


def spawner(entry):
    name, weight, lo, hi = entry
    return {"type": name if ":" in name else "minecraft:" + name, "weight": weight, "minCount": lo, "maxCount": hi}


def biome_json(temp, down, precip, effects, feats, spawners, carvers):
    return {"has_precipitation": precip, "temperature": round(temp, 2), "downfall": down, "effects": effects,
            "carvers": carvers, "features": feats, "spawners": spawners, "spawn_costs": {}}


# ----------------------------------------------------------------- Hollow Deep
def dimension():
    cells = list(itertools.product(range(3), repeat=4))
    spans = [[-1.0, -0.2], [-0.2, 0.2], [0.2, 1.0]]
    entries, theme_biomes, n = [], {}, 0
    for theme, ids in DIM_BIOMES.items():
        fog, sky, water, wfog, grass, foliage, particle, _top, _under, temp, down, base = THEMES[theme]
        for i, bid in enumerate(ids):
            k, extra = VARIANTS[i]
            effects = {"sky_color": shade(sky, k), "fog_color": shade(fog, k), "water_color": shade(water, k),
                       "water_fog_color": shade(wfog, k), "grass_color": shade(grass, k),
                       "foliage_color": shade(foliage, k),
                       "particle": {"options": {"type": particle}, "probability": 0.004},
                       "mood_sound": {"sound": "minecraft:ambient.cave", "tick_delay": 6000,
                                      "block_search_extent": 8, "offset": 2.0}}
            spawners = {c: [] for c in CATEGORIES}
            write(os.path.join(DATA, "worldgen", "biome", bid + ".json"),
                  biome_json(temp + 0.04 * (i - 2), down, False, effects, features(base, extra), spawners, {}))
            t, h, e, w = cells[n]
            n += 1
            entries.append({"biome": NS + bid, "parameters": {
                "temperature": spans[t], "humidity": spans[h], "continentalness": [-1.0, 1.0],
                "erosion": spans[e], "depth": [-1.0, 1.0], "weirdness": spans[w], "offset": 0.0}})
            theme_biomes.setdefault(theme, []).append(NS + bid)
    write(os.path.join(DATA, "dimension", "hollow_deep.json"), {
        "type": "biomesunseen:hollow_deep",
        "generator": {"type": "minecraft:noise", "settings": "biomesunseen:hollow_deep",
                      "biome_source": {"type": "minecraft:multi_noise", "biomes": entries}}}, width=400)
    all_ids = [b for ids in theme_biomes.values() for b in ids]
    write(os.path.join(DATA, "specs", "dimension_biomes.json"),
          [{"id": b[len(NS):], "name": title(b[len(NS):])} for b in all_ids], width=400)
    write(os.path.join(DATA, "tags", "worldgen", "biome", "hollow_deep.json"), {"replace": False, "values": all_ids})
    write(os.path.join(DATA, "tags", "worldgen", "biome", "has_structure", "heart_arena.json"),
          {"replace": False, "values": theme_biomes["heartwood"]})
    return theme_biomes


def ycg(f, t, fv, tv):
    return {"type": "minecraft:y_clamped_gradient", "from_y": f, "to_y": t, "from_value": fv, "to_value": tv}


def shifted(noise):
    return {"type": "minecraft:shifted_noise", "noise": noise, "xz_scale": 2.0, "y_scale": 0,
            "shift_x": "minecraft:shift_x", "shift_y": 0, "shift_z": "minecraft:shift_z"}


def noise_settings(theme_biomes):
    profile = {"type": "minecraft:add", "argument1": ycg(4, 48, 3.0, -1.0), "argument2": ycg(140, 196, -1.0, 3.0)}
    bumps = {"type": "minecraft:mul", "argument1": 2.2,
             "argument2": {"type": "minecraft:noise", "noise": "minecraft:cave_cheese", "xz_scale": 1.0, "y_scale": 1.2}}
    final = {"type": "minecraft:squeeze", "argument": {"type": "minecraft:mul", "argument1": 0.64,
             "argument2": {"type": "minecraft:interpolated", "argument": {"type": "minecraft:blend_density",
             "argument": {"type": "minecraft:add", "argument1": profile, "argument2": bumps}}}}}
    block = lambda n: {"type": "minecraft:block", "result_state": {"Name": n}}
    depth = lambda add: {"type": "minecraft:stone_depth", "offset": 0, "surface_type": "floor",
                         "add_surface_depth": add, "secondary_depth_range": 0}
    rules = [
        {"type": "minecraft:condition", "if_true": {"type": "minecraft:vertical_gradient", "random_name": "minecraft:bedrock_floor",
         "true_at_and_below": {"above_bottom": 0}, "false_at_and_above": {"above_bottom": 5}},
         "then_run": block("minecraft:bedrock")},
        {"type": "minecraft:condition", "if_true": {"type": "minecraft:not", "invert": {"type": "minecraft:vertical_gradient",
         "random_name": "minecraft:bedrock_roof", "true_at_and_below": {"below_top": 5}, "false_at_and_above": {"below_top": 0}}},
         "then_run": block("minecraft:bedrock")},
    ]
    for theme, ids in theme_biomes.items():
        top, under = THEMES[theme][7], THEMES[theme][8]
        rules.append({"type": "minecraft:condition", "if_true": {"type": "minecraft:biome", "biome_is": ids},
                      "then_run": {"type": "minecraft:sequence", "sequence": [
                          {"type": "minecraft:condition", "if_true": depth(False), "then_run": block(top)},
                          {"type": "minecraft:condition", "if_true": depth(True), "then_run": block(under)}]}})
    write(os.path.join(DATA, "worldgen", "noise_settings", "hollow_deep.json"), {
        "sea_level": 0, "disable_mob_generation": False, "aquifers_enabled": False, "ore_veins_enabled": False,
        "legacy_random_source": False, "default_block": {"Name": "minecraft:deepslate"},
        "default_fluid": {"Name": "minecraft:water", "Properties": {"level": "0"}},
        "noise": {"min_y": 0, "height": 256, "size_horizontal": 1, "size_vertical": 2},
        "noise_router": {"barrier": 0, "fluid_level_floodedness": 0, "fluid_level_spread": 0, "lava": 0,
                         "temperature": shifted("minecraft:temperature"), "vegetation": shifted("minecraft:vegetation"),
                         "continents": 0, "erosion": shifted("minecraft:erosion"), "depth": 0,
                         "ridges": shifted("minecraft:ridge"), "initial_density_without_jaggedness": 0,
                         "final_density": final, "vein_toggle": 0, "vein_ridged": 0, "vein_gap": 0},
        "spawn_target": [], "surface_rule": {"type": "minecraft:sequence", "sequence": rules}}, width=260)


def spawn_modifiers(theme_biomes):
    for theme, ids in theme_biomes.items():
        spawners = []
        for row in MOBS:
            if row[13] == theme:
                weight, lo, hi = SPAWN_BY_ARCH[row[2]]
                spawners.append({"type": NS + row[0], "weight": weight, "minCount": lo, "maxCount": hi})
        write(os.path.join(DATA, "forge", "biome_modifier", "spawns_%s.json" % theme),
              {"type": "forge:add_spawns", "biomes": ids, "spawners": spawners})


# ------------------------------------------------------------------- Overworld
def overworld():
    specs, ids = [], []
    index = {g: 0 for g in OW_GROUPS}
    for bid, name, group, top, under, veg, k in OW_BIOMES:
        temp, down, sky, fog, water, wfog, grass, foliage, pairs, critters = OW_GROUPS[group]
        i = index[group]
        index[group] += 1
        t, h = pairs[i // 4]
        effects = {"sky_color": shade(sky, k), "fog_color": shade(fog, k), "water_color": shade(water, k),
                   "water_fog_color": wfog, "grass_color": shade(grass, k), "foliage_color": shade(foliage, k)}
        feats = features({1: ["minecraft:lake_lava_underground", "minecraft:lake_lava_surface"],
                          3: ["minecraft:monster_room", "minecraft:monster_room_deep", "minecraft:amethyst_geode"],
                          6: ORES_STEP, 8: ["minecraft:spring_water", "minecraft:spring_lava"],
                          9: VEG[veg], 10: ["minecraft:freeze_top_layer"]}, {})
        spawners = {c: [] for c in CATEGORIES}
        spawners["monster"] = [spawner(m) for m in STANDARD_MONSTERS]
        spawners["creature"] = [spawner(c) for c in critters]
        spawners["ambient"] = [spawner(("bat", 10, 8, 8))]
        if group == "coast":
            spawners["water_creature"] = [spawner(("squid", 10, 1, 4))]
            spawners["water_ambient"] = [spawner(("cod", 15, 3, 6))]
        carvers = {"air": ["minecraft:cave", "minecraft:cave_extra_underground", "minecraft:canyon"]}
        data = biome_json(temp, down, group != "arid", effects, feats, spawners, carvers)
        data["creature_spawn_probability"] = 0.1
        write(os.path.join(DATA, "worldgen", "biome", bid + ".json"), data)
        specs.append({"id": bid, "name": name, "group": group, "t": t, "h": h, "l": i % 4, "top": top, "under": under})
        ids.append(NS + bid)
    write(os.path.join(DATA, "specs", "overworld.json"), specs, width=400)
    write(os.path.join(DATA, "tags", "worldgen", "biome", "overworld_biomes.json"), {"replace": False, "values": ids})
    cells = {(s["t"], s["h"], s["l"]) for s in specs}
    assert len(cells) == len(specs), "overworld climate cells must be unique"


def main():
    theme_biomes = dimension()
    noise_settings(theme_biomes)
    spawn_modifiers(theme_biomes)
    overworld()
    print("generated %d Hollow Deep biomes and %d Overworld biomes" % (sum(map(len, DIM_BIOMES.values())), len(OW_BIOMES)))


if __name__ == "__main__":
    main()
