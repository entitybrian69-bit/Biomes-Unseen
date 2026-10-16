package com.biomesunseen.core;

/**
 * Small numeric helpers shared by worldgen and entity AI code.
 */
public final class MathUtil {

    private MathUtil() {
    }

    public static double clamp(double v, double min, double max) {
        return v < min ? min : (v > max ? max : v);
    }

    public static int clamp(int v, int min, int max) {
        return v < min ? min : (v > max ? max : v);
    }

    /** Smoothstep in [0,1] for a value in [edge0, edge1]. */
    public static double smoothstep(double edge0, double edge1, double x) {
        double t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0);
        return t * t * (3.0 - 2.0 * t);
    }

    /** Deterministic 2D value noise in [0,1] (cached-free, cheap). */
    public static double valueNoise2d(int x, int y, int seed) {
        int n = x * 374761393 + y * 668265263 + seed * 1274126177;
        n = (n ^ (n >> 13)) * 1274126177;
        n = n ^ (n >> 16);
        return ((n & 0x7FFFFFFF) / (double) 0x7FFFFFFF);
    }

    /** Weighted pick using cumulative weights; indexWeights must be non-empty. */
    public static int weightedPick(double[] cumulativeWeights, double roll) {
        for (int i = 0; i < cumulativeWeights.length; i++) {
            if (roll <= cumulativeWeights[i]) {
                return i;
            }
        }
        return cumulativeWeights.length - 1;
    }
}
