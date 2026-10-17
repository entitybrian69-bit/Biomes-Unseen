package com.biomesunseen.worldgen;

import java.util.Collections;

import net.minecraft.core.BlockPos;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;

import com.biomesunseen.registry.ModBlocks;

/**
 * Travel between the overworld and the three Biomes Unseen dimensions.
 *
 * <p>The destination is found by walking {@link MinecraftServer#getAllLevels()}
 * and comparing {@code Level#dimension().location()}, which needs no
 * registry-key helpers (their package moved three times between 1.16.5 and
 * 26.x) and no server mappings beyond what every target exposes.</p>
 *
 * <p>A 3x3 landing pad of the dimension's own stone is laid down on arrival so
 * the player never lands inside terrain or over the void, and arriving back in
 * the overworld reuses the world spawn.</p>
 */
public final class UnseenTravel {

    public static final String MOD_ID = "biomesunseen";

    /** Where each player stepped into a dimension, so the way back is exact. */
    private static final java.util.Map<java.util.UUID, double[]> RETURN =
            new java.util.HashMap<java.util.UUID, double[]>();

    private UnseenTravel() {
    }

    public static boolean travel(Level level, Player player, String dimensionId) {
        MinecraftServer server = level.getServer();
        if (server == null) {
            return false;
        }
        String key = MOD_ID + ":" + dimensionId;
        if (level.dimension().location().toString().equals(key)) {
            ServerLevel overworld = find(server, "minecraft:overworld");
            if (overworld == null) {
                return false;
            }
            double[] home = RETURN.get(player.getUUID());
            double hx = home == null ? 0.0D : home[0];
            double hy = home == null ? 100.0D : home[1];
            double hz = home == null ? 0.0D : home[2];
            buildArrival(overworld, (int) Math.floor(hx), (int) Math.floor(hy),
                    (int) Math.floor(hz), Blocks.STONE.defaultBlockState());
            return send(player, overworld, hx, hy, hz);
        }
        RETURN.put(player.getUUID(), new double[]{player.getX(), player.getY(), player.getZ()});
        ServerLevel target = find(server, key);
        if (target == null) {
            return false;
        }
        int x = (int) Math.floor(player.getX());
        int z = (int) Math.floor(player.getZ());
        int y = arrivalY(dimensionId);
        buildArrival(target, x, y, z, floorFor(dimensionId));
        return send(player, target, x + 0.5D, y, z + 0.5D);
    }

    private static ServerLevel find(MinecraftServer server, String key) {
        for (ServerLevel candidate : server.getAllLevels()) {
            if (candidate.dimension().location().toString().equals(key)) {
                return candidate;
            }
        }
        return null;
    }

    private static int arrivalY(String dimensionId) {
        if ("aetherfall".equals(dimensionId)) {
            return 128;
        }
        if ("void_between".equals(dimensionId)) {
            return 96;
        }
        return 48;
    }

    private static void buildArrival(ServerLevel level, int x, int y, int z, BlockState floor) {
        for (int dx = -1; dx <= 1; dx++) {
            for (int dz = -1; dz <= 1; dz++) {
                level.setBlock(new BlockPos(x + dx, y - 1, z + dz), floor, 3, 512);
                level.setBlock(new BlockPos(x + dx, y, z + dz),
                        Blocks.AIR.defaultBlockState(), 3, 512);
                level.setBlock(new BlockPos(x + dx, y + 1, z + dz),
                        Blocks.AIR.defaultBlockState(), 3, 512);
            }
        }
    }

    private static BlockState floorFor(String dimensionId) {
        Block block;
        if ("aetherfall".equals(dimensionId)) {
            block = ModBlocks.DECOR.get("skyglass").get();
        } else if ("void_between".equals(dimensionId)) {
            block = ModBlocks.DECOR.get("voidstone").get();
        } else {
            block = ModBlocks.DECOR.get("hollowstone").get();
        }
        if (block == null) {
            return Blocks.STONE.defaultBlockState();
        }
        return block.defaultBlockState();
    }

    private static boolean send(Player player, ServerLevel target, double x, double y, double z) {
        player.changeDimension(target);
        player.setPos(x, y, z);
        return true;
    }
}
