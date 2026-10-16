package com.biomesunseen.util;

import com.biomesunseen.BiomesUnseen;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Level-of-detail cache for distant structure starts.  Structure placement
 * queries outside the configured radius are answered from this LRU cache
 * instead of re-running noise/placement code every chunk tick.
 */
public final class LodCache {

    private static final int MAX_ENTRIES = 4096;
    private static final Map<Long, Boolean> STRUCTURE_PRESENCE =
            new LinkedHashMap<Long, Boolean>(256, 0.75F, true) {
                @Override
                protected boolean removeEldestEntry(Map.Entry<Long, Boolean> eldest) {
                    return size() > MAX_ENTRIES;
                }
            };

    private LodCache() {
    }

    /** Chunk-radius within which structure starts are fully resolved. */
    public static int lodRadius() {
        int v = BiomesUnseen.config().structureLodDistance;
        return v < 16 ? 16 : v;
    }

    /** True when a chunk is within the full-resolution band. */
    public static boolean isHighDetail(long chunkX, long chunkZ, long cameraX, long cameraZ) {
        long dx = chunkX - cameraX;
        long dz = chunkZ - cameraZ;
        long r = lodRadius() >> 4;
        return dx * dx + dz * dz <= r * r;
    }

    /** Cached structure-presence query (chunk key packed as x/z). */
    public static Boolean cachedPresence(long chunkKey, java.util.function.Supplier<Boolean> compute) {
        synchronized (STRUCTURE_PRESENCE) {
            Boolean value = STRUCTURE_PRESENCE.get(chunkKey);
            if (value != null) {
                return value;
            }
        }
        Boolean computed = compute.get();
        synchronized (STRUCTURE_PRESENCE) {
            STRUCTURE_PRESENCE.put(chunkKey, computed);
        }
        return computed;
    }

    /** Pack a chunk position into a cache key. */
    public static long chunkKey(int chunkX, int chunkZ) {
        return ((long) chunkX << 32) ^ (chunkZ & 0xFFFFFFFFL);
    }

    /** Drop all cached entries (called on dimension unload). */
    public static void invalidate() {
        synchronized (STRUCTURE_PRESENCE) {
            STRUCTURE_PRESENCE.clear();
        }
    }
}
