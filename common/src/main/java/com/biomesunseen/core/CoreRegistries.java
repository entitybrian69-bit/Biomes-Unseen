package com.biomesunseen.core;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * Static id tables for particles, sound events and advancements.  The
 * platform registries and datagen providers consume these so ids never drift.
 */
public final class CoreRegistries {

    /** Particle type ids (without namespace). */
    public static final List<String> PARTICLE_IDS = Collections.unmodifiableList(Arrays.asList(new String[]{
            "crystal_spark",
            "ember_flake",
            "void_mote",
            "spore_drift",
            "frost_mote",
            "storm_arc",
            "petal_burst",
            "heal_glow"
    }));

    /** Sound event ids (full "event.path" form used by sounds.json). */
    public static final List<String> SOUND_EVENT_IDS = Collections.unmodifiableList(Arrays.asList(new String[]{
            "ambient.biomesunseen.crystal_loop",
            "ambient.biomesunseen.ember_loop",
            "ambient.biomesunseen.verdant_loop",
            "ambient.biomesunseen.frost_loop",
            "ambient.biomesunseen.storm_loop",
            "ambient.biomesunseen.mire_loop",
            "ambient.biomesunseen.sky_loop",
            "ambient.biomesunseen.void_loop",
            "music.biomesunseen.crystal_theme",
            "music.biomesunseen.ember_theme",
            "music.biomesunseen.verdant_theme",
            "music.biomesunseen.frost_theme",
            "music.biomesunseen.storm_theme",
            "music.biomesunseen.mire_theme",
            "music.biomesunseen.sky_theme",
            "music.biomesunseen.void_theme",
            "music.biomesunseen.boss_heart",
            "music.biomesunseen.boss_serpent",
            "subtitles.biomesunseen.heart_roar",
            "subtitles.biomesunseen.serpent_hiss",
            "entity.biomesunseen.lumox.ambient",
            "entity.biomesunseen.lumox.hurt",
            "entity.biomesunseen.lumox.death",
            "entity.biomesunseen.heart_of_the_forest.ambient",
            "entity.biomesunseen.heart_of_the_forest.hurt",
            "entity.biomesunseen.heart_of_the_forest.death",
            "entity.biomesunseen.void_serpent.ambient",
            "entity.biomesunseen.void_serpent.hurt",
            "entity.biomesunseen.void_serpent.death",
            "block.biomesunseen.ore_chime",
            "block.biomesunseen.crystal_resonate",
            "block.biomesunseen.mire_step",
            "block.biomesunseen.ember_crackle"
    }));

    /** Advancement ids in unlock order. */
    public static final List<String> ADVANCEMENT_IDS = Collections.unmodifiableList(Arrays.asList(new String[]{
            "root"
            "biome_explorer"
            "biome_master"
            "first_ore"
            "all_ores"
            "first_structure"
            "all_structures"
            "heart_of_the_forest"
            "void_serpent"
            "tame_mob"
            "all_mobs"
            "boss_hunter"
    }));

    private CoreRegistries() {
    }

    public static String particleKey(String id) {
        return ModConstants.NAMESPACE + id;
    }
}
