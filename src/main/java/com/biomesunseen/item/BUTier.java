package com.biomesunseen.item;

import net.minecraft.world.item.Tier;
import net.minecraft.world.item.crafting.Ingredient;

import java.util.function.Supplier;

/**
 * A tool tier built from the generated gear table.
 *
 * Forge's {@code Tiers} enum is closed, so a mod adding ten gear families has
 * to supply its own {@link Tier}. Rather than write ten near-identical classes,
 * one parameterised implementation is constructed per row of
 * {@code BUContent.GEAR_TIER}.
 */
public final class BUTier implements Tier {

    private final int level;
    private final int uses;
    private final float speed;
    private final float attackDamageBonus;
    private final int enchantmentValue;
    private final Supplier<Ingredient> repairIngredient;

    public BUTier(int level, int uses, float speed, float attackDamageBonus,
                  int enchantmentValue, Supplier<Ingredient> repairIngredient) {
        this.level = level;
        this.uses = uses;
        this.speed = speed;
        this.attackDamageBonus = attackDamageBonus;
        this.enchantmentValue = enchantmentValue;
        this.repairIngredient = repairIngredient;
    }

    @Override
    public int getUses() {
        return uses;
    }

    @Override
    public float getSpeed() {
        return speed;
    }

    @Override
    public float getAttackDamageBonus() {
        return attackDamageBonus;
    }

    @Override
    public int getLevel() {
        return level;
    }

    @Override
    public int getEnchantmentValue() {
        return enchantmentValue;
    }

    @Override
    public Ingredient getRepairIngredient() {
        return repairIngredient.get();
    }

}
