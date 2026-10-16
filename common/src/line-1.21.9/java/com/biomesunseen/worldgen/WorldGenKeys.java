package com.biomesunseen.worldgen;

import com.biomesunseen.core.Content;
import com.biomesunseen.core.ModConstants;

import java.util.Collections;
import java.util.LinkedHashSet;
import java.util.Set;

/**
 * Stable id table for all 80 biomes, 20 ore features and
 * 30 structures, plus biome-group lookups used by spawn and
 * structure placement code.
 */
public final class WorldGenKeys {

    // Biome ids (without namespace).
    public static final String CRYSTAL_SPIRE_REACH = "crystal_spire_reach";
    public static final String PRISMARINE_HOLLOWS = "prismarine_hollows";
    public static final String GLITTERFALL_CAVERNS = "glitterfall_caverns";
    public static final String QUARTZ_BLOOM_FLATS = "quartz_bloom_flats";
    public static final String AMETHYSTINE_RIDGE = "amethystine_ridge";
    public static final String SHATTERGLASS_DESERT = "shatterglass_desert";
    public static final String LUMINOUS_LEDGE = "luminous_ledge";
    public static final String ECHO_CRYSTAL_GROVE = "echo_crystal_grove";
    public static final String FROST_PRISM_BASIN = "frost_prism_basin";
    public static final String STAINED_GLASS_MESA = "stained_glass_mesa";
    public static final String EMBERITE_BASIN = "emberite_basin";
    public static final String ASHFALL_STEPPE = "ashfall_steppe";
    public static final String CINDER_BLOOM_FIELDS = "cinder_bloom_fields";
    public static final String MOLTEN_ARCHIPELAGO = "molten_archipelago";
    public static final String SOOTVEIL_WASTES = "sootveil_wastes";
    public static final String PYROCLAST_RIDGE = "pyroclast_ridge";
    public static final String HEARTHFIRE_GLADE = "hearthfire_glade";
    public static final String SCORCHED_BRAMBLE = "scorched_bramble";
    public static final String OBSIDIAN_DELTA = "obsidian_delta";
    public static final String MAGMA_VENT_GARDEN = "magma_vent_garden";
    public static final String VERDANT_CANOPY = "verdant_canopy";
    public static final String SYLVANITE_GARDENS = "sylvanite_gardens";
    public static final String MOSSBOUND_HOLLOW = "mossbound_hollow";
    public static final String ANCIENT_BOUGH_REACH = "ancient_bough_reach";
    public static final String PETALWIND_MEADOW = "petalwind_meadow";
    public static final String ROOTWOVEN_TANGLE = "rootwoven_tangle";
    public static final String FERNLIGHT_GROTTO = "fernlight_grotto";
    public static final String BLOOMING_THICKET = "blooming_thicket";
    public static final String EMERALD_CASCADE = "emerald_cascade";
    public static final String WHISPERLEAF_FOREST = "whisperleaf_forest";
    public static final String FROSTSTEEL_TUNDRA = "froststeel_tundra";
    public static final String RIMEVEIL_PEAKS = "rimeveil_peaks";
    public static final String SILENT_SNOWFIELD = "silent_snowfield";
    public static final String GLACIAL_CATHEDRAL = "glacial_cathedral";
    public static final String HOARFROST_MEADOW = "hoarfrost_meadow";
    public static final String BOREAL_CRYSTAL_TAIGA = "boreal_crystal_taiga";
    public static final String ICEBOUND_MIRE = "icebound_mire";
    public static final String POLAR_GLASS_SHORE = "polar_glass_shore";
    public static final String WINTER_BLOOM_GARDEN = "winter_bloom_garden";
    public static final String FROZEN_ZEPHYR_HOLLOWS = "frozen_zephyr_hollows";
    public static final String THUNDERGLASS_HIGHLANDS = "thunderglass_highlands";
    public static final String STORMCALL_PLATEAU = "stormcall_plateau";
    public static final String WINDSCARRED_BUTTES = "windscarred_buttes";
    public static final String RAINLASH_JUNGLE = "rainlash_jungle";
    public static final String CLOUDRIFT_SUMMIT = "cloudrift_summit";
    public static final String STATIC_BLOOM_FIELDS = "static_bloom_fields";
    public static final String MONSOON_DELTA = "monsoon_delta";
    public static final String SHRIEKING_WINDS_EXPANSE = "shrieking_winds_expanse";
    public static final String LIGHTNINGGLASS_SPIRE = "lightningglass_spire";
    public static final String TEMPEST_BASIN = "tempest_basin";
    public static final String MURKIRON_BOGS = "murkiron_bogs";
    public static final String PEAT_HOLLOW_MIRE = "peat_hollow_mire";
    public static final String DROWNED_ROOT_MARSH = "drowned_root_marsh";
    public static final String SPORECHOKED_MIRE = "sporechoked_mire";
    public static final String BLACKWILLOW_BAYOU = "blackwillow_bayou";
    public static final String SILTVEIL_FENS = "siltveil_fens";
    public static final String BOG_EMBER_QUAGMIRE = "bog_ember_quagmire";
    public static final String HOLLOWREED_WETLANDS = "hollowreed_wetlands";
    public static final String MIRE_GLASS_POOLS = "mire_glass_pools";
    public static final String GLOOMWATER_FLATS = "gloomwater_flats";
    public static final String SKYWISP_EXPANSE = "skywisp_expanse";
    public static final String SKYSTONE_ARCHIPELAGO = "skystone_archipelago";
    public static final String CLOUD_BLOOM_TERRACE = "cloud_bloom_terrace";
    public static final String ZEPHYR_GARDENS = "zephyr_gardens";
    public static final String HIGHWIND_PAMPAS = "highwind_pampas";
    public static final String AERIAL_SHOALS = "aerial_shoals";
    public static final String SUNSPIRE_ISLES = "sunspire_isles";
    public static final String FLOATING_REEF_HAVEN = "floating_reef_haven";
    public static final String WIND_DANCER_PLAINS = "wind_dancer_plains";
    public static final String HORIZON_STEPPE = "horizon_steppe";
    public static final String VOIDSHARD_RIFTS = "voidshard_rifts";
    public static final String GLOOMSHARD_DEPTHS = "gloomshard_depths";
    public static final String UNSEEING_ABYSS = "unseeing_abyss";
    public static final String WHISPERING_VOID_BARRENS = "whispering_void_barrens";
    public static final String NULLGLASS_WASTES = "nullglass_wastes";
    public static final String ECLIPSE_SHADE_REALM = "eclipse_shade_realm";
    public static final String STARLESS_HOLLOW = "starless_hollow";
    public static final String RIFTVEIL_TUNDRA = "riftveil_tundra";
    public static final String ENTROPY_SCARS = "entropy_scars";
    public static final String BLACK_SUN_BASIN = "black_sun_basin";

    private WorldGenKeys() {
    }

    /** Full biome key, e.g. "biomesunseen:crystal_spire_reach". */
    public static String biomeKey(String biomeId) {
        return ModConstants.NAMESPACE + biomeId;
    }

    /** Full ore feature key, e.g. "biomesunseen:azurethril_ore". */
    public static String oreFeatureKey(String oreId) {
        return ModConstants.NAMESPACE + oreId + "_ore";
    }

    /** Full structure key, e.g. "biomesunseen:ruined_sanctum". */
    public static String structureKey(String structureId) {
        return ModConstants.NAMESPACE + structureId;
    }

    /** All biome keys in catalog order. */
    public static Set<String> allBiomeKeys() {
        Set<String> out = new LinkedHashSet<String>();
        for (int i = 0; i < Content.BIOMES.size(); i++) {
            out.add(biomeKey(Content.BIOMES.get(i).id));
        }
        return Collections.unmodifiableSet(out);
    }

    /** Biome keys belonging to a group. */
    public static Set<String> biomeKeysInGroup(String group) {
        Set<String> out = new LinkedHashSet<String>();
        for (int i = 0; i < Content.BIOMES.size(); i++) {
            if (Content.BIOMES.get(i).group.equals(group)) {
                out.add(biomeKey(Content.BIOMES.get(i).id));
            }
        }
        return Collections.unmodifiableSet(out);
    }
}
