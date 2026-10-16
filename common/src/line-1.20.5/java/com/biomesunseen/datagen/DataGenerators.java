package com.biomesunseen.datagen;

import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Data generation entrypoint.  Regenerates every data and asset file the mod
 * ships: blockstates, models, loot tables, recipes, tags, worldgen JSON,
 * biome JSON, structure JSON, spawn data, lang and advancements.
 *
 * Run with:  java -cp <classpath> com.biomesunseen.datagen.DataGenerators [outputDir]
 * or through the Gradle task:  ./gradlew :<module>:runDatagen
 */
public final class DataGenerators {

    private DataGenerators() {
    }

    public static void main(String[] args) throws Exception {
        Path output = args.length > 0 ? Paths.get(args[0]) : Paths.get("src", "generated", "resources");
        generate(output);
    }

    /** Run every provider against the given output root. */
    public static void generate(Path output) throws Exception {
        ModLangProvider.run(output);
        ModBlockStateProvider.run(output);
        ModItemModelProvider.run(output);
        ModLootProvider.run(output);
        ModRecipeProvider.run(output);
        ModTagsProvider.run(output);
        ModWorldGenProvider.run(output);
        ModAdvancementProvider.run(output);
        System.out.println("Biomes Unseen datagen complete: " + output.toAbsolutePath());
    }
}
