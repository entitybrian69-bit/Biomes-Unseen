package com.biomesunseen.item;

import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.PickaxeItem;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tier;

import com.biomesunseen.core.OreDef;

/**
 * Factories for ore-derived gear.  Tools and armor inherit their stats from
 * the ore definition, keeping the whole catalog consistent.
 */
public final class UnseenGearItems {

    private UnseenGearItems() {
    }

    public static PickaxeItem pickaxe(OreDef ore, UnseenToolTier tier, Item.Properties properties) {
        return new UnseenPickaxeItem(ore, tier, properties);
    }

    public static SwordItem sword(OreDef ore, UnseenToolTier tier, Item.Properties properties) {
        return new UnseenSwordItem(ore, tier, properties);
    }

    public static ArmorItem helmet(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, EquipmentSlot.HEAD, properties);
    }

    public static ArmorItem chestplate(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, EquipmentSlot.CHEST, properties);
    }

    public static ArmorItem leggings(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, EquipmentSlot.LEGS, properties);
    }

    public static ArmorItem boots(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, EquipmentSlot.FEET, properties);
    }

    /** Concrete pickaxe bound to its ore. */
    public static final class UnseenPickaxeItem extends PickaxeItem {
        private final OreDef ore;

        UnseenPickaxeItem(OreDef ore, UnseenToolTier tier, Item.Properties properties) {
            super(tier, (int) ore.toolAttackDamage - 1, (float) (ore.toolSpeed / 2.5) - 2.4F, properties);
            this.ore = ore;
        }

        public OreDef ore() {
            return ore;
        }
    }

    /** Concrete sword bound to its ore. */
    public static final class UnseenSwordItem extends SwordItem {
        private final OreDef ore;

        UnseenSwordItem(OreDef ore, UnseenToolTier tier, Item.Properties properties) {
            super(tier, (int) ore.toolAttackDamage, (float) (ore.toolSpeed / 2.5), properties);
            this.ore = ore;
        }

        public OreDef ore() {
            return ore;
        }
    }

    /** Concrete armor piece bound to its ore. */
    public static final class UnseenArmorItem extends ArmorItem {
        private final OreDef ore;

        UnseenArmorItem(OreDef ore, UnseenArmorMaterial material, EquipmentSlot slot, Item.Properties properties) {
            super(material, slot, properties);
            this.ore = ore;
        }

        public OreDef ore() {
            return ore;
        }
    }
}
