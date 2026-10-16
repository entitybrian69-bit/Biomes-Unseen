package com.biomesunseen.item;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.Identifier;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;

import com.biomesunseen.core.OreDef;

import java.util.EnumMap;
import java.util.Map;
import java.util.function.Supplier;

/**
 * Armor material derived from an ore definition.  From 1.21.2 the vanilla
 * ArmorMaterial is a record keyed on an equipment asset, so this class builds
 * one from the ore catalog.
 */
public final class UnseenArmorMaterial {

    private final OreDef ore;
    private final Supplier<net.minecraft.world.item.crafting.Ingredient> repairIngredient;
    private final ArmorMaterial material;

    public UnseenArmorMaterial(OreDef ore,
            Supplier<net.minecraft.world.item.crafting.Ingredient> repairIngredient) {
        this.ore = ore;
        this.repairIngredient = repairIngredient;
        Map<ArmorType, Integer> defense = new EnumMap<>(ArmorType.class);
        defense.put(ArmorType.HELMET, ore.toolMiningLevel + 2);
        defense.put(ArmorType.CHESTPLATE, ore.toolMiningLevel + 5);
        defense.put(ArmorType.LEGGINGS, ore.toolMiningLevel + 4);
        defense.put(ArmorType.BOOTS, ore.toolMiningLevel + 2);
        this.material = new ArmorMaterial(
                Math.max(1, ore.toolDurability / 33) * 13,
                defense,
                ore.toolEnchantability,
                SoundEvents.ARMOR_EQUIP_IRON,
                ore.toolMiningLevel * 0.5F,
                ore.toolMiningLevel >= 4 ? 0.1F : 0.0F,
                TagKey.create(Registries.ITEM,
                        Identifier.fromNamespaceAndPath("biomesunseen", "repairs_armor")),
                ResourceKey.create(
                        ResourceKey.createRegistryKey(
                                Identifier.fromNamespaceAndPath("minecraft", "equipment_asset")),
                        Identifier.fromNamespaceAndPath("minecraft", "iron")));
    }

    /** @return the record the armor item constructor needs. */
    public ArmorMaterial material() {
        return material;
    }

    public OreDef ore() {
        return ore;
    }

    public int getDefenseForType(ArmorType type) {
        Integer value = material.defense().get(type);
        return value == null ? 0 : value;
    }

    public int getEnchantmentValue() {
        return ore.toolEnchantability;
    }

    public net.minecraft.world.item.crafting.Ingredient getRepairIngredient() {
        return repairIngredient.get();
    }

    public float getToughness() {
        return ore.toolMiningLevel * 0.5F;
    }

    public float getKnockbackResistance() {
        return ore.toolMiningLevel >= 4 ? 0.1F : 0.0F;
    }
}
