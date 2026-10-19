package com.biomesunseen.mixin;

import com.biomesunseen.world.OverworldBiomeInjector;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.biome.MultiNoiseBiomeSourceParameterList;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;

/**
 * Splices the twelve seeded Overworld biomes into the vanilla noise list.
 *
 * <p>1.20.1 places Overworld biomes by sampling
 * {@link MultiNoiseBiomeSourceParameterList.Preset#OVERWORLD}, whose point list
 * is built inside the preset enum and is not exposed for extension. Forge's
 * {@code BiomeModifier} system can add spawns and features to a biome that
 * already generates, but it cannot add a new noise point -- so a registered
 * Overworld biome with complete worldgen JSON still never appears in a world.
 *
 * <p>This mixin is therefore the load-bearing piece of Overworld integration:
 * without it, the twelve highest-weight biomes exist in the registry and in the
 * creative tab but not on the map. It is deliberately narrow -- it touches only
 * the OVERWORLD preset, and only appends, so vanilla terrain is unchanged.
 */
@Mixin(MultiNoiseBiomeSourceParameterList.Preset.class)
public abstract class MultiNoiseBiomeSourceParameterListPresetMixin {

    /**
     * Append our parameter points to the freshly built Overworld list.
     *
     * Runs at RETURN of {@code apply}, which is called when a level stem is
     * resolved -- late enough that the biome registry is populated and a
     * {@link net.minecraft.core.Holder} can be obtained for each seeded biome,
     * which is why {@link OverworldBiomeInjector#inject} runs first on
     * ServerAboutToStart.
     */
    @Inject(method = "apply", at = @At("RETURN"), cancellable = true)
    private void biomesUnseen$appendSeededOverworldBiomes(
            Function<ResourceKey<MultiNoiseBiomeSourceParameterList>,
                    MultiNoiseBiomeSourceParameterList> keyMapper,
            CallbackInfoReturnable<MultiNoiseBiomeSourceParameterList> callback) {

        // Only the Overworld is extended. The Nether and End presets route
        // through the same method, and their biome placement must stay vanilla.
        Object self = this;
        if (self != MultiNoiseBiomeSourceParameterList.Preset.OVERWORLD) {
            return;
        }

        MultiNoiseBiomeSourceParameterList vanilla = callback.getReturnValue();
        if (vanilla == null) {
            return;
        }
        List<MultiNoiseBiomeSourceParameterList.ParameterPoint> extra =
                OverworldBiomeInjector.seedPoints();
        if (extra.isEmpty()) {
            return;
        }

        List<MultiNoiseBiomeSourceParameterList.ParameterPoint> combined =
                new ArrayList<>(vanilla.values());
        combined.addAll(extra);
        callback.setReturnValue(new MultiNoiseBiomeSourceParameterList(
                vanilla.key(), combined));
    }
}
