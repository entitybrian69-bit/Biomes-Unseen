package com.biomesunseen.registry;

import net.minecraft.core.particles.SimpleParticleType;
import net.minecraft.core.particles.ParticleType;

import com.biomesunseen.core.CoreRegistries;
import com.biomesunseen.core.ModConstants;

import dev.architectury.registry.registries.RegistrySupplier;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * All 8 custom particle types (crystal sparks, embers, void motes, ...).
 */
public final class ModParticles {

    public static final Map<String, RegistrySupplier<ParticleType<SimpleParticleType>>> BY_ID =
            new LinkedHashMap<String, RegistrySupplier<ParticleType<SimpleParticleType>>>();

    static {
        for (int i = 0; i < CoreRegistries.PARTICLE_IDS.size(); i++) {
            String id = CoreRegistries.PARTICLE_IDS.get(i);
            BY_ID.put(id, narrow(ModRegistries.PARTICLES.register(id, () -> newSimple())));
        }
    }

    /**
     * The vanilla simple particle type keeps its constructor protected, so the
     * eight Biomes Unseen types are instantiated reflectively - this keeps the
     * registration code identical on every API line.
     */
    private static SimpleParticleType newSimple() {
        try {
            java.lang.reflect.Constructor<SimpleParticleType> ctor =
                    SimpleParticleType.class.getDeclaredConstructor(boolean.class);
            ctor.setAccessible(true);
            return ctor.newInstance(Boolean.TRUE);
        } catch (ReflectiveOperationException e) {
            throw new IllegalStateException("Cannot build particle type", e);
        }
    }

    private ModParticles() {
    }

    public static void registerContent() {
        // Static initializers populate BY_ID.
    }

    /** The particle register is declared with a wildcard; narrow it for typed lookups. */
    @SuppressWarnings("unchecked")
    private static RegistrySupplier<ParticleType<SimpleParticleType>> narrow(RegistrySupplier<?> supplier) {
        return (RegistrySupplier) supplier;
    }

    public static ParticleType<?> byId(String id) {
        RegistrySupplier<ParticleType<SimpleParticleType>> supplier = BY_ID.get(id);
        return supplier == null ? null : supplier.get();
    }

    public static java.util.Set<String> allIds() {
        return Collections.unmodifiableSet(BY_ID.keySet());
    }
}
