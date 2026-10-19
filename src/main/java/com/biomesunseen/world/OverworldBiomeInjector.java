package com.biomesunseen.world;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.init.BUBiomes;
import com.biomesunseen.init.BUContent;
import net.minecraft.core.Registry;
import net.minecraft.core.RegistryAccess;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.level.biome.Biome;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Resolves the twelve seeded Overworld biomes for worldgen injection.
 *
 * <p>1.20.1 places Overworld biomes by sampling a fixed list of climate
 * parameter points held in
 * {@code MultiNoiseBiomeSourceParameterList.Preset#OVERWORLD}. A biome that is
 * registered but absent from that list never generates, no matter how complete
 * its worldgen JSON is -- which is why this class exists.
 *
 * <p>It does the part that needs a live server: confirming each authored biome
 * actually exists in the loaded registry and caching its noise parameters. The
 * splice into the vanilla list happens in the biome-source mixin, which is the
 * only place that has to touch the climate API directly. Keeping that surface
 * in one class means an API change costs one file, not two.
 *
 * <p>The parameters come from {@code BUContent.SEEDED_OVERWORLD_PARAMETERS},
 * generated from the content tables. Authoring the numbers in the biome table
 * rather than here is what lets a designer move a biome around the Overworld
 * without touching Java.
 */
public final class OverworldBiomeInjector {

    /**
     * One resolved seeded biome.
     *
     * Deliberately plain data -- no Minecraft types -- so this class compiles
     * against nothing but the registry lookup it performs.
     */
    public static final class SeedBiome {
        public final String id;
        public final ResourceKey<Biome> key;
        public final float temperature;
        public final float humidity;
        public final float continentalness;
        public final float erosion;
        public final float depth;
        public final float weirdness;
        public final float offset;

        SeedBiome(String id, ResourceKey<Biome> key, float temperature, float humidity,
                  float continentalness, float erosion, float depth, float weirdness,
                  float offset) {
            this.id = id;
            this.key = key;
            this.temperature = temperature;
            this.humidity = humidity;
            this.continentalness = continentalness;
            this.erosion = erosion;
            this.depth = depth;
            this.weirdness = weirdness;
            this.offset = offset;
        }
    }

    private static List<SeedBiome> seeds = Collections.emptyList();
    private static boolean injected;

    private OverworldBiomeInjector() {
    }

    /**
     * Resolve the seeded biomes against the loaded registry.
     *
     * Called on ServerAboutToStart, the first moment the biome registry is
     * populated -- a biome key cannot be confirmed to exist before then.
     */
    public static void inject(MinecraftServer server) {
        if (injected) {
            return;
        }
        RegistryAccess access = server.registryAccess();
        Registry<Biome> biomes = access.registryOrThrow(
                net.minecraft.core.registries.Registries.BIOME);

        List<SeedBiome> resolved = new ArrayList<>();
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
            if (biomes.getHolder(key).isEmpty()) {
                BiomesUnseen.LOGGER.error(
                        "Seeded Overworld biome {} is not defined by the datapack; skipping", id);
                continue;
            }
            resolved.add(new SeedBiome(id, key,
                    (Float) row[1], (Float) row[2], (Float) row[3], (Float) row[4],
                    (Float) row[5], (Float) row[6], (Float) row[7]));
        }

        seeds = Collections.unmodifiableList(resolved);
        injected = true;
        BiomesUnseen.LOGGER.info(
                "Biomes Unseen: resolved {} seeded Overworld biome(s) for injection", seeds.size());
    }

    /** The resolved seeds, for the biome source to splice in. */
    public static List<SeedBiome> seeds() {
        return seeds;
    }

    public static boolean hasInjected() {
        return injected;
    }
}
