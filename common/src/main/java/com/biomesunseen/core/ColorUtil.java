package com.biomesunseen.core;

/**
 * Integer color helpers used by particles, spawn eggs and biome tinting.
 */
public final class ColorUtil {

    private ColorUtil() {
    }

    public static int red(int color) {
        return (color >> 16) & 0xFF;
    }

    public static int green(int color) {
        return (color >> 8) & 0xFF;
    }

    public static int blue(int color) {
        return color & 0xFF;
    }

    /** Pack r/g/b (0..255) into a 0xRRGGBB int. */
    public static int rgb(int r, int g, int b) {
        return ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF);
    }

    /** Scale a colour toward white (factor > 1) or black (factor < 1). */
    public static int shade(int color, double factor) {
        int r = clamp((int) (red(color) * factor));
        int g = clamp((int) (green(color) * factor));
        int b = clamp((int) (blue(color) * factor));
        return rgb(r, g, b);
    }

    /** Linearly interpolate two packed colours; t in [0,1]. */
    public static int lerp(int a, int b, double t) {
        int r = (int) (red(a) + (red(b) - red(a)) * t);
        int g = (int) (green(a) + (green(b) - green(a)) * t);
        int bl = (int) (blue(a) + (blue(b) - blue(a)) * t);
        return rgb(r, g, bl);
    }

    /** Stable hue jitter derived from a string key, in [0,1). */
    public static double jitter(String key) {
        return Content.stableHash(key) / 255.0;
    }

    private static int clamp(int v) {
        return v < 0 ? 0 : (v > 255 ? 255 : v);
    }
}
