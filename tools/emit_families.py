# -*- coding: utf-8 -*-
"""Emits per-line Java source trees: registries, blocks, items, config,
worldgen, utilities.  Entity/client/datagen trees are emitted by
emit_families2.py.  Every line tree is complete, standalone Java."""

import os

from content import (MOD_ID, ORE_ROWS, DECOR_ROWS, PLANT_ROWS, BIOME_ROWS,
                     STRUCTURE_ROWS, MOB_ROWS, BOSS_ROWS, CONFIG_ROWS,
                     PARTICLE_TYPES)
from lines import LINES, types_for, registry_constant

PKG = "com/biomesunseen"


def _w(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def _s(v):
    return '"%s"' % str(v).replace("\\", "\\\\").replace('"', '\\"')


def _camel(oid):
    return "".join(part.capitalize() for part in oid.split("_"))


def _imports(flags, names):
    t = types_for(flags)
    seen = set()
    out = []
    for n in names:
        full = t[n]
        if full.startswith("java.") or full in seen:
            continue
        seen.add(full)
        out.append("import %s;" % full)
    return "\n".join(out)


def _reg(flags, kind):
    return registry_constant(flags, kind)


def _sound_event_expr(flags, rl_expr):
    if flags["sound_ctor"] == "factory":
        return "SoundEvent.createVariableRangeEvent(" + rl_expr + ")"
    return "new SoundEvent(" + rl_expr + ")"


def emit(root, line_key):
    F = LINES[line_key]
    T = types_for(F)
    base = "common/src/line-%s/java/com/biomesunseen" % line_key

    # ================================================================== #
    # BiomesUnseen.java - common bootstrap
    # ================================================================== #
    _w(root, base + "/BiomesUnseen.java", '''package com.biomesunseen;

import com.biomesunseen.config.ModConfig;
import com.biomesunseen.registry.ModRegistries;
import com.biomesunseen.worldgen.ModWorldGen;
import com.biomesunseen.core.ModConstants;

/**
 * Common bootstrap shared by every loader entrypoint for Minecraft %(mc)s.
 * Loaders call {@link #init()} during mod construction, {@link #setup()} at
 * registry freeze and {@link #initClient()} from the client entrypoint.
 */
public final class BiomesUnseen {

    public static final String MOD_ID = ModConstants.MOD_ID;

    private static ModConfig config = ModConfig.createDefault();
    private static boolean initialized;

    private BiomesUnseen() {
    }

    /** Loader-agnostic mod construction: registers and config. */
    public static synchronized void init() {
        if (initialized) {
            return;
        }
        initialized = true;
        config = ModConfig.load();
        ModRegistries.registerAll();
        ModWorldGen.prepare();
    }

    /** Registry-freeze phase: worldgen hooks, spawn caps, boss arenas. */
    public static void setup() {
        ModWorldGen.install();
    }

    /** Client-only phase: renderers, particles, config screen. */
    public static void initClient() {
        com.biomesunseen.client.ClientSetup.init();
    }

    public static ModConfig config() {
        return config;
    }

    /** Replace the live config (used by the Cloth Config save hook). */
    public static void setConfig(ModConfig newConfig) {
        config = newConfig;
        ModConfig.save(config);
        com.biomesunseen.util.SpawnCaps.reload();
    }

    public static String versionString() {
        return ModConstants.MOD_VERSION;
    }
}
''' % {"mc": F["mc"]})

    # ================================================================== #
    # config/ModConfig.java
    # ================================================================== #
    fields = []
    defaults = []
    parses = []
    for (key, typ, default, comment) in CONFIG_ROWS:
        jtype = {"double": "double", "int": "int", "boolean": "boolean"}[typ]
        parse = {"double": "Double.parseDouble(v)", "int": "Integer.parseInt(v)",
                 "boolean": "Boolean.parseBoolean(v)"}[typ]
        fields.append("    /** %s */\n    public %s %s;" % (comment, jtype, key))
        defaults.append("        cfg.%s = %s;" % (key, default))
        parses.append(
            "            if (@Q@%s@Q@.equals(key)) {\n"
            "                cfg.%s = %s;\n"
            "            }" % (key, key, parse))

    template = """package com.biomesunseen.config;

import com.biomesunseen.core.ModConstants;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Runtime configuration.  Stored as flat JSON in the loader config directory
 * and editable through Cloth Config.  All defaults enable every feature so
 * the world generates full of life out of the box.
 */
public final class ModConfig {

@FIELDS@

    private ModConfig() {
    }

    public static ModConfig createDefault() {
        ModConfig cfg = new ModConfig();
@DEFAULTS@
        return cfg;
    }

    private static File configFile() {
        return new File(@Q@config@Q@, ModConstants.CONFIG_FILE);
    }

    /** Load from disk, creating the file with defaults on first run. */
    public static ModConfig load() {
        ModConfig cfg = createDefault();
        File file = configFile();
        if (!file.exists()) {
            save(cfg);
            return cfg;
        }
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(
                new FileInputStream(file), StandardCharsets.UTF_8))) {
            Map<String, String> values = parseFlatJson(reader);
            cfg.apply(values);
        } catch (Exception ignored) {
            // Corrupt config: fall back to defaults and rewrite the file.
            save(cfg);
        }
        return cfg;
    }

    /** Write the config to disk as stable, human-editable JSON. */
    public static void save(ModConfig cfg) {
        try {
            File file = configFile();
            File parent = file.getParentFile();
            if (parent != null && !parent.exists()) {
                parent.mkdirs();
            }
            try (Writer writer = new OutputStreamWriter(
                    new FileOutputStream(file), StandardCharsets.UTF_8)) {
                writer.write(@Q@{@BS@n@Q@);
                Map<String, String> map = cfg.toMap();
                int i = 0;
                for (Map.Entry<String, String> entry : map.entrySet()) {
                    writer.write(@Q@  @BS@@Q@@Q@);
                    writer.write(entry.getKey());
                    writer.write(@Q@@BS@@Q@: @Q@);
                    writer.write(entry.getValue());
                    if (++i < map.size()) {
                        writer.write(@Q@,@Q@);
                    }
                    writer.write(@Q@@BS@n@Q@);
                }
                writer.write(@Q@}@BS@n@Q@);
            }
        } catch (Exception ignored) {
            // Best-effort persistence; defaults remain in memory.
        }
    }

    public Map<String, String> toMap() {
        Map<String, String> map = new LinkedHashMap<String, String>();
@TOMAP@
        return map;
    }

    public void apply(Map<String, String> values) {
        for (Map.Entry<String, String> entry : values.entrySet()) {
            String key = entry.getKey();
            String v = entry.getValue();
            if (v == null) {
                continue;
            }
            v = v.trim();
            try {
@PARSES@
            } catch (NumberFormatException ignored) {
                // Keep the current value for malformed entries.
            }
        }
    }

    /**
     * Minimal flat-JSON reader for @Q@{@Q@key@Q@: value@Q@}@Q@ documents.
     * Avoids a Gson dependency so the config layer compiles on every
     * Minecraft line.
     */
    private static Map<String, String> parseFlatJson(BufferedReader reader) throws Exception {
        Map<String, String> out = new LinkedHashMap<String, String>();
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            sb.append(line).append(@Q@@BS@n@Q@);
        }
        String text = sb.toString();
        int i = 0;
        int n = text.length();
        while (i < n) {
            int keyStart = text.indexOf(@Q@@BS@@Q@@Q@, i);
            if (keyStart < 0) {
                break;
            }
            int keyEnd = text.indexOf(@Q@@BS@@Q@@Q@, keyStart + 1);
            if (keyEnd < 0) {
                break;
            }
            String key = text.substring(keyStart + 1, keyEnd);
            int colon = text.indexOf(@Q@:@Q@, keyEnd);
            if (colon < 0) {
                break;
            }
            int j = colon + 1;
            while (j < n && Character.isWhitespace(text.charAt(j))) {
                j++;
            }
            int k = j;
            while (k < n && text.charAt(k) != @Q@,@Q@.charAt(0)
                    && text.charAt(k) != @Q@@BS@n@Q@.charAt(0)
                    && text.charAt(k) != @Q@}@Q@.charAt(0)) {
                k++;
            }
            String value = text.substring(j, k).trim();
            out.put(key, value);
            i = k;
        }
        return out;
    }
}
"""
    template = template.replace("@FIELDS@", "\n\n".join(fields))
    template = template.replace("@DEFAULTS@", "\n".join(defaults))
    template = template.replace("@TOMAP@", "\n".join(
        "        map.put(@Q@%s@Q@, String.valueOf(%s));" % (k, k)
        for (k, _t, _d, _c) in CONFIG_ROWS))
    template = template.replace("@PARSES@", "\n".join(parses))
    template = template.replace("@Q@", '"').replace("@BS@", "\\")
    _w(root, base + "/config/ModConfig.java", template)

    # ================================================================== #
    # config/ClothConfigScreen.java
    # ================================================================== #
    category_rows = []
    for (key, typ, _default, comment) in CONFIG_ROWS:
        entry = "        entries.addEntry(configBuilder.startTextComment(ComponentLike.literal(\\\"%s\\\"))" % comment
        category_rows.append(key)
    _w(root, base + "/config/ClothConfigScreen.java", '''package com.biomesunseen.config;

import com.biomesunseen.BiomesUnseen;

import net.minecraft.network.chat.Component;

import java.lang.reflect.Method;
import java.util.function.Consumer;
import java.util.function.UnaryOperator;

/**
 * Cloth Config screen factory.  Every ModConfig field is editable, grouped
 * into gameplay categories, and persisted through ModConfig.save on close.
 * The platform layer supplies the parent screen and translation text so this
 * class stays free of version-specific client calls.
 *
 * <p>Cloth Config is accessed reflectively and is an optional runtime
 * dependency: when Cloth Config is installed the full editable screen is
 * built; when it is absent this factory returns the parent screen unchanged.
 * Reflection keeps every Minecraft-version module compilable without a
 * version-specific Cloth Config artifact on the classpath.</p>
 */
public final class ClothConfigScreen {

    private ClothConfigScreen() {
    }

    /**
     * Build the Cloth Config screen.
     *
     * @param title display title of the screen
     * @param parent the screen to return to
     * @param translator translation lookup used for labels
     * @return the finished screen, or the parent screen when Cloth Config is absent
     */
    public static Object build(String title, Object parent, UnaryOperator<String> translator) {
        Class<?> builderType;
        try {
            builderType = Class.forName("me.shedaniel.clothconfig2.api.ConfigBuilder");
        } catch (ClassNotFoundException missing) {
            // Cloth Config is optional; without it there is no screen to open.
            return parent;
        }
        try {
            Object builder = callStatic(builderType, "create");
            call(builder, "setTitle", Component.literal(title));
            call(builder, "setSavingRunnable",
                    (Runnable) () -> BiomesUnseen.setConfig(BiomesUnseen.config()));
            if (parent != null) {
                call(builder, "setParentScreen", parent);
            }
            Object entryBuilder = call(builder, "entryBuilder");
            ModConfig cfg = BiomesUnseen.config();

            Object general = call(builder, "getOrCreateCategory", Component.literal("General"));
            addBool(general, entryBuilder, translator.apply("enableAllBiomes"), cfg.enableAllBiomes, true, v -> cfg.enableAllBiomes = v);
            addBool(general, entryBuilder, translator.apply("enableAllOres"), cfg.enableAllOres, true, v -> cfg.enableAllOres = v);
            addBool(general, entryBuilder, translator.apply("enableAllStructures"), cfg.enableAllStructures, true, v -> cfg.enableAllStructures = v);
            addBool(general, entryBuilder, translator.apply("enableAllMobs"), cfg.enableAllMobs, true, v -> cfg.enableAllMobs = v);
            addBool(general, entryBuilder, translator.apply("enableBosses"), cfg.enableBosses, true, v -> cfg.enableBosses = v);
            addBool(general, entryBuilder, translator.apply("enableLoreBooks"), cfg.enableLoreBooks, true, v -> cfg.enableLoreBooks = v);
            addBool(general, entryBuilder, translator.apply("enableStructureLoot"), cfg.enableStructureLoot, true, v -> cfg.enableStructureLoot = v);

            Object world = call(builder, "getOrCreateCategory", Component.literal("World"));
            addDouble(world, entryBuilder, translator.apply("biomeRarityMultiplier"), cfg.biomeRarityMultiplier, 1.0D, 0.0D, 10.0D, v -> cfg.biomeRarityMultiplier = v);
            addDouble(world, entryBuilder, translator.apply("biomeTerraformingStrength"), cfg.biomeTerraformingStrength, 1.0D, 0.0D, 3.0D, v -> cfg.biomeTerraformingStrength = v);
            addDouble(world, entryBuilder, translator.apply("oreRateMultiplier"), cfg.oreRateMultiplier, 1.0D, 0.0D, 10.0D, v -> cfg.oreRateMultiplier = v);
            addDouble(world, entryBuilder, translator.apply("structureSpacingMultiplier"), cfg.structureSpacingMultiplier, 1.0D, 0.1D, 10.0D, v -> cfg.structureSpacingMultiplier = v);
            addDouble(world, entryBuilder, translator.apply("weatherIntensity"), cfg.weatherIntensity, 1.0D, 0.0D, 3.0D, v -> cfg.weatherIntensity = v);
            addInt(world, entryBuilder, translator.apply("structureLodDistance"), cfg.structureLodDistance, 128, 16, 1024, v -> cfg.structureLodDistance = v);

            Object mobs = call(builder, "getOrCreateCategory", Component.literal("Mobs & Performance"));
            addDouble(mobs, entryBuilder, translator.apply("mobSpawnMultiplier"), cfg.mobSpawnMultiplier, 1.0D, 0.0D, 10.0D, v -> cfg.mobSpawnMultiplier = v);
            addInt(mobs, entryBuilder, translator.apply("mobGlobalCap"), cfg.mobGlobalCap, 180, 0, 2000, v -> cfg.mobGlobalCap = v);
            addInt(mobs, entryBuilder, translator.apply("entityAiThrottle"), cfg.entityAiThrottle, 2, 1, 20, v -> cfg.entityAiThrottle = v);
            addDouble(mobs, entryBuilder, translator.apply("ambientParticleDensity"), cfg.ambientParticleDensity, 1.0D, 0.0D, 3.0D, v -> cfg.ambientParticleDensity = v);
            addDouble(mobs, entryBuilder, translator.apply("musicFrequencyMultiplier"), cfg.musicFrequencyMultiplier, 1.0D, 0.1D, 10.0D, v -> cfg.musicFrequencyMultiplier = v);
            addBool(mobs, entryBuilder, translator.apply("enableAdaptiveMobs"), cfg.enableAdaptiveMobs, true, v -> cfg.enableAdaptiveMobs = v);
            addBool(mobs, entryBuilder, translator.apply("enablePackTactics"), cfg.enablePackTactics, true, v -> cfg.enablePackTactics = v);

            return call(builder, "build");
        } catch (ReflectiveOperationException e) {
            throw new IllegalStateException("Cloth Config API could not be accessed", e);
        }
    }

    /** Add one boolean entry to a category. */
    private static void addBool(Object category, Object entryBuilder, String label,
                                boolean value, boolean defaultValue, Consumer<Boolean> save)
            throws ReflectiveOperationException {
        Object entry = call(entryBuilder, "startBooleanField", Component.literal(label), Boolean.valueOf(value));
        entry = call(entry, "setDefaultValue", Boolean.valueOf(defaultValue));
        entry = call(entry, "setSaveConsumer", save);
        call(category, "addEntry", call(entry, "build"));
    }

    /** Add one double entry with slider bounds to a category. */
    private static void addDouble(Object category, Object entryBuilder, String label,
                                  double value, double defaultValue, double min, double max,
                                  Consumer<Double> save)
            throws ReflectiveOperationException {
        Object entry = call(entryBuilder, "startDoubleField", Component.literal(label), Double.valueOf(value));
        entry = call(entry, "setDefaultValue", Double.valueOf(defaultValue));
        entry = call(entry, "setMin", Double.valueOf(min));
        entry = call(entry, "setMax", Double.valueOf(max));
        entry = call(entry, "setSaveConsumer", save);
        call(category, "addEntry", call(entry, "build"));
    }

    /** Add one integer entry with bounds to a category. */
    private static void addInt(Object category, Object entryBuilder, String label,
                               int value, int defaultValue, int min, int max,
                               Consumer<Integer> save)
            throws ReflectiveOperationException {
        Object entry = call(entryBuilder, "startIntField", Component.literal(label), Integer.valueOf(value));
        entry = call(entry, "setDefaultValue", Integer.valueOf(defaultValue));
        entry = call(entry, "setMin", Integer.valueOf(min));
        entry = call(entry, "setMax", Integer.valueOf(max));
        entry = call(entry, "setSaveConsumer", save);
        call(category, "addEntry", call(entry, "build"));
    }

    /** Invoke the named instance method whose parameters accept the given arguments. */
    private static Object call(Object target, String name, Object... args)
            throws ReflectiveOperationException {
        Method method = find(target.getClass(), name, args);
        return method.invoke(target, args);
    }

    /** Invoke the named static method whose parameters accept the given arguments. */
    private static Object callStatic(Class<?> type, String name, Object... args)
            throws ReflectiveOperationException {
        Method method = find(type, name, args);
        return method.invoke(null, args);
    }

    /** Find the uniquely matching method by name, arity and boxed argument types. */
    private static Method find(Class<?> type, String name, Object[] args) {
        Method match = null;
        for (Method method : type.getMethods()) {
            if (!method.getName().equals(name)
                    || method.getParameterCount() != args.length) {
                continue;
            }
            Class<?>[] params = method.getParameterTypes();
            boolean ok = true;
            for (int i = 0; i < params.length; i++) {
                if (args[i] == null) {
                    if (params[i].isPrimitive()) {
                        ok = false;
                        break;
                    }
                } else if (!wrap(params[i]).isInstance(args[i])) {
                    ok = false;
                    break;
                }
            }
            if (ok) {
                match = method;
                break;
            }
        }
        if (match == null) {
            throw new IllegalStateException(
                    "No method " + type.getName() + "#" + name + " accepts the given arguments");
        }
        return match;
    }

    /** Box primitive parameter types so isInstance checks work for both. */
    private static Class<?> wrap(Class<?> type) {
        if (!type.isPrimitive()) {
            return type;
        }
        if (type == boolean.class) return Boolean.class;
        if (type == byte.class) return Byte.class;
        if (type == short.class) return Short.class;
        if (type == char.class) return Character.class;
        if (type == int.class) return Integer.class;
        if (type == long.class) return Long.class;
        if (type == float.class) return Float.class;
        if (type == double.class) return Double.class;
        return type;
    }
}
''')

    # ================================================================== #
    # platform/PlatformExpect.java
    # ================================================================== #
    expect_pkg = ("me.shedaniel.architectury.injectables.annotations.ExpectPlatform"
                  if F["expect"] == "me.shedaniel"
                  else "dev.architectury.injectables.annotations.ExpectPlatform")
    _w(root, base + "/platform/PlatformExpect.java", '''package com.biomesunseen.platform;

import %(expect)s;

/**
 * Loader-specific hooks.  Each platform module ships
 * com.biomesunseen.platform.PlatformExpectImpl with the concrete behaviour.
 */
public final class PlatformExpect {

    private PlatformExpect() {
    }

    /** True when running on Fabric. */
    @ExpectPlatform
    public static boolean isFabric() {
        throw new AssertionError();
    }

    /** True when running on Forge or NeoForge. */
    @ExpectPlatform
    public static boolean isForgeLike() {
        throw new AssertionError();
    }

    /** Loader config directory (contains biomesunseen.json). */
    @ExpectPlatform
    public static String configDirectory() {
        throw new AssertionError();
    }

    /** Open the Cloth Config screen for Biomes Unseen. */
    @ExpectPlatform
    public static void openConfigScreen(Object parentScreen) {
        throw new AssertionError();
    }

    /**
     * Register spawn placements for one mob id (ground/monster/water rules
     * handled by the platform entity spawn API).
     */
    @ExpectPlatform
    public static void registerSpawnPlacement(String mobId,
            net.minecraft.world.entity.EntityType<net.minecraft.world.entity.Mob> type) {
        throw new AssertionError();
    }

    /** Inject every custom biome into the overworld climate system. */
    @ExpectPlatform
    public static void installBiomeInjection() {
        throw new AssertionError();
    }

    /** Register biome modification hooks (features, spawns, ambience). */
    @ExpectPlatform
    public static void installBiomeModifications() {
        throw new AssertionError();
    }

    /** Play a global music disc-style track inside a boss arena. */
    @ExpectPlatform
    public static void playBossMusic(net.minecraft.server.level.ServerLevel level,
            net.minecraft.core.BlockPos center, String soundEventId, int radius) {
        throw new AssertionError();
    }

    /** True when the given mod id is loaded (used for optional compat). */
    @ExpectPlatform
    public static boolean isModLoaded(String modId) {
        throw new AssertionError();
    }
}
''' % {"expect": expect_pkg})

    # ================================================================== #
    # util/AiThrottle.java
    # ================================================================== #
    _w(root, base + "/util/AiThrottle.java", '''package com.biomesunseen.util;

import com.biomesunseen.BiomesUnseen;

/**
 * Central AI throttling.  Custom mobs only think every N ticks (config
 * "entityAiThrottle"), which keeps large mob counts cheap without making
 * behaviour visibly stiff: goals still run on their own cadence.
 */
public final class AiThrottle {

    private AiThrottle() {
    }

    /** Effective think interval in ticks, minimum 1. */
    public static int interval() {
        int v = BiomesUnseen.config().entityAiThrottle;
        return v < 1 ? 1 : v;
    }

    /**
     * True when the entity with the given id should think this tick.
     * Deterministic stagger spreads decisions across the interval.
     */
    public static boolean shouldThink(int entityId, long gameTime) {
        int interval = interval();
        return ((gameTime + (entityId % interval)) % interval) == 0L;
    }

    /** Reduced goal-flag evaluation for throttled entities. */
    public static boolean cheapCanUse(int entityId, long gameTime, int cost) {
        if (cost <= 1) {
            return true;
        }
        return shouldThink(entityId, gameTime);
    }
}
''')

    # ================================================================== #
    # util/SpawnCaps.java
    # ================================================================== #
    _w(root, base + "/util/SpawnCaps.java", '''package com.biomesunseen.util;

import com.biomesunseen.BiomesUnseen;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Global custom-mob cap enforcement.  Loaded counts are tracked per dimension
 * and checked before every spawn so mob farms cannot flood the server.
 */
public final class SpawnCaps {

    private static final Map<String, AtomicInteger> COUNTS = new ConcurrentHashMap<String, AtomicInteger>();
    private static volatile int cap = 180;

    private SpawnCaps() {
    }

    static {
        reload();
    }

    /** Re-read the cap from config (called when the config changes). */
    public static void reload() {
        int v = BiomesUnseen.config().mobGlobalCap;
        cap = v < 0 ? 0 : v;
    }

    /** True when a custom mob may spawn in this dimension. */
    public static boolean allowSpawn(String dimensionKey) {
        AtomicInteger counter = COUNTS.get(dimensionKey);
        if (counter == null) {
            counter = new AtomicInteger();
            COUNTS.put(dimensionKey, counter);
        }
        return counter.get() < cap;
    }

    /** Track a spawn. */
    public static void onSpawn(String dimensionKey) {
        AtomicInteger counter = COUNTS.get(dimensionKey);
        if (counter == null) {
            counter = new AtomicInteger();
            COUNTS.put(dimensionKey, counter);
        }
        counter.incrementAndGet();
    }

    /** Track a death/despawn. */
    public static void onRemoved(String dimensionKey) {
        AtomicInteger counter = COUNTS.get(dimensionKey);
        if (counter != null) {
            counter.updateAndGet(v -> v > 0 ? v - 1 : 0);
        }
    }

    public static int currentCount(String dimensionKey) {
        AtomicInteger counter = COUNTS.get(dimensionKey);
        return counter == null ? 0 : counter.get();
    }
}
''')

    # ================================================================== #
    # util/LodCache.java
    # ================================================================== #
    _w(root, base + "/util/LodCache.java", '''package com.biomesunseen.util;

import com.biomesunseen.BiomesUnseen;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Level-of-detail cache for distant structure starts.  Structure placement
 * queries outside the configured radius are answered from this LRU cache
 * instead of re-running noise/placement code every chunk tick.
 */
public final class LodCache {

    private static final int MAX_ENTRIES = 4096;
    private static final Map<Long, Boolean> STRUCTURE_PRESENCE =
            new LinkedHashMap<Long, Boolean>(256, 0.75F, true) {
                @Override
                protected boolean removeEldestEntry(Map.Entry<Long, Boolean> eldest) {
                    return size() > MAX_ENTRIES;
                }
            };

    private LodCache() {
    }

    /** Chunk-radius within which structure starts are fully resolved. */
    public static int lodRadius() {
        int v = BiomesUnseen.config().structureLodDistance;
        return v < 16 ? 16 : v;
    }

    /** True when a chunk is within the full-resolution band. */
    public static boolean isHighDetail(long chunkX, long chunkZ, long cameraX, long cameraZ) {
        long dx = chunkX - cameraX;
        long dz = chunkZ - cameraZ;
        long r = lodRadius() >> 4;
        return dx * dx + dz * dz <= r * r;
    }

    /** Cached structure-presence query (chunk key packed as x/z). */
    public static Boolean cachedPresence(long chunkKey, java.util.function.Supplier<Boolean> compute) {
        synchronized (STRUCTURE_PRESENCE) {
            Boolean value = STRUCTURE_PRESENCE.get(chunkKey);
            if (value != null) {
                return value;
            }
        }
        Boolean computed = compute.get();
        synchronized (STRUCTURE_PRESENCE) {
            STRUCTURE_PRESENCE.put(chunkKey, computed);
        }
        return computed;
    }

    /** Pack a chunk position into a cache key. */
    public static long chunkKey(int chunkX, int chunkZ) {
        return ((long) chunkX << 32) ^ (chunkZ & 0xFFFFFFFFL);
    }

    /** Drop all cached entries (called on dimension unload). */
    public static void invalidate() {
        synchronized (STRUCTURE_PRESENCE) {
            STRUCTURE_PRESENCE.clear();
        }
    }
}
''')

    # ================================================================== #
    # block/UnseenOreBlock.java
    # ================================================================== #
    mat_args = "net.minecraft.world.level.material.MapColor" if F["pkgs"] == "modern" else "net.minecraft.block.material.Material"
    if F["material"]:
        props_expr = ("BlockBehaviour.Properties.of(Material.STONE, MapColor.NONE)"
                      if F["pkgs"] == "modern"
                      else "AbstractBlock.Properties.of(Material.STONE)")
    else:
        props_expr = "BlockBehaviour.Properties.of()"
    # 1.16/1.17 use Material; 1.18-1.19.2 mojmap still has Material + MapColor variants.
    if F["pkgs"] == "legacy":
        ore_props = "AbstractBlock.Properties.of(Material.STONE).strength(3.0F, 3.0F)"
    elif F["material"]:
        ore_props = ("BlockBehaviour.Properties.of(Material.STONE).strength(3.0F, 3.0F)"
                     if F["mc"] in ("1.17.1", "1.18.2")
                     else "BlockBehaviour.Properties.of().strength(3.0F, 3.0F)")
    else:
        ore_props = "BlockBehaviour.Properties.of().strength(3.0F, 3.0F)"
    _w(root, base + "/block/UnseenOreBlock.java", '''package com.biomesunseen.block;

%(imports)s

import com.biomesunseen.core.OreDef;

/**
 * A custom ore block.  Carries its OreDef for loot/particle/mining behaviour
 * and glows when the ore definition calls for it.
 */
public class UnseenOreBlock extends Block {

    private final OreDef ore;

    public UnseenOreBlock(OreDef ore) {
        super(buildProperties(ore));
        this.ore = ore;
    }

    private static BlockBehaviour.Properties buildProperties(OreDef ore) {
        BlockBehaviour.Properties properties = %(props)s;
        if (ore.glows) {
            properties = properties.lightLevel(state -> 8);
        }
        return properties.randomTicks();
    }

    public OreDef ore() {
        return ore;
    }

    /** Mining particle colour used by the platform particle hook. */
    public int particleColor() {
        return ore.particleColor;
    }

    /** Mining sound event id (always the shared ore chime set). */
    public String miningSoundId() {
        return "block.biomesunseen.ore_chime";
    }
}
''' % {
        "imports": _imports(F, ["Block", "BlockBehaviour"]),
        "props": ore_props,
    })

    # ================================================================== #
    # block/UnseenDecorBlock.java
    # ================================================================== #
    if F["pkgs"] == "legacy":
        decor_props = ("AbstractBlock.Properties.of(%s).strength(1.5F, 6.0F)"
                       % "Material.STONE")
    else:
        decor_props = "BlockBehaviour.Properties.of()"
    _w(root, base + "/block/UnseenDecorBlock.java", '''package com.biomesunseen.block;

%(imports)s

import com.biomesunseen.core.DecorDef;

/**
 * Decorative palette block used by biome terrain and structures.
 */
public class UnseenDecorBlock extends Block {

    private final DecorDef decor;

    public UnseenDecorBlock(DecorDef decor) {
        super(buildProperties(decor));
        this.decor = decor;
    }

    private static BlockBehaviour.Properties buildProperties(DecorDef decor) {
        BlockBehaviour.Properties properties = %(props)s;
        properties = properties.strength("stone".equals(decor.material) ? 1.5F : 1.0F, 6.0F);
        if (decor.isTransparent()) {
            properties = properties.noOcclusion().isViewBlocking((state, getter, pos) -> false);
        }
        if (decor.lightLevel() > 0) {
            properties = properties.lightLevel(state -> decor.lightLevel());
        }
        return properties;
    }

    public DecorDef decor() {
        return decor;
    }
}
''' % {
        "imports": _imports(F, ["Block", "BlockBehaviour"]),
        "props": decor_props,
    })

    # ================================================================== #
    # block/UnseenPlantBlock.java
    # ================================================================== #
    if F["pkgs"] == "legacy":
        plant_super = "net.minecraft.block.GrassBlock"
        # Use a simple BushBlock-like behaviour: extend Block with no collision
        plant_extends = "Block"
    else:
        plant_extends = "Block"
    _w(root, base + "/block/UnseenPlantBlock.java", '''package com.biomesunseen.block;

%(imports)s

import com.biomesunseen.core.PlantDef;

/**
 * Decorative plant block: cross-shaped, fragile, optionally pottable.
 * Non-solid so the world stays walkable and alive.
 */
public class UnseenPlantBlock extends Block {

    private final PlantDef plant;

    public UnseenPlantBlock(PlantDef plant) {
        super(buildProperties());
        this.plant = plant;
    }

    private static BlockBehaviour.Properties buildProperties() {
        BlockBehaviour.Properties properties = %(props)s;
        return properties.noCollission().instabreak().offsetType(BlockBehaviour.OffsetType.XZ)
                .sound(SoundType.GRASS);
    }

    public PlantDef plant() {
        return plant;
    }
}
''' % {
        "imports": _imports(F, ["Block", "BlockBehaviour", "SoundType"]),
        "props": ("AbstractBlock.Properties.of(net.minecraft.block.material.Material.PLANT)"
                  if F["pkgs"] == "legacy" else "BlockBehaviour.Properties.of()"),
    })

    # ================================================================== #
    # item/UnseenToolTier.java (legacy and modern method names)
    # ================================================================== #
    if F["pkgs"] == "legacy":
        tier_body = '''package com.biomesunseen.item;

import net.minecraft.item.IItemTier;
import net.minecraft.item.crafting.Ingredient;

import com.biomesunseen.core.OreDef;

import java.util.function.Supplier;

/**
 * Tool tier derived from an ore definition: durability, mining level, speed
 * and enchantability all come straight from the ore catalog.
 */
public class UnseenToolTier implements IItemTier {

    private final OreDef ore;
    private final Supplier<Ingredient> repairIngredient;

    public UnseenToolTier(OreDef ore, Supplier<Ingredient> repairIngredient) {
        this.ore = ore;
        this.repairIngredient = repairIngredient;
    }

    @Override
    public int getMaxUses() {
        return ore.toolDurability;
    }

    @Override
    public float getEfficiency() {
        return (float) ore.toolSpeed;
    }

    @Override
    public float getAttackDamageBonus() {
        return (float) ore.toolAttackDamage;
    }

    @Override
    public int getHarvestLevel() {
        return ore.toolMiningLevel;
    }

    @Override
    public int getEnchantability() {
        return ore.toolEnchantability;
    }

    @Override
    public Ingredient getRepairMaterial() {
        return repairIngredient.get();
    }

    public OreDef ore() {
        return ore;
    }
}
'''
    else:
        tier_body = '''package com.biomesunseen.item;

import net.minecraft.world.item.Tier;
import net.minecraft.world.item.crafting.Ingredient;

import com.biomesunseen.core.OreDef;

import java.util.function.Supplier;

/**
 * Tool tier derived from an ore definition: durability, mining level, speed
 * and enchantability all come straight from the ore catalog.
 */
public class UnseenToolTier implements Tier {

    private final OreDef ore;
    private final Supplier<Ingredient> repairIngredient;

    public UnseenToolTier(OreDef ore, Supplier<Ingredient> repairIngredient) {
        this.ore = ore;
        this.repairIngredient = repairIngredient;
    }

    @Override
    public int getUses() {
        return ore.toolDurability;
    }

    @Override
    public float getSpeed() {
        return (float) ore.toolSpeed;
    }

    @Override
    public float getAttackDamageBonus() {
        return (float) ore.toolAttackDamage;
    }

    @Override
    public int getLevel() {
        return ore.toolMiningLevel;
    }

    @Override
    public int getEnchantmentValue() {
        return ore.toolEnchantability;
    }

    @Override
    public Ingredient getRepairIngredient() {
        return repairIngredient.get();
    }

    public OreDef ore() {
        return ore;
    }
}
'''
    _w(root, base + "/item/UnseenToolTier.java", tier_body)

    if F["pkgs"] == "legacy":
        armor_body = '''package com.biomesunseen.item;

import net.minecraft.inventory.EquipmentSlotType;
import net.minecraft.item.IArmorMaterial;
import net.minecraft.item.crafting.Ingredient;
import net.minecraft.util.SoundEvent;
import net.minecraft.util.SoundEvents;

import com.biomesunseen.core.OreDef;

import java.util.function.Supplier;

/**
 * Armor material derived from an ore definition.  Defense values scale with
 * the ore's tool tier so stronger ores make stronger armor.
 */
public class UnseenArmorMaterial implements IArmorMaterial {

    private static final int[] BASE_DURABILITY = new int[]{13, 15, 16, 11};
    private static final int[] BASE_DEFENSE = new int[]{2, 5, 6, 2};

    private final OreDef ore;
    private final Supplier<Ingredient> repairIngredient;

    public UnseenArmorMaterial(OreDef ore, Supplier<Ingredient> repairIngredient) {
        this.ore = ore;
        this.repairIngredient = repairIngredient;
    }

    @Override
    public int getDurabilityForSlot(EquipmentSlotType slot) {
        return BASE_DURABILITY[slot.getIndex()] * (ore.toolDurability / 33);
    }

    @Override
    public int getDefenseForSlot(EquipmentSlotType slot) {
        return BASE_DEFENSE[slot.getIndex()] + ore.toolMiningLevel;
    }

    @Override
    public int getEnchantmentValue() {
        return ore.toolEnchantability;
    }

    @Override
    public SoundEvent getEquipSound() {
        return SoundEvents.ARMOR_EQUIP_IRON;
    }

    @Override
    public Ingredient getRepairMaterial() {
        return repairIngredient.get();
    }

    @Override
    public String getName() {
        return "biomesunseen:" + ore.id;
    }

    @Override
    public float getToughness() {
        return ore.toolMiningLevel * 0.5F;
    }

    @Override
    public float getKnockbackResistance() {
        return ore.toolMiningLevel >= 4 ? 0.1F : 0.0F;
    }

    public OreDef ore() {
        return ore;
    }
}
'''
    else:
        armor_body = '''package com.biomesunseen.item;

import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;

import com.biomesunseen.core.OreDef;

import java.util.function.Supplier;

/**
 * Armor material derived from an ore definition.  Defense values scale with
 * the ore's tool tier so stronger ores make stronger armor.
 */
public class UnseenArmorMaterial implements ArmorMaterial {

    private static final int[] BASE_DURABILITY = new int[]{13, 15, 16, 11};
    private static final int[] BASE_DEFENSE = new int[]{2, 5, 6, 2};

    private final OreDef ore;
    private final Supplier<Ingredient> repairIngredient;

    public UnseenArmorMaterial(OreDef ore, Supplier<Ingredient> repairIngredient) {
        this.ore = ore;
        this.repairIngredient = repairIngredient;
    }

    @Override
    public int getDurabilityForSlot(EquipmentSlot slot) {
        return BASE_DURABILITY[slot.getIndex()] * (ore.toolDurability / 33);
    }

    @Override
    public int getDefenseForSlot(EquipmentSlot slot) {
        return BASE_DEFENSE[slot.getIndex()] + ore.toolMiningLevel;
    }

    @Override
    public int getEnchantmentValue() {
        return ore.toolEnchantability;
    }

    @Override
    public SoundEvent getEquipSound() {
        return SoundEvents.ARMOR_EQUIP_IRON;
    }

    @Override
    public Ingredient getRepairIngredient() {
        return repairIngredient.get();
    }

    @Override
    public String getName() {
        return "biomesunseen:" + ore.id;
    }

    @Override
    public float getToughness() {
        return ore.toolMiningLevel * 0.5F;
    }

    @Override
    public float getKnockbackResistance() {
        return ore.toolMiningLevel >= 4 ? 0.1F : 0.0F;
    }

    public OreDef ore() {
        return ore;
    }
}
'''
    _w(root, base + "/item/UnseenArmorMaterial.java", armor_body)

    # ================================================================== #
    # item/UnseenGearItems.java - pickaxe/sword/armor factories
    # ================================================================== #
    if F["pkgs"] == "legacy":
        gear_head = '''package com.biomesunseen.item;

import net.minecraft.inventory.EquipmentSlotType;
import net.minecraft.item.ArmorItem;
import net.minecraft.item.IArmorMaterial;
import net.minecraft.item.IItemTier;
import net.minecraft.item.Item;
import net.minecraft.item.PickaxeItem;
import net.minecraft.item.SwordItem;

import com.biomesunseen.core.OreDef;
'''
        armor_slot_expr = "EquipmentSlotType"
        pickaxe_ctor = "super(tier, (int) ore.toolAttackDamage - 1, (float) (ore.toolSpeed / 2.5) - 2.4F, properties)"
        sword_ctor = "super(tier, (int) ore.toolAttackDamage, (float) (ore.toolSpeed / 2.5), properties)"
        gear_factories = '''    public static PickaxeItem pickaxe(OreDef ore, UnseenToolTier tier, Item.Properties properties) {
        return new UnseenPickaxeItem(ore, tier, properties);
    }

    public static SwordItem sword(OreDef ore, UnseenToolTier tier, Item.Properties properties) {
        return new UnseenSwordItem(ore, tier, properties);
    }

    public static ArmorItem helmet(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, EquipmentSlotType.HEAD, properties);
    }

    public static ArmorItem chestplate(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, EquipmentSlotType.CHEST, properties);
    }

    public static ArmorItem leggings(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, EquipmentSlotType.LEGS, properties);
    }

    public static ArmorItem boots(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, EquipmentSlotType.FEET, properties);
    }
'''
        armor_ctor = "super(material, slot, properties)"
        armor_inner_slot = "EquipmentSlotType slot"
    else:
        gear_head = '''package com.biomesunseen.item;

import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.PickaxeItem;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tier;

import com.biomesunseen.core.OreDef;
'''
        if F.get("tool_new"):
            pickaxe_ctor = "super(tier, (float) ore.toolAttackDamage - 1.0F, (float) (ore.toolSpeed / 2.5) - 2.4F, properties)"
            sword_ctor = "super(tier, (float) ore.toolAttackDamage, (float) (ore.toolSpeed / 2.5), properties)"
        else:
            pickaxe_ctor = "super(tier, (int) ore.toolAttackDamage - 1, (float) (ore.toolSpeed / 2.5) - 2.4F, properties)"
            sword_ctor = "super(tier, (int) ore.toolAttackDamage, (float) (ore.toolSpeed / 2.5), properties)"
        gear_factories = '''    public static PickaxeItem pickaxe(OreDef ore, UnseenToolTier tier, Item.Properties properties) {
        return new UnseenPickaxeItem(ore, tier, properties);
    }

    public static SwordItem sword(OreDef ore, UnseenToolTier tier, Item.Properties properties) {
        return new UnseenSwordItem(ore, tier, properties);
    }

    public static ArmorItem helmet(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, ArmorItem.Type.HELMET, properties);
    }

    public static ArmorItem chestplate(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, ArmorItem.Type.CHESTPLATE, properties);
    }

    public static ArmorItem leggings(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, ArmorItem.Type.LEGGINGS, properties);
    }

    public static ArmorItem boots(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, ArmorItem.Type.BOOTS, properties);
    }
'''
        armor_ctor = "super(material, slot, properties)"
        armor_inner_slot = "ArmorItem.Type slot"

    gear_body = gear_head + '''
/**
 * Factories for ore-derived gear.  Tools and armor inherit their stats from
 * the ore definition, keeping the whole catalog consistent.
 */
public final class UnseenGearItems {

    private UnseenGearItems() {
    }

''' + gear_factories + '''
    /** Concrete pickaxe bound to its ore. */
    public static final class UnseenPickaxeItem extends PickaxeItem {
        private final OreDef ore;

        UnseenPickaxeItem(OreDef ore, UnseenToolTier tier, Item.Properties properties) {
            ''' + pickaxe_ctor + ''';
            this.ore = ore;
        }

        public OreDef ore() {
            return ore;
        }
    }

    /** Concrete sword bound to its ore. */
    public static final class UnseenSwordItem extends SwordItem {
        private final OreDef ore;

        UnseenSwordItem(OreDef ore, UnseenToolTier tier, Item.Properties properties) {
            ''' + sword_ctor + ''';
            this.ore = ore;
        }

        public OreDef ore() {
            return ore;
        }
    }

    /** Concrete armor piece bound to its ore. */
    public static final class UnseenArmorItem extends ArmorItem {
        private final OreDef ore;

        UnseenArmorItem(OreDef ore, UnseenArmorMaterial material, ''' + armor_inner_slot + ''', Item.Properties properties) {
            ''' + armor_ctor + ''';
            this.ore = ore;
        }

        public OreDef ore() {
            return ore;
        }
    }
}
'''
    _w(root, base + "/item/UnseenGearItems.java", gear_body)

    return F
