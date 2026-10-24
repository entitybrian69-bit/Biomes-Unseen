"""Canonical global decoration order for features shared by modded biomes.

This sequence is a topological order of the vanilla Minecraft 1.20.1 biome
feature constraints for features used here (plus the custom-only forest_rock).
Keep generated biome feature lists as subsequences; otherwise FeatureSorter can
find cross-biome cycles during chunk generation.
"""
FEATURE_ORDER = {
    7: [
        "minecraft:glow_lichen",
        "minecraft:large_dripstone",
        "minecraft:pointed_dripstone",
    ],
    9: [
        "minecraft:bamboo_light",
        "minecraft:dark_forest_vegetation",
        "minecraft:flower_forest_flowers",
        "minecraft:patch_tall_grass",
        "minecraft:forest_rock",
        "minecraft:cave_vines",
        "minecraft:patch_sunflower",
        "minecraft:spore_blossom",
        "minecraft:trees_birch",
        "minecraft:trees_birch_and_oak",
        "minecraft:trees_flower_forest",
        "minecraft:trees_jungle",
        "minecraft:trees_plains",
        "minecraft:flower_plains",
        "minecraft:patch_grass_plain",
        "minecraft:trees_savanna",
        "minecraft:trees_snowy",
        "minecraft:patch_grass_jungle",
        "minecraft:trees_swamp",
        "minecraft:flower_swamp",
        "minecraft:trees_taiga",
        "minecraft:flower_default",
        "minecraft:patch_grass_forest",
        "minecraft:patch_grass_taiga",
        "minecraft:patch_dead_bush",
        "minecraft:patch_waterlily",
        "minecraft:brown_mushroom_swamp",
        "minecraft:red_mushroom_swamp",
        "minecraft:brown_mushroom_normal",
        "minecraft:red_mushroom_normal",
        "minecraft:patch_sugar_cane",
        "minecraft:patch_pumpkin",
        "minecraft:patch_berry_common",
        "minecraft:patch_cactus_desert",
        "minecraft:patch_melon",
    ],
}
