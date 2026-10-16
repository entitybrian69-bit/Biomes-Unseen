package com.biomesunseen.item;

import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.ItemUtils;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.level.Level;

import com.biomesunseen.core.OreDef;

/**
 * Potion-effect tonic distilled from an ore.  Each ore maps to its potion
 * effect from the ore catalog ("use in potions").
 */
public class UnseenTonicItem extends Item {

    private final OreDef ore;

    public UnseenTonicItem(OreDef ore, Item.Properties properties) {
        super(properties);
        this.ore = ore;
    }

    public OreDef ore() {
        return ore;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        player.addEffect(new MobEffectInstance(effectFor(ore), 20 * 60, 0));
        if (!player.getAbilities().instabuild) {
            stack.shrink(1);
        }
        return InteractionResultHolder.success(stack);
    }

    private static net.minecraft.core.Holder<net.minecraft.world.effect.MobEffect> effectFor(OreDef ore) {
        if ("fire_resistance".equals(ore.potionEffect)) {
            return MobEffects.FIRE_RESISTANCE;
        }
        if ("swiftness".equals(ore.potionEffect)) {
            return MobEffects.MOVEMENT_SPEED;
        }
        if ("strength".equals(ore.potionEffect)) {
            return MobEffects.DAMAGE_BOOST;
        }
        if ("regeneration".equals(ore.potionEffect)) {
            return MobEffects.REGENERATION;
        }
        if ("invisibility".equals(ore.potionEffect)) {
            return MobEffects.INVISIBILITY;
        }
        if ("night_vision".equals(ore.potionEffect)) {
            return MobEffects.NIGHT_VISION;
        }
        if ("water_breathing".equals(ore.potionEffect)) {
            return MobEffects.WATER_BREATHING;
        }
        if ("poison".equals(ore.potionEffect)) {
            return MobEffects.POISON;
        }
        if ("slowness".equals(ore.potionEffect)) {
            return MobEffects.MOVEMENT_SLOWDOWN;
        }
        if ("haste".equals(ore.potionEffect)) {
            return MobEffects.DIG_SPEED;
        }
        if ("levitation".equals(ore.potionEffect)) {
            return MobEffects.LEVITATION;
        }
        if ("absorption".equals(ore.potionEffect)) {
            return MobEffects.ABSORPTION;
        }
        return MobEffects.DAMAGE_RESISTANCE;
    }

}
