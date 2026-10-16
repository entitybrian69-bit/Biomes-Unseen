package com.biomesunseen.block;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.AbstractBlock;
import net.minecraft.world.level.block.SoundType;

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

    private static AbstractBlock.Properties buildProperties() {
        AbstractBlock.Properties properties = AbstractBlock.Properties.of(net.minecraft.world.level.material.Material.PLANT);
        return properties.noCollission().instabreak().offsetType(AbstractBlock.OffsetType.XZ)
                .sound(SoundType.GRASS);
    }

    public PlantDef plant() {
        return plant;
    }
}
