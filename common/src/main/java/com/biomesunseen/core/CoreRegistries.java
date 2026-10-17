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
            "heal_glow",
            "hollow_mote",
            "aurora_dust",
            "glitch_spark"
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
            "block.biomesunseen.ember_crackle",
            "ambient.biomesunseen.hollow_deep_loop",
            "music.biomesunseen.hollow_deep_theme",
            "entity.biomesunseen.glowmoth.ambient",
            "ambient.biomesunseen.aetherfall_loop",
            "music.biomesunseen.aetherfall_theme",
            "entity.biomesunseen.dawnfinch.ambient",
            "ambient.biomesunseen.void_between_loop",
            "music.biomesunseen.void_between_theme",
            "entity.biomesunseen.glitchling.ambient",
            "music.biomesunseen.heart_of_the_forest_phase1",
            "music.biomesunseen.heart_of_the_forest_phase2",
            "music.biomesunseen.heart_of_the_forest_phase3",
            "music.biomesunseen.heart_of_the_forest_phase4",
            "music.biomesunseen.void_serpent_phase1",
            "music.biomesunseen.void_serpent_phase2",
            "music.biomesunseen.void_serpent_phase3",
            "music.biomesunseen.void_serpent_phase4",
            "music.biomesunseen.warden_of_the_hollow_deep_phase1",
            "music.biomesunseen.warden_of_the_hollow_deep_phase2",
            "music.biomesunseen.warden_of_the_hollow_deep_phase3",
            "music.biomesunseen.warden_of_the_hollow_deep_phase4",
            "music.biomesunseen.the_skyward_crown_phase1",
            "music.biomesunseen.the_skyward_crown_phase2",
            "music.biomesunseen.the_skyward_crown_phase3",
            "music.biomesunseen.the_skyward_crown_phase4",
            "music.biomesunseen.the_unraveling_phase1",
            "music.biomesunseen.the_unraveling_phase2",
            "music.biomesunseen.the_unraveling_phase3",
            "music.biomesunseen.the_unraveling_phase4"
    }));

    /** Advancement ids in unlock order. */
    public static final List<String> ADVANCEMENT_IDS = Collections.unmodifiableList(Arrays.asList(new String[]{
            "root",
            "biome_explorer",
            "biome_master",
            "first_ore",
            "all_ores",
            "first_structure",
            "all_structures",
            "heart_of_the_forest",
            "void_serpent",
            "tame_mob",
            "all_mobs",
            "boss_hunter",
            "enter_hollow_deep",
            "enter_aetherfall",
            "enter_void_between",
            "warden_of_the_hollow_deep",
            "the_skyward_crown",
            "the_unraveling",
            "boss_master"
    }));

    private CoreRegistries() {
    }

    public static String particleKey(String id) {
        return ModConstants.NAMESPACE + id;
    }
}
