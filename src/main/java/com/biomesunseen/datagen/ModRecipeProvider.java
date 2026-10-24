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
import net.minecraft.data.recipes.ShapedRecipeBuilder;
import net.minecraft.data.recipes.ShapelessRecipeBuilder;
import net.minecraft.data.recipes.SimpleCookingRecipeBuilder;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Items;
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
        buildWeapons(writer);
    }

    private void buildWeapons(Consumer<FinishedRecipe> writer) {
        ShapedRecipeBuilder.shaped(RecipeCategory.COMBAT, ModItems.HOLLOWITE_SWORD.get())
                .pattern("H").pattern("H").pattern("S")
                .define('H', ModItems.HOLLOWITE_INGOT.get()).define('S', Items.STICK)
                .unlockedBy("has_hollowite", has(ModItems.HOLLOWITE_INGOT.get()))
                .save(writer, new ResourceLocation(BiomesUnseen.MOD_ID, "hollowite_sword"));
        ShapedRecipeBuilder.shaped(RecipeCategory.COMBAT, ModItems.HOLLOWITE_BATTLEAXE.get())
                .pattern("HHH").pattern("HSH").pattern(" S ")
                .define('H', ModItems.HOLLOWITE_INGOT.get()).define('S', Items.STICK)
                .unlockedBy("has_hollowite", has(ModItems.HOLLOWITE_INGOT.get()))
                .save(writer, new ResourceLocation(BiomesUnseen.MOD_ID, "hollowite_battleaxe"));
        ShapedRecipeBuilder.shaped(RecipeCategory.MISC, ModItems.HOLLOW_PORTAL.get())
                .pattern("OAO").pattern("AEA").pattern("OAO")
                .define('O', Items.OBSIDIAN).define('A', Items.AMETHYST_SHARD).define('E', Items.ENDER_EYE)
                .unlockedBy("has_ender_eye", has(Items.ENDER_EYE))
                .save(writer, new ResourceLocation(BiomesUnseen.MOD_ID, "hollow_portal"));
        ShapedRecipeBuilder.shaped(RecipeCategory.MISC, ModItems.HOLLOW_SIGIL.get())
                .pattern("OEO").pattern("GPG").pattern("OEO")
                .define('O', Items.OBSIDIAN).define('E', Items.ENDER_PEARL)
                .define('G', Items.GLOWSTONE_DUST).define('P', Items.PAPER)
                .unlockedBy("has_obsidian", has(Items.OBSIDIAN))
                .save(writer, new ResourceLocation(BiomesUnseen.MOD_ID, "hollow_sigil"));
        ShapelessRecipeBuilder.shapeless(RecipeCategory.MISC, ModItems.FIELD_GUIDE.get())
                .requires(Items.BOOK).requires(Items.PAPER).requires(Items.COMPASS)
                .unlockedBy("has_book", has(Items.BOOK))
                .save(writer, new ResourceLocation(BiomesUnseen.MOD_ID, "field_guide"));
        for (OreSpec spec : Specs.ores()) {
            var material = ModItems.ORE_ITEMS.get(spec.id()).get();
            var sword = ModItems.ORE_SWORDS.get(spec.id()).get();
            ShapedRecipeBuilder.shaped(RecipeCategory.COMBAT, sword)
                    .pattern("M").pattern("M").pattern("S")
                    .define('M', material).define('S', Items.STICK)
                    .unlockedBy("has_material", has(material))
                    .save(writer, new ResourceLocation(BiomesUnseen.MOD_ID, spec.id() + "_sword"));
        }
    }
}
