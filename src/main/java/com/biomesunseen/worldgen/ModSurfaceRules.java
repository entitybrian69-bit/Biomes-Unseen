package com.biomesunseen.worldgen;

import com.biomesunseen.spec.OverworldBiomeSpec;
import com.biomesunseen.spec.Specs;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.levelgen.SurfaceRules;
import net.minecraftforge.registries.ForgeRegistries;

import java.util.ArrayList;
import java.util.List;

/** Overworld surface rules: top and under block per generated biome, read from specs/overworld.json. */
public final class ModSurfaceRules {
    private ModSurfaceRules() {
    }

    public static SurfaceRules.RuleSource makeRules() {
        List<SurfaceRules.RuleSource> rules = new ArrayList<>();
        for (OverworldBiomeSpec spec : Specs.overworld()) {
            Block top = ForgeRegistries.BLOCKS.getValue(new ResourceLocation(spec.top()));
            Block under = ForgeRegistries.BLOCKS.getValue(new ResourceLocation(spec.under()));
            if (top != null && under != null) {
                rules.add(layers(OverworldRegion.key(spec.id()), top, under));
            }
        }
        return SurfaceRules.sequence(rules.toArray(new SurfaceRules.RuleSource[0]));
    }

    private static SurfaceRules.RuleSource layers(ResourceKey<Biome> biome, Block top, Block under) {
        return SurfaceRules.ifTrue(SurfaceRules.isBiome(biome),
                SurfaceRules.sequence(
                        SurfaceRules.ifTrue(SurfaceRules.ON_FLOOR, SurfaceRules.state(top.defaultBlockState())),
                        SurfaceRules.ifTrue(SurfaceRules.UNDER_FLOOR, SurfaceRules.state(under.defaultBlockState()))));
    }
}
