package com.biomesunseen.item;

import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;

import com.biomesunseen.core.OreDef;

import java.util.function.Supplier;

/**
 * Armor material derived from an ore definition.  Defense values scale with
 * the ore's tool tier so stronger ores make stronger armor.
 */
public class UnseenArmorMaterial implements ArmorMaterial {

    private static final int[] BASE_DURABILITY = new int[]{13, 15, 16, 11};
    private static final int[] BASE_DEFENSE = new int[]{2, 5, 6, 2};

    private final OreDef ore;
    private final Supplier<Ingredient> repairIngredient;

    public UnseenArmorMaterial(OreDef ore, Supplier<Ingredient> repairIngredient) {
        this.ore = ore;
        this.repairIngredient = repairIngredient;
    }

    /** Boots, leggings, chestplate, helmet -> index into the stat tables. */
    private static int indexOf(EquipmentSlot type) {
        switch (type) {
            case FEET:
                return 0;
            case LEGS:
                return 1;
            case CHEST:
                return 2;
            default:
                return 3;
        }
    }

    @Override
    public int getDurabilityForType(EquipmentSlot type) {
        return BASE_DURABILITY[indexOf(type)] * (ore.toolDurability / 33);
    }

    @Override
    public int getDefenseForType(EquipmentSlot type) {
        return BASE_DEFENSE[indexOf(type)] + ore.toolMiningLevel;
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
    public Ingredient getRepairIngredient() {
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
