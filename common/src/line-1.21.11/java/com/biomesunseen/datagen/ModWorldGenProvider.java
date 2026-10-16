package com.biomesunseen.datagen;

import com.biomesunseen.core.BiomeDef;
import com.biomesunseen.core.Content;
import com.biomesunseen.core.MobDef;
import com.biomesunseen.core.OreDef;
import com.biomesunseen.core.StructureDef;

import java.nio.file.Path;

/**
 * Generates worldgen JSON: configured/placed ore features, biome documents
 * (with features + spawns), structure sets and jigsaw start pools.
 */
public final class ModWorldGenProvider {

    private ModWorldGenProvider() {
    }

    public static void run(Path output) throws Exception {
        Path configured = output.resolve("data/biomesunseen/worldgen/configured_feature");
        Path placed = output.resolve("data/biomesunseen/worldgen/placed_feature");
        Path biomes = output.resolve("data/biomesunseen/worldgen/biome");
        Path structureSets = output.resolve("data/biomesunseen/worldgen/structure_set");
        Path structures = output.resolve("data/biomesunseen/worldgen/structure");
        Path pools = output.resolve("data/biomesunseen/worldgen/template_pool");

        for (OreDef ore : Content.ORES) {
            JsonWriter.obj()
                    .put("type", "minecraft:ore")
                    .put("config", JsonWriter.obj()
                            .put("size", ore.veinSize)
                            .putRawArray("targets",
                                    JsonWriter.obj()
                                            .put("target", JsonWriter.obj()
                                                    .put("predicate_type", "minecraft:tag_match")
                                                    .put("tag", "minecraft:stone_ore_replaceables"))
                                            .put("state", JsonWriter.obj()
                                                    .put("Name", "biomesunseen:" + ore.id + "_ore")),
                                    JsonWriter.obj()
                                            .put("target", JsonWriter.obj()
                                                    .put("predicate_type", "minecraft:tag_match")
                                                    .put("tag", "minecraft:deepslate_ore_replaceables"))
                                            .put("state", JsonWriter.obj()
                                                    .put("Name", "biomesunseen:" + ore.id + "_ore"))))
                    .writeTo(configured.resolve(ore.id + "_ore.json"));
            JsonWriter.obj()
                    .put("feature", "biomesunseen:" + ore.id + "_ore")
                    .putRawArray("placement",
                            JsonWriter.obj().put("type", "minecraft:count").put("count", ore.veinsPerChunk),
                            JsonWriter.obj().put("type", "minecraft:in_square"),
                            JsonWriter.obj().put("type", "minecraft:height_range")
                                    .put("height", JsonWriter.obj()
                                            .put("type", "minecraft:uniform")
                                            .put("min_inclusive", JsonWriter.obj().put("absolute", ore.minY))
                                            .put("max_inclusive", JsonWriter.obj().put("absolute", ore.maxY))))
                    .writeTo(placed.resolve(ore.id + "_ore.json"));
        }

        for (BiomeDef def : Content.BIOMES) {
            JsonWriter features = JsonWriter.obj();
            java.util.List<String> featureList = new java.util.ArrayList<String>();
            for (OreDef ore : Content.ORES) {
                if (ore.biomeGroup == null || ore.biomeGroup.equals(def.group)) {
                    featureList.add("biomesunseen:" + ore.id + "_ore");
                }
            }
            java.util.List<String> spawnList = new java.util.ArrayList<String>();
            JsonWriter spawners = JsonWriter.obj();
            java.util.List<JsonWriter> monsterList = new java.util.ArrayList<JsonWriter>();
            java.util.List<JsonWriter> creatureList = new java.util.ArrayList<JsonWriter>();
            for (MobDef mob : Content.MOBS) {
                boolean inGroup = false;
                for (String g : mob.biomeGroups) {
                    if (g.equals(def.group)) {
                        inGroup = true;
                        break;
                    }
                }
                if (!inGroup) {
                    continue;
                }
                JsonWriter entry = JsonWriter.obj()
                        .put("type", "biomesunseen:" + mob.id)
                        .put("weight", mob.spawnWeight)
                        .put("minCount", 1)
                        .put("maxCount", mob.pack ? 4 : 2);
                if ("monster".equals(mob.category)) {
                    monsterList.add(entry);
                } else {
                    creatureList.add(entry);
                }
            }
            JsonWriter biome = JsonWriter.obj()
                    .put("temperature", def.temperature)
                    .put("downfall", def.downfall)
                    .put("has_precipitation", !"clear".equals(def.weather))
                    .put("effects", JsonWriter.obj()
                            .put("grass_color", def.grassColor)
                            .put("foliage_color", def.foliageColor)
                            .put("water_color", def.waterColor)
                            .put("sky_color", def.skyColor)
                            .put("fog_color", def.fogColor))
                    .put("spawners", JsonWriter.obj()
                            .putRawArray("monster", monsterList.toArray(new JsonWriter[0]))
                            .putRawArray("creature", creatureList.toArray(new JsonWriter[0])));
            java.util.List<java.util.List<String>> steps = new java.util.ArrayList<java.util.List<String>>();
            for (int i = 0; i < 11; i++) {
                steps.add(i == 6 ? featureList : new java.util.ArrayList<String>());
            }
            JsonWriter generation = JsonWriter.obj();
            // Raw step lists for the 10 generation steps.
            JsonWriter rawSteps = JsonWriter.obj();
            for (int i = 0; i < 10; i++) {
                java.util.List<String> stepFeatures = i == 6 ? featureList : new java.util.ArrayList<String>();
                rawSteps.putArray("step" + i, stepFeatures.toArray(new String[0]));
            }
            biome.put("carvers", JsonWriter.obj().put("air", "minecraft:overworld"));
            biome.put("features", rawSteps);
            biome.writeTo(biomes.resolve(def.id + ".json"));
        }

        for (StructureDef def : Content.STRUCTURES) {
            JsonWriter.obj()
                    .put("type", "minecraft:jigsaw")
                    .put("config", JsonWriter.obj()
                            .put("start_pool", "biomesunseen:" + def.startPool)
                            .put("size", 3)
                            .put("max_distance_from_center", def.maxDistanceFromCenter)
                            .put("start_height", JsonWriter.obj()
                                    .put("type", "minecraft:constant")
                                    .put("height", 0)))
                    .put("biomes", JsonWriter.obj().putArray("values", biomeKeysFor(def)))
                    .put("spawn_overrides", JsonWriter.obj())
                    .writeTo(structures.resolve(def.id + ".json"));
            JsonWriter.obj()
                    .putRawArray("structures", JsonWriter.obj()
                            .put("structure", "biomesunseen:" + def.id)
                            .put("weight", (int) Math.round(def.rarity * 10)))
                    .put("placement", JsonWriter.obj()
                            .put("type", "minecraft:random_spread")
                            .put("salt", Math.abs(def.id.hashCode() % 100000))
                            .put("spacing", def.spacing)
                            .put("separation", def.separation)
                            .put("spread_type", "linear"))
                    .writeTo(structureSets.resolve(def.id + ".json"));
            JsonWriter.obj()
                    .put("fallback", "minecraft:empty")
                    .putRawArray("elements", JsonWriter.obj()
                            .put("weight", 1)
                            .put("element", JsonWriter.obj()
                                    .put("element_type", "minecraft:legacy_single_pool_element")
                                    .put("location", "biomesunseen:" + def.id + "/start")
                                    .put("projection", "rigid")
                                    .put("processors", "minecraft:empty")))
                    .writeTo(pools.resolve(def.startPool + ".json"));
        }
    }

    private static String[] biomeKeysFor(StructureDef def) {
        java.util.List<String> keys = new java.util.ArrayList<String>();
        for (BiomeDef biome : Content.BIOMES) {
            if (def.spawnsInGroup(biome.group)) {
                keys.add("biomesunseen:" + biome.id);
            }
        }
        return keys.toArray(new String[0]);
    }
}
