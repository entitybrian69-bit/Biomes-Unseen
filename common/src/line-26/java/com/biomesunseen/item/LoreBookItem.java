package com.biomesunseen.item;

import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.ItemUtils;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.level.Level;

/**
 * Lore journal found in structures.  Reading it surfaces the theme's journal
 * text (written into en_us.json) and unlocks structure advancements.
 */
public class LoreBookItem extends Item {

    private final String theme;

    public LoreBookItem(String theme, Item.Properties properties) {
        super(properties);
        this.theme = theme;
    }

    public String theme() {
        return theme;
    }

    @Override
    public InteractionResult use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level.isClientSide()) {
            return InteractionResult.SUCCESS;
        }
        player.displayClientMessage(net.minecraft.network.chat.Component.translatable(
                "book.biomesunseen." + theme), false);
        return InteractionResult.SUCCESS;
    }

}
