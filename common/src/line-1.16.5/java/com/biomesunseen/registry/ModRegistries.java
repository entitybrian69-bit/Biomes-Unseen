package com.biomesunseen.registry;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.item.Item;
import net.minecraft.core.particles.ParticleType;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.core.Registry;

import com.biomesunseen.core.ModConstants;

import me.shedaniel.architectury.registry.DeferredRegister;

/**
 * Every Architectury DeferredRegister used by Biomes Unseen.  Registration
 * order matters: entities before items so spawn eggs can resolve their
 * EntityType at construction time.
 */
public final class ModRegistries {

    public static final String MOD_ID = ModConstants.MOD_ID;

    public static final DeferredRegister<Block> BLOCKS =
            DeferredRegister.create(MOD_ID, Registry.BLOCK_REGISTRY);
    public static final DeferredRegister<Item> ITEMS =
            DeferredRegister.create(MOD_ID, Registry.ITEM_REGISTRY);
    public static final DeferredRegister<EntityType<?>> ENTITIES =
            DeferredRegister.create(MOD_ID, Registry.ENTITY_TYPE_REGISTRY);
    public static final DeferredRegister<SoundEvent> SOUNDS =
            DeferredRegister.create(MOD_ID, Registry.SOUND_EVENT_REGISTRY);
    public static final DeferredRegister<ParticleType<?>> PARTICLES =
            DeferredRegister.create(MOD_ID, Registry.PARTICLE_TYPE_REGISTRY);

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
