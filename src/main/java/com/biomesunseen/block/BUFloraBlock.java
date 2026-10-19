package com.biomesunseen.block;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.BushBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * A plant rendered as a single cutout cross.
 *
 * Extends {@link BushBlock} rather than {@code FlowerBlock} on purpose: the
 * flower base class requires a suspicious-stew {@code MobEffect}, which would
 * force 27 flora species to each claim a vanilla effect they do not have.
 * BushBlock gives the same survivability rules (needs a valid ground block,
 * breaks instantly, no collision) without that coupling.
 */
public class BUFloraBlock extends BushBlock {

    /** Plants occupy most but not all of their cell, matching the cross model. */
    protected static final VoxelShape SHAPE = box(2.0D, 0.0D, 2.0D, 14.0D, 13.0D, 14.0D);

    public BUFloraBlock(Properties properties) {
        super(properties);
    }

    @Override
    @SuppressWarnings("deprecation")
    public VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos,
                               CollisionContext context) {
        return SHAPE;
    }
}
