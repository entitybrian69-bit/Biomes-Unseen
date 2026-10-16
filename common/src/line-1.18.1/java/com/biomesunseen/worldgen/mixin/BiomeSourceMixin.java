package com.biomesunseen.worldgen.mixin;

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
