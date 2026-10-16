package com.biomesunseen.item;

import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.potion.EffectInstance;
import net.minecraft.potion.Effects;
import net.minecraft.world.InteractionResult;
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
    public InteractionResult use(Level world, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        player.addEffect(new EffectInstance(effectFor(ore), 20 * 60, 0));
        if (!player.abilities.instabuild) {
            stack.shrink(1);
        }
        return InteractionResult.SUCCESS;
    }

    private static net.minecraft.potion.Effect effectFor(OreDef ore) {
        if ("fire_resistance".equals(ore.potionEffect)) {
            return Effects.FIRE_RESISTANCE;
        }
        if ("swiftness".equals(ore.potionEffect)) {
            return Effects.MOVEMENT_SPEED;
        }
        if ("strength".equals(ore.potionEffect)) {
            return Effects.DAMAGE_BOOST;
        }
        if ("regeneration".equals(ore.potionEffect)) {
            return Effects.REGENERATION;
        }
        if ("invisibility".equals(ore.potionEffect)) {
            return Effects.INVISIBILITY;
        }
        if ("night_vision".equals(ore.potionEffect)) {
            return Effects.NIGHT_VISION;
        }
        if ("water_breathing".equals(ore.potionEffect)) {
            return Effects.WATER_BREATHING;
        }
        if ("poison".equals(ore.potionEffect)) {
            return Effects.POISON;
        }
        if ("slowness".equals(ore.potionEffect)) {
            return Effects.MOVEMENT_SLOWDOWN;
        }
        if ("haste".equals(ore.potionEffect)) {
            return Effects.DIG_SPEED;
        }
        if ("levitation".equals(ore.potionEffect)) {
            return Effects.LEVITATION;
        }
        if ("absorption".equals(ore.potionEffect)) {
            return Effects.ABSORPTION;
        }
        return Effects.DAMAGE_RESISTANCE;
    }

}
