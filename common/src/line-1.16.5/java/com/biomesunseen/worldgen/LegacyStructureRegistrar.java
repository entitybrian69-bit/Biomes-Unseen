package com.biomesunseen.worldgen;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.levelgen.StructureSettings;
import net.minecraft.world.level.levelgen.feature.StructureFeature;
import net.minecraft.world.level.levelgen.feature.configurations.StructureFeatureConfiguration;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.core.Content;
import com.biomesunseen.core.StructureDef;

/**
 * Registers separation settings for every jigsaw structure on lines where
 * structure spacing is code-driven (1.16.5/1.17.1/1.18.1).  The structure
 * definitions and jigsaw pools themselves ship as datapack JSON.
 */
public final class LegacyStructureRegistrar {

    private LegacyStructureRegistrar() {
    }

    /** Install separation settings for all structures. */
    public static void install() {
        for (int i = 0; i < Content.STRUCTURES.size(); i++) {
            StructureDef def = Content.STRUCTURES.get(i);
            if (!BiomesUnseen.config().enableAllStructures) {
                continue;
            }
            StructureFeature<?> structure = StructureFeature.STRUCTURES_REGISTRY.get(def.id);
            if (structure == null) {
                continue;
            }
            StructureFeatureConfiguration settings = new StructureFeatureConfiguration(
                    ModWorldGen.structureSpacing(def),
                    ModWorldGen.structureSeparation(def),
                    14357621);
            StructureSettings.DEFAULTS.put(structure, settings);
        }
    }
}
