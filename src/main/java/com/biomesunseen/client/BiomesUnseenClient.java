package com.biomesunseen.client;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.client.render.BUBossRenderer;
import com.biomesunseen.client.render.BUCreatureRenderer;
import com.biomesunseen.init.BUContent;
import com.biomesunseen.init.BUEntities;
import net.minecraft.client.renderer.entity.EntityRenderers;
import net.minecraft.world.entity.EntityType;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.EntityRenderersEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/**
 * Client-side registration.
 *
 * Every one of the 85 entity types gets a renderer bound here. Registration is
 * driven by the generated content table rather than written out per species, so
 * a new creature authored in tools/content/mobs.py is rendered on the next
 * codegen run without a change in this file -- and, more importantly, cannot be
 * silently forgotten, which would leave it invisible in game.
 *
 * Runs on the mod event bus and only on the physical client, so a dedicated
 * server never loads the renderer classes.
 */
@Mod.EventBusSubscriber(modid = BiomesUnseen.MODID, value = Dist.CLIENT, bus = Mod.EventBusSubscriber.Bus.MOD)
public final class BiomesUnseenClient {

    private BiomesUnseenClient() {
    }

    /**
     * Bind a renderer to every registered entity type.
     *
     * Bosses get {@link BUBossRenderer} (their own 64x64 atlas and multi-part
     * rig) and everything else gets {@link BUCreatureRenderer} (the shared
     * family rig with a per-species texture).
     */
    @SubscribeEvent
    public static void registerRenderers(EntityRenderersEvent.RegisterRenderers event) {
        int creatures = 0;
        int bosses = 0;
        for (com.biomesunseen.entity.MobData data : BUContent.MOBS) {
            EntityType<?> type = BUEntities.entityType(data.id);
            if (type == null) {
                BiomesUnseen.LOGGER.error("No entity type registered for creature {}", data.id);
                continue;
            }
            registerCreature(event, type);
            creatures++;
        }
        for (com.biomesunseen.entity.BossData data : BUContent.BOSSES) {
            EntityType<?> type = BUEntities.entityType(data.id);
            if (type == null) {
                BiomesUnseen.LOGGER.error("No entity type registered for boss {}", data.id);
                continue;
            }
            registerBoss(event, type);
            bosses++;
        }
        BiomesUnseen.LOGGER.info("Biomes Unseen: bound renderers for {} creatures and {} bosses",
                creatures, bosses);
    }

    /**
     * Type-safe bridge to {@link EntityRenderersEvent#registerEntityRenderer}.
     *
     * The event's method is generic over the entity class, and the registry
     * hands back {@code EntityType<?>}, so the unchecked cast is isolated here
     * with a suppression rather than scattered through the loop.
     */
    @SuppressWarnings({"unchecked", "rawtypes"})
    private static void registerCreature(EntityRenderersEvent.RegisterRenderers event,
                                        EntityType<?> type) {
        event.registerEntityRenderer((EntityType) type, BUCreatureRenderer::new);
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    private static void registerBoss(EntityRenderersEvent.RegisterRenderers event,
                                    EntityType<?> type) {
        event.registerEntityRenderer((EntityType) type, BUBossRenderer::new);
    }
}
