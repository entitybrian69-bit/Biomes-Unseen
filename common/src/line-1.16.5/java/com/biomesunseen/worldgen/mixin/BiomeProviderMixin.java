package com.biomesunseen.worldgen.mixin;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.BiomeProvider;

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
