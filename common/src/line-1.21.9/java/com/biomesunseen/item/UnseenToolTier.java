package com.biomesunseen.item;

import net.minecraft.tags.BlockTags;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.ToolMaterial;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.block.Block;

import com.biomesunseen.core.OreDef;

import java.util.function.Supplier;

/**
 * Tool material derived from an ore definition: durability, mining speed,
 * attack bonus and enchantability all come straight from the ore catalog.
 */
public class UnseenToolTier implements ToolMaterial {

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
    public TagKey<Block> getIncorrectBlocksForDrops() {
        return BlockTags.INCORRECT_FOR_NETHERITE_TOOL;
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

    public int getLevel() {
        return ore.toolMiningLevel;
    }
}
