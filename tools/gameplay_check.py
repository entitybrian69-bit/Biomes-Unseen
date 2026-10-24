"""Focused checks for the Hollow Portal, its travel route, and translated guide UI."""
import json
import os


LOCALES = ("es_es", "fr_fr", "de_de", "pt_br", "ru_ru", "zh_cn", "ja_jp")


def check_gameplay_assets(root):
    errors = []
    generated = os.path.join(root, "src", "generated", "resources")
    main = os.path.join(root, "src", "main", "resources")
    java = os.path.join(root, "src", "main", "java", "com", "biomesunseen")

    def require(path, label):
        if not os.path.exists(path):
            errors.append("missing %s (%s)" % (label, os.path.relpath(path, root)))
            return None
        return path

    def load(path, label):
        path = require(path, label)
        if path is None:
            return {}
        try:
            with open(path, encoding="utf-8") as stream:
                return json.load(stream)
        except (OSError, ValueError) as exc:
            errors.append("%s is invalid JSON (%s)" % (label, exc))
            return {}

    mod_assets = os.path.join(generated, "assets", "biomesunseen")
    mod_data = os.path.join(generated, "data", "biomesunseen")
    blockstate = load(os.path.join(mod_assets, "blockstates", "hollow_portal.json"), "Hollow Portal blockstate")
    if blockstate.get("variants", {}).get("", {}).get("model") != "biomesunseen:block/hollow_portal":
        errors.append("Hollow Portal blockstate does not point to its model")
    model = load(os.path.join(mod_assets, "models", "block", "hollow_portal.json"), "Hollow Portal block model")
    if (model.get("parent") != "minecraft:block/cross"
            or model.get("textures", {}).get("cross") != "biomesunseen:block/hollow_portal"
            or model.get("render_type") != "minecraft:cutout"):
        errors.append("Hollow Portal model is not a textured, cutout cross plane")
    require(os.path.join(main, "assets", "biomesunseen", "textures", "block", "hollow_portal.png"),
            "Hollow Portal texture")
    require(os.path.join(mod_assets, "models", "item", "hollow_portal.json"), "Hollow Portal item model")

    recipe = load(os.path.join(mod_data, "recipes", "hollow_portal.json"), "Hollow Portal recipe")
    if recipe.get("type") != "minecraft:crafting_shaped" or recipe.get("result", {}).get("item") != "biomesunseen:hollow_portal":
        errors.append("Hollow Portal recipe does not craft the registered block")
    loot = load(os.path.join(mod_data, "loot_tables", "blocks", "hollow_portal.json"), "Hollow Portal loot table")
    if "biomesunseen:hollow_portal" not in json.dumps(loot):
        errors.append("Hollow Portal loot table does not drop the block")
    core_recipes = {
        "field_guide": "field_guide", "hollow_sigil": "hollow_sigil",
        "hollowite_sword": "hollowite_sword", "hollowite_battleaxe": "hollowite_battleaxe",
    }
    for recipe_id, result_id in core_recipes.items():
        crafted = load(os.path.join(mod_data, "recipes", recipe_id + ".json"), recipe_id + " recipe")
        if crafted.get("result", {}).get("item") != "biomesunseen:" + result_id:
            errors.append("%s recipe does not produce its registered item" % recipe_id)
    ores_path = os.path.join(main, "data", "biomesunseen", "specs", "ores.json")
    if os.path.exists(ores_path):
        with open(ores_path, encoding="utf-8") as stream:
            for ore in json.load(stream):
                sword_id = ore["id"] + "_sword"
                sword = load(os.path.join(mod_data, "recipes", sword_id + ".json"), sword_id + " recipe")
                if sword.get("result", {}).get("item") != "biomesunseen:" + sword_id:
                    errors.append("%s recipe does not produce its matching weapon" % sword_id)

    sounds = load(os.path.join(main, "assets", "biomesunseen", "sounds.json"), "sound definitions")
    if "hollow_gate.travel" not in sounds:
        errors.append("Hollow Portal travel sound event is not defined")
    for path, label, needle in (
            (os.path.join(java, "registry", "ModBlocks.java"), "portal block registration", 'register("hollow_portal"'),
            (os.path.join(java, "registry", "ModItems.java"), "portal item registration", 'register("hollow_portal"'),
            (os.path.join(java, "registry", "ModSounds.java"), "portal travel sound registration", 'reg("hollow_gate.travel")'),
            (os.path.join(java, "block", "HollowPortalBlock.java"), "portal collision travel handler", "HollowTravel.travel(player, pos)"),
            (os.path.join(java, "worldgen", "HollowTravel.java"), "two-way dimension transfer", "player.teleportTo(destination"),
            (os.path.join(java, "item", "HollowSigilItem.java"), "sigil travel integration", "HollowTravel.travel(serverPlayer)"),
            (os.path.join(java, "event", "WorldgenAudit.java"), "portal recipe startup audit", 'hasRecipe(event, "hollow_portal")'),
            (os.path.join(java, "event", "HollowTravelSmokeTest.java"), "server-side player travel smoke test", "portal.entityInside(")):
        path = require(path, label)
        if path:
            with open(path, encoding="utf-8") as stream:
                if needle not in stream.read():
                    errors.append("%s is not wired into gameplay" % label)

    english = load(os.path.join(mod_assets, "lang", "en_us.json"), "English language file")
    english_keys = ("block.biomesunseen.hollow_portal", "guide.biomesunseen.dimension",
                    "guide.biomesunseen.portal", "message.biomesunseen.hollow_travel.wrong_dimension",
                    "message.biomesunseen.hollow_travel.cooldown")
    if not all(key in english for key in english_keys):
        errors.append("English language file is missing portal/guide text")
    for locale in LOCALES:
        translated = load(os.path.join(mod_assets, "lang", locale + ".json"), locale + " language file")
        if (not translated or "guide.biomesunseen.title" not in translated
                or "guide.biomesunseen.portal" not in translated
                or "message.biomesunseen.hollow_travel.wrong_dimension" not in translated
                or "message.biomesunseen.hollow_travel.cooldown" not in translated):
            errors.append("%s language file is empty or lacks Field Guide/portal translations" % locale)
    return errors
