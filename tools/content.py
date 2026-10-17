# -*- coding: utf-8 -*-
"""Biomes Unseen - canonical content tables.

Every table here is expanded into real Java sources, data JSON and assets by the
other tools/* emitters.  Nothing in this file is a placeholder: each entry is a
complete definition used verbatim in generated code.
"""

MOD_ID = "biomesunseen"
MOD_NAME = "Biomes Unseen"
MOD_VERSION = "1.0.3"
MOD_GROUP = "com.biomesunseen"
MOD_DESCRIPTION = (
    "A massive world-generation, adventure, biome, structure, ore, mob and boss "
    "mod: 80 biomes, 20 ores, 30 structures, 25 mobs and 2 multi-phase bosses."
)
MOD_LICENSE = "MIT"
MOD_AUTHORS = "Biomes Unseen Team"

# ---------------------------------------------------------------------------
# Target matrix.  (mc_version, java_version, loaders, family)
# family selects the shared source tree compiled into that module.
# ---------------------------------------------------------------------------

FAMILY_V116 = "v116"    # 1.16.5          - SurfaceBuilder / ConfiguredFeature era
FAMILY_V117 = "v117"    # 1.17.1          - last pre-noise-overhaul worldgen
FAMILY_V118 = "v118"    # 1.18.1-1.19.2   - PlacedFeature / MultiNoise era
FAMILY_MODERN = "modern"  # 1.19.3-1.21.11 - current registry + structure-set era
FAMILY_V26 = "v26"      # 26.x            - modern MultiNoise / StructureSet era

TARGETS = [
    # (mc, java, loaders, family)
    ("1.16.5",   8,  ("fabric", "forge"),   FAMILY_V116),
    ("1.17.1",  16,  ("fabric", "forge"),   FAMILY_V117),
    ("1.18.1",  17,  ("fabric", "forge"),   FAMILY_V118),
    ("1.18.2",  17,  ("fabric", "forge"),   FAMILY_V118),
    ("1.19",    17,  ("fabric", "forge"),   FAMILY_V118),
    ("1.19.1",  17,  ("fabric", "forge"),   FAMILY_V118),
    ("1.19.2",  17,  ("fabric", "forge"),   FAMILY_V118),
    ("1.19.3",  17,  ("fabric", "forge"),   FAMILY_MODERN),
    ("1.19.4",  17,  ("fabric", "forge"),   FAMILY_MODERN),
    ("1.20",    17,  ("fabric", "forge"),   FAMILY_MODERN),
    ("1.20.1",  17,  ("fabric", "forge"),   FAMILY_MODERN),
    ("1.20.2",  17,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("1.20.3",  17,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("1.20.4",  17,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("1.20.5",  21,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("1.20.6",  21,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("1.21",    21,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("1.21.1",  21,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("1.21.2",  21,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("1.21.3",  21,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("1.21.4",  21,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("1.21.5",  21,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("1.21.6",  21,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("1.21.7",  21,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("1.21.8",  21,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("1.21.9",  21,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("1.21.10", 21,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("1.21.11", 21,  ("fabric", "neoforge"), FAMILY_MODERN),
    ("26.1",    25,  ("fabric", "neoforge"), FAMILY_V26),
    ("26.1.1",  25,  ("fabric", "neoforge"), FAMILY_V26),
    ("26.1.2",  25,  ("fabric", "neoforge"), FAMILY_V26),
    ("26.2",    25,  ("fabric", "neoforge"), FAMILY_V26),
    ("26.3",    25,  ("fabric", "neoforge"), FAMILY_V26),
]

# ---------------------------------------------------------------------------
# Dependency versions per Minecraft line.  These are the pinned versions the
# build resolves; BUILD.md documents how to bump them.
# ---------------------------------------------------------------------------

FABRIC_LOADER_VERSION = "0.16.9"
FABRIC_API_VERSIONS = {
    "1.16.5": "0.42.0+1.16",
    "1.17.1": "0.46.1+1.17",
    "1.18.1": "0.46.6+1.18",
    "1.18.2": "0.77.0+1.18.2",
    "1.19": "0.58.0+1.19",
    "1.19.1": "0.58.5+1.19.1",
    "1.19.2": "0.76.1+1.19.2",
    "1.19.3": "0.76.1+1.19.3",
    "1.19.4": "0.87.2+1.19.4",
    "1.20": "0.83.0+1.20",
    "1.20.1": "0.92.11+1.20.1",
    "1.20.2": "0.91.6+1.20.2",
    "1.20.3": "0.91.1+1.20.3",
    "1.20.4": "0.97.3+1.20.4",
    "1.20.5": "0.97.8+1.20.5",
    "1.20.6": "0.100.8+1.20.6",
    "1.21": "0.102.1+1.21",
    "1.21.1": "0.116.17+1.21.1",
    "1.21.2": "0.106.1+1.21.2",
    "1.21.3": "0.114.1+1.21.3",
    "1.21.4": "0.119.4+1.21.4",
    "1.21.5": "0.128.1+1.21.5",
    "1.21.6": "0.128.2+1.21.6",
    "1.21.7": "0.129.0+1.21.7",
    "1.21.8": "0.136.1+1.21.8",
    "1.21.9": "0.134.1+1.21.9",
    "1.21.10": "0.138.4+1.21.10",
    "1.21.11": "0.141.6+1.21.11",
    "26.1": "0.152.1+26.1",
    "26.1.1": "0.145.4+26.1.1",
    "26.1.2": "0.155.3+26.1.2",
    "26.2": "0.161.0+26.2",
    "26.3": "0.163.0+26.3",
}
YARN_VERSIONS = {
    "1.16.5": "1.16.5+build.10",
    "1.17.1": "1.17.1+build.65",
    "1.18.1": "1.18.1+build.22",
    "1.18.2": "1.18.2+build.4",
    "1.19": "1.19+build.4",
    "1.19.1": "1.19.1+build.6",
    "1.19.2": "1.19.2+build.28",
    "1.19.3": "1.19.3+build.5",
    "1.19.4": "1.19.4+build.2",
    "1.20": "1.20+build.1",
    "1.20.1": "1.20.1+build.10",
    "1.20.2": "1.20.2+build.4",
    "1.20.3": "1.20.3+build.2",
    "1.20.4": "1.20.4+build.3",
    "1.20.5": "1.20.5+build.1",
    "1.20.6": "1.20.6+build.3",
    "1.21": "1.21+build.9",
    "1.21.1": "1.21.1+build.3",
    "1.21.2": "1.21.2+build.1",
    "1.21.3": "1.21.3+build.2",
    "1.21.4": "1.21.4+build.8",
    "1.21.5": "1.21.5+build.1",
    "1.21.6": "1.21.6+build.1",
    "1.21.7": "1.21.7+build.1",
    "1.21.8": "1.21.8+build.1",
    "1.21.9": "1.21.9+build.1",
    "1.21.10": "1.21.10+build.1",
    "1.21.11": "1.21.11+build.1",
    "26.1": "26.1+build.1",
    "26.1.1": "26.1.1+build.1",
    "26.1.2": "26.1.2+build.1",
    "26.2": "26.2+build.1",
    "26.3": "26.3+build.1",
}
FORGE_VERSIONS = {
    "1.16.5": "1.16.5-36.2.42",
    "1.17.1": "1.17.1-37.1.1",
    "1.18.1": "1.18.1-39.1.2",
    "1.18.2": "1.18.2-40.2.21",
    "1.19": "1.19-41.1.0",
    "1.19.1": "1.19.1-42.0.9",
    "1.19.2": "1.19.2-43.4.2",
    "1.19.3": "1.19.3-44.1.23",
    "1.19.4": "1.19.4-45.2.0",
    "1.20": "1.20-46.0.14",
    "1.20.1": "1.20.1-47.3.12",
}
NEOFORGE_VERSIONS = {
    "1.20.2": "20.2.51-beta",
    "1.20.3": "20.3.+",
    "1.20.4": "20.4.+",
    "1.20.5": "20.5.+",
    "1.20.6": "20.6.+",
    "1.21": "21.0.+",
    "1.21.1": "21.1.+",
    "1.21.2": "21.2.+",
    "1.21.3": "21.3.+",
    "1.21.4": "21.4.+",
    "1.21.5": "21.5.+",
    "1.21.6": "21.6.+",
    "1.21.7": "21.7.+",
    "1.21.8": "21.8.+",
    "1.21.9": "21.9.+",
    "1.21.10": "21.10.+",
    "1.21.11": "21.11.+",
    "26.1": "26.1.2.3",
    "26.1.1": "26.1.1.3",
    "26.1.2": "26.1.2.3",
    "26.2": "26.2.+",
    "26.3": "26.3.+",
}
ARCHITECTURY_API_VERSIONS = {
    "1.16.5": "1.32.68",
    "1.17.1": "3.6.18",
    "1.18.1": "3.6.18",
    "1.18.2": "3.9.66",
    "1.19": "4.5.76",
    "1.19.1": "4.5.76",
    "1.19.2": "5.12.45",
    "1.19.3": "6.4.62",
    "1.19.4": "7.1.86",
    "1.20": "8.2.91",
    "1.20.1": "9.1.13",
    "1.20.2": "10.0.18",
    "1.20.3": "11.1.17",
    "1.20.4": "11.1.17",
    "1.20.5": "12.1.4",
    "1.20.6": "12.1.4",
    "1.21": "13.0.8",
    "1.21.1": "14.0.4",
    "1.21.2": "14.0.4",
    "1.21.3": "14.0.4",
    "1.21.4": "15.0.3",
    "1.21.5": "16.1.4",
    "1.21.6": "17.0.8",
    "1.21.7": "17.0.8",
    "1.21.8": "17.0.8",
    "1.21.9": "18.0.8",
    "1.21.10": "18.0.8",
    "1.21.11": "19.0.1",
    "26.1": "20.0.12",
    "26.1.1": "20.0.12",
    "26.1.2": "20.0.12",
    "26.2": "21.0.7",
    "26.3": "22.0.5",
}
GECKOLIB_VERSIONS = {
    "1.17.1": "3.0.57",
    "1.18.1": "3.0.57",
    "1.18.2": "3.0.57",
    "1.19": "3.1.40",
    "1.19.1": "3.1.40",
    "1.19.2": "3.1.40",
    "1.19.3": "3.1.40",
    "1.19.4": "3.1.40",
    "1.20": "3.1.40",
    "1.20.1": "4.4.9",
    "1.20.2": "4.4.9",
    "1.20.3": "4.4.9",
    "1.20.4": "4.4.9",
    "1.20.5": "4.4.9",
    "1.20.6": "4.4.9",
    "1.21": "4.7.5",
    "1.21.1": "4.7.5",
    "1.21.2": "4.8.1",
    "1.21.3": "4.8.1",
    "1.21.4": "4.8.3",
    "1.21.5": "4.8.3",
    "1.21.6": "4.9.2",
    "1.21.7": "4.9.2",
    "1.21.8": "4.9.4",
    "1.21.9": "4.10.1",
    "1.21.10": "4.10.1",
    "1.21.11": "4.10.4",
    "26.1": "5.0.2",
    "26.1.1": "5.0.2",
    "26.1.2": "5.0.2",
    "26.2": "5.1.0",
    "26.3": "5.1.2",
}


def geckolib_coord(loader, mc):
    """Full Maven coordinate of a GeckoLib build that actually exists.

    Published artifacts were verified against the official GeckoLib maven
    (dl.cloudsmith.io/public/geckolib3/geckolib/maven). Some Minecraft
    versions were never published a per-patch artifact; those map to the
    closest published artifact of the same API generation.
    """
    G3 = "software.bernie.geckolib"
    if mc.startswith("26"):
        return "com.geckolib:geckolib-%s-26.3:5.5.7" % loader
    if mc == "1.17.1":
        return ("%s:geckolib-forge-1.17.1:3.0.0" % G3) if loader == "forge" \
            else ("%s:geckolib-fabric-1.18.2:3.0.35" % G3)
    if mc in ("1.18.1", "1.18.2"):
        return "%s:geckolib-%s-1.18.2:3.0.35" % (G3, loader)
    if mc in ("1.19", "1.19.1", "1.19.2", "1.19.3"):
        return "%s:geckolib-%s-1.19:3.1.40" % (G3, loader)
    if mc == "1.19.4":
        return ("%s:geckolib-fabric-1.19.4:4.2" % G3) if loader == "fabric" \
            else ("%s:geckolib-forge-1.20.1:4.4.9" % G3)
    if mc in ("1.20", "1.20.1", "1.20.2", "1.20.3", "1.20.4", "1.20.5", "1.20.6"):
        if loader == "neoforge":
            return "%s:geckolib-neoforge-1.20.2:4.3.1" % G3
        return "%s:geckolib-%s-1.20.1:4.4.9" % (G3, loader)
    return "%s:geckolib-%s-1.21.1:4.7.5" % (G3, loader)
CLOTH_CONFIG_VERSIONS = {
    "1.16.5": "4.17.132",
    "1.17.1": "5.3.63",
    "1.18.1": "6.1.50",
    "1.18.2": "6.5.133",
    "1.19": "7.0.74",
    "1.19.1": "7.0.74",
    "1.19.2": "8.3.134",
    "1.19.3": "9.1.104",
    "1.19.4": "10.1.135",
    "1.20": "10.1.135",
    "1.20.1": "11.1.136",
    "1.20.2": "12.0.137",
    "1.20.3": "13.0.138",
    "1.20.4": "13.0.138",
    "1.20.5": "14.0.139",
    "1.20.6": "14.0.139",
    "1.21": "15.0.140",
    "1.21.1": "16.0.143",
    "1.21.2": "16.0.143",
    "1.21.3": "17.0.144",
    "1.21.4": "17.0.144",
    "1.21.5": "18.0.145",
    "1.21.6": "19.0.147",
    "1.21.7": "19.0.147",
    "1.21.8": "19.0.147",
    "1.21.9": "20.0.149",
    "1.21.10": "20.0.149",
    "1.21.11": "21.11.153",
    "26.1": "26.1.154",
    "26.1.1": "26.1.154",
    "26.1.2": "26.1.154",
    "26.2": "26.2.155",
    "26.3": "26.3.159",
}
LOOM_VERSION = "1.17.493"
LOOM_VERSION_MID = "1.17.493"     # 1.21.6+
LOOM_VERSION_NEW = "1.17.493"     # 26.x

GRADLE_VERSION = "9.8.1"

# ---------------------------------------------------------------------------
# Biomes: 8 groups x 10 = 80.
# (id, display, group, grass, foliage, water, sky, fog, temperature,
#  downfall, category, depth, scale, rarity, weather, ambient_sound, music)
# ---------------------------------------------------------------------------

BIOME_GROUPS = {
    "crystal": {
        "grass": 0x7FE8D8, "foliage": 0x63D4C2, "water": 0x3FDCD2,
        "sky": 0xA8F4FF, "fog": 0xCFF9FF,
        "ambient": "ambient.biomesunseen.crystal_loop",
        "music": "music.biomesunseen.crystal_theme",
        "category": "crystal",
    },
    "ember": {
        "grass": 0xC25A2E, "foliage": 0xA8431F, "water": 0xFF7A3C,
        "sky": 0xFFB37A, "fog": 0xE8875A,
        "ambient": "ambient.biomesunseen.ember_loop",
        "music": "music.biomesunseen.ember_theme",
        "category": "ember",
    },
    "verdant": {
        "grass": 0x52C844, "foliage": 0x2FA83C, "water": 0x2E86C1,
        "sky": 0x87CEEB, "fog": 0xBFE6A8,
        "ambient": "ambient.biomesunseen.verdant_loop",
        "music": "music.biomesunseen.verdant_theme",
        "category": "forest",
    },
    "frost": {
        "grass": 0xA8E6CF, "foliage": 0x8FD8C8, "water": 0x6FB8E8,
        "sky": 0xD6F0FF, "fog": 0xEAF8FF,
        "ambient": "ambient.biomesunseen.frost_loop",
        "music": "music.biomesunseen.frost_theme",
        "category": "frost",
    },
    "storm": {
        "grass": 0x6E7F8A, "foliage": 0x56697A, "water": 0x3E6B8F,
        "sky": 0x7A8FA8, "fog": 0x9AAFC2,
        "ambient": "ambient.biomesunseen.storm_loop",
        "music": "music.biomesunseen.storm_theme",
        "category": "storm",
    },
    "mire": {
        "grass": 0x5C6B3C, "foliage": 0x4A5A30, "water": 0x3C4A2E,
        "sky": 0x8A9A6A, "fog": 0x6E7A52,
        "ambient": "ambient.biomesunseen.mire_loop",
        "music": "music.biomesunseen.mire_theme",
        "category": "mire",
    },
    "sky": {
        "grass": 0x9ADF7A, "foliage": 0x7ACB5E, "water": 0x5EC8FF,
        "sky": 0xB8E8FF, "fog": 0xE0F6FF,
        "ambient": "ambient.biomesunseen.sky_loop",
        "music": "music.biomesunseen.sky_theme",
        "category": "sky",
    },
    "void": {
        "grass": 0x6A4A8A, "foliage": 0x5A3A7A, "water": 0x4A2A6A,
        "sky": 0x2A1A3A, "fog": 0x3A2A4A,
        "ambient": "ambient.biomesunseen.void_loop",
        "music": "music.biomesunseen.void_theme",
        "category": "void",
    },
}

# (id, display, group, depth, scale, temperature, downfall, rarity, weather)
BIOME_ROWS = [
    # -- crystal ------------------------------------------------------------
    ("crystal_spire_reach", "Crystal Spire Reach", "crystal", 1.2, 2.1, 0.6, 0.4, 10, "clear"),
    ("prismarine_hollows", "Prismarine Hollows", "crystal", -0.2, 0.9, 0.7, 0.6, 8, "rain"),
    ("glitterfall_caverns", "Glitterfall Caverns", "crystal", -0.45, 0.6, 0.55, 0.7, 7, "clear"),
    ("quartz_bloom_flats", "Quartz Bloom Flats", "crystal", 0.05, 0.18, 0.75, 0.35, 9, "clear"),
    ("amethystine_ridge", "Amethystine Ridge", "crystal", 1.35, 1.9, 0.35, 0.45, 8, "clear"),
    ("shatterglass_desert", "Shatterglass Desert", "crystal", 0.12, 0.25, 1.25, 0.05, 7, "clear"),
    ("luminous_ledge", "Luminous Ledge", "crystal", 0.85, 1.4, 0.65, 0.5, 7, "clear"),
    ("echo_crystal_grove", "Echo Crystal Grove", "crystal", 0.3, 0.75, 0.6, 0.75, 9, "thunder"),
    ("frost_prism_basin", "Frost Prism Basin", "crystal", -0.15, 0.5, 0.15, 0.65, 6, "snow"),
    ("stained_glass_mesa", "Stained Glass Mesa", "crystal", 0.95, 1.6, 0.9, 0.25, 7, "clear"),
    # -- ember --------------------------------------------------------------
    ("emberite_basin", "Emberite Basin", "ember", -0.1, 0.45, 1.6, 0.0, 8, "clear"),
    ("ashfall_steppe", "Ashfall Steppe", "ember", 0.1, 0.22, 1.35, 0.05, 9, "clear"),
    ("cinder_bloom_fields", "Cinder Bloom Fields", "ember", 0.05, 0.15, 1.2, 0.15, 8, "clear"),
    ("molten_archipelago", "Molten Archipelago", "ember", -0.35, 0.8, 1.8, 0.0, 6, "clear"),
    ("sootveil_wastes", "Sootveil Wastes", "ember", 0.15, 0.3, 1.45, 0.0, 7, "clear"),
    ("pyroclast_ridge", "Pyroclast Ridge", "ember", 1.4, 2.0, 1.5, 0.05, 7, "clear"),
    ("hearthfire_glade", "Hearthfire Glade", "ember", 0.25, 0.55, 0.95, 0.35, 9, "clear"),
    ("scorched_bramble", "Scorched Bramble", "ember", 0.2, 0.5, 1.1, 0.2, 7, "clear"),
    ("obsidian_delta", "Obsidian Delta", "ember", -0.15, 0.35, 1.7, 0.0, 6, "clear"),
    ("magma_vent_garden", "Magma Vent Garden", "ember", -0.3, 0.6, 1.75, 0.0, 6, "thunder"),
    # -- verdant ------------------------------------------------------------
    ("verdant_canopy", "Verdant Canopy", "verdant", 0.35, 0.8, 0.8, 0.85, 10, "rain"),
    ("sylvanite_gardens", "Sylvanite Gardens", "verdant", 0.25, 0.55, 0.75, 0.8, 9, "clear"),
    ("mossbound_hollow", "Mossbound Hollow", "verdant", -0.2, 0.65, 0.7, 0.95, 8, "rain"),
    ("ancient_bough_reach", "Ancient Bough Reach", "verdant", 0.5, 1.0, 0.72, 0.88, 8, "rain"),
    ("petalwind_meadow", "Petalwind Meadow", "verdant", 0.08, 0.12, 0.78, 0.65, 10, "clear"),
    ("rootwoven_tangle", "Rootwoven Tangle", "verdant", 0.15, 0.45, 0.76, 0.92, 7, "rain"),
    ("fernlight_grotto", "Fernlight Grotto", "verdant", -0.3, 0.5, 0.74, 0.98, 7, "rain"),
    ("blooming_thicket", "Blooming Thicket", "verdant", 0.2, 0.4, 0.82, 0.8, 8, "clear"),
    ("emerald_cascade", "Emerald Cascade", "verdant", 1.0, 1.7, 0.65, 0.9, 7, "rain"),
    ("whisperleaf_forest", "Whisperleaf Forest", "verdant", 0.3, 0.7, 0.68, 0.9, 8, "rain"),
    # -- frost --------------------------------------------------------------
    ("froststeel_tundra", "Froststeel Tundra", "frost", 0.1, 0.2, -0.5, 0.5, 9, "snow"),
    ("rimeveil_peaks", "Rimeveil Peaks", "frost", 1.5, 2.2, -0.45, 0.55, 8, "snow"),
    ("silent_snowfield", "Silent Snowfield", "frost", 0.05, 0.1, -0.6, 0.45, 9, "snow"),
    ("glacial_cathedral", "Glacial Cathedral", "frost", 0.9, 1.8, -0.55, 0.6, 7, "snow"),
    ("hoarfrost_meadow", "Hoarfrost Meadow", "frost", 0.08, 0.15, -0.35, 0.7, 8, "snow"),
    ("boreal_crystal_taiga", "Boreal Crystal Taiga", "frost", 0.35, 0.8, -0.4, 0.65, 8, "snow"),
    ("icebound_mire", "Icebound Mire", "frost", -0.2, 0.35, -0.5, 0.8, 7, "snow"),
    ("polar_glass_shore", "Polar Glass Shore", "frost", 0.0, 0.12, -0.42, 0.55, 7, "snow"),
    ("winter_bloom_garden", "Winter Bloom Garden", "frost", 0.2, 0.4, -0.25, 0.75, 7, "snow"),
    ("frozen_zephyr_hollows", "Frozen Zephyr Hollows", "frost", -0.1, 0.4, -0.48, 0.5, 7, "snow"),
    # -- storm --------------------------------------------------------------
    ("thunderglass_highlands", "Thunderglass Highlands", "storm", 1.1, 1.8, 0.5, 0.7, 8, "thunder"),
    ("stormcall_plateau", "Stormcall Plateau", "storm", 1.25, 1.1, 0.45, 0.8, 8, "thunder"),
    ("windscarred_buttes", "Windscarred Buttes", "storm", 1.35, 1.6, 0.6, 0.25, 7, "clear"),
    ("rainlash_jungle", "Rainlash Jungle", "storm", 0.3, 0.65, 0.95, 0.95, 8, "rain"),
    ("cloudrift_summit", "Cloudrift Summit", "storm", 1.8, 2.4, 0.15, 0.65, 6, "thunder"),
    ("static_bloom_fields", "Static Bloom Fields", "storm", 0.1, 0.2, 0.55, 0.6, 8, "thunder"),
    ("monsoon_delta", "Monsoon Delta", "storm", -0.25, 0.3, 0.85, 1.0, 7, "rain"),
    ("shrieking_winds_expanse", "Shrieking Winds Expanse", "storm", 0.15, 0.3, 0.4, 0.45, 7, "thunder"),
    ("lightningglass_spire", "Lightningglass Spire", "storm", 1.55, 2.3, 0.35, 0.55, 6, "thunder"),
    ("tempest_basin", "Tempest Basin", "storm", -0.05, 0.4, 0.5, 0.9, 7, "thunder"),
    # -- mire ---------------------------------------------------------------
    ("murkiron_bogs", "Murkiron Bogs", "mire", -0.25, 0.3, 0.65, 0.9, 8, "rain"),
    ("peat_hollow_mire", "Peat Hollow Mire", "mire", -0.3, 0.25, 0.6, 0.95, 8, "rain"),
    ("drowned_root_marsh", "Drowned Root Marsh", "mire", -0.28, 0.35, 0.7, 0.92, 7, "rain"),
    ("sporechoked_mire", "Sporechoked Mire", "mire", -0.2, 0.4, 0.75, 1.0, 7, "rain"),
    ("blackwillow_bayou", "Blackwillow Bayou", "mire", -0.15, 0.35, 0.72, 0.95, 7, "rain"),
    ("siltveil_fens", "Siltveil Fens", "mire", -0.18, 0.28, 0.68, 0.98, 8, "rain"),
    ("bog_ember_quagmire", "Bog Ember Quagmire", "mire", -0.32, 0.3, 0.8, 0.9, 6, "rain"),
    ("hollowreed_wetlands", "Hollowreed Wetlands", "mire", -0.1, 0.2, 0.66, 0.9, 8, "rain"),
    ("mire_glass_pools", "Mire Glass Pools", "mire", -0.35, 0.22, 0.7, 0.85, 7, "rain"),
    ("gloomwater_flats", "Gloomwater Flats", "mire", -0.22, 0.18, 0.62, 0.95, 7, "rain"),
    # -- sky ----------------------------------------------------------------
    ("skywisp_expanse", "Skywisp Expanse", "sky", 1.6, 2.5, 0.4, 0.5, 7, "clear"),
    ("skystone_archipelago", "Skystone Archipelago", "sky", 1.2, 2.2, 0.5, 0.55, 8, "clear"),
    ("cloud_bloom_terrace", "Cloud Bloom Terrace", "sky", 1.45, 1.3, 0.55, 0.6, 8, "clear"),
    ("zephyr_gardens", "Zephyr Gardens", "sky", 1.1, 1.1, 0.6, 0.55, 9, "clear"),
    ("highwind_pampas", "Highwind Pampas", "sky", 1.3, 0.9, 0.5, 0.35, 8, "clear"),
    ("aerial_shoals", "Aerial Shoals", "sky", 1.7, 2.6, 0.45, 0.5, 6, "clear"),
    ("sunspire_isles", "Sunspire Isles", "sky", 1.9, 2.8, 0.65, 0.35, 6, "clear"),
    ("floating_reef_haven", "Floating Reef Haven", "sky", 1.55, 2.4, 0.58, 0.6, 7, "clear"),
    ("wind_dancer_plains", "Wind Dancer Plains", "sky", 1.0, 0.7, 0.52, 0.45, 9, "clear"),
    ("horizon_steppe", "Horizon Steppe", "sky", 1.15, 0.8, 0.48, 0.4, 8, "clear"),
    # -- void ---------------------------------------------------------------
    ("voidshard_rifts", "Voidshard Rifts", "void", -0.4, 0.9, 0.3, 0.2, 6, "clear"),
    ("gloomshard_depths", "Gloomshard Depths", "void", -0.55, 0.7, 0.25, 0.25, 6, "clear"),
    ("unseeing_abyss", "Unseeing Abyss", "void", -0.7, 1.1, 0.2, 0.15, 5, "clear"),
    ("whispering_void_barrens", "Whispering Void Barrens", "void", -0.15, 0.35, 0.28, 0.2, 6, "clear"),
    ("nullglass_wastes", "Nullglass Wastes", "void", -0.05, 0.2, 0.32, 0.1, 6, "clear"),
    ("eclipse_shade_realm", "Eclipse Shade Realm", "void", -0.3, 0.6, 0.22, 0.3, 5, "clear"),
    ("starless_hollow", "Starless Hollow", "void", -0.6, 0.8, 0.18, 0.2, 5, "clear"),
    ("riftveil_tundra", "Riftveil Tundra", "void", 0.05, 0.25, -0.2, 0.4, 6, "snow"),
    ("entropy_scars", "Entropy Scars", "void", -0.25, 0.85, 0.26, 0.15, 5, "thunder"),
    ("black_sun_basin", "Black Sun Basin", "void", -0.35, 0.5, 0.35, 0.05, 5, "clear"),
]

assert len(BIOME_ROWS) == 80

# ---------------------------------------------------------------------------
# Ores: 20.  (id, display, color_hex, particle_hex, minY, maxY, vein_size,
#             veins_per_chunk, rarity, biome_group or None, stone_tag,
#             glow, tool_material stats: (durability, mining_level, speed,
#             attack_damage, enchantability), potion_effect, machine_tier)
# ---------------------------------------------------------------------------

ORE_ROWS = [
    ("azurethril", "Azurethril", 0x40E0D0, 0x80FFF0, 40, 90, 7, 6, 1.0, "crystal", "stone", True,
     (820, 3, 8.0, 3.0, 22), "swiftness", 2),
    ("emberite", "Emberite", 0xFF6A00, 0xFFB060, 10, 48, 6, 5, 1.0, "ember", "stone", True,
     (1010, 3, 7.5, 3.5, 15), "fire_resistance", 3),
    ("voidshard", "Voidshard", 0x2A0A3A, 0x9A40D0, 0, 20, 5, 3, 0.7, "void", "deepslate", True,
     (1560, 4, 9.0, 4.0, 18), "invisibility", 3),
    ("glimmer_quartz", "Glimmer Quartz", 0xF0F8FF, 0xFFFFFF, 20, 80, 8, 8, 1.1, None, "stone", True,
     (640, 2, 7.0, 2.5, 26), "night_vision", 1),
    ("sylvanite", "Sylvanite", 0x2E8B57, 0x66FF99, 40, 100, 7, 6, 1.0, "verdant", "stone", False,
     (780, 3, 7.2, 3.0, 24), "regeneration", 2),
    ("froststeel", "Froststeel", 0x87CEEB, 0xC0F0FF, 24, 72, 6, 5, 1.0, "frost", "stone", False,
     (930, 3, 7.8, 3.2, 19), "slowness", 2),
    ("murkiron", "Murkiron", 0x556B2F, 0x88AA55, 0, 40, 9, 7, 1.1, "mire", "stone", False,
     (700, 2, 6.5, 2.8, 21), "poison", 1),
    ("sunstone", "Sunstone", 0xFFD700, 0xFFEE88, 48, 120, 5, 4, 0.9, "sky", "stone", True,
     (1120, 3, 8.2, 3.4, 20), "strength", 2),
    ("moonshard", "Moonshard", 0xB0C4DE, 0xE0EEFF, 60, 150, 4, 3, 0.8, None, "stone", True,
     (1080, 3, 8.0, 3.3, 23), "regeneration", 2),
    ("thunderglass", "Thunderglass", 0xE8E864, 0xFFFFA0, 70, 140, 5, 4, 0.85, "storm", "stone", True,
     (1150, 3, 8.5, 3.1, 25), "swiftness", 2),
    ("crimsonite", "Crimsonite", 0xB22222, 0xFF5555, 5, 45, 6, 5, 1.0, "ember", "stone", False,
     (1250, 4, 8.0, 3.8, 14), "strength", 3),
    ("veridium", "Veridium", 0x008080, 0x40FFD0, 30, 85, 7, 6, 1.0, "verdant", "stone", False,
     (850, 3, 7.4, 3.0, 22), "regeneration", 2),
    ("petrified_amber", "Petrified Amber", 0xFFBF00, 0xFFE066, 30, 70, 6, 5, 0.95, "verdant", "stone", True,
     (720, 2, 6.8, 2.7, 28), "haste", 1),
    ("stelliferrum", "Stelliferrum", 0x1A2A6A, 0x6A8AFF, 0, 12, 3, 2, 0.5, None, "deepslate", True,
     (2100, 4, 10.0, 4.5, 12), "strength", 4),
    ("skystone", "Skystone", 0xB0B8C0, 0xD8E8FF, 90, 200, 8, 6, 1.0, "sky", "stone", False,
     (680, 2, 6.6, 2.6, 20), "levitation", 1),
    ("ashium", "Ashium", 0x696969, 0xA0A0A0, 15, 60, 8, 7, 1.1, "ember", "stone", False,
     (760, 2, 7.0, 2.9, 17), "fire_resistance", 2),
    ("tideglass", "Tideglass", 0x20B2AA, 0x70FFE8, 30, 63, 6, 5, 1.0, None, "stone", True,
     (800, 3, 7.3, 2.9, 24), "water_breathing", 2),
    ("gloomshard", "Gloomshard", 0x1A0022, 0x552277, 0, 30, 5, 4, 0.8, "void", "deepslate", True,
     (1320, 4, 8.6, 3.9, 16), "invisibility", 3),
    ("prismatic_ore", "Prismatic Ore", 0xFF69B4, 0xFFFFFF, 40, 90, 3, 2, 0.45, "crystal", "stone", True,
     (1680, 4, 9.5, 4.2, 30), "regeneration", 4),
    ("hearthstone", "Hearthstone", 0xCD5C5C, 0xFF9A76, 20, 60, 7, 6, 1.05, None, "stone", True,
     (740, 2, 6.9, 2.8, 26), "absorption", 1),
]

assert len(ORE_ROWS) == 20

# ---------------------------------------------------------------------------
# Decorative / biome-palette blocks:  (id, display, color, sound, material)
# ---------------------------------------------------------------------------

DECOR_ROWS = [
    ("crystal_shard_block", "Crystal Shard Block", 0x40E0D0, "glass", "crystal"),
    ("ember_rock", "Ember Rock", 0x8A3A1A, "basalt", "stone"),
    ("verdant_soils", "Verdant Soils", 0x3A7A2A, "grass", "soil"),
    ("frostbloom_ice", "Frostbloom Ice", 0xA8D8F0, "glass", "ice"),
    ("storm_shale", "Storm Shale", 0x5A6A7A, "stone", "stone"),
    ("mire_muck", "Mire Muck", 0x4A5A2A, "mud", "soil"),
    ("skystone_bricks", "Skystone Bricks", 0xB8C4D0, "stone", "stone"),
    ("nullglass", "Nullglass", 0x2A1A3A, "glass", "crystal"),
    ("living_heartwood", "Living Heartwood", 0x6A4A2A, "wood", "wood"),
    ("void_veined_stone", "Void Veined Stone", 0x3A2A4A, "deepslate", "stone"),
    ("glowcap_block", "Glowcap Block", 0xC8A832, "fungus", "plant"),
    ("sunstone_bricks", "Sunstone Bricks", 0xE8C860, "stone", "stone"),
]

assert len(DECOR_ROWS) == 12

# ---------------------------------------------------------------------------
# Plants: (id, display, color, height, potted, flower)
# ---------------------------------------------------------------------------

PLANT_ROWS = [
    ("glitterbloom", "Glitterbloom", 0x9AF0E0, 1, True, True),
    ("ember_petal", "Ember Petal", 0xFF7040, 1, True, True),
    ("whisper_fern", "Whisper Fern", 0x4A9A3A, 2, False, False),
    ("rimebell", "Rimebell", 0xB8E8FF, 1, True, True),
    ("stormvine", "Stormvine", 0x6A8AAA, 3, False, False),
    ("bog_lantern", "Bog Lantern", 0xD8C840, 1, True, True),
    ("sky_puff", "Sky Puff", 0xE8F0FF, 2, False, False),
    ("void_orchid", "Void Orchid", 0x7A4AA0, 1, True, True),
    ("sunpetal", "Sunpetal", 0xFFD040, 1, True, True),
    ("mossblossom", "Mossblossom", 0x8AC860, 1, True, True),
]

assert len(PLANT_ROWS) == 10

# ---------------------------------------------------------------------------
# Structures: 30.  (id, display, group, category, spacing, separation,
#                   rarity, max_distance, has_boss, boss_id, start_pool,
#                   biome_groups (tuple), loot_tier, lore_theme)
# ---------------------------------------------------------------------------

STRUCTURE_ROWS = [
    ("ruined_sanctum", "Ruined Sanctum", "crystal", "ruin", 24, 10, 0.6, 128, False, None, "sanctum_start", ("crystal", "verdant"), 2, "pilgrims"),
    ("crystal_spire_outpost", "Crystal Spire Outpost", "crystal", "tower", 32, 12, 0.55, 160, False, None, "spire_outpost_start", ("crystal",), 3, "spirewardens"),
    ("sunken_archive", "Sunken Archive", "mire", "ruin", 28, 11, 0.5, 144, False, None, "archive_start", ("mire", "frost"), 3, "scholars"),
    ("ember_fortress", "Ember Fortress", "ember", "fortress", 36, 14, 0.5, 192, False, None, "ember_fortress_start", ("ember",), 4, "pyrewrights"),
    ("fungal_cathedral", "Fungal Cathedral", "mire", "temple", 30, 12, 0.55, 160, False, None, "fungal_cathedral_start", ("mire", "verdant"), 3, "myconids"),
    ("skywatch_tower", "Skywatch Tower", "sky", "tower", 26, 10, 0.6, 144, False, None, "skywatch_start", ("sky", "storm"), 3, "skywatchers"),
    ("drowned_mausoleum", "Drowned Mausoleum", "mire", "tomb", 34, 13, 0.45, 176, False, None, "mausoleum_start", ("mire",), 4, "the_drowned_court"),
    ("verdant_circle", "Verdant Circle", "verdant", "shrine", 22, 9, 0.65, 128, False, None, "verdant_circle_start", ("verdant",), 2, "grovekeepers"),
    ("frost_hollow", "Frost Hollow", "frost", "shrine", 24, 10, 0.6, 128, False, None, "frost_hollow_start", ("frost",), 2, "winter_singers"),
    ("storm_observatory", "Storm Observatory", "storm", "tower", 30, 12, 0.5, 160, False, None, "observatory_start", ("storm", "sky"), 3, "stormcallers"),
    ("mire_bog_ruins", "Mire Bog Ruins", "mire", "ruin", 20, 8, 0.7, 112, False, None, "bog_ruins_start", ("mire",), 2, "dredgers"),
    ("whispering_menhir", "Whispering Menhir", "void", "shrine", 26, 10, 0.55, 144, False, None, "menhir_start", ("void", "storm"), 3, "the_unspoken"),
    ("prism_labyrinth", "Prism Labyrinth", "crystal", "dungeon", 34, 13, 0.45, 176, False, None, "labyrinth_start", ("crystal",), 4, "prismwrights"),
    ("void_rift_gate", "Void Rift Gate", "void", "portal", 40, 15, 0.4, 208, False, None, "rift_gate_start", ("void",), 5, "riftwalkers"),
    ("ancient_forge", "Ancient Forge", "ember", "forge", 32, 12, 0.5, 176, False, None, "forge_start", ("ember", "frost"), 4, "the_first_smiths"),
    ("pilgrim_rest", "Pilgrim Rest", "verdant", "house", 16, 7, 0.75, 96, False, None, "pilgrim_rest_start", ("verdant", "sky"), 1, "wayfarers"),
    ("mossbound_keep", "Mossbound Keep", "verdant", "fortress", 34, 13, 0.5, 176, False, None, "keep_start", ("verdant", "mire"), 4, "the_mossbound_order"),
    ("shrieking_winds_shrine", "Shrieking Winds Shrine", "storm", "shrine", 24, 10, 0.6, 128, False, None, "winds_shrine_start", ("storm",), 2, "windbinders"),
    ("obsidian_delta_camp", "Obsidian Delta Camp", "ember", "camp", 18, 8, 0.7, 112, False, None, "delta_camp_start", ("ember",), 2, "ashwalkers"),
    ("treetop_covenant", "Treetop Covenant", "verdant", "temple", 28, 11, 0.55, 160, False, None, "covenant_start", ("verdant", "sky"), 3, "the_canopy_covenant"),
    ("canyon_caravan", "Canyon Caravan", "storm", "camp", 18, 8, 0.7, 112, False, None, "caravan_start", ("storm", "ember"), 2, "the_long_road"),
    ("glitterfall_cave", "Glitterfall Cave", "crystal", "dungeon", 22, 9, 0.6, 128, False, None, "glitterfall_start", ("crystal",), 3, "delvers"),
    ("hollow_bell_tower", "Hollow Bell Tower", "frost", "tower", 26, 10, 0.55, 144, False, None, "bell_tower_start", ("frost", "void"), 3, "the_last_ringers"),
    ("drowned_court", "Drowned Court", "mire", "palace", 38, 14, 0.4, 192, False, None, "drowned_court_start", ("mire",), 5, "the_drowned_court"),
    ("barrow_mounds", "Barrow Mounds", "void", "tomb", 24, 10, 0.6, 128, False, None, "barrow_start", ("void", "mire"), 3, "the_barrow_kings"),
    ("alchemists_spire", "Alchemist's Spire", "crystal", "tower", 30, 12, 0.5, 160, False, None, "alchemist_start", ("crystal", "ember"), 4, "the_crucible_circle"),
    ("cradle_of_roots", "Cradle of Roots", "verdant", "boss_arena", 48, 18, 0.35, 256, True, "heart_of_the_forest", "cradle_start", ("verdant", "mire"), 5, "the_heart_of_the_forest"),
    ("serpents_maw", "Serpent's Maw", "void", "boss_arena", 48, 18, 0.35, 256, True, "void_serpent", "serpent_maw_start", ("void", "sky"), 5, "the_void_serpent"),
    ("eclipse_altar", "Eclipse Altar", "void", "temple", 36, 14, 0.45, 192, False, None, "eclipse_start", ("void", "frost"), 4, "eclipse_cultists"),
    ("lost_ziggurat", "Lost Ziggurat", "sky", "pyramid", 38, 14, 0.4, 192, False, None, "ziggurat_start", ("sky", "verdant"), 5, "the_skyborne_empire"),
]

assert len(STRUCTURE_ROWS) == 30

# ---------------------------------------------------------------------------
# Mobs: 25.  (id, display, category, health, speed, attack, defense, size_w,
#             size_h, behavior tuple, tameable, tradable, pack, herd, flees,
#             terrain_use, biome_groups, spawn_weight, night_only, anims,
#             base_color, glow)
# ---------------------------------------------------------------------------

MOB_ROWS = [
    ("lumox", "Lumox", "creature", 14.0, 0.28, 2.0, 1.0, 0.9, 1.2,
     ("graze", "follow_herd", "tameable"), True, False, False, True, True, False,
     ("crystal", "verdant"), 12, False, ("idle", "walk", "run", "eat", "graze", "sit", "tame"),
     0x7FE8D8, True),
    ("brambleback", "Brambleback", "creature", 28.0, 0.24, 5.0, 4.0, 1.4, 1.6,
     ("tank", "guard_herd", "reflect_damage"), False, False, True, True, False, True,
     ("verdant", "mire"), 9, False, ("idle", "walk", "run", "attack", "bramble_shield", "hurt", "death"),
     0x4A7A2A, False),
    ("siltstrider", "Siltstrider", "creature", 12.0, 0.32, 1.5, 0.5, 0.7, 1.8,
     ("water_walk", "flee", "skitter"), False, False, False, False, True, True,
     ("mire",), 10, False, ("idle", "walk", "run", "skitter", "flee", "hurt", "death"),
     0x6A7A4A, False),
    ("glimmermoth", "Glimmermoth", "creature", 6.0, 0.30, 0.5, 0.0, 0.8, 0.6,
     ("flock", "swarm", "ambient_fly", "attracted_to_light"), False, False, True, True, True, False,
     ("crystal", "verdant"), 14, False, ("idle", "fly", "flutter", "land", "hurt", "death"),
     0x9AF0E0, True),
    ("peat_hopper", "Peat Hopper", "creature", 8.0, 0.33, 1.0, 0.5, 0.6, 0.7,
     ("hop", "flee", "burrow"), False, False, False, False, True, True,
     ("mire", "verdant"), 12, False, ("idle", "walk", "hop", "burrow", "flee", "hurt", "death"),
     0x8A7A3A, False),
    ("ember_calf", "Ember Calf", "creature", 20.0, 0.26, 3.0, 1.5, 1.0, 1.3,
     ("graze", "follow_herd", "fire_immune", "tameable"), True, False, False, True, False, False,
     ("ember",), 10, False, ("idle", "walk", "run", "eat", "ember_burst", "sit", "tame"),
     0xFF6A2A, True),
    ("frost_fawn", "Frost Fawn", "creature", 12.0, 0.34, 1.5, 0.5, 0.7, 1.1,
     ("graze", "follow_herd", "flee", "tameable"), True, False, False, True, True, False,
     ("frost",), 12, False, ("idle", "walk", "run", "graze", "flee", "sit", "tame"),
     0xC8E8FF, False),
    ("murkling", "Murkling", "monster", 16.0, 0.30, 4.0, 1.0, 0.8, 1.0,
     ("pack_tactics", "ambush", "water_affinity"), False, False, True, False, False, True,
     ("mire",), 10, True, ("idle", "walk", "run", "attack", "lurk", "hurt", "death"),
     0x4A5A3A, False),
    ("spore_sprout", "Spore Sprout", "creature", 10.0, 0.22, 0.5, 0.5, 0.7, 0.9,
     ("plant_self", "tameable", "spread_spores"), True, False, False, False, True, False,
     ("mire", "verdant"), 9, False, ("idle", "walk", "bloom", "spore_burst", "sit", "tame"),
     0xC8A832, True),
    ("skywisp", "Skywisp", "creature", 8.0, 0.35, 0.5, 0.0, 0.9, 0.8,
     ("follow_weather", "flock", "ambient_fly"), False, False, True, True, True, False,
     ("sky", "storm"), 12, False, ("idle", "fly", "soar", "glide", "hurt", "death"),
     0xE8F0FF, True),
    ("thunder_ram", "Thunder Ram", "creature", 26.0, 0.30, 6.0, 3.0, 1.1, 1.4,
     ("charge", "pack_tactics", "shock_on_hit"), False, False, True, True, False, True,
     ("storm", "sky"), 8, False, ("idle", "walk", "run", "charge", "headbutt", "hurt", "death"),
     0x6A7A8A, False),
    ("mosshorn", "Mosshorn", "creature", 22.0, 0.25, 3.0, 2.0, 1.2, 1.5,
     ("wander_trade", "graze", "barter"), False, True, False, True, False, False,
     ("verdant", "mire", "frost"), 8, False, ("idle", "walk", "run", "eat", "trade", "graze"),
     0x6A8A4A, False),
    ("cinder_pup", "Cinder Pup", "creature", 14.0, 0.36, 4.0, 1.0, 0.7, 0.8,
     ("pack_tactics", "tameable", "flee_when_alone"), True, False, True, False, True, False,
     ("ember",), 11, False, ("idle", "walk", "run", "attack", "beg", "sit", "tame"),
     0xD85A2A, True),
    ("echo_howler", "Echo Howler", "monster", 24.0, 0.28, 5.0, 2.0, 1.0, 1.5,
     ("call_pack", "intimidate", "pack_tactics"), False, False, True, False, False, True,
     ("void", "storm"), 8, True, ("idle", "walk", "run", "howl", "attack", "hurt", "death"),
     0x3A2A4A, False),
    ("dune_skimmer", "Dune Skimmer", "creature", 10.0, 0.40, 1.5, 0.5, 0.8, 0.7,
     ("flee", "burrow", "swarm_day"), False, False, True, False, True, False,
     ("crystal", "ember"), 10, False, ("idle", "walk", "run", "skitter", "burrow", "hurt", "death"),
     0xE8C88A, False),
    ("tide_caller", "Tide Caller", "creature", 18.0, 0.27, 2.0, 1.5, 0.8, 1.4,
     ("heal_allies", "water_affinity", "tide_pull"), False, False, True, False, False, True,
     ("mire", "storm"), 7, False, ("idle", "walk", "swim", "cast", "heal", "hurt", "death"),
     0x2A8A8A, True),
    ("gloom_stalker", "Gloom Stalker", "monster", 20.0, 0.33, 6.0, 1.5, 0.8, 1.3,
     ("night_hunt", "pack_tactics", "stalk"), False, False, True, False, False, True,
     ("void", "mire"), 9, True, ("idle", "walk", "run", "stalk", "pounce", "attack", "hurt", "death"),
     0x2A1A3A, True),
    ("crystal_hermit", "Crystal Hermit", "creature", 16.0, 0.20, 2.0, 5.0, 1.0, 1.1,
     ("fortify", "terrain_use", "shell"), False, False, False, False, True, True,
     ("crystal",), 8, False, ("idle", "walk", "shell", "fortify", "hurt", "death"),
     0x40C0C0, True),
    ("wind_dancer", "Wind Dancer", "creature", 7.0, 0.38, 0.5, 0.0, 0.9, 0.7,
     ("flock", "dance", "ambient_fly"), False, False, True, True, True, False,
     ("sky",), 13, False, ("idle", "fly", "dance", "glide", "hurt", "death"),
     0xB8E8FF, False),
    ("mire_golem", "Mire Golem", "creature", 40.0, 0.18, 7.0, 6.0, 1.6, 2.2,
     ("terrain_use", "build_mounds", "tank"), False, False, False, False, False, True,
     ("mire",), 5, False, ("idle", "walk", "attack", "slam", "build", "hurt", "death"),
     0x5A6A3A, False),
    ("lantern_fox", "Lantern Fox", "creature", 12.0, 0.37, 3.0, 0.5, 0.6, 0.7,
     ("tameable", "light_aura", "flee", "fetch"), True, False, False, False, True, False,
     ("verdant", "frost", "sky"), 11, True, ("idle", "walk", "run", "pounce", "beg", "sit", "tame"),
     0xFFD08A, True),
    ("reef_grazer", "Reef Grazer", "creature", 18.0, 0.24, 1.5, 2.0, 1.3, 1.0,
     ("water_herd", "graze", "follow_herd"), False, False, False, True, True, False,
     ("mire", "crystal"), 9, False, ("idle", "swim", "walk", "graze", "hurt", "death"),
     0x3AAAB0, False),
    ("ash_crawler", "Ash Crawler", "monster", 9.0, 0.31, 3.0, 1.0, 0.6, 0.5,
     ("swarm", "pack_tactics", "burrow"), False, False, True, False, False, True,
     ("ember",), 11, False, ("idle", "walk", "run", "attack", "burrow", "hurt", "death"),
     0x6A3A2A, False),
    ("star_whale", "Star Whale", "creature", 60.0, 0.16, 2.0, 8.0, 3.5, 2.8,
     ("ambient_fly", "flock", "gentle_giant", "levitate"), False, False, True, True, False, False,
     ("sky", "void"), 3, False, ("idle", "fly", "swim_air", "pulse", "hurt", "death"),
     0x5A6AA0, True),
    ("petal_wing", "Petal Wing", "creature", 5.0, 0.34, 0.5, 0.0, 0.5, 0.5,
     ("pollinate", "flock", "flee", "attracted_to_flowers"), False, False, True, True, True, False,
     ("verdant", "crystal"), 14, False, ("idle", "fly", "flutter", "pollinate", "hurt", "death"),
     0xFF9AC8, True),
]

assert len(MOB_ROWS) == 25

# ---------------------------------------------------------------------------
# Bosses: 2.
# (id, display, health, speed, attack, size_w, size_h, arena_structure,
#  music, phases, attacks, loot_table, biome_group, color, glow)
# ---------------------------------------------------------------------------

BOSS_ROWS = [
    ("heart_of_the_forest", "The Heart of the Forest", 480.0, 0.24, 12.0, 2.6, 4.2,
     "cradle_of_roots", "music.biomesunseen.boss_heart",
     ("dormant", "awakening", "wrath", "final_bloom"),
     ("root_slam", "spore_cloud", "summon_brambleback", "verdant_beam", "regenerate", "quake_stomp"),
     "bosses/heart_of_the_forest", "verdant", 0x2FA83C, True),
    ("void_serpent", "The Void Serpent", 520.0, 0.36, 14.0, 1.8, 1.8,
     "serpents_maw", "music.biomesunseen.boss_serpent",
     ("coiled", "phasing", "frenzy", "unmaking"),
     ("void_beam", "phase_shift", "tail_sweep", "rift_barrage", "devour", "gravity_well"),
     "bosses/void_serpent", "void", 0x6A2AB0, True),
]

assert len(BOSS_ROWS) == 2

# ---------------------------------------------------------------------------
# Sounds / music registry entries (referenced by assets/biomesunseen/sounds.json)
# ---------------------------------------------------------------------------

SOUND_EVENTS = [
    "ambient.biomesunseen.crystal_loop", "ambient.biomesunseen.ember_loop",
    "ambient.biomesunseen.verdant_loop", "ambient.biomesunseen.frost_loop",
    "ambient.biomesunseen.storm_loop", "ambient.biomesunseen.mire_loop",
    "ambient.biomesunseen.sky_loop", "ambient.biomesunseen.void_loop",
    "music.biomesunseen.crystal_theme", "music.biomesunseen.ember_theme",
    "music.biomesunseen.verdant_theme", "music.biomesunseen.frost_theme",
    "music.biomesunseen.storm_theme", "music.biomesunseen.mire_theme",
    "music.biomesunseen.sky_theme", "music.biomesunseen.void_theme",
    "music.biomesunseen.boss_heart", "music.biomesunseen.boss_serpent",
    "subtitles.biomesunseen.heart_roar", "subtitles.biomesunseen.serpent_hiss",
    "entity.biomesunseen.lumox.ambient", "entity.biomesunseen.lumox.hurt",
    "entity.biomesunseen.lumox.death", "entity.biomesunseen.heart_of_the_forest.ambient",
    "entity.biomesunseen.heart_of_the_forest.hurt", "entity.biomesunseen.heart_of_the_forest.death",
    "entity.biomesunseen.void_serpent.ambient", "entity.biomesunseen.void_serpent.hurt",
    "entity.biomesunseen.void_serpent.death",
    "block.biomesunseen.ore_chime", "block.biomesunseen.crystal_resonate",
    "block.biomesunseen.mire_step", "block.biomesunseen.ember_crackle",
]

PARTICLE_TYPES = [
    "crystal_spark", "ember_flake", "void_mote", "spore_drift",
    "frost_mote", "storm_arc", "petal_burst", "heal_glow",
]

# ---------------------------------------------------------------------------
# Config schema.  (key, type, default, comment)
# ---------------------------------------------------------------------------

CONFIG_ROWS = [
    ("biomeRarityMultiplier", "double", "1.0", "Global multiplier applied to every custom biome's rarity weight."),
    ("biomeTerraformingStrength", "double", "1.0", "Scales custom terrain depth/score values. 0 disables custom shapes."),
    ("enableAllBiomes", "boolean", "true", "Master toggle for the 80 custom biomes."),
    ("enableAllOres", "boolean", "true", "Master toggle for the 20 custom ores."),
    ("enableAllStructures", "boolean", "true", "Master toggle for the 30 custom structures."),
    ("enableAllMobs", "boolean", "true", "Master toggle for the 25 custom mobs."),
    ("enableBosses", "boolean", "true", "Master toggle for the 2 boss encounters."),
    ("oreRateMultiplier", "double", "1.0", "Multiplier applied to ore veins-per-chunk."),
    ("structureSpacingMultiplier", "double", "1.0", "Multiplier applied to structure spacing (higher = rarer)."),
    ("mobSpawnMultiplier", "double", "1.0", "Multiplier applied to all custom mob spawn weights."),
    ("mobGlobalCap", "int", "180", "Hard cap on custom mobs per world tick window."),
    ("entityAiThrottle", "int", "2", "AI think-interval in ticks for custom mobs (higher = cheaper)."),
    ("ambientParticleDensity", "double", "1.0", "Density multiplier for biome ambient particles."),
    ("structureLodDistance", "int", "128", "Chunk radius within which structure starts are fully resolved."),
    ("musicFrequencyMultiplier", "double", "1.0", "Multiplier for custom biome music delay."),
    ("weatherIntensity", "double", "1.0", "Intensity of custom biome weather (rain/thunder chance)."),
    ("enableLoreBooks", "boolean", "true", "Spawn lore books, journals and murals in structures."),
    ("enableAdaptiveMobs", "boolean", "true", "Allow environmental adaptation behaviours."),
    ("enablePackTactics", "boolean", "true", "Allow pack/coordinated mob tactics."),
    ("enableStructureLoot", "boolean", "true", "Generate structure loot chests."),
]

# ---------------------------------------------------------------------------
# Advancements (JSON generated from this)
# ---------------------------------------------------------------------------

ADVANCEMENT_ROWS = [
    ("root", "Biomes Unseen", "Discover a Biomes Unseen biome", None),
    ("biome_explorer", "Unseen Explorer", "Discover 10 Biomes Unseen biomes", "root"),
    ("biome_master", "Beyond the Veil", "Discover all 80 Biomes Unseen biomes", "biome_explorer"),
    ("first_ore", "Hidden Riches", "Mine any Biomes Unseen ore", "root"),
    ("all_ores", "Mineral Majesty", "Mine all 20 Biomes Unseen ores", "first_ore"),
    ("first_structure", "Built by Unseen Hands", "Enter a Biomes Unseen structure", "root"),
    ("all_structures", "Cartographer of Shadows", "Enter all 30 Biomes Unseen structures", "first_structure"),
    ("heart_of_the_forest", "Heart of the Forest", "Defeat The Heart of the Forest", "first_structure"),
    ("void_serpent", "The Void Serpent", "Defeat The Void Serpent", "first_structure"),
    ("tame_mob", "A Bond Unseen", "Tame a Biomes Unseen creature", "root"),
    ("all_mobs", "Menagerie of the Unseen", "Encounter all 25 Biomes Unseen mobs", "tame_mob"),
    ("boss_hunter", "Unseen Slayer", "Defeat both bosses", "heart_of_the_forest"),
]

# ===========================================================================
# Expansion pack: three full dimensions (Part B / Part C scope).
#
# The tables below are the single source of truth for the dimension content.
# Every emitter imports the combined ALL_* views so each of the 66 modules
# ships exactly the same catalog.
# ===========================================================================

# ---------------------------------------------------------------------------
# Dimension groups (biome palettes, ambience and music per dimension).
# ---------------------------------------------------------------------------

DIMENSION_GROUPS = {
    "hollow_deep": {
        "grass": 0x2A6A5A, "foliage": 0x1E5A4A, "water": 0x2E6A7A,
        "sky": 0x05070C, "fog": 0x14231F,
        "ambient": "ambient.biomesunseen.hollow_deep_loop",
        "music": "music.biomesunseen.hollow_deep_theme",
        "category": "hollow_deep",
    },
    "aetherfall": {
        "grass": 0x9AD8FF, "foliage": 0x7AB8E8, "water": 0x8AD8FF,
        "sky": 0x6A4A8A, "fog": 0xC8A8E8,
        "ambient": "ambient.biomesunseen.aetherfall_loop",
        "music": "music.biomesunseen.aetherfall_theme",
        "category": "aetherfall",
    },
    "void_between": {
        "grass": 0x5A2A7A, "foliage": 0x3A1A5A, "water": 0x2A0A4A,
        "sky": 0x08040C, "fog": 0x1A0A22,
        "ambient": "ambient.biomesunseen.void_between_loop",
        "music": "music.biomesunseen.void_between_theme",
        "category": "void_between",
    },
}

BIOME_GROUPS.update(DIMENSION_GROUPS)

# ---------------------------------------------------------------------------
# Dimension definitions.
# frame        - portal frame block (one of the dimension's stones)
# portal       - portal block id
# key          - igniter item dropped by the dimension's key mob
# source_mob   - mob that drops the key
# settings     - vanilla noise settings used by the dimension generator
# effects      - dimension effects id
# ---------------------------------------------------------------------------

DIMENSION_DEFS = [
    {
        "id": "hollow_deep",
        "display": "The Hollow Deep",
        "group": "hollow_deep",
        "frame": "hollowstone",
        "portal": "hollow_deep_portal",
        "key": "hollow_heart_key",
        "source_mob": "glowmoth",
        "settings": "caves",
        "dimension_type": "minecraft:the_nether",
        "fill_biome": "minecraft:lush_caves",
        "key_ore": "lumenshard",
        "effects": "minecraft:the_nether",
        "fixed_time": 18000,
        "has_skylight": False,
        "ambient_light": 0.08,
        "arrival_y": 48,
        "story": "A buried world of living light and patient stone.",
    },
    {
        "id": "aetherfall",
        "display": "Aetherfall",
        "group": "aetherfall",
        "frame": "skyglass",
        "portal": "aetherfall_portal",
        "key": "aetherfall_key",
        "source_mob": "dawnfinch",
        "settings": "floating_islands",
        "dimension_type": "minecraft:overworld",
        "fill_biome": "minecraft:meadow",
        "key_ore": "skyiron",
        "effects": "minecraft:overworld",
        "fixed_time": 13000,
        "has_skylight": True,
        "ambient_light": 0.35,
        "arrival_y": 128,
        "story": "Endless twilight above a sea of clouds.",
    },
    {
        "id": "void_between",
        "display": "The Void Between",
        "group": "void_between",
        "frame": "voidstone",
        "portal": "void_between_portal",
        "key": "void_between_key",
        "source_mob": "glitchling",
        "settings": "overworld",
        "dimension_type": "minecraft:the_end",
        "fill_biome": "minecraft:end_barrens",
        "key_ore": "nullite",
        "effects": "minecraft:the_end",
        "fixed_time": 18000,
        "has_skylight": False,
        "ambient_light": 0.02,
        "arrival_y": 96,
        "story": "The place reality goes to forget itself.",
    },
]

DIMENSION_BY_ID = {d["id"]: d for d in DIMENSION_DEFS}


def dimension_for_biome(biome_id):
    for dim in DIMENSION_DEFS:
        for row in DIM_BIOME_ROWS:
            if row[0] == biome_id:
                return dim["id"]
    return "overworld"


def dimension_for_ore(ore_id):
    for dim in DIMENSION_DEFS:
        for row in DIM_ORE_ROWS:
            if row[0] == ore_id:
                return dim["id"]
    return "overworld"


def dimension_for_mob(mob_id):
    for dim in DIMENSION_DEFS:
        for row in DIM_MOB_ROWS:
            if row[0] == mob_id:
                return dim["id"]
    return "overworld"


def dimension_for_structure(sid):
    for dim in DIMENSION_DEFS:
        for row in DIM_STRUCTURE_ROWS:
            if row[0] == sid:
                return dim["id"]
    return "overworld"


# ---------------------------------------------------------------------------
# 60 dimension biomes: 20 per dimension.
# (id, display, group, depth, scale, temperature, downfall, rarity, weather)
# ---------------------------------------------------------------------------

_HOLLOW_NAMES = [
    ("glowroot_caverns", "Glowroot Caverns"), ("fungal_abyss", "Fungal Abyss"),
    ("crystal_vein_hollows", "Crystal Vein Hollows"), ("emberworm_tunnels", "Emberworm Tunnels"),
    ("sunless_grotto", "Sunless Grotto"), ("mantle_chasm", "Mantle Chasm"),
    ("lantern_mushroom_sea", "Lantern Mushroom Sea"), ("deepstone_spires", "Deepstone Spires"),
    ("echo_lake_depths", "Echo Lake Depths"), ("fossil_rib_catacombs", "Fossil Rib Catacombs"),
    ("magma_siphon_gallery", "Magma Siphon Gallery"), ("pale_mycelium_gardens", "Pale Mycelium Gardens"),
    ("hollowstone_maze", "Hollowstone Maze"), ("voidlight_crevasse", "Voidlight Crevasse"),
    ("buried_temple_depths", "Buried Temple Depths"), ("shimmering_sinkhole", "Shimmering Sinkhole"),
    ("root_tangled_depths", "Root-Tangled Depths"), ("ancient_ossuary", "Ancient Ossuary"),
    ("prismatic_underlake", "Prismatic Underlake"), ("the_first_ember", "The First Ember"),
]
_AETHER_NAMES = [
    ("dawnlit_isle", "Dawnlit Isle"), ("aurora_drift", "Aurora Drift"),
    ("skyglass_archipelago", "Skyglass Archipelago"), ("cloudstep_meadow", "Cloudstep Meadow"),
    ("windward_ridge", "Windward Ridge"), ("twilight_canopy", "Twilight Canopy"),
    ("starfall_hollows", "Starfall Hollows"), ("sunflare_plateau", "Sunflare Plateau"),
    ("moonpetal_gardens", "Moonpetal Gardens"), ("aether_current_spires", "Aether Current Spires"),
    ("floating_ruins_expanse", "Floating Ruins Expanse"), ("halo_shore", "Halo Shore"),
    ("cerulean_skylake", "Cerulean Skylake"), ("thunderhead_reef", "Thunderhead Reef"),
    ("glimmerwind_fields", "Glimmerwind Fields"), ("celestial_terrace", "Celestial Terrace"),
    ("duskveil_cliffs", "Duskveil Cliffs"), ("luminark_shoals", "Luminark Shoals"),
    ("skyforge_isles", "Skyforge Isles"), ("the_last_horizon", "The Last Horizon"),
]
_VOID_NAMES = [
    ("glitchfield_barrens", "Glitchfield Barrens"), ("inverted_woods", "Inverted Woods"),
    ("shardstorm_expanse", "Shardstorm Expanse"), ("null_spire_wastes", "Null Spire Wastes"),
    ("echo_chamber_rifts", "Echo Chamber Rifts"), ("mirrorlake_absurdity", "Mirrorlake Absurdity"),
    ("halfworld_terraces", "Halfworld Terraces"), ("screaming_static_plains", "Screaming Static Plains"),
    ("forgotten_code_caverns", "Forgotten Code Caverns"), ("obsidian_dreamscape", "Obsidian Dreamscape"),
    ("whisper_gallery", "Whisper Gallery"), ("unraveling_meadow", "Unraveling Meadow"),
    ("paradox_dunes", "Paradox Dunes"), ("entropy_gardens", "Entropy Gardens"),
    ("hollow_reflection_sea", "Hollow Reflection Sea"), ("static_bloom_basin", "Static Bloom Basin"),
    ("impossible_stairways", "Impossible Stairways"), ("dreamt_mountains", "Dreamt Mountains"),
    ("the_unwritten", "The Unwritten"), ("edges_of_everything", "Edges of Everything"),
]


def _dim_biome_rows(names, group, base_temp, span, weather_cycle):
    rows = []
    for idx, (bid, display) in enumerate(names):
        depth = round(-0.6 + 0.06 * (idx % 10), 2)
        scale = round(0.22 + 0.09 * ((idx * 3) % 9), 2)
        temp = round(base_temp + span * ((idx % 7) / 6.0 - 0.5), 2)
        downfall = round(0.25 + 0.7 * ((idx * 5) % 10) / 9.0, 2)
        weather = weather_cycle[idx % len(weather_cycle)]
        rarity = 6 + (idx % 6)
        rows.append((bid, display, group, depth, scale, temp, downfall, rarity, weather))
    return rows


DIM_BIOME_ROWS = (
    _dim_biome_rows(_HOLLOW_NAMES, "hollow_deep", 0.45, 0.6, ("clear", "clear", "rain"))
    + _dim_biome_rows(_AETHER_NAMES, "aetherfall", 0.55, 0.5, ("clear", "clear", "thunder"))
    + _dim_biome_rows(_VOID_NAMES, "void_between", 0.3, 0.7, ("clear", "thunder", "clear"))
)

assert len(DIM_BIOME_ROWS) == 60

# ---------------------------------------------------------------------------
# 5 stones per dimension (15 new palette blocks).
# (id, display, color, sound, material)
# ---------------------------------------------------------------------------

DIM_STONE_ROWS = [
    ("hollowstone", "Hollowstone", 0x3A4A44, "deepslate", "stone"),
    ("deepslate_marrow", "Deepslate Marrow", 0x4A3A3A, "stone", "stone"),
    ("glowgabbro", "Glowgabbro", 0x2E5A50, "stone", "stone"),
    ("emberlimestone", "Emberlimestone", 0x6A4A3A, "stone", "stone"),
    ("fossilshale", "Fossilshale", 0x5A5A4A, "stone", "stone"),
    ("skyglass", "Skyglass", 0x9AD8F0, "glass", "crystal"),
    ("cloudstone", "Cloudstone", 0xD8E4F0, "stone", "stone"),
    ("dawnquartzite", "Dawnquartzite", 0xE8D8B8, "stone", "stone"),
    ("windslate", "Windslate", 0x7A9AA8, "stone", "stone"),
    ("starfall_basalt", "Starfall Basalt", 0x4A4A6A, "basalt", "stone"),
    ("voidstone", "Voidstone", 0x2A1A3A, "deepslate", "stone"),
    ("nullslate", "Nullslate", 0x1E1E2A, "stone", "stone"),
    ("paradox_granite", "Paradox Granite", 0x6A3A5A, "stone", "stone"),
    ("echoeslate", "Echoeslate", 0x3A3A5A, "stone", "stone"),
    ("static_breccia", "Static Breccia", 0x5A2A4A, "stone", "stone"),
]

assert len(DIM_STONE_ROWS) == 15

# ---------------------------------------------------------------------------
# 8 dimension ores per dimension (24).
# Same tuple shape as ORE_ROWS.
# ---------------------------------------------------------------------------

DIM_ORE_ROWS = [
    # -- Hollow Deep --------------------------------------------------------
    ("lumenshard", "Lumenshard", 0x80FFD0, 0xC0FFF0, 5, 40, 6, 7, 1.2, "hollow_deep", "stone", True,
     (900, 3, 8.0, 3.2, 24), "night_vision", 2),
    ("deepiron", "Deep Iron", 0x8A7A6A, 0xC8B8A0, 0, 30, 9, 8, 1.2, "hollow_deep", "deepslate", False,
     (860, 3, 7.6, 3.1, 18), "strength", 2),
    ("biolumite", "Biolumite", 0x40E0A0, 0x90FFD0, 8, 48, 5, 6, 1.0, "hollow_deep", "stone", True,
     (980, 3, 8.2, 3.3, 26), "regeneration", 3),
    ("hollow_crystal", "Hollow Crystal", 0xB0A0FF, 0xE0D8FF, 12, 60, 4, 4, 0.8, "hollow_deep", "stone", True,
     (1200, 4, 9.0, 4.0, 28), "levitation", 3),
    ("embercoal", "Embercoal", 0xFF6A30, 0xFFA070, 0, 64, 10, 9, 1.3, "hollow_deep", "stone", True,
     (700, 2, 6.8, 2.6, 15), "fire_resistance", 1),
    ("fungisteel", "Fungisteel", 0x6A8A3A, 0xA0C860, 10, 50, 7, 6, 1.0, "hollow_deep", "stone", False,
     (940, 3, 7.8, 3.2, 22), "poison", 2),
    ("abyss_opal", "Abyss Opal", 0x2A4A8A, 0x5A8AFF, 20, 70, 3, 3, 0.6, "hollow_deep", "deepslate", True,
     (1600, 4, 9.6, 4.3, 30), "water_breathing", 4),
    ("corestone", "Corestone", 0xFF3A2A, 0xFF8070, 0, 16, 2, 2, 0.4, "hollow_deep", "deepslate", True,
     (2400, 4, 10.5, 5.0, 12), "absorption", 4),
    # -- Aetherfall ---------------------------------------------------------
    ("skyiron", "Skyiron", 0xB8C8D8, 0xE0F0FF, 80, 200, 8, 7, 1.1, "aetherfall", "stone", False,
     (880, 3, 7.8, 3.1, 20), "swiftness", 2),
    ("dawnsilver", "Dawnsilver", 0xF0E0A0, 0xFFF0C8, 90, 220, 6, 5, 0.9, "aetherfall", "stone", True,
     (1040, 3, 8.4, 3.4, 26), "regeneration", 3),
    ("windquartz", "Windquartz", 0xC8F0FF, 0xE8FFFF, 70, 180, 7, 6, 1.0, "aetherfall", "stone", True,
     (780, 2, 7.2, 2.8, 24), "levitation", 1),
    ("cloudite", "Cloudite", 0xE8F0FF, 0xFFFFFF, 100, 240, 6, 6, 1.0, "aetherfall", "stone", False,
     (820, 3, 7.4, 2.9, 22), "slow_falling", 2),
    ("sunforged", "Sunforged", 0xFFC040, 0xFFE090, 60, 160, 5, 4, 0.8, "aetherfall", "stone", True,
     (1300, 4, 9.2, 4.0, 24), "strength", 3),
    ("starfall_ore", "Starfall Ore", 0x8A8AFF, 0xC0C0FF, 120, 250, 4, 3, 0.6, "aetherfall", "stone", True,
     (1500, 4, 9.4, 4.2, 30), "night_vision", 3),
    ("aurorite", "Aurorite", 0x60FFC8, 0xA0FFE0, 110, 230, 5, 4, 0.7, "aetherfall", "stone", True,
     (1180, 3, 8.6, 3.6, 28), "absorption", 3),
    ("aetherglass", "Aetherglass", 0xA0D8FF, 0xE0F4FF, 140, 260, 8, 7, 1.0, "aetherfall", "stone", True,
     (760, 2, 7.0, 2.7, 26), "water_breathing", 2),
    # -- The Void Between ---------------------------------------------------
    ("nullite", "Nullite", 0x3A2A4A, 0x7A5A9A, 0, 30, 5, 5, 0.9, "void_between", "deepslate", True,
     (1350, 4, 8.8, 3.9, 18), "invisibility", 3),
    ("glitchstone", "Glitchstone", 0xFF40A0, 0xFF90D0, 10, 50, 6, 6, 1.0, "void_between", "stone", True,
     (1020, 3, 8.4, 3.5, 28), "swiftness", 3),
    ("paradox_shard", "Paradox Shard", 0x40D0FF, 0x90F0FF, 20, 70, 4, 4, 0.7, "void_between", "stone", True,
     (1450, 4, 9.2, 4.1, 30), "levitation", 3),
    ("entropy_crystal", "Entropy Crystal", 0xA040FF, 0xD090FF, 5, 40, 3, 3, 0.55, "void_between", "deepslate", True,
     (1750, 4, 9.8, 4.5, 32), "regeneration", 4),
    ("void_ember", "Void Ember", 0x2A0A3A, 0x6A2A8A, 0, 24, 7, 6, 1.0, "void_between", "deepslate", True,
     (880, 3, 7.6, 3.0, 20), "fire_resistance", 2),
    ("mirrorshard", "Mirrorshard", 0xC0C0D8, 0xF0F0FF, 30, 90, 5, 5, 0.8, "void_between", "stone", True,
     (1100, 3, 8.2, 3.4, 26), "invisibility", 2),
    ("static_ore", "Static Ore", 0xE0E040, 0xFFFF90, 15, 65, 6, 6, 0.9, "void_between", "stone", True,
     (960, 3, 7.8, 3.2, 22), "haste", 2),
    ("finality", "Finality", 0xFFFFFF, 0xFFD0FF, 0, 12, 2, 2, 0.35, "void_between", "deepslate", True,
     (2600, 4, 11.0, 5.5, 10), "absorption", 4),
]

assert len(DIM_ORE_ROWS) == 24

# ---------------------------------------------------------------------------
# 10 dimension mobs per dimension (30).
# Same tuple shape as MOB_ROWS.
# ---------------------------------------------------------------------------

DIM_MOB_ROWS = [
    # (id, display, category, hp, speed, attack, defense, width, height,
    #  behaviors, tame, trade, pack, herd, flees, terrain, biome_groups,
    #  weight, night, anims, color, glow)
    # -- Hollow Deep --------------------------------------------------------
    ("glowmoth", "Glowmoth", "creature", 7.0, 0.34, 0.5, 0.0, 0.8, 0.6,
     ("flock", "ambient_fly", "graze"), True, False, False, True, True, True,
     ("hollow_deep",), 12, False, ("idle", "walk", "fly", "flutter", "graze", "hurt", "death"), 0x80FFD0, True),
    ("tunnel_hound", "Tunnel Hound", "monster", 22.0, 0.32, 5.0, 1.5, 0.9, 1.0,
     ("pack_tactics", "follow_herd"), False, False, True, False, False, False,
     ("hollow_deep",), 10, True, ("idle", "walk", "run", "attack", "pounce", "hurt", "death"), 0x5A6A5A, True),
    ("crystal_beetle", "Crystal Beetle", "creature", 14.0, 0.22, 2.0, 4.0, 0.9, 0.8,
     ("graze", "terrain_use"), False, False, False, False, False, True,
     ("hollow_deep",), 9, False, ("idle", "walk", "graze", "burrow", "hurt", "death"), 0x40C0C0, True),
    ("magma_snail", "Magma Snail", "creature", 18.0, 0.14, 2.0, 3.0, 1.1, 0.9,
     ("graze", "terrain_use"), False, False, False, False, False, True,
     ("hollow_deep",), 9, False, ("idle", "walk", "graze", "slam", "hurt", "death"), 0xFF6A30, True),
    ("echo_bat", "Echo Bat", "creature", 8.0, 0.38, 1.0, 0.0, 0.6, 0.5,
     ("flock", "ambient_fly"), False, False, False, True, True, True,
     ("hollow_deep",), 13, True, ("idle", "fly", "glide", "dive", "hurt", "death"), 0x3A2A4A, False),
    ("root_gnawer", "Root Gnawer", "monster", 16.0, 0.30, 4.0, 1.0, 0.8, 0.7,
     ("pack_tactics", "graze"), False, False, True, True, False, False,
     ("hollow_deep",), 10, False, ("idle", "walk", "run", "attack", "graze", "hurt", "death"), 0x6A4A2A, False),
    ("deep_lurker", "Deep Lurker", "monster", 30.0, 0.26, 7.0, 2.0, 1.3, 1.6,
     ("terrain_use", "pack_tactics"), False, False, False, False, False, True,
     ("hollow_deep",), 6, True, ("idle", "walk", "swim", "attack", "pounce", "hurt", "death"), 0x1E2A3A, True),
    ("lantern_jelly", "Lantern Jelly", "creature", 12.0, 0.20, 1.0, 1.0, 0.9, 0.9,
     ("flock", "terrain_use"), False, False, False, True, True, True,
     ("hollow_deep",), 11, False, ("idle", "swim", "surface", "dive", "hurt", "death"), 0x60FFE0, True),
    ("stoneback", "Stoneback", "creature", 34.0, 0.20, 4.0, 6.0, 1.5, 1.5,
     ("graze", "follow_herd", "pack_tactics"), False, False, True, True, False, False,
     ("hollow_deep",), 7, False, ("idle", "walk", "run", "graze", "headbutt", "hurt", "death"), 0x5A4A3A, False),
    ("mycopath", "Mycopath", "creature", 16.0, 0.24, 2.0, 2.0, 1.0, 1.2,
     ("wander_trade", "barter", "graze"), False, True, False, True, True, False,
     ("hollow_deep",), 8, False, ("idle", "walk", "trade", "offer", "accept", "graze", "hurt", "death"), 0xC8A832, True),
    # -- Aetherfall ---------------------------------------------------------
    ("skyray", "Skyray", "creature", 18.0, 0.36, 3.0, 1.0, 1.4, 0.6,
     ("ambient_fly", "flock"), False, False, False, True, True, True,
     ("aetherfall",), 12, False, ("idle", "fly", "glide", "dive", "hurt", "death"), 0x8AD8FF, True),
    ("cloud_heron", "Cloud Heron", "creature", 14.0, 0.30, 2.0, 0.5, 1.0, 1.4,
     ("ambient_fly", "flock", "graze"), False, False, False, True, True, True,
     ("aetherfall",), 10, False, ("idle", "fly", "glide", "walk", "flee", "hurt", "death"), 0xE8F0FF, False),
    ("zephyr_pup", "Zephyr Pup", "creature", 16.0, 0.35, 3.0, 1.0, 0.8, 0.8,
     ("pack_tactics", "follow_herd"), True, False, True, True, False, False,
     ("aetherfall",), 11, False, ("idle", "walk", "run", "attack", "beg", "sit", "tame", "hurt", "death"), 0xB8E8FF, True),
    ("island_tortoise", "Island Tortoise", "creature", 40.0, 0.14, 3.0, 7.0, 1.8, 1.4,
     ("graze", "follow_herd", "terrain_use"), False, False, False, True, False, True,
     ("aetherfall",), 7, False, ("idle", "walk", "graze", "shell", "hurt", "death"), 0x8A9A6A, False),
    ("dawnfinch", "Dawnfinch", "creature", 6.0, 0.40, 0.5, 0.0, 0.5, 0.5,
     ("flock", "ambient_fly", "graze"), True, False, False, True, True, True,
     ("aetherfall",), 14, False, ("idle", "fly", "flutter", "graze", "sit", "tame", "hurt", "death"), 0xFFD08A, True),
    ("storm_jay", "Storm Jay", "creature", 10.0, 0.42, 2.0, 0.0, 0.7, 0.6,
     ("flock", "ambient_fly"), False, False, False, True, False, True,
     ("aetherfall",), 12, False, ("idle", "fly", "dive", "soar", "hurt", "death"), 0x6A7A8A, False),
    ("summit_ram", "Summit Ram", "creature", 30.0, 0.28, 6.0, 3.0, 1.2, 1.4,
     ("pack_tactics", "follow_herd", "graze"), False, False, True, True, False, False,
     ("aetherfall",), 8, False, ("idle", "walk", "run", "charge", "headbutt", "hurt", "death"), 0xD8E4F0, False),
    ("mistgraz", "Mistgraz", "creature", 22.0, 0.22, 2.0, 2.0, 1.2, 1.2,
     ("graze", "follow_herd"), False, False, False, True, True, False,
     ("aetherfall",), 10, False, ("idle", "walk", "run", "graze", "flee", "hurt", "death"), 0xC8D8E8, False),
    ("star_serpent", "Star Serpent", "monster", 26.0, 0.34, 6.0, 2.0, 1.2, 1.0,
     ("ambient_fly", "pack_tactics"), False, False, False, False, False, True,
     ("aetherfall",), 7, True, ("idle", "fly", "attack", "pounce", "hurt", "death"), 0x8A8AFF, True),
    ("windlark", "Windlark", "creature", 8.0, 0.44, 0.5, 0.0, 0.6, 0.5,
     ("flock", "ambient_fly", "graze"), True, False, False, True, True, True,
     ("aetherfall",), 13, False, ("idle", "fly", "dance", "glide", "sit", "tame", "hurt", "death"), 0xC8F0FF, True),
    # -- The Void Between ---------------------------------------------------
    ("glitchling", "Glitchling", "monster", 10.0, 0.40, 3.0, 0.0, 0.6, 0.6,
     ("pack_tactics", "follow_herd"), False, False, True, True, True, False,
     ("void_between",), 13, False, ("idle", "walk", "run", "attack", "blink", "hurt", "death"), 0xFF40A0, True),
    ("null_stalker", "Null Stalker", "monster", 24.0, 0.34, 6.0, 1.0, 0.9, 1.4,
     ("pack_tactics", "terrain_use"), False, False, False, False, False, True,
     ("void_between",), 9, True, ("idle", "walk", "run", "stalk", "pounce", "attack", "hurt", "death"), 0x1E1E2A, True),
    ("mirror_wisp", "Mirror Wisp", "creature", 8.0, 0.36, 0.5, 0.0, 0.7, 0.7,
     ("ambient_fly", "flock"), False, False, False, True, True, True,
     ("void_between",), 12, False, ("idle", "fly", "glide", "heal", "hurt", "death"), 0xC0C0D8, True),
    ("paradox_beast", "Paradox Beast", "monster", 34.0, 0.26, 8.0, 3.0, 1.4, 1.6,
     ("terrain_use", "pack_tactics"), False, False, False, False, False, True,
     ("void_between",), 6, False, ("idle", "walk", "run", "charge", "slam", "hurt", "death"), 0x6A3A5A, True),
    ("static_crawler", "Static Crawler", "monster", 14.0, 0.33, 4.0, 1.0, 0.7, 0.5,
     ("pack_tactics", "terrain_use"), False, False, True, False, True, True,
     ("void_between",), 11, False, ("idle", "walk", "run", "attack", "burrow", "hurt", "death"), 0xE0E040, True),
    ("dream_eater", "Dream Eater", "monster", 28.0, 0.29, 7.0, 2.0, 1.1, 1.3,
     ("pack_tactics", "graze"), False, False, False, False, False, False,
     ("void_between",), 7, True, ("idle", "walk", "run", "stalk", "attack", "devour", "hurt", "death"), 0x5A2A7A, True),
    ("shardwing", "Shardwing", "creature", 12.0, 0.38, 3.0, 0.5, 0.9, 0.7,
     ("ambient_fly", "flock"), False, False, False, True, True, True,
     ("void_between",), 12, False, ("idle", "fly", "glide", "dive", "hurt", "death"), 0xA0D8FF, True),
    ("inverse_grazer", "Inverse Grazer", "creature", 20.0, 0.22, 2.0, 3.0, 1.2, 1.2,
     ("graze", "follow_herd"), False, False, False, True, True, False,
     ("void_between",), 9, False, ("idle", "walk", "graze", "float", "hurt", "death"), 0x3A1A5A, True),
    ("echo_husk", "Echo Husk", "monster", 20.0, 0.31, 5.0, 2.0, 0.9, 1.5,
     ("pack_tactics", "follow_herd"), False, False, True, True, False, False,
     ("void_between",), 9, False, ("idle", "walk", "run", "howl", "attack", "hurt", "death"), 0x3A3A5A, False),
    ("unravel_spawn", "Unravel Spawn", "creature", 16.0, 0.27, 1.0, 1.0, 1.0, 1.0,
     ("wander_trade", "barter"), False, True, False, False, False, False,
     ("void_between",), 7, False, ("idle", "walk", "trade", "offer", "accept", "blink", "hurt", "death"), 0xFF90D0, True),
]

assert len(DIM_MOB_ROWS) == 30

# ---------------------------------------------------------------------------
# 5 structures per dimension + 3 overworld portal structures.
# Same tuple shape as STRUCTURE_ROWS.
# ---------------------------------------------------------------------------

DIM_STRUCTURE_ROWS = [
    # -- Hollow Deep --------------------------------------------------------
    ("wardens_spire_arena", "Warden's Spire Arena", "hollow_deep", "boss_arena", 48, 18, 0.35, 256,
     True, "warden_of_the_hollow_deep", "warden_spire_start", ("hollow_deep",), 5, "the_warden"),
    ("glowroot_shrine", "Glowroot Shrine", "hollow_deep", "shrine", 22, 9, 0.65, 128,
     False, None, "glowroot_shrine_start", ("hollow_deep",), 2, "rootkeepers"),
    ("fossil_vault", "Fossil Vault", "hollow_deep", "tomb", 26, 10, 0.55, 160,
     False, None, "fossil_vault_start", ("hollow_deep",), 3, "bonecharters"),
    ("ember_siphon", "Ember Siphon", "hollow_deep", "forge", 30, 12, 0.5, 176,
     False, None, "ember_siphon_start", ("hollow_deep",), 4, "siphonwrights"),
    ("mycelium_circle", "Mycelium Circle", "hollow_deep", "shrine", 20, 8, 0.7, 112,
     False, None, "mycelium_circle_start", ("hollow_deep",), 2, "myconids"),
    # -- Aetherfall ---------------------------------------------------------
    ("crowns_eyrie", "Crown's Eyrie", "aetherfall", "boss_arena", 48, 18, 0.35, 256,
     True, "the_skyward_crown", "crowns_eyrie_start", ("aetherfall",), 5, "the_crown"),
    ("skyglass_temple", "Skyglass Temple", "aetherfall", "temple", 24, 10, 0.6, 144,
     False, None, "skyglass_temple_start", ("aetherfall",), 3, "glasspriests"),
    ("windward_beacon", "Windward Beacon", "aetherfall", "tower", 28, 11, 0.55, 160,
     False, None, "windward_beacon_start", ("aetherfall",), 3, "beaconkeepers"),
    ("starfall_observatory", "Starfall Observatory", "aetherfall", "tower", 30, 12, 0.5, 176,
     False, None, "starfall_observatory_start", ("aetherfall",), 4, "starwatchers"),
    ("halo_gatehouse", "Halo Gatehouse", "aetherfall", "ruin", 22, 9, 0.65, 128,
     False, None, "halo_gatehouse_start", ("aetherfall",), 2, "gatekeepers"),
    # -- The Void Between ---------------------------------------------------
    ("unraveling_nexus", "Unraveling Nexus", "void_between", "boss_arena", 48, 18, 0.35, 256,
     True, "the_unraveling", "unraveling_nexus_start", ("void_between",), 5, "the_unraveling"),
    ("paradox_arch", "Paradox Arch", "void_between", "ruin", 22, 9, 0.65, 128,
     False, None, "paradox_arch_start", ("void_between",), 3, "archivists"),
    ("mirror_vault", "Mirror Vault", "void_between", "dungeon", 26, 10, 0.55, 160,
     False, None, "mirror_vault_start", ("void_between",), 4, "mirrorkeepers"),
    ("static_ziggurat", "Static Ziggurat", "void_between", "pyramid", 32, 12, 0.5, 176,
     False, None, "static_ziggurat_start", ("void_between",), 4, "static_priests"),
    ("forgotten_library", "Forgotten Library", "void_between", "ruin", 28, 11, 0.55, 160,
     False, None, "forgotten_library_start", ("void_between",), 4, "the_unwritten"),
]

assert len(DIM_STRUCTURE_ROWS) == 15

# Overworld portal sites: a pre-built frame for each dimension so the portal is
# reachable without prior knowledge of the recipe.  The key item still has to
# be earned from the dimension's mob (a closed loop: the site shows where to go,
# the key opens it).
PORTAL_STRUCTURE_ROWS = [
    ("hollow_deep_gate", "Hollow Deep Gate", "verdant", "portal", 40, 15, 0.4, 208,
     False, None, "hollow_deep_gate_start", ("verdant", "mire"), 3, "gatekeepers"),
    ("aetherfall_gate", "Aetherfall Gate", "sky", "portal", 40, 15, 0.4, 208,
     False, None, "aetherfall_gate_start", ("sky", "storm"), 3, "gatekeepers"),
    ("void_between_gate", "Void Between Gate", "void", "portal", 40, 15, 0.4, 208,
     False, None, "void_between_gate_start", ("void",), 4, "gatekeepers"),
]

assert len(PORTAL_STRUCTURE_ROWS) == 3

# ---------------------------------------------------------------------------
# 3 dimension bosses (5 total with the two overworld bosses).
# Same tuple shape as BOSS_ROWS.
# ---------------------------------------------------------------------------

DIM_BOSS_ROWS = [
    ("warden_of_the_hollow_deep", "Warden of the Hollow Deep", 620.0, 0.22, 16.0, 3.2, 5.0,
     "wardens_spire_arena", "music.biomesunseen.boss_warden",
     ("buried", "awakens", "spire_risen", "collapse"),
     ("slam", "tremor_wave", "tunnel_ambush", "spire_rise", "hollow_beam", "summon_glowmoth"),
     "bosses/warden_of_the_hollow_deep", "hollow_deep", 0x2A8A6A, True),
    ("the_skyward_crown", "The Skyward Crown", 560.0, 0.34, 14.0, 2.4, 3.8,
     "crowns_eyrie", "music.biomesunseen.boss_crown",
     ("descending", "haloed", "shardfall", "last_light"),
     ("aerial_dive", "gust_knockback", "sunbeam", "shard_split", "orbit_shards", "summon_dawnfinch"),
     "bosses/the_skyward_crown", "aetherfall", 0xFFD060, True),
    ("the_unraveling", "The Unraveling", 700.0, 0.30, 18.0, 2.8, 4.0,
     "unraveling_nexus", "music.biomesunseen.boss_unraveling",
     ("quadruped", "serpent", "humanoid", "unmade"),
     ("glitch_lunge", "rift_crawl", "reality_tear", "form_shift", "entropy_wave", "static_barrage"),
     "bosses/the_unraveling", "void_between", 0xFF40A0, True),
]

assert len(DIM_BOSS_ROWS) == 3

# ---------------------------------------------------------------------------
# Combined catalog views.  Every emitter works from these so a target can
# never ship a partial catalog.
# ---------------------------------------------------------------------------

ALL_BIOME_ROWS = BIOME_ROWS + DIM_BIOME_ROWS
ALL_ORE_ROWS = ORE_ROWS + DIM_ORE_ROWS
# Portal blocks are ordinary blocks with a glass-like look; the journey itself
# is driven by the dimension key item (see PORTAL_ROWS / UnseenTravel).
PORTAL_BLOCK_ROWS = [
    ("hollow_deep_portal", "Hollow Deep Portal", 0x2A8A6A, "glass", "glass"),
    ("aetherfall_portal", "Aetherfall Portal", 0x9AD8F0, "glass", "glass"),
    ("void_between_portal", "Void Between Portal", 0x5A2A7A, "glass", "glass"),
]

ALL_DECOR_ROWS = DECOR_ROWS + DIM_STONE_ROWS + PORTAL_BLOCK_ROWS
ALL_PLANT_ROWS = list(PLANT_ROWS)
ALL_STRUCTURE_ROWS = STRUCTURE_ROWS + DIM_STRUCTURE_ROWS + PORTAL_STRUCTURE_ROWS
ALL_MOB_ROWS = MOB_ROWS + DIM_MOB_ROWS
ALL_BOSS_ROWS = BOSS_ROWS + DIM_BOSS_ROWS

assert len(ALL_BIOME_ROWS) == 140
assert len(ALL_ORE_ROWS) == 44
assert len(ALL_DECOR_ROWS) == 30
assert len(ALL_STRUCTURE_ROWS) == 48
assert len(ALL_MOB_ROWS) == 55
assert len(ALL_BOSS_ROWS) == 5

# ---------------------------------------------------------------------------
# Portal catalog.
# ---------------------------------------------------------------------------

PORTAL_ROWS = [
    (d["id"], d["display"], d["frame"], d["portal"], d["key"],
     d["source_mob"], d["arrival_y"])
    for d in DIMENSION_DEFS
]

# ---------------------------------------------------------------------------
# Extra sound events: dimension ambience/music and per-phase boss tracks.
# ---------------------------------------------------------------------------

for _d in DIMENSION_DEFS:
    SOUND_EVENTS.append(_d["ambient"] if False else "ambient.biomesunseen.%s_loop" % _d["id"])
    SOUND_EVENTS.append("music.biomesunseen.%s_theme" % _d["id"])
    SOUND_EVENTS.append("entity.biomesunseen.%s.ambient" % _d["source_mob"])

for _b in BOSS_ROWS + DIM_BOSS_ROWS:
    for _phase in range(1, 5):
        SOUND_EVENTS.append("music.biomesunseen.%s_phase%d" % (_b[0], _phase))

SOUND_EVENTS = list(dict.fromkeys(SOUND_EVENTS))

# Extra particle types used by the new dimensions.
PARTICLE_TYPES.extend(["hollow_mote", "aurora_dust", "glitch_spark"])

# ---------------------------------------------------------------------------
# Advancements for the new dimensions and bosses.
# ---------------------------------------------------------------------------

ADVANCEMENT_ROWS.extend([
    ("enter_hollow_deep", "Into the Hollow Deep", "Enter The Hollow Deep", "root"),
    ("enter_aetherfall", "Above the Clouds", "Enter Aetherfall", "root"),
    ("enter_void_between", "Between Everything", "Enter The Void Between", "root"),
    ("warden_of_the_hollow_deep", "The Warden Falls", "Defeat the Warden of the Hollow Deep", "enter_hollow_deep"),
    ("the_skyward_crown", "Crownbreaker", "Defeat The Skyward Crown", "enter_aetherfall"),
    ("the_unraveling", "Unmade", "Defeat The Unraveling", "enter_void_between"),
    ("boss_master", "Warden of Five", "Defeat all five bosses", "boss_hunter"),
])
