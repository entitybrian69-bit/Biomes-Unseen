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
        addBlock(ModBlocks.HOLLOW_PORTAL, "Hollow Portal");
        addItem(ModItems.HOLLOWITE_INGOT, "Hollowite Ingot");
        addItem(ModItems.HOLLOWITE_SWORD, "Hollowite Sword");
        addItem(ModItems.HOLLOWITE_BATTLEAXE, "Hollowite Battleaxe");
        addItem(ModItems.FIELD_GUIDE, "Biomes Unseen Field Guide");
        addItem(ModItems.HOLLOW_SIGIL, "Hollow Sigil");
        add("guide.biomesunseen.title", "BIOMES UNSEEN — FIELD GUIDE");
        add("guide.biomesunseen.world", "Start a NEW world for all new biomes and structures. Old chunks never regenerate.");
        add("guide.biomesunseen.biomes", "Find a biome: /locate biome biomesunseen:amber_meadow");
        add("guide.biomesunseen.structures", "Find a structure: /locate structure biomesunseen:windmill_ruin");
        add("guide.biomesunseen.dimension", "Use a Hollow Sigil to travel to or from the Hollow Deep. The sigil returns you to Overworld spawn. Backup command: /execute in biomesunseen:hollow_deep run tp @s 0 100 0");
        add("guide.biomesunseen.portal", "Craft a Hollow Portal with 4 obsidian, 4 amethyst shards, and 1 ender eye; walk into it to travel. Its return gate brings you beside that portal if it remains intact.");
        add("guide.biomesunseen.weapons", "Craft ore swords from their matching materials; combine Hollowite and sticks for a battleaxe.");
        add("message.biomesunseen.hollow_travel.wrong_dimension", "Hollow travel only connects the Overworld and Hollow Deep.");
        add("message.biomesunseen.hollow_travel.cooldown", "Hollow travel is recharging. Wait a moment before trying again.");
        add("item.biomesunseen.hollow_sigil.wrong_dimension", "The sigil only works in the Overworld and Hollow Deep.");
        add("item.biomesunseen.hollow_sigil.dimension_missing", "Hollow Deep is not loaded. Create a new world with Biomes Unseen installed.");

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
            addItem(ModItems.ORE_SWORDS.get(spec.id()), spec.name() + " Sword");
        }

        for (NamedSpec biome : Specs.dimensionBiomes()) {
            add("biome." + BiomesUnseen.MOD_ID + "." + biome.id(), biome.name());
        }
        for (OverworldBiomeSpec biome : Specs.overworld()) {
            add("biome." + BiomesUnseen.MOD_ID + "." + biome.id(), biome.name());
        }
    }
}
