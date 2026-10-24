package com.biomesunseen.datagen;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.registry.ModBlocks;
import com.biomesunseen.spec.OreSpec;
import com.biomesunseen.spec.Specs;
import net.minecraft.core.HolderLookup;
import net.minecraft.data.PackOutput;
import net.minecraft.data.tags.BlockTagsProvider;
import net.minecraft.tags.BlockTags;
import net.minecraftforge.common.Tags;
import net.minecraftforge.common.data.ExistingFileHelper;
import org.jetbrains.annotations.Nullable;

import java.util.concurrent.CompletableFuture;

public class ModBlockTagsProvider extends BlockTagsProvider {
    public ModBlockTagsProvider(PackOutput output, CompletableFuture<HolderLookup.Provider> lookup,
                                @Nullable ExistingFileHelper helper) {
        super(output, lookup, BiomesUnseen.MOD_ID, helper);
    }

    @Override
    protected void addTags(HolderLookup.Provider provider) {
        tag(BlockTags.MINEABLE_WITH_PICKAXE).add(ModBlocks.HOLLOWITE_ORE.get());
        tag(BlockTags.NEEDS_IRON_TOOL).add(ModBlocks.HOLLOWITE_ORE.get());
        tag(Tags.Blocks.ORES).add(ModBlocks.HOLLOWITE_ORE.get());
        for (OreSpec spec : Specs.ores()) {
            var block = ModBlocks.ORES.get(spec.id()).get();
            tag(BlockTags.MINEABLE_WITH_PICKAXE).add(block);
            tag(Tags.Blocks.ORES).add(block);
            switch (spec.tier()) {
                case 0 -> tag(BlockTags.NEEDS_STONE_TOOL).add(block);
                case 1 -> tag(BlockTags.NEEDS_IRON_TOOL).add(block);
                default -> tag(BlockTags.NEEDS_DIAMOND_TOOL).add(block);
            }
        }
    }
}
