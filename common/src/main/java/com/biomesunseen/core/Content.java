package com.biomesunseen.core;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The complete Biomes Unseen content catalog: 80 biomes, 20 ores, 12 palette
 * blocks, 10 plants, 30 structures, 25 mobs and 2 bosses.  Pure Java so every
 * version family can read the exact same definitions.
 */
public final class Content {

    public static final List<BiomeDef> BIOMES = Collections.unmodifiableList(Arrays.asList(new BiomeDef[]{
        new BiomeDef("crystal_spire_reach", "Crystal Spire Reach", "crystal", 0x7FE8D8, 0x63D4C2, 0x3FDCD2, 0xA8F4FF, 0xCFF9FF, 0.6, 0.4, "crystal", 1.2, 2.1, 10, "clear", "ambient.biomesunseen.crystal_loop", "music.biomesunseen.crystal_theme"),
        new BiomeDef("prismarine_hollows", "Prismarine Hollows", "crystal", 0x7FE8D8, 0x63D4C2, 0x3FDCD2, 0xA8F4FF, 0xCFF9FF, 0.7, 0.6, "crystal", -0.2, 0.9, 8, "rain", "ambient.biomesunseen.crystal_loop", "music.biomesunseen.crystal_theme"),
        new BiomeDef("glitterfall_caverns", "Glitterfall Caverns", "crystal", 0x7FE8D8, 0x63D4C2, 0x3FDCD2, 0xA8F4FF, 0xCFF9FF, 0.55, 0.7, "crystal", -0.45, 0.6, 7, "clear", "ambient.biomesunseen.crystal_loop", "music.biomesunseen.crystal_theme"),
        new BiomeDef("quartz_bloom_flats", "Quartz Bloom Flats", "crystal", 0x7FE8D8, 0x63D4C2, 0x3FDCD2, 0xA8F4FF, 0xCFF9FF, 0.75, 0.35, "crystal", 0.05, 0.18, 9, "clear", "ambient.biomesunseen.crystal_loop", "music.biomesunseen.crystal_theme"),
        new BiomeDef("amethystine_ridge", "Amethystine Ridge", "crystal", 0x7FE8D8, 0x63D4C2, 0x3FDCD2, 0xA8F4FF, 0xCFF9FF, 0.35, 0.45, "crystal", 1.35, 1.9, 8, "clear", "ambient.biomesunseen.crystal_loop", "music.biomesunseen.crystal_theme"),
        new BiomeDef("shatterglass_desert", "Shatterglass Desert", "crystal", 0x7FE8D8, 0x63D4C2, 0x3FDCD2, 0xA8F4FF, 0xCFF9FF, 1.25, 0.05, "crystal", 0.12, 0.25, 7, "clear", "ambient.biomesunseen.crystal_loop", "music.biomesunseen.crystal_theme"),
        new BiomeDef("luminous_ledge", "Luminous Ledge", "crystal", 0x7FE8D8, 0x63D4C2, 0x3FDCD2, 0xA8F4FF, 0xCFF9FF, 0.65, 0.5, "crystal", 0.85, 1.4, 7, "clear", "ambient.biomesunseen.crystal_loop", "music.biomesunseen.crystal_theme"),
        new BiomeDef("echo_crystal_grove", "Echo Crystal Grove", "crystal", 0x7FE8D8, 0x63D4C2, 0x3FDCD2, 0xA8F4FF, 0xCFF9FF, 0.6, 0.75, "crystal", 0.3, 0.75, 9, "thunder", "ambient.biomesunseen.crystal_loop", "music.biomesunseen.crystal_theme"),
        new BiomeDef("frost_prism_basin", "Frost Prism Basin", "crystal", 0x7FE8D8, 0x63D4C2, 0x3FDCD2, 0xA8F4FF, 0xCFF9FF, 0.15, 0.65, "crystal", -0.15, 0.5, 6, "snow", "ambient.biomesunseen.crystal_loop", "music.biomesunseen.crystal_theme"),
        new BiomeDef("stained_glass_mesa", "Stained Glass Mesa", "crystal", 0x7FE8D8, 0x63D4C2, 0x3FDCD2, 0xA8F4FF, 0xCFF9FF, 0.9, 0.25, "crystal", 0.95, 1.6, 7, "clear", "ambient.biomesunseen.crystal_loop", "music.biomesunseen.crystal_theme"),
        new BiomeDef("emberite_basin", "Emberite Basin", "ember", 0xC25A2E, 0xA8431F, 0xFF7A3C, 0xFFB37A, 0xE8875A, 1.6, 0, "ember", -0.1, 0.45, 8, "clear", "ambient.biomesunseen.ember_loop", "music.biomesunseen.ember_theme"),
        new BiomeDef("ashfall_steppe", "Ashfall Steppe", "ember", 0xC25A2E, 0xA8431F, 0xFF7A3C, 0xFFB37A, 0xE8875A, 1.35, 0.05, "ember", 0.1, 0.22, 9, "clear", "ambient.biomesunseen.ember_loop", "music.biomesunseen.ember_theme"),
        new BiomeDef("cinder_bloom_fields", "Cinder Bloom Fields", "ember", 0xC25A2E, 0xA8431F, 0xFF7A3C, 0xFFB37A, 0xE8875A, 1.2, 0.15, "ember", 0.05, 0.15, 8, "clear", "ambient.biomesunseen.ember_loop", "music.biomesunseen.ember_theme"),
        new BiomeDef("molten_archipelago", "Molten Archipelago", "ember", 0xC25A2E, 0xA8431F, 0xFF7A3C, 0xFFB37A, 0xE8875A, 1.8, 0, "ember", -0.35, 0.8, 6, "clear", "ambient.biomesunseen.ember_loop", "music.biomesunseen.ember_theme"),
        new BiomeDef("sootveil_wastes", "Sootveil Wastes", "ember", 0xC25A2E, 0xA8431F, 0xFF7A3C, 0xFFB37A, 0xE8875A, 1.45, 0, "ember", 0.15, 0.3, 7, "clear", "ambient.biomesunseen.ember_loop", "music.biomesunseen.ember_theme"),
        new BiomeDef("pyroclast_ridge", "Pyroclast Ridge", "ember", 0xC25A2E, 0xA8431F, 0xFF7A3C, 0xFFB37A, 0xE8875A, 1.5, 0.05, "ember", 1.4, 2, 7, "clear", "ambient.biomesunseen.ember_loop", "music.biomesunseen.ember_theme"),
        new BiomeDef("hearthfire_glade", "Hearthfire Glade", "ember", 0xC25A2E, 0xA8431F, 0xFF7A3C, 0xFFB37A, 0xE8875A, 0.95, 0.35, "ember", 0.25, 0.55, 9, "clear", "ambient.biomesunseen.ember_loop", "music.biomesunseen.ember_theme"),
        new BiomeDef("scorched_bramble", "Scorched Bramble", "ember", 0xC25A2E, 0xA8431F, 0xFF7A3C, 0xFFB37A, 0xE8875A, 1.1, 0.2, "ember", 0.2, 0.5, 7, "clear", "ambient.biomesunseen.ember_loop", "music.biomesunseen.ember_theme"),
        new BiomeDef("obsidian_delta", "Obsidian Delta", "ember", 0xC25A2E, 0xA8431F, 0xFF7A3C, 0xFFB37A, 0xE8875A, 1.7, 0, "ember", -0.15, 0.35, 6, "clear", "ambient.biomesunseen.ember_loop", "music.biomesunseen.ember_theme"),
        new BiomeDef("magma_vent_garden", "Magma Vent Garden", "ember", 0xC25A2E, 0xA8431F, 0xFF7A3C, 0xFFB37A, 0xE8875A, 1.75, 0, "ember", -0.3, 0.6, 6, "thunder", "ambient.biomesunseen.ember_loop", "music.biomesunseen.ember_theme"),
        new BiomeDef("verdant_canopy", "Verdant Canopy", "verdant", 0x52C844, 0x2FA83C, 0x2E86C1, 0x87CEEB, 0xBFE6A8, 0.8, 0.85, "forest", 0.35, 0.8, 10, "rain", "ambient.biomesunseen.verdant_loop", "music.biomesunseen.verdant_theme"),
        new BiomeDef("sylvanite_gardens", "Sylvanite Gardens", "verdant", 0x52C844, 0x2FA83C, 0x2E86C1, 0x87CEEB, 0xBFE6A8, 0.75, 0.8, "forest", 0.25, 0.55, 9, "clear", "ambient.biomesunseen.verdant_loop", "music.biomesunseen.verdant_theme"),
        new BiomeDef("mossbound_hollow", "Mossbound Hollow", "verdant", 0x52C844, 0x2FA83C, 0x2E86C1, 0x87CEEB, 0xBFE6A8, 0.7, 0.95, "forest", -0.2, 0.65, 8, "rain", "ambient.biomesunseen.verdant_loop", "music.biomesunseen.verdant_theme"),
        new BiomeDef("ancient_bough_reach", "Ancient Bough Reach", "verdant", 0x52C844, 0x2FA83C, 0x2E86C1, 0x87CEEB, 0xBFE6A8, 0.72, 0.88, "forest", 0.5, 1, 8, "rain", "ambient.biomesunseen.verdant_loop", "music.biomesunseen.verdant_theme"),
        new BiomeDef("petalwind_meadow", "Petalwind Meadow", "verdant", 0x52C844, 0x2FA83C, 0x2E86C1, 0x87CEEB, 0xBFE6A8, 0.78, 0.65, "forest", 0.08, 0.12, 10, "clear", "ambient.biomesunseen.verdant_loop", "music.biomesunseen.verdant_theme"),
        new BiomeDef("rootwoven_tangle", "Rootwoven Tangle", "verdant", 0x52C844, 0x2FA83C, 0x2E86C1, 0x87CEEB, 0xBFE6A8, 0.76, 0.92, "forest", 0.15, 0.45, 7, "rain", "ambient.biomesunseen.verdant_loop", "music.biomesunseen.verdant_theme"),
        new BiomeDef("fernlight_grotto", "Fernlight Grotto", "verdant", 0x52C844, 0x2FA83C, 0x2E86C1, 0x87CEEB, 0xBFE6A8, 0.74, 0.98, "forest", -0.3, 0.5, 7, "rain", "ambient.biomesunseen.verdant_loop", "music.biomesunseen.verdant_theme"),
        new BiomeDef("blooming_thicket", "Blooming Thicket", "verdant", 0x52C844, 0x2FA83C, 0x2E86C1, 0x87CEEB, 0xBFE6A8, 0.82, 0.8, "forest", 0.2, 0.4, 8, "clear", "ambient.biomesunseen.verdant_loop", "music.biomesunseen.verdant_theme"),
        new BiomeDef("emerald_cascade", "Emerald Cascade", "verdant", 0x52C844, 0x2FA83C, 0x2E86C1, 0x87CEEB, 0xBFE6A8, 0.65, 0.9, "forest", 1, 1.7, 7, "rain", "ambient.biomesunseen.verdant_loop", "music.biomesunseen.verdant_theme"),
        new BiomeDef("whisperleaf_forest", "Whisperleaf Forest", "verdant", 0x52C844, 0x2FA83C, 0x2E86C1, 0x87CEEB, 0xBFE6A8, 0.68, 0.9, "forest", 0.3, 0.7, 8, "rain", "ambient.biomesunseen.verdant_loop", "music.biomesunseen.verdant_theme"),
        new BiomeDef("froststeel_tundra", "Froststeel Tundra", "frost", 0xA8E6CF, 0x8FD8C8, 0x6FB8E8, 0xD6F0FF, 0xEAF8FF, -0.5, 0.5, "frost", 0.1, 0.2, 9, "snow", "ambient.biomesunseen.frost_loop", "music.biomesunseen.frost_theme"),
        new BiomeDef("rimeveil_peaks", "Rimeveil Peaks", "frost", 0xA8E6CF, 0x8FD8C8, 0x6FB8E8, 0xD6F0FF, 0xEAF8FF, -0.45, 0.55, "frost", 1.5, 2.2, 8, "snow", "ambient.biomesunseen.frost_loop", "music.biomesunseen.frost_theme"),
        new BiomeDef("silent_snowfield", "Silent Snowfield", "frost", 0xA8E6CF, 0x8FD8C8, 0x6FB8E8, 0xD6F0FF, 0xEAF8FF, -0.6, 0.45, "frost", 0.05, 0.1, 9, "snow", "ambient.biomesunseen.frost_loop", "music.biomesunseen.frost_theme"),
        new BiomeDef("glacial_cathedral", "Glacial Cathedral", "frost", 0xA8E6CF, 0x8FD8C8, 0x6FB8E8, 0xD6F0FF, 0xEAF8FF, -0.55, 0.6, "frost", 0.9, 1.8, 7, "snow", "ambient.biomesunseen.frost_loop", "music.biomesunseen.frost_theme"),
        new BiomeDef("hoarfrost_meadow", "Hoarfrost Meadow", "frost", 0xA8E6CF, 0x8FD8C8, 0x6FB8E8, 0xD6F0FF, 0xEAF8FF, -0.35, 0.7, "frost", 0.08, 0.15, 8, "snow", "ambient.biomesunseen.frost_loop", "music.biomesunseen.frost_theme"),
        new BiomeDef("boreal_crystal_taiga", "Boreal Crystal Taiga", "frost", 0xA8E6CF, 0x8FD8C8, 0x6FB8E8, 0xD6F0FF, 0xEAF8FF, -0.4, 0.65, "frost", 0.35, 0.8, 8, "snow", "ambient.biomesunseen.frost_loop", "music.biomesunseen.frost_theme"),
        new BiomeDef("icebound_mire", "Icebound Mire", "frost", 0xA8E6CF, 0x8FD8C8, 0x6FB8E8, 0xD6F0FF, 0xEAF8FF, -0.5, 0.8, "frost", -0.2, 0.35, 7, "snow", "ambient.biomesunseen.frost_loop", "music.biomesunseen.frost_theme"),
        new BiomeDef("polar_glass_shore", "Polar Glass Shore", "frost", 0xA8E6CF, 0x8FD8C8, 0x6FB8E8, 0xD6F0FF, 0xEAF8FF, -0.42, 0.55, "frost", 0, 0.12, 7, "snow", "ambient.biomesunseen.frost_loop", "music.biomesunseen.frost_theme"),
        new BiomeDef("winter_bloom_garden", "Winter Bloom Garden", "frost", 0xA8E6CF, 0x8FD8C8, 0x6FB8E8, 0xD6F0FF, 0xEAF8FF, -0.25, 0.75, "frost", 0.2, 0.4, 7, "snow", "ambient.biomesunseen.frost_loop", "music.biomesunseen.frost_theme"),
        new BiomeDef("frozen_zephyr_hollows", "Frozen Zephyr Hollows", "frost", 0xA8E6CF, 0x8FD8C8, 0x6FB8E8, 0xD6F0FF, 0xEAF8FF, -0.48, 0.5, "frost", -0.1, 0.4, 7, "snow", "ambient.biomesunseen.frost_loop", "music.biomesunseen.frost_theme"),
        new BiomeDef("thunderglass_highlands", "Thunderglass Highlands", "storm", 0x6E7F8A, 0x56697A, 0x3E6B8F, 0x7A8FA8, 0x9AAFC2, 0.5, 0.7, "storm", 1.1, 1.8, 8, "thunder", "ambient.biomesunseen.storm_loop", "music.biomesunseen.storm_theme"),
        new BiomeDef("stormcall_plateau", "Stormcall Plateau", "storm", 0x6E7F8A, 0x56697A, 0x3E6B8F, 0x7A8FA8, 0x9AAFC2, 0.45, 0.8, "storm", 1.25, 1.1, 8, "thunder", "ambient.biomesunseen.storm_loop", "music.biomesunseen.storm_theme"),
        new BiomeDef("windscarred_buttes", "Windscarred Buttes", "storm", 0x6E7F8A, 0x56697A, 0x3E6B8F, 0x7A8FA8, 0x9AAFC2, 0.6, 0.25, "storm", 1.35, 1.6, 7, "clear", "ambient.biomesunseen.storm_loop", "music.biomesunseen.storm_theme"),
        new BiomeDef("rainlash_jungle", "Rainlash Jungle", "storm", 0x6E7F8A, 0x56697A, 0x3E6B8F, 0x7A8FA8, 0x9AAFC2, 0.95, 0.95, "storm", 0.3, 0.65, 8, "rain", "ambient.biomesunseen.storm_loop", "music.biomesunseen.storm_theme"),
        new BiomeDef("cloudrift_summit", "Cloudrift Summit", "storm", 0x6E7F8A, 0x56697A, 0x3E6B8F, 0x7A8FA8, 0x9AAFC2, 0.15, 0.65, "storm", 1.8, 2.4, 6, "thunder", "ambient.biomesunseen.storm_loop", "music.biomesunseen.storm_theme"),
        new BiomeDef("static_bloom_fields", "Static Bloom Fields", "storm", 0x6E7F8A, 0x56697A, 0x3E6B8F, 0x7A8FA8, 0x9AAFC2, 0.55, 0.6, "storm", 0.1, 0.2, 8, "thunder", "ambient.biomesunseen.storm_loop", "music.biomesunseen.storm_theme"),
        new BiomeDef("monsoon_delta", "Monsoon Delta", "storm", 0x6E7F8A, 0x56697A, 0x3E6B8F, 0x7A8FA8, 0x9AAFC2, 0.85, 1, "storm", -0.25, 0.3, 7, "rain", "ambient.biomesunseen.storm_loop", "music.biomesunseen.storm_theme"),
        new BiomeDef("shrieking_winds_expanse", "Shrieking Winds Expanse", "storm", 0x6E7F8A, 0x56697A, 0x3E6B8F, 0x7A8FA8, 0x9AAFC2, 0.4, 0.45, "storm", 0.15, 0.3, 7, "thunder", "ambient.biomesunseen.storm_loop", "music.biomesunseen.storm_theme"),
        new BiomeDef("lightningglass_spire", "Lightningglass Spire", "storm", 0x6E7F8A, 0x56697A, 0x3E6B8F, 0x7A8FA8, 0x9AAFC2, 0.35, 0.55, "storm", 1.55, 2.3, 6, "thunder", "ambient.biomesunseen.storm_loop", "music.biomesunseen.storm_theme"),
        new BiomeDef("tempest_basin", "Tempest Basin", "storm", 0x6E7F8A, 0x56697A, 0x3E6B8F, 0x7A8FA8, 0x9AAFC2, 0.5, 0.9, "storm", -0.05, 0.4, 7, "thunder", "ambient.biomesunseen.storm_loop", "music.biomesunseen.storm_theme"),
        new BiomeDef("murkiron_bogs", "Murkiron Bogs", "mire", 0x5C6B3C, 0x4A5A30, 0x3C4A2E, 0x8A9A6A, 0x6E7A52, 0.65, 0.9, "mire", -0.25, 0.3, 8, "rain", "ambient.biomesunseen.mire_loop", "music.biomesunseen.mire_theme"),
        new BiomeDef("peat_hollow_mire", "Peat Hollow Mire", "mire", 0x5C6B3C, 0x4A5A30, 0x3C4A2E, 0x8A9A6A, 0x6E7A52, 0.6, 0.95, "mire", -0.3, 0.25, 8, "rain", "ambient.biomesunseen.mire_loop", "music.biomesunseen.mire_theme"),
        new BiomeDef("drowned_root_marsh", "Drowned Root Marsh", "mire", 0x5C6B3C, 0x4A5A30, 0x3C4A2E, 0x8A9A6A, 0x6E7A52, 0.7, 0.92, "mire", -0.28, 0.35, 7, "rain", "ambient.biomesunseen.mire_loop", "music.biomesunseen.mire_theme"),
        new BiomeDef("sporechoked_mire", "Sporechoked Mire", "mire", 0x5C6B3C, 0x4A5A30, 0x3C4A2E, 0x8A9A6A, 0x6E7A52, 0.75, 1, "mire", -0.2, 0.4, 7, "rain", "ambient.biomesunseen.mire_loop", "music.biomesunseen.mire_theme"),
        new BiomeDef("blackwillow_bayou", "Blackwillow Bayou", "mire", 0x5C6B3C, 0x4A5A30, 0x3C4A2E, 0x8A9A6A, 0x6E7A52, 0.72, 0.95, "mire", -0.15, 0.35, 7, "rain", "ambient.biomesunseen.mire_loop", "music.biomesunseen.mire_theme"),
        new BiomeDef("siltveil_fens", "Siltveil Fens", "mire", 0x5C6B3C, 0x4A5A30, 0x3C4A2E, 0x8A9A6A, 0x6E7A52, 0.68, 0.98, "mire", -0.18, 0.28, 8, "rain", "ambient.biomesunseen.mire_loop", "music.biomesunseen.mire_theme"),
        new BiomeDef("bog_ember_quagmire", "Bog Ember Quagmire", "mire", 0x5C6B3C, 0x4A5A30, 0x3C4A2E, 0x8A9A6A, 0x6E7A52, 0.8, 0.9, "mire", -0.32, 0.3, 6, "rain", "ambient.biomesunseen.mire_loop", "music.biomesunseen.mire_theme"),
        new BiomeDef("hollowreed_wetlands", "Hollowreed Wetlands", "mire", 0x5C6B3C, 0x4A5A30, 0x3C4A2E, 0x8A9A6A, 0x6E7A52, 0.66, 0.9, "mire", -0.1, 0.2, 8, "rain", "ambient.biomesunseen.mire_loop", "music.biomesunseen.mire_theme"),
        new BiomeDef("mire_glass_pools", "Mire Glass Pools", "mire", 0x5C6B3C, 0x4A5A30, 0x3C4A2E, 0x8A9A6A, 0x6E7A52, 0.7, 0.85, "mire", -0.35, 0.22, 7, "rain", "ambient.biomesunseen.mire_loop", "music.biomesunseen.mire_theme"),
        new BiomeDef("gloomwater_flats", "Gloomwater Flats", "mire", 0x5C6B3C, 0x4A5A30, 0x3C4A2E, 0x8A9A6A, 0x6E7A52, 0.62, 0.95, "mire", -0.22, 0.18, 7, "rain", "ambient.biomesunseen.mire_loop", "music.biomesunseen.mire_theme"),
        new BiomeDef("skywisp_expanse", "Skywisp Expanse", "sky", 0x9ADF7A, 0x7ACB5E, 0x5EC8FF, 0xB8E8FF, 0xE0F6FF, 0.4, 0.5, "sky", 1.6, 2.5, 7, "clear", "ambient.biomesunseen.sky_loop", "music.biomesunseen.sky_theme"),
        new BiomeDef("skystone_archipelago", "Skystone Archipelago", "sky", 0x9ADF7A, 0x7ACB5E, 0x5EC8FF, 0xB8E8FF, 0xE0F6FF, 0.5, 0.55, "sky", 1.2, 2.2, 8, "clear", "ambient.biomesunseen.sky_loop", "music.biomesunseen.sky_theme"),
        new BiomeDef("cloud_bloom_terrace", "Cloud Bloom Terrace", "sky", 0x9ADF7A, 0x7ACB5E, 0x5EC8FF, 0xB8E8FF, 0xE0F6FF, 0.55, 0.6, "sky", 1.45, 1.3, 8, "clear", "ambient.biomesunseen.sky_loop", "music.biomesunseen.sky_theme"),
        new BiomeDef("zephyr_gardens", "Zephyr Gardens", "sky", 0x9ADF7A, 0x7ACB5E, 0x5EC8FF, 0xB8E8FF, 0xE0F6FF, 0.6, 0.55, "sky", 1.1, 1.1, 9, "clear", "ambient.biomesunseen.sky_loop", "music.biomesunseen.sky_theme"),
        new BiomeDef("highwind_pampas", "Highwind Pampas", "sky", 0x9ADF7A, 0x7ACB5E, 0x5EC8FF, 0xB8E8FF, 0xE0F6FF, 0.5, 0.35, "sky", 1.3, 0.9, 8, "clear", "ambient.biomesunseen.sky_loop", "music.biomesunseen.sky_theme"),
        new BiomeDef("aerial_shoals", "Aerial Shoals", "sky", 0x9ADF7A, 0x7ACB5E, 0x5EC8FF, 0xB8E8FF, 0xE0F6FF, 0.45, 0.5, "sky", 1.7, 2.6, 6, "clear", "ambient.biomesunseen.sky_loop", "music.biomesunseen.sky_theme"),
        new BiomeDef("sunspire_isles", "Sunspire Isles", "sky", 0x9ADF7A, 0x7ACB5E, 0x5EC8FF, 0xB8E8FF, 0xE0F6FF, 0.65, 0.35, "sky", 1.9, 2.8, 6, "clear", "ambient.biomesunseen.sky_loop", "music.biomesunseen.sky_theme"),
        new BiomeDef("floating_reef_haven", "Floating Reef Haven", "sky", 0x9ADF7A, 0x7ACB5E, 0x5EC8FF, 0xB8E8FF, 0xE0F6FF, 0.58, 0.6, "sky", 1.55, 2.4, 7, "clear", "ambient.biomesunseen.sky_loop", "music.biomesunseen.sky_theme"),
        new BiomeDef("wind_dancer_plains", "Wind Dancer Plains", "sky", 0x9ADF7A, 0x7ACB5E, 0x5EC8FF, 0xB8E8FF, 0xE0F6FF, 0.52, 0.45, "sky", 1, 0.7, 9, "clear", "ambient.biomesunseen.sky_loop", "music.biomesunseen.sky_theme"),
        new BiomeDef("horizon_steppe", "Horizon Steppe", "sky", 0x9ADF7A, 0x7ACB5E, 0x5EC8FF, 0xB8E8FF, 0xE0F6FF, 0.48, 0.4, "sky", 1.15, 0.8, 8, "clear", "ambient.biomesunseen.sky_loop", "music.biomesunseen.sky_theme"),
        new BiomeDef("voidshard_rifts", "Voidshard Rifts", "void", 0x6A4A8A, 0x5A3A7A, 0x4A2A6A, 0x2A1A3A, 0x3A2A4A, 0.3, 0.2, "void", -0.4, 0.9, 6, "clear", "ambient.biomesunseen.void_loop", "music.biomesunseen.void_theme"),
        new BiomeDef("gloomshard_depths", "Gloomshard Depths", "void", 0x6A4A8A, 0x5A3A7A, 0x4A2A6A, 0x2A1A3A, 0x3A2A4A, 0.25, 0.25, "void", -0.55, 0.7, 6, "clear", "ambient.biomesunseen.void_loop", "music.biomesunseen.void_theme"),
        new BiomeDef("unseeing_abyss", "Unseeing Abyss", "void", 0x6A4A8A, 0x5A3A7A, 0x4A2A6A, 0x2A1A3A, 0x3A2A4A, 0.2, 0.15, "void", -0.7, 1.1, 5, "clear", "ambient.biomesunseen.void_loop", "music.biomesunseen.void_theme"),
        new BiomeDef("whispering_void_barrens", "Whispering Void Barrens", "void", 0x6A4A8A, 0x5A3A7A, 0x4A2A6A, 0x2A1A3A, 0x3A2A4A, 0.28, 0.2, "void", -0.15, 0.35, 6, "clear", "ambient.biomesunseen.void_loop", "music.biomesunseen.void_theme"),
        new BiomeDef("nullglass_wastes", "Nullglass Wastes", "void", 0x6A4A8A, 0x5A3A7A, 0x4A2A6A, 0x2A1A3A, 0x3A2A4A, 0.32, 0.1, "void", -0.05, 0.2, 6, "clear", "ambient.biomesunseen.void_loop", "music.biomesunseen.void_theme"),
        new BiomeDef("eclipse_shade_realm", "Eclipse Shade Realm", "void", 0x6A4A8A, 0x5A3A7A, 0x4A2A6A, 0x2A1A3A, 0x3A2A4A, 0.22, 0.3, "void", -0.3, 0.6, 5, "clear", "ambient.biomesunseen.void_loop", "music.biomesunseen.void_theme"),
        new BiomeDef("starless_hollow", "Starless Hollow", "void", 0x6A4A8A, 0x5A3A7A, 0x4A2A6A, 0x2A1A3A, 0x3A2A4A, 0.18, 0.2, "void", -0.6, 0.8, 5, "clear", "ambient.biomesunseen.void_loop", "music.biomesunseen.void_theme"),
        new BiomeDef("riftveil_tundra", "Riftveil Tundra", "void", 0x6A4A8A, 0x5A3A7A, 0x4A2A6A, 0x2A1A3A, 0x3A2A4A, -0.2, 0.4, "void", 0.05, 0.25, 6, "snow", "ambient.biomesunseen.void_loop", "music.biomesunseen.void_theme"),
        new BiomeDef("entropy_scars", "Entropy Scars", "void", 0x6A4A8A, 0x5A3A7A, 0x4A2A6A, 0x2A1A3A, 0x3A2A4A, 0.26, 0.15, "void", -0.25, 0.85, 5, "thunder", "ambient.biomesunseen.void_loop", "music.biomesunseen.void_theme"),
        new BiomeDef("black_sun_basin", "Black Sun Basin", "void", 0x6A4A8A, 0x5A3A7A, 0x4A2A6A, 0x2A1A3A, 0x3A2A4A, 0.35, 0.05, "void", -0.35, 0.5, 5, "clear", "ambient.biomesunseen.void_loop", "music.biomesunseen.void_theme"),
        new BiomeDef("glowroot_caverns", "Glowroot Caverns", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.15, 0.25, "hollow_deep", -0.6, 0.22, 6, "clear", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("fungal_abyss", "Fungal Abyss", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.25, 0.64, "hollow_deep", -0.54, 0.49, 7, "clear", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("crystal_vein_hollows", "Crystal Vein Hollows", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.35, 0.25, "hollow_deep", -0.48, 0.76, 8, "rain", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("emberworm_tunnels", "Emberworm Tunnels", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.45, 0.64, "hollow_deep", -0.42, 0.22, 9, "clear", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("sunless_grotto", "Sunless Grotto", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.55, 0.25, "hollow_deep", -0.36, 0.49, 10, "clear", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("mantle_chasm", "Mantle Chasm", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.65, 0.64, "hollow_deep", -0.3, 0.76, 11, "rain", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("lantern_mushroom_sea", "Lantern Mushroom Sea", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.75, 0.25, "hollow_deep", -0.24, 0.22, 6, "clear", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("deepstone_spires", "Deepstone Spires", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.15, 0.64, "hollow_deep", -0.18, 0.49, 7, "clear", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("echo_lake_depths", "Echo Lake Depths", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.25, 0.25, "hollow_deep", -0.12, 0.76, 8, "rain", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("fossil_rib_catacombs", "Fossil Rib Catacombs", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.35, 0.64, "hollow_deep", -0.06, 0.22, 9, "clear", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("magma_siphon_gallery", "Magma Siphon Gallery", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.45, 0.25, "hollow_deep", -0.6, 0.49, 10, "clear", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("pale_mycelium_gardens", "Pale Mycelium Gardens", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.55, 0.64, "hollow_deep", -0.54, 0.76, 11, "rain", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("hollowstone_maze", "Hollowstone Maze", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.65, 0.25, "hollow_deep", -0.48, 0.22, 6, "clear", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("voidlight_crevasse", "Voidlight Crevasse", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.75, 0.64, "hollow_deep", -0.42, 0.49, 7, "clear", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("buried_temple_depths", "Buried Temple Depths", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.15, 0.25, "hollow_deep", -0.36, 0.76, 8, "rain", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("shimmering_sinkhole", "Shimmering Sinkhole", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.25, 0.64, "hollow_deep", -0.3, 0.22, 9, "clear", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("root_tangled_depths", "Root-Tangled Depths", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.35, 0.25, "hollow_deep", -0.24, 0.49, 10, "clear", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("ancient_ossuary", "Ancient Ossuary", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.45, 0.64, "hollow_deep", -0.18, 0.76, 11, "rain", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("prismatic_underlake", "Prismatic Underlake", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.55, 0.25, "hollow_deep", -0.12, 0.22, 6, "clear", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("the_first_ember", "The First Ember", "hollow_deep", 0x2A6A5A, 0x1E5A4A, 0x2E6A7A, 0x05070C, 0x14231F, 0.65, 0.64, "hollow_deep", -0.06, 0.49, 7, "clear", "ambient.biomesunseen.hollow_deep_loop", "music.biomesunseen.hollow_deep_theme"),
        new BiomeDef("dawnlit_isle", "Dawnlit Isle", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.3, 0.25, "aetherfall", -0.6, 0.22, 6, "clear", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("aurora_drift", "Aurora Drift", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.38, 0.64, "aetherfall", -0.54, 0.49, 7, "clear", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("skyglass_archipelago", "Skyglass Archipelago", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.47, 0.25, "aetherfall", -0.48, 0.76, 8, "thunder", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("cloudstep_meadow", "Cloudstep Meadow", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.55, 0.64, "aetherfall", -0.42, 0.22, 9, "clear", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("windward_ridge", "Windward Ridge", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.63, 0.25, "aetherfall", -0.36, 0.49, 10, "clear", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("twilight_canopy", "Twilight Canopy", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.72, 0.64, "aetherfall", -0.3, 0.76, 11, "thunder", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("starfall_hollows", "Starfall Hollows", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.8, 0.25, "aetherfall", -0.24, 0.22, 6, "clear", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("sunflare_plateau", "Sunflare Plateau", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.3, 0.64, "aetherfall", -0.18, 0.49, 7, "clear", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("moonpetal_gardens", "Moonpetal Gardens", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.38, 0.25, "aetherfall", -0.12, 0.76, 8, "thunder", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("aether_current_spires", "Aether Current Spires", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.47, 0.64, "aetherfall", -0.06, 0.22, 9, "clear", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("floating_ruins_expanse", "Floating Ruins Expanse", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.55, 0.25, "aetherfall", -0.6, 0.49, 10, "clear", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("halo_shore", "Halo Shore", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.63, 0.64, "aetherfall", -0.54, 0.76, 11, "thunder", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("cerulean_skylake", "Cerulean Skylake", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.72, 0.25, "aetherfall", -0.48, 0.22, 6, "clear", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("thunderhead_reef", "Thunderhead Reef", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.8, 0.64, "aetherfall", -0.42, 0.49, 7, "clear", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("glimmerwind_fields", "Glimmerwind Fields", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.3, 0.25, "aetherfall", -0.36, 0.76, 8, "thunder", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("celestial_terrace", "Celestial Terrace", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.38, 0.64, "aetherfall", -0.3, 0.22, 9, "clear", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("duskveil_cliffs", "Duskveil Cliffs", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.47, 0.25, "aetherfall", -0.24, 0.49, 10, "clear", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("luminark_shoals", "Luminark Shoals", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.55, 0.64, "aetherfall", -0.18, 0.76, 11, "thunder", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("skyforge_isles", "Skyforge Isles", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.63, 0.25, "aetherfall", -0.12, 0.22, 6, "clear", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("the_last_horizon", "The Last Horizon", "aetherfall", 0x9AD8FF, 0x7AB8E8, 0x8AD8FF, 0x6A4A8A, 0xC8A8E8, 0.72, 0.64, "aetherfall", -0.06, 0.49, 7, "clear", "ambient.biomesunseen.aetherfall_loop", "music.biomesunseen.aetherfall_theme"),
        new BiomeDef("glitchfield_barrens", "Glitchfield Barrens", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, -0.05, 0.25, "void_between", -0.6, 0.22, 6, "clear", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("inverted_woods", "Inverted Woods", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.07, 0.64, "void_between", -0.54, 0.49, 7, "thunder", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("shardstorm_expanse", "Shardstorm Expanse", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.18, 0.25, "void_between", -0.48, 0.76, 8, "clear", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("null_spire_wastes", "Null Spire Wastes", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.3, 0.64, "void_between", -0.42, 0.22, 9, "clear", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("echo_chamber_rifts", "Echo Chamber Rifts", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.42, 0.25, "void_between", -0.36, 0.49, 10, "thunder", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("mirrorlake_absurdity", "Mirrorlake Absurdity", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.53, 0.64, "void_between", -0.3, 0.76, 11, "clear", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("halfworld_terraces", "Halfworld Terraces", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.65, 0.25, "void_between", -0.24, 0.22, 6, "clear", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("screaming_static_plains", "Screaming Static Plains", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, -0.05, 0.64, "void_between", -0.18, 0.49, 7, "thunder", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("forgotten_code_caverns", "Forgotten Code Caverns", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.07, 0.25, "void_between", -0.12, 0.76, 8, "clear", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("obsidian_dreamscape", "Obsidian Dreamscape", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.18, 0.64, "void_between", -0.06, 0.22, 9, "clear", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("whisper_gallery", "Whisper Gallery", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.3, 0.25, "void_between", -0.6, 0.49, 10, "thunder", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("unraveling_meadow", "Unraveling Meadow", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.42, 0.64, "void_between", -0.54, 0.76, 11, "clear", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("paradox_dunes", "Paradox Dunes", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.53, 0.25, "void_between", -0.48, 0.22, 6, "clear", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("entropy_gardens", "Entropy Gardens", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.65, 0.64, "void_between", -0.42, 0.49, 7, "thunder", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("hollow_reflection_sea", "Hollow Reflection Sea", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, -0.05, 0.25, "void_between", -0.36, 0.76, 8, "clear", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("static_bloom_basin", "Static Bloom Basin", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.07, 0.64, "void_between", -0.3, 0.22, 9, "clear", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("impossible_stairways", "Impossible Stairways", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.18, 0.25, "void_between", -0.24, 0.49, 10, "thunder", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("dreamt_mountains", "Dreamt Mountains", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.3, 0.64, "void_between", -0.18, 0.76, 11, "clear", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("the_unwritten", "The Unwritten", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.42, 0.25, "void_between", -0.12, 0.22, 6, "clear", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme"),
        new BiomeDef("edges_of_everything", "Edges of Everything", "void_between", 0x5A2A7A, 0x3A1A5A, 0x2A0A4A, 0x08040C, 0x1A0A22, 0.53, 0.64, "void_between", -0.06, 0.49, 7, "thunder", "ambient.biomesunseen.void_between_loop", "music.biomesunseen.void_between_theme")
    }));

    public static final List<OreDef> ORES = Collections.unmodifiableList(Arrays.asList(new OreDef[]{
        new OreDef("azurethril", "Azurethril", 0x40E0D0, 0x80FFF0, 40, 90, 7, 6, 1, "crystal", "stone", true, 820, 3, 8, 3, 22, "swiftness", 2),
        new OreDef("emberite", "Emberite", 0xFF6A00, 0xFFB060, 10, 48, 6, 5, 1, "ember", "stone", true, 1010, 3, 7.5, 3.5, 15, "fire_resistance", 3),
        new OreDef("voidshard", "Voidshard", 0x2A0A3A, 0x9A40D0, 0, 20, 5, 3, 0.7, "void", "deepslate", true, 1560, 4, 9, 4, 18, "invisibility", 3),
        new OreDef("glimmer_quartz", "Glimmer Quartz", 0xF0F8FF, 0xFFFFFF, 20, 80, 8, 8, 1.1, null, "stone", true, 640, 2, 7, 2.5, 26, "night_vision", 1),
        new OreDef("sylvanite", "Sylvanite", 0x2E8B57, 0x66FF99, 40, 100, 7, 6, 1, "verdant", "stone", false, 780, 3, 7.2, 3, 24, "regeneration", 2),
        new OreDef("froststeel", "Froststeel", 0x87CEEB, 0xC0F0FF, 24, 72, 6, 5, 1, "frost", "stone", false, 930, 3, 7.8, 3.2, 19, "slowness", 2),
        new OreDef("murkiron", "Murkiron", 0x556B2F, 0x88AA55, 0, 40, 9, 7, 1.1, "mire", "stone", false, 700, 2, 6.5, 2.8, 21, "poison", 1),
        new OreDef("sunstone", "Sunstone", 0xFFD700, 0xFFEE88, 48, 120, 5, 4, 0.9, "sky", "stone", true, 1120, 3, 8.2, 3.4, 20, "strength", 2),
        new OreDef("moonshard", "Moonshard", 0xB0C4DE, 0xE0EEFF, 60, 150, 4, 3, 0.8, null, "stone", true, 1080, 3, 8, 3.3, 23, "regeneration", 2),
        new OreDef("thunderglass", "Thunderglass", 0xE8E864, 0xFFFFA0, 70, 140, 5, 4, 0.85, "storm", "stone", true, 1150, 3, 8.5, 3.1, 25, "swiftness", 2),
        new OreDef("crimsonite", "Crimsonite", 0xB22222, 0xFF5555, 5, 45, 6, 5, 1, "ember", "stone", false, 1250, 4, 8, 3.8, 14, "strength", 3),
        new OreDef("veridium", "Veridium", 0x008080, 0x40FFD0, 30, 85, 7, 6, 1, "verdant", "stone", false, 850, 3, 7.4, 3, 22, "regeneration", 2),
        new OreDef("petrified_amber", "Petrified Amber", 0xFFBF00, 0xFFE066, 30, 70, 6, 5, 0.95, "verdant", "stone", true, 720, 2, 6.8, 2.7, 28, "haste", 1),
        new OreDef("stelliferrum", "Stelliferrum", 0x1A2A6A, 0x6A8AFF, 0, 12, 3, 2, 0.5, null, "deepslate", true, 2100, 4, 10, 4.5, 12, "strength", 4),
        new OreDef("skystone", "Skystone", 0xB0B8C0, 0xD8E8FF, 90, 200, 8, 6, 1, "sky", "stone", false, 680, 2, 6.6, 2.6, 20, "levitation", 1),
        new OreDef("ashium", "Ashium", 0x696969, 0xA0A0A0, 15, 60, 8, 7, 1.1, "ember", "stone", false, 760, 2, 7, 2.9, 17, "fire_resistance", 2),
        new OreDef("tideglass", "Tideglass", 0x20B2AA, 0x70FFE8, 30, 63, 6, 5, 1, null, "stone", true, 800, 3, 7.3, 2.9, 24, "water_breathing", 2),
        new OreDef("gloomshard", "Gloomshard", 0x1A0022, 0x552277, 0, 30, 5, 4, 0.8, "void", "deepslate", true, 1320, 4, 8.6, 3.9, 16, "invisibility", 3),
        new OreDef("prismatic_ore", "Prismatic Ore", 0xFF69B4, 0xFFFFFF, 40, 90, 3, 2, 0.45, "crystal", "stone", true, 1680, 4, 9.5, 4.2, 30, "regeneration", 4),
        new OreDef("hearthstone", "Hearthstone", 0xCD5C5C, 0xFF9A76, 20, 60, 7, 6, 1.05, null, "stone", true, 740, 2, 6.9, 2.8, 26, "absorption", 1),
        new OreDef("lumenshard", "Lumenshard", 0x80FFD0, 0xC0FFF0, 5, 40, 6, 7, 1.2, "hollow_deep", "stone", true, 900, 3, 8, 3.2, 24, "night_vision", 2),
        new OreDef("deepiron", "Deep Iron", 0x8A7A6A, 0xC8B8A0, 0, 30, 9, 8, 1.2, "hollow_deep", "deepslate", false, 860, 3, 7.6, 3.1, 18, "strength", 2),
        new OreDef("biolumite", "Biolumite", 0x40E0A0, 0x90FFD0, 8, 48, 5, 6, 1, "hollow_deep", "stone", true, 980, 3, 8.2, 3.3, 26, "regeneration", 3),
        new OreDef("hollow_crystal", "Hollow Crystal", 0xB0A0FF, 0xE0D8FF, 12, 60, 4, 4, 0.8, "hollow_deep", "stone", true, 1200, 4, 9, 4, 28, "levitation", 3),
        new OreDef("embercoal", "Embercoal", 0xFF6A30, 0xFFA070, 0, 64, 10, 9, 1.3, "hollow_deep", "stone", true, 700, 2, 6.8, 2.6, 15, "fire_resistance", 1),
        new OreDef("fungisteel", "Fungisteel", 0x6A8A3A, 0xA0C860, 10, 50, 7, 6, 1, "hollow_deep", "stone", false, 940, 3, 7.8, 3.2, 22, "poison", 2),
        new OreDef("abyss_opal", "Abyss Opal", 0x2A4A8A, 0x5A8AFF, 20, 70, 3, 3, 0.6, "hollow_deep", "deepslate", true, 1600, 4, 9.6, 4.3, 30, "water_breathing", 4),
        new OreDef("corestone", "Corestone", 0xFF3A2A, 0xFF8070, 0, 16, 2, 2, 0.4, "hollow_deep", "deepslate", true, 2400, 4, 10.5, 5, 12, "absorption", 4),
        new OreDef("skyiron", "Skyiron", 0xB8C8D8, 0xE0F0FF, 80, 200, 8, 7, 1.1, "aetherfall", "stone", false, 880, 3, 7.8, 3.1, 20, "swiftness", 2),
        new OreDef("dawnsilver", "Dawnsilver", 0xF0E0A0, 0xFFF0C8, 90, 220, 6, 5, 0.9, "aetherfall", "stone", true, 1040, 3, 8.4, 3.4, 26, "regeneration", 3),
        new OreDef("windquartz", "Windquartz", 0xC8F0FF, 0xE8FFFF, 70, 180, 7, 6, 1, "aetherfall", "stone", true, 780, 2, 7.2, 2.8, 24, "levitation", 1),
        new OreDef("cloudite", "Cloudite", 0xE8F0FF, 0xFFFFFF, 100, 240, 6, 6, 1, "aetherfall", "stone", false, 820, 3, 7.4, 2.9, 22, "slow_falling", 2),
        new OreDef("sunforged", "Sunforged", 0xFFC040, 0xFFE090, 60, 160, 5, 4, 0.8, "aetherfall", "stone", true, 1300, 4, 9.2, 4, 24, "strength", 3),
        new OreDef("starfall_ore", "Starfall Ore", 0x8A8AFF, 0xC0C0FF, 120, 250, 4, 3, 0.6, "aetherfall", "stone", true, 1500, 4, 9.4, 4.2, 30, "night_vision", 3),
        new OreDef("aurorite", "Aurorite", 0x60FFC8, 0xA0FFE0, 110, 230, 5, 4, 0.7, "aetherfall", "stone", true, 1180, 3, 8.6, 3.6, 28, "absorption", 3),
        new OreDef("aetherglass", "Aetherglass", 0xA0D8FF, 0xE0F4FF, 140, 260, 8, 7, 1, "aetherfall", "stone", true, 760, 2, 7, 2.7, 26, "water_breathing", 2),
        new OreDef("nullite", "Nullite", 0x3A2A4A, 0x7A5A9A, 0, 30, 5, 5, 0.9, "void_between", "deepslate", true, 1350, 4, 8.8, 3.9, 18, "invisibility", 3),
        new OreDef("glitchstone", "Glitchstone", 0xFF40A0, 0xFF90D0, 10, 50, 6, 6, 1, "void_between", "stone", true, 1020, 3, 8.4, 3.5, 28, "swiftness", 3),
        new OreDef("paradox_shard", "Paradox Shard", 0x40D0FF, 0x90F0FF, 20, 70, 4, 4, 0.7, "void_between", "stone", true, 1450, 4, 9.2, 4.1, 30, "levitation", 3),
        new OreDef("entropy_crystal", "Entropy Crystal", 0xA040FF, 0xD090FF, 5, 40, 3, 3, 0.55, "void_between", "deepslate", true, 1750, 4, 9.8, 4.5, 32, "regeneration", 4),
        new OreDef("void_ember", "Void Ember", 0x2A0A3A, 0x6A2A8A, 0, 24, 7, 6, 1, "void_between", "deepslate", true, 880, 3, 7.6, 3, 20, "fire_resistance", 2),
        new OreDef("mirrorshard", "Mirrorshard", 0xC0C0D8, 0xF0F0FF, 30, 90, 5, 5, 0.8, "void_between", "stone", true, 1100, 3, 8.2, 3.4, 26, "invisibility", 2),
        new OreDef("static_ore", "Static Ore", 0xE0E040, 0xFFFF90, 15, 65, 6, 6, 0.9, "void_between", "stone", true, 960, 3, 7.8, 3.2, 22, "haste", 2),
        new OreDef("finality", "Finality", 0xFFFFFF, 0xFFD0FF, 0, 12, 2, 2, 0.35, "void_between", "deepslate", true, 2600, 4, 11, 5.5, 10, "absorption", 4)
    }));

    public static final List<DecorDef> DECOR = Collections.unmodifiableList(Arrays.asList(new DecorDef[]{
        new DecorDef("crystal_shard_block", "Crystal Shard Block", 0x40E0D0, "glass", "crystal"),
        new DecorDef("ember_rock", "Ember Rock", 0x8A3A1A, "basalt", "stone"),
        new DecorDef("verdant_soils", "Verdant Soils", 0x3A7A2A, "grass", "soil"),
        new DecorDef("frostbloom_ice", "Frostbloom Ice", 0xA8D8F0, "glass", "ice"),
        new DecorDef("storm_shale", "Storm Shale", 0x5A6A7A, "stone", "stone"),
        new DecorDef("mire_muck", "Mire Muck", 0x4A5A2A, "mud", "soil"),
        new DecorDef("skystone_bricks", "Skystone Bricks", 0xB8C4D0, "stone", "stone"),
        new DecorDef("nullglass", "Nullglass", 0x2A1A3A, "glass", "crystal"),
        new DecorDef("living_heartwood", "Living Heartwood", 0x6A4A2A, "wood", "wood"),
        new DecorDef("void_veined_stone", "Void Veined Stone", 0x3A2A4A, "deepslate", "stone"),
        new DecorDef("glowcap_block", "Glowcap Block", 0xC8A832, "fungus", "plant"),
        new DecorDef("sunstone_bricks", "Sunstone Bricks", 0xE8C860, "stone", "stone"),
        new DecorDef("hollowstone", "Hollowstone", 0x3A4A44, "deepslate", "stone"),
        new DecorDef("deepslate_marrow", "Deepslate Marrow", 0x4A3A3A, "stone", "stone"),
        new DecorDef("glowgabbro", "Glowgabbro", 0x2E5A50, "stone", "stone"),
        new DecorDef("emberlimestone", "Emberlimestone", 0x6A4A3A, "stone", "stone"),
        new DecorDef("fossilshale", "Fossilshale", 0x5A5A4A, "stone", "stone"),
        new DecorDef("skyglass", "Skyglass", 0x9AD8F0, "glass", "crystal"),
        new DecorDef("cloudstone", "Cloudstone", 0xD8E4F0, "stone", "stone"),
        new DecorDef("dawnquartzite", "Dawnquartzite", 0xE8D8B8, "stone", "stone"),
        new DecorDef("windslate", "Windslate", 0x7A9AA8, "stone", "stone"),
        new DecorDef("starfall_basalt", "Starfall Basalt", 0x4A4A6A, "basalt", "stone"),
        new DecorDef("voidstone", "Voidstone", 0x2A1A3A, "deepslate", "stone"),
        new DecorDef("nullslate", "Nullslate", 0x1E1E2A, "stone", "stone"),
        new DecorDef("paradox_granite", "Paradox Granite", 0x6A3A5A, "stone", "stone"),
        new DecorDef("echoeslate", "Echoeslate", 0x3A3A5A, "stone", "stone"),
        new DecorDef("static_breccia", "Static Breccia", 0x5A2A4A, "stone", "stone"),
        new DecorDef("hollow_deep_portal", "Hollow Deep Portal", 0x2A8A6A, "glass", "glass"),
        new DecorDef("aetherfall_portal", "Aetherfall Portal", 0x9AD8F0, "glass", "glass"),
        new DecorDef("void_between_portal", "Void Between Portal", 0x5A2A7A, "glass", "glass")
    }));

    public static final List<PlantDef> PLANTS = Collections.unmodifiableList(Arrays.asList(new PlantDef[]{
        new PlantDef("glitterbloom", "Glitterbloom", 0x9AF0E0, 1, true, true),
        new PlantDef("ember_petal", "Ember Petal", 0xFF7040, 1, true, true),
        new PlantDef("whisper_fern", "Whisper Fern", 0x4A9A3A, 2, false, false),
        new PlantDef("rimebell", "Rimebell", 0xB8E8FF, 1, true, true),
        new PlantDef("stormvine", "Stormvine", 0x6A8AAA, 3, false, false),
        new PlantDef("bog_lantern", "Bog Lantern", 0xD8C840, 1, true, true),
        new PlantDef("sky_puff", "Sky Puff", 0xE8F0FF, 2, false, false),
        new PlantDef("void_orchid", "Void Orchid", 0x7A4AA0, 1, true, true),
        new PlantDef("sunpetal", "Sunpetal", 0xFFD040, 1, true, true),
        new PlantDef("mossblossom", "Mossblossom", 0x8AC860, 1, true, true)
    }));

    public static final List<StructureDef> STRUCTURES = Collections.unmodifiableList(Arrays.asList(new StructureDef[]{
        new StructureDef("ruined_sanctum", "Ruined Sanctum", "crystal", "ruin", 24, 10, 0.6, 128, false, null, "sanctum_start", new String[]{"crystal", "verdant"}, 2, "pilgrims"),
        new StructureDef("crystal_spire_outpost", "Crystal Spire Outpost", "crystal", "tower", 32, 12, 0.55, 160, false, null, "spire_outpost_start", new String[]{"crystal"}, 3, "spirewardens"),
        new StructureDef("sunken_archive", "Sunken Archive", "mire", "ruin", 28, 11, 0.5, 144, false, null, "archive_start", new String[]{"mire", "frost"}, 3, "scholars"),
        new StructureDef("ember_fortress", "Ember Fortress", "ember", "fortress", 36, 14, 0.5, 192, false, null, "ember_fortress_start", new String[]{"ember"}, 4, "pyrewrights"),
        new StructureDef("fungal_cathedral", "Fungal Cathedral", "mire", "temple", 30, 12, 0.55, 160, false, null, "fungal_cathedral_start", new String[]{"mire", "verdant"}, 3, "myconids"),
        new StructureDef("skywatch_tower", "Skywatch Tower", "sky", "tower", 26, 10, 0.6, 144, false, null, "skywatch_start", new String[]{"sky", "storm"}, 3, "skywatchers"),
        new StructureDef("drowned_mausoleum", "Drowned Mausoleum", "mire", "tomb", 34, 13, 0.45, 176, false, null, "mausoleum_start", new String[]{"mire"}, 4, "the_drowned_court"),
        new StructureDef("verdant_circle", "Verdant Circle", "verdant", "shrine", 22, 9, 0.65, 128, false, null, "verdant_circle_start", new String[]{"verdant"}, 2, "grovekeepers"),
        new StructureDef("frost_hollow", "Frost Hollow", "frost", "shrine", 24, 10, 0.6, 128, false, null, "frost_hollow_start", new String[]{"frost"}, 2, "winter_singers"),
        new StructureDef("storm_observatory", "Storm Observatory", "storm", "tower", 30, 12, 0.5, 160, false, null, "observatory_start", new String[]{"storm", "sky"}, 3, "stormcallers"),
        new StructureDef("mire_bog_ruins", "Mire Bog Ruins", "mire", "ruin", 20, 8, 0.7, 112, false, null, "bog_ruins_start", new String[]{"mire"}, 2, "dredgers"),
        new StructureDef("whispering_menhir", "Whispering Menhir", "void", "shrine", 26, 10, 0.55, 144, false, null, "menhir_start", new String[]{"void", "storm"}, 3, "the_unspoken"),
        new StructureDef("prism_labyrinth", "Prism Labyrinth", "crystal", "dungeon", 34, 13, 0.45, 176, false, null, "labyrinth_start", new String[]{"crystal"}, 4, "prismwrights"),
        new StructureDef("void_rift_gate", "Void Rift Gate", "void", "portal", 40, 15, 0.4, 208, false, null, "rift_gate_start", new String[]{"void"}, 5, "riftwalkers"),
        new StructureDef("ancient_forge", "Ancient Forge", "ember", "forge", 32, 12, 0.5, 176, false, null, "forge_start", new String[]{"ember", "frost"}, 4, "the_first_smiths"),
        new StructureDef("pilgrim_rest", "Pilgrim Rest", "verdant", "house", 16, 7, 0.75, 96, false, null, "pilgrim_rest_start", new String[]{"verdant", "sky"}, 1, "wayfarers"),
        new StructureDef("mossbound_keep", "Mossbound Keep", "verdant", "fortress", 34, 13, 0.5, 176, false, null, "keep_start", new String[]{"verdant", "mire"}, 4, "the_mossbound_order"),
        new StructureDef("shrieking_winds_shrine", "Shrieking Winds Shrine", "storm", "shrine", 24, 10, 0.6, 128, false, null, "winds_shrine_start", new String[]{"storm"}, 2, "windbinders"),
        new StructureDef("obsidian_delta_camp", "Obsidian Delta Camp", "ember", "camp", 18, 8, 0.7, 112, false, null, "delta_camp_start", new String[]{"ember"}, 2, "ashwalkers"),
        new StructureDef("treetop_covenant", "Treetop Covenant", "verdant", "temple", 28, 11, 0.55, 160, false, null, "covenant_start", new String[]{"verdant", "sky"}, 3, "the_canopy_covenant"),
        new StructureDef("canyon_caravan", "Canyon Caravan", "storm", "camp", 18, 8, 0.7, 112, false, null, "caravan_start", new String[]{"storm", "ember"}, 2, "the_long_road"),
        new StructureDef("glitterfall_cave", "Glitterfall Cave", "crystal", "dungeon", 22, 9, 0.6, 128, false, null, "glitterfall_start", new String[]{"crystal"}, 3, "delvers"),
        new StructureDef("hollow_bell_tower", "Hollow Bell Tower", "frost", "tower", 26, 10, 0.55, 144, false, null, "bell_tower_start", new String[]{"frost", "void"}, 3, "the_last_ringers"),
        new StructureDef("drowned_court", "Drowned Court", "mire", "palace", 38, 14, 0.4, 192, false, null, "drowned_court_start", new String[]{"mire"}, 5, "the_drowned_court"),
        new StructureDef("barrow_mounds", "Barrow Mounds", "void", "tomb", 24, 10, 0.6, 128, false, null, "barrow_start", new String[]{"void", "mire"}, 3, "the_barrow_kings"),
        new StructureDef("alchemists_spire", "Alchemist's Spire", "crystal", "tower", 30, 12, 0.5, 160, false, null, "alchemist_start", new String[]{"crystal", "ember"}, 4, "the_crucible_circle"),
        new StructureDef("cradle_of_roots", "Cradle of Roots", "verdant", "boss_arena", 48, 18, 0.35, 256, true, "heart_of_the_forest", "cradle_start", new String[]{"verdant", "mire"}, 5, "the_heart_of_the_forest"),
        new StructureDef("serpents_maw", "Serpent's Maw", "void", "boss_arena", 48, 18, 0.35, 256, true, "void_serpent", "serpent_maw_start", new String[]{"void", "sky"}, 5, "the_void_serpent"),
        new StructureDef("eclipse_altar", "Eclipse Altar", "void", "temple", 36, 14, 0.45, 192, false, null, "eclipse_start", new String[]{"void", "frost"}, 4, "eclipse_cultists"),
        new StructureDef("lost_ziggurat", "Lost Ziggurat", "sky", "pyramid", 38, 14, 0.4, 192, false, null, "ziggurat_start", new String[]{"sky", "verdant"}, 5, "the_skyborne_empire"),
        new StructureDef("wardens_spire_arena", "Warden's Spire Arena", "hollow_deep", "boss_arena", 48, 18, 0.35, 256, true, "warden_of_the_hollow_deep", "warden_spire_start", new String[]{"hollow_deep"}, 5, "the_warden"),
        new StructureDef("glowroot_shrine", "Glowroot Shrine", "hollow_deep", "shrine", 22, 9, 0.65, 128, false, null, "glowroot_shrine_start", new String[]{"hollow_deep"}, 2, "rootkeepers"),
        new StructureDef("fossil_vault", "Fossil Vault", "hollow_deep", "tomb", 26, 10, 0.55, 160, false, null, "fossil_vault_start", new String[]{"hollow_deep"}, 3, "bonecharters"),
        new StructureDef("ember_siphon", "Ember Siphon", "hollow_deep", "forge", 30, 12, 0.5, 176, false, null, "ember_siphon_start", new String[]{"hollow_deep"}, 4, "siphonwrights"),
        new StructureDef("mycelium_circle", "Mycelium Circle", "hollow_deep", "shrine", 20, 8, 0.7, 112, false, null, "mycelium_circle_start", new String[]{"hollow_deep"}, 2, "myconids"),
        new StructureDef("crowns_eyrie", "Crown's Eyrie", "aetherfall", "boss_arena", 48, 18, 0.35, 256, true, "the_skyward_crown", "crowns_eyrie_start", new String[]{"aetherfall"}, 5, "the_crown"),
        new StructureDef("skyglass_temple", "Skyglass Temple", "aetherfall", "temple", 24, 10, 0.6, 144, false, null, "skyglass_temple_start", new String[]{"aetherfall"}, 3, "glasspriests"),
        new StructureDef("windward_beacon", "Windward Beacon", "aetherfall", "tower", 28, 11, 0.55, 160, false, null, "windward_beacon_start", new String[]{"aetherfall"}, 3, "beaconkeepers"),
        new StructureDef("starfall_observatory", "Starfall Observatory", "aetherfall", "tower", 30, 12, 0.5, 176, false, null, "starfall_observatory_start", new String[]{"aetherfall"}, 4, "starwatchers"),
        new StructureDef("halo_gatehouse", "Halo Gatehouse", "aetherfall", "ruin", 22, 9, 0.65, 128, false, null, "halo_gatehouse_start", new String[]{"aetherfall"}, 2, "gatekeepers"),
        new StructureDef("unraveling_nexus", "Unraveling Nexus", "void_between", "boss_arena", 48, 18, 0.35, 256, true, "the_unraveling", "unraveling_nexus_start", new String[]{"void_between"}, 5, "the_unraveling"),
        new StructureDef("paradox_arch", "Paradox Arch", "void_between", "ruin", 22, 9, 0.65, 128, false, null, "paradox_arch_start", new String[]{"void_between"}, 3, "archivists"),
        new StructureDef("mirror_vault", "Mirror Vault", "void_between", "dungeon", 26, 10, 0.55, 160, false, null, "mirror_vault_start", new String[]{"void_between"}, 4, "mirrorkeepers"),
        new StructureDef("static_ziggurat", "Static Ziggurat", "void_between", "pyramid", 32, 12, 0.5, 176, false, null, "static_ziggurat_start", new String[]{"void_between"}, 4, "static_priests"),
        new StructureDef("forgotten_library", "Forgotten Library", "void_between", "ruin", 28, 11, 0.55, 160, false, null, "forgotten_library_start", new String[]{"void_between"}, 4, "the_unwritten"),
        new StructureDef("hollow_deep_gate", "Hollow Deep Gate", "verdant", "portal", 40, 15, 0.4, 208, false, null, "hollow_deep_gate_start", new String[]{"verdant", "mire"}, 3, "gatekeepers"),
        new StructureDef("aetherfall_gate", "Aetherfall Gate", "sky", "portal", 40, 15, 0.4, 208, false, null, "aetherfall_gate_start", new String[]{"sky", "storm"}, 3, "gatekeepers"),
        new StructureDef("void_between_gate", "Void Between Gate", "void", "portal", 40, 15, 0.4, 208, false, null, "void_between_gate_start", new String[]{"void"}, 4, "gatekeepers")
    }));

    public static final List<MobDef> MOBS = Collections.unmodifiableList(Arrays.asList(new MobDef[]{
        new MobDef("lumox", "Lumox", "creature", 14, 0.28, 2, 1, 0.9, 1.2, new String[]{"graze", "follow_herd", "tameable"}, true, false, false, true, true, false, new String[]{"crystal", "verdant"}, 12, false, new String[]{"idle", "walk", "run", "eat", "graze", "sit", "tame"}, 0x7FE8D8, true),
        new MobDef("brambleback", "Brambleback", "creature", 28, 0.24, 5, 4, 1.4, 1.6, new String[]{"tank", "guard_herd", "reflect_damage"}, false, false, true, true, false, true, new String[]{"verdant", "mire"}, 9, false, new String[]{"idle", "walk", "run", "attack", "bramble_shield", "hurt", "death"}, 0x4A7A2A, false),
        new MobDef("siltstrider", "Siltstrider", "creature", 12, 0.32, 1.5, 0.5, 0.7, 1.8, new String[]{"water_walk", "flee", "skitter"}, false, false, false, false, true, true, new String[]{"mire"}, 10, false, new String[]{"idle", "walk", "run", "skitter", "flee", "hurt", "death"}, 0x6A7A4A, false),
        new MobDef("glimmermoth", "Glimmermoth", "creature", 6, 0.3, 0.5, 0, 0.8, 0.6, new String[]{"flock", "swarm", "ambient_fly", "attracted_to_light"}, false, false, true, true, true, false, new String[]{"crystal", "verdant"}, 14, false, new String[]{"idle", "fly", "flutter", "land", "hurt", "death"}, 0x9AF0E0, true),
        new MobDef("peat_hopper", "Peat Hopper", "creature", 8, 0.33, 1, 0.5, 0.6, 0.7, new String[]{"hop", "flee", "burrow"}, false, false, false, false, true, true, new String[]{"mire", "verdant"}, 12, false, new String[]{"idle", "walk", "hop", "burrow", "flee", "hurt", "death"}, 0x8A7A3A, false),
        new MobDef("ember_calf", "Ember Calf", "creature", 20, 0.26, 3, 1.5, 1, 1.3, new String[]{"graze", "follow_herd", "fire_immune", "tameable"}, true, false, false, true, false, false, new String[]{"ember"}, 10, false, new String[]{"idle", "walk", "run", "eat", "ember_burst", "sit", "tame"}, 0xFF6A2A, true),
        new MobDef("frost_fawn", "Frost Fawn", "creature", 12, 0.34, 1.5, 0.5, 0.7, 1.1, new String[]{"graze", "follow_herd", "flee", "tameable"}, true, false, false, true, true, false, new String[]{"frost"}, 12, false, new String[]{"idle", "walk", "run", "graze", "flee", "sit", "tame"}, 0xC8E8FF, false),
        new MobDef("murkling", "Murkling", "monster", 16, 0.3, 4, 1, 0.8, 1, new String[]{"pack_tactics", "ambush", "water_affinity"}, false, false, true, false, false, true, new String[]{"mire"}, 10, true, new String[]{"idle", "walk", "run", "attack", "lurk", "hurt", "death"}, 0x4A5A3A, false),
        new MobDef("spore_sprout", "Spore Sprout", "creature", 10, 0.22, 0.5, 0.5, 0.7, 0.9, new String[]{"plant_self", "tameable", "spread_spores"}, true, false, false, false, true, false, new String[]{"mire", "verdant"}, 9, false, new String[]{"idle", "walk", "bloom", "spore_burst", "sit", "tame"}, 0xC8A832, true),
        new MobDef("skywisp", "Skywisp", "creature", 8, 0.35, 0.5, 0, 0.9, 0.8, new String[]{"follow_weather", "flock", "ambient_fly"}, false, false, true, true, true, false, new String[]{"sky", "storm"}, 12, false, new String[]{"idle", "fly", "soar", "glide", "hurt", "death"}, 0xE8F0FF, true),
        new MobDef("thunder_ram", "Thunder Ram", "creature", 26, 0.3, 6, 3, 1.1, 1.4, new String[]{"charge", "pack_tactics", "shock_on_hit"}, false, false, true, true, false, true, new String[]{"storm", "sky"}, 8, false, new String[]{"idle", "walk", "run", "charge", "headbutt", "hurt", "death"}, 0x6A7A8A, false),
        new MobDef("mosshorn", "Mosshorn", "creature", 22, 0.25, 3, 2, 1.2, 1.5, new String[]{"wander_trade", "graze", "barter"}, false, true, false, true, false, false, new String[]{"verdant", "mire", "frost"}, 8, false, new String[]{"idle", "walk", "run", "eat", "trade", "graze"}, 0x6A8A4A, false),
        new MobDef("cinder_pup", "Cinder Pup", "creature", 14, 0.36, 4, 1, 0.7, 0.8, new String[]{"pack_tactics", "tameable", "flee_when_alone"}, true, false, true, false, true, false, new String[]{"ember"}, 11, false, new String[]{"idle", "walk", "run", "attack", "beg", "sit", "tame"}, 0xD85A2A, true),
        new MobDef("echo_howler", "Echo Howler", "monster", 24, 0.28, 5, 2, 1, 1.5, new String[]{"call_pack", "intimidate", "pack_tactics"}, false, false, true, false, false, true, new String[]{"void", "storm"}, 8, true, new String[]{"idle", "walk", "run", "howl", "attack", "hurt", "death"}, 0x3A2A4A, false),
        new MobDef("dune_skimmer", "Dune Skimmer", "creature", 10, 0.4, 1.5, 0.5, 0.8, 0.7, new String[]{"flee", "burrow", "swarm_day"}, false, false, true, false, true, false, new String[]{"crystal", "ember"}, 10, false, new String[]{"idle", "walk", "run", "skitter", "burrow", "hurt", "death"}, 0xE8C88A, false),
        new MobDef("tide_caller", "Tide Caller", "creature", 18, 0.27, 2, 1.5, 0.8, 1.4, new String[]{"heal_allies", "water_affinity", "tide_pull"}, false, false, true, false, false, true, new String[]{"mire", "storm"}, 7, false, new String[]{"idle", "walk", "swim", "cast", "heal", "hurt", "death"}, 0x2A8A8A, true),
        new MobDef("gloom_stalker", "Gloom Stalker", "monster", 20, 0.33, 6, 1.5, 0.8, 1.3, new String[]{"night_hunt", "pack_tactics", "stalk"}, false, false, true, false, false, true, new String[]{"void", "mire"}, 9, true, new String[]{"idle", "walk", "run", "stalk", "pounce", "attack", "hurt", "death"}, 0x2A1A3A, true),
        new MobDef("crystal_hermit", "Crystal Hermit", "creature", 16, 0.2, 2, 5, 1, 1.1, new String[]{"fortify", "terrain_use", "shell"}, false, false, false, false, true, true, new String[]{"crystal"}, 8, false, new String[]{"idle", "walk", "shell", "fortify", "hurt", "death"}, 0x40C0C0, true),
        new MobDef("wind_dancer", "Wind Dancer", "creature", 7, 0.38, 0.5, 0, 0.9, 0.7, new String[]{"flock", "dance", "ambient_fly"}, false, false, true, true, true, false, new String[]{"sky"}, 13, false, new String[]{"idle", "fly", "dance", "glide", "hurt", "death"}, 0xB8E8FF, false),
        new MobDef("mire_golem", "Mire Golem", "creature", 40, 0.18, 7, 6, 1.6, 2.2, new String[]{"terrain_use", "build_mounds", "tank"}, false, false, false, false, false, true, new String[]{"mire"}, 5, false, new String[]{"idle", "walk", "attack", "slam", "build", "hurt", "death"}, 0x5A6A3A, false),
        new MobDef("lantern_fox", "Lantern Fox", "creature", 12, 0.37, 3, 0.5, 0.6, 0.7, new String[]{"tameable", "light_aura", "flee", "fetch"}, true, false, false, false, true, false, new String[]{"verdant", "frost", "sky"}, 11, true, new String[]{"idle", "walk", "run", "pounce", "beg", "sit", "tame"}, 0xFFD08A, true),
        new MobDef("reef_grazer", "Reef Grazer", "creature", 18, 0.24, 1.5, 2, 1.3, 1, new String[]{"water_herd", "graze", "follow_herd"}, false, false, false, true, true, false, new String[]{"mire", "crystal"}, 9, false, new String[]{"idle", "swim", "walk", "graze", "hurt", "death"}, 0x3AAAB0, false),
        new MobDef("ash_crawler", "Ash Crawler", "monster", 9, 0.31, 3, 1, 0.6, 0.5, new String[]{"swarm", "pack_tactics", "burrow"}, false, false, true, false, false, true, new String[]{"ember"}, 11, false, new String[]{"idle", "walk", "run", "attack", "burrow", "hurt", "death"}, 0x6A3A2A, false),
        new MobDef("star_whale", "Star Whale", "creature", 60, 0.16, 2, 8, 3.5, 2.8, new String[]{"ambient_fly", "flock", "gentle_giant", "levitate"}, false, false, true, true, false, false, new String[]{"sky", "void"}, 3, false, new String[]{"idle", "fly", "swim_air", "pulse", "hurt", "death"}, 0x5A6AA0, true),
        new MobDef("petal_wing", "Petal Wing", "creature", 5, 0.34, 0.5, 0, 0.5, 0.5, new String[]{"pollinate", "flock", "flee", "attracted_to_flowers"}, false, false, true, true, true, false, new String[]{"verdant", "crystal"}, 14, false, new String[]{"idle", "fly", "flutter", "pollinate", "hurt", "death"}, 0xFF9AC8, true),
        new MobDef("glowmoth", "Glowmoth", "creature", 7, 0.34, 0.5, 0, 0.8, 0.6, new String[]{"flock", "ambient_fly", "graze"}, true, false, false, true, true, true, new String[]{"hollow_deep"}, 12, false, new String[]{"idle", "walk", "fly", "flutter", "graze", "hurt", "death"}, 0x80FFD0, true),
        new MobDef("tunnel_hound", "Tunnel Hound", "monster", 22, 0.32, 5, 1.5, 0.9, 1, new String[]{"pack_tactics", "follow_herd"}, false, false, true, false, false, false, new String[]{"hollow_deep"}, 10, true, new String[]{"idle", "walk", "run", "attack", "pounce", "hurt", "death"}, 0x5A6A5A, true),
        new MobDef("crystal_beetle", "Crystal Beetle", "creature", 14, 0.22, 2, 4, 0.9, 0.8, new String[]{"graze", "terrain_use"}, false, false, false, false, false, true, new String[]{"hollow_deep"}, 9, false, new String[]{"idle", "walk", "graze", "burrow", "hurt", "death"}, 0x40C0C0, true),
        new MobDef("magma_snail", "Magma Snail", "creature", 18, 0.14, 2, 3, 1.1, 0.9, new String[]{"graze", "terrain_use"}, false, false, false, false, false, true, new String[]{"hollow_deep"}, 9, false, new String[]{"idle", "walk", "graze", "slam", "hurt", "death"}, 0xFF6A30, true),
        new MobDef("echo_bat", "Echo Bat", "creature", 8, 0.38, 1, 0, 0.6, 0.5, new String[]{"flock", "ambient_fly"}, false, false, false, true, true, true, new String[]{"hollow_deep"}, 13, true, new String[]{"idle", "fly", "glide", "dive", "hurt", "death"}, 0x3A2A4A, false),
        new MobDef("root_gnawer", "Root Gnawer", "monster", 16, 0.3, 4, 1, 0.8, 0.7, new String[]{"pack_tactics", "graze"}, false, false, true, true, false, false, new String[]{"hollow_deep"}, 10, false, new String[]{"idle", "walk", "run", "attack", "graze", "hurt", "death"}, 0x6A4A2A, false),
        new MobDef("deep_lurker", "Deep Lurker", "monster", 30, 0.26, 7, 2, 1.3, 1.6, new String[]{"terrain_use", "pack_tactics"}, false, false, false, false, false, true, new String[]{"hollow_deep"}, 6, true, new String[]{"idle", "walk", "swim", "attack", "pounce", "hurt", "death"}, 0x1E2A3A, true),
        new MobDef("lantern_jelly", "Lantern Jelly", "creature", 12, 0.2, 1, 1, 0.9, 0.9, new String[]{"flock", "terrain_use"}, false, false, false, true, true, true, new String[]{"hollow_deep"}, 11, false, new String[]{"idle", "swim", "surface", "dive", "hurt", "death"}, 0x60FFE0, true),
        new MobDef("stoneback", "Stoneback", "creature", 34, 0.2, 4, 6, 1.5, 1.5, new String[]{"graze", "follow_herd", "pack_tactics"}, false, false, true, true, false, false, new String[]{"hollow_deep"}, 7, false, new String[]{"idle", "walk", "run", "graze", "headbutt", "hurt", "death"}, 0x5A4A3A, false),
        new MobDef("mycopath", "Mycopath", "creature", 16, 0.24, 2, 2, 1, 1.2, new String[]{"wander_trade", "barter", "graze"}, false, true, false, true, true, false, new String[]{"hollow_deep"}, 8, false, new String[]{"idle", "walk", "trade", "offer", "accept", "graze", "hurt", "death"}, 0xC8A832, true),
        new MobDef("skyray", "Skyray", "creature", 18, 0.36, 3, 1, 1.4, 0.6, new String[]{"ambient_fly", "flock"}, false, false, false, true, true, true, new String[]{"aetherfall"}, 12, false, new String[]{"idle", "fly", "glide", "dive", "hurt", "death"}, 0x8AD8FF, true),
        new MobDef("cloud_heron", "Cloud Heron", "creature", 14, 0.3, 2, 0.5, 1, 1.4, new String[]{"ambient_fly", "flock", "graze"}, false, false, false, true, true, true, new String[]{"aetherfall"}, 10, false, new String[]{"idle", "fly", "glide", "walk", "flee", "hurt", "death"}, 0xE8F0FF, false),
        new MobDef("zephyr_pup", "Zephyr Pup", "creature", 16, 0.35, 3, 1, 0.8, 0.8, new String[]{"pack_tactics", "follow_herd"}, true, false, true, true, false, false, new String[]{"aetherfall"}, 11, false, new String[]{"idle", "walk", "run", "attack", "beg", "sit", "tame", "hurt", "death"}, 0xB8E8FF, true),
        new MobDef("island_tortoise", "Island Tortoise", "creature", 40, 0.14, 3, 7, 1.8, 1.4, new String[]{"graze", "follow_herd", "terrain_use"}, false, false, false, true, false, true, new String[]{"aetherfall"}, 7, false, new String[]{"idle", "walk", "graze", "shell", "hurt", "death"}, 0x8A9A6A, false),
        new MobDef("dawnfinch", "Dawnfinch", "creature", 6, 0.4, 0.5, 0, 0.5, 0.5, new String[]{"flock", "ambient_fly", "graze"}, true, false, false, true, true, true, new String[]{"aetherfall"}, 14, false, new String[]{"idle", "fly", "flutter", "graze", "sit", "tame", "hurt", "death"}, 0xFFD08A, true),
        new MobDef("storm_jay", "Storm Jay", "creature", 10, 0.42, 2, 0, 0.7, 0.6, new String[]{"flock", "ambient_fly"}, false, false, false, true, false, true, new String[]{"aetherfall"}, 12, false, new String[]{"idle", "fly", "dive", "soar", "hurt", "death"}, 0x6A7A8A, false),
        new MobDef("summit_ram", "Summit Ram", "creature", 30, 0.28, 6, 3, 1.2, 1.4, new String[]{"pack_tactics", "follow_herd", "graze"}, false, false, true, true, false, false, new String[]{"aetherfall"}, 8, false, new String[]{"idle", "walk", "run", "charge", "headbutt", "hurt", "death"}, 0xD8E4F0, false),
        new MobDef("mistgraz", "Mistgraz", "creature", 22, 0.22, 2, 2, 1.2, 1.2, new String[]{"graze", "follow_herd"}, false, false, false, true, true, false, new String[]{"aetherfall"}, 10, false, new String[]{"idle", "walk", "run", "graze", "flee", "hurt", "death"}, 0xC8D8E8, false),
        new MobDef("star_serpent", "Star Serpent", "monster", 26, 0.34, 6, 2, 1.2, 1, new String[]{"ambient_fly", "pack_tactics"}, false, false, false, false, false, true, new String[]{"aetherfall"}, 7, true, new String[]{"idle", "fly", "attack", "pounce", "hurt", "death"}, 0x8A8AFF, true),
        new MobDef("windlark", "Windlark", "creature", 8, 0.44, 0.5, 0, 0.6, 0.5, new String[]{"flock", "ambient_fly", "graze"}, true, false, false, true, true, true, new String[]{"aetherfall"}, 13, false, new String[]{"idle", "fly", "dance", "glide", "sit", "tame", "hurt", "death"}, 0xC8F0FF, true),
        new MobDef("glitchling", "Glitchling", "monster", 10, 0.4, 3, 0, 0.6, 0.6, new String[]{"pack_tactics", "follow_herd"}, false, false, true, true, true, false, new String[]{"void_between"}, 13, false, new String[]{"idle", "walk", "run", "attack", "blink", "hurt", "death"}, 0xFF40A0, true),
        new MobDef("null_stalker", "Null Stalker", "monster", 24, 0.34, 6, 1, 0.9, 1.4, new String[]{"pack_tactics", "terrain_use"}, false, false, false, false, false, true, new String[]{"void_between"}, 9, true, new String[]{"idle", "walk", "run", "stalk", "pounce", "attack", "hurt", "death"}, 0x1E1E2A, true),
        new MobDef("mirror_wisp", "Mirror Wisp", "creature", 8, 0.36, 0.5, 0, 0.7, 0.7, new String[]{"ambient_fly", "flock"}, false, false, false, true, true, true, new String[]{"void_between"}, 12, false, new String[]{"idle", "fly", "glide", "heal", "hurt", "death"}, 0xC0C0D8, true),
        new MobDef("paradox_beast", "Paradox Beast", "monster", 34, 0.26, 8, 3, 1.4, 1.6, new String[]{"terrain_use", "pack_tactics"}, false, false, false, false, false, true, new String[]{"void_between"}, 6, false, new String[]{"idle", "walk", "run", "charge", "slam", "hurt", "death"}, 0x6A3A5A, true),
        new MobDef("static_crawler", "Static Crawler", "monster", 14, 0.33, 4, 1, 0.7, 0.5, new String[]{"pack_tactics", "terrain_use"}, false, false, true, false, true, true, new String[]{"void_between"}, 11, false, new String[]{"idle", "walk", "run", "attack", "burrow", "hurt", "death"}, 0xE0E040, true),
        new MobDef("dream_eater", "Dream Eater", "monster", 28, 0.29, 7, 2, 1.1, 1.3, new String[]{"pack_tactics", "graze"}, false, false, false, false, false, false, new String[]{"void_between"}, 7, true, new String[]{"idle", "walk", "run", "stalk", "attack", "devour", "hurt", "death"}, 0x5A2A7A, true),
        new MobDef("shardwing", "Shardwing", "creature", 12, 0.38, 3, 0.5, 0.9, 0.7, new String[]{"ambient_fly", "flock"}, false, false, false, true, true, true, new String[]{"void_between"}, 12, false, new String[]{"idle", "fly", "glide", "dive", "hurt", "death"}, 0xA0D8FF, true),
        new MobDef("inverse_grazer", "Inverse Grazer", "creature", 20, 0.22, 2, 3, 1.2, 1.2, new String[]{"graze", "follow_herd"}, false, false, false, true, true, false, new String[]{"void_between"}, 9, false, new String[]{"idle", "walk", "graze", "float", "hurt", "death"}, 0x3A1A5A, true),
        new MobDef("echo_husk", "Echo Husk", "monster", 20, 0.31, 5, 2, 0.9, 1.5, new String[]{"pack_tactics", "follow_herd"}, false, false, true, true, false, false, new String[]{"void_between"}, 9, false, new String[]{"idle", "walk", "run", "howl", "attack", "hurt", "death"}, 0x3A3A5A, false),
        new MobDef("unravel_spawn", "Unravel Spawn", "creature", 16, 0.27, 1, 1, 1, 1, new String[]{"wander_trade", "barter"}, false, true, false, false, false, false, new String[]{"void_between"}, 7, false, new String[]{"idle", "walk", "trade", "offer", "accept", "blink", "hurt", "death"}, 0xFF90D0, true)
    }));

    public static final List<BossDef> BOSSES = Collections.unmodifiableList(Arrays.asList(new BossDef[]{
        new BossDef("heart_of_the_forest", "The Heart of the Forest", 480, 0.24, 12, 2.6, 4.2, "cradle_of_roots", "music.biomesunseen.boss_heart", new String[]{"dormant", "awakening", "wrath", "final_bloom"}, new String[]{"root_slam", "spore_cloud", "summon_brambleback", "verdant_beam", "regenerate", "quake_stomp"}, "bosses/heart_of_the_forest", "verdant", 0x2FA83C, true),
        new BossDef("void_serpent", "The Void Serpent", 520, 0.36, 14, 1.8, 1.8, "serpents_maw", "music.biomesunseen.boss_serpent", new String[]{"coiled", "phasing", "frenzy", "unmaking"}, new String[]{"void_beam", "phase_shift", "tail_sweep", "rift_barrage", "devour", "gravity_well"}, "bosses/void_serpent", "void", 0x6A2AB0, true),
        new BossDef("warden_of_the_hollow_deep", "Warden of the Hollow Deep", 620, 0.22, 16, 3.2, 5, "wardens_spire_arena", "music.biomesunseen.boss_warden", new String[]{"buried", "awakens", "spire_risen", "collapse"}, new String[]{"slam", "tremor_wave", "tunnel_ambush", "spire_rise", "hollow_beam", "summon_glowmoth"}, "bosses/warden_of_the_hollow_deep", "hollow_deep", 0x2A8A6A, true),
        new BossDef("the_skyward_crown", "The Skyward Crown", 560, 0.34, 14, 2.4, 3.8, "crowns_eyrie", "music.biomesunseen.boss_crown", new String[]{"descending", "haloed", "shardfall", "last_light"}, new String[]{"aerial_dive", "gust_knockback", "sunbeam", "shard_split", "orbit_shards", "summon_dawnfinch"}, "bosses/the_skyward_crown", "aetherfall", 0xFFD060, true),
        new BossDef("the_unraveling", "The Unraveling", 700, 0.3, 18, 2.8, 4, "unraveling_nexus", "music.biomesunseen.boss_unraveling", new String[]{"quadruped", "serpent", "humanoid", "unmade"}, new String[]{"glitch_lunge", "rift_crawl", "reality_tear", "form_shift", "entropy_wave", "static_barrage"}, "bosses/the_unraveling", "void_between", 0xFF40A0, true)
    }));

    private static final Map<String, BiomeDef> BIOME_BY_ID = indexBiomes();
    private static final Map<String, OreDef> ORE_BY_ID = indexOres();
    private static final Map<String, MobDef> MOB_BY_ID = indexMobs();
    private static final Map<String, BossDef> BOSS_BY_ID = indexBosses();
    private static final Map<String, StructureDef> STRUCTURE_BY_ID = indexStructures();

    private Content() {
    }

    private static Map<String, BiomeDef> indexBiomes() {
        Map<String, BiomeDef> map = new LinkedHashMap<String, BiomeDef>();
        for (int i = 0; i < BIOMES.size(); i++) {
            BiomeDef def = BIOMES.get(i);
            map.put(def.id, def);
        }
        return Collections.unmodifiableMap(map);
    }

    private static Map<String, OreDef> indexOres() {
        Map<String, OreDef> map = new LinkedHashMap<String, OreDef>();
        for (int i = 0; i < ORES.size(); i++) {
            OreDef def = ORES.get(i);
            map.put(def.id, def);
        }
        return Collections.unmodifiableMap(map);
    }

    private static Map<String, MobDef> indexMobs() {
        Map<String, MobDef> map = new LinkedHashMap<String, MobDef>();
        for (int i = 0; i < MOBS.size(); i++) {
            MobDef def = MOBS.get(i);
            map.put(def.id, def);
        }
        return Collections.unmodifiableMap(map);
    }

    private static Map<String, BossDef> indexBosses() {
        Map<String, BossDef> map = new LinkedHashMap<String, BossDef>();
        for (int i = 0; i < BOSSES.size(); i++) {
            BossDef def = BOSSES.get(i);
            map.put(def.id, def);
        }
        return Collections.unmodifiableMap(map);
    }

    private static Map<String, StructureDef> indexStructures() {
        Map<String, StructureDef> map = new LinkedHashMap<String, StructureDef>();
        for (int i = 0; i < STRUCTURES.size(); i++) {
            StructureDef def = STRUCTURES.get(i);
            map.put(def.id, def);
        }
        return Collections.unmodifiableMap(map);
    }

    public static BiomeDef biome(String id) {
        return BIOME_BY_ID.get(id);
    }

    public static OreDef ore(String id) {
        return ORE_BY_ID.get(id);
    }

    public static MobDef mob(String id) {
        return MOB_BY_ID.get(id);
    }

    public static BossDef boss(String id) {
        return BOSS_BY_ID.get(id);
    }

    public static StructureDef structure(String id) {
        return STRUCTURE_BY_ID.get(id);
    }

    /** Biome ids belonging to a group, in catalog order. */
    public static List<String> biomeIdsInGroup(String group) {
        List<String> out = new ArrayList<String>();
        for (int i = 0; i < BIOMES.size(); i++) {
            BiomeDef def = BIOMES.get(i);
            if (def.group.equals(group)) {
                out.add(def.id);
            }
        }
        return out;
    }

    /** Ore ids, in catalog order. */
    public static List<String> allOreIds() {
        List<String> out = new ArrayList<String>();
        for (int i = 0; i < ORES.size(); i++) {
            out.add(ORES.get(i).id);
        }
        return out;
    }

    /** Mob ids, in catalog order. */
    public static List<String> allMobIds() {
        List<String> out = new ArrayList<String>();
        for (int i = 0; i < MOBS.size(); i++) {
            out.add(MOBS.get(i).id);
        }
        return out;
    }

    /** Structure ids, in catalog order. */
    public static List<String> allStructureIds() {
        List<String> out = new ArrayList<String>();
        for (int i = 0; i < STRUCTURES.size(); i++) {
            out.add(STRUCTURES.get(i).id);
        }
        return out;
    }

    /** Biome ids, in catalog order. */
    public static List<String> allBiomeIds() {
        List<String> out = new ArrayList<String>();
        for (int i = 0; i < BIOMES.size(); i++) {
            out.add(BIOMES.get(i).id);
        }
        return out;
    }

    /** Stable pseudo-random 0..255 noise used by texture/particle jitter. */
    public static int stableHash(String key) {
        int h = 0;
        for (int i = 0; i < key.length(); i++) {
            h = 31 * h + key.charAt(i);
        }
        return (h ^ (h >>> 16)) & 0xFF;
    }
}
