package com.biomesunseen.neoforge;

import com.biomesunseen.BiomesUnseen;

import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.fml.loading.FMLEnvironment;

/**
 * NeoForge entrypoint for Biomes Unseen.
 */
@Mod("biomesunseen")
public class BiomesUnseenNeoForge {

    public BiomesUnseenNeoForge(IEventBus modBus) {
        BiomesUnseen.init();
        modBus.addListener(this::onCommonSetup);
        if (FMLEnvironment.dist == Dist.CLIENT) {
            modBus.addListener(this::onClientSetup);
        }
    }

    private void onCommonSetup(FMLCommonSetupEvent event) {
        event.enqueueWork(BiomesUnseen::setup);
    }

    private void onClientSetup(FMLClientSetupEvent event) {
        event.enqueueWork(BiomesUnseen::initClient);
    }
}
