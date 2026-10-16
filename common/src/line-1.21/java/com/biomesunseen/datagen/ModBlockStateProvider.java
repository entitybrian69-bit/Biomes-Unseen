package com.biomesunseen.datagen;

import com.biomesunseen.core.Content;
import com.biomesunseen.core.DecorDef;
import com.biomesunseen.core.OreDef;
import com.biomesunseen.core.PlantDef;

import java.nio.file.Path;

/**
 * Generates blockstates and block models for all 42 blocks.
 */
public final class ModBlockStateProvider {

    private ModBlockStateProvider() {
    }

    public static void run(Path output) throws Exception {
        Path states = output.resolve("assets/biomesunseen/blockstates");
        Path models = output.resolve("assets/biomesunseen/models/block");
        for (OreDef ore : Content.ORES) {
            String id = ore.id + "_ore";
            JsonWriter state = JsonWriter.obj()
                    .put("variants", JsonWriter.obj()
                            .put("", JsonWriter.obj()
                                    .put("model", "biomesunseen:block/" + id)));
            state.writeTo(states.resolve(id + ".json"));
            JsonWriter.obj()
                    .put("parent", "minecraft:block/cube_all")
                    .put("textures", JsonWriter.obj().put("all", "biomesunseen:block/" + id))
                    .writeTo(models.resolve(id + ".json"));
        }
        for (DecorDef decor : Content.DECOR) {
            JsonWriter.obj()
                    .put("variants", JsonWriter.obj()
                            .put("", JsonWriter.obj()
                                    .put("model", "biomesunseen:block/" + decor.id)))
                    .writeTo(states.resolve(decor.id + ".json"));
            JsonWriter.obj()
                    .put("parent", "minecraft:block/cube_all")
                    .put("textures", JsonWriter.obj().put("all", "biomesunseen:block/" + decor.id))
                    .writeTo(models.resolve(decor.id + ".json"));
        }
        for (PlantDef plant : Content.PLANTS) {
            JsonWriter.obj()
                    .put("variants", JsonWriter.obj()
                            .put("", JsonWriter.obj()
                                    .put("model", "biomesunseen:block/" + plant.id)))
                    .writeTo(states.resolve(plant.id + ".json"));
            JsonWriter.obj()
                    .put("parent", "minecraft:block/cross")
                    .put("textures", JsonWriter.obj().put("cross", "biomesunseen:block/" + plant.id))
                    .writeTo(models.resolve(plant.id + ".json"));
        }
    }
}
