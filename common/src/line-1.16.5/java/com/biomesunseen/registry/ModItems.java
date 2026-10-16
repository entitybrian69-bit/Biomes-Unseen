package com.biomesunseen.registry;

import net.minecraft.block.Block;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.item.BlockItem;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.SpawnEggItem;
import net.minecraft.item.crafting.Ingredient;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.MobEntity;

import com.biomesunseen.core.Content;
import com.biomesunseen.core.ModConstants;
import com.biomesunseen.core.OreDef;
import com.biomesunseen.item.UnseenArmorMaterial;
import com.biomesunseen.item.UnseenGearItems;
import com.biomesunseen.item.UnseenToolTier;

import me.shedaniel.architectury.registry.DeferredRegister;
import me.shedaniel.architectury.registry.RegistrySupplier;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;

/**
 * All items: 20 ore minerals, 120 gear pieces, 20
 * tonics, 4 machine cores, 27 spawn eggs, 29 lore
 * books, 25 mob trophies and the tab sigil.  Everything is
 * created from the shared Content catalog so items can never drift from
 * worldgen.
 */
public final class ModItems {

    public static final String MOD_ID = ModConstants.MOD_ID;

    public static ItemGroup MAIN;

    /** Every registered item, in creative-tab order. */
    public static final List<RegistrySupplier<Item>> ALL_ITEMS =
            new ArrayList<RegistrySupplier<Item>>();

    public static RegistrySupplier<Item> UNSEEN_SIGIL;

    /** ore id -> mineral item */
    public static final Map<String, RegistrySupplier<Item>> MINERALS =
            new LinkedHashMap<String, RegistrySupplier<Item>>();
    /** ore id -> tool tier */
    public static final Map<String, UnseenToolTier> TOOL_TIERS =
            new LinkedHashMap<String, UnseenToolTier>();
    /** ore id -> armor material */
    public static final Map<String, UnseenArmorMaterial> ARMOR_MATERIALS =
            new LinkedHashMap<String, UnseenArmorMaterial>();
    /** "<ore_id>_<slot>" -> gear item (pickaxe|sword|helmet|chestplate|leggings|boots) */
    public static final Map<String, RegistrySupplier<Item>> GEAR =
            new LinkedHashMap<String, RegistrySupplier<Item>>();
    /** ore id -> tonic item (applies the ore's potion effect) */
    public static final Map<String, RegistrySupplier<Item>> TONICS =
            new LinkedHashMap<String, RegistrySupplier<Item>>();
    /** tier number -> machine core item */
    public static final Map<Integer, RegistrySupplier<Item>> MACHINE_CORES =
            new LinkedHashMap<Integer, RegistrySupplier<Item>>();
    /** mob id -> spawn egg */
    public static final Map<String, RegistrySupplier<Item>> SPAWN_EGGS =
            new LinkedHashMap<String, RegistrySupplier<Item>>();
    /** lore theme -> journal item */
    public static final Map<String, RegistrySupplier<Item>> LORE_BOOKS =
            new LinkedHashMap<String, RegistrySupplier<Item>>();
    /** mob id -> trophy drop item */
    public static final Map<String, RegistrySupplier<Item>> TROPHIES =
            new LinkedHashMap<String, RegistrySupplier<Item>>();

    private static RegistrySupplier<Item> track(RegistrySupplier<Item> supplier) {
        ALL_ITEMS.add(supplier);
        return supplier;
    }

    private ModItems() {
    }

    public static void registerContent() {
        MAIN = new ItemGroup("biomesunseen") {
            @Override
            public ItemStack makeIcon() {
                return new ItemStack(UNSEEN_SIGIL.get());
            }
        };
        UNSEEN_SIGIL = track(ModRegistries.ITEMS.register("unseen_sigil",
                () -> new Item(new Item.Properties().stacksTo(16).tab(MAIN))));

        // Block items for every registered block.
        for (RegistrySupplier<Block> block : ModBlocks.allOres().values()) {
            track(ModRegistries.ITEMS.register(block.getId().getPath(),
                    () -> new BlockItem(block.get(), new Item.Properties().tab(MAIN))));
        }
        for (RegistrySupplier<Block> block : ModBlocks.allDecor().values()) {
            track(ModRegistries.ITEMS.register(block.getId().getPath(),
                    () -> new BlockItem(block.get(), new Item.Properties().tab(MAIN))));
        }
        for (RegistrySupplier<Block> block : ModBlocks.allPlants().values()) {
            track(ModRegistries.ITEMS.register(block.getId().getPath(),
                    () -> new BlockItem(block.get(), new Item.Properties().tab(MAIN))));
        }

        // Ore minerals, tool tiers, armor materials, gear and tonics.
        for (int i = 0; i < Content.ORES.size(); i++) {
            final OreDef ore = Content.ORES.get(i);
            RegistrySupplier<Item> mineral = track(ModRegistries.ITEMS.register(ore.id,
                    () -> new Item(new Item.Properties().tab(MAIN))));
            MINERALS.put(ore.id, mineral);
            TOOL_TIERS.put(ore.id, new UnseenToolTier(ore,
                    () -> Ingredient.of(mineral.get())));
            ARMOR_MATERIALS.put(ore.id, new UnseenArmorMaterial(ore,
                    () -> Ingredient.of(mineral.get())));
            GEAR.put(ore.id + "_pickaxe", track(ModRegistries.ITEMS.register(
                    ore.id + "_pickaxe",
                    () -> UnseenGearItems.pickaxe(ore, TOOL_TIERS.get(ore.id),
                            new Item.Properties().tab(MAIN)))));
            GEAR.put(ore.id + "_sword", track(ModRegistries.ITEMS.register(
                    ore.id + "_sword",
                    () -> UnseenGearItems.sword(ore, TOOL_TIERS.get(ore.id),
                            new Item.Properties().tab(MAIN)))));
            GEAR.put(ore.id + "_helmet", track(ModRegistries.ITEMS.register(
                    ore.id + "_helmet",
                    () -> UnseenGearItems.helmet(ore, ARMOR_MATERIALS.get(ore.id),
                            new Item.Properties().tab(MAIN)))));
            GEAR.put(ore.id + "_chestplate", track(ModRegistries.ITEMS.register(
                    ore.id + "_chestplate",
                    () -> UnseenGearItems.chestplate(ore, ARMOR_MATERIALS.get(ore.id),
                            new Item.Properties().tab(MAIN)))));
            GEAR.put(ore.id + "_leggings", track(ModRegistries.ITEMS.register(
                    ore.id + "_leggings",
                    () -> UnseenGearItems.leggings(ore, ARMOR_MATERIALS.get(ore.id),
                            new Item.Properties().tab(MAIN)))));
            GEAR.put(ore.id + "_boots", track(ModRegistries.ITEMS.register(
                    ore.id + "_boots",
                    () -> UnseenGearItems.boots(ore, ARMOR_MATERIALS.get(ore.id),
                            new Item.Properties().tab(MAIN)))));
            TONICS.put(ore.id, track(ModRegistries.ITEMS.register(
                    ore.id + "_tonic",
                    () -> new com.biomesunseen.item.UnseenTonicItem(ore,
                            new Item.Properties().stacksTo(16).tab(MAIN)))));
        }

        // Machine cores, one per machine tier used by the ore catalog.
        for (int tier = 1; tier <= 4; tier++) {
            MACHINE_CORES.put(tier, track(ModRegistries.ITEMS.register(
                    "machine_core_t" + tier,
                    () -> new Item(new Item.Properties().stacksTo(16).tab(MAIN)))));
        }

        // Spawn eggs for every mob and boss.
        for (int i = 0; i < Content.MOBS.size(); i++) {
            final String mobId = Content.MOBS.get(i).id;
            final int color = Content.MOBS.get(i).baseColor;
            final int accent = com.biomesunseen.core.ColorUtil.shade(color, 0.55D);
            SPAWN_EGGS.put(mobId, track(ModRegistries.ITEMS.register(
                    mobId + "_spawn_egg",
                    () -> new SpawnEggItem((EntityType<? extends MobEntity>) (EntityType<?>) ModEntities.MOB_TYPES.get(mobId).get(),
                            color, accent, new Item.Properties().tab(MAIN)))));
        }
        for (int i = 0; i < Content.BOSSES.size(); i++) {
            final String bossId = Content.BOSSES.get(i).id;
            final int color = Content.BOSSES.get(i).color;
            final int accent = com.biomesunseen.core.ColorUtil.shade(color, 0.5D);
            SPAWN_EGGS.put(bossId, track(ModRegistries.ITEMS.register(
                    bossId + "_spawn_egg",
                    () -> new SpawnEggItem((EntityType<? extends MobEntity>) (EntityType<?>) ModEntities.BOSS_TYPES.get(bossId).get(),
                            color, accent, new Item.Properties().tab(MAIN)))));
        }

        // Lore journals: one per structure lore theme.
        LinkedHashSet<String> themes = new LinkedHashSet<String>();
        for (int i = 0; i < Content.STRUCTURES.size(); i++) {
            themes.add(Content.STRUCTURES.get(i).loreTheme);
        }
        for (final String theme : themes) {
            LORE_BOOKS.put(theme, track(ModRegistries.ITEMS.register(
                    "lore_journal_" + theme,
                    () -> new com.biomesunseen.item.LoreBookItem(theme,
                            new Item.Properties().stacksTo(1).tab(MAIN)))));
        }

        // Mob trophies used in crafting and structure decor.
        for (int i = 0; i < Content.MOBS.size(); i++) {
            final String mobId = Content.MOBS.get(i).id;
            TROPHIES.put(mobId, track(ModRegistries.ITEMS.register(
                    mobId + "_trophy",
                    () -> new Item(new Item.Properties().tab(MAIN)))));
        }
    }

    public static RegistrySupplier<Item> mineral(String oreId) {
        return MINERALS.get(oreId);
    }
}
