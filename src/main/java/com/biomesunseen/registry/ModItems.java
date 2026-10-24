package com.biomesunseen.registry;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.spec.MobSpec;
import com.biomesunseen.spec.OreSpec;
import com.biomesunseen.spec.Specs;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraftforge.common.ForgeSpawnEggItem;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

import java.util.LinkedHashMap;
import java.util.Map;

public final class ModItems {
    public static final DeferredRegister<Item> ITEMS =
            DeferredRegister.create(ForgeRegistries.ITEMS, BiomesUnseen.MOD_ID);

    public static final RegistryObject<Item> HOLLOWITE_ORE = ITEMS.register("hollowite_ore",
            () -> new BlockItem(ModBlocks.HOLLOWITE_ORE.get(), new Item.Properties()));

    public static final RegistryObject<Item> HOLLOWITE_INGOT = ITEMS.register("hollowite_ingot",
            () -> new Item(new Item.Properties()));

    public static final RegistryObject<Item> HOLLOW_STALKER_SPAWN_EGG = egg("hollow_stalker_spawn_egg",
            ModEntities.HOLLOW_STALKER, 0x1F2D27, 0x7CFFB2);
    public static final RegistryObject<Item> SPORELING_SPAWN_EGG = egg("sporeling_spawn_egg",
            ModEntities.SPORELING, 0xB8703B, 0xFFE98A);
    public static final RegistryObject<Item> GLOOM_CRAWLER_SPAWN_EGG = egg("gloom_crawler_spawn_egg",
            ModEntities.GLOOM_CRAWLER, 0x2A2438, 0xB066FF);
    public static final RegistryObject<Item> CRYSTAL_GOLEM_SPAWN_EGG = egg("crystal_golem_spawn_egg",
            ModEntities.CRYSTAL_GOLEM, 0x5A4A8A, 0xA5FFF2);
    public static final RegistryObject<Item> MIRE_WRAITH_SPAWN_EGG = egg("mire_wraith_spawn_egg",
            ModEntities.MIRE_WRAITH, 0x2A3A2A, 0xB5FF7A);
    public static final RegistryObject<Item> HEART_OF_THE_FOREST_SPAWN_EGG = egg("heart_of_the_forest_spawn_egg",
            ModEntities.HEART_OF_THE_FOREST, 0x3B2616, 0x7CFFB2);

    /** Spawn eggs for the generated mobs, keyed by mob id. */
    public static final Map<String, RegistryObject<Item>> SPEC_EGGS = new LinkedHashMap<>();

    static {
        for (MobSpec spec : Specs.mobs()) {
            SPEC_EGGS.put(spec.id(), egg(spec.id() + "_spawn_egg", ModEntities.SPEC_MOBS.get(spec.id()),
                    spec.eggPrimary(), spec.eggSecondary()));
        }
    }

    /** Generated ore block items and drop items, keyed by ore id. */
    public static final Map<String, RegistryObject<Item>> ORE_BLOCK_ITEMS = new LinkedHashMap<>();
    public static final Map<String, RegistryObject<Item>> ORE_ITEMS = new LinkedHashMap<>();

    static {
        for (OreSpec spec : Specs.ores()) {
            ORE_BLOCK_ITEMS.put(spec.id(), ITEMS.register(spec.blockId(),
                    () -> new BlockItem(ModBlocks.ORES.get(spec.id()).get(), new Item.Properties())));
            ORE_ITEMS.put(spec.id(), ITEMS.register(spec.item(), () -> new Item(new Item.Properties())));
        }
    }

    private static <T extends Mob> RegistryObject<Item> egg(String name,
            RegistryObject<EntityType<T>> type, int background, int highlight) {
        return ITEMS.register(name, () -> new ForgeSpawnEggItem(type, background, highlight, new Item.Properties()));
    }

    private ModItems() {
    }

    public static void register(IEventBus bus) {
        ITEMS.register(bus);
    }
}
