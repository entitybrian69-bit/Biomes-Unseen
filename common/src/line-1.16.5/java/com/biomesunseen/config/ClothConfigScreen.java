package com.biomesunseen.config;

import com.biomesunseen.BiomesUnseen;

import me.shedaniel.clothconfig2.api.ConfigBuilder;
import me.shedaniel.clothconfig2.api.ConfigCategory;
import me.shedaniel.clothconfig2.api.ConfigEntryBuilder;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Consumer;

/**
 * Cloth Config screen factory.  Every ModConfig field is editable, grouped
 * into gameplay categories, and persisted through ModConfig.save on close.
 * The platform layer supplies the parent screen and translation text so this
 * class stays free of version-specific client calls.
 */
public final class ClothConfigScreen {

    private ClothConfigScreen() {
    }

    /**
     * Build the Cloth Config screen.
     *
     * @param title display title of the screen
     * @param parent the screen to return to
     * @param translator translation lookup used for labels
     * @return the finished screen
     */
    public static Object build(String title, Object parent, java.util.function.UnaryOperator<String> translator) {
        ConfigBuilder builder = ConfigBuilder.create()
                .setTitle(new net.minecraft.util.text.StringTextComponent(title))
                .setSavingRunnable(() -> BiomesUnseen.setConfig(BiomesUnseen.config()));
        builder.setParentScreen((net.minecraft.client.gui.screen.Screen) parent);
        ConfigEntryBuilder entryBuilder = builder.entryBuilder();
        ModConfig cfg = BiomesUnseen.config();

        ConfigCategory general = builder.getOrCreateCategory(new net.minecraft.util.text.StringTextComponent("General"));
        general.addEntry(entryBuilder.startBooleanField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("enableAllBiomes")), cfg.enableAllBiomes)
                .setDefaultValue(true)
                .setSaveConsumer(v -> cfg.enableAllBiomes = v)
                .build());
        general.addEntry(entryBuilder.startBooleanField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("enableAllOres")), cfg.enableAllOres)
                .setDefaultValue(true)
                .setSaveConsumer(v -> cfg.enableAllOres = v)
                .build());
        general.addEntry(entryBuilder.startBooleanField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("enableAllStructures")), cfg.enableAllStructures)
                .setDefaultValue(true)
                .setSaveConsumer(v -> cfg.enableAllStructures = v)
                .build());
        general.addEntry(entryBuilder.startBooleanField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("enableAllMobs")), cfg.enableAllMobs)
                .setDefaultValue(true)
                .setSaveConsumer(v -> cfg.enableAllMobs = v)
                .build());
        general.addEntry(entryBuilder.startBooleanField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("enableBosses")), cfg.enableBosses)
                .setDefaultValue(true)
                .setSaveConsumer(v -> cfg.enableBosses = v)
                .build());
        general.addEntry(entryBuilder.startBooleanField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("enableLoreBooks")), cfg.enableLoreBooks)
                .setDefaultValue(true)
                .setSaveConsumer(v -> cfg.enableLoreBooks = v)
                .build());
        general.addEntry(entryBuilder.startBooleanField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("enableStructureLoot")), cfg.enableStructureLoot)
                .setDefaultValue(true)
                .setSaveConsumer(v -> cfg.enableStructureLoot = v)
                .build());

        ConfigCategory world = builder.getOrCreateCategory(new net.minecraft.util.text.StringTextComponent("World"));
        world.addEntry(entryBuilder.startDoubleField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("biomeRarityMultiplier")), cfg.biomeRarityMultiplier)
                .setDefaultValue(1.0).setMin(0.0).setMax(10.0)
                .setSaveConsumer(v -> cfg.biomeRarityMultiplier = v).build());
        world.addEntry(entryBuilder.startDoubleField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("biomeTerraformingStrength")), cfg.biomeTerraformingStrength)
                .setDefaultValue(1.0).setMin(0.0).setMax(3.0)
                .setSaveConsumer(v -> cfg.biomeTerraformingStrength = v).build());
        world.addEntry(entryBuilder.startDoubleField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("oreRateMultiplier")), cfg.oreRateMultiplier)
                .setDefaultValue(1.0).setMin(0.0).setMax(10.0)
                .setSaveConsumer(v -> cfg.oreRateMultiplier = v).build());
        world.addEntry(entryBuilder.startDoubleField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("structureSpacingMultiplier")), cfg.structureSpacingMultiplier)
                .setDefaultValue(1.0).setMin(0.1).setMax(10.0)
                .setSaveConsumer(v -> cfg.structureSpacingMultiplier = v).build());
        world.addEntry(entryBuilder.startDoubleField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("weatherIntensity")), cfg.weatherIntensity)
                .setDefaultValue(1.0).setMin(0.0).setMax(3.0)
                .setSaveConsumer(v -> cfg.weatherIntensity = v).build());
        world.addEntry(entryBuilder.startIntField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("structureLodDistance")), cfg.structureLodDistance)
                .setDefaultValue(128).setMin(16).setMax(1024)
                .setSaveConsumer(v -> cfg.structureLodDistance = v).build());

        ConfigCategory mobs = builder.getOrCreateCategory(new net.minecraft.util.text.StringTextComponent("Mobs & Performance"));
        mobs.addEntry(entryBuilder.startDoubleField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("mobSpawnMultiplier")), cfg.mobSpawnMultiplier)
                .setDefaultValue(1.0).setMin(0.0).setMax(10.0)
                .setSaveConsumer(v -> cfg.mobSpawnMultiplier = v).build());
        mobs.addEntry(entryBuilder.startIntField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("mobGlobalCap")), cfg.mobGlobalCap)
                .setDefaultValue(180).setMin(0).setMax(2000)
                .setSaveConsumer(v -> cfg.mobGlobalCap = v).build());
        mobs.addEntry(entryBuilder.startIntField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("entityAiThrottle")), cfg.entityAiThrottle)
                .setDefaultValue(2).setMin(1).setMax(20)
                .setSaveConsumer(v -> cfg.entityAiThrottle = v).build());
        mobs.addEntry(entryBuilder.startDoubleField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("ambientParticleDensity")), cfg.ambientParticleDensity)
                .setDefaultValue(1.0).setMin(0.0).setMax(3.0)
                .setSaveConsumer(v -> cfg.ambientParticleDensity = v).build());
        mobs.addEntry(entryBuilder.startDoubleField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("musicFrequencyMultiplier")), cfg.musicFrequencyMultiplier)
                .setDefaultValue(1.0).setMin(0.1).setMax(10.0)
                .setSaveConsumer(v -> cfg.musicFrequencyMultiplier = v).build());
        mobs.addEntry(entryBuilder.startBooleanField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("enableAdaptiveMobs")), cfg.enableAdaptiveMobs)
                .setDefaultValue(true)
                .setSaveConsumer(v -> cfg.enableAdaptiveMobs = v).build());
        mobs.addEntry(entryBuilder.startBooleanField(
                        new net.minecraft.util.text.StringTextComponent(translator.apply("enablePackTactics")), cfg.enablePackTactics)
                .setDefaultValue(true)
                .setSaveConsumer(v -> cfg.enablePackTactics = v).build());

        return builder.build();
    }
}
