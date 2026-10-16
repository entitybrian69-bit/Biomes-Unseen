package com.biomesunseen.item;

import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ToolMaterial;

import com.biomesunseen.core.OreDef;

/**
 * Factories for ore-derived gear.  Tools and armor inherit their stats from
 * the ore definition, keeping the whole catalog consistent.
 */
public final class UnseenGearItems {

    private UnseenGearItems() {
    }

    public static Item pickaxe(OreDef ore, UnseenToolTier tier, Item.Properties properties) {
        return new UnseenPickaxeItem(ore, tier, properties);
    }

    public static Item sword(OreDef ore, UnseenToolTier tier, Item.Properties properties) {
        return new UnseenSwordItem(ore, tier, properties);
    }

    public static Item helmet(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, ArmorType.HELMET, properties);
    }

    public static Item chestplate(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, ArmorType.CHESTPLATE, properties);
    }

    public static Item leggings(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, ArmorType.LEGGINGS, properties);
    }

    public static Item boots(OreDef ore, UnseenArmorMaterial material, Item.Properties properties) {
        return new UnseenArmorItem(ore, material, ArmorType.BOOTS, properties);
    }

    /** Concrete pickaxe bound to its ore. */
    public static final class UnseenPickaxeItem extends Item {
        private final OreDef ore;

        UnseenPickaxeItem(OreDef ore, UnseenToolTier tier, Item.Properties properties) {
            super(properties);
            this.ore = ore;
        }

        public OreDef ore() {
            return ore;
        }
    }

    /** Concrete sword bound to its ore. */
    public static final class UnseenSwordItem extends Item {
        private final OreDef ore;

        UnseenSwordItem(OreDef ore, UnseenToolTier tier, Item.Properties properties) {
            super(properties);
            this.ore = ore;
        }

        public OreDef ore() {
            return ore;
        }
    }

    /** Concrete armor piece bound to its ore. */
    public static final class UnseenArmorItem extends Item {
        private final OreDef ore;

        UnseenArmorItem(OreDef ore, UnseenArmorMaterial material, ArmorType slot, Item.Properties properties) {
            super(properties);
            this.ore = ore;
        }

        public OreDef ore() {
            return ore;
        }
    }
}
