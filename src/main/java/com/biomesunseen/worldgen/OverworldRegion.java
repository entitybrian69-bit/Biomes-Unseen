package com.biomesunseen.worldgen;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.spec.OverworldBiomeSpec;
import com.biomesunseen.spec.Specs;
import com.mojang.datafixers.util.Pair;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.Climate;
import terrablender.api.Region;
import terrablender.api.RegionType;

import java.util.function.Consumer;

/** TerraBlender region holding the 80 generated Overworld biomes, placed by climate band. */
public class OverworldRegion extends Region {
    private static final float[][] TEMPERATURE = {
            {-1.0F, -0.45F}, {-0.45F, -0.15F}, {-0.15F, 0.2F}, {0.2F, 0.55F}, {0.55F, 1.0F}};
    private static final float[][] HUMIDITY = {
            {-1.0F, -0.35F}, {-0.35F, -0.1F}, {-0.1F, 0.1F}, {0.1F, 0.3F}, {0.3F, 1.0F}};
    /** continentalness min/max, erosion min/max. */
    private static final float[][] LAND = {
            {-0.11F, 0.03F, -1.0F, 0.05F}, {0.03F, 0.3F, -1.0F, -0.2F},
            {0.03F, 0.3F, -0.2F, 1.0F}, {0.3F, 1.0F, -1.0F, 1.0F}};

    public OverworldRegion(ResourceLocation name, int weight) {
        super(name, RegionType.OVERWORLD, weight);
    }

    public static ResourceKey<Biome> key(String id) {
        return ResourceKey.create(Registries.BIOME, new ResourceLocation(BiomesUnseen.MOD_ID, id));
    }

    @Override
    public void addBiomes(Registry<Biome> registry,
                          Consumer<Pair<Climate.ParameterPoint, ResourceKey<Biome>>> mapper) {
        Climate.Parameter surface = Climate.Parameter.point(0.0F);
        Climate.Parameter weirdness = Climate.Parameter.span(-1.0F, 1.0F);
        for (OverworldBiomeSpec spec : Specs.overworld()) {
            float[] t = TEMPERATURE[spec.t()];
            float[] h = HUMIDITY[spec.h()];
            float[] land = LAND[spec.l()];
            // VERIFY: Region#addBiome helper signature in the TerraBlender version used.
            this.addBiome(mapper,
                    Climate.Parameter.span(t[0], t[1]), Climate.Parameter.span(h[0], h[1]),
                    Climate.Parameter.span(land[0], land[1]), Climate.Parameter.span(land[2], land[3]),
                    surface, weirdness, 0.0F, key(spec.id()));
        }
    }
}
