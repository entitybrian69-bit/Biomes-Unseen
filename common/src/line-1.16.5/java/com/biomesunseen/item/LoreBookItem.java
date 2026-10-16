package com.biomesunseen.item;

import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.potion.EffectInstance;
import net.minecraft.potion.Effects;
import net.minecraft.util.ActionResultType;
import net.minecraft.util.Hand;
import net.minecraft.world.World;

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
    public ActionResultType use(World world, PlayerEntity player, Hand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (world.isClientSide) {
            return ActionResultType.SUCCESS;
        }
        player.sendMessage(new net.minecraft.util.text.TranslationTextComponent(
                "book.biomesunseen." + theme), player.getUUID());
        return ActionResultType.SUCCESS;
    }

}
