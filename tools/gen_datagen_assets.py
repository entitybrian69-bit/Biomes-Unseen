#!/usr/bin/env python3
"""Pre-generate the JSON that the Forge data generators (runData) would emit.

The mod's Java data providers live in src/main/java/com/biomesunseen/datagen,
but `gradle runData` cannot always launch: TerraBlender's MixinBuiltInRegistries
targets an SRG method name that is absent in the mapped dev/datagen runtime, so
the game crashes during Bootstrap before any provider runs. This script emits the
same assets deterministically from the spec tables into src/generated/resources/,
which is already a registered resource source dir (build.gradle) and the exact
output path of runData. If runData succeeds it simply overwrites identical paths.

Standard library only. Run via tools/gen_all.py.
"""
import json
import os

from langdata import CORE_TRANSLATIONS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "src", "main", "resources")
GEN = os.path.join(ROOT, "src", "generated", "resources")
MOD = "biomesunseen"
A = os.path.join(GEN, "assets", MOD)
DM = os.path.join(GEN, "data", MOD)
DMC = os.path.join(GEN, "data", "minecraft")
DFG = os.path.join(GEN, "data", "forge")
SPECS = os.path.join(RES, "data", MOD, "specs")

NAMED_EGGS = [
    ("hollow_stalker", "Hollow Stalker"),
    ("sporeling", "Sporeling"),
    ("gloom_crawler", "Gloom Crawler"),
    ("crystal_golem", "Crystal Golem"),
    ("mire_wraith", "Mire Wraith"),
    ("heart_of_the_forest", "The Heart of the Forest"),
]
NAMED_LOOT = {
    "hollow_stalker": ("bone", 0, 2),
    "sporeling": ("brown_mushroom", 0, 2),
    "gloom_crawler": ("string", 0, 2),
    "crystal_golem": ("amethyst_shard", 1, 4),
    "mire_wraith": ("slime_ball", 0, 2),
}
LOCALES = ["es_es", "fr_fr", "de_de", "pt_br", "ru_ru", "zh_cn", "ja_jp"]
TIER_TAG = {0: "needs_stone_tool", 1: "needs_iron_tool"}


def load(name):
    with open(os.path.join(SPECS, name), encoding="utf-8") as fh:
        return json.load(fh)


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")


def loc(path):
    return "%s:%s" % (MOD, path)


def ore_blocks(ores):
    # hollowite_ore plus one block per generated ore spec.
    return ["hollowite_ore"] + [o["id"] + "_ore" for o in ores]


def gen_blockstates_and_models(ores):
    for block in ore_blocks(ores):
        dump(os.path.join(A, "blockstates", block + ".json"),
             {"variants": {"": {"model": loc("block/" + block)}}})
        dump(os.path.join(A, "models", "block", block + ".json"),
             {"parent": "minecraft:block/cube_all",
              "textures": {"all": loc("block/" + block)}})
        # Inventory model for the block item mirrors the block model.
        dump(os.path.join(A, "models", "item", block + ".json"),
             {"parent": loc("block/" + block)})
    dump(os.path.join(A, "blockstates", "hollow_portal.json"),
         {"variants": {"": {"model": loc("block/hollow_portal")}}})
    dump(os.path.join(A, "models", "block", "hollow_portal.json"),
         {"parent": "minecraft:block/cross", "render_type": "minecraft:cutout",
          "textures": {"cross": loc("block/hollow_portal")}})
    dump(os.path.join(A, "models", "item", "hollow_portal.json"),
         {"parent": loc("block/hollow_portal")})


def gen_item_models(ores, mobs):
    simple_items = ["hollowite_ingot", "field_guide", "hollow_sigil"]
    for name in simple_items:
        dump(os.path.join(A, "models", "item", name + ".json"),
             {"parent": "minecraft:item/generated", "textures": {"layer0": loc("item/" + name)}})
    handheld = ["hollowite_sword", "hollowite_battleaxe"] + [o["id"] + "_sword" for o in ores]
    for name in handheld:
        dump(os.path.join(A, "models", "item", name + ".json"),
             {"parent": "minecraft:item/handheld", "textures": {"layer0": loc("item/" + name)}})
    for o in ores:
        dump(os.path.join(A, "models", "item", o["item"] + ".json"),
             {"parent": "minecraft:item/generated",
              "textures": {"layer0": loc("item/" + o["item"])}})
    for name, _ in NAMED_EGGS:
        dump(os.path.join(A, "models", "item", name + "_spawn_egg.json"),
             {"parent": "minecraft:item/template_spawn_egg"})
    for m in mobs:
        dump(os.path.join(A, "models", "item", m["id"] + "_spawn_egg.json"),
             {"parent": "minecraft:item/template_spawn_egg"})


def gen_lang(ores, mobs, overworld, dimension):
    lang = {
        "itemGroup.%s.main" % MOD: "Biomes Unseen",
        "block.%s.hollowite_ore" % MOD: "Hollowite Ore",
        "block.%s.hollow_portal" % MOD: "Hollow Portal",
        "item.%s.hollowite_ingot" % MOD: "Hollowite Ingot",
        "item.%s.hollowite_sword" % MOD: "Hollowite Sword",
        "item.%s.hollowite_battleaxe" % MOD: "Hollowite Battleaxe",
        "item.%s.field_guide" % MOD: "Biomes Unseen Field Guide",
        "item.%s.hollow_sigil" % MOD: "Hollow Sigil",
        "guide.%s.title" % MOD: "BIOMES UNSEEN — FIELD GUIDE",
        "guide.%s.world" % MOD: "Start a NEW world for all new biomes and structures. Old chunks never regenerate.",
        "guide.%s.biomes" % MOD: "Find a biome: /locate biome biomesunseen:amber_meadow",
        "guide.%s.structures" % MOD: "Find a structure: /locate structure biomesunseen:windmill_ruin",
        "guide.%s.dimension" % MOD: "Use a Hollow Sigil to travel to or from the Hollow Deep. The sigil returns you to Overworld spawn. Backup command: /execute in biomesunseen:hollow_deep run tp @s 0 100 0",
        "guide.%s.portal" % MOD: "Craft a Hollow Portal with 4 obsidian, 4 amethyst shards, and 1 ender eye; walk into it to travel. Its return gate brings you beside that portal if it remains intact.",
        "guide.%s.weapons" % MOD: "Craft ore swords from their matching materials; combine Hollowite and sticks for a battleaxe.",
        "message.%s.hollow_travel.wrong_dimension" % MOD: "Hollow travel only connects the Overworld and Hollow Deep.",
        "message.%s.hollow_travel.cooldown" % MOD: "Hollow travel is recharging. Wait a moment before trying again.",
        "item.%s.hollow_sigil.wrong_dimension" % MOD: "The sigil only works in the Overworld and Hollow Deep.",
        "item.%s.hollow_sigil.dimension_missing" % MOD: "Hollow Deep is not loaded. Create a new world with Biomes Unseen installed.",
    }
    for name, pretty in NAMED_EGGS:
        lang["entity.%s.%s" % (MOD, name)] = pretty
        lang["item.%s.%s_spawn_egg" % (MOD, name)] = pretty + " Spawn Egg"
    for m in mobs:
        lang["entity.%s.%s" % (MOD, m["id"])] = m["name"]
        lang["item.%s.%s_spawn_egg" % (MOD, m["id"])] = m["name"] + " Spawn Egg"
    for o in ores:
        lang["block.%s.%s_ore" % (MOD, o["id"])] = o["name"] + " Ore"
        lang["item.%s.%s" % (MOD, o["item"])] = o["itemName"]
        lang["item.%s.%s_sword" % (MOD, o["id"])] = o["name"] + " Sword"
    for b in overworld + dimension:
        lang["biome.%s.%s" % (MOD, b["id"])] = b["name"]
    dump(os.path.join(A, "lang", "en_us.json"), lang)
    for locale in LOCALES:
        dump(os.path.join(A, "lang", locale + ".json"), CORE_TRANSLATIONS[locale])


def cooking(kind, recipe_id, ingredient, result, xp, time):
    dump(os.path.join(DM, "recipes", recipe_id + ".json"), {
        "type": "minecraft:" + kind,
        "category": "misc",
        "ingredient": {"item": loc(ingredient)},
        "result": loc(result),
        "experience": xp,
        "cookingtime": time,
    })


def shaped_recipe(recipe_id, pattern, key, result, category="combat"):
    dump(os.path.join(DM, "recipes", recipe_id + ".json"), {
        "type": "minecraft:crafting_shaped", "category": category,
        "pattern": pattern, "key": key, "result": {"item": loc(result)},
    })


def gen_recipes(ores):
    cooking("smelting", "hollowite_ingot_from_smelting",
            "hollowite_ore", "hollowite_ingot", 0.9, 200)
    cooking("blasting", "hollowite_ingot_from_blasting",
            "hollowite_ore", "hollowite_ingot", 0.9, 100)
    shaped_recipe("hollowite_sword", ["H", "H", "S"],
                  {"H": {"item": loc("hollowite_ingot")}, "S": {"item": "minecraft:stick"}},
                  "hollowite_sword")
    shaped_recipe("hollowite_battleaxe", ["HHH", "HSH", " S "],
                  {"H": {"item": loc("hollowite_ingot")}, "S": {"item": "minecraft:stick"}},
                  "hollowite_battleaxe")
    shaped_recipe("hollow_portal", ["OAO", "AEA", "OAO"], {
        "O": {"item": "minecraft:obsidian"}, "A": {"item": "minecraft:amethyst_shard"},
        "E": {"item": "minecraft:ender_eye"}}, "hollow_portal", "misc")
    shaped_recipe("hollow_sigil", ["OEO", "GPG", "OEO"], {
        "O": {"item": "minecraft:obsidian"}, "E": {"item": "minecraft:ender_pearl"},
        "G": {"item": "minecraft:glowstone_dust"}, "P": {"item": "minecraft:paper"}}, "hollow_sigil", "misc")
    dump(os.path.join(DM, "recipes", "field_guide.json"), {
        "type": "minecraft:crafting_shapeless", "category": "misc",
        "ingredients": [{"item": "minecraft:book"}, {"item": "minecraft:paper"},
                        {"item": "minecraft:compass"}],
        "result": {"item": loc("field_guide")},
    })
    for o in ores:
        cooking("smelting", o["item"] + "_from_smelting",
                o["id"] + "_ore", o["item"], 0.7, 200)
        cooking("blasting", o["item"] + "_from_blasting",
                o["id"] + "_ore", o["item"], 0.7, 100)
        shaped_recipe(o["id"] + "_sword", ["M", "M", "S"], {
            "M": {"item": loc(o["item"])}, "S": {"item": "minecraft:stick"}},
            o["id"] + "_sword")


def ore_loot(block, drop, lo, hi):
    silk = {"condition": "minecraft:match_tool", "predicate": {"enchantments": [
        {"enchantment": "minecraft:silk_touch", "levels": {"min": 1}}]}}
    return {
        "type": "minecraft:block",
        "pools": [{
            "rolls": 1, "bonus_rolls": 0,
            "entries": [{
                "type": "minecraft:alternatives",
                "children": [
                    {"type": "minecraft:item", "name": loc(block),
                     "conditions": [silk]},
                    {"type": "minecraft:item", "name": loc(drop),
                     "functions": [
                         {"function": "minecraft:set_count",
                          "count": {"type": "minecraft:uniform", "min": lo, "max": hi},
                          "add": False},
                         {"function": "minecraft:apply_bonus",
                          "enchantment": "minecraft:fortune",
                          "formula": "minecraft:ore_drops"},
                         {"function": "minecraft:explosion_decay"}]},
                ],
            }],
        }],
    }


def gen_block_loot(ores):
    dump(os.path.join(DM, "loot_tables", "blocks", "hollow_portal.json"), {
        "type": "minecraft:block",
        "pools": [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": loc("hollow_portal")}]}],
    })
    dump(os.path.join(DM, "loot_tables", "blocks", "hollowite_ore.json"),
         ore_loot("hollowite_ore", "hollowite_ingot", 1, 1))
    for o in ores:
        dump(os.path.join(DM, "loot_tables", "blocks", o["id"] + "_ore.json"),
             ore_loot(o["id"] + "_ore", o["item"],
                       o.get("dropMin", 1), o.get("dropMax", 1)))


def named_entity_loot(item, lo, hi):
    return {
        "type": "minecraft:entity",
        "pools": [
            {"rolls": 1, "bonus_rolls": 0, "entries": [{
                "type": "minecraft:item", "name": "minecraft:" + item,
                "functions": [
                    {"function": "minecraft:set_count",
                     "count": {"type": "minecraft:uniform", "min": lo, "max": hi}},
                    {"function": "minecraft:looting_enchant",
                     "count": {"type": "minecraft:uniform", "min": 0, "max": 1}}]}]},
            {"rolls": 1, "bonus_rolls": 0, "entries": [{
                "type": "minecraft:item", "name": loc("hollowite_ingot"),
                "functions": [
                    {"function": "minecraft:set_count",
                     "count": {"type": "minecraft:uniform", "min": 0, "max": 1}}]}]},
        ],
    }


def gen_named_entity_loot():
    for name, (item, lo, hi) in NAMED_LOOT.items():
        dump(os.path.join(DM, "loot_tables", "entities", name + ".json"),
             named_entity_loot(item, lo, hi))


def gen_block_tags(ores):
    values = [loc(b) for b in ore_blocks(ores)]
    dump(os.path.join(DMC, "tags", "blocks", "mineable", "pickaxe.json"),
         {"replace": False, "values": values})
    dump(os.path.join(DFG, "tags", "blocks", "ores.json"),
         {"replace": False, "values": values})
    buckets = {}
    buckets["needs_iron_tool"] = [loc("hollowite_ore")]
    for o in ores:
        tag = TIER_TAG.get(o["tier"], "needs_diamond_tool")
        buckets.setdefault(tag, []).append(loc(o["id"] + "_ore"))
    for tag, vals in buckets.items():
        dump(os.path.join(DMC, "tags", "blocks", tag + ".json"),
             {"replace": False, "values": vals})


def main():
    ores = load("ores.json")
    mobs = load("mobs.json")
    overworld = load("overworld.json")
    dimension = load("dimension_biomes.json")
    gen_blockstates_and_models(ores)
    gen_item_models(ores, mobs)
    gen_lang(ores, mobs, overworld, dimension)
    gen_recipes(ores)
    gen_block_loot(ores)
    gen_named_entity_loot()
    gen_block_tags(ores)
    count = sum(len(files) for _, _, files in os.walk(GEN))
    print("generated %d data-generator asset file(s) into src/generated/resources" % count)


if __name__ == "__main__":
    main()
