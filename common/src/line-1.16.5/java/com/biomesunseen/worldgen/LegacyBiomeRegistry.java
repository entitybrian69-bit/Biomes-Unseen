package com.biomesunseen.worldgen;

import net.minecraft.core.Registry;
import net.minecraft.world.biome.Biome;

/**
 * Access to the server's biome registry (legacy line).
 */
public final class LegacyBiomeRegistry {

    private static Registry<Biome> biomes;

    private LegacyBiomeRegistry() {
    }

    /** Called from the mixin once the dynamic registry is available. */
    public static void set(Registry<Biome> registry) {
        biomes = registry;
    }

    public static Registry<Biome> get() {
        return biomes;
    }
}
