package com.biomesunseen.worldgen;

import com.biomesunseen.BiomesUnseen;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.biome.Biome;

public final class ModBiomes {
    public static final ResourceKey<Biome> HEARTWOOD_HOLLOW = key("heartwood_hollow");
    public static final ResourceKey<Biome> GLOWCAP_GROTTO = key("glowcap_grotto");
    public static final ResourceKey<Biome> CRYSTAL_HOLLOWS = key("crystal_hollows");
    public static final ResourceKey<Biome> ASHEN_DEPTHS = key("ashen_depths");
    public static final ResourceKey<Biome> MIRE_OF_WHISPERS = key("mire_of_whispers");

    private ModBiomes() {
    }

    private static ResourceKey<Biome> key(String name) {
        return ResourceKey.create(Registries.BIOME, new ResourceLocation(BiomesUnseen.MOD_ID, name));
    }
}
