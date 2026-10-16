package com.biomesunseen.worldgen;

import net.minecraft.resources.ResourceKey;
import net.minecraft.core.Registry;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.resources.ResourceLocation;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.core.BiomeDef;
import com.biomesunseen.core.Content;
import com.biomesunseen.core.MathUtil;
import com.biomesunseen.core.ModConstants;

import java.util.List;

/**
 * Climate-pocket biome selector used by the legacy biome-source mixin.  For
 * every column it decides deterministically (shared value-noise, cached)
 * whether an "unseen pocket" replaces the vanilla biome, and which custom
 * biome fills it based on temperature/depth matching.  No per-tick scans:
 * selection is O(1) per query and results are cache-friendly.
 */
public final class UnseenBiomeSelector {

    /** Chance a column becomes an unseen pocket (1/N). */
    private static final int POCKET_MODULO = 24;
    private static double[] WEIGHT_TABLE;
    private static boolean warmed;

    private UnseenBiomeSelector() {
    }

    /** Pre-compute the cumulative rarity table once. */
    public static synchronized void warmUp() {
        if (warmed) {
            return;
        }
        warmed = true;
        double multiplier = BiomesUnseen.config().biomeRarityMultiplier;
        List<BiomeDef> biomes = Content.BIOMES;
        WEIGHT_TABLE = new double[biomes.size()];
        double total = 0.0;
        for (int i = 0; i < biomes.size(); i++) {
            total += biomes.get(i).effectiveRarity(multiplier);
            WEIGHT_TABLE[i] = total;
        }
    }

    /**
     * Decide the custom biome for a block position, or null to keep vanilla.
     * Called from the biome provider mixin.
     */
    public static Object select(int x, int z, double vanillaTemperature) {
        warmUp();
        if (!BiomesUnseen.config().enableAllBiomes) {
            return null;
        }
        int noise = (int) (MathUtil.valueNoise2d(x >> 3, z >> 3, 0xB10) * 4096.0);
        if (noise % POCKET_MODULO != 0) {
            return null;
        }
        double roll = MathUtil.valueNoise2d(x >> 5, z >> 5, 0x5EED);
        List<BiomeDef> biomes = Content.BIOMES;
        double total = WEIGHT_TABLE[biomes.size() - 1];
        if (total <= 0.0) {
            return null;
        }
        double target = roll * total;
        for (int i = 0; i < biomes.size(); i++) {
            if (target <= WEIGHT_TABLE[i]) {
                BiomeDef def = biomes.get(i);
                // Temperature band filter keeps tundra away from desert pockets.
                if (vanillaTemperature >= 1.0 && def.temperature < 0.4) {
                    return null;
                }
                if (vanillaTemperature <= 0.2 && def.temperature > 0.9) {
                    return null;
                }
                return biomeRegistryKey(def.id);
            }
        }
        return null;
    }

    private static Object biomeRegistryKey(String biomeId) {
        ResourceLocation location = new ResourceLocation(ModConstants.MOD_ID, biomeId);
        Registry<Biome> registry = com.biomesunseen.worldgen.LegacyBiomeRegistry.get();
        if (registry == null) {
            return null;
        }
        return registry.get(location);
    }
}
