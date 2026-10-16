package com.biomesunseen.item;

import net.minecraft.world.item.Tier;
import net.minecraft.world.item.crafting.Ingredient;

import com.biomesunseen.core.OreDef;

import java.util.function.Supplier;

/**
 * Tool tier derived from an ore definition: durability, mining level, speed
 * and enchantability all come straight from the ore catalog.
 */
public class UnseenToolTier implements Tier {

    private final OreDef ore;
    private final Supplier<Ingredient> repairIngredient;

    public UnseenToolTier(OreDef ore, Supplier<Ingredient> repairIngredient) {
        this.ore = ore;
        this.repairIngredient = repairIngredient;
    }

    @Override
    public int getUses() {
        return ore.toolDurability;
    }

    @Override
    public float getSpeed() {
        return (float) ore.toolSpeed;
    }

    @Override
    public float getAttackDamageBonus() {
        return (float) ore.toolAttackDamage;
    }

    @Override
    public net.minecraft.tags.TagKey<net.minecraft.world.level.block.Block> getIncorrectBlocksForDrops() {
        int level = ore.toolMiningLevel;
        if (level >= 4) {
            return net.minecraft.tags.BlockTags.INCORRECT_FOR_NETHERITE_TOOL;
        }
        if (level == 3) {
            return net.minecraft.tags.BlockTags.INCORRECT_FOR_DIAMOND_TOOL;
        }
        if (level == 2) {
            return net.minecraft.tags.BlockTags.INCORRECT_FOR_IRON_TOOL;
        }
        if (level == 1) {
            return net.minecraft.tags.BlockTags.INCORRECT_FOR_STONE_TOOL;
        }
        return net.minecraft.tags.BlockTags.INCORRECT_FOR_WOODEN_TOOL;
    }

    @Override
    public int getEnchantmentValue() {
        return ore.toolEnchantability;
    }

    @Override
    public Ingredient getRepairIngredient() {
        return repairIngredient.get();
    }

    public OreDef ore() {
        return ore;
    }
}
