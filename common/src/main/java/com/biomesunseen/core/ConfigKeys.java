package com.biomesunseen.core;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Configuration model shared by every platform.  Backed by JSON
 * (config/biomesunseen.json) and editable through Cloth Config.  Defaults
 * enable all content so the world generates full of life out of the box.
 */
public final class ConfigKeys {

    /** Global multiplier applied to every custom biome's rarity weight. */
    public double biomeRarityMultiplier = 1.0;

    /** Scales custom terrain depth/score values. 0 disables custom shapes. */
    public double biomeTerraformingStrength = 1.0;

    /** Master toggle for the 80 custom biomes. */
    public boolean enableAllBiomes = true;

    /** Master toggle for the 20 custom ores. */
    public boolean enableAllOres = true;

    /** Master toggle for the 30 custom structures. */
    public boolean enableAllStructures = true;

    /** Master toggle for the 25 custom mobs. */
    public boolean enableAllMobs = true;

    /** Master toggle for the 2 boss encounters. */
    public boolean enableBosses = true;

    /** Multiplier applied to ore veins-per-chunk. */
    public double oreRateMultiplier = 1.0;

    /** Multiplier applied to structure spacing (higher = rarer). */
    public double structureSpacingMultiplier = 1.0;

    /** Multiplier applied to all custom mob spawn weights. */
    public double mobSpawnMultiplier = 1.0;

    /** Hard cap on custom mobs per world tick window. */
    public int mobGlobalCap = 180;

    /** AI think-interval in ticks for custom mobs (higher = cheaper). */
    public int entityAiThrottle = 2;

    /** Density multiplier for biome ambient particles. */
    public double ambientParticleDensity = 1.0;

    /** Chunk radius within which structure starts are fully resolved. */
    public int structureLodDistance = 128;

    /** Multiplier for custom biome music delay. */
    public double musicFrequencyMultiplier = 1.0;

    /** Intensity of custom biome weather (rain/thunder chance). */
    public double weatherIntensity = 1.0;

    /** Spawn lore books, journals and murals in structures. */
    public boolean enableLoreBooks = true;

    /** Allow environmental adaptation behaviours. */
    public boolean enableAdaptiveMobs = true;

    /** Allow pack/coordinated mob tactics. */
    public boolean enablePackTactics = true;

    /** Generate structure loot chests. */
    public boolean enableStructureLoot = true;

    /** Serialise every field to a stable key/value map. */
    public Map<String, String> toMap() {
        Map<String, String> map = new LinkedHashMap<String, String>();
        map.put("biomeRarityMultiplier", String.valueOf(biomeRarityMultiplier));
        map.put("biomeTerraformingStrength", String.valueOf(biomeTerraformingStrength));
        map.put("enableAllBiomes", String.valueOf(enableAllBiomes));
        map.put("enableAllOres", String.valueOf(enableAllOres));
        map.put("enableAllStructures", String.valueOf(enableAllStructures));
        map.put("enableAllMobs", String.valueOf(enableAllMobs));
        map.put("enableBosses", String.valueOf(enableBosses));
        map.put("oreRateMultiplier", String.valueOf(oreRateMultiplier));
        map.put("structureSpacingMultiplier", String.valueOf(structureSpacingMultiplier));
        map.put("mobSpawnMultiplier", String.valueOf(mobSpawnMultiplier));
        map.put("mobGlobalCap", String.valueOf(mobGlobalCap));
        map.put("entityAiThrottle", String.valueOf(entityAiThrottle));
        map.put("ambientParticleDensity", String.valueOf(ambientParticleDensity));
        map.put("structureLodDistance", String.valueOf(structureLodDistance));
        map.put("musicFrequencyMultiplier", String.valueOf(musicFrequencyMultiplier));
        map.put("weatherIntensity", String.valueOf(weatherIntensity));
        map.put("enableLoreBooks", String.valueOf(enableLoreBooks));
        map.put("enableAdaptiveMobs", String.valueOf(enableAdaptiveMobs));
        map.put("enablePackTactics", String.valueOf(enablePackTactics));
        map.put("enableStructureLoot", String.valueOf(enableStructureLoot));
        return map;
    }

    /** Apply values from a key/value map; unknown keys are ignored. */
    public void apply(Map<String, String> values) {
        for (Map.Entry<String, String> entry : values.entrySet()) {
            String key = entry.getKey();
            String value = entry.getValue();
            try {
            if (key.equals("biomeRarityMultiplier")) {
                biomeRarityMultiplier = Double.parseDouble(value);
            }
            if (key.equals("biomeTerraformingStrength")) {
                biomeTerraformingStrength = Double.parseDouble(value);
            }
            if (key.equals("enableAllBiomes")) {
                enableAllBiomes = Boolean.parseBoolean(value);
            }
            if (key.equals("enableAllOres")) {
                enableAllOres = Boolean.parseBoolean(value);
            }
            if (key.equals("enableAllStructures")) {
                enableAllStructures = Boolean.parseBoolean(value);
            }
            if (key.equals("enableAllMobs")) {
                enableAllMobs = Boolean.parseBoolean(value);
            }
            if (key.equals("enableBosses")) {
                enableBosses = Boolean.parseBoolean(value);
            }
            if (key.equals("oreRateMultiplier")) {
                oreRateMultiplier = Double.parseDouble(value);
            }
            if (key.equals("structureSpacingMultiplier")) {
                structureSpacingMultiplier = Double.parseDouble(value);
            }
            if (key.equals("mobSpawnMultiplier")) {
                mobSpawnMultiplier = Double.parseDouble(value);
            }
            if (key.equals("mobGlobalCap")) {
                mobGlobalCap = Integer.parseInt(value);
            }
            if (key.equals("entityAiThrottle")) {
                entityAiThrottle = Integer.parseInt(value);
            }
            if (key.equals("ambientParticleDensity")) {
                ambientParticleDensity = Double.parseDouble(value);
            }
            if (key.equals("structureLodDistance")) {
                structureLodDistance = Integer.parseInt(value);
            }
            if (key.equals("musicFrequencyMultiplier")) {
                musicFrequencyMultiplier = Double.parseDouble(value);
            }
            if (key.equals("weatherIntensity")) {
                weatherIntensity = Double.parseDouble(value);
            }
            if (key.equals("enableLoreBooks")) {
                enableLoreBooks = Boolean.parseBoolean(value);
            }
            if (key.equals("enableAdaptiveMobs")) {
                enableAdaptiveMobs = Boolean.parseBoolean(value);
            }
            if (key.equals("enablePackTactics")) {
                enablePackTactics = Boolean.parseBoolean(value);
            }
            if (key.equals("enableStructureLoot")) {
                enableStructureLoot = Boolean.parseBoolean(value);
            }
            } catch (NumberFormatException ignored) {
                // Keep the previous value when a config entry is malformed.
            }
        }
    }

    /** Fresh instance with stock defaults. */
    public static ConfigKeys defaults() {
        return new ConfigKeys();
    }
}
