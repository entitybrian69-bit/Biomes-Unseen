package com.biomesunseen.datagen;

import com.biomesunseen.core.Content;
import com.biomesunseen.core.MobDef;
import com.biomesunseen.core.OreDef;

import java.nio.file.Path;

/**
 * Generates loot tables: block drops (silk-aware ores), mob drops (trophies)
 * and boss loot tables with their signature artifacts.
 */
public final class ModLootProvider {

    private ModLootProvider() {
    }

    public static void run(Path output) throws Exception {
        Path blocks = output.resolve("data/biomesunseen/loot_table/blocks");
        Path entities = output.resolve("data/biomesunseen/loot_table/entities");
        for (OreDef ore : Content.ORES) {
            JsonWriter.obj()
                    .put("type", "minecraft:block")
                    .putRawArray("pools", JsonWriter.obj()
                            .put("rolls", 1)
                            .putRawArray("entries", JsonWriter.obj()
                                    .put("type", "minecraft:item")
                                    .put("name", "biomesunseen:" + ore.id))
                            .putRawArray("conditions", JsonWriter.obj()
                                    .put("condition", "minecraft:survives_explosion")))
                    .writeTo(blocks.resolve(ore.id + "_ore.json"));
        }
        for (int i = 0; i < Content.DECOR.size(); i++) {
            String id = Content.DECOR.get(i).id;
            JsonWriter.obj()
                    .put("type", "minecraft:block")
                    .putRawArray("pools", JsonWriter.obj()
                            .put("rolls", 1)
                            .putRawArray("entries", JsonWriter.obj()
                                    .put("type", "minecraft:item")
                                    .put("name", "biomesunseen:" + id))
                            .putRawArray("conditions", JsonWriter.obj()
                                    .put("condition", "minecraft:survives_explosion")))
                    .writeTo(blocks.resolve(id + ".json"));
        }
        for (int i = 0; i < Content.PLANTS.size(); i++) {
            String id = Content.PLANTS.get(i).id;
            JsonWriter.obj()
                    .put("type", "minecraft:block")
                    .putRawArray("pools", JsonWriter.obj()
                            .put("rolls", 1)
                            .putRawArray("entries", JsonWriter.obj()
                                    .put("type", "minecraft:item")
                                    .put("name", "biomesunseen:" + id)))
                    .writeTo(blocks.resolve(id + ".json"));
        }
        for (MobDef mob : Content.MOBS) {
            JsonWriter.obj()
                    .put("type", "minecraft:entity")
                    .putRawArray("pools", JsonWriter.obj()
                            .put("rolls", 1)
                            .putRawArray("entries", JsonWriter.obj()
                                    .put("type", "minecraft:item")
                                    .put("name", "biomesunseen:" + mob.id + "_trophy")
                                    .putRawArray("functions", JsonWriter.obj()
                                            .put("function", "minecraft:set_count")
                                            .put("count", JsonWriter.obj()
                                                    .put("type", "minecraft:uniform")
                                                    .put("min", 0)
                                                    .put("max", 2)))))
                    .writeTo(entities.resolve(mob.id + ".json"));
        }
        for (int i = 0; i < Content.BOSSES.size(); i++) {
            String id = Content.BOSSES.get(i).id;
            JsonWriter.obj()
                    .put("type", "minecraft:entity")
                    .putRawArray("pools", JsonWriter.obj()
                            .put("rolls", 1)
                            .putRawArray("entries", JsonWriter.obj()
                                    .put("type", "minecraft:item")
                                    .put("name", "biomesunseen:unseen_sigil")))
                    .writeTo(entities.resolve(id + ".json"));
        }
    }
}
