package com.biomesunseen.block;

import net.minecraft.block.Block;
import net.minecraft.block.AbstractBlock;
import net.minecraft.block.SoundType;

import com.biomesunseen.core.PlantDef;

/**
 * Decorative plant block: cross-shaped, fragile, optionally pottable.
 * Non-solid so the world stays walkable and alive.
 */
public class UnseenPlantBlock extends Block {

    private final PlantDef plant;

    public UnseenPlantBlock(PlantDef plant) {
        super(buildProperties());
        this.plant = plant;
    }

    private static BlockBehaviour.Properties buildProperties() {
        BlockBehaviour.Properties properties = AbstractBlock.Properties.of(net.minecraft.block.material.Material.PLANT);
        return properties.noCollission().instabreak().offsetType(BlockBehaviour.OffsetType.XZ)
                .sound(SoundType.GRASS);
    }

    public PlantDef plant() {
        return plant;
    }
}
