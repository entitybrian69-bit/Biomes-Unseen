package com.biomesunseen.platform;

import me.shedaniel.architectury.injectables.annotations.ExpectPlatform;

/**
 * Loader-specific hooks.  Each platform module ships
 * com.biomesunseen.platform.PlatformExpectImpl with the concrete behaviour.
 */
public final class PlatformExpect {

    private PlatformExpect() {
    }

    /** True when running on Fabric. */
    @ExpectPlatform
    public static boolean isFabric() {
        throw new AssertionError();
    }

    /** True when running on Forge or NeoForge. */
    @ExpectPlatform
    public static boolean isForgeLike() {
        throw new AssertionError();
    }

    /** Loader config directory (contains biomesunseen.json). */
    @ExpectPlatform
    public static String configDirectory() {
        throw new AssertionError();
    }

    /** Open the Cloth Config screen for Biomes Unseen. */
    @ExpectPlatform
    public static void openConfigScreen(Object parentScreen) {
        throw new AssertionError();
    }

    /**
     * Register spawn placements for one mob id (ground/monster/water rules
     * handled by the platform entity spawn API).
     */
    @ExpectPlatform
    public static void registerSpawnPlacement(String mobId,
            net.minecraft.entity.EntityType<net.minecraft.entity.MobEntity> type) {
        throw new AssertionError();
    }

    /** Inject every custom biome into the overworld climate system. */
    @ExpectPlatform
    public static void installBiomeInjection() {
        throw new AssertionError();
    }

    /** Register biome modification hooks (features, spawns, ambience). */
    @ExpectPlatform
    public static void installBiomeModifications() {
        throw new AssertionError();
    }

    /** Play a global music disc-style track inside a boss arena. */
    @ExpectPlatform
    public static void playBossMusic(net.minecraft.world.server.ServerWorld level,
            net.minecraft.util.math.BlockPos center, String soundEventId, int radius) {
        throw new AssertionError();
    }

    /** True when the given mod id is loaded (used for optional compat). */
    @ExpectPlatform
    public static boolean isModLoaded(String modId) {
        throw new AssertionError();
    }
}
