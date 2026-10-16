package com.biomesunseen.item;

import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.crafting.Ingredient;

import com.biomesunseen.core.OreDef;

import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.function.Supplier;

/**
 * Armor material derived from an ore definition.  From 1.20.5 the vanilla
 * ArmorMaterial is a final record, so this class builds one and hands the
 * armor items a holder of it.
 */
public final class UnseenArmorMaterial {

    private final OreDef ore;
    private final Supplier<Ingredient> repairIngredient;
    private final ArmorMaterial material;
    private final Holder<ArmorMaterial> holder;

    public UnseenArmorMaterial(OreDef ore, Supplier<Ingredient> repairIngredient) {
        this.ore = ore;
        this.repairIngredient = repairIngredient;
        Map<ArmorItem.Type, Integer> defense = new EnumMap<>(ArmorItem.Type.class);
        defense.put(ArmorItem.Type.HELMET, ore.toolMiningLevel + 2);
        defense.put(ArmorItem.Type.CHESTPLATE, ore.toolMiningLevel + 5);
        defense.put(ArmorItem.Type.LEGGINGS, ore.toolMiningLevel + 4);
        defense.put(ArmorItem.Type.BOOTS, ore.toolMiningLevel + 2);
        this.material = new ArmorMaterial(
                defense,
                ore.toolEnchantability,
                SoundEvents.ARMOR_EQUIP_IRON,
                repairIngredient,
                List.of(new ArmorMaterial.Layer(net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("biomesunseen", ore.id))),
                ore.toolMiningLevel * 0.5F,
                ore.toolMiningLevel >= 4 ? 0.1F : 0.0F);
        this.holder = Holder.direct(this.material);
    }

    /** @return the holder the ArmorItem constructor needs. */
    public Holder<ArmorMaterial> holder() {
        return holder;
    }

    public ArmorMaterial material() {
        return material;
    }

    public OreDef ore() {
        return ore;
    }

    public int getDefenseForType(ArmorItem.Type type) {
        return material.getDefense(type);
    }

    public int getEnchantmentValue() {
        return ore.toolEnchantability;
    }

    public Ingredient getRepairIngredient() {
        return repairIngredient.get();
    }

    public float getToughness() {
        return ore.toolMiningLevel * 0.5F;
    }

    public float getKnockbackResistance() {
        return ore.toolMiningLevel >= 4 ? 0.1F : 0.0F;
    }
}
