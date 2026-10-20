package com.biomesunseen;

import com.biomesunseen.entity.BUBoss;
import com.biomesunseen.entity.BUCreature;
import com.biomesunseen.init.BUBiomes;
import com.biomesunseen.init.BUBlocks;
import com.biomesunseen.init.BUContent;
import com.biomesunseen.init.BUCreativeTabs;
import com.biomesunseen.init.BUDimensions;
import com.biomesunseen.init.BUEntities;
import com.biomesunseen.init.BUItems;
import com.biomesunseen.init.BUParticles;
import com.biomesunseen.init.BUSounds;
import com.mojang.logging.LogUtils;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import org.slf4j.Logger;
import software.bernie.geckolib.GeckoLib;
import terrablender.api.Regions;
import terrablender.api.SurfaceRuleManager;
import com.biomesunseen.world.BUOverworldRegion;
import com.biomesunseen.world.BUOverworldSurfaceRules;

/**
 * Biomes Unseen -- entry point.
 *
 * A total-conversion worldgen expansion: 140 biomes across four dimensions,
 * 264 blocks, 285 items, 85 creatures, 115 jigsaw structures and five
 * multi-phase bosses.
 *
 * The registries here are thin. All content ids live in the generated
 * {@link com.biomesunseen.init.BUContent} table, which is produced from
 * tools/content/* and is the same source the JSON resources and textures were
 * generated from -- so the Java, the datapack and the art cannot disagree about
 * what exists.
 */
@Mod(BiomesUnseen.MODID)
public class BiomesUnseen {

    public static final String MODID = "biomesunseen";
    public static final Logger LOGGER = LogUtils.getLogger();

    public BiomesUnseen() {
        IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();

        BUBlocks.register(modBus);
        BUItems.register(modBus);
        BUEntities.register(modBus);
        BUSounds.register(modBus);
        BUParticles.register(modBus);
        BUCreativeTabs.register(modBus);

        // Biomes, dimensions and structures are data-driven in 1.20.1: the JSON
        // under data/biomesunseen/worldgen supplies the objects, and these
        // classes only hold the ResourceKeys the Java side needs to point at.
        BUBiomes.init();
        BUDimensions.init();

        // GeckoLib must be initialised before any GeckoEntity is constructed,
        // otherwise the animation cache is never attached.
        GeckoLib.initialize();

        modBus.addListener(this::commonSetup);
        modBus.addListener(BUEntities::registerAttributes);
        MinecraftForge.EVENT_BUS.register(this);

        LOGGER.info("Biomes Unseen loaded: {} blocks, {} items, {} creatures, {} bosses, {} biomes",
                BUBlocks.all().size(), BUItems.all().size(), BUContent.MOBS.length,
                BUContent.BOSSES.length, BUBiomes.all().size());
    }

    /**
     * Register the Overworld region and its surface rules with TerraBlender.
     *
     * Both have to happen in common setup and on the mod thread: TerraBlender
     * assembles the Overworld's blended parameter list once the biome registry is
     * populated, and the surface rules resolve their blocks from that same
     * frozen registry. Doing either earlier would register a region whose biome
     * keys cannot yet be confirmed to exist.
     */
    private void commonSetup(final FMLCommonSetupEvent event) {
        event.enqueueWork(() -> {
            Regions.register(new BUOverworldRegion());
            SurfaceRuleManager.addSurfaceRules(
                    SurfaceRuleManager.RuleCategory.OVERWORLD, MODID,
                    BUOverworldSurfaceRules.makeRules());
            LOGGER.info("Biomes Unseen common setup complete");
        });
    }
}
