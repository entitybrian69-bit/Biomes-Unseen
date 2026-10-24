package com.biomesunseen;

import com.biomesunseen.registry.ModBlocks;
import com.biomesunseen.registry.ModCreativeTabs;
import com.biomesunseen.registry.ModEntities;
import com.biomesunseen.registry.ModItems;
import com.biomesunseen.registry.ModSounds;
import com.biomesunseen.worldgen.ModTerraBlender;
import com.mojang.logging.LogUtils;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import org.slf4j.Logger;

@Mod(BiomesUnseen.MOD_ID)
public class BiomesUnseen {
    public static final String MOD_ID = "biomesunseen";
    public static final Logger LOGGER = LogUtils.getLogger();

    public BiomesUnseen() {
        IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();
        ModBlocks.register(modBus);
        ModItems.register(modBus);
        ModSounds.register(modBus);
        ModEntities.register(modBus);
        ModCreativeTabs.register(modBus);
        modBus.addListener(this::commonSetup);
    }

    private void commonSetup(final FMLCommonSetupEvent event) {
        event.enqueueWork(ModTerraBlender::register);
        LOGGER.info("Biomes Unseen: common setup");
    }
}
