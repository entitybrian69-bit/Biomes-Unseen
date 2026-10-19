package com.biomesunseen.world;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.init.BUBiomes;
import com.biomesunseen.init.BUContent;
import net.minecraft.core.Holder;
import net.minecraft.core.Registry;
import net.minecraft.core.RegistryAccess;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.Climate;
import net.minecraft.world.level.biome.MultiNoiseBiomeSourceParameterList;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Builds the multi-noise parameter points for the twelve seeded Overworld biomes.
 *
 * <p>1.20.1 places Overworld biomes by sampling a fixed list of
 * {@link Climate.ParameterPoint}s held in
 * {@link MultiNoiseBiomeSourceParameterList.Preset#OVERWORLD}. A biome that is
 * registered but absent from that list never generates, no matter how complete
 * its worldgen JSON is -- which is why this class exists.
 *
 * <p>It computes the extra points here, from the parameters the content tables
 * authored, and exposes them for the biome-source mixin to splice into the
 * vanilla list. Authoring the numbers in the biome table rather than in this
 * class is what lets a designer move a biome around the Overworld without
 * touching Java.
 */
public final class OverworldBiomeInjector {

    /**
     * The parameter points to append to the vanilla Overworld list.
     *
     * Empty until {@link #inject} runs, and unmodifiable afterwards.
     */
    private static List<MultiNoiseBiomeSourceParameterList.ParameterPoint> seedPoints =
            Collections.emptyList();

    private static boolean injected;

    private OverworldBiomeInjector() {
    }

    /**
     * Resolve the twelve seeded biomes into parameter points.
     *
     * Called on ServerAboutToStart, which is the first moment the biome registry
     * is populated -- a {@link Holder} cannot be obtained before then.
     *
     * @param server the starting server, whose registry access holds the biomes
     */
    public static void inject(MinecraftServer server) {
        if (injected) {
            return;
        }
        RegistryAccess access = server.registryAccess();
        Registry<Biome> biomes = access.registryOrThrow(
                net.minecraft.core.registries.Registries.BIOME);

        List<MultiNoiseBiomeSourceParameterList.ParameterPoint> built = new ArrayList<>();

        for (Object[] row : BUContent.SEEDED_OVERWORLD_PARAMETERS) {
            String id = (String) row[0];
            ResourceKey<Biome> key = BUBiomes.get(id);
            if (key == null) {
                BiomesUnseen.LOGGER.warn("Seeded Overworld biome {} has no resource key", id);
                continue;
            }
            // A biome the datapack does not define cannot be placed. Skipping it
            // keeps the world loadable; logging it makes the gap findable rather
            // than leaving a silent hole in the Overworld.
            if (!biomes.getHolder(key).isPresent()) {
                BiomesUnseen.LOGGER.error(
                        "Seeded Overworld biome {} is not defined by the datapack; skipping", id);
                continue;
            }
            Holder<Biome> holder = biomes.getHolderOrThrow(key);

            float temperature = (Float) row[1];
            float humidity = (Float) row[2];
            float continentalness = (Float) row[3];
            float erosion = (Float) row[4];
            float depth = (Float) row[5];
            float weirdness = (Float) row[6];
            float offset = (Float) row[7];

            built.add(new MultiNoiseBiomeSourceParameterList.ParameterPoint(
                    Climate.parameters(
                            point(temperature),
                            point(humidity),
                            point(continentalness),
                            point(erosion),
                            point(depth),
                            point(weirdness),
                            offset),
                    holder));
        }

        seedPoints = Collections.unmodifiableList(built);
        injected = true;
        BiomesUnseen.LOGGER.info(
                "Biomes Unseen: resolved {} seeded Overworld biome parameter points", built.size());
    }

    /**
     * One noise coordinate, widened into a band.
     *
     * An exact value would confine the biome to a single hyperplane of noise
     * space, which reads as one thin stripe across the world rather than a
     * place. Widening it gives the biome a real footprint while keeping it
     * inside the climate the designer authored.
     */
    private static Climate.Parameter point(float value) {
        float spread = 0.075F;
        return Climate.parameter(value - spread, value + spread);
    }

    /** The resolved points, for the biome source to append. */
    public static List<MultiNoiseBiomeSourceParameterList.ParameterPoint> seedPoints() {
        return seedPoints;
    }

    /** Whether {@link #inject} has already run. */
    public static boolean hasInjected() {
        return injected;
    }
}
