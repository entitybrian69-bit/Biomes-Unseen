package com.biomesunseen.worldgen;

import net.minecraft.world.gen.feature.structure.Structure;
import net.minecraft.world.gen.feature.structure.StructureSeparationSettings;
import net.minecraft.world.gen.settings.DimensionStructuresSettings;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.core.Content;
import com.biomesunseen.core.StructureDef;

/**
 * Registers separation settings for every jigsaw structure on lines where
 * structure spacing is code-driven (1.16.5/1.17.1).  The structure
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
            Structure<?> structure = Structure.STRUCTURES_REGISTRY.get(def.id);
            if (structure == null) {
                continue;
            }
            StructureSeparationSettings settings = new StructureSeparationSettings(
                    ModWorldGen.structureSpacing(def),
                    ModWorldGen.structureSeparation(def),
                    14357621);
            DimensionStructuresSettings.DEFAULTS.put(structure, settings);
        }
    }
}
