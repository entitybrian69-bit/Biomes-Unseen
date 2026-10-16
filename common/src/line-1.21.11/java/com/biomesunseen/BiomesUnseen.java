package com.biomesunseen;

import com.biomesunseen.config.ModConfig;
import com.biomesunseen.registry.ModRegistries;
import com.biomesunseen.worldgen.ModWorldGen;
import com.biomesunseen.core.ModConstants;

/**
 * Common bootstrap shared by every loader entrypoint for Minecraft 1.21.11.
 * Loaders call {@link #init()} during mod construction, {@link #setup()} at
 * registry freeze and {@link #initClient()} from the client entrypoint.
 */
public final class BiomesUnseen {

    public static final String MOD_ID = ModConstants.MOD_ID;

    private static ModConfig config = ModConfig.createDefault();
    private static boolean initialized;

    private BiomesUnseen() {
    }

    /** Loader-agnostic mod construction: registers and config. */
    public static synchronized void init() {
        if (initialized) {
            return;
        }
        initialized = true;
        config = ModConfig.load();
        ModRegistries.registerAll();
        ModWorldGen.prepare();
    }

    /** Registry-freeze phase: worldgen hooks, spawn caps, boss arenas. */
    public static void setup() {
        ModWorldGen.install();
    }

    /** Client-only phase: renderers, particles, config screen. */
    public static void initClient() {
        com.biomesunseen.client.ClientSetup.init();
    }

    public static ModConfig config() {
        return config;
    }

    /** Replace the live config (used by the Cloth Config save hook). */
    public static void setConfig(ModConfig newConfig) {
        config = newConfig;
        ModConfig.save(config);
        com.biomesunseen.util.SpawnCaps.reload();
    }

    public static String versionString() {
        return ModConstants.MOD_VERSION;
    }
}
