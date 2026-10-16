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
    public int getLevel() {
        return ore.toolMiningLevel;
    }

    @Override
    public int getEnchantability() {
        return ore.toolEnchantability;
    }

    @Override
    public Ingredient getRepairMaterial() {
        return repairIngredient.get();
    }

    public OreDef ore() {
        return ore;
    }
}
