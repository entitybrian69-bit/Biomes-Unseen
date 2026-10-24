#!/usr/bin/env python3
"""Biomes Unseen repo validator (pure standard library).

Checks:
  1. texdata matrices are well formed (via gen_textures.validate)
  2. every texture a model/geo/datagen provider references has a texdata entry
  3. every .png has the PNG magic bytes; every geo model's texture size matches its sprite
  4. every .ogg has OggS + vorbis headers; every sounds.json entry has a file
  5. AI-goal grep: every entity class (own source or superclass) has FloatGoal,
     MeleeAttackGoal, HurtByTargetGoal, NearestAttackableTargetGoal; bosses also RangedAttackGoal
  6. every entity registered in ModEntities has geo + animation + texture entry
  7. all resource JSON parses; no TODO markers; no source file over 350 lines
  8. generated content: every spec mob/ore has model, texture, loot and sounds; biome features are
     known vanilla ids; dimension/structure/biome-modifier references resolve to real files
Usage: python tools/validate.py   (exit code 1 if any error)
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import gen_textures  # noqa: E402

MOD = "biomesunseen"
RES = os.path.join(ROOT, "src", "main", "resources")
GEN = os.path.join(ROOT, "src", "generated", "resources")
ASSETS = [os.path.join(RES, "assets", MOD), os.path.join(GEN, "assets", MOD)]
JAVA = os.path.join(ROOT, "src", "main", "java")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
GOALS = ["FloatGoal", "MeleeAttackGoal", "HurtByTargetGoal", "NearestAttackableTargetGoal"]
MAX_LINES = 350

DATA = os.path.join(RES, "data", MOD)
SPECS = os.path.join(DATA, "specs")
KNOWN_FEATURES = set("""
glow_lichen spore_blossom cave_vines amethyst_geode large_dripstone pointed_dripstone lake_lava_underground
lake_lava_surface monster_room monster_room_deep spring_water spring_lava freeze_top_layer ore_dirt ore_gravel
ore_granite_upper ore_granite_lower ore_diorite_upper ore_diorite_lower ore_andesite_upper ore_andesite_lower
ore_tuff ore_coal_upper ore_coal_lower ore_iron_upper ore_iron_middle ore_iron_small ore_gold ore_gold_lower
ore_redstone ore_redstone_lower ore_diamond ore_diamond_large ore_diamond_buried ore_lapis ore_lapis_buried
ore_copper trees_plains trees_birch trees_taiga trees_snowy trees_swamp trees_savanna trees_jungle
trees_flower_forest trees_birch_and_oak dark_forest_vegetation flower_default flower_plains flower_forest_flowers
flower_swamp patch_grass_plain patch_grass_forest patch_grass_taiga patch_grass_jungle patch_tall_grass
patch_dead_bush patch_cactus_desert patch_sugar_cane patch_pumpkin patch_melon patch_waterlily
brown_mushroom_normal red_mushroom_normal brown_mushroom_swamp red_mushroom_swamp bamboo_light forest_rock
patch_berry_common patch_sunflower
""".split())
KNOWN_CARVERS = {"minecraft:cave", "minecraft:cave_extra_underground", "minecraft:canyon"}

errors, warnings = [], []


def rel(path):
    return os.path.relpath(path, ROOT)


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def check_sprites():
    sprites = gen_textures.load_sprites()
    for key, rows in sprites.items():
        try:
            gen_textures.validate(key, rows)
        except SystemExit as exc:
            errors.append("texdata: %s" % exc)
    return sprites


def texture_refs():
    """Yield (source, texture key) for every texture reference in models, blockstates and datagen."""
    pattern = re.compile(r'"%s:((?:block|item|entity)/[a-z0-9_/]+)"' % MOD)
    for base in ASSETS:
        for path in glob.glob(os.path.join(base, "models", "**", "*.json"), recursive=True):
            for key in pattern.findall(read(path)):
                yield rel(path), key
    mod_loc = re.compile(r'modLoc\("((?:block|item|entity)/[a-z0-9_/]+)"\)')
    for path in glob.glob(os.path.join(JAVA, "**", "datagen", "*.java"), recursive=True):
        for key in mod_loc.findall(read(path)):
            yield rel(path), key
    for path in glob.glob(os.path.join(ASSETS[0], "geo", "entity", "*.geo.json")):
        name = os.path.basename(path)[: -len(".geo.json")]
        yield rel(path), "entity/" + name


def check_texture_refs(sprites):
    for source, key in texture_refs():
        if key not in sprites:
            errors.append("%s references texture '%s' with no texdata entry" % (source, key))
    for path in glob.glob(os.path.join(ASSETS[0], "geo", "entity", "*.geo.json")):
        name = os.path.basename(path)[: -len(".geo.json")]
        sprite = sprites.get("entity/" + name)
        if sprite is None:
            continue
        desc = json.loads(read(path))["minecraft:geometry"][0]["description"]
        if (desc["texture_width"], desc["texture_height"]) != (len(sprite[0]), len(sprite)):
            errors.append("%s: texture size %sx%s != sprite %dx%d" % (
                rel(path), desc["texture_width"], desc["texture_height"], len(sprite[0]), len(sprite)))


def check_png(sprites):
    found = set()
    for base in ASSETS:
        for path in glob.glob(os.path.join(base, "textures", "**", "*.png"), recursive=True):
            found.add(os.path.relpath(path, os.path.join(base, "textures"))[:-4].replace(os.sep, "/"))
            with open(path, "rb") as fh:
                if fh.read(8) != PNG_MAGIC:
                    errors.append("%s: bad PNG magic bytes" % rel(path))
    for key in sprites:
        if key not in found:
            warnings.append("texture '%s' not generated yet (run tools/gen_textures.py)" % key)


def check_ogg():
    sounds_path = os.path.join(ASSETS[0], "sounds.json")
    for path in glob.glob(os.path.join(ASSETS[0], "sounds", "**", "*.ogg"), recursive=True):
        with open(path, "rb") as fh:
            head = fh.read(64)
        if head[:4] != b"OggS" or b"\x01vorbis" not in head:
            errors.append("%s: missing OggS/vorbis header" % rel(path))
    if not os.path.exists(sounds_path):
        errors.append("sounds.json missing")
        return
    for event, entry in json.loads(read(sounds_path)).items():
        for sound in entry["sounds"]:
            name = sound["name"] if isinstance(sound, dict) else sound
            namespace, _, path = name.partition(":")
            target = os.path.join(ASSETS[0], "sounds", *path.split("/")) + ".ogg"
            if namespace == MOD and not os.path.exists(target):
                warnings.append("sound '%s' has no file yet (run tools/gen_audio.py)" % event)


def java_sources():
    return glob.glob(os.path.join(JAVA, "**", "*.java"), recursive=True)


def check_ai_goals():
    sources = {os.path.basename(p)[:-5]: read(p) for p in java_sources()}

    def has(cls, tokens, depth=0):
        src = sources.get(cls)
        if src is None or depth > 6:
            return False
        if all(t in src for t in tokens):
            return True
        parent = re.search(r"class\s+%s\s+extends\s+(\w+)" % cls, src)
        return bool(parent) and has(parent.group(1), tokens, depth + 1)

    for path in java_sources():
        if os.sep + "entity" + os.sep not in path:
            continue
        cls = os.path.basename(path)[:-5]
        src = sources[cls]
        if not re.search(r"class\s+%s\s+extends\s+(Monster|BaseHollowMob)" % cls, src):
            continue
        tokens = GOALS + (["RangedAttackGoal"] if os.sep + "boss" + os.sep in path else [])
        if not has(cls, tokens):
            errors.append("%s: missing required AI goals %s" % (rel(path), tokens))


def check_registered_entities(sprites):
    path = os.path.join(JAVA, "com", MOD, "registry", "ModEntities.java")
    names = re.findall(r'register\("([a-z0-9_]+)",', read(path))
    if not names:
        errors.append("no entities found in ModEntities")
    for name in names:
        for sub, ext in (("geo", ".geo.json"), ("animations", ".animation.json")):
            if not os.path.exists(os.path.join(ASSETS[0], sub, "entity", name + ext)):
                errors.append("entity '%s' missing %s/entity/%s%s" % (name, sub, name, ext))
        if "entity/" + name not in sprites:
            errors.append("entity '%s' has no texdata entry entity/%s" % (name, name))


def check_json_and_source():
    for base in (RES, GEN):
        for path in glob.glob(os.path.join(base, "**", "*.json"), recursive=True):
            try:
                json.loads(read(path))
            except ValueError as exc:
                errors.append("%s: invalid JSON (%s)" % (rel(path), exc))
    files = java_sources() + glob.glob(os.path.join(ROOT, "tools", "**", "*.py"), recursive=True)
    for path in files:
        text = read(path)
        count = text.count("\n")
        if count > MAX_LINES:
            errors.append("%s: %d lines (limit %d)" % (rel(path), count, MAX_LINES))
        if "TODO" in text and os.path.basename(path) != "validate.py":
            errors.append("%s: contains TODO" % rel(path))


def load_spec(name):
    path = os.path.join(SPECS, name)
    if not os.path.exists(path):
        warnings.append("specs/%s missing (run tools/gen_all.py)" % name)
        return []
    return json.loads(read(path))


def check_generated(sprites):
    mobs, ores = load_spec("mobs.json"), load_spec("ores.json")
    sounds = json.loads(read(os.path.join(ASSETS[0], "sounds.json")))
    for m in mobs:
        mid = m["id"]
        for sub, ext in (("geo", ".geo.json"), ("animations", ".animation.json")):
            if not os.path.exists(os.path.join(ASSETS[0], sub, "entity", mid + ext)):
                errors.append("mob '%s' missing %s file" % (mid, sub))
        if "entity/" + mid not in sprites:
            errors.append("mob '%s' has no texdata entry" % mid)
        if not os.path.exists(os.path.join(DATA, "loot_tables", "entities", mid + ".json")):
            errors.append("mob '%s' has no loot table" % mid)
        if "generic_%s.ambient" % m["archetype"] not in sounds:
            errors.append("mob '%s': no sounds for archetype %s" % (mid, m["archetype"]))
    for o in ores:
        for key in ("block/%s_ore" % o["id"], "item/" + o["item"]):
            if key not in sprites:
                errors.append("ore '%s' has no texdata entry %s" % (o["id"], key))
    return {m["id"] for m in mobs}


def biome_ids():
    return {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(DATA, "worldgen", "biome", "*.json"))}


def check_worldgen(spec_mobs):
    biomes = biome_ids()
    for name in sorted(biomes):
        data = json.loads(read(os.path.join(DATA, "worldgen", "biome", name + ".json")))
        for step in data["features"]:
            for fid in step:
                if fid.startswith("minecraft:") and fid[10:] not in KNOWN_FEATURES:
                    errors.append("biome %s uses unlisted vanilla feature %s" % (name, fid))
        for carver in data["carvers"].get("air", []):
            if carver not in KNOWN_CARVERS:
                errors.append("biome %s uses unknown carver %s" % (name, carver))
    dim = os.path.join(DATA, "dimension", "hollow_deep.json")
    if os.path.exists(dim):
        for entry in json.loads(read(dim))["generator"]["biome_source"]["biomes"]:
            if entry["biome"].split(":")[1] not in biomes:
                errors.append("dimension references missing biome %s" % entry["biome"])
    entities = spec_mobs | {"hollow_stalker", "sporeling", "gloom_crawler", "crystal_golem", "mire_wraith"}
    tags = os.path.join(DATA, "tags", "worldgen", "biome")
    for path in glob.glob(os.path.join(DATA, "forge", "biome_modifier", "*.json")):
        data = json.loads(read(path))
        biome_set = data.get("biomes")
        if isinstance(biome_set, str) and biome_set.startswith("#biomesunseen:"):
            if not os.path.exists(os.path.join(tags, biome_set[14:] + ".json")):
                errors.append("%s: biome tag %s missing" % (rel(path), biome_set))
        for b in biome_set if isinstance(biome_set, list) else []:
            if b.split(":")[1] not in biomes:
                errors.append("%s: missing biome %s" % (rel(path), b))
        for sp in data.get("spawners", []):
            if sp["type"].startswith("biomesunseen:") and sp["type"][13:] not in entities:
                errors.append("%s: unknown mob %s" % (rel(path), sp["type"]))
        feature = data.get("features")
        if feature and not os.path.exists(os.path.join(DATA, "worldgen", "placed_feature", feature[13:] + ".json")):
            errors.append("%s: placed feature %s missing" % (rel(path), feature))
    for path in glob.glob(os.path.join(DATA, "worldgen", "structure", "*.json")):
        data = json.loads(read(path))
        tag = data["biomes"][len("#biomesunseen:"):]
        if not os.path.exists(os.path.join(tags, tag + ".json")):
            errors.append("%s: biome tag %s missing" % (rel(path), tag))
        pool = data["start_pool"][len("biomesunseen:"):]
        pool_path = os.path.join(DATA, "worldgen", "template_pool", pool + ".json")
        if not os.path.exists(pool_path):
            errors.append("%s: template pool %s missing" % (rel(path), pool))
            continue
        template = json.loads(read(pool_path))["elements"][0]["element"]["location"][len("biomesunseen:"):]
        if not os.path.exists(os.path.join(DATA, "structures", template + ".nbt")):
            warnings.append("structure template %s.nbt missing (run tools/gen_structure_set.py)" % template)
    structures = len(glob.glob(os.path.join(DATA, "worldgen", "structure", "*.json")))
    ores = len(glob.glob(os.path.join(DATA, "worldgen", "placed_feature", "ore_*.json")))
    print("content: %d biomes, %d mobs, %d structures, %d ore features" % (len(biomes), len(spec_mobs), structures, ores))


def main():
    sprites = check_sprites()
    check_texture_refs(sprites)
    check_png(sprites)
    check_ogg()
    check_ai_goals()
    check_registered_entities(sprites)
    spec_mobs = check_generated(sprites)
    check_worldgen(spec_mobs)
    check_json_and_source()
    for w in warnings:
        print("WARN  " + w)
    for e in errors:
        print("ERROR " + e)
    print("%d error(s), %d warning(s)" % (len(errors), len(warnings)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
