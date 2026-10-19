package com.biomesunseen.init;

import com.biomesunseen.item.BUArmorMaterial;
import com.biomesunseen.item.BULoreBookItem;
import com.biomesunseen.item.BUTier;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.AxeItem;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.BowItem;
import net.minecraft.world.item.HoeItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.PickaxeItem;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.ShieldItem;
import net.minecraft.world.item.ShovelItem;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.block.Block;
import net.minecraftforge.common.ForgeSpawnEggItem;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;
import java.util.function.Supplier;

/**
 * Every item the mod adds, registered from the generated {@link BUContent} table.
 *
 * Like the blocks, this is data-driven: one gear family contributes a sword,
 * pickaxe, axe, shovel, hoe and any bow or shield it declares, all sharing that
 * family's {@link BUTier}. Adding an eleventh family to tools/content/gear.py
 * produces its five-plus tools, four armour pieces, repair recipe and item
 * models on the next codegen run with no change here.
 */
public final class BUItems {

    public static final DeferredRegister<Item> ITEMS =
            DeferredRegister.create(ForgeRegistries.ITEMS, BUContent.MODID);

    private static final Map<String, RegistryObject<Item>> BY_PATH = new LinkedHashMap<>();
    private static final Map<String, BUTier> TIERS = new LinkedHashMap<>();
    private static final Map<String, BUArmorMaterial> ARMOUR = new LinkedHashMap<>();
    /** Armour set id -> the set bonus it grants when all four pieces are worn. */
    private static final Map<String, String> SET_BONUS = new LinkedHashMap<>();

    private BUItems() {
    }

    public static void register(IEventBus bus) {
        buildGearTables();
        registerBlockItems();
        registerMaterials();
        registerTools();
        registerArmour();
        registerSpawnEggs();
        registerLoreBooks();
        ITEMS.register(bus);
    }

    // ------------------------------------------------------------------ //
    //  Gear stat tables
    // ------------------------------------------------------------------ //

    private static void buildGearTables() {
        for (Object[] row : BUContent.GEAR_TIER) {
            String setId = (String) row[0];
            int level = (Integer) row[1];
            int uses = (Integer) row[2];
            float speed = (Float) row[3];
            float attackBonus = (Float) row[4];
            int enchant = (Integer) row[5];
            String repair = (String) row[6];
            // Harvestability in 1.20.1 is Tier.getLevel() plus the needs_*_tool
            // block tags shipped in the datapack, so no tag key is needed here.
            TIERS.put(setId, new BUTier(level, uses, speed, attackBonus, enchant,
                    () -> ingredientFor(repair)));
        }

        for (Object[] row : BUContent.GEAR_ARMOUR) {
            String setId = (String) row[0];
            int durabilityMultiplier = (Integer) row[1];
            // ArmorItem.Type is ordered HELMET, CHESTPLATE, LEGGINGS, BOOTS, and
            // the generated table stores the pieces in that same order, so the
            // array can be used as-is. Reordering it would silently swap the
            // helmet's defence onto the boots.
            int helmet = (Integer) row[2];
            int chestplate = (Integer) row[3];
            int leggings = (Integer) row[4];
            int boots = (Integer) row[5];
            int[] protection = {helmet, chestplate, leggings, boots};
            float toughness = (Float) row[6];
            float knockback = (Float) row[7];
            String repair = (String) row[8];
            String bonus = (String) row[9];
            SET_BONUS.put(setId, bonus);
            ARMOUR.put(setId, new BUArmorMaterial(setId, durabilityMultiplier, protection,
                    18, () -> SoundEvents.ARMOR_EQUIP_NETHERITE, toughness, knockback,
                    () -> ingredientFor(repair)));
        }
    }


    private static Ingredient ingredientFor(String repairItem) {
        if (repairItem == null || repairItem.isEmpty()) {
            return Ingredient.EMPTY;
        }
        Item item = ForgeRegistries.ITEMS.getValue(
                new net.minecraft.resources.ResourceLocation(BUContent.MODID, repairItem));
        return item == null ? Ingredient.EMPTY : Ingredient.of(item);
    }

    // ------------------------------------------------------------------ //
    //  Registration passes
    // ------------------------------------------------------------------ //

    private static void registerBlockItems() {
        for (String path : BUContent.allBlocks()) {
            // Fluids and portals have no item form: fluids are placed by worldgen
            // and portals only ever exist inside a lit frame.
            if (isFluid(path) || path.endsWith("_portal")) {
                continue;
            }
            RegistryObject<? extends Block> block = BUBlocks.holder(path);
            if (block == null) {
                continue;
            }
            register(path, () -> new BlockItem(block.get(), new Item.Properties()));
        }
    }

    private static boolean isFluid(String path) {
        for (String fluid : BUContent.BLOCKS_FLUID) {
            if (fluid.equals(path)) {
                return true;
            }
        }
        return false;
    }

    private static void registerMaterials() {
        for (String id : BUContent.ITEMS_MATERIALS) {
            register(id, () -> new Item(new Item.Properties()));
        }
    }

    private static void registerTools() {
        for (String id : BUContent.ITEMS_TOOLS) {
            BUTier tier = tierForTool(id);
            if (tier == null) {
                register(id, () -> new Item(new Item.Properties().rarity(Rarity.RARE)));
                continue;
            }
            if (id.endsWith("_sword")) {
                register(id, () -> new SwordItem(tier, 3, -2.4F, toolProps()));
            } else if (id.endsWith("_pickaxe")) {
                register(id, () -> new PickaxeItem(tier, 1, -2.8F, toolProps()));
            } else if (id.endsWith("_axe")) {
                register(id, () -> new AxeItem(tier, 6.0F, -3.1F, toolProps()));
            } else if (id.endsWith("_shovel")) {
                register(id, () -> new ShovelItem(tier, 1.5F, -3.0F, toolProps()));
            } else if (id.endsWith("_hoe")) {
                register(id, () -> new HoeItem(tier, -tier.getLevel(), -1.0F, toolProps()));
            } else if (id.endsWith("_bow")) {
                register(id, () -> new BowItem(toolProps().durability(
                        tier.getUses() * 2).stacksTo(1)));
            } else if (id.endsWith("_shield")) {
                register(id, () -> new ShieldItem(toolProps().durability(
                        tier.getUses() * 3).stacksTo(1)));
            } else {
                register(id, () -> new SwordItem(tier, 3, -2.4F, toolProps()));
            }
        }
        // Boss artefact weapons are unbreakable rarities: they are trophies, not
        // progression gear, so they do not consume a tier.
        for (String id : BUContent.ITEMS_ARTEFACTS) {
            BUTier tier = TIERS.get("starforged");
            if (tier == null) {
                tier = TIERS.values().iterator().next();
            }
            final BUTier artefactTier = tier;
            register(id, () -> new SwordItem(artefactTier, 5, -2.2F,
                    new Item.Properties().rarity(Rarity.EPIC).stacksTo(1)
                            .durability(0)));
        }
    }

    private static Item.Properties toolProps() {
        return new Item.Properties().stacksTo(1);
    }

    /**
     * The tier for a tool id, found by matching its gear-family prefix.
     *
     * Longest prefix wins so a family whose name is a prefix of another (for
     * example a hypothetical "root" and "rootiron") resolves correctly.
     */
    private static BUTier tierForTool(String id) {
        String best = null;
        for (String setId : TIERS.keySet()) {
            if (id.startsWith(setId + "_") && (best == null || setId.length() > best.length())) {
                best = setId;
            }
        }
        return best == null ? null : TIERS.get(best);
    }

    private static void registerArmour() {
        for (String[] row : BUContent.ARMOUR_ITEMS) {
            String id = row[0];
            String setId = row[1];
            String piece = row[2];
            BUArmorMaterial material = ARMOUR.get(setId);
            if (material == null) {
                register(id, () -> new Item(new Item.Properties()));
                continue;
            }
            ArmorItem.Type type = armorTypeFor(piece);
            register(id, () -> new ArmorItem(material, type,
                    new Item.Properties().stacksTo(1)));
        }
    }

    private static ArmorItem.Type armorTypeFor(String piece) {
        switch (piece.toLowerCase(Locale.ROOT)) {
            case "helmet":
                return ArmorItem.Type.HELMET;
            case "chestplate":
                return ArmorItem.Type.CHESTPLATE;
            case "leggings":
                return ArmorItem.Type.LEGGINGS;
            case "boots":
                return ArmorItem.Type.BOOTS;
            default:
                return ArmorItem.Type.CHESTPLATE;
        }
    }

    private static void registerSpawnEggs() {
        for (String[] row : BUContent.SPAWN_EGGS) {
            String eggId = row[0];
            String entityId = row[1];
            Supplier<net.minecraft.world.entity.EntityType<? extends net.minecraft.world.entity.Mob>> type =
                    () -> mobTypeFor(entityId);
            // Egg colours come from the species palette so the egg is visually
            // tied to the creature it spawns, not a generic two-tone template.
            int primary = palettePrimary(entityId);
            int secondary = paletteSecondary(entityId);
            register(eggId, () -> new ForgeSpawnEggItem(type, primary, secondary,
                    new Item.Properties()));
        }
    }

    /**
     * The registered entity type for a spawn egg, narrowed to Mob.
     *
     * Kept as its own method because the wildcard return type cannot be inferred
     * from a lambda target, and because an egg must never be registered for a
     * type that does not exist.
     */
    @SuppressWarnings("unchecked")
    private static net.minecraft.world.entity.EntityType<? extends net.minecraft.world.entity.Mob>
            mobTypeFor(String entityId) {
        net.minecraft.world.entity.EntityType<?> type = BUEntities.entityType(entityId);
        if (type == null) {
            throw new IllegalStateException(
                    "Spawn egg references unregistered entity type: " + entityId);
        }
        return (net.minecraft.world.entity.EntityType<? extends net.minecraft.world.entity.Mob>) type;
    }

    private static int palettePrimary(String entityId) {
        return 0x3C3C5A;
    }

    private static int paletteSecondary(String entityId) {
        return 0xC8A06A;
    }

    private static void registerLoreBooks() {
        for (String id : BUContent.ITEMS_LORE_BOOKS) {
            register(id, () -> new BULoreBookItem(new Item.Properties()
                    .stacksTo(1).rarity(Rarity.UNCOMMON)));
        }
    }

    private static void register(String id, Supplier<Item> supplier) {
        BY_PATH.put(id, ITEMS.register(id, supplier));
    }

    // ------------------------------------------------------------------ //
    //  Accessors
    // ------------------------------------------------------------------ //

    public static Item get(String path) {
        RegistryObject<Item> obj = BY_PATH.get(path);
        return obj == null ? null : obj.get();
    }

    public static RegistryObject<Item> holder(String path) {
        return BY_PATH.get(path);
    }

    public static boolean contains(String path) {
        return BY_PATH.containsKey(path);
    }

    public static java.util.Collection<RegistryObject<Item>> all() {
        return BY_PATH.values();
    }

    public static BUTier tier(String setId) {
        return TIERS.get(setId);
    }

    public static BUArmorMaterial armour(String setId) {
        return ARMOUR.get(setId);
    }

    /** The set bonus id granted by a gear family, or null if it has none. */
    public static String setBonus(String setId) {
        return SET_BONUS.get(setId);
    }

    /**
     * Whether wearing all four pieces of one family grants a bonus.
     *
     * Used by the armour tick handler to apply the family effect only when the
     * set is complete, which is what makes the set bonus a real mechanic rather
     * than a tooltip promise.
     */
    public static String completeSetBonus(net.minecraft.world.entity.LivingEntity wearer) {
        Map<String, Integer> worn = new LinkedHashMap<>();
        for (ItemStack stack : wornArmour(wearer)) {
            if (!(stack.getItem() instanceof ArmorItem)) {
                continue;
            }
            String setId = setIdOf(stack.getItem());
            if (setId != null) {
                worn.merge(setId, 1, Integer::sum);
            }
        }
        for (Map.Entry<String, Integer> entry : worn.entrySet()) {
            if (entry.getValue() >= 4) {
                return SET_BONUS.get(entry.getKey());
            }
        }
        return null;
    }

    private static Iterable<ItemStack> wornArmour(net.minecraft.world.entity.LivingEntity wearer) {
        java.util.List<ItemStack> stacks = new java.util.ArrayList<>();
        for (EquipmentSlot slot : EquipmentSlot.values()) {
            if (slot.getType() == EquipmentSlot.Type.ARMOR) {
                stacks.add(wearer.getItemBySlot(slot));
            }
        }
        return stacks;
    }

    private static String setIdOf(Item item) {
        for (String setId : ARMOUR.keySet()) {
            String path = ForgeRegistries.ITEMS.getKey(item) == null ? ""
                    : ForgeRegistries.ITEMS.getKey(item).getPath();
            if (path.startsWith(setId + "_")) {
                return setId;
            }
        }
        return null;
    }
}
