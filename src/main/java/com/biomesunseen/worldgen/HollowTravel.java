package com.biomesunseen.worldgen;

import com.biomesunseen.registry.ModBlocks;
import com.biomesunseen.registry.ModSounds;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundSource;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.chunk.ChunkStatus;
import net.minecraft.world.level.levelgen.Heightmap;

/** Shared safe, two-way player transfer used by both the gate block and Hollow Sigil. */
public final class HollowTravel {
    private static final BlockPos HOLLOW_ARRIVAL = new BlockPos(0, 100, 0);
    private static final BlockPos HOLLOW_RETURN_PORTAL = HOLLOW_ARRIVAL.offset(0, 0, 2);
    private static final String OVERWORLD_PORTAL_KEY = "BiomesUnseenOverworldPortal";

    private HollowTravel() {
    }

    public static boolean travel(ServerPlayer player) {
        return travel(player, null);
    }

    public static boolean travel(ServerPlayer player, BlockPos sourcePortal) {
        if (player.isOnPortalCooldown()) {
            player.displayClientMessage(
                    Component.translatable("message.biomesunseen.hollow_travel.cooldown"), true);
            return false;
        }

        ResourceKey<Level> current = player.level().dimension();
        ResourceKey<Level> destinationKey;
        if (current.equals(Level.OVERWORLD)) {
            destinationKey = ModDimensions.HOLLOW_DEEP_LEVEL;
            if (sourcePortal == null) {
                player.getPersistentData().remove(OVERWORLD_PORTAL_KEY);
            } else {
                player.getPersistentData().putIntArray(OVERWORLD_PORTAL_KEY,
                        new int[]{sourcePortal.getX(), sourcePortal.getY(), sourcePortal.getZ()});
            }
        } else if (current.equals(ModDimensions.HOLLOW_DEEP_LEVEL)) {
            destinationKey = Level.OVERWORLD;
        } else {
            player.displayClientMessage(
                    Component.translatable("message.biomesunseen.hollow_travel.wrong_dimension"), true);
            return false;
        }

        ServerLevel destination = player.getServer().getLevel(destinationKey);
        if (destination == null) {
            player.displayClientMessage(
                    Component.translatable("item.biomesunseen.hollow_sigil.dimension_missing"), true);
            return false;
        }

        player.level().playSound(null, player.blockPosition(), ModSounds.HOLLOW_GATE_TRAVEL.get(),
                SoundSource.BLOCKS, 0.9F, 0.95F + player.getRandom().nextFloat() * 0.1F);
        if (destinationKey.equals(ModDimensions.HOLLOW_DEEP_LEVEL)) {
            prepareHollowLanding(destination);
            player.teleportTo(destination, HOLLOW_ARRIVAL.getX() + 0.5, HOLLOW_ARRIVAL.getY(),
                    HOLLOW_ARRIVAL.getZ() + 0.5, player.getYRot(), player.getXRot());
        } else {
            BlockPos returnPos = storedPortalExit(player, destination);
            if (returnPos == null) {
                BlockPos spawn = destination.getSharedSpawnPos();
                int y = destination.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                        spawn.getX(), spawn.getZ());
                returnPos = new BlockPos(spawn.getX(), y, spawn.getZ());
            }
            player.teleportTo(destination, returnPos.getX() + 0.5, returnPos.getY(), returnPos.getZ() + 0.5,
                    player.getYRot(), player.getXRot());
            player.getPersistentData().remove(OVERWORLD_PORTAL_KEY);
        }
        player.setPortalCooldown();
        destination.playSound(null, player.blockPosition(), ModSounds.HOLLOW_GATE_TRAVEL.get(),
                SoundSource.BLOCKS, 0.9F, 0.95F + player.getRandom().nextFloat() * 0.1F);
        return true;
    }

    private static BlockPos storedPortalExit(ServerPlayer player, ServerLevel overworld) {
        int[] coordinates = player.getPersistentData().getIntArray(OVERWORLD_PORTAL_KEY);
        if (coordinates.length != 3) {
            return null;
        }
        BlockPos portal = new BlockPos(coordinates[0], coordinates[1], coordinates[2]);
        if (!overworld.getBlockState(portal).is(ModBlocks.HOLLOW_PORTAL.get())) {
            return null;
        }
        int[][] directions = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
        for (int[] direction : directions) {
            BlockPos feet = portal.offset(direction[0], 0, direction[1]);
            if (overworld.getBlockState(feet.below()).blocksMotion()
                    && !overworld.getBlockState(feet).blocksMotion()
                    && !overworld.getBlockState(feet.above()).blocksMotion()) {
                return feet;
            }
        }
        return null;
    }

    private static void prepareHollowLanding(ServerLevel destination) {
        int chunkX = HOLLOW_ARRIVAL.getX() >> 4;
        int chunkZ = HOLLOW_ARRIVAL.getZ() >> 4;
        destination.getChunkSource().getChunk(chunkX, chunkZ, ChunkStatus.FULL, true);
        for (int dx = -2; dx <= 2; dx++) {
            for (int dz = -2; dz <= 2; dz++) {
                destination.setBlockAndUpdate(HOLLOW_ARRIVAL.offset(dx, -1, dz),
                        Blocks.MOSSY_STONE_BRICKS.defaultBlockState());
            }
        }
        for (int dy = 0; dy <= 2; dy++) {
            destination.setBlockAndUpdate(HOLLOW_ARRIVAL.above(dy), Blocks.AIR.defaultBlockState());
            destination.setBlockAndUpdate(HOLLOW_RETURN_PORTAL.above(dy), Blocks.AIR.defaultBlockState());
        }
        destination.setBlockAndUpdate(HOLLOW_RETURN_PORTAL, ModBlocks.HOLLOW_PORTAL.get().defaultBlockState());
    }
}
