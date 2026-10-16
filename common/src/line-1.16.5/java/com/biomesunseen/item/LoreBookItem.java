package com.biomesunseen.item;

import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.potion.EffectInstance;
import net.minecraft.potion.Effects;
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
    public InteractionResult use(Level world, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (world.isClientSide) {
            return InteractionResult.SUCCESS;
        }
        player.sendMessage(new net.minecraft.network.chat.TranslatableComponent(
                "book.biomesunseen." + theme), player.getUUID());
        return InteractionResult.SUCCESS;
    }

}
