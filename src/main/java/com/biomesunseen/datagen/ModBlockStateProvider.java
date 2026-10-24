package com.biomesunseen.datagen;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.registry.ModBlocks;
import com.biomesunseen.spec.OreSpec;
import com.biomesunseen.spec.Specs;
import net.minecraft.data.PackOutput;
import net.minecraftforge.client.model.generators.BlockStateProvider;
import net.minecraftforge.common.data.ExistingFileHelper;

public class ModBlockStateProvider extends BlockStateProvider {
    public ModBlockStateProvider(PackOutput output, ExistingFileHelper helper) {
        super(output, BiomesUnseen.MOD_ID, helper);
    }

    @Override
    protected void registerStatesAndModels() {
        // The portal is a non-colliding cross model, rendered with cutout transparency in ClientEvents.
        simpleBlockWithItem(ModBlocks.HOLLOW_PORTAL.get(),
                models().cross("hollow_portal", modLoc("block/hollow_portal")));
        // Requires textures/block/hollowite_ore.png (tools/gen_textures.py) to exist.
        simpleBlockWithItem(ModBlocks.HOLLOWITE_ORE.get(),
                models().cubeAll("hollowite_ore", modLoc("block/hollowite_ore")));
        for (OreSpec spec : Specs.ores()) {
            simpleBlockWithItem(ModBlocks.ORES.get(spec.id()).get(),
                    models().cubeAll(spec.blockId(), modLoc("block/" + spec.blockId())));
        }
    }
}
