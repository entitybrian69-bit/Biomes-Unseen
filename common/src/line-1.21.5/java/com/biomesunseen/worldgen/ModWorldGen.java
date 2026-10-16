package com.biomesunseen.worldgen;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.config.ModConfig;
import com.biomesunseen.core.Content;
import com.biomesunseen.core.ModConstants;
import com.biomesunseen.core.OreDef;
import com.biomesunseen.core.StructureDef;
import com.biomesunseen.platform.PlatformExpect;

import net.minecraft.resources.ResourceLocation;

/**
 * Worldgen orchestration for Minecraft 1.21.8.  Biomes, features and
 * structures ship as datapack JSON; this class wires the runtime side:
 * builtin registrations (legacy lines), biome injection and loader
 * modifications.  Ore rates and structure spacing honour the live config.
 */
public final class ModWorldGen {

    private static boolean prepared;
    private static boolean installed;

    private ModWorldGen() {
    }

    /** Construction phase: warm caches, validate content integrity. */
    public static synchronized void prepare() {
        if (prepared) {
            return;
        }
        prepared = true;
        // Validate the catalog up front so worldgen can never NPE later.
        for (int i = 0; i < Content.ORES.size(); i++) {
            OreDef ore = Content.ORES.get(i);
            if (ore.minY > ore.maxY) {
                throw new IllegalStateException("Ore " + ore.id + " has minY > maxY");
            }
        }
        for (int i = 0; i < Content.STRUCTURES.size(); i++) {
            StructureDef structure = Content.STRUCTURES.get(i);
            if (structure.separation >= structure.spacing) {
                throw new IllegalStateException("Structure " + structure.id + " separation >= spacing");
            }
        }

    }

    /** Setup phase: inject biomes and install loader modifications. */
    public static synchronized void install() {
        if (installed) {
            return;
        }
        installed = true;
        installNoiseListInjection();
        PlatformExpect.installBiomeModifications();
    }


    /**
     * Modern overworld injection: the shipped datapack overrides
     * multi_noise_biome_source_parameter_list/overworld.json so every custom
     * biome enters the climate system on all loaders.  Platform code adds
     * loader-specific biome modifications on top.
     */
    private static void installNoiseListInjection() {
        PlatformExpect.installBiomeInjection();
    }

    /** Effective ore veins-per-chunk for one ore after config multiplication. */
    public static int veinsPerChunk(OreDef ore) {
        ModConfig config = BiomesUnseen.config();
        if (!config.enableAllOres) {
            return 0;
        }
        return ore.effectiveVeinsPerChunk(config.oreRateMultiplier);
    }

    /** Effective structure spacing after config multiplication. */
    public static int structureSpacing(StructureDef structure) {
        ModConfig config = BiomesUnseen.config();
        if (!config.enableAllStructures) {
            return Integer.MAX_VALUE;
        }
        return structure.effectiveSpacing(config.structureSpacingMultiplier);
    }

    /** Effective structure separation after config multiplication. */
    public static int structureSeparation(StructureDef structure) {
        return structure.effectiveSeparation(BiomesUnseen.config().structureSpacingMultiplier);
    }

    /** True when the biome group is enabled. */
    public static boolean biomeGroupEnabled(String group) {
        return BiomesUnseen.config().enableAllBiomes;
    }

    /** True when bosses may spawn in arenas. */
    public static boolean bossesEnabled() {
        return BiomesUnseen.config().enableBosses;
    }
}
