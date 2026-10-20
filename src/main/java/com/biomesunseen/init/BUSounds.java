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

    /**
     * The registered event for an authored id, or null if it does not exist.
     *
     * Accepts either the bare id the content tables use ("music.ethereal") or a
     * fully qualified one ("biomesunseen:music.ethereal"). Both forms occur: the
     * biome JSONs and BossData carry qualified ids, while the registry keys are
     * bare. Normalising here is what stops a lookup silently missing -- a
     * qualified id passed to a bare-keyed map returns null rather than throwing,
     * so boss music would simply never play and nothing would report it.
     */
    public static SoundEvent get(String id) {
        if (id == null) {
            return null;
        }
        String bare = id.indexOf(':') >= 0 ? id.substring(id.indexOf(':') + 1) : id;
        RegistryObject<SoundEvent> holder = BY_ID.get(bare);
        return holder == null ? null : holder.get();
    }

    /**
     * Whether a sound id ships real audio.
     *
     * Registering a SoundEvent whose id has no sounds.json definition is
     * harmless, but starting it makes the client log "Unable to play unknown
     * soundEvent" -- for boss music that is once per sighting, and for biome
     * music every 12-24 seconds per player. Playback is therefore gated on this
     * rather than on registration.
     *
     * The list is generated from which .ogg files actually exist, so dropping a
     * track in and re-running the generators switches it on with no Java edit.
     */
    public static boolean hasAudio(String id) {
        if (id == null) {
            return false;
        }
        String bare = id.indexOf(':') >= 0 ? id.substring(id.indexOf(':') + 1) : id;
        for (String shipped : BUContent.SOUNDS_WITH_AUDIO) {
            if (shipped.equals(bare)) {
                return true;
            }
        }
        return false;
    }

    public static boolean contains(String id) {
        if (id == null) {
            return false;
        }
        String bare = id.indexOf(':') >= 0 ? id.substring(id.indexOf(':') + 1) : id;
        return BY_ID.containsKey(bare);
    }

    public static java.util.Collection<RegistryObject<SoundEvent>> all() {
        return BY_ID.values();
    }
}
