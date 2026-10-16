package com.biomesunseen.worldgen;

import net.minecraft.core.Registry;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.levelgen.StructureSeparationSettings;
import net.minecraft.world.level.levelgen.feature.StructureFeature;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.core.Content;
import com.biomesunseen.core.StructureDef;

/**
 * Registers separation settings for every jigsaw structure on lines where
 * structure spacing is code-driven (the 1.18.1 line).  The structure
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
            ResourceLocation key = new ResourceLocation("biomesunseen", def.id);
            StructureFeature<?, ?> structure = Registry.STRUCTURE_FEATURE.get(key);
            if (structure == null) {
                continue;
            }
            StructureSeparationSettings settings = new StructureSeparationSettings(
                    ModWorldGen.structureSpacing(def),
                    ModWorldGen.structureSeparation(def),
                    14357621);
            structure.setSeparationSettings(settings);
        }
    }
}
