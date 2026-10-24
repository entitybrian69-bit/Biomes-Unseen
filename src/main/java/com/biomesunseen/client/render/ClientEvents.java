package com.biomesunseen.client.render;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.registry.ModEntities;
import com.biomesunseen.spec.MobSpec;
import com.biomesunseen.spec.Specs;
import net.minecraft.client.renderer.entity.EntityRenderersEvent;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = BiomesUnseen.MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class ClientEvents {
    private ClientEvents() {
    }

    @SubscribeEvent
    public static void registerRenderers(EntityRenderersEvent.RegisterRenderers event) {
        event.registerEntityRenderer(ModEntities.HOLLOW_STALKER.get(), HollowStalkerRenderer::new);
        event.registerEntityRenderer(ModEntities.SPORELING.get(), SporelingRenderer::new);
        event.registerEntityRenderer(ModEntities.GLOOM_CRAWLER.get(), GloomCrawlerRenderer::new);
        event.registerEntityRenderer(ModEntities.CRYSTAL_GOLEM.get(), CrystalGolemRenderer::new);
        event.registerEntityRenderer(ModEntities.MIRE_WRAITH.get(), MireWraithRenderer::new);
        event.registerEntityRenderer(ModEntities.HEART_OF_THE_FOREST.get(), HeartOfTheForestRenderer::new);
        for (MobSpec spec : Specs.mobs()) {
            event.registerEntityRenderer(ModEntities.SPEC_MOBS.get(spec.id()).get(),
                    context -> new SpecMobRenderer(context, spec));
        }
    }
}
