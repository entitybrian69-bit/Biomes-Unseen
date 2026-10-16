# -*- coding: utf-8 -*-
"""Emits worldgen Java for one API line: ModWorldGen, WorldGenKeys, legacy
biome-source injection helper + mixin (used where no API exists)."""

import os

from content import BIOME_ROWS, BIOME_GROUPS, ORE_ROWS, STRUCTURE_ROWS
from lines import LINES, types_for, registry_constant
from emit_families import _w, _s, _camel, _imports


def emit_worldgen(root, line_key):
    F = LINES[line_key]
    legacy = F["pkgs"] == "legacy"
    base = "common/src/line-%s/java/com/biomesunseen" % line_key
    wg = F["worldgen"]

    # ------------------------------------------------------------------ #
    # worldgen/WorldGenKeys.java
    # ------------------------------------------------------------------ #
    biome_consts = []
    for (bid, display, group, *_r) in BIOME_ROWS:
        biome_consts.append(
            '    public static final String %s = "%s";'
            % (bid.upper(), bid))
    _w(root, base + "/worldgen/WorldGenKeys.java", '''package com.biomesunseen.worldgen;

import com.biomesunseen.core.Content;
import com.biomesunseen.core.ModConstants;

import java.util.Collections;
import java.util.LinkedHashSet;
import java.util.Set;

/**
 * Stable id table for all %(n_biomes)s biomes, %(n_ores)s ore features and
 * %(n_structures)s structures, plus biome-group lookups used by spawn and
 * structure placement code.
 */
public final class WorldGenKeys {

    // Biome ids (without namespace).
%(biome_consts)s

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
''' % {
        "n_biomes": len(BIOME_ROWS),
        "n_ores": len(ORE_ROWS),
        "n_structures": len(STRUCTURE_ROWS),
        "biome_consts": "\n".join(biome_consts),
    })

    # ------------------------------------------------------------------ #
    # worldgen/ModWorldGen.java
    # ------------------------------------------------------------------ #
    if wg == "legacy":
        legacy_block = ""
        legacy_call = ""
        legacy_imports = ""
    else:
        legacy_block = ""
        legacy_call = ""
        legacy_imports = ""

    if F["biome_add"] == "mixin_legacy":
        inject_block = '''
    /**
     * Legacy overworld injection: a mixin calls UnseenBiomeSelector from the
     * biome provider so custom biomes appear in climate pockets.  Nothing to
     * do at runtime besides warming the selector's noise tables.
     */
    private static void installLegacyInjection() {
        UnseenBiomeSelector.warmUp();
    }
'''
        inject_call = "        installLegacyInjection();"
    else:
        inject_block = '''
    /**
     * Modern overworld injection: the shipped datapack overrides
     * multi_noise_biome_source_parameter_list/overworld.json so every custom
     * biome enters the climate system on all loaders.  Platform code adds
     * loader-specific biome modifications on top.
     */
    private static void installNoiseListInjection() {
        PlatformExpect.installBiomeInjection();
    }
'''
        inject_call = "        installNoiseListInjection();"

    _w(root, base + "/worldgen/ModWorldGen.java", '''package com.biomesunseen.worldgen;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.config.ModConfig;
import com.biomesunseen.core.Content;
import com.biomesunseen.core.ModConstants;
import com.biomesunseen.core.OreDef;
import com.biomesunseen.core.StructureDef;
import com.biomesunseen.platform.PlatformExpect;

import net.minecraft.resources.ResourceLocation;

/**
 * Worldgen orchestration for Minecraft %(mc)s.  Biomes, features and
 * structures ship as datapack JSON; this class wires the runtime side:
 * builtin registrations (legacy lines), biome injection and loader
 * modifications.  Ore rates and structure spacing honour the live config.
 */
public final class ModWorldGen {

    private static boolean prepared;
    private static boolean installed;

    private ModWorldGen() {
    }

    /** Construction phase: warm caches, validate content integrity. */
    public static synchronized void prepare() {
        if (prepared) {
            return;
        }
        prepared = true;
        // Validate the catalog up front so worldgen can never NPE later.
        for (int i = 0; i < Content.ORES.size(); i++) {
            OreDef ore = Content.ORES.get(i);
            if (ore.minY > ore.maxY) {
                throw new IllegalStateException("Ore " + ore.id + " has minY > maxY");
            }
        }
        for (int i = 0; i < Content.STRUCTURES.size(); i++) {
            StructureDef structure = Content.STRUCTURES.get(i);
            if (structure.separation >= structure.spacing) {
                throw new IllegalStateException("Structure " + structure.id + " separation >= spacing");
            }
        }
%(legacy_call)s
    }

    /** Setup phase: inject biomes and install loader modifications. */
    public static synchronized void install() {
        if (installed) {
            return;
        }
        installed = true;
%(inject_call)s
        PlatformExpect.installBiomeModifications();
    }

%(inject_block)s%(legacy_block)s
    /** Effective ore veins-per-chunk for one ore after config multiplication. */
    public static int veinsPerChunk(OreDef ore) {
        ModConfig config = BiomesUnseen.config();
        if (!config.enableAllOres) {
            return 0;
        }
        return ore.effectiveVeinsPerChunk(config.oreRateMultiplier);
    }

    /** Effective structure spacing after config multiplication. */
    public static int structureSpacing(StructureDef structure) {
        ModConfig config = BiomesUnseen.config();
        if (!config.enableAllStructures) {
            return Integer.MAX_VALUE;
        }
        return structure.effectiveSpacing(config.structureSpacingMultiplier);
    }

    /** Effective structure separation after config multiplication. */
    public static int structureSeparation(StructureDef structure) {
        return structure.effectiveSeparation(BiomesUnseen.config().structureSpacingMultiplier);
    }

    /** True when the biome group is enabled. */
    public static boolean biomeGroupEnabled(String group) {
        return BiomesUnseen.config().enableAllBiomes;
    }

    /** True when bosses may spawn in arenas. */
    public static boolean bossesEnabled() {
        return BiomesUnseen.config().enableBosses;
    }
}
''' % {
        "mc": F["mc"],
        "legacy_call": legacy_call,
        "inject_call": inject_call,
        "inject_block": inject_block,
        "legacy_block": legacy_block,
    })

    # ------------------------------------------------------------------ #
    # Legacy biome selector + mixin (mixin_legacy lines only)
    # ------------------------------------------------------------------ #
    if F["biome_add"] == "mixin_legacy":
        if legacy:
            sel_imports = ("import net.minecraft.util.RegistryKey;\n"
                           "import net.minecraft.util.registry.Registry;\n"
                           "import net.minecraft.world.biome.Biome;\n"
                           "import net.minecraft.util.ResourceLocation;")
            biome_t = "Biome"
        else:
            sel_imports = ("import net.minecraft.core.Registry;\n"
                           "import net.minecraft.resources.ResourceKey;\n"
                           "import net.minecraft.resources.ResourceLocation;\n"
                           "import net.minecraft.world.level.biome.Biome;")
            biome_t = "Biome"
        _w(root, base + "/worldgen/UnseenBiomeSelector.java", '''package com.biomesunseen.worldgen;

%(imports)s

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.core.BiomeDef;
import com.biomesunseen.core.Content;
import com.biomesunseen.core.MathUtil;
import com.biomesunseen.core.ModConstants;

import java.util.List;

/**
 * Climate-pocket biome selector used by the legacy biome-source mixin.  For
 * every column it decides deterministically (shared value-noise, cached)
 * whether an "unseen pocket" replaces the vanilla biome, and which custom
 * biome fills it based on temperature/depth matching.  No per-tick scans:
 * selection is O(1) per query and results are cache-friendly.
 */
public final class UnseenBiomeSelector {

    /** Chance a column becomes an unseen pocket (1/N). */
    private static final int POCKET_MODULO = 24;
    private static double[] WEIGHT_TABLE;
    private static boolean warmed;

    private UnseenBiomeSelector() {
    }

    /** Pre-compute the cumulative rarity table once. */
    public static synchronized void warmUp() {
        if (warmed) {
            return;
        }
        warmed = true;
        double multiplier = BiomesUnseen.config().biomeRarityMultiplier;
        List<BiomeDef> biomes = Content.BIOMES;
        WEIGHT_TABLE = new double[biomes.size()];
        double total = 0.0;
        for (int i = 0; i < biomes.size(); i++) {
            total += biomes.get(i).effectiveRarity(multiplier);
            WEIGHT_TABLE[i] = total;
        }
    }

    /**
     * Decide the custom biome for a block position, or null to keep vanilla.
     * Called from the biome provider mixin.
     */
    public static Object select(int x, int z, double vanillaTemperature) {
        warmUp();
        if (!BiomesUnseen.config().enableAllBiomes) {
            return null;
        }
        int noise = (int) (MathUtil.valueNoise2d(x >> 3, z >> 3, 0xB10) * 4096.0);
        if (noise %% POCKET_MODULO != 0) {
            return null;
        }
        double roll = MathUtil.valueNoise2d(x >> 5, z >> 5, 0x5EED);
        List<BiomeDef> biomes = Content.BIOMES;
        double total = WEIGHT_TABLE[biomes.size() - 1];
        if (total <= 0.0) {
            return null;
        }
        double target = roll * total;
        for (int i = 0; i < biomes.size(); i++) {
            if (target <= WEIGHT_TABLE[i]) {
                BiomeDef def = biomes.get(i);
                // Temperature band filter keeps tundra away from desert pockets.
                if (vanillaTemperature >= 1.0 && def.temperature < 0.4) {
                    return null;
                }
                if (vanillaTemperature <= 0.2 && def.temperature > 0.9) {
                    return null;
                }
                return biomeRegistryKey(def.id);
            }
        }
        return null;
    }

    private static Object biomeRegistryKey(String biomeId) {
        ResourceLocation location = new ResourceLocation(ModConstants.MOD_ID, biomeId);
        Registry<Biome> registry = com.biomesunseen.worldgen.LegacyBiomeRegistry.get();
        if (registry == null) {
            return null;
        }
        return registry.get(location);
    }
}
''' % {"imports": sel_imports})

        # Registry accessor that works on both legacy package generations.
        if legacy:
            reg_body = '''package com.biomesunseen.worldgen;

import net.minecraft.util.registry.Registry;
import net.minecraft.world.biome.Biome;

/**
 * Access to the server's biome registry (legacy line).
 */
public final class LegacyBiomeRegistry {

    private static Registry<Biome> biomes;

    private LegacyBiomeRegistry() {
    }

    /** Called from the mixin once the dynamic registry is available. */
    public static void set(Registry<Biome> registry) {
        biomes = registry;
    }

    public static Registry<Biome> get() {
        return biomes;
    }
}
'''
        else:
            reg_body = '''package com.biomesunseen.worldgen;

import net.minecraft.core.Registry;
import net.minecraft.world.level.biome.Biome;

/**
 * Access to the server's biome registry (legacy-injection line).
 */
public final class LegacyBiomeRegistry {

    private static Registry<Biome> biomes;

    private LegacyBiomeRegistry() {
    }

    /** Called from the mixin once the dynamic registry is available. */
    public static void set(Registry<Biome> registry) {
        biomes = registry;
    }

    public static Registry<Biome> get() {
        return biomes;
    }
}
'''
        _w(root, base + "/worldgen/LegacyBiomeRegistry.java", reg_body)

        # The mixin itself.  Targets the biome provider used by the overworld
        # on this package generation.
        if legacy:
            mixin_body = '''package com.biomesunseen.worldgen.mixin;

import net.minecraft.util.math.BlockPos;
import net.minecraft.world.biome.Biome;
import net.minecraft.world.biome.provider.BiomeProvider;

import com.biomesunseen.worldgen.UnseenBiomeSelector;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Mixin used only where no biome-injection API exists (1.16.5/1.17.1 and the
 * 1.18.1 line).  After the vanilla provider picks a biome, we may replace it
 * with a deterministic "unseen pocket" biome.
 */
@Mixin(BiomeProvider.class)
public abstract class BiomeProviderMixin {

    @Inject(method = "getNoiseBiome", at = @At("RETURN"), cancellable = true)
    private void biomesunseen$injectPocket(int x, int y, int z,
            CallbackInfoReturnable<Biome> cir) {
        Biome vanilla = cir.getReturnValue();
        if (vanilla == null) {
            return;
        }
        double temperature = vanilla.getBaseTemperature();
        Object replacement = UnseenBiomeSelector.select(x << 2, z << 2, temperature);
        if (replacement instanceof Biome) {
            cir.setReturnValue((Biome) replacement);
        }
    }
}
'''
        else:
            mixin_body = '''package com.biomesunseen.worldgen.mixin;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.BiomeSource;

import com.biomesunseen.worldgen.UnseenBiomeSelector;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Mixin used only where no biome-injection API exists (the 1.18.1 line).
 * After the vanilla biome source picks a biome, we may replace it with a
 * deterministic "unseen pocket" biome.
 */
@Mixin(BiomeSource.class)
public abstract class BiomeSourceMixin {

    @Inject(method = "getNoiseBiome", at = @At("RETURN"), cancellable = true)
    private void biomesunseen$injectPocket(int x, int y, int z,
            CallbackInfoReturnable<Biome> cir) {
        Biome vanilla = cir.getReturnValue();
        if (vanilla == null) {
            return;
        }
        double temperature = 0.7D;
        Object replacement = UnseenBiomeSelector.select(x << 2, z << 2, temperature);
        if (replacement instanceof Biome) {
            cir.setReturnValue((Biome) replacement);
        }
    }
}
'''
        mixin_name = "BiomeProviderMixin" if legacy else "BiomeSourceMixin"
        _w(root, base + "/worldgen/mixin/%s.java" % mixin_name, mixin_body)

    # ------------------------------------------------------------------ #


    # ------------------------------------------------------------------ #
    # Legacy structure separation registrar (structures="legacy" lines)
    # ------------------------------------------------------------------ #
    if F["structures"] == "legacy":
        # 1.16.5/1.17.1/1.18.1 all expose StructureFeature#STRUCTURES_REGISTRY
        # (BiMap<String, StructureFeature<?>>), the 3-arg
        # feature.configurations.StructureFeatureConfiguration and
        # net.minecraft.world.level.levelgen.StructureSettings - verified in the
        # ### ALL-CLASSES index of probe-fabric-1.16.5/1.17.1/1.18.1.
        struct_body = """package com.biomesunseen.worldgen;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.levelgen.StructureSettings;
import net.minecraft.world.level.levelgen.feature.StructureFeature;
import net.minecraft.world.level.levelgen.feature.configurations.StructureFeatureConfiguration;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.core.Content;
import com.biomesunseen.core.StructureDef;

/**
 * Registers separation settings for every jigsaw structure on lines where
 * structure spacing is code-driven (1.16.5/1.17.1/1.18.1).  The structure
 * definitions and jigsaw pools themselves ship as datapack JSON.
 */
public final class LegacyStructureRegistrar {

    private LegacyStructureRegistrar() {
    }

    /** Install separation settings for all structures. */
    public static void install() {
        for (int i = 0; i < Content.STRUCTURES.size(); i++) {
            StructureDef def = Content.STRUCTURES.get(i);
            if (!BiomesUnseen.config().enableAllStructures) {
                continue;
            }
            StructureFeature<?> structure = StructureFeature.STRUCTURES_REGISTRY.get(def.id);
            if (structure == null) {
                continue;
            }
            StructureFeatureConfiguration settings = new StructureFeatureConfiguration(
                    ModWorldGen.structureSpacing(def),
                    ModWorldGen.structureSeparation(def),
                    14357621);
            StructureSettings.DEFAULTS.put(structure, settings);
        }
    }
}
"""
        _w(root, base + "/worldgen/LegacyStructureRegistrar.java", struct_body)

        # Hook it into ModWorldGen.install()
        mg_path = os.path.join(root, base + "/worldgen/ModWorldGen.java")
        with open(mg_path) as fh:
            text = fh.read()
        text = text.replace(
            "        PlatformExpect.installBiomeModifications();",
            "        PlatformExpect.installBiomeModifications();\n"
            "        LegacyStructureRegistrar.install();")
        with open(mg_path, "w") as fh:
            fh.write(text)

