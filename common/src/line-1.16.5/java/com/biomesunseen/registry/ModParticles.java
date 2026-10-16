package com.biomesunseen.registry;

import net.minecraft.particles.BasicParticleType;
import net.minecraft.particles.ParticleType;

import com.biomesunseen.core.CoreRegistries;
import com.biomesunseen.core.ModConstants;

import me.shedaniel.architectury.registry.RegistrySupplier;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * All 8 custom particle types (crystal sparks, embers, void motes, ...).
 */
public final class ModParticles {

    public static final Map<String, RegistrySupplier<ParticleType<?>>> BY_ID =
            new LinkedHashMap<String, RegistrySupplier<ParticleType<?>>>();

    static {
        for (int i = 0; i < CoreRegistries.PARTICLE_IDS.size(); i++) {
            String id = CoreRegistries.PARTICLE_IDS.get(i);
            BY_ID.put(id, PARTICLES.register(id, () -> new BasicParticleType(true)));
        }
    }

    private ModParticles() {
    }

    public static void registerContent() {
        // Static initializers populate BY_ID.
    }

    public static ParticleType<?> byId(String id) {
        RegistrySupplier<ParticleType<?>> supplier = BY_ID.get(id);
        return supplier == null ? null : supplier.get();
    }

    public static java.util.Set<String> allIds() {
        return Collections.unmodifiableSet(BY_ID.keySet());
    }
}
