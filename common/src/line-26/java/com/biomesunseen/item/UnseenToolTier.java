package com.biomesunseen.item;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.ToolMaterial;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.block.Block;

import com.biomesunseen.core.OreDef;

import java.util.function.Supplier;

/**
 * Tool material derived from an ore definition.  From 1.21.2 the vanilla
 * ToolMaterial is a final record, so this builds one from the ore catalog
 * instead of implementing an interface.
 */
public final class UnseenToolTier {

    private final OreDef ore;
    private final Supplier<Ingredient> repairIngredient;
    private final ToolMaterial material;

    public UnseenToolTier(OreDef ore, Supplier<Ingredient> repairIngredient) {
        this.ore = ore;
        this.repairIngredient = repairIngredient;
        this.material = new ToolMaterial(
                TagKey.create(Registries.BLOCK,
                        Identifier.fromNamespaceAndPath(
                                "biomesunseen", "incorrect_for_" + ore.id)),
                ore.toolDurability,
                (float) ore.toolSpeed,
                (float) ore.toolAttackDamage,
                ore.toolEnchantability,
                TagKey.create(Registries.ITEM,
                        Identifier.fromNamespaceAndPath(
                                "c", "ores/" + ore.id)));
    }

    /** @return the vanilla record the tool items are constructed from. */
    public ToolMaterial material() {
        return material;
    }

    public OreDef ore() {
        return ore;
    }

    public int getUses() {
        return ore.toolDurability;
    }

    public float getSpeed() {
        return (float) ore.toolSpeed;
    }

    public float getAttackDamageBonus() {
        return (float) ore.toolAttackDamage;
    }

    public int getEnchantmentValue() {
        return ore.toolEnchantability;
    }

    public int getLevel() {
        return ore.toolMiningLevel;
    }

    public Ingredient getRepairIngredient() {
        return repairIngredient.get();
    }
}
