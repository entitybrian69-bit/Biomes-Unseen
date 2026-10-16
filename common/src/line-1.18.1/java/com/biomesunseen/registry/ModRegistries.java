package com.biomesunseen.registry;

import net.minecraft.core.Registry;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.core.ModConstants;

import dev.architectury.registry.DeferredRegister;

/**
 * Every Architectury DeferredRegister used by Biomes Unseen.  Registration
 * order matters: entities before items so spawn eggs can resolve their
 * EntityType at construction time.
 */
public final class ModRegistries {

    public static final String MOD_ID = ModConstants.MOD_ID;

    public static final DeferredRegister<net.minecraft.world.level.block.Block> BLOCKS =
            DeferredRegister.create(MOD_ID, Registry.BLOCK);
    public static final DeferredRegister<net.minecraft.world.item.Item> ITEMS =
            DeferredRegister.create(MOD_ID, Registry.ITEM);
    public static final DeferredRegister<net.minecraft.world.entity.EntityType<?>> ENTITIES =
            DeferredRegister.create(MOD_ID, Registry.ENTITY_TYPE);
    public static final DeferredRegister<net.minecraft.sounds.SoundEvent> SOUNDS =
            DeferredRegister.create(MOD_ID, Registry.SOUND_EVENT);
    public static final DeferredRegister<net.minecraft.core.particles.ParticleType<?>> PARTICLES =
            DeferredRegister.create(MOD_ID, Registry.PARTICLE_TYPE);

    private ModRegistries() {
    }

    /** Kick every deferred register, then populate the content holders. */
    public static void registerAll() {
        ENTITIES.register();
        BLOCKS.register();
        ITEMS.register();
        SOUNDS.register();
        PARTICLES.register();
        ModEntities.registerContent();
        ModBlocks.registerContent();
        ModItems.registerContent();
        ModSounds.registerContent();
        ModParticles.registerContent();
    }
}
