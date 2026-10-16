package com.biomesunseen.forge;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.platform.PlatformExpect;

import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.FMLClientSetupEvent;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.fml.loading.FMLEnvironment;

/**
 * Forge entrypoint for Biomes Unseen.
 */
@Mod("biomesunseen")
public class BiomesUnseenForge {

    public BiomesUnseenForge() {
        BiomesUnseen.init();
        IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();
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
