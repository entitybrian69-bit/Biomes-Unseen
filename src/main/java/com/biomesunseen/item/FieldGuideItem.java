package com.biomesunseen.item;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

/** An in-game quick-start guide printed to chat when used. */
public class FieldGuideItem extends Item {
    public FieldGuideItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!level.isClientSide) {
            player.displayClientMessage(Component.translatable("guide.biomesunseen.title")
                    .withStyle(ChatFormatting.GOLD).withStyle(ChatFormatting.BOLD), false);
            player.displayClientMessage(Component.translatable("guide.biomesunseen.world"), false);
            player.displayClientMessage(Component.translatable("guide.biomesunseen.biomes"), false);
            player.displayClientMessage(Component.translatable("guide.biomesunseen.structures"), false);
            player.displayClientMessage(Component.translatable("guide.biomesunseen.dimension"), false);
            player.displayClientMessage(Component.translatable("guide.biomesunseen.weapons"), false);
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide);
    }
}
