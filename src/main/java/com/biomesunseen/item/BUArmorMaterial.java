package com.biomesunseen.item;

import net.minecraft.sounds.SoundEvent;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.crafting.Ingredient;

import java.util.function.Supplier;

/**
 * An armour material built from the generated gear table.
 *
 * One parameterised implementation serves all ten families; each is constructed
 * from a row of {@code BUContent.GEAR_ARMOUR}, which carries the per-slot
 * defence values, toughness, knockback resistance and repair ingredient.
 *
 * 1.20.1 indexes armour by {@link ArmorItem.Type} rather than by
 * {@code EquipmentSlot}, so the defence array is ordered to match that enum
 * (boots, leggings, chestplate, helmet).
 */
public final class BUArmorMaterial implements ArmorMaterial {

    /** Vanilla's per-slot durability base, indexed by ArmorItem.Type ordinal. */
    private static final int[] DURABILITY_PER_TYPE = {13, 15, 16, 11};

    private final String name;
    private final int durabilityMultiplier;
    private final int[] protection;
    private final int enchantmentValue;
    private final Supplier<SoundEvent> equipSound;
    private final float toughness;
    private final float knockbackResistance;
    private final Supplier<Ingredient> repairIngredient;

    /**
     * @param protection defence indexed by {@link ArmorItem.Type} ordinal:
     *                   {helmet, chestplate, leggings, boots}
     */
    public BUArmorMaterial(String name, int durabilityMultiplier, int[] protection,
                           int enchantmentValue, Supplier<SoundEvent> equipSound,
                           float toughness, float knockbackResistance,
                           Supplier<Ingredient> repairIngredient) {
        this.name = name;
        this.durabilityMultiplier = durabilityMultiplier;
        this.protection = protection;
        this.enchantmentValue = enchantmentValue;
        this.equipSound = equipSound;
        this.toughness = toughness;
        this.knockbackResistance = knockbackResistance;
        this.repairIngredient = repairIngredient;
    }

    @Override
    public int getDurabilityForType(ArmorItem.Type type) {
        return DURABILITY_PER_TYPE[type.ordinal()] * durabilityMultiplier;
    }

    @Override
    public int getDefenseForType(ArmorItem.Type type) {
        return protection[type.ordinal()];
    }

    @Override
    public int getEnchantmentValue() {
        return enchantmentValue;
    }

    @Override
    public SoundEvent getEquipSound() {
        return equipSound.get();
    }

    @Override
    public Ingredient getRepairIngredient() {
        return repairIngredient.get();
    }

    @Override
    public String getName() {
        // Must be the namespaced material name: it is used to locate the armour
        // texture layer, so a bare name would point at a missing texture.
        return "biomesunseen:" + name;
    }

    @Override
    public float getToughness() {
        return toughness;
    }

    @Override
    public float getKnockbackResistance() {
        return knockbackResistance;
    }
}
