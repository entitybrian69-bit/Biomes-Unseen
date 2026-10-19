package com.biomesunseen.init;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Every sound the mod registers: biome music tracks, dimension ambience and
 * the five boss themes.
 *
 * The ids come from the generated table, which collects them from the biome and
 * boss content tables -- so a biome that names a music track is guaranteed to
 * have a registered SoundEvent behind it, and a track that nothing references is
 * never registered.
 *
 * Sound ids in the content tables are dotted ("music.ethereal", "ambient.drip")
 * and are registered under exactly that path, because ResourceLocation paths
 * permit dots and the biome worldgen JSON references them verbatim.
 */
public final class BUSounds {

    public static final DeferredRegister<SoundEvent> SOUNDS =
            DeferredRegister.create(ForgeRegistries.SOUND_EVENTS, BUContent.MODID);

    /** Keyed by the authored (dotted) id, as the content tables spell it. */
    private static final Map<String, RegistryObject<SoundEvent>> BY_ID = new LinkedHashMap<>();

    private BUSounds() {
    }

    public static void register(IEventBus bus) {
        for (String id : BUContent.SOUNDS) {
            ResourceLocation location = new ResourceLocation(BUContent.MODID, pathFor(id));
            BY_ID.put(id, SOUNDS.register(pathFor(id),
                    () -> SoundEvent.createVariableRangeEvent(location)));
        }
        SOUNDS.register(bus);
    }

    /**
     * Registry path for an authored sound id.
     *
     * Passed through unchanged: ResourceLocation paths permit dots, and the
     * biome worldgen JSON references these ids verbatim, so rewriting them here
     * would register a SoundEvent no biome can find.
     */
    private static String pathFor(String id) {
        return id;
    }

    /** The registered event for an authored id, or null if it does not exist. */
    public static SoundEvent get(String id) {
        RegistryObject<SoundEvent> holder = BY_ID.get(id);
        return holder == null ? null : holder.get();
    }

    public static boolean contains(String id) {
        return BY_ID.containsKey(id);
    }

    public static java.util.Collection<RegistryObject<SoundEvent>> all() {
        return BY_ID.values();
    }
}
