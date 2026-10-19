package com.biomesunseen.init;

import net.minecraft.core.particles.ParticleType;
import net.minecraft.core.particles.SimpleParticleType;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Ambient biome particles.
 *
 * These are {@link SimpleParticleType}s: they carry no extra data, which is the
 * right shape for drifting motes, spores and embers. Each biome names one in
 * its effects block, and the sprite is a hand-authored 16x16 texture under
 * textures/particle rather than a recolor of a vanilla puff.
 */
public final class BUParticles {

    public static final DeferredRegister<ParticleType<?>> PARTICLES =
            DeferredRegister.create(ForgeRegistries.PARTICLE_TYPES, BUContent.MODID);

    private static final Map<String, RegistryObject<ParticleType<?>>> BY_ID = new LinkedHashMap<>();

    private BUParticles() {
    }

    public static void register(IEventBus bus) {
        for (String id : BUContent.PARTICLES) {
            // true = always visible, so a biome's ambience reads even at low
            // particle settings; the density is still governed by the biome JSON.
            BY_ID.put(id, PARTICLES.register(id, () -> new SimpleParticleType(true)));
        }
        PARTICLES.register(bus);
    }

    public static ParticleType<?> get(String id) {
        RegistryObject<ParticleType<?>> holder = BY_ID.get(id);
        return holder == null ? null : holder.get();
    }

    public static boolean contains(String id) {
        return BY_ID.containsKey(id);
    }

    public static java.util.Collection<RegistryObject<ParticleType<?>>> all() {
        return BY_ID.values();
    }
}
