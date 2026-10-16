package com.biomesunseen.item;

import net.minecraft.inventory.EquipmentSlotType;
import net.minecraft.item.IArmorMaterial;
import net.minecraft.item.crafting.Ingredient;
import net.minecraft.util.SoundEvent;
import net.minecraft.util.SoundEvents;

import com.biomesunseen.core.OreDef;

import java.util.function.Supplier;

/**
 * Armor material derived from an ore definition.  Defense values scale with
 * the ore's tool tier so stronger ores make stronger armor.
 */
public class UnseenArmorMaterial implements IArmorMaterial {

    private static final int[] BASE_DURABILITY = new int[]{13, 15, 16, 11};
    private static final int[] BASE_DEFENSE = new int[]{2, 5, 6, 2};

    private final OreDef ore;
    private final Supplier<Ingredient> repairIngredient;

    public UnseenArmorMaterial(OreDef ore, Supplier<Ingredient> repairIngredient) {
        this.ore = ore;
        this.repairIngredient = repairIngredient;
    }

    @Override
    public int getDurabilityForSlot(EquipmentSlotType slot) {
        return BASE_DURABILITY[slot.getIndex()] * (ore.toolDurability / 33);
    }

    @Override
    public int getDefenseForSlot(EquipmentSlotType slot) {
        return BASE_DEFENSE[slot.getIndex()] + ore.toolMiningLevel;
    }

    @Override
    public int getEnchantmentValue() {
        return ore.toolEnchantability;
    }

    @Override
    public SoundEvent getEquipSound() {
        return SoundEvents.ARMOR_EQUIP_IRON;
    }

    @Override
    public Ingredient getRepairMaterial() {
        return repairIngredient.get();
    }

    @Override
    public String getName() {
        return "biomesunseen:" + ore.id;
    }

    @Override
    public float getToughness() {
        return ore.toolMiningLevel * 0.5F;
    }

    @Override
    public float getKnockbackResistance() {
        return ore.toolMiningLevel >= 4 ? 0.1F : 0.0F;
    }

    public OreDef ore() {
        return ore;
    }
}
