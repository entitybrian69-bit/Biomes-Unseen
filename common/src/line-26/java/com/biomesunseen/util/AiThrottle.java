package com.biomesunseen.util;

import com.biomesunseen.BiomesUnseen;

/**
 * Central AI throttling.  Custom mobs only think every N ticks (config
 * "entityAiThrottle"), which keeps large mob counts cheap without making
 * behaviour visibly stiff: goals still run on their own cadence.
 */
public final class AiThrottle {

    private AiThrottle() {
    }

    /** Effective think interval in ticks, minimum 1. */
    public static int interval() {
        int v = BiomesUnseen.config().entityAiThrottle;
        return v < 1 ? 1 : v;
    }

    /**
     * True when the entity with the given id should think this tick.
     * Deterministic stagger spreads decisions across the interval.
     */
    public static boolean shouldThink(int entityId, long gameTime) {
        int interval = interval();
        return ((gameTime + (entityId % interval)) % interval) == 0L;
    }

    /** Reduced goal-flag evaluation for throttled entities. */
    public static boolean cheapCanUse(int entityId, long gameTime, int cost) {
        if (cost <= 1) {
            return true;
        }
        return shouldThink(entityId, gameTime);
    }
}
