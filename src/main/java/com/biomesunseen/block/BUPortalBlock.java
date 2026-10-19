package com.biomesunseen.block;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.init.BUDimensions;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.portal.PortalInfo;
import net.minecraft.world.phys.Vec3;

/**
 * A dimension gate.
 *
 * Each of the three portal blocks (Hollow Deep, Aetherfall, Void) carries the
 * dimension it leads to, and stepping in teleports the entity there. The portal
 * has no collision and no item form: it exists only inside a lit frame, so it
 * cannot be collected and carried.
 *
 * The destination is resolved from {@link BUDimensions} rather than hardcoded,
 * which keeps the block, the level stem JSON and the dimension type JSON in
 * agreement by construction.
 */
public class BUPortalBlock extends Block {

    private final String destinationDimension;

    public BUPortalBlock(Properties properties, String destinationDimension) {
        super(properties);
        this.destinationDimension = destinationDimension;
    }

    /** The registry path of the dimension this gate opens onto. */
    public String destination() {
        return destinationDimension;
    }

    @Override
    @SuppressWarnings("deprecation")
    public void entityInside(BlockState state, Level level, BlockPos pos, Entity entity) {
        if (level.isClientSide() || entity.isPassenger() || entity.isVehicle()) {
            return;
        }
        // Riders and passengers would be detached by the teleport; the vanilla
        // portal has the same guard.
        if (entity.isInsidePortalCooldown() || entity.portalCooldown > 0) {
            return;
        }
        if (!(level instanceof ServerLevel serverLevel)) {
            return;
        }
        MinecraftServer server = serverLevel.getServer();
        if (server == null) {
            return;
        }
        ResourceKey<Level> targetKey = BUDimensions.levelKey(destinationDimension);
        ServerLevel target = server.getLevel(targetKey);
        if (target == null) {
            BiomesUnseen.LOGGER.warn("Portal at {} targets unregistered dimension {}",
                    pos, destinationDimension);
            return;
        }
        if (target == serverLevel) {
            // Already standing in the destination dimension: bounce home.
            target = server.overworld();
        }
        Vec3 safe = BUDimensions.findSafeLanding(target, entity);
        PortalInfo info = new PortalInfo(safe, Vec3.ZERO, entity.getYRot(), entity.getXRot());
        entity.changeDimension(target, new net.minecraftforge.common.util.ITeleporter() {
            @Override
            public PortalInfo getPortalInfo(Entity entityToMove, ServerLevel dest,
                                            java.util.function.Function<Entity, PortalInfo> defaultGetter) {
                return info;
            }

            @Override
            public boolean playTeleportSound(Entity entity, ServerLevel source, ServerLevel dest) {
                return false;
            }

            @Override
            public BlockState getPortalBlockState(ServerLevel level, BlockPos pos) {
                return state;
            }
        });
        entity.portalCooldown = 200;
    }
}
