package com.biomesunseen.datagen;

import com.biomesunseen.core.Content;
import com.biomesunseen.core.OreDef;

import java.nio.file.Path;

/**
 * Generates recipes: ore smelting (mineral extraction), gear crafting,
 * tonics from minerals and machine cores from ores.
 */
public final class ModRecipeProvider {

    private ModRecipeProvider() {
    }

    public static void run(Path output) throws Exception {
        Path recipes = output.resolve("data/biomesunseen/recipe");
        for (OreDef ore : Content.ORES) {
            // Smelting: ore block -> mineral
            JsonWriter.obj()
                    .put("type", "minecraft:smelting")
                    .putRawArray("ingredient", JsonWriter.obj()
                            .put("item", "biomesunseen:" + ore.id + "_ore"))
                    .put("result", "biomesunseen:" + ore.id)
                    .put("experience", 0.7)
                    .put("cookingtime", 200)
                    .writeTo(recipes.resolve(ore.id + "_from_smelting.json"));
            // Blasting for faster processing
            JsonWriter.obj()
                    .put("type", "minecraft:blasting")
                    .putRawArray("ingredient", JsonWriter.obj()
                            .put("item", "biomesunseen:" + ore.id + "_ore"))
                    .put("result", "biomesunseen:" + ore.id)
                    .put("experience", 0.7)
                    .put("cookingtime", 100)
                    .writeTo(recipes.resolve(ore.id + "_from_blasting.json"));
            // Pickaxe: 3 minerals + 2 sticks
            JsonWriter.obj()
                    .put("type", "minecraft:crafting_shaped")
                    .putRawArray("pattern", com.biomesunseen.datagen.JsonWriter.obj()
                            .put("0", "MMM")
                            .put("1", " S ")
                            .put("2", " S "))
                    .put("key", JsonWriter.obj()
                            .put("M", JsonWriter.obj().put("item", "biomesunseen:" + ore.id))
                            .put("S", JsonWriter.obj().put("item", "minecraft:stick")))
                    .put("result", JsonWriter.obj()
                            .put("item", "biomesunseen:" + ore.id + "_pickaxe"))
                    .writeTo(recipes.resolve(ore.id + "_pickaxe.json"));
            // Tonic: mineral + glass bottle
            JsonWriter.obj()
                    .put("type", "minecraft:crafting_shapeless")
                    .putRawArray("ingredients", JsonWriter.obj()
                            .put("item", "biomesunseen:" + ore.id),
                            JsonWriter.obj().put("item", "minecraft:glass_bottle"))
                    .put("result", JsonWriter.obj()
                            .put("item", "biomesunseen:" + ore.id + "_tonic"))
                    .writeTo(recipes.resolve(ore.id + "_tonic.json"));
        }
        // Machine cores: tiered from minerals
        for (int tier = 1; tier <= 4; tier++) {
            OreDef ore = Content.ORES.get(Math.min(Content.ORES.size() - 1, tier * 4));
            JsonWriter.obj()
                    .put("type", "minecraft:crafting_shaped")
                    .putRawArray("pattern", com.biomesunseen.datagen.JsonWriter.obj()
                            .put("0", "MMM")
                            .put("1", "MCM")
                            .put("2", "MMM"))
                    .put("key", JsonWriter.obj()
                            .put("M", JsonWriter.obj().put("item", "biomesunseen:" + ore.id))
                            .put("C", JsonWriter.obj().put("item", "minecraft:redstone")))
                    .put("result", JsonWriter.obj()
                            .put("item", "biomesunseen:machine_core_t" + tier))
                    .writeTo(recipes.resolve("machine_core_t" + tier + ".json"));
        }
    }
}
