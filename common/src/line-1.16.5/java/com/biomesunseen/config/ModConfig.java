package com.biomesunseen.config;

import com.biomesunseen.core.ModConstants;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Runtime configuration.  Stored as flat JSON in the loader config directory
 * and editable through Cloth Config.  All defaults enable every feature so
 * the world generates full of life out of the box.
 */
public final class ModConfig {

    /** Global multiplier applied to every custom biome's rarity weight. */
    public double biomeRarityMultiplier;

    /** Scales custom terrain depth/score values. 0 disables custom shapes. */
    public double biomeTerraformingStrength;

    /** Master toggle for the 80 custom biomes. */
    public boolean enableAllBiomes;

    /** Master toggle for the 20 custom ores. */
    public boolean enableAllOres;

    /** Master toggle for the 30 custom structures. */
    public boolean enableAllStructures;

    /** Master toggle for the 25 custom mobs. */
    public boolean enableAllMobs;

    /** Master toggle for the 2 boss encounters. */
    public boolean enableBosses;

    /** Multiplier applied to ore veins-per-chunk. */
    public double oreRateMultiplier;

    /** Multiplier applied to structure spacing (higher = rarer). */
    public double structureSpacingMultiplier;

    /** Multiplier applied to all custom mob spawn weights. */
    public double mobSpawnMultiplier;

    /** Hard cap on custom mobs per world tick window. */
    public int mobGlobalCap;

    /** AI think-interval in ticks for custom mobs (higher = cheaper). */
    public int entityAiThrottle;

    /** Density multiplier for biome ambient particles. */
    public double ambientParticleDensity;

    /** Chunk radius within which structure starts are fully resolved. */
    public int structureLodDistance;

    /** Multiplier for custom biome music delay. */
    public double musicFrequencyMultiplier;

    /** Intensity of custom biome weather (rain/thunder chance). */
    public double weatherIntensity;

    /** Spawn lore books, journals and murals in structures. */
    public boolean enableLoreBooks;

    /** Allow environmental adaptation behaviours. */
    public boolean enableAdaptiveMobs;

    /** Allow pack/coordinated mob tactics. */
    public boolean enablePackTactics;

    /** Generate structure loot chests. */
    public boolean enableStructureLoot;

    private ModConfig() {
    }

    public static ModConfig createDefault() {
        ModConfig cfg = new ModConfig();
        cfg.biomeRarityMultiplier = 1.0;
        cfg.biomeTerraformingStrength = 1.0;
        cfg.enableAllBiomes = true;
        cfg.enableAllOres = true;
        cfg.enableAllStructures = true;
        cfg.enableAllMobs = true;
        cfg.enableBosses = true;
        cfg.oreRateMultiplier = 1.0;
        cfg.structureSpacingMultiplier = 1.0;
        cfg.mobSpawnMultiplier = 1.0;
        cfg.mobGlobalCap = 180;
        cfg.entityAiThrottle = 2;
        cfg.ambientParticleDensity = 1.0;
        cfg.structureLodDistance = 128;
        cfg.musicFrequencyMultiplier = 1.0;
        cfg.weatherIntensity = 1.0;
        cfg.enableLoreBooks = true;
        cfg.enableAdaptiveMobs = true;
        cfg.enablePackTactics = true;
        cfg.enableStructureLoot = true;
        return cfg;
    }

    private static File configFile() {
        return new File("config", ModConstants.CONFIG_FILE);
    }

    /** Load from disk, creating the file with defaults on first run. */
    public static ModConfig load() {
        ModConfig cfg = createDefault();
        File file = configFile();
        if (!file.exists()) {
            save(cfg);
            return cfg;
        }
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(
                new FileInputStream(file), StandardCharsets.UTF_8))) {
            Map<String, String> values = parseFlatJson(reader);
            cfg.apply(values);
        } catch (Exception ignored) {
            // Corrupt config: fall back to defaults and rewrite the file.
            save(cfg);
        }
        return cfg;
    }

    /** Write the config to disk as stable, human-editable JSON. */
    public static void save(ModConfig cfg) {
        try {
            File file = configFile();
            File parent = file.getParentFile();
            if (parent != null && !parent.exists()) {
                parent.mkdirs();
            }
            try (Writer writer = new OutputStreamWriter(
                    new FileOutputStream(file), StandardCharsets.UTF_8)) {
                writer.write("{\n");
                Map<String, String> map = cfg.toMap();
                int i = 0;
                for (Map.Entry<String, String> entry : map.entrySet()) {
                    writer.write("  \"");
                    writer.write(entry.getKey());
                    writer.write("\": ");
                    writer.write(entry.getValue());
                    if (++i < map.size()) {
                        writer.write(",");
                    }
                    writer.write("\n");
                }
                writer.write("}\n");
            }
        } catch (Exception ignored) {
            // Best-effort persistence; defaults remain in memory.
        }
    }

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

    public void apply(Map<String, String> values) {
        for (Map.Entry<String, String> entry : values.entrySet()) {
            String key = entry.getKey();
            String v = entry.getValue();
            if (v == null) {
                continue;
            }
            v = v.trim();
            try {
            if ("biomeRarityMultiplier".equals(key)) {
                biomeRarityMultiplier = Double.parseDouble(v);
            }
            if ("biomeTerraformingStrength".equals(key)) {
                biomeTerraformingStrength = Double.parseDouble(v);
            }
            if ("enableAllBiomes".equals(key)) {
                enableAllBiomes = Boolean.parseBoolean(v);
            }
            if ("enableAllOres".equals(key)) {
                enableAllOres = Boolean.parseBoolean(v);
            }
            if ("enableAllStructures".equals(key)) {
                enableAllStructures = Boolean.parseBoolean(v);
            }
            if ("enableAllMobs".equals(key)) {
                enableAllMobs = Boolean.parseBoolean(v);
            }
            if ("enableBosses".equals(key)) {
                enableBosses = Boolean.parseBoolean(v);
            }
            if ("oreRateMultiplier".equals(key)) {
                oreRateMultiplier = Double.parseDouble(v);
            }
            if ("structureSpacingMultiplier".equals(key)) {
                structureSpacingMultiplier = Double.parseDouble(v);
            }
            if ("mobSpawnMultiplier".equals(key)) {
                mobSpawnMultiplier = Double.parseDouble(v);
            }
            if ("mobGlobalCap".equals(key)) {
                mobGlobalCap = Integer.parseInt(v);
            }
            if ("entityAiThrottle".equals(key)) {
                entityAiThrottle = Integer.parseInt(v);
            }
            if ("ambientParticleDensity".equals(key)) {
                ambientParticleDensity = Double.parseDouble(v);
            }
            if ("structureLodDistance".equals(key)) {
                structureLodDistance = Integer.parseInt(v);
            }
            if ("musicFrequencyMultiplier".equals(key)) {
                musicFrequencyMultiplier = Double.parseDouble(v);
            }
            if ("weatherIntensity".equals(key)) {
                weatherIntensity = Double.parseDouble(v);
            }
            if ("enableLoreBooks".equals(key)) {
                enableLoreBooks = Boolean.parseBoolean(v);
            }
            if ("enableAdaptiveMobs".equals(key)) {
                enableAdaptiveMobs = Boolean.parseBoolean(v);
            }
            if ("enablePackTactics".equals(key)) {
                enablePackTactics = Boolean.parseBoolean(v);
            }
            if ("enableStructureLoot".equals(key)) {
                enableStructureLoot = Boolean.parseBoolean(v);
            }
            } catch (NumberFormatException ignored) {
                // Keep the current value for malformed entries.
            }
        }
    }

    /**
     * Minimal flat-JSON reader for "{"key": value"}" documents.
     * Avoids a Gson dependency so the config layer compiles on every
     * Minecraft line.
     */
    private static Map<String, String> parseFlatJson(BufferedReader reader) throws Exception {
        Map<String, String> out = new LinkedHashMap<String, String>();
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            sb.append(line).append("\n");
        }
        String text = sb.toString();
        int i = 0;
        int n = text.length();
        while (i < n) {
            int keyStart = text.indexOf("\"", i);
            if (keyStart < 0) {
                break;
            }
            int keyEnd = text.indexOf("\"", keyStart + 1);
            if (keyEnd < 0) {
                break;
            }
            String key = text.substring(keyStart + 1, keyEnd);
            int colon = text.indexOf(":", keyEnd);
            if (colon < 0) {
                break;
            }
            int j = colon + 1;
            while (j < n && Character.isWhitespace(text.charAt(j))) {
                j++;
            }
            int k = j;
            while (k < n && text.charAt(k) != ",".charAt(0)
                    && text.charAt(k) != "\n".charAt(0)
                    && text.charAt(k) != "}".charAt(0)) {
                k++;
            }
            String value = text.substring(j, k).trim();
            out.put(key, value);
            i = k;
        }
        return out;
    }
}
