package com.biomesunseen.datagen;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.registry.ModBlocks;
import com.biomesunseen.registry.ModItems;
import com.biomesunseen.spec.OreSpec;
import com.biomesunseen.spec.Specs;
import net.minecraft.data.PackOutput;
import net.minecraft.data.recipes.FinishedRecipe;
import net.minecraft.data.recipes.RecipeCategory;
import net.minecraft.data.recipes.RecipeProvider;
import net.minecraft.data.recipes.SimpleCookingRecipeBuilder;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.crafting.Ingredient;

import java.util.function.Consumer;

public class ModRecipeProvider extends RecipeProvider {
    public ModRecipeProvider(PackOutput output) {
        super(output);
    }

    @Override
    protected void buildRecipes(Consumer<FinishedRecipe> writer) {
        Ingredient ore = Ingredient.of(ModBlocks.HOLLOWITE_ORE.get());
        SimpleCookingRecipeBuilder
                .smelting(ore, RecipeCategory.MISC, ModItems.HOLLOWITE_INGOT.get(), 0.9F, 200)
                .unlockedBy("has_hollowite_ore", has(ModBlocks.HOLLOWITE_ORE.get()))
                .save(writer, new ResourceLocation(BiomesUnseen.MOD_ID, "hollowite_ingot_from_smelting"));
        SimpleCookingRecipeBuilder
                .blasting(ore, RecipeCategory.MISC, ModItems.HOLLOWITE_INGOT.get(), 0.9F, 100)
                .unlockedBy("has_hollowite_ore", has(ModBlocks.HOLLOWITE_ORE.get()))
                .save(writer, new ResourceLocation(BiomesUnseen.MOD_ID, "hollowite_ingot_from_blasting"));
        for (OreSpec spec : Specs.ores()) {
            var block = ModBlocks.ORES.get(spec.id()).get();
            var drop = ModItems.ORE_ITEMS.get(spec.id()).get();
            Ingredient input = Ingredient.of(block);
            SimpleCookingRecipeBuilder.smelting(input, RecipeCategory.MISC, drop, 0.7F, 200)
                    .unlockedBy("has_" + spec.blockId(), has(block))
                    .save(writer, new ResourceLocation(BiomesUnseen.MOD_ID, spec.item() + "_from_smelting"));
            SimpleCookingRecipeBuilder.blasting(input, RecipeCategory.MISC, drop, 0.7F, 100)
                    .unlockedBy("has_" + spec.blockId(), has(block))
                    .save(writer, new ResourceLocation(BiomesUnseen.MOD_ID, spec.item() + "_from_blasting"));
        }
    }
}
