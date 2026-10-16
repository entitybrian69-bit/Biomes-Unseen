package com.biomesunseen.worldgen.mixin;

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
        double temperature = vanilla.getTemperature(new net.minecraft.util.math.BlockPos(x << 2, 0, z << 2));
        Object replacement = UnseenBiomeSelector.select(x << 2, z << 2, temperature);
        if (replacement instanceof Biome) {
            cir.setReturnValue((Biome) replacement);
        }
    }
}
