package com.biomesunseen.config;

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
            call(builder, "setTitle", new net.minecraft.network.chat.TextComponent(title));
            call(builder, "setSavingRunnable",
                    (Runnable) () -> BiomesUnseen.setConfig(BiomesUnseen.config()));
            if (parent != null) {
                call(builder, "setParentScreen", parent);
            }
            Object entryBuilder = call(builder, "entryBuilder");
            ModConfig cfg = BiomesUnseen.config();

            Object general = call(builder, "getOrCreateCategory", new net.minecraft.network.chat.TextComponent("General"));
            addBool(general, entryBuilder, translator.apply("enableAllBiomes"), cfg.enableAllBiomes, true, v -> cfg.enableAllBiomes = v);
            addBool(general, entryBuilder, translator.apply("enableAllOres"), cfg.enableAllOres, true, v -> cfg.enableAllOres = v);
            addBool(general, entryBuilder, translator.apply("enableAllStructures"), cfg.enableAllStructures, true, v -> cfg.enableAllStructures = v);
            addBool(general, entryBuilder, translator.apply("enableAllMobs"), cfg.enableAllMobs, true, v -> cfg.enableAllMobs = v);
            addBool(general, entryBuilder, translator.apply("enableBosses"), cfg.enableBosses, true, v -> cfg.enableBosses = v);
            addBool(general, entryBuilder, translator.apply("enableLoreBooks"), cfg.enableLoreBooks, true, v -> cfg.enableLoreBooks = v);
            addBool(general, entryBuilder, translator.apply("enableStructureLoot"), cfg.enableStructureLoot, true, v -> cfg.enableStructureLoot = v);

            Object world = call(builder, "getOrCreateCategory", new net.minecraft.network.chat.TextComponent("Level"));
            addDouble(world, entryBuilder, translator.apply("biomeRarityMultiplier"), cfg.biomeRarityMultiplier, 1.0D, 0.0D, 10.0D, v -> cfg.biomeRarityMultiplier = v);
            addDouble(world, entryBuilder, translator.apply("biomeTerraformingStrength"), cfg.biomeTerraformingStrength, 1.0D, 0.0D, 3.0D, v -> cfg.biomeTerraformingStrength = v);
            addDouble(world, entryBuilder, translator.apply("oreRateMultiplier"), cfg.oreRateMultiplier, 1.0D, 0.0D, 10.0D, v -> cfg.oreRateMultiplier = v);
            addDouble(world, entryBuilder, translator.apply("structureSpacingMultiplier"), cfg.structureSpacingMultiplier, 1.0D, 0.1D, 10.0D, v -> cfg.structureSpacingMultiplier = v);
            addDouble(world, entryBuilder, translator.apply("weatherIntensity"), cfg.weatherIntensity, 1.0D, 0.0D, 3.0D, v -> cfg.weatherIntensity = v);
            addInt(world, entryBuilder, translator.apply("structureLodDistance"), cfg.structureLodDistance, 128, 16, 1024, v -> cfg.structureLodDistance = v);

            Object mobs = call(builder, "getOrCreateCategory", new net.minecraft.network.chat.TextComponent("Mobs & Performance"));
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
        Object entry = call(entryBuilder, "startBooleanField", new net.minecraft.network.chat.TextComponent(label), Boolean.valueOf(value));
        entry = call(entry, "setDefaultValue", Boolean.valueOf(defaultValue));
        entry = call(entry, "setSaveConsumer", save);
        call(category, "addEntry", call(entry, "build"));
    }

    /** Add one double entry with slider bounds to a category. */
    private static void addDouble(Object category, Object entryBuilder, String label,
                                  double value, double defaultValue, double min, double max,
                                  Consumer<Double> save)
            throws ReflectiveOperationException {
        Object entry = call(entryBuilder, "startDoubleField", new net.minecraft.network.chat.TextComponent(label), Double.valueOf(value));
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
        Object entry = call(entryBuilder, "startIntField", new net.minecraft.network.chat.TextComponent(label), Integer.valueOf(value));
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
