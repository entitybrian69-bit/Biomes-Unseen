package com.biomesunseen.fabric.client;

import com.biomesunseen.BiomesUnseen;

import net.fabricmc.api.ClientModInitializer;

/**
 * Fabric client entrypoint: animated renderers, particles, config screen.
 */
public class BiomesUnseenFabricClient implements ClientModInitializer {

    @Override
    public void onInitializeClient() {
        BiomesUnseen.initClient();
    }
}
