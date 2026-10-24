package com.biomesunseen.item;

import com.biomesunseen.worldgen.ModDimensions;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.chunk.ChunkStatus;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.resources.ResourceKey;

/** Reusable, two-way travel between the Overworld and the Hollow Deep. */
public class HollowSigilItem extends Item {
    private static final BlockPos ARRIVAL = new BlockPos(0, 100, 0);

    public HollowSigilItem(Properties properties) {
        super(properties.stacksTo(1));
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!(player instanceof ServerPlayer serverPlayer)) {
            return InteractionResultHolder.sidedSuccess(stack, level.isClientSide);
        }

        ResourceKey<Level> current = serverPlayer.level().dimension();
        ResourceKey<Level> destinationKey;
        if (current.equals(Level.OVERWORLD)) {
            destinationKey = ModDimensions.HOLLOW_DEEP_LEVEL;
        } else if (current.equals(ModDimensions.HOLLOW_DEEP_LEVEL)) {
            destinationKey = Level.OVERWORLD;
        } else {
            serverPlayer.displayClientMessage(Component.translatable("item.biomesunseen.hollow_sigil.wrong_dimension"), true);
            return InteractionResultHolder.fail(stack);
        }

        ServerLevel destination = serverPlayer.getServer().getLevel(destinationKey);
        if (destination == null) {
            serverPlayer.displayClientMessage(Component.translatable("item.biomesunseen.hollow_sigil.dimension_missing"), true);
            return InteractionResultHolder.fail(stack);
        }

        if (destinationKey.equals(ModDimensions.HOLLOW_DEEP_LEVEL)) {
            arriveInHollowDeep(serverPlayer, destination);
        } else {
            BlockPos spawn = destination.getSharedSpawnPos();
            int y = destination.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, spawn.getX(), spawn.getZ());
            serverPlayer.teleportTo(destination, spawn.getX() + 0.5, y, spawn.getZ() + 0.5,
                    serverPlayer.getYRot(), serverPlayer.getXRot());
        }
        serverPlayer.getCooldowns().addCooldown(this, 40);
        return InteractionResultHolder.sidedSuccess(stack, false);
    }

    private static void arriveInHollowDeep(ServerPlayer player, ServerLevel destination) {
        int chunkX = ARRIVAL.getX() >> 4;
        int chunkZ = ARRIVAL.getZ() >> 4;
        destination.getChunkSource().getChunk(chunkX, chunkZ, ChunkStatus.FULL, true);
        for (int dx = -2; dx <= 2; dx++) {
            for (int dz = -2; dz <= 2; dz++) {
                destination.setBlockAndUpdate(ARRIVAL.offset(dx, -1, dz), Blocks.MOSSY_STONE_BRICKS.defaultBlockState());
            }
        }
        for (int dy = 0; dy <= 2; dy++) {
            destination.setBlockAndUpdate(ARRIVAL.above(dy), Blocks.AIR.defaultBlockState());
        }
        player.teleportTo(destination, ARRIVAL.getX() + 0.5, ARRIVAL.getY(), ARRIVAL.getZ() + 0.5,
                player.getYRot(), player.getXRot());
    }
}
