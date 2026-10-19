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

    /** Persistent-data key holding the game time of the last transit. */
    private static final String COOLDOWN_KEY = "BiomesUnseenPortalCooldown";
    /** Ticks before the same entity may use a gate again. */
    private static final int COOLDOWN_TICKS = 100;

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
        // portal guards the same way.
        if (!(level instanceof ServerLevel serverLevel)) {
            return;
        }
        if (isOnCooldown(entity, level)) {
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
        ServerLevel destination = target;
        markCooldown(entity, level);

        entity.changeDimension(destination, new net.minecraftforge.common.util.ITeleporter() {
            /**
             * Place the entity in the destination dimension.
             *
             * This is the only abstract method Forge's ITeleporter declares, and
             * it is where a custom destination is honoured: {@code repositionEntity}
             * performs the cross-dimension move and hands back the (possibly new)
             * entity instance, which is then positioned at the safe landing spot
             * resolved above rather than at a matching portal coordinate.
             */
            @Override
            public Entity placeEntity(Entity moving, ServerLevel currentWorld,
                                     ServerLevel destWorld, float yaw,
                                     java.util.function.Function<Boolean, Entity> repositionEntity) {
                Entity placed = repositionEntity.apply(false);
                placed.teleportTo(safe.x, safe.y, safe.z);
                placed.setDeltaMovement(Vec3.ZERO);
                placed.hurtMarked = true;
                return placed;
            }

            /** Returning false suppresses the vanilla portal whoosh. */
            @Override
            public boolean playTeleportSound(net.minecraft.server.level.ServerPlayer player,
                                            ServerLevel sourceWorld, ServerLevel destWorld) {
                return false;
            }

            /**
             * A custom dimension gate, not a nether portal.
             *
             * Returning false stops Forge from trying to build or link a
             * {@code BlockPattern} portal frame, which this block does not have.
             */
            @Override
            public boolean isVanilla() {
                return false;
            }
        });
    }

    /**
     * Whether the entity has teleported too recently to go again.
     *
     * {@code entityInside} fires every tick the entity stands in the block, so
     * without a guard a single step through would teleport repeatedly. The
     * cooldown lives in the entity's Forge persistent data rather than in
     * {@code Entity.portalCooldown}, which is private and governs vanilla
     * nether portals -- sharing it would let a nether trip suppress this gate.
     */
    private boolean isOnCooldown(Entity entity, Level level) {
        long last = entity.getPersistentData().getLong(COOLDOWN_KEY);
        return last != 0L && level.getGameTime() - last < COOLDOWN_TICKS;
    }

    private void markCooldown(Entity entity, Level level) {
        entity.getPersistentData().putLong(COOLDOWN_KEY, level.getGameTime());
    }
}
