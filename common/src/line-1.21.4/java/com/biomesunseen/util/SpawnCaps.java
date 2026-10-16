package com.biomesunseen.util;

import com.biomesunseen.BiomesUnseen;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Global custom-mob cap enforcement.  Loaded counts are tracked per dimension
 * and checked before every spawn so mob farms cannot flood the server.
 */
public final class SpawnCaps {

    private static final Map<String, AtomicInteger> COUNTS = new ConcurrentHashMap<String, AtomicInteger>();
    private static volatile int cap = 180;

    private SpawnCaps() {
    }

    static {
        reload();
    }

    /** Re-read the cap from config (called when the config changes). */
    public static void reload() {
        int v = BiomesUnseen.config().mobGlobalCap;
        cap = v < 0 ? 0 : v;
    }

    /** True when a custom mob may spawn in this dimension. */
    public static boolean allowSpawn(String dimensionKey) {
        AtomicInteger counter = COUNTS.get(dimensionKey);
        if (counter == null) {
            counter = new AtomicInteger();
            COUNTS.put(dimensionKey, counter);
        }
        return counter.get() < cap;
    }

    /** Track a spawn. */
    public static void onSpawn(String dimensionKey) {
        AtomicInteger counter = COUNTS.get(dimensionKey);
        if (counter == null) {
            counter = new AtomicInteger();
            COUNTS.put(dimensionKey, counter);
        }
        counter.incrementAndGet();
    }

    /** Track a death/despawn. */
    public static void onRemoved(String dimensionKey) {
        AtomicInteger counter = COUNTS.get(dimensionKey);
        if (counter != null) {
            counter.updateAndGet(v -> v > 0 ? v - 1 : 0);
        }
    }

    public static int currentCount(String dimensionKey) {
        AtomicInteger counter = COUNTS.get(dimensionKey);
        return counter == null ? 0 : counter.get();
    }
}
