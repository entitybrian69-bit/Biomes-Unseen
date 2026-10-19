package com.biomesunseen.init;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.biome.Biome;

import java.util.Collection;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * ResourceKeys for all 140 biomes.
 *
 * In 1.20.1 biomes are data-driven: the object itself is built by the game from
 * {@code data/biomesunseen/worldgen/biome/<id>.json}. Java therefore does not
 * register biomes -- it holds the keys that worldgen, spawn placement and the
 * custom biome source point at.
 *
 * The keys are derived from the same generated table that produced those JSON
 * files, so a biome the datapack defines and a biome the Java references cannot
 * drift apart.
 */
public final class BUBiomes {

    /** Biome id -> key, in content-table order. */
    private static final Map<String, ResourceKey<Biome>> BY_ID = new LinkedHashMap<>();
    /** Keys grouped by dimension, for the biome sources and spawn placement. */
    private static final Map<String, java.util.List<ResourceKey<Biome>>> BY_DIMENSION =
            new LinkedHashMap<>();

    private BUBiomes() {
    }

    /** Build every key. Called once from the mod constructor. */
    public static void init() {
        for (String[] row : BUContent.DIMENSION_BIOMES) {
            String dimension = row[0];
            java.util.List<ResourceKey<Biome>> keys = new java.util.ArrayList<>();
            for (String id : row[1].split(",")) {
                if (id.isEmpty()) {
                    continue;
                }
                ResourceKey<Biome> key = key(id);
                BY_ID.put(id, key);
                keys.add(key);
            }
            BY_DIMENSION.put(dimension, Collections.unmodifiableList(keys));
        }
    }

    /** The ResourceKey for a biome registry path. */
    public static ResourceKey<Biome> key(String id) {
        return ResourceKey.create(Registries.BIOME,
                new ResourceLocation(BUContent.MODID, id));
    }

    public static ResourceKey<Biome> get(String id) {
        return BY_ID.get(id);
    }

    public static boolean contains(String id) {
        return BY_ID.containsKey(id);
    }

    /** Every biome key the mod adds. */
    public static Collection<ResourceKey<Biome>> all() {
        return BY_ID.values();
    }

    /** Every biome key belonging to one dimension. */
    public static java.util.List<ResourceKey<Biome>> inDimension(String dimension) {
        return BY_DIMENSION.getOrDefault(dimension, Collections.emptyList());
    }
}
