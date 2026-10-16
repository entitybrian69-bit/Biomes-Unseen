package com.biomesunseen.registry;

import net.minecraft.block.Block;
import net.minecraft.entity.EntityType;
import net.minecraft.item.Item;
import net.minecraft.particles.ParticleType;
import net.minecraft.util.SoundEvent;
import net.minecraft.util.registry.Registry;

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
            DeferredRegister.create(MOD_ID, Registry.BLOCK);
    public static final DeferredRegister<Item> ITEMS =
            DeferredRegister.create(MOD_ID, Registry.ITEM);
    public static final DeferredRegister<EntityType<?>> ENTITIES =
            DeferredRegister.create(MOD_ID, Registry.ENTITY_TYPE);
    public static final DeferredRegister<SoundEvent> SOUNDS =
            DeferredRegister.create(MOD_ID, Registry.SOUND_EVENT);
    public static final DeferredRegister<ParticleType<?>> PARTICLES =
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
