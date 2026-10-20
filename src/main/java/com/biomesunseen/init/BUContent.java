package com.biomesunseen.init;

import com.biomesunseen.entity.BossData;
import com.biomesunseen.entity.BossData.PhaseData;
import com.biomesunseen.entity.MobData;

/**
 * GENERATED FILE -- do not edit by hand.
 *
 * Produced by tools/generate_java.py from tools/content/* and tools/registry.py.
 * Regenerate with:  python3 tools/generate_java.py
 *
 * This class is pure data. It is the single source of truth the Java
 * registries loop over, so the registries, the JSON resources and the emitted
 * textures can never disagree about which ids exist. Adding a biome, ore, mob
 * or gear set to the content tables makes it appear here on the next run, and
 * the registration loops in BUBlocks / BUItems / BUEntities pick it up with no
 * further code changes.
 */
public final class BUContent {

    public static final String MODID = "biomesunseen";

    private BUContent() {
    }

    // ------------------------------------------------------------------
    //  BLOCKS
    // ------------------------------------------------------------------
    /** Plain six-faced cubes: stone, loam, planks, ore hosts. */
    public static final String[] BLOCKS_CUBE = {
            "abyssal_silt", "abyssite_block", "aether_leaves", "aether_loam", "aether_planks",
            "aetherfall_portal_frame", "aetherstone", "amber_loam", "ancient_rune_block", "ashen_core_stone",
            "ashen_dirt", "ashen_stone", "basaltic_hollowstone", "blight_leaves", "blight_loam",
            "blight_planks", "blight_stone", "bloomglass_stone", "brine_mud", "chrono_grit", "cinder_sand",
            "cloudstone", "crystal_dirt", "crystal_leaves", "dawn_marble", "emberquartz_stone",
            "fracture_shale", "frost_silt", "frostvein_stone", "gilded_aetherstone", "glimmerleaf_leaves",
            "glimmerleaf_stone", "glitch_concrete", "glitch_loam", "gloomslate", "graveamber_stone",
            "hollow_deep_portal_frame", "hollow_leaves", "hollow_loam", "hollow_planks", "hollow_silt",
            "hollow_stone", "lumen_dirt", "lumen_leaves", "lumen_planks", "lumen_sand", "mossy_umberstone",
            "mycelial_slimestone", "null_basalt", "obsidian_grit", "parchment_silt", "petrichorite_stone",
            "petrified_dirt", "petrified_leaves", "petrified_planks", "petrified_wood_stone",
            "pyroclast_stone", "river_gravel", "root_loam", "rootiron_stone", "runeglass_grit",
            "sakura_leaves", "sakura_planks", "salt_crust", "salt_flat_hardpan", "scorched_hardpan",
            "shard_grit", "slag_stone", "spiritwood_leaves", "spiritwood_planks", "spiritwood_stone",
            "spore_chalk", "spore_loam", "spore_sand", "sporeamber_stone", "static_stone", "stormcell_stone",
            "sulphur_crust", "sunbleached_dirt", "sunbleached_sand", "sunbleached_stone", "sunken_stone",
            "sunscorch_hardpan", "sunscorch_stone", "sunspore_stone", "tide_sand", "tideglass_sand",
            "titanite_gravel", "twilight_shale", "umber_dirt", "umberstone", "verdant_stone", "void_leaves",
            "void_loam", "void_planks", "void_portal_frame", "voidstone", "wet_silt", "witherite_stone"
        };


    /** Turf blocks: authored top over an authored side/substrate. */
    public static final String[] BLOCKS_GRASS = {
            "aether_grass_block", "ash_grass_block", "blight_grass_block", "crystal_grass_block",
            "hollow_grass_block", "lumen_grass_block", "mossy_umber_grass", "petrified_grass_block",
            "spore_grass_block", "sunbleached_grass_block", "tidegrass_block", "umber_grass_block",
            "void_grass_block"
        };


    /** Pillars with a distinct end grain (axis-property blockstates). */
    public static final String[] BLOCKS_LOG = {
            "aether_log", "blight_log", "hollow_log", "lumen_log", "petrified_log", "sakura_log",
            "spiritwood_log", "void_log"
        };


    /** Ore blocks: Fortune-aware drop, Silk Touch alternative. */
    public static final String[] BLOCKS_ORE = {
            "aetherium_ore", "ashen_core_ore", "basaltic_hollow_core_ore", "bloodstone_ore", "chronosite_ore",
            "coralite_ore", "dawnshard_ore", "deep_pearl_ore", "deepslate_ashen_core_ore",
            "deepslate_bloodstone_ore", "deepslate_coralite_ore", "deepslate_emberquartz_ore",
            "deepslate_frostbloom_ore", "deepslate_glacierite_ore", "deepslate_glimmerleaf_ore",
            "deepslate_graveamber_ore", "deepslate_kelpstone_ore", "deepslate_lumenite_ore",
            "deepslate_petrichorite_ore", "deepslate_rootiron_ore", "deepslate_spiritwood_ore",
            "deepslate_sporeamber_ore", "deepslate_stormcell_ore", "deepslate_sunscorch_ore",
            "deepslate_tideglass_ore", "deepslate_titanite_ore", "deepslate_umbrite_ore",
            "deepslate_wraithsalt_ore", "duskite_ore", "echo_crystal_ore", "emberquartz_ore",
            "fracture_shale_ore", "frostbloom_ore", "glacierite_ore", "glacierite_void_ore", "glimmerleaf_ore",
            "gloomite_ore", "graveamber_ore", "hollowite_ore", "kelpstone_ore", "lumenite_ore",
            "lumenshade_ore", "moonpetal_ore", "mycelium_ore", "nullite_ore", "petrichorite_ore",
            "root_heart_ore", "rootiron_ore", "runeglass_ore", "skylead_ore", "spiritwood_ore",
            "sporeamber_ore", "starfall_ore", "staticite_ore", "stormcell_aether_ore", "stormcell_ore",
            "sunscorch_ore", "sunspore_ore", "tideglass_ore", "titanite_ore", "umbrite_ore", "voidsteel_ore",
            "witherite_ore", "wraithsalt_ore"
        };


    /** Compressed storage blocks (9x material recipe). */
    public static final String[] BLOCKS_MINERAL = {
            "aetherium_block", "ashen_core_block", "basaltic_hollow_core_block", "bloodstone_block",
            "chronosite_block", "coralite_block", "dawnshard_block", "deep_pearl_block", "duskite_block",
            "echo_crystal_block", "emberquartz_block", "fracture_shale_block", "frostbloom_block",
            "glacierite_block", "glacierite_void_block", "glimmerleaf_block", "gloomite_block",
            "graveamber_block", "hollowite_block", "kelpstone_block", "lumenite_block", "lumenshade_block",
            "moonpetal_block", "mycelium_block", "nullite_block", "petrichorite_block", "root_heart_block",
            "rootiron_block", "runeglass_block", "skylead_block", "spiritwood_block", "sporeamber_block",
            "starfall_block", "staticite_block", "stormcell_aether_block", "stormcell_block",
            "sunscorch_block", "sunspore_block", "tideglass_block", "titanite_block", "umbrite_block",
            "voidsteel_block", "witherite_block", "wraithsalt_block"
        };


    /** Flora: single cutout cross, no collision. */
    public static final String[] BLOCKS_FLORA = {
            "aether_crystal_spike", "aether_sapling", "aurora_fern", "blight_sapling", "blight_tendril",
            "bloodcap_cluster", "glimmerleaf_sprout", "glowcap_cluster", "hollow_crystal_spike",
            "hollow_sapling", "lumen_fern", "lumen_sapling", "marigold", "moonpetal_bush", "orchid_bloom",
            "petrified_sapling", "sakura_blossom", "sakura_sapling", "spiritwood_sapling", "sporecap_cluster",
            "starfall_bloom", "sunspore_pod", "tide_kelp", "void_crystal_spike", "void_sapling",
            "void_tendril", "voidcap_cluster"
        };


    /** Dimension gates: no collision, translucent, no item form. */
    public static final String[] BLOCKS_PORTAL = {
            "aetherfall_portal", "hollow_deep_portal", "void_portal"
        };


    /** Emissive cubes that light their surroundings. */
    public static final String[] BLOCKS_LANTERN = {
            "bioluminescent_lantern"
        };


    /** Pillar-shaped interactive block (boss summoning). */
    public static final String[] BLOCKS_ALTAR = {
            "boss_altar"
        };


    /** Grass block -> the substrate it shows underneath and drops. */
    public static final String[][] GRASS_SUBSTRATE = {
            { "aether_grass_block", "aether_loam" },
            { "ash_grass_block", "ashen_dirt" },
            { "blight_grass_block", "blight_loam" },
            { "crystal_grass_block", "crystal_dirt" },
            { "hollow_grass_block", "hollow_loam" },
            { "lumen_grass_block", "lumen_dirt" },
            { "mossy_umber_grass", "umber_dirt" },
            { "petrified_grass_block", "petrified_dirt" },
            { "spore_grass_block", "root_loam" },
            { "sunbleached_grass_block", "sunbleached_dirt" },
            { "tidegrass_block", "wet_silt" },
            { "umber_grass_block", "umber_dirt" },
            { "void_grass_block", "void_loam" },
    };

    /** Log block -> the planks it crafts into. */
    public static final String[][] LOG_TO_PLANKS = {
            { "aether_log", "aether_planks" },
            { "blight_log", "blight_planks" },
            { "hollow_log", "hollow_planks" },
            { "lumen_log", "lumen_planks" },
            { "petrified_log", "petrified_planks" },
            { "sakura_log", "sakura_planks" },
            { "spiritwood_log", "spiritwood_planks" },
            { "void_log", "void_planks" },
    };

    /** Fluid blocks, registered with a real ForgeFlowingFluid. */
    public static final String[] BLOCKS_FLUID = {
            "aether_essence", "hollow_water", "lumen_water", "void_fluid"
        };

    // ------------------------------------------------------------------
    //  ITEMS
    // ------------------------------------------------------------------
    /** Crafting materials: ore drops, refined ingots, mob drops, boss components. */
    public static final String[] ITEMS_MATERIALS = {
            "abyssite_shard", "aetherium_ingot", "aetherium_refined", "ashen_core_fragment", "basaltic_core",
            "biomesunseen_tab_icon", "bloodstone_gem", "bloomglass_pane", "chronosite_core", "claw",
            "coralite_polish", "crown_shard", "dawnshard", "deep_pearl", "duskite_gem", "echo_crystal",
            "emberquartz_shard", "fang", "feather", "fracture_shale_shard", "frostbloom_bloom",
            "glacierite_shard", "glimmerleaf_fiber", "gloomite_shard", "graveamber_chunk", "heart_fruit",
            "heart_of_the_forest_artefact", "heart_of_the_forest_seed", "heartwood_core", "hollowite_gem",
            "hollowite_refined", "kelpstone_raw", "kelpstone_shard", "lore_fragment", "lumenite_shard",
            "lumenshade_ingot", "lumenshade_refined", "moonpetal", "mushroom_cap", "music_disc_unseen",
            "mycelium_culture", "nullite_refined", "nullite_shard", "petrichorite_crystal", "portal_igniter",
            "reality_compass", "root_heart_fragment", "rootiron_ingot", "rootiron_refined", "runeglass_pane",
            "scale", "serpent_fang", "skylead_ingot", "skyward_crown_regalia", "spiritwood_splinter",
            "spore_pod", "sporeamber_chunk", "starfall_core", "staticite_cell", "stormcell_core",
            "sunscorch_ingot", "the_skyward_crown_artefact", "the_unraveling_artefact", "tideglass_pane",
            "titanite_plate", "umbrite", "umbrite_raw", "unraveling_core", "unraveling_paradox",
            "void_serpent_artefact", "void_serpent_scale", "voidsteel_ingot", "warden_carapace",
            "warden_of_the_hollow_deep_artefact", "warden_of_the_hollow_deep_sigil", "witherite_dust",
            "wraithsalt_crystal"
        };


    /** Tools, bows and shields; the tier comes from GEAR_TIER via the set prefix. */
    public static final String[] ITEMS_TOOLS = {
            "aetherium_axe", "aetherium_bow", "aetherium_hoe", "aetherium_pickaxe", "aetherium_shovel",
            "aetherium_sword", "chronos_axe", "chronos_bow", "chronos_hoe", "chronos_pickaxe",
            "chronos_shield", "chronos_shovel", "chronos_sword", "gloomsteel_axe", "gloomsteel_hoe",
            "gloomsteel_pickaxe", "gloomsteel_shield", "gloomsteel_shovel", "gloomsteel_sword",
            "hollowite_axe", "hollowite_bow", "hollowite_hoe", "hollowite_pickaxe", "hollowite_shovel",
            "hollowite_sword", "lumenshade_axe", "lumenshade_bow", "lumenshade_hoe", "lumenshade_pickaxe",
            "lumenshade_shovel", "lumenshade_sword", "nullite_axe", "nullite_bow", "nullite_hoe",
            "nullite_pickaxe", "nullite_shield", "nullite_shovel", "nullite_sword", "pyroclast_axe",
            "pyroclast_hoe", "pyroclast_pickaxe", "pyroclast_shield", "pyroclast_shovel", "pyroclast_sword",
            "rootiron_axe", "rootiron_bow", "rootiron_hoe", "rootiron_pickaxe", "rootiron_shield",
            "rootiron_shovel", "rootiron_sword", "starforged_axe", "starforged_bow", "starforged_hoe",
            "starforged_pickaxe", "starforged_shield", "starforged_shovel", "starforged_sword",
            "voidstone_axe", "voidstone_bow", "voidstone_hoe", "voidstone_pickaxe", "voidstone_shield",
            "voidstone_shovel", "voidstone_sword"
        };


    /** Boss artefact weapons, crafted from a boss core. */
    public static final String[] ITEMS_ARTEFACTS = {
            "heart_of_forest_staff", "hollow_tremor_maul", "skyward_sceptre", "unraveling_conduit",
            "void_serpent_fang"
        };


    /** Written lore books; each opens a GUI page of authored text. */
    public static final String[] ITEMS_LORE_BOOKS = {
            "lore_book", "lore_book_aether", "lore_book_ancient", "lore_book_ash", "lore_book_colossus",
            "lore_book_death", "lore_book_deep", "lore_book_frost", "lore_book_grove", "lore_book_heart",
            "lore_book_hollow", "lore_book_mire", "lore_book_road", "lore_book_star", "lore_book_tide",
            "lore_book_unraveling", "lore_book_void"
        };


    /** Armour items as {itemId, setId, slot}. */
    public static final String[][] ARMOUR_ITEMS = {
            { "aetherium_boots", "aetherium", "boots" },
            { "aetherium_chestplate", "aetherium", "chestplate" },
            { "aetherium_helmet", "aetherium", "helmet" },
            { "aetherium_leggings", "aetherium", "leggings" },
            { "chronos_boots", "chronos", "boots" },
            { "chronos_chestplate", "chronos", "chestplate" },
            { "chronos_helmet", "chronos", "helmet" },
            { "chronos_leggings", "chronos", "leggings" },
            { "gloomsteel_boots", "gloomsteel", "boots" },
            { "gloomsteel_chestplate", "gloomsteel", "chestplate" },
            { "gloomsteel_helmet", "gloomsteel", "helmet" },
            { "gloomsteel_leggings", "gloomsteel", "leggings" },
            { "hollowite_boots", "hollowite", "boots" },
            { "hollowite_chestplate", "hollowite", "chestplate" },
            { "hollowite_helmet", "hollowite", "helmet" },
            { "hollowite_leggings", "hollowite", "leggings" },
            { "lumenshade_boots", "lumenshade", "boots" },
            { "lumenshade_chestplate", "lumenshade", "chestplate" },
            { "lumenshade_helmet", "lumenshade", "helmet" },
            { "lumenshade_leggings", "lumenshade", "leggings" },
            { "nullite_boots", "nullite", "boots" },
            { "nullite_chestplate", "nullite", "chestplate" },
            { "nullite_helmet", "nullite", "helmet" },
            { "nullite_leggings", "nullite", "leggings" },
            { "pyroclast_boots", "pyroclast", "boots" },
            { "pyroclast_chestplate", "pyroclast", "chestplate" },
            { "pyroclast_helmet", "pyroclast", "helmet" },
            { "pyroclast_leggings", "pyroclast", "leggings" },
            { "rootiron_boots", "rootiron", "boots" },
            { "rootiron_chestplate", "rootiron", "chestplate" },
            { "rootiron_helmet", "rootiron", "helmet" },
            { "rootiron_leggings", "rootiron", "leggings" },
            { "starforged_boots", "starforged", "boots" },
            { "starforged_chestplate", "starforged", "chestplate" },
            { "starforged_helmet", "starforged", "helmet" },
            { "starforged_leggings", "starforged", "leggings" },
            { "voidstone_boots", "voidstone", "boots" },
            { "voidstone_chestplate", "voidstone", "chestplate" },
            { "voidstone_helmet", "voidstone", "helmet" },
            { "voidstone_leggings", "voidstone", "leggings" },
    };

    /** Spawn eggs as {itemId, entityId}; the texture is per-species. */
    public static final String[][] SPAWN_EGGS = {
            { "abyssal_leviathan_spawn_egg", "abyssal_leviathan" },
            { "amber_sentinel_spawn_egg", "amber_sentinel" },
            { "astral_scribe_aether_spawn_egg", "astral_scribe_aether" },
            { "astral_scribe_spawn_egg", "astral_scribe" },
            { "aurora_stag_spawn_egg", "aurora_stag" },
            { "blighthound_spawn_egg", "blighthound" },
            { "bogcrawler_spawn_egg", "bogcrawler" },
            { "canopy_glider_spawn_egg", "canopy_glider" },
            { "canyon_skulk_spawn_egg", "canyon_skulk" },
            { "chrono_warden_spawn_egg", "chrono_warden" },
            { "cloudfin_spawn_egg", "cloudfin" },
            { "coralback_crab_spawn_egg", "coralback_crab" },
            { "crown_sentinel_spawn_egg", "crown_sentinel" },
            { "duskstalker_spawn_egg", "duskstalker" },
            { "echo_bat_spawn_egg", "echo_bat" },
            { "emberling_spawn_egg", "emberling" },
            { "fossil_wraith_spawn_egg", "fossil_wraith" },
            { "fracture_hound_spawn_egg", "fracture_hound" },
            { "frostling_spawn_egg", "frostling" },
            { "frozen_mariner_spawn_egg", "frozen_mariner" },
            { "fungal_titan_spawn_egg", "fungal_titan" },
            { "gale_harrier_spawn_egg", "gale_harrier" },
            { "garden_aberration_spawn_egg", "garden_aberration" },
            { "glacier_ox_spawn_egg", "glacier_ox" },
            { "glimmerwing_spawn_egg", "glimmerwing" },
            { "gloomstalker_spawn_egg", "gloomstalker" },
            { "glowcap_grub_spawn_egg", "glowcap_grub" },
            { "grove_warden_spawn_egg", "grove_warden" },
            { "heart_of_the_forest_spawn_egg", "heart_of_the_forest" },
            { "highland_goat_spawn_egg", "highland_goat" },
            { "hollow_drowned_spawn_egg", "hollow_drowned" },
            { "hollow_scout_spawn_egg", "hollow_scout" },
            { "kelp_serpent_spawn_egg", "kelp_serpent" },
            { "lanternkeeper_spawn_egg", "lanternkeeper" },
            { "luminous_jelly_spawn_egg", "luminous_jelly" },
            { "magma_lurker_spawn_egg", "magma_lurker" },
            { "marrow_hound_spawn_egg", "marrow_hound" },
            { "meadow_skipper_spawn_egg", "meadow_skipper" },
            { "mire_wisp_spawn_egg", "mire_wisp" },
            { "mirror_walk_spawn_egg", "mirror_walk" },
            { "moor_sentinel_spawn_egg", "moor_sentinel" },
            { "mossback_hare_spawn_egg", "mossback_hare" },
            { "mycelial_horror_spawn_egg", "mycelial_horror" },
            { "null_swimmer_spawn_egg", "null_swimmer" },
            { "orchard_tender_spawn_egg", "orchard_tender" },
            { "orchid_mantis_spawn_egg", "orchid_mantis" },
            { "petaldancer_spawn_egg", "petaldancer" },
            { "primal_cat_spawn_egg", "primal_cat" },
            { "quarry_construct_spawn_egg", "quarry_construct" },
            { "reefglider_spawn_egg", "reefglider" },
            { "rime_stag_spawn_egg", "rime_stag" },
            { "river_lamprey_spawn_egg", "river_lamprey" },
            { "roadwarden_spawn_egg", "roadwarden" },
            { "rootburrower_spawn_egg", "rootburrower" },
            { "rotstalker_spawn_egg", "rotstalker" },
            { "rune_construct_spawn_egg", "rune_construct" },
            { "savanna_strider_spawn_egg", "savanna_strider" },
            { "shardling_spawn_egg", "shardling" },
            { "shorelurker_spawn_egg", "shorelurker" },
            { "silkweaver_spawn_egg", "silkweaver" },
            { "sky_citizen_spawn_egg", "sky_citizen" },
            { "slag_golem_spawn_egg", "slag_golem" },
            { "spire_climber_spawn_egg", "spire_climber" },
            { "sporeling_deep_spawn_egg", "sporeling_deep" },
            { "sporeling_spawn_egg", "sporeling" },
            { "static_wraith_spawn_egg", "static_wraith" },
            { "steppe_rider_spawn_egg", "steppe_rider" },
            { "stonehide_boar_spawn_egg", "stonehide_boar" },
            { "stormcell_wisp_spawn_egg", "stormcell_wisp" },
            { "sunscorch_vulture_spawn_egg", "sunscorch_vulture" },
            { "temple_guardian_spawn_egg", "temple_guardian" },
            { "the_skyward_crown_spawn_egg", "the_skyward_crown" },
            { "the_unraveling_spawn_egg", "the_unraveling" },
            { "thicket_sprite_spawn_egg", "thicket_sprite" },
            { "trench_angler_spawn_egg", "trench_angler" },
            { "unraveling_shard_aether_spawn_egg", "unraveling_shard_aether" },
            { "unraveling_shard_spawn_egg", "unraveling_shard" },
            { "vault_keeper_spawn_egg", "vault_keeper" },
            { "veilmourner_spawn_egg", "veilmourner" },
            { "veilwing_spawn_egg", "veilwing" },
            { "void_scout_spawn_egg", "void_scout" },
            { "void_serpent_spawn_egg", "void_serpent" },
            { "warden_acolyte_spawn_egg", "warden_acolyte" },
            { "warden_of_the_hollow_deep_spawn_egg", "warden_of_the_hollow_deep" },
            { "warren_skitter_spawn_egg", "warren_skitter" },
    };

    // ------------------------------------------------------------------
    //  GEAR STATS
    // ------------------------------------------------------------------
    /**
     * Tool sets as {setId, tierLevel, uses, speed, attackDamageBonus,
     * enchantmentValue, repairItem}.
     *
     * tierLevel is the harvest level (1 stone .. 5 netherite-plus) and
     * drives both the Tier and the needs_x_tool tag the blocks use.
     */
    public static final Object[][] GEAR_TIER = {
            { "lumenshade", 4, 1840f, 11.0f, 4.0f, 26, "lumenshade_ingot" },
            { "voidstone", 5, 2480f, 13.0f, 6.0f, 30, "voidsteel_ingot" },
            { "aetherium", 4, 1560f, 15.0f, 4.0f, 34, "aetherium_ingot" },
            { "chronos", 5, 2100f, 12.0f, 5.0f, 40, "chronosite_core" },
            { "pyroclast", 4, 1980f, 10.0f, 7.0f, 18, "ashen_core_fragment" },
            { "hollowite", 4, 2260f, 9.0f, 5.0f, 22, "hollowite_gem" },
            { "rootiron", 3, 890f, 8.0f, 3.0f, 14, "rootiron_ingot" },
            { "gloomsteel", 4, 1720f, 11.0f, 5.0f, 20, "gloomite_shard" },
            { "nullite", 5, 3120f, 14.0f, 8.0f, 12, "nullite_shard" },
            { "starforged", 5, 2640f, 14.0f, 6.0f, 36, "starfall_core" },
    };

    /**
     * Armour sets as {setId, durabilityMultiplier, boots, leggings,
     * chestplate, helmet, toughness, knockbackResistance, repairItem,
     * setBonus}.
     *
     * The four defence values are emitted in ArmorItem.Type ordinal order
     * (BOOTS, LEGGINGS, CHESTPLATE, HELMET), which is the order
     * BUArmorMaterial.getDefenseForType indexes them by. That matches
     * ArmorSetSpec.protection, authored boots-first, so the row is a direct
     * copy of the tuple with no reordering anywhere in the chain.
     */
    public static final Object[][] GEAR_ARMOUR = {
            { "lumenshade", 42, 3, 6, 8, 3, 2.0f, 0.0f, "lumenshade_ingot", "lumenshade_glow" },
            { "voidstone", 48, 4, 7, 9, 4, 3.0f, 0.1f, "voidsteel_ingot", "voidstone_phase" },
            { "aetherium", 36, 3, 6, 8, 3, 2.5f, 0.0f, "aetherium_ingot", "aetherium_flight_assist" },
            { "chronos", 44, 4, 7, 9, 4, 3.0f, 0.15f, "chronosite_core", "chronos_haste" },
            { "pyroclast", 46, 4, 7, 9, 4, 3.5f, 0.0f, "ashen_core_fragment", "pyroclast_fire_aura" },
            { "hollowite", 50, 4, 8, 10, 4, 4.0f, 0.1f, "hollowite_gem", "hollowite_night_vision" },
            { "rootiron", 30, 2, 5, 7, 2, 1.0f, 0.0f, "rootiron_ingot", "rootiron_regeneration" },
            { "gloomsteel", 40, 3, 6, 8, 3, 2.5f, 0.1f, "gloomite_shard", "gloomsteel_invisibility" },
            { "nullite", 54, 4, 8, 10, 4, 4.5f, 0.2f, "nullite_shard", "nullite_wither_aura" },
            { "starforged", 52, 4, 8, 10, 4, 4.0f, 0.15f, "starfall_core", "starforged_luck" },
    };

    // ------------------------------------------------------------------
    //  ENTITIES
    // ------------------------------------------------------------------
    /**
     * The 80 non-boss creatures, as MobData records.
     *
     * Field order matches com.biomesunseen.entity.MobData exactly; the
     * goal tokens are resolved to real Goal instances by BUGoalFactory.
     */
    public static final MobData[] MOBS = {
            new MobData(
                    "glimmerwing", "avian", "overworld",
                    false, 8.0f, 0.34f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.5f,
                    false, false, "translucent",
                    0.25f, 64, 64,
                    new String[] {
                    "float", "fly_random", "tempt", "look_at_player", "follow_flock_leader"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "ambient", 40, 3, 6,
                    2,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    0.5f, 0.5f
            ),
            new MobData(
                    "mossback_hare", "quadruped", "overworld",
                    false, 6.0f, 0.4f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.7f,
                    false, false, "cutout",
                    0.3f, 64, 64,
                    new String[] {
                    "float", "panic", "breed", "tempt", "follow_parent", "herd_follow_leader", "eat_block",
                    "look_at_player", "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 25, 2, 4,
                    2,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    0.6f, 0.6f
            ),
            new MobData(
                    "petaldancer", "biped", "overworld",
                    false, 12.0f, 0.32f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.9f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "panic", "breed", "tempt", "follow_parent", "herd_follow_leader", "eat_block",
                    "look_at_player", "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 30, 2, 5,
                    3,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "duskstalker", "quadruped", "overworld",
                    true, 24.0f, 0.33f,
                    5.0f, 0.0f, 24.0f,
                    2.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "ambush_lie_in_wait", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 25, 1, 2,
                    8,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "sporeling", "fungal", "overworld",
                    false, 10.0f, 0.24f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.75f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "seek_shelter_from_sun", "seek_bioluminescence", "panic", "tempt", "look_at_player",
                    "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 35, 3, 6,
                    3,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "mire_wisp", "fungal", "overworld",
                    false, 8.0f, 0.3f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.55f,
                    true, false, "translucent",
                    0.2f, 64, 64,
                    new String[] {
                    "float", "fly_random", "seek_bioluminescence", "look_at_player"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "ambient", 30, 1, 3,
                    2,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "bogcrawler", "arthropod", "overworld",
                    true, 18.0f, 0.28f,
                    4.0f, 0.0f, 24.0f,
                    3.0f, 1.0f,
                    false, true, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 30, 1, 3,
                    6,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "aurora_stag", "quadruped", "overworld",
                    false, 28.0f, 0.34f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 1.25f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "panic", "breed", "tempt", "follow_parent", "herd_follow_leader", "eat_block",
                    "look_at_player", "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 18, 2, 4,
                    6,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "thicket_sprite", "biped", "overworld",
                    false, 10.0f, 0.35f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.5f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "trade_with_player", "look_at_trading_player", "panic", "tempt", "open_door",
                    "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "ambient", 20, 1, 2,
                    4,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "silkweaver", "arthropod", "overworld",
                    true, 16.0f, 0.26f,
                    3.5f, 0.0f, 24.0f,
                    0.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "ranged_attack", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
                    "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 22, 2, 3,
                    5,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "canopy_glider", "quadruped", "overworld",
                    false, 14.0f, 0.33f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.8f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "panic", "breed", "tempt", "follow_parent", "herd_follow_leader", "eat_block",
                    "look_at_player", "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 20, 1, 3,
                    4,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "frostling", "biped", "overworld",
                    true, 16.0f, 0.3f,
                    4.0f, 0.0f, 24.0f,
                    0.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 30, 2, 4,
                    5,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "glacier_ox", "quadruped", "overworld",
                    false, 40.0f, 0.24f,
                    3.0f, 0.0f, 24.0f,
                    4.0f, 1.4f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "panic", "breed", "tempt", "follow_parent", "herd_follow_leader", "eat_block",
                    "look_at_player", "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 15, 2, 4,
                    8,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "stonehide_boar", "quadruped", "overworld",
                    true, 26.0f, 0.32f,
                    5.0f, 0.0f, 24.0f,
                    5.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 20, 2, 4,
                    7,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "fossil_wraith", "biped", "overworld",
                    true, 20.0f, 0.3f,
                    5.5f, 0.0f, 24.0f,
                    0.0f, 1.0f,
                    true, false, "translucent",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 25, 1, 2,
                    8,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "marrow_hound", "quadruped", "overworld",
                    true, 22.0f, 0.38f,
                    6.0f, 0.0f, 24.0f,
                    0.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
                    "pack_call_for_help", "avoid_creeper", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 25, 2, 3,
                    7,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "temple_guardian", "biped", "overworld",
                    true, 36.0f, 0.28f,
                    7.0f, 0.0f, 24.0f,
                    6.0f, 1.3f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 20, 1, 2,
                    12,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "astral_scribe", "biped", "overworld",
                    false, 18.0f, 0.26f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.95f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "trade_with_player", "look_at_trading_player", "panic", "tempt", "open_door",
                    "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 18, 1, 1,
                    6,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "moor_sentinel", "biped", "overworld",
                    true, 34.0f, 0.25f,
                    8.0f, 0.0f, 24.0f,
                    8.0f, 1.5f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 12, 1, 1,
                    14,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "slag_golem", "biped", "overworld",
                    true, 44.0f, 0.22f,
                    9.0f, 0.0f, 24.0f,
                    10.0f, 1.6f,
                    true, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 15, 1, 1,
                    16,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "emberling", "fungal", "overworld",
                    true, 12.0f, 0.34f,
                    4.0f, 0.0f, 24.0f,
                    0.0f, 0.7f,
                    true, false, "translucent",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 32, 2, 5,
                    5,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "magma_lurker", "arthropod", "overworld",
                    true, 30.0f, 0.26f,
                    7.0f, 0.0f, 24.0f,
                    6.0f, 1.2f,
                    true, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "ambush_lie_in_wait", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 22, 1, 2,
                    10,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "canyon_skulk", "quadruped", "overworld",
                    true, 20.0f, 0.36f,
                    5.5f, 0.0f, 24.0f,
                    0.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "ambush_lie_in_wait", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 24, 1, 3,
                    7,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "sunscorch_vulture", "avian", "overworld",
                    true, 14.0f, 0.32f,
                    4.5f, 0.0f, 24.0f,
                    0.0f, 0.9f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "fly_random", "swoop_attack", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
                    "land_on_ground", "look_at_player", "follow_flock_leader"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 22, 1, 3,
                    5,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "blighthound", "quadruped", "overworld",
                    true, 24.0f, 0.37f,
                    6.0f, 0.0f, 24.0f,
                    0.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
                    "pack_call_for_help", "avoid_creeper", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 28, 2, 4,
                    8,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "rotstalker", "biped", "overworld",
                    true, 22.0f, 0.3f,
                    5.5f, 0.0f, 24.0f,
                    2.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "ambush_lie_in_wait", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 22, 1, 2,
                    7,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "reefglider", "serpent", "overworld",
                    false, 12.0f, 0.34f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.9f,
                    false, true, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "swim_random", "follow_flock_leader", "tempt", "look_at_player"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "water_creature", 40, 3, 6,
                    3,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "coralback_crab", "arthropod", "overworld",
                    true, 16.0f, 0.22f,
                    4.0f, 0.0f, 24.0f,
                    8.0f, 0.85f,
                    false, true, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "swim_random", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
                    "look_at_player"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "water_creature", 30, 2, 5,
                    5,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "shorelurker", "serpent", "overworld",
                    true, 22.0f, 0.3f,
                    5.5f, 0.0f, 24.0f,
                    0.0f, 1.0f,
                    false, true, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "swim_random", "swim_toward_player", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player", "look_at_player", "follow_flock_leader"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "water_creature", 20, 1, 2,
                    7,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "river_lamprey", "serpent", "overworld",
                    true, 10.0f, 0.36f,
                    3.5f, 0.0f, 24.0f,
                    0.0f, 0.7f,
                    false, true, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "swim_random", "swim_toward_player", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player", "look_at_player", "follow_flock_leader"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "water_creature", 25, 2, 4,
                    4,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "kelp_serpent", "serpent", "overworld",
                    true, 32.0f, 0.32f,
                    7.0f, 0.0f, 24.0f,
                    0.0f, 1.5f,
                    false, true, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "swim_random", "swim_toward_player", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player", "look_at_player", "follow_flock_leader"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "water_creature", 12, 1, 1,
                    12,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "trench_angler", "serpent", "overworld",
                    true, 28.0f, 0.28f,
                    8.0f, 0.0f, 24.0f,
                    0.0f, 1.3f,
                    false, true, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "swim_random", "swim_toward_player", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player", "look_at_player", "follow_flock_leader"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "water_creature", 28, 1, 2,
                    10,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "abyssal_leviathan", "serpent", "overworld",
                    true, 80.0f, 0.3f,
                    12.0f, 0.0f, 24.0f,
                    8.0f, 2.6f,
                    false, true, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "swim_random", "swim_toward_player", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player", "look_at_player", "follow_flock_leader"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "water_creature", 4, 1, 1,
                    60,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "highland_goat", "quadruped", "overworld",
                    false, 18.0f, 0.3f,
                    3.0f, 0.0f, 24.0f,
                    2.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "panic", "breed", "tempt", "follow_parent", "herd_follow_leader", "eat_block",
                    "look_at_player", "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 22, 2, 5,
                    4,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "gale_harrier", "avian", "overworld",
                    true, 18.0f, 0.34f,
                    5.0f, 0.0f, 24.0f,
                    0.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "fly_random", "swoop_attack", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
                    "land_on_ground", "look_at_player", "follow_flock_leader"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 20, 1, 2,
                    6,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "steppe_rider", "quadruped", "overworld",
                    false, 32.0f, 0.4f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 1.2f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "panic", "sit_when_ordered", "follow_owner", "owner_hurt_by_target", "owner_hurt_target",
                    "breed", "tempt", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 20, 2, 4,
                    6,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "savanna_strider", "biped", "overworld",
                    false, 20.0f, 0.36f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 1.35f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "panic", "breed", "tempt", "follow_parent", "herd_follow_leader", "eat_block",
                    "look_at_player", "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 22, 3, 6,
                    5,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "primal_cat", "quadruped", "overworld",
                    true, 22.0f, 0.4f,
                    6.0f, 0.0f, 24.0f,
                    0.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "ambush_lie_in_wait", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 18, 1, 2,
                    8,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "orchid_mantis", "arthropod", "overworld",
                    true, 16.0f, 0.3f,
                    6.5f, 0.0f, 24.0f,
                    0.0f, 0.9f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "ambush_lie_in_wait", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 20, 1, 1,
                    6,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "amber_sentinel", "biped", "overworld",
                    true, 30.0f, 0.26f,
                    7.0f, 0.0f, 24.0f,
                    6.0f, 1.25f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 14, 1, 1,
                    11,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "veilmourner", "biped", "overworld",
                    true, 26.0f, 0.28f,
                    6.0f, 0.0f, 24.0f,
                    3.0f, 1.0f,
                    false, false, "translucent",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 15, 1, 1,
                    10,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "roadwarden", "biped", "overworld",
                    false, 28.0f, 0.28f,
                    3.0f, 0.0f, 24.0f,
                    5.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "trade_with_player", "look_at_trading_player", "panic", "tempt", "open_door",
                    "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 12, 1, 1,
                    8,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "rootburrower", "arthropod", "overworld",
                    true, 20.0f, 0.28f,
                    5.0f, 0.0f, 24.0f,
                    4.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "ambush_lie_in_wait", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 22, 1, 3,
                    7,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "grove_warden", "biped", "overworld",
                    true, 38.0f, 0.26f,
                    7.0f, 0.0f, 24.0f,
                    6.0f, 1.4f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 18, 1, 2,
                    14,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "lanternkeeper", "biped", "overworld",
                    false, 24.0f, 0.26f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "trade_with_player", "look_at_trading_player", "panic", "tempt", "open_door",
                    "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 12, 1, 1,
                    8,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "rime_stag", "quadruped", "overworld",
                    false, 30.0f, 0.34f,
                    3.0f, 0.0f, 24.0f,
                    3.0f, 1.25f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "panic", "breed", "tempt", "follow_parent", "herd_follow_leader", "eat_block",
                    "look_at_player", "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 15, 1, 3,
                    7,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "meadow_skipper", "arthropod", "overworld",
                    false, 6.0f, 0.36f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.5f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "fly_random", "tempt", "look_at_player", "follow_flock_leader"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "ambient", 32, 3, 6,
                    1,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "frozen_mariner", "biped", "overworld",
                    true, 28.0f, 0.26f,
                    6.5f, 0.0f, 24.0f,
                    5.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 12, 1, 1,
                    10,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "luminous_jelly", "fungal", "overworld",
                    false, 10.0f, 0.24f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.8f,
                    false, true, "translucent",
                    0.4f, 64, 64,
                    new String[] {
                    "swim_random", "follow_flock_leader", "look_at_player"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "water_creature", 35, 3, 6,
                    3,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "hollow_scout", "biped", "hollow_deep",
                    false, 24.0f, 0.3f,
                    3.0f, 0.0f, 24.0f,
                    2.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "trade_with_player", "look_at_trading_player", "panic", "tempt", "open_door",
                    "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 20, 1, 2,
                    8,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "glowcap_grub", "arthropod", "hollow_deep",
                    false, 10.0f, 0.2f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.6f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "panic", "tempt", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 28, 2, 4,
                    2,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "gloomstalker", "quadruped", "hollow_deep",
                    true, 28.0f, 0.35f,
                    7.0f, 0.0f, 24.0f,
                    3.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "ambush_lie_in_wait", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 28, 1, 2,
                    9,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "sporeling_deep", "fungal", "hollow_deep",
                    false, 12.0f, 0.24f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.8f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "seek_shelter_from_sun", "seek_bioluminescence", "panic", "tempt", "look_at_player",
                    "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 38, 3, 6,
                    3,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "mycelial_horror", "fungal", "hollow_deep",
                    true, 48.0f, 0.24f,
                    9.0f, 0.0f, 24.0f,
                    4.0f, 1.7f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 10, 1, 1,
                    18,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "fungal_titan", "biped", "hollow_deep",
                    true, 56.0f, 0.22f,
                    10.0f, 0.0f, 24.0f,
                    8.0f, 2.0f,
                    true, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 8, 1, 1,
                    22,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "vault_keeper", "biped", "hollow_deep",
                    true, 34.0f, 0.26f,
                    8.0f, 0.0f, 24.0f,
                    7.0f, 1.2f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 15, 1, 1,
                    14,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "hollow_drowned", "biped", "hollow_deep",
                    true, 24.0f, 0.28f,
                    6.0f, 0.0f, 24.0f,
                    2.0f, 1.0f,
                    false, true, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "swim_random", "swim_toward_player", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player", "look_at_player", "follow_flock_leader"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "water_creature", 26, 2, 4,
                    8,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "warren_skitter", "arthropod", "hollow_deep",
                    true, 12.0f, 0.4f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.65f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
                    "pack_call_for_help", "avoid_creeper", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 40, 4, 8,
                    3,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "echo_bat", "avian", "hollow_deep",
                    true, 10.0f, 0.36f,
                    3.5f, 0.0f, 24.0f,
                    0.0f, 0.6f,
                    false, false, "translucent",
                    0.4f, 64, 64,
                    new String[] {
                    "fly_random", "swoop_attack", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
                    "land_on_ground", "look_at_player", "follow_flock_leader"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "ambient", 32, 3, 6,
                    3,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "warden_acolyte", "biped", "hollow_deep",
                    true, 36.0f, 0.27f,
                    8.5f, 0.0f, 24.0f,
                    9.0f, 1.3f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 18, 1, 2,
                    15,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "veilwing", "avian", "aetherfall",
                    false, 14.0f, 0.36f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.85f,
                    false, false, "translucent",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "fly_random", "tempt", "look_at_player", "follow_flock_leader"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "ambient", 32, 2, 5,
                    4,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "cloudfin", "serpent", "aetherfall",
                    false, 14.0f, 0.34f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.9f,
                    false, false, "translucent",
                    0.4f, 64, 64,
                    new String[] {
                    "swim_random", "follow_flock_leader", "tempt", "look_at_player"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "water_creature", 35, 3, 6,
                    3,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "crown_sentinel", "biped", "aetherfall",
                    true, 40.0f, 0.28f,
                    9.0f, 0.0f, 24.0f,
                    10.0f, 1.45f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 22, 1, 2,
                    18,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "quarry_construct", "biped", "aetherfall",
                    true, 32.0f, 0.24f,
                    8.0f, 0.0f, 24.0f,
                    8.0f, 1.3f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 18, 1, 2,
                    13,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "rune_construct", "biped", "aetherfall",
                    true, 28.0f, 0.26f,
                    7.5f, 0.0f, 24.0f,
                    6.0f, 1.15f,
                    true, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "ranged_attack", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
                    "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 18, 1, 2,
                    12,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "stormcell_wisp", "fungal", "aetherfall",
                    true, 14.0f, 0.34f,
                    5.0f, 0.0f, 24.0f,
                    0.0f, 0.65f,
                    true, false, "translucent",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "fly_random", "ranged_attack", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 26, 2, 4,
                    6,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "orchard_tender", "biped", "aetherfall",
                    false, 26.0f, 0.26f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "trade_with_player", "look_at_trading_player", "panic", "tempt", "open_door",
                    "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 14, 1, 1,
                    9,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "astral_scribe_aether", "biped", "aetherfall",
                    false, 20.0f, 0.26f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "trade_with_player", "look_at_trading_player", "panic", "tempt", "open_door",
                    "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 16, 1, 1,
                    7,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "unraveling_shard_aether", "arthropod", "aetherfall",
                    false, 18.0f, 0.3f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 0.7f,
                    false, false, "translucent",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "fly_random", "look_at_player", "follow_flock_leader"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "ambient", 20, 2, 4,
                    5,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "sky_citizen", "biped", "aetherfall",
                    false, 22.0f, 0.28f,
                    3.0f, 0.0f, 24.0f,
                    0.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "trade_with_player", "look_at_trading_player", "panic", "tempt", "open_door",
                    "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "creature", 18, 2, 3,
                    6,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "void_scout", "biped", "void_between",
                    true, 26.0f, 0.32f,
                    7.0f, 0.0f, 24.0f,
                    3.0f, 1.0f,
                    false, false, "translucent",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 20, 1, 2,
                    10,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "fracture_hound", "quadruped", "void_between",
                    true, 30.0f, 0.37f,
                    8.0f, 0.0f, 24.0f,
                    4.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
                    "pack_call_for_help", "avoid_creeper", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 30, 2, 4,
                    11,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "static_wraith", "biped", "void_between",
                    true, 24.0f, 0.3f,
                    7.5f, 0.0f, 24.0f,
                    2.0f, 1.0f,
                    true, false, "translucent",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "ranged_attack", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
                    "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 28, 1, 3,
                    10,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "garden_aberration", "fungal", "void_between",
                    true, 32.0f, 0.26f,
                    8.0f, 0.0f, 24.0f,
                    3.0f, 1.25f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 22, 1, 2,
                    13,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "null_swimmer", "serpent", "void_between",
                    true, 26.0f, 0.32f,
                    7.0f, 0.0f, 24.0f,
                    0.0f, 1.1f,
                    false, true, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "swim_random", "swim_toward_player", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player", "look_at_player", "follow_flock_leader"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "water_creature", 30, 2, 4,
                    9,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "chrono_warden", "biped", "void_between",
                    true, 42.0f, 0.27f,
                    9.5f, 0.0f, 24.0f,
                    8.0f, 1.4f,
                    true, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 16, 1, 1,
                    20,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "shardling", "arthropod", "void_between",
                    true, 12.0f, 0.4f,
                    4.0f, 0.0f, 24.0f,
                    0.0f, 0.6f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
                    "pack_call_for_help", "avoid_creeper", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 34, 3, 6,
                    4,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "spire_climber", "arthropod", "void_between",
                    true, 20.0f, 0.34f,
                    6.0f, 0.0f, 24.0f,
                    5.0f, 1.0f,
                    false, false, "cutout",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "ambush_lie_in_wait", "melee_attack", "hurt_by_target",
                    "nearest_attackable_target_player", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 26, 1, 3,
                    8,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "mirror_walk", "biped", "void_between",
                    true, 28.0f, 0.3f,
                    7.5f, 0.0f, 24.0f,
                    3.0f, 1.0f,
                    false, false, "translucent",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player", "look_at_player",
                    "random_look_around", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 20, 1, 2,
                    11,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
            new MobData(
                    "unraveling_shard", "arthropod", "void_between",
                    true, 22.0f, 0.34f,
                    6.5f, 0.0f, 24.0f,
                    2.0f, 0.8f,
                    true, false, "translucent",
                    0.4f, 64, 64,
                    new String[] {
                    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
                    "pack_call_for_help", "avoid_creeper", "look_at_player", "water_avoiding_random_stroll"
        },
                    new String[] {
                    "minecraft:player"
        },
                    "monster", 25, 2, 4,
                    9,
                    new String[] {
                    "animation.idle", "animation.walk", "animation.attack", "animation.hurt", "animation.death"
        },
                    1.0f, 1.0f
            ),
    };

    /** The 5 bosses, as BossData records with their phase machines. */
    public static final BossData[] BOSSES = {
            new BossData(
                    "heart_of_the_forest", "The Heart of the Forest", "overworld",
                    "biomesunseen:music.boss.heart_of_the_forest", "green",
                    "notched_6", 3.2f,
                    64, 64,
                    "biomesunseen:heart_of_the_forest_seed", "biomesunseen:entities/boss/heart_of_the_forest",
                    "heart_of_the_forest_arena",
                    new PhaseData[] {
                        new PhaseData(
                                1, "Awakening", 0.75f,
                                "animation.spawn",
                                new String[] {
                                "branch_sweep", "stomp"
        },
                                new String[] {
                                "melee_attack"
        },
                                true, 40
                        ),
                        new PhaseData(
                                2, "Root Surge", 0.5f,
                                "animation.phase.summon_roots",
                                new String[] {
                                "root_eruption", "summon_grove_wardens", "branch_sweep"
        },
                                new String[] {
                                "summon_minions"
        },
                                true, 40
                        ),
                        new PhaseData(
                                3, "Seed Volley", 0.25f,
                                "animation.phase.explosive_seeds",
                                new String[] {
                                "explosive_seed_volley", "root_eruption", "branch_sweep"
        },
                                new String[] {
                                "ranged_attack"
        },
                                true, 40
                        ),
                        new PhaseData(
                                4, "Heart Exposed", 0.0f,
                                "animation.phase.heart_exposed",
                                new String[] {
                                "heart_pulse", "root_eruption", "explosive_seed_volley", "branch_sweep"
        },
                                new String[] {
                                "melee_attack", "ranged_attack"
        },
                                true, 40
                        ),
                    },
                    3.0f, 3.4f
            ),
            new BossData(
                    "void_serpent", "The Void Serpent", "void_between",
                    "biomesunseen:music.boss.void_serpent", "purple",
                    "notched_10", 2.6f,
                    64, 64,
                    "biomesunseen:void_serpent_scale", "biomesunseen:entities/boss/void_serpent",
                    "void_serpent_arena",
                    new PhaseData[] {
                        new PhaseData(
                                1, "Coiled", 0.7f,
                                "animation.spawn",
                                new String[] {
                                "head_strike", "tail_lash"
        },
                                new String[] {
                                "melee_attack"
        },
                                true, 40
                        ),
                        new PhaseData(
                                2, "Phasing", 0.45f,
                                "animation.phase.phase_out",
                                new String[] {
                                "phase_out", "phase_in", "head_strike", "void_spit"
        },
                                new String[] {
                                "phase_shift", "ranged_attack"
        },
                                true, 40
                        ),
                        new PhaseData(
                                3, "Constriction", 0.2f,
                                "animation.phase.coil_slam",
                                new String[] {
                                "coil_slam", "phase_out", "void_spit", "head_strike"
        },
                                new String[] {
                                "melee_attack"
        },
                                true, 40
                        ),
                        new PhaseData(
                                4, "Unravelling", 0.0f,
                                "animation.phase.phase_in",
                                new String[] {
                                "rapid_phase", "coil_slam", "void_spit", "head_strike", "arena_decay"
        },
                                new String[] {
                                "melee_attack", "ranged_attack", "phase_shift"
        },
                                true, 40
                        ),
                    },
                    2.4f, 1.6f
            ),
            new BossData(
                    "warden_of_the_hollow_deep", "Warden of the Hollow Deep", "hollow_deep",
                    "biomesunseen:music.boss.warden_of_the_hollow_deep", "blue",
                    "notched_12", 3.4f,
                    64, 64,
                    "biomesunseen:warden_of_the_hollow_deep_sigil", "biomesunseen:entities/boss/warden_of_the_hollow_deep",
                    "warden_of_the_hollow_deep_arena",
                    new PhaseData[] {
                        new PhaseData(
                                1, "Burrowed", 0.75f,
                                "animation.spawn",
                                new String[] {
                                "drill_strike", "tremor_pulse"
        },
                                new String[] {
                                "melee_attack"
        },
                                true, 40
                        ),
                        new PhaseData(
                                2, "Tremor Slam", 0.5f,
                                "animation.phase.tremor_slam",
                                new String[] {
                                "tremor_slam", "drill_strike", "carapace_guard"
        },
                                new String[] {
                                "melee_attack"
        },
                                true, 40
                        ),
                        new PhaseData(
                                3, "Spire Rise", 0.25f,
                                "animation.phase.spire_rise",
                                new String[] {
                                "spire_rise", "tremor_slam", "drill_strike"
        },
                                new String[] {
                                "melee_attack", "summon_minions"
        },
                                true, 40
                        ),
                        new PhaseData(
                                4, "Core Breach", 0.0f,
                                "animation.phase.burrow",
                                new String[] {
                                "core_vent", "spire_rise", "tremor_slam", "drill_strike"
        },
                                new String[] {
                                "melee_attack", "ranged_attack"
        },
                                true, 40
                        ),
                    },
                    3.4f, 2.4f
            ),
            new BossData(
                    "the_skyward_crown", "The Skyward Crown", "aetherfall",
                    "biomesunseen:music.boss.the_skyward_crown", "yellow",
                    "notched_20", 2.8f,
                    64, 64,
                    "biomesunseen:skyward_crown_regalia", "biomesunseen:entities/boss/the_skyward_crown",
                    "the_skyward_crown_arena",
                    new PhaseData[] {
                        new PhaseData(
                                1, "Enthroned", 0.8f,
                                "animation.spawn",
                                new String[] {
                                "wing_gust", "summon_crown_sentinels", "talons"
        },
                                new String[] {
                                "melee_attack", "summon_minions"
        },
                                true, 40
                        ),
                        new PhaseData(
                                2, "Aerial Dive", 0.55f,
                                "animation.phase.aerial_dive",
                                new String[] {
                                "aerial_dive", "wing_gust", "feather_volley", "talons"
        },
                                new String[] {
                                "melee_attack", "ranged_attack", "fly"
        },
                                true, 40
                        ),
                        new PhaseData(
                                3, "Crown Split", 0.3f,
                                "animation.phase.crown_split",
                                new String[] {
                                "crown_split", "shard_orbit", "aerial_dive", "feather_volley"
        },
                                new String[] {
                                "summon_minions", "ranged_attack"
        },
                                true, 60
                        ),
                        new PhaseData(
                                4, "Coronation", 0.0f,
                                "animation.phase.shard_orbit",
                                new String[] {
                                "coronation_burst", "aerial_dive", "crown_split", "feather_volley", "wing_gust", "arena_decay"
        },
                                new String[] {
                                "melee_attack", "ranged_attack", "summon_minions"
        },
                                true, 40
                        ),
                    },
                    2.8f, 2.6f
            ),
            new BossData(
                    "the_unraveling", "The Unraveling", "void_between",
                    "biomesunseen:music.boss.the_unraveling", "pink",
                    "notched_6", 2.2f,
                    64, 64,
                    "biomesunseen:unraveling_paradox", "biomesunseen:entities/boss/the_unraveling",
                    "the_unraveling_arena",
                    new PhaseData[] {
                        new PhaseData(
                                1, "Quadruped", 0.75f,
                                "animation.form.quadruped",
                                new String[] {
                                "charge", "claw_flurry", "glitch_step"
        },
                                new String[] {
                                "melee_attack"
        },
                                true, 40
                        ),
                        new PhaseData(
                                2, "Serpent", 0.5f,
                                "animation.form.serpent",
                                new String[] {
                                "constrict", "corruption_spit", "glitch_step", "claw_flurry"
        },
                                new String[] {
                                "melee_attack", "ranged_attack"
        },
                                true, 40
                        ),
                        new PhaseData(
                                3, "Humanoid", 0.25f,
                                "animation.form.humanoid",
                                new String[] {
                                "unraveling_slam", "summon_shards", "corruption_spit", "glitch_step"
        },
                                new String[] {
                                "melee_attack", "summon_minions"
        },
                                true, 40
                        ),
                        new PhaseData(
                                4, "Terminal", 0.0f,
                                "animation.phase.glitch_burst",
                                new String[] {
                                "form_cycle", "unraveling_slam", "constrict", "charge", "summon_shards", "arena_decay"
        },
                                new String[] {
                                "melee_attack", "ranged_attack", "summon_minions"
        },
                                true, 40
                        ),
                    },
                    1.6f, 2.6f
            ),
    };

    /** Entity id -> {textureWidth, textureHeight} in pixels. */
    public static final Object[][] ENTITY_TEXTURE_SIZE = {
            { "abyssal_leviathan", 64, 64 },
            { "amber_sentinel", 64, 64 },
            { "astral_scribe", 64, 64 },
            { "astral_scribe_aether", 64, 64 },
            { "aurora_stag", 64, 64 },
            { "blighthound", 64, 64 },
            { "bogcrawler", 64, 64 },
            { "canopy_glider", 64, 64 },
            { "canyon_skulk", 64, 64 },
            { "chrono_warden", 64, 64 },
            { "cloudfin", 64, 64 },
            { "coralback_crab", 64, 64 },
            { "crown_sentinel", 64, 64 },
            { "duskstalker", 64, 64 },
            { "echo_bat", 64, 64 },
            { "emberling", 64, 64 },
            { "fossil_wraith", 64, 64 },
            { "fracture_hound", 64, 64 },
            { "frostling", 64, 64 },
            { "frozen_mariner", 64, 64 },
            { "fungal_titan", 64, 64 },
            { "gale_harrier", 64, 64 },
            { "garden_aberration", 64, 64 },
            { "glacier_ox", 64, 64 },
            { "glimmerwing", 64, 64 },
            { "gloomstalker", 64, 64 },
            { "glowcap_grub", 64, 64 },
            { "grove_warden", 64, 64 },
            { "heart_of_the_forest", 64, 64 },
            { "highland_goat", 64, 64 },
            { "hollow_drowned", 64, 64 },
            { "hollow_scout", 64, 64 },
            { "kelp_serpent", 64, 64 },
            { "lanternkeeper", 64, 64 },
            { "luminous_jelly", 64, 64 },
            { "magma_lurker", 64, 64 },
            { "marrow_hound", 64, 64 },
            { "meadow_skipper", 64, 64 },
            { "mire_wisp", 64, 64 },
            { "mirror_walk", 64, 64 },
            { "moor_sentinel", 64, 64 },
            { "mossback_hare", 64, 64 },
            { "mycelial_horror", 64, 64 },
            { "null_swimmer", 64, 64 },
            { "orchard_tender", 64, 64 },
            { "orchid_mantis", 64, 64 },
            { "petaldancer", 64, 64 },
            { "primal_cat", 64, 64 },
            { "quarry_construct", 64, 64 },
            { "reefglider", 64, 64 },
            { "rime_stag", 64, 64 },
            { "river_lamprey", 64, 64 },
            { "roadwarden", 64, 64 },
            { "rootburrower", 64, 64 },
            { "rotstalker", 64, 64 },
            { "rune_construct", 64, 64 },
            { "savanna_strider", 64, 64 },
            { "shardling", 64, 64 },
            { "shorelurker", 64, 64 },
            { "silkweaver", 64, 64 },
            { "sky_citizen", 64, 64 },
            { "slag_golem", 64, 64 },
            { "spire_climber", 64, 64 },
            { "sporeling", 64, 64 },
            { "sporeling_deep", 64, 64 },
            { "static_wraith", 64, 64 },
            { "steppe_rider", 64, 64 },
            { "stonehide_boar", 64, 64 },
            { "stormcell_wisp", 64, 64 },
            { "sunscorch_vulture", 64, 64 },
            { "temple_guardian", 64, 64 },
            { "the_skyward_crown", 64, 64 },
            { "the_unraveling", 64, 64 },
            { "thicket_sprite", 64, 64 },
            { "trench_angler", 64, 64 },
            { "unraveling_shard", 64, 64 },
            { "unraveling_shard_aether", 64, 64 },
            { "vault_keeper", 64, 64 },
            { "veilmourner", 64, 64 },
            { "veilwing", 64, 64 },
            { "void_scout", 64, 64 },
            { "void_serpent", 64, 64 },
            { "warden_acolyte", 64, 64 },
            { "warden_of_the_hollow_deep", 64, 64 },
            { "warren_skitter", 64, 64 },
    };

    // ------------------------------------------------------------------
    //  BIOMES / DIMENSIONS / AMBIENCE
    // ------------------------------------------------------------------
    /** Every dimension the mod adds biomes to. */
    public static final String[] DIMENSIONS = {
            "aetherfall", "hollow_deep", "overworld", "void_between"
        };


    /** Biome ids per dimension, for the biome source parameter lists. */
    public static final String[][] DIMENSION_BIOMES = {
            { "aetherfall",
              "aurora_bridge,celestial_orchard,cloud_sea,crown_apex,dawn_landing,dawn_marble_quarry,featherfall_grove,floating_meadow,gilded_archive,gilded_citadel,hymn_halls,moonpetal_skyfield,runeglass_fields,shatterbelt,skyward_steps,starfall_vault,stormcell_spire,sunspire_plateau,twilight_terrace,zephyr_reach" },
            { "hollow_deep",
              "basaltic_fissures,chitin_warrens,crystal_vault,deep_bloom_reach,echo_chasm,fungal_forest,gloomslate_depths,glowcap_grotto,hollow_core,hollow_oasis,hollow_threshold,lantern_terraces,luminous_sea,mycelial_wastes,pearl_depths,root_cathedral,spore_chalk_flats,sunken_hollow_city,tremor_ward,weeping_galleries" },
            { "overworld",
              "abyssal_trench,aetherveil_reach,amberwood,ancestor_grove,ashen_caldera,ashen_necropolis,aurora_steppe,blackwater_bog,blighted_marches,bloomfield,brine_marsh,bronze_steppe,cinder_dunes,colossal_boneyard,coral_atoll_ring,coral_shallows,crystalline_tundra,dreaming_atoll,duskwood_hollow,emberfall_ridge,flooded_ruins,forged_waste,frozen_expanse,geyser_lagoon,ghostlight_marsh,glacial_lake,glacier_maw,glimmering_thicket,glimmerleaf_woodland,grave_ice_field,harvest_hollows,hieroglyph_canyon,hollowlight_basin,howling_peaks,ironstone_ravine,jewel_reef,kelp_cathedral,leviathan_graveyard,lumenshade_glade,luminescent_grove,mangrove_labyrinth,marigold_march,megalith_moor,monolith_shore,moonpetal_meadow,obsidian_shelf,old_king_road,orchid_lagoon,pearl_beds,petal_drift_flats,petrified_colossi,petrified_forest,primal_savanna,pyroclast_fields,rimeforest,river_of_lights,rootdeep_hollow,ruined_observatory,sakura_highlands,saltflat_mirage,scorched_glassland,seagrass_meadow,shattered_archive,silken_canopy,starfall_glade,stormback_steppe,sulphur_vents,sunken_cathedral,sunken_temple_reach,sunscorch_badlands,sunspore_barrens,tidal_flats,tideglass_bay,titan_graveyard,veilwood,verdantheight,volcanic_wasteland,whispering_mire,whitewater_gorge,witherwood" },
            { "void_between",
              "abyssal_shelf_void,bleeding_spires,chromatic_reef,chrono_shelf,dusk_mirror,fracture_plains,glitch_garden,hollow_echo,memory_vault,null_sea,outer_margin,paradox_hollow,recursive_fields,serpent_run,shardfall_expanse,static_wastes,terminal_glade,unraveling_nexus,void_threshold,wither_veil" },
    };

    /**
     * Every Overworld biome the mod adds.
     *
     * Bound to the TerraBlender Overworld region by BUOverworldRegion,
     * which blends their authored climate parameters against vanilla so
     * they generate in normal Overworld play without replacing any
     * vanilla biome.
     */
    /** Placed by the TerraBlender Overworld region. */
    public static final String[] SEEDED_OVERWORLD_BIOMES = {
            "abyssal_trench", "aetherveil_reach", "amberwood", "ancestor_grove", "ashen_caldera",
            "ashen_necropolis", "aurora_steppe", "blackwater_bog", "blighted_marches", "bloomfield",
            "brine_marsh", "bronze_steppe", "cinder_dunes", "colossal_boneyard", "coral_atoll_ring",
            "coral_shallows", "crystalline_tundra", "dreaming_atoll", "duskwood_hollow", "emberfall_ridge",
            "flooded_ruins", "forged_waste", "frozen_expanse", "geyser_lagoon", "ghostlight_marsh",
            "glacial_lake", "glacier_maw", "glimmering_thicket", "glimmerleaf_woodland", "grave_ice_field",
            "harvest_hollows", "hieroglyph_canyon", "hollowlight_basin", "howling_peaks", "ironstone_ravine",
            "jewel_reef", "kelp_cathedral", "leviathan_graveyard", "lumenshade_glade", "luminescent_grove",
            "mangrove_labyrinth", "marigold_march", "megalith_moor", "monolith_shore", "moonpetal_meadow",
            "obsidian_shelf", "old_king_road", "orchid_lagoon", "pearl_beds", "petal_drift_flats",
            "petrified_colossi", "petrified_forest", "primal_savanna", "pyroclast_fields", "rimeforest",
            "river_of_lights", "rootdeep_hollow", "ruined_observatory", "sakura_highlands", "saltflat_mirage",
            "scorched_glassland", "seagrass_meadow", "shattered_archive", "silken_canopy", "starfall_glade",
            "stormback_steppe", "sulphur_vents", "sunken_cathedral", "sunken_temple_reach",
            "sunscorch_badlands", "sunspore_barrens", "tidal_flats", "tideglass_bay", "titan_graveyard",
            "veilwood", "verdantheight", "volcanic_wasteland", "whispering_mire", "whitewater_gorge",
            "witherwood"
        };


    /**
     * Multi-noise parameters for SEEDED_OVERWORLD_BIOMES as
     * {biomeId, temperature, humidity, continentalness, erosion,
     * depth, weirdness, offset, weight}.
     */
    public static final Object[][] SEEDED_OVERWORLD_PARAMETERS = {
            { "abyssal_trench", 0.3f, 1.0f, -0.6f, 0.7f, -0.6f, -0.2f, 0.0f, 90 },
            { "aetherveil_reach", 0.3f, 0.4f, 0.6f, 0.1f, 0.0f, 0.0f, 0.0f, 100 },
            { "amberwood", 0.65f, 0.6f, 0.35f, 0.25f, 0.0f, 0.05f, 0.0f, 120 },
            { "ancestor_grove", 0.6f, 0.75f, 0.3f, 0.2f, 0.0f, 0.0f, 0.0f, 100 },
            { "ashen_caldera", 1.5f, 0.15f, 0.4f, 0.7f, 0.25f, 0.25f, 0.0f, 100 },
            { "ashen_necropolis", 0.35f, 0.2f, 0.45f, 0.4f, 0.0f, 0.2f, 0.0f, 100 },
            { "aurora_steppe", 0.25f, 0.3f, 0.5f, 0.3f, 0.0f, 0.0f, 0.0f, 100 },
            { "blackwater_bog", 0.65f, 1.0f, -0.15f, 0.6f, -0.05f, 0.1f, 0.0f, 100 },
            { "blighted_marches", 0.5f, 0.85f, 0.35f, 0.55f, -0.05f, 0.1f, 0.0f, 100 },
            { "bloomfield", 0.75f, 0.7f, 0.3f, 0.45f, 0.0f, -0.05f, 0.0f, 120 },
            { "brine_marsh", 0.8f, 1.0f, -0.1f, 0.65f, -0.05f, 0.05f, 0.0f, 100 },
            { "bronze_steppe", 0.55f, 0.3f, 0.55f, 0.4f, 0.0f, 0.05f, 0.0f, 100 },
            { "cinder_dunes", 1.35f, 0.03f, 0.5f, 0.4f, 0.0f, 0.1f, 0.0f, 100 },
            { "colossal_boneyard", 0.4f, 0.2f, 0.5f, 0.4f, 0.0f, 0.15f, 0.0f, 100 },
            { "coral_atoll_ring", 0.85f, 1.0f, -0.45f, 0.35f, 0.0f, -0.15f, 0.0f, 100 },
            { "coral_shallows", 0.85f, 0.95f, -0.25f, 0.5f, -0.05f, -0.1f, 0.0f, 120 },
            { "crystalline_tundra", 0.05f, 0.4f, 0.45f, 0.35f, 0.0f, 0.0f, 0.0f, 100 },
            { "dreaming_atoll", 0.85f, 0.9f, -0.2f, 0.4f, 0.0f, 0.0f, 0.0f, 100 },
            { "duskwood_hollow", 0.5f, 0.8f, 0.3f, 0.2f, 0.0f, 0.0f, 0.0f, 100 },
            { "emberfall_ridge", 0.9f, 0.3f, 0.65f, 0.7f, 0.2f, 0.2f, 0.0f, 120 },
            { "flooded_ruins", 0.7f, 0.95f, -0.15f, 0.55f, -0.05f, -0.05f, 0.0f, 100 },
            { "forged_waste", 0.8f, 0.15f, 0.5f, 0.45f, 0.0f, 0.1f, 0.0f, 100 },
            { "frozen_expanse", -0.6f, 0.3f, 0.6f, 0.3f, 0.0f, 0.0f, 0.0f, 100 },
            { "geyser_lagoon", 0.95f, 0.9f, -0.25f, 0.55f, 0.0f, 0.1f, 0.0f, 100 },
            { "ghostlight_marsh", 0.65f, 1.0f, 0.38f, 0.65f, 0.0f, 0.0f, 0.0f, 100 },
            { "glacial_lake", 0.0f, 0.6f, -0.2f, 0.3f, 0.05f, 0.0f, 0.0f, 100 },
            { "glacier_maw", -0.7f, 0.5f, 0.65f, 0.8f, -0.15f, 0.15f, 0.0f, 100 },
            { "glimmering_thicket", 0.7f, 0.8f, 0.35f, 0.25f, 0.0f, 0.0f, 0.0f, 100 },
            { "glimmerleaf_woodland", 0.7f, 0.8f, 0.28f, 0.22f, 0.0f, 0.05f, 0.0f, 120 },
            { "grave_ice_field", -0.8f, 0.4f, 0.5f, 0.45f, 0.0f, 0.1f, 0.0f, 100 },
            { "harvest_hollows", 0.65f, 0.6f, 0.4f, 0.4f, 0.0f, 0.0f, 0.0f, 120 },
            { "hieroglyph_canyon", 0.7f, 0.15f, 0.6f, 0.7f, -0.1f, 0.1f, 0.0f, 100 },
            { "hollowlight_basin", 0.45f, 0.75f, 0.15f, 0.45f, 0.0f, 0.0f, 0.0f, 100 },
            { "howling_peaks", 0.1f, 0.35f, 0.75f, 0.85f, 0.35f, 0.25f, 0.0f, 100 },
            { "ironstone_ravine", 0.5f, 0.25f, 0.55f, 0.85f, -0.2f, 0.2f, 0.0f, 100 },
            { "jewel_reef", 0.8f, 1.0f, -0.4f, 0.5f, -0.1f, -0.15f, 0.0f, 120 },
            { "kelp_cathedral", 0.7f, 1.0f, -0.3f, 0.5f, -0.2f, -0.1f, 0.0f, 100 },
            { "leviathan_graveyard", 0.4f, 1.0f, -0.55f, 0.65f, -0.5f, -0.15f, 0.0f, 80 },
            { "lumenshade_glade", 0.6f, 0.8f, 0.22f, 0.3f, 0.0f, 0.0f, 0.0f, 100 },
            { "luminescent_grove", 0.65f, 0.85f, 0.25f, 0.15f, 0.0f, 0.0f, 0.0f, 100 },
            { "mangrove_labyrinth", 0.9f, 1.0f, -0.2f, 0.5f, 0.0f, 0.0f, 0.0f, 100 },
            { "marigold_march", 0.7f, 0.65f, 0.45f, 0.35f, 0.0f, 0.0f, 0.0f, 120 },
            { "megalith_moor", 0.45f, 0.55f, 0.45f, 0.35f, 0.0f, 0.05f, 0.0f, 100 },
            { "monolith_shore", 0.5f, 0.75f, -0.3f, 0.3f, 0.0f, -0.05f, 0.0f, 100 },
            { "moonpetal_meadow", 0.55f, 0.7f, 0.2f, 0.4f, 0.0f, 0.0f, 0.0f, 100 },
            { "obsidian_shelf", 0.9f, 0.2f, -0.15f, 0.5f, 0.0f, 0.2f, 0.0f, 100 },
            { "old_king_road", 0.5f, 0.4f, 0.4f, 0.3f, 0.0f, 0.0f, 0.0f, 100 },
            { "orchid_lagoon", 0.85f, 1.0f, -0.1f, 0.6f, 0.0f, -0.05f, 0.0f, 120 },
            { "pearl_beds", 0.8f, 1.0f, -0.35f, 0.35f, -0.1f, -0.1f, 0.0f, 100 },
            { "petal_drift_flats", 0.6f, 0.6f, 0.55f, 0.55f, 0.0f, 0.0f, 0.0f, 100 },
            { "petrified_colossi", 0.4f, 0.2f, 0.5f, 0.35f, 0.1f, 0.2f, 0.0f, 100 },
            { "petrified_forest", 0.5f, 0.35f, 0.35f, 0.25f, 0.0f, 0.1f, 0.0f, 100 },
            { "primal_savanna", 0.95f, 0.15f, 0.55f, 0.4f, 0.0f, 0.0f, 0.0f, 120 },
            { "pyroclast_fields", 1.3f, 0.1f, 0.5f, 0.5f, 0.05f, 0.15f, 0.0f, 120 },
            { "rimeforest", -0.4f, 0.55f, 0.4f, 0.25f, 0.0f, 0.05f, 0.0f, 100 },
            { "river_of_lights", 0.6f, 0.9f, -0.05f, 0.4f, 0.0f, 0.0f, 0.0f, 110 },
            { "rootdeep_hollow", 0.55f, 0.8f, 0.25f, 0.55f, -0.15f, 0.1f, 0.0f, 100 },
            { "ruined_observatory", 0.35f, 0.3f, 0.55f, 0.2f, 0.05f, 0.2f, 0.0f, 100 },
            { "sakura_highlands", 0.6f, 0.65f, 0.5f, 0.3f, 0.1f, 0.05f, 0.0f, 120 },
            { "saltflat_mirage", 1.15f, 0.05f, 0.6f, 0.25f, 0.0f, 0.05f, 0.0f, 100 },
            { "scorched_glassland", 1.4f, 0.02f, 0.55f, 0.5f, 0.0f, 0.15f, 0.0f, 100 },
            { "seagrass_meadow", 0.75f, 1.0f, -0.3f, 0.3f, -0.08f, -0.05f, 0.0f, 110 },
            { "shattered_archive", 0.45f, 0.35f, 0.35f, 0.45f, 0.05f, 0.3f, 0.0f, 100 },
            { "silken_canopy", 0.75f, 0.85f, 0.3f, 0.1f, 0.0f, 0.0f, 0.0f, 100 },
            { "starfall_glade", 0.4f, 0.5f, 0.1f, 0.5f, 0.0f, 0.0f, 0.0f, 100 },
            { "stormback_steppe", 0.55f, 0.55f, 0.6f, 0.3f, 0.0f, -0.1f, 0.0f, 100 },
            { "sulphur_vents", 1.25f, 0.35f, 0.45f, 0.55f, 0.0f, 0.2f, 0.0f, 100 },
            { "sunken_cathedral", 0.55f, 1.0f, -0.4f, 0.6f, -0.35f, -0.1f, 0.0f, 90 },
            { "sunken_temple_reach", 0.75f, 0.9f, -0.1f, 0.5f, 0.0f, -0.1f, 0.0f, 100 },
            { "sunscorch_badlands", 1.1f, 0.05f, 0.6f, 0.55f, 0.05f, 0.1f, 0.0f, 120 },
            { "sunspore_barrens", 1.0f, 0.25f, 0.55f, 0.45f, 0.0f, 0.05f, 0.0f, 120 },
            { "tidal_flats", 0.75f, 0.95f, -0.2f, 0.3f, 0.0f, -0.05f, 0.0f, 110 },
            { "tideglass_bay", 0.8f, 0.9f, -0.35f, 0.4f, 0.0f, -0.1f, 0.0f, 120 },
            { "titan_graveyard", 0.3f, 0.25f, 0.55f, 0.5f, 0.05f, 0.25f, 0.0f, 100 },
            { "veilwood", 0.55f, 0.85f, 0.28f, 0.2f, 0.0f, 0.0f, 0.0f, 100 },
            { "verdantheight", 0.6f, 0.85f, 0.2f, 0.75f, 0.15f, 0.1f, 0.0f, 120 },
            { "volcanic_wasteland", 1.6f, 0.05f, 0.5f, 0.6f, 0.1f, 0.2f, 0.0f, 100 },
            { "whispering_mire", 0.6f, 0.95f, 0.4f, 0.6f, 0.0f, 0.0f, 0.0f, 100 },
            { "whitewater_gorge", 0.5f, 0.8f, 0.3f, 0.9f, -0.1f, 0.15f, 0.0f, 100 },
            { "witherwood", 0.45f, 0.5f, 0.3f, 0.3f, 0.0f, 0.15f, 0.0f, 100 },
    };

    /**
     * Surface materials for SEEDED_OVERWORLD_BIOMES as
     * {biomeId, surfaceTop, surfaceFiller}.
     *
     * Consumed by BUOverworldSurfaceRules, which registers biome-gated
     * surface rules through TerraBlender so each biome gets its authored
     * crust without those materials bleeding into vanilla biomes.
     */
    public static final Object[][] OVERWORLD_SURFACES = {
            { "abyssal_trench", "biomesunseen:abyssal_silt", "biomesunseen:abyssal_silt" },
            { "aetherveil_reach", "biomesunseen:aether_grass_block", "minecraft:dirt" },
            { "amberwood", "biomesunseen:umber_grass_block", "biomesunseen:amber_loam" },
            { "ancestor_grove", "biomesunseen:lumen_grass_block", "biomesunseen:lumen_dirt" },
            { "ashen_caldera", "biomesunseen:ash_grass_block", "biomesunseen:ashen_dirt" },
            { "ashen_necropolis", "biomesunseen:ash_grass_block", "biomesunseen:ashen_dirt" },
            { "aurora_steppe", "biomesunseen:crystal_grass_block", "minecraft:dirt" },
            { "blackwater_bog", "biomesunseen:blight_grass_block", "biomesunseen:brine_mud" },
            { "blighted_marches", "biomesunseen:blight_grass_block", "biomesunseen:blight_loam" },
            { "bloomfield", "biomesunseen:lumen_grass_block", "biomesunseen:lumen_dirt" },
            { "brine_marsh", "biomesunseen:tidegrass_block", "biomesunseen:brine_mud" },
            { "bronze_steppe", "biomesunseen:umber_grass_block", "biomesunseen:umber_dirt" },
            { "cinder_dunes", "biomesunseen:cinder_sand", "biomesunseen:cinder_sand" },
            { "colossal_boneyard", "biomesunseen:ash_grass_block", "biomesunseen:ashen_dirt" },
            { "coral_atoll_ring", "biomesunseen:tide_sand", "biomesunseen:wet_silt" },
            { "coral_shallows", "biomesunseen:tidegrass_block", "biomesunseen:wet_silt" },
            { "crystalline_tundra", "biomesunseen:crystal_grass_block", "biomesunseen:crystal_dirt" },
            { "dreaming_atoll", "biomesunseen:lumen_sand", "minecraft:dirt" },
            { "duskwood_hollow", "biomesunseen:spore_grass_block", "minecraft:dirt" },
            { "emberfall_ridge", "biomesunseen:ash_grass_block", "biomesunseen:ashen_dirt" },
            { "flooded_ruins", "biomesunseen:tidegrass_block", "biomesunseen:wet_silt" },
            { "forged_waste", "biomesunseen:ash_grass_block", "biomesunseen:ashen_dirt" },
            { "frozen_expanse", "biomesunseen:crystal_grass_block", "biomesunseen:frost_silt" },
            { "geyser_lagoon", "biomesunseen:tidegrass_block", "biomesunseen:wet_silt" },
            { "ghostlight_marsh", "biomesunseen:spore_grass_block", "minecraft:dirt" },
            { "glacial_lake", "biomesunseen:crystal_grass_block", "biomesunseen:frost_silt" },
            { "glacier_maw", "biomesunseen:crystal_grass_block", "biomesunseen:frost_silt" },
            { "glimmering_thicket", "biomesunseen:lumen_grass_block", "minecraft:dirt" },
            { "glimmerleaf_woodland", "biomesunseen:lumen_grass_block", "biomesunseen:lumen_dirt" },
            { "grave_ice_field", "biomesunseen:crystal_grass_block", "biomesunseen:frost_silt" },
            { "harvest_hollows", "biomesunseen:umber_grass_block", "biomesunseen:umber_dirt" },
            { "hieroglyph_canyon", "biomesunseen:sunbleached_sand", "biomesunseen:sunbleached_stone" },
            { "hollowlight_basin", "biomesunseen:spore_grass_block", "minecraft:dirt" },
            { "howling_peaks", "biomesunseen:ash_grass_block", "biomesunseen:titanite_gravel" },
            { "ironstone_ravine", "biomesunseen:umber_grass_block", "biomesunseen:umber_dirt" },
            { "jewel_reef", "biomesunseen:tide_sand", "biomesunseen:wet_silt" },
            { "kelp_cathedral", "biomesunseen:tide_sand", "biomesunseen:wet_silt" },
            { "leviathan_graveyard", "biomesunseen:abyssal_silt", "biomesunseen:abyssal_silt" },
            { "lumenshade_glade", "biomesunseen:lumen_grass_block", "minecraft:dirt" },
            { "luminescent_grove", "biomesunseen:lumen_grass_block", "biomesunseen:lumen_dirt" },
            { "mangrove_labyrinth", "biomesunseen:tidegrass_block", "biomesunseen:brine_mud" },
            { "marigold_march", "biomesunseen:lumen_grass_block", "biomesunseen:lumen_dirt" },
            { "megalith_moor", "biomesunseen:mossy_umber_grass", "biomesunseen:umber_dirt" },
            { "monolith_shore", "biomesunseen:tidegrass_block", "biomesunseen:wet_silt" },
            { "moonpetal_meadow", "biomesunseen:lumen_grass_block", "minecraft:dirt" },
            { "obsidian_shelf", "biomesunseen:ash_grass_block", "biomesunseen:obsidian_grit" },
            { "old_king_road", "biomesunseen:umber_grass_block", "biomesunseen:umber_dirt" },
            { "orchid_lagoon", "biomesunseen:tidegrass_block", "biomesunseen:wet_silt" },
            { "pearl_beds", "biomesunseen:tide_sand", "biomesunseen:wet_silt" },
            { "petal_drift_flats", "biomesunseen:lumen_grass_block", "minecraft:dirt" },
            { "petrified_colossi", "biomesunseen:petrified_grass_block", "biomesunseen:petrified_dirt" },
            { "petrified_forest", "biomesunseen:petrified_grass_block", "biomesunseen:petrified_dirt" },
            { "primal_savanna", "biomesunseen:sunbleached_grass_block", "biomesunseen:sunbleached_dirt" },
            { "pyroclast_fields", "biomesunseen:ash_grass_block", "biomesunseen:ashen_dirt" },
            { "rimeforest", "biomesunseen:crystal_grass_block", "biomesunseen:frost_silt" },
            { "river_of_lights", "biomesunseen:tide_sand", "biomesunseen:wet_silt" },
            { "rootdeep_hollow", "biomesunseen:spore_grass_block", "biomesunseen:root_loam" },
            { "ruined_observatory", "biomesunseen:crystal_grass_block", "biomesunseen:crystal_dirt" },
            { "sakura_highlands", "biomesunseen:lumen_grass_block", "biomesunseen:lumen_dirt" },
            { "saltflat_mirage", "biomesunseen:salt_crust", "biomesunseen:salt_flat_hardpan" },
            { "scorched_glassland", "biomesunseen:tideglass_sand", "biomesunseen:scorched_hardpan" },
            { "seagrass_meadow", "biomesunseen:tide_sand", "biomesunseen:wet_silt" },
            { "shattered_archive", "biomesunseen:ash_grass_block", "biomesunseen:parchment_silt" },
            { "silken_canopy", "biomesunseen:lumen_grass_block", "minecraft:dirt" },
            { "starfall_glade", "biomesunseen:lumen_grass_block", "minecraft:dirt" },
            { "stormback_steppe", "biomesunseen:umber_grass_block", "biomesunseen:umber_dirt" },
            { "sulphur_vents", "biomesunseen:ash_grass_block", "biomesunseen:sulphur_crust" },
            { "sunken_cathedral", "biomesunseen:abyssal_silt", "biomesunseen:abyssal_silt" },
            { "sunken_temple_reach", "biomesunseen:tidegrass_block", "biomesunseen:wet_silt" },
            { "sunscorch_badlands", "biomesunseen:sunbleached_sand", "biomesunseen:sunscorch_hardpan" },
            { "sunspore_barrens", "biomesunseen:spore_grass_block", "biomesunseen:spore_sand" },
            { "tidal_flats", "biomesunseen:tide_sand", "biomesunseen:wet_silt" },
            { "tideglass_bay", "biomesunseen:tide_sand", "biomesunseen:wet_silt" },
            { "titan_graveyard", "biomesunseen:ash_grass_block", "biomesunseen:titanite_gravel" },
            { "veilwood", "biomesunseen:lumen_grass_block", "minecraft:dirt" },
            { "verdantheight", "biomesunseen:lumen_grass_block", "biomesunseen:lumen_dirt" },
            { "volcanic_wasteland", "biomesunseen:ash_grass_block", "biomesunseen:ashen_dirt" },
            { "whispering_mire", "biomesunseen:spore_grass_block", "minecraft:dirt" },
            { "whitewater_gorge", "biomesunseen:umber_grass_block", "biomesunseen:river_gravel" },
            { "witherwood", "biomesunseen:blight_grass_block", "biomesunseen:blight_loam" },
    };

    /** Every SoundEvent the mod registers (music, ambience, boss themes). */
    public static final String[] SOUNDS = {
            "ambient.ash_wind", "ambient.blight", "ambient.deep_water", "ambient.drip", "ambient.ember",
            "ambient.hymn", "ambient.rapids", "ambient.static", "ambient.storm", "ambient.stream",
            "ambient.surf", "ambient.tremor", "ambient.underwater", "ambient.whisper", "ambient.wind_high",
            "ambient.wind_low", "music.aetherfall", "music.ancient", "music.aquatic",
            "music.boss.heart_of_the_forest", "music.boss.the_skyward_crown", "music.boss.the_unraveling",
            "music.boss.void_serpent", "music.boss.warden_of_the_hollow_deep", "music.ethereal", "music.harsh",
            "music.hollow_deep", "music.vibrant", "music.void_between"
        };


    /** Subset of SOUNDS that ship real audio; playback is gated on this. */
    public static final String[] SOUNDS_WITH_AUDIO = {
            "ambient.ash_wind", "ambient.blight", "ambient.deep_water", "ambient.drip", "ambient.ember",
            "ambient.hymn", "ambient.rapids", "ambient.static", "ambient.storm", "ambient.stream",
            "ambient.surf", "ambient.tremor", "ambient.underwater", "ambient.whisper", "ambient.wind_high",
            "ambient.wind_low", "music.aetherfall", "music.ancient", "music.aquatic",
            "music.boss.heart_of_the_forest", "music.boss.the_skyward_crown", "music.boss.the_unraveling",
            "music.boss.void_serpent", "music.boss.warden_of_the_hollow_deep", "music.ethereal", "music.harsh",
            "music.hollow_deep", "music.vibrant", "music.void_between"
        };


    /** Ambient biome particle types. */
    public static final String[] PARTICLES = {
            "aetherveil_mote", "aurora_ribbon", "ember_drift", "heat_shimmer", "lumen_mote", "moonpetal_drift",
            "page_drift", "pollen_drift", "spore_drift", "starfall_ember", "void_fracture"
        };


    /**
     * Ore generation parameters as {oreBlock, hostStone, minY, maxY,
     * veinSize, veinsPerChunk, dimension, experience}.
     */
    public static final Object[][] ORE_GEN = {
            { "lumenite_ore", "stone", -32, 48, 7, 9, "overworld", 3 },
            { "deepslate_lumenite_ore", "deepslate", -32, 48, 7, 9, "overworld", 3 },
            { "umbrite_ore", "stone", -48, 32, 9, 10, "overworld", 1 },
            { "deepslate_umbrite_ore", "deepslate", -48, 32, 9, 10, "overworld", 1 },
            { "petrichorite_ore", "stone", -24, 56, 6, 7, "overworld", 2 },
            { "deepslate_petrichorite_ore", "deepslate", -24, 56, 6, 7, "overworld", 2 },
            { "sunscorch_ore", "stone", -56, 16, 5, 6, "overworld", 4 },
            { "deepslate_sunscorch_ore", "deepslate", -56, 16, 5, 6, "overworld", 4 },
            { "glimmerleaf_ore", "stone", -16, 64, 8, 11, "overworld", 1 },
            { "deepslate_glimmerleaf_ore", "deepslate", -16, 64, 8, 11, "overworld", 1 },
            { "tideglass_ore", "stone", -32, 48, 10, 8, "overworld", 1 },
            { "deepslate_tideglass_ore", "deepslate", -32, 48, 10, 8, "overworld", 1 },
            { "emberquartz_ore", "stone", -60, 8, 6, 7, "overworld", 3 },
            { "deepslate_emberquartz_ore", "deepslate", -60, 8, 6, 7, "overworld", 3 },
            { "frostbloom_ore", "stone", -40, 40, 5, 6, "overworld", 2 },
            { "deepslate_frostbloom_ore", "deepslate", -40, 40, 5, 6, "overworld", 2 },
            { "sporeamber_ore", "stone", -24, 56, 7, 9, "overworld", 1 },
            { "deepslate_sporeamber_ore", "deepslate", -24, 56, 7, 9, "overworld", 1 },
            { "rootiron_ore", "stone", -56, 40, 8, 12, "overworld", 2 },
            { "deepslate_rootiron_ore", "deepslate", -56, 40, 8, 12, "overworld", 2 },
            { "graveamber_ore", "stone", -64, -8, 4, 4, "overworld", 3 },
            { "deepslate_graveamber_ore", "deepslate", -64, -8, 4, 4, "overworld", 3 },
            { "wraithsalt_ore", "stone", -48, 24, 9, 10, "overworld", 1 },
            { "deepslate_wraithsalt_ore", "deepslate", -48, 24, 9, 10, "overworld", 1 },
            { "bloodstone_ore", "stone", -64, 0, 5, 5, "overworld", 4 },
            { "deepslate_bloodstone_ore", "deepslate", -64, 0, 5, 5, "overworld", 4 },
            { "coralite_ore", "stone", -24, 48, 7, 8, "overworld", 1 },
            { "deepslate_coralite_ore", "deepslate", -24, 48, 7, 8, "overworld", 1 },
            { "kelpstone_ore", "stone", -16, 56, 10, 9, "overworld", 0 },
            { "deepslate_kelpstone_ore", "deepslate", -16, 56, 10, 9, "overworld", 0 },
            { "stormcell_ore", "stone", -48, 24, 4, 4, "overworld", 4 },
            { "deepslate_stormcell_ore", "deepslate", -48, 24, 4, 4, "overworld", 4 },
            { "glacierite_ore", "stone", -40, 40, 6, 6, "overworld", 2 },
            { "deepslate_glacierite_ore", "deepslate", -40, 40, 6, 6, "overworld", 2 },
            { "ashen_core_ore", "stone", -64, -16, 4, 4, "overworld", 5 },
            { "deepslate_ashen_core_ore", "deepslate", -64, -16, 4, 4, "overworld", 5 },
            { "spiritwood_ore", "stone", -32, 48, 7, 8, "overworld", 2 },
            { "deepslate_spiritwood_ore", "deepslate", -32, 48, 7, 8, "overworld", 2 },
            { "titanite_ore", "stone", -64, 8, 6, 7, "overworld", 3 },
            { "deepslate_titanite_ore", "deepslate", -64, 8, 6, 7, "overworld", 3 },
            { "hollowite_ore", "hollow_stone", -56, 48, 6, 8, "hollow_deep", 4 },
            { "mycelium_ore", "mycelial_slimestone", -48, 56, 8, 10, "hollow_deep", 2 },
            { "gloomite_ore", "gloomslate", -64, 8, 5, 6, "hollow_deep", 4 },
            { "deep_pearl_ore", "spore_chalk", -40, 32, 4, 5, "hollow_deep", 3 },
            { "echo_crystal_ore", "gloomslate", -64, 0, 5, 5, "hollow_deep", 4 },
            { "root_heart_ore", "hollow_stone", -32, 24, 3, 3, "hollow_deep", 6 },
            { "lumenshade_ore", "hollow_stone", -56, 32, 6, 7, "hollow_deep", 4 },
            { "basaltic_hollow_core_ore", "basaltic_hollowstone", -64, -8, 7, 6, "hollow_deep", 4 },
            { "aetherium_ore", "aetherstone", -32, 96, 5, 6, "aetherfall", 6 },
            { "dawnshard_ore", "dawn_marble", -16, 112, 6, 8, "aetherfall", 4 },
            { "skylead_ore", "cloudstone", -24, 120, 9, 10, "aetherfall", 2 },
            { "starfall_ore", "aetherstone", 16, 128, 4, 4, "aetherfall", 6 },
            { "stormcell_aether_ore", "twilight_shale", -32, 96, 5, 5, "aetherfall", 4 },
            { "runeglass_ore", "dawn_marble", -16, 112, 7, 7, "aetherfall", 3 },
            { "moonpetal_ore", "aetherstone", -8, 120, 8, 9, "aetherfall", 2 },
            { "sunspore_ore", "gilded_aetherstone", 0, 128, 6, 7, "aetherfall", 4 },
            { "voidsteel_ore", "voidstone", -64, 64, 5, 6, "void_between", 6 },
            { "nullite_ore", "null_basalt", -64, 48, 4, 4, "void_between", 6 },
            { "staticite_ore", "static_stone", -48, 64, 8, 9, "void_between", 4 },
            { "chronosite_ore", "fracture_shale", -64, 32, 3, 3, "void_between", 7 },
            { "duskite_ore", "voidstone", -56, 56, 6, 7, "void_between", 4 },
            { "witherite_ore", "fracture_shale", -64, 16, 7, 8, "void_between", 4 },
            { "fracture_shale_ore", "fracture_shale", -48, 64, 9, 11, "void_between", 2 },
            { "glacierite_void_ore", "null_basalt", -64, 8, 5, 6, "void_between", 4 },
    };

    /** Portal structures; the portal block is placed by these. */
    public static final String[] PORTAL_STRUCTURES = {
            "aetherfall_portal", "hollow_deep_portal", "void_portal"
        };


    /** Boss arena structures; entering one can trigger the fight. */
    public static final String[] BOSS_ARENAS = {
            "heart_of_the_forest_arena", "the_skyward_crown_arena", "the_unraveling_arena",
            "void_serpent_arena", "warden_of_the_hollow_deep_arena"
        };


    /** Every block id the mod registers, across all kinds. */
    public static String[] allBlocks() {
        java.util.List<String> all = new java.util.ArrayList<>();
        all.addAll(java.util.Arrays.asList(BLOCKS_CUBE));
        all.addAll(java.util.Arrays.asList(BLOCKS_GRASS));
        all.addAll(java.util.Arrays.asList(BLOCKS_LOG));
        all.addAll(java.util.Arrays.asList(BLOCKS_ORE));
        all.addAll(java.util.Arrays.asList(BLOCKS_MINERAL));
        all.addAll(java.util.Arrays.asList(BLOCKS_FLORA));
        all.addAll(java.util.Arrays.asList(BLOCKS_PORTAL));
        all.addAll(java.util.Arrays.asList(BLOCKS_LANTERN));
        all.addAll(java.util.Arrays.asList(BLOCKS_ALTAR));
        all.addAll(java.util.Arrays.asList(BLOCKS_FLUID));
        return all.toArray(new String[0]);
    }
}
