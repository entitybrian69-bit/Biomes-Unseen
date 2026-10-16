package com.biomesunseen.fabric;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.platform.PlatformExpect;

import net.fabricmc.api.ModInitializer;

/**
 * Fabric entrypoint for Biomes Unseen.
 */
public class BiomesUnseenFabric implements ModInitializer {

    @Override
    public void onInitialize() {
        BiomesUnseen.init();
        BiomesUnseen.setup();
    }
}
