package com.biomesunseen.client;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.client.particle.BUAmbientParticle;
import com.biomesunseen.client.render.BUBossRenderer;
import com.biomesunseen.client.render.BUCreatureRenderer;
import com.biomesunseen.init.BUBlocks;
import com.biomesunseen.init.BUContent;
import com.biomesunseen.init.BUEntities;
import com.biomesunseen.init.BUParticles;
import net.minecraft.client.renderer.ItemBlockRenderTypes;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.EntityRenderers;
import net.minecraft.core.particles.ParticleType;
import net.minecraft.core.particles.SimpleParticleType;
import net.minecraft.world.entity.EntityType;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.EntityRenderersEvent;
import net.minecraftforge.client.event.RegisterParticleProvidersEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.FMLClientSetupEvent;
import net.minecraftforge.registries.RegistryObject;
import net.minecraft.world.level.material.Fluid;

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
     * Bind a provider to every registered particle type.
     *
     * A {@link ParticleType} that is registered but has no provider cannot be
     * instantiated on the client: {@code ParticleEngine} finds no factory and the
     * particle simply does not appear, with a warning logged per spawn attempt.
     * Because 63 biomes name one of these in their effects block, that would
     * repeat continuously for as long as a player stood in any of them, and every
     * hand-authored sprite under {@code textures/particle} would stay unloaded.
     *
     * Driven by the registry rather than written out per type, so a particle
     * authored in {@code BUContent.PARTICLES} is bound on the next codegen run and
     * cannot be silently forgotten.
     */
    @SubscribeEvent
    public static void registerParticles(RegisterParticleProvidersEvent event) {
        int bound = 0;
        for (RegistryObject<ParticleType<?>> holder : BUParticles.all()) {
            ParticleType<?> type = holder.get();
            if (type == null) {
                BiomesUnseen.LOGGER.error("Particle type {} resolved to null", holder.getId());
                continue;
            }
            if (registerAmbient(event, holder.getId().getPath(), type)) {
                bound++;
            }
        }
        BiomesUnseen.LOGGER.info("Biomes Unseen: bound {} ambient particle providers", bound);
    }

    /**
     * Give every liquid a translucent chunk render layer.
     *
     * Forge resolves a fluid's layer through {@code ItemBlockRenderTypes
     * #getRenderLayer(FluidState)}, which looks the state's fluid up in a map
     * seeded only with vanilla's water and lava and otherwise defaults to
     * {@code RenderType#solid()}. Fluids are not reached by the model-level
     * {@code render_type} field that our block models use for cutout flora and
     * translucent portals -- that path feeds the block's layer, while a liquid's
     * block model is particle-only and the fluid renderer draws the volume.
     * Without this call all four liquids mesh into the solid layer, where there
     * is no blending, so hollow_water and the rest would read as painted glass
     * cubes rather than liquid.
     *
     * Both the source and the flowing fluid of every set are registered, because
     * the lookup keys on the state's own fluid type and a spreading liquid is a
     * {@code Flowing} state rather than a {@code Source} one. Iterating the
     * registry rather than naming four ids is what keeps a fifth liquid authored
     * in {@code BUContent.BLOCKS_FLUID} from being silently left opaque.
     *
     * {@code setRenderLayer} asserts {@code ClientModLoader.isLoading()} and
     * throws otherwise, so this must run from {@code FMLClientSetupEvent} -- not
     * from a constructor, a static initialiser, or a common-setup event.
     */
    @SubscribeEvent
    public static void registerFluidLayers(FMLClientSetupEvent event) {
        int bound = 0;
        for (RegistryObject<Fluid> holder : BUBlocks.FLUIDS.getEntries()) {
            Fluid fluid = holder.get();
            if (fluid == null) {
                BiomesUnseen.LOGGER.error("Fluid {} resolved to null", holder.getId());
                continue;
            }
            ItemBlockRenderTypes.setRenderLayer(fluid, RenderType.translucent());
            bound++;
        }
        BiomesUnseen.LOGGER.info("Biomes Unseen: gave {} fluids a translucent render layer", bound);
    }

    /**
     * Bind one type to {@link BUAmbientParticle}.
     *
     * {@code registerSpriteSet} is generic over {@code T extends ParticleOptions}
     * while the registry hands back {@code ParticleType<?>}, so the cast is
     * confined here and guarded by an instanceof rather than scattered through the
     * loop. Every type registered by {@link BUParticles} is a
     * {@link SimpleParticleType} by construction; the check exists so a future
     * type carrying extra data fails loudly here instead of being skipped.
     */
    @SuppressWarnings("unchecked")
    private static boolean registerAmbient(RegisterParticleProvidersEvent event,
                                           String id, ParticleType<?> type) {
        if (!(type instanceof SimpleParticleType)) {
            BiomesUnseen.LOGGER.error(
                    "Particle {} is not a SimpleParticleType, so it has no ambient provider", id);
            return false;
        }
        event.registerSpriteSet((ParticleType<SimpleParticleType>) type,
                                BUAmbientParticle.Provider::new);
        return true;
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
