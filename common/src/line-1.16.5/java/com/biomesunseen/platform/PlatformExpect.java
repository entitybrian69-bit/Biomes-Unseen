package com.biomesunseen.platform;

import java.lang.reflect.Method;

/**
 * Loader-specific hooks.  Each platform module ships
 * com.biomesunseen.platform.PlatformExpectImpl with the concrete behaviour;
 * this bridge dispatches to it reflectively so no annotation processor or
 * extra library is needed at compile time.
 */
public final class PlatformExpect {

    private static final Class<?> IMPL = loadImpl();

    private PlatformExpect() {
    }

    private static Class<?> loadImpl() {
        try {
            return Class.forName("com.biomesunseen.platform.PlatformExpectImpl");
        } catch (ClassNotFoundException e) {
            throw new IllegalStateException("PlatformExpectImpl is missing", e);
        }
    }

    private static Object call(String name, Object... args) {
        try {
            for (Method m : IMPL.getMethods()) {
                if (m.getName().equals(name) && m.getParameterCount() == args.length) {
                    return m.invoke(null, args);
                }
            }
            throw new IllegalStateException("No PlatformExpectImpl." + name + " with "
                    + args.length + " arguments");
        } catch (ReflectiveOperationException e) {
            throw new IllegalStateException("PlatformExpectImpl." + name + " failed", e);
        }
    }

    /** True when running on Fabric. */
    public static boolean isFabric() {
        return Boolean.TRUE.equals(call("isFabric"));
    }

    /** True when running on Forge or NeoForge. */
    public static boolean isForgeLike() {
        return Boolean.TRUE.equals(call("isForgeLike"));
    }

    /** Loader config directory (contains biomesunseen.json). */
    public static String configDirectory() {
        return (String) call("configDirectory");
    }

    /** Open the Cloth Config screen for Biomes Unseen. */
    public static void openConfigScreen(Object parentScreen) {
        call("openConfigScreen", parentScreen);
    }

    /**
     * Register spawn placements for one mob id (ground/monster/water rules
     * handled by the platform entity spawn API).
     */
    public static void registerSpawnPlacement(String mobId,
            net.minecraft.entity.EntityType<net.minecraft.entity.MobEntity> type) {
        call("registerSpawnPlacement", mobId, type);
    }

    /** Inject every custom biome into the overworld climate system. */
    public static void installBiomeInjection() {
        call("installBiomeInjection");
    }

    /** Register biome modification hooks (features, spawns, ambience). */
    public static void installBiomeModifications() {
        call("installBiomeModifications");
    }

    /** Play a global music disc-style track inside a boss arena. */
    public static void playBossMusic(net.minecraft.world.server.ServerWorld level,
            net.minecraft.util.math.BlockPos center, String soundEventId, int radius) {
        call("playBossMusic", level, center, soundEventId, radius);
    }

    /** True when the given mod id is loaded (used for optional compat). */
    public static boolean isModLoaded(String modId) {
        return Boolean.TRUE.equals(call("isModLoaded", modId));
    }
}
