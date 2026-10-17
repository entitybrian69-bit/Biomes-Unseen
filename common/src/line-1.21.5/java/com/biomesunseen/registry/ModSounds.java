package com.biomesunseen.registry;

import net.minecraft.sounds.SoundEvent;
import net.minecraft.resources.ResourceLocation;

import com.biomesunseen.core.CoreRegistries;
import com.biomesunseen.core.ModConstants;

import dev.architectury.registry.registries.RegistrySupplier;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * All 62 sound events: biome ambience, music, mob calls and block sounds.
 */
public final class ModSounds {

    public static final Map<String, RegistrySupplier<SoundEvent>> BY_ID =
            new LinkedHashMap<String, RegistrySupplier<SoundEvent>>();

    static {
        for (int i = 0; i < CoreRegistries.SOUND_EVENT_IDS.size(); i++) {
            String id = CoreRegistries.SOUND_EVENT_IDS.get(i);
            BY_ID.put(id, ModRegistries.SOUNDS.register(id, () -> SoundEvent.createVariableRangeEvent(net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(ModConstants.MOD_ID, id))));
        }
    }

    private ModSounds() {
    }

    public static void registerContent() {
        // Static initializers populate BY_ID.
    }

    /** Resolve a sound event by its sounds.json key (e.g. "music.biomesunseen.boss_heart"). */
    public static SoundEvent byId(String id) {
        RegistrySupplier<SoundEvent> supplier = BY_ID.get(id);
        return supplier == null ? null : supplier.get();
    }

    public static java.util.Set<String> allIds() {
        return Collections.unmodifiableSet(BY_ID.keySet());
    }
}
