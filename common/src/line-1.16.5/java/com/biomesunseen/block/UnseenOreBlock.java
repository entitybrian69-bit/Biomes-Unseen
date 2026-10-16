package com.biomesunseen.block;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.AbstractBlock;

import com.biomesunseen.core.OreDef;

/**
 * A custom ore block.  Carries its OreDef for loot/particle/mining behaviour
 * and glows when the ore definition calls for it.
 */
public class UnseenOreBlock extends Block {

    private final OreDef ore;

    public UnseenOreBlock(OreDef ore) {
        super(buildProperties(ore));
        this.ore = ore;
    }

    private static AbstractBlock.Properties buildProperties(OreDef ore) {
        AbstractBlock.Properties properties = AbstractBlock.Properties.of(net.minecraft.world.level.material.Material.STONE).strength(3.0F, 3.0F);
        if (ore.glows) {
            properties = properties.lightLevel(state -> 8);
        }
        return properties.randomTicks();
    }

    public OreDef ore() {
        return ore;
    }

    /** Mining particle colour used by the platform particle hook. */
    public int particleColor() {
        return ore.particleColor;
    }

    /** Mining sound event id (always the shared ore chime set). */
    public String miningSoundId() {
        return "block.biomesunseen.ore_chime";
    }
}
