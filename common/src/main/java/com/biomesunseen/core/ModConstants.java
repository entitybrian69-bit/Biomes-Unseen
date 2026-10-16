package com.biomesunseen.core;

/**
 * Immutable mod metadata shared by every loader and Minecraft version.
 */
public final class ModConstants {

    public static final String MOD_ID = "biomesunseen";
    public static final String MOD_NAME = "Biomes Unseen";
    public static final String MOD_VERSION = "1.0.0";
    public static final String MOD_DESCRIPTION = "A massive world-generation, adventure, biome, structure, ore, mob and boss mod.";
    public static final String MOD_LICENSE = "MIT";
    public static final String MOD_AUTHORS = "Biomes Unseen Team";

    /** Root resource namespace, e.g. "biomesunseen:crystal_spire_reach". */
    public static final String NAMESPACE = MOD_ID + ":";

    /** Config file name used by the JSON config store. */
    public static final String CONFIG_FILE = "biomesunseen.json";

    private ModConstants() {
    }
}
