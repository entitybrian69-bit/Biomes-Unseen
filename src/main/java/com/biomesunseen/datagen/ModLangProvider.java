package com.biomesunseen.datagen;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.registry.ModBlocks;
import com.biomesunseen.registry.ModEntities;
import com.biomesunseen.registry.ModItems;
import com.biomesunseen.spec.MobSpec;
import com.biomesunseen.spec.NamedSpec;
import com.biomesunseen.spec.OreSpec;
import com.biomesunseen.spec.OverworldBiomeSpec;
import com.biomesunseen.spec.Specs;
import net.minecraft.data.PackOutput;
import net.minecraftforge.common.data.LanguageProvider;

/** Complete en_us translations. */
public class ModLangProvider extends LanguageProvider {
    public ModLangProvider(PackOutput output, String locale) {
        super(output, BiomesUnseen.MOD_ID, locale);
    }

    @Override
    protected void addTranslations() {
        add("itemGroup." + BiomesUnseen.MOD_ID + ".main", "Biomes Unseen");

        addBlock(ModBlocks.HOLLOWITE_ORE, "Hollowite Ore");
        addItem(ModItems.HOLLOWITE_INGOT, "Hollowite Ingot");

        addEntityType(ModEntities.HOLLOW_STALKER, "Hollow Stalker");
        addEntityType(ModEntities.SPORELING, "Sporeling");
        addEntityType(ModEntities.GLOOM_CRAWLER, "Gloom Crawler");
        addEntityType(ModEntities.CRYSTAL_GOLEM, "Crystal Golem");
        addEntityType(ModEntities.MIRE_WRAITH, "Mire Wraith");
        addEntityType(ModEntities.HEART_OF_THE_FOREST, "The Heart of the Forest");

        addItem(ModItems.HOLLOW_STALKER_SPAWN_EGG, "Hollow Stalker Spawn Egg");
        addItem(ModItems.SPORELING_SPAWN_EGG, "Sporeling Spawn Egg");
        addItem(ModItems.GLOOM_CRAWLER_SPAWN_EGG, "Gloom Crawler Spawn Egg");
        addItem(ModItems.CRYSTAL_GOLEM_SPAWN_EGG, "Crystal Golem Spawn Egg");
        addItem(ModItems.MIRE_WRAITH_SPAWN_EGG, "Mire Wraith Spawn Egg");
        addItem(ModItems.HEART_OF_THE_FOREST_SPAWN_EGG, "The Heart of the Forest Spawn Egg");

        for (MobSpec spec : Specs.mobs()) {
            addEntityType(ModEntities.SPEC_MOBS.get(spec.id()), spec.name());
            addItem(ModItems.SPEC_EGGS.get(spec.id()), spec.name() + " Spawn Egg");
        }
        for (OreSpec spec : Specs.ores()) {
            addBlock(ModBlocks.ORES.get(spec.id()), spec.name() + " Ore");
            addItem(ModItems.ORE_ITEMS.get(spec.id()), spec.itemName());
        }

        for (NamedSpec biome : Specs.dimensionBiomes()) {
            add("biome." + BiomesUnseen.MOD_ID + "." + biome.id(), biome.name());
        }
        for (OverworldBiomeSpec biome : Specs.overworld()) {
            add("biome." + BiomesUnseen.MOD_ID + "." + biome.id(), biome.name());
        }
    }
}
