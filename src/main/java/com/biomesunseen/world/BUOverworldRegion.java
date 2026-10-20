package com.biomesunseen.world;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.init.BUBiomes;
import com.biomesunseen.init.BUContent;
import com.mojang.datafixers.util.Pair;
import net.minecraft.core.Registry;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.Climate;
import terrablender.api.ParameterUtils;
import terrablender.api.Region;
import terrablender.api.RegionType;
import terrablender.api.VanillaParameterOverlayBuilder;

import java.util.List;
import java.util.function.Consumer;

/**
 * The TerraBlender region that places all 80 Overworld biomes.
 *
 * <p>1.20.1 decides which Overworld biome occupies a column by sampling a fixed
 * list of climate parameter points held in
 * {@code MultiNoiseBiomeSourceParameterList.Preset.OVERWORLD}. That list is
 * built inside the preset enum and no datapack can append to it, so a biome can
 * be registered, fully authored and still never appear in a world. TerraBlender
 * is the supported way in: it owns the blend, and because Biomes O' Plenty and
 * Oh The Biomes You've Gone use the same hook, adding biomes here coexists with
 * every other biome mod in a pack instead of fighting it for climate space.
 *
 * <p>Points are contributed through {@link VanillaParameterOverlayBuilder}
 * rather than by writing a parameter list outright. The overlay merges our
 * points against vanilla's, which is what keeps vanilla biomes generating
 * unchanged -- replacing the list would have silently rewritten the Overworld.
 *
 * <p>Every climate coordinate comes from the authored biome table via
 * {@code BUContent.SEEDED_OVERWORLD_PARAMETERS}, so a designer moving a biome
 * around the Overworld edits tools/content/biomes.py and not this class.
 */
public class BUOverworldRegion extends Region {

    /**
     * How much of the Overworld this region claims, relative to other regions.
     *
     * TerraBlender weights regions against one another and against vanilla. Four
     * is enough for 80 biomes to be genuinely findable across a world without
     * crowding out vanilla or every other mod's region -- at this weight a long
     * journey crosses several of our biomes, but the Overworld still reads as
     * Minecraft first.
     */
    public static final int WEIGHT = 4;

    /**
     * Half-width of each authored climate coordinate at a weight of 100.
     *
     * An exact value would confine a biome to a single hyperplane of noise space,
     * which appears as one thin stripe across the world rather than a place.
     * Widening each coordinate into a band gives the biome a real footprint while
     * keeping it inside the climate its author intended, and the bands are narrow
     * enough that neighbouring biomes stay distinct instead of smearing together.
     */
    private static final float BASE_SPREAD = 0.075F;

    /**
     * How far a biome's authored weight may widen or narrow its band.
     *
     * Weight is authored per biome across 60..130 and is the only lever on how
     * common a biome is: in a multi-noise source a biome's frequency is the
     * volume of climate space its parameter point occupies, so scaling the band
     * by weight is what makes a rare biome rare. Capping the scale keeps the
     * heaviest biome from smearing across its neighbours' climate.
     */
    private static final float WEIGHT_SCALE = 0.35F;

    public BUOverworldRegion() {
        super(new ResourceLocation(BiomesUnseen.MODID, "overworld"),
                RegionType.OVERWORLD, WEIGHT);
    }

    /**
     * Contribute one parameter point per authored Overworld biome.
     *
     * Called by TerraBlender while it assembles the Overworld's blended parameter
     * list, with the live biome registry so each key can be confirmed to exist
     * before it is contributed.
     */
    @Override
    public void addBiomes(Registry<Biome> registry,
                          Consumer<Pair<Climate.ParameterPoint, ResourceKey<Biome>>> mapper) {
        VanillaParameterOverlayBuilder builder = new VanillaParameterOverlayBuilder();
        int bound = 0;

        for (Object[] row : BUContent.SEEDED_OVERWORLD_PARAMETERS) {
            String id = (String) row[0];
            ResourceKey<Biome> key = BUBiomes.get(id);
            if (key == null) {
                BiomesUnseen.LOGGER.warn("Overworld biome {} has no resource key", id);
                continue;
            }
            // A biome the datapack does not define cannot be placed. Skipping it
            // keeps the world loadable and logs the gap, rather than contributing
            // a key that resolves to nothing and leaves a hole in the Overworld.
            if (registry.getHolder(key).isEmpty()) {
                BiomesUnseen.LOGGER.error(
                        "Overworld biome {} is not defined by the datapack; skipping", id);
                continue;
            }
            for (Climate.ParameterPoint point : parameterPoints(row)) {
                builder.add(point, key);
            }
            bound++;
        }

        builder.build().forEach(mapper);
        BiomesUnseen.LOGGER.info(
                "Biomes Unseen: blended {} Overworld biomes into the TerraBlender region", bound);
    }

    /**
     * Build the parameter point for one authored biome row.
     *
     * The row is {id, temperature, humidity, continentalness, erosion, depth,
     * weirdness, offset, weight}. TerraBlender's builder takes the cartesian
     * product of the values supplied per axis, so passing exactly one band per
     * axis yields exactly one point.
     */
    private static List<Climate.ParameterPoint> parameterPoints(Object[] row) {
        float temperature = (Float) row[1];
        float humidity = (Float) row[2];
        float continentalness = (Float) row[3];
        float erosion = (Float) row[4];
        float depth = (Float) row[5];
        float weirdness = (Float) row[6];
        float offset = (Float) row[7];

        int weight = row.length > 8 ? (Integer) row[8] : 100;
        float spread = spreadFor(weight);

        return new ParameterUtils.ParameterPointListBuilder()
                .temperature(band(temperature, spread))
                .humidity(band(humidity, spread))
                .continentalness(band(continentalness, spread))
                .erosion(band(erosion, spread))
                .depth(band(depth, spread))
                .weirdness(band(weirdness, spread))
                .offset(offset)
                .build();
    }

    /**
     * The band half-width for one biome's authored weight.
     *
     * Weight 100 gets the base spread; the authored 60..130 range maps to roughly
     * 0.86x..1.11x of it, so a common biome occupies noticeably more climate
     * space than a rare one without either dominating or vanishing.
     */
    private static float spreadFor(int weight) {
        return BASE_SPREAD * (1.0F + WEIGHT_SCALE * (weight - 100) / 100.0F);
    }

    /**
     * Widen one authored coordinate into a band, clamped to noise space.
     *
     * Clamping matters: an authored value near the edge of the range would
     * otherwise produce a band reaching outside [-1, 1], which the multi-noise
     * sampler never visits and which would quietly shrink the biome.
     */
    private static Climate.Parameter band(float value, float spread) {
        float low = Math.max(-1.0F, value - spread);
        float high = Math.min(1.0F, value + spread);
        return Climate.Parameter.span(low, high);
    }
}
