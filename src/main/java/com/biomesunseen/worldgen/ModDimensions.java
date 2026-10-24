package com.biomesunseen.worldgen;

import com.biomesunseen.BiomesUnseen;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.dimension.DimensionType;

public final class ModDimensions {
    public static final ResourceKey<Level> HOLLOW_DEEP_LEVEL = ResourceKey.create(
            Registries.DIMENSION, new ResourceLocation(BiomesUnseen.MOD_ID, "hollow_deep"));
    public static final ResourceKey<DimensionType> HOLLOW_DEEP_TYPE = ResourceKey.create(
            Registries.DIMENSION_TYPE, new ResourceLocation(BiomesUnseen.MOD_ID, "hollow_deep"));

    private ModDimensions() {
    }
}
