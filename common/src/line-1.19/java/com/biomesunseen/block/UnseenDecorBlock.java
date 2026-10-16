package com.biomesunseen.block;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;

import com.biomesunseen.core.DecorDef;

/**
 * Decorative palette block used by biome terrain and structures.
 */
public class UnseenDecorBlock extends Block {

    private final DecorDef decor;

    public UnseenDecorBlock(DecorDef decor) {
        super(buildProperties(decor));
        this.decor = decor;
    }

    private static BlockBehaviour.Properties buildProperties(DecorDef decor) {
        BlockBehaviour.Properties properties = BlockBehaviour.Properties.of(net.minecraft.world.level.material.Material.STONE).strength(1.5F, 6.0F);
        properties = properties.strength("stone".equals(decor.material) ? 1.5F : 1.0F, 6.0F);
        if (decor.isTransparent()) {
            properties = properties.noOcclusion().isViewBlocking((state, getter, pos) -> false);
        }
        if (decor.lightLevel() > 0) {
            properties = properties.lightLevel(state -> decor.lightLevel());
        }
        return properties;
    }

    public DecorDef decor() {
        return decor;
    }
}
