package com.biomesunseen.init;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.entity.EntityType;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

/**
 * Four creative tabs: blocks, gear, nature (spawn eggs) and lore.
 *
 * Splitting them keeps 264 blocks and 285 items from becoming one unusable
 * scroll, and it puts the spawn eggs and lore books where a player building a
 * world expects to find them rather than buried after the last ore block.
 */
public final class BUCreativeTabs {

    public static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, BUContent.MODID);

    public static final RegistryObject<CreativeModeTab> BLOCKS =
            TABS.register("blocks", () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.biomesunseen.blocks"))
                    .icon(BUCreativeTabs::blockIcon)
                    .displayItems((parameters, output) -> {
                        for (String path : BUContent.allBlocks()) {
                            Item item = BUItems.get(path);
                            if (item != null && item != Items.AIR) {
                                output.accept(item);
                            }
                        }
                    })
                    .build());

    public static final RegistryObject<CreativeModeTab> GEAR =
            TABS.register("gear", () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.biomesunseen.gear"))
                    .icon(BUCreativeTabs::gearIcon)
                    .displayItems((parameters, output) -> {
                        for (String id : BUContent.ITEMS_TOOLS) {
                            accept(output, id);
                        }
                        for (String[] row : BUContent.ARMOUR_ITEMS) {
                            accept(output, row[0]);
                        }
                        for (String id : BUContent.ITEMS_ARTEFACTS) {
                            accept(output, id);
                        }
                        for (String id : BUContent.ITEMS_MATERIALS) {
                            accept(output, id);
                        }
                    })
                    .build());

    public static final RegistryObject<CreativeModeTab> NATURE =
            TABS.register("nature", () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.biomesunseen.nature"))
                    .icon(BUCreativeTabs::natureIcon)
                    .displayItems((parameters, output) -> {
                        for (String[] row : BUContent.SPAWN_EGGS) {
                            accept(output, row[0]);
                        }
                    })
                    .build());

    public static final RegistryObject<CreativeModeTab> LORE =
            TABS.register("lore", () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.biomesunseen"))
                    .icon(BUCreativeTabs::loreIcon)
                    .displayItems((parameters, output) -> {
                        for (String id : BUContent.ITEMS_LORE_BOOKS) {
                            accept(output, id);
                        }
                        accept(output, "portal_igniter");
                        accept(output, "reality_compass");
                        accept(output, "music_disc_unseen");
                    })
                    .build());

    private BUCreativeTabs() {
    }

    public static void register(IEventBus bus) {
        TABS.register(bus);
    }

    private static void accept(CreativeModeTab.Output output, String id) {
        Item item = BUItems.get(id);
        if (item != null && item != Items.AIR) {
            output.accept(item);
        }
    }

    // ---- tab icons ----------------------------------------------------- //
    // Each icon is a real registered item rather than a placeholder, so the tab
    // never renders as a missing-texture cube.

    private static ItemStack blockIcon() {
        Item item = BUItems.get("boss_altar");
        if (item == null) {
            item = BUItems.get(BUContent.BLOCKS_CUBE.length > 0
                    ? BUContent.BLOCKS_CUBE[0] : "");
        }
        return item == null ? new ItemStack(Items.STONE) : new ItemStack(item);
    }

    private static ItemStack gearIcon() {
        Item item = BUItems.get("starforged_sword");
        return item == null ? new ItemStack(Items.NETHERITE_SWORD) : new ItemStack(item);
    }

    private static ItemStack natureIcon() {
        Item item = BUItems.get("heart_of_the_forest_spawn_egg");
        if (item == null && BUContent.SPAWN_EGGS.length > 0) {
            item = BUItems.get(BUContent.SPAWN_EGGS[0][0]);
        }
        return item == null ? new ItemStack(Items.EGG) : new ItemStack(item);
    }

    private static ItemStack loreIcon() {
        Item item = BUItems.get("lore_book_heart");
        return item == null ? new ItemStack(Items.BOOK) : new ItemStack(item);
    }
}
