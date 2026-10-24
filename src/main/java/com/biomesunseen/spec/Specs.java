package com.biomesunseen.spec;

import com.biomesunseen.BiomesUnseen;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Loads the generated spec tables from the classpath. A missing file yields an empty list,
 * so the mod still loads (with only the hand-written content) if the generators were not run.
 */
public final class Specs {
    private static final String BASE = "/data/" + BiomesUnseen.MOD_ID + "/specs/";
    private static final List<MobSpec> MOBS = loadMobs();
    private static final Map<String, MobSpec> MOB_BY_ID = index();
    private static final List<OreSpec> ORES = loadOres();
    private static final List<OverworldBiomeSpec> OVERWORLD = loadOverworld();
    private static final List<NamedSpec> DIMENSION_BIOMES = loadDimensionBiomes();

    private Specs() {
    }

    public static List<MobSpec> mobs() {
        return MOBS;
    }

    public static MobSpec mobById(String id) {
        return MOB_BY_ID.get(id);
    }

    public static List<OreSpec> ores() {
        return ORES;
    }

    public static List<OverworldBiomeSpec> overworld() {
        return OVERWORLD;
    }

    public static List<NamedSpec> dimensionBiomes() {
        return DIMENSION_BIOMES;
    }

    private static JsonArray read(String file) {
        try (InputStream in = Specs.class.getResourceAsStream(BASE + file)) {
            if (in == null) {
                BiomesUnseen.LOGGER.warn("Spec file {} not found; run the tools/gen_*.py generators", file);
                return new JsonArray();
            }
            return JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonArray();
        } catch (Exception e) {
            BiomesUnseen.LOGGER.error("Failed to read spec file {}", file, e);
            return new JsonArray();
        }
    }

    private static List<MobSpec> loadMobs() {
        List<MobSpec> list = new ArrayList<>();
        for (JsonElement e : read("mobs.json")) {
            list.add(MobSpec.fromJson(e.getAsJsonObject()));
        }
        return Collections.unmodifiableList(list);
    }

    private static Map<String, MobSpec> index() {
        Map<String, MobSpec> map = new LinkedHashMap<>();
        for (MobSpec spec : MOBS) {
            map.put(spec.id(), spec);
        }
        return map;
    }

    private static List<OreSpec> loadOres() {
        List<OreSpec> list = new ArrayList<>();
        for (JsonElement e : read("ores.json")) {
            list.add(OreSpec.fromJson(e.getAsJsonObject()));
        }
        return Collections.unmodifiableList(list);
    }

    private static List<OverworldBiomeSpec> loadOverworld() {
        List<OverworldBiomeSpec> list = new ArrayList<>();
        for (JsonElement e : read("overworld.json")) {
            list.add(OverworldBiomeSpec.fromJson(e.getAsJsonObject()));
        }
        return Collections.unmodifiableList(list);
    }

    private static List<NamedSpec> loadDimensionBiomes() {
        List<NamedSpec> list = new ArrayList<>();
        for (JsonElement e : read("dimension_biomes.json")) {
            list.add(NamedSpec.fromJson(e.getAsJsonObject()));
        }
        return Collections.unmodifiableList(list);
    }
}
