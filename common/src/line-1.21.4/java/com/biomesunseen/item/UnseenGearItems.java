package com.biomesunseen.item;

import net.minecraft.world.item.equipment.ArmorType;

import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.PickaxeItem;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.ToolMaterial;

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
        return new UnseenArmorItem(ore, material, ArmorType.HELMET, properties);
    }

    public static ArmorItem chestplate(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, ArmorType.CHESTPLATE, properties);
    }

    public static ArmorItem leggings(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, ArmorType.LEGGINGS, properties);
    }

    public static ArmorItem boots(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, ArmorType.BOOTS, properties);
    }

    /** Concrete pickaxe bound to its ore. */
    public static final class UnseenPickaxeItem extends PickaxeItem {
        private final OreDef ore;

        UnseenPickaxeItem(OreDef ore, UnseenToolTier tier, Item.Properties properties) {
            super(tier.material(), (int) ore.toolAttackDamage - 1, (float) (ore.toolSpeed / 2.5) - 2.4F, properties);
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
            super(tier.material(), (int) ore.toolAttackDamage, (float) (ore.toolSpeed / 2.5), properties);
            this.ore = ore;
        }

        public OreDef ore() {
            return ore;
        }
    }

    /** Concrete armor piece bound to its ore. */
    public static final class UnseenArmorItem extends ArmorItem {
        private final OreDef ore;

        UnseenArmorItem(OreDef ore, UnseenArmorMaterial material, ArmorType slot, Item.Properties properties) {
            super(material.holder(), slot, properties);
            this.ore = ore;
        }

        public OreDef ore() {
            return ore;
        }
    }
}
