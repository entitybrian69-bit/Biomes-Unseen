package com.biomesunseen.worldgen;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.spec.Specs;
import net.minecraft.resources.ResourceLocation;
import terrablender.api.Regions;
import terrablender.api.SurfaceRuleManager;

public final class ModTerraBlender {
    /** Phase 6: the 80 generated biomes are injected into the Overworld. */
    public static final boolean INJECT_INTO_OVERWORLD = true;
    private static final int REGION_WEIGHT = 3;

    private ModTerraBlender() {
    }

    /** Call from FMLCommonSetupEvent#enqueueWork. */
    public static void register() {
        if (!INJECT_INTO_OVERWORLD || Specs.overworld().isEmpty()) {
            BiomesUnseen.LOGGER.info("Overworld injection skipped (disabled or specs/overworld.json missing)");
            return;
        }
        Regions.register(new OverworldRegion(new ResourceLocation(BiomesUnseen.MOD_ID, "overworld"), REGION_WEIGHT));
        // VERIFY: SurfaceRuleManager.RuleCategory.OVERWORLD name in the TerraBlender version used.
        SurfaceRuleManager.addSurfaceRules(SurfaceRuleManager.RuleCategory.OVERWORLD,
                BiomesUnseen.MOD_ID, ModSurfaceRules.makeRules());
    }
}
