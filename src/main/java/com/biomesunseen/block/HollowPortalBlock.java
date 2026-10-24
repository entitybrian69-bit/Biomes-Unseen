package com.biomesunseen.block;

import com.biomesunseen.worldgen.HollowTravel;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;

/** A craftable, walk-through gate linking the Overworld and Hollow Deep. */
public class HollowPortalBlock extends Block {
    public HollowPortalBlock(Properties properties) {
        super(properties);
    }

    @Override
    public void entityInside(BlockState state, Level level, BlockPos pos, Entity entity) {
        if (level.isClientSide || !(entity instanceof ServerPlayer player)
                || player.isOnPortalCooldown() || player.isPassenger() || player.isVehicle()) {
            return;
        }
        HollowTravel.travel(player, pos);
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        for (int i = 0; i < 3; i++) {
            double x = pos.getX() + 0.15D + random.nextDouble() * 0.7D;
            double y = pos.getY() + 0.15D + random.nextDouble() * 0.7D;
            double z = pos.getZ() + 0.15D + random.nextDouble() * 0.7D;
            level.addParticle(ParticleTypes.PORTAL, x, y, z,
                    (random.nextDouble() - 0.5D) * 0.12D,
                    (random.nextDouble() - 0.5D) * 0.12D,
                    (random.nextDouble() - 0.5D) * 0.12D);
        }
    }
}
