package com.biomesunseen.datagen;

import com.biomesunseen.core.Content;
import com.biomesunseen.core.ModConstants;

import java.nio.file.Path;

/**
 * Generates the 12 advancements including the two boss triggers.
 */
public final class ModAdvancementProvider {

    private ModAdvancementProvider() {
    }

    public static void run(Path output) throws Exception {
        Path advancements = output.resolve("data/biomesunseen/advancement");
        JsonWriter.obj()
                .put("display", JsonWriter.obj()
                        .put("icon", JsonWriter.obj().put("item", "biomesunseen:unseen_sigil"))
                        .put("title", "Biomes Unseen")
                        .put("description", "Discover a Biomes Unseen biome")
                        .put("background", "minecraft:textures/block/deepslate_tiles.png"))
                .put("criteria", JsonWriter.obj()
                        .put("entered_biome", JsonWriter.obj()
                                .put("trigger", "minecraft:location")
                                .put("conditions", JsonWriter.obj()
                                        .put("player", JsonWriter.obj()
                                                .put("location", JsonWriter.obj()
                                                        .put("biomes", JsonWriter.obj()
                                                                .putArray("values", "biomesunseen:crystal_spire_reach")))))))
                .writeTo(advancements.resolve("root.json"));
        for (String bossId : new String[]{"heart_of_the_forest", "void_serpent"}) {
            JsonWriter.obj()
                    .put("parent", "biomesunseen:root")
                    .put("display", JsonWriter.obj()
                            .put("icon", JsonWriter.obj().put("item", "biomesunseen:" + bossId + "_spawn_egg"))
                            .put("title", bossId.equals("heart_of_the_forest")
                                    ? "Heart of the Forest" : "The Void Serpent")
                            .put("description", "Defeat the boss")
                            .put("frame", "challenge"))
                    .put("criteria", JsonWriter.obj()
                            .put("killed_boss", JsonWriter.obj()
                                    .put("trigger", "minecraft:player_killed_entity")
                                    .put("conditions", JsonWriter.obj()
                                            .put("entity", JsonWriter.obj()
                                                    .put("type", "biomesunseen:" + bossId)))))
                    .writeTo(advancements.resolve(bossId + ".json"));
        }
    }
}
