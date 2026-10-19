package com.biomesunseen.init;

import com.biomesunseen.block.BUFluidType;
import com.biomesunseen.block.BUFloraBlock;
import com.biomesunseen.block.BUPortalBlock;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.LiquidBlock;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.FlowingFluid;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fluids.ForgeFlowingFluid;
import net.minecraftforge.fluids.FluidType;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Supplier;

/**
 * Every block the mod adds, registered from the generated {@link BUContent}
 * table.
 *
 * The registration is data-driven rather than 264 hand-written fields: each
 * kind of block has one {@link BlockBehaviour.Properties} recipe here, and the
 * id list comes from the same content table that produced the textures, the
 * blockstates and the loot tables. That is what keeps a newly authored ore or
 * biome surface material from needing a code change to appear in game.
 */
public final class BUBlocks {

    public static final DeferredRegister<Block> BLOCKS =
            DeferredRegister.create(ForgeRegistries.BLOCKS, BUContent.MODID);
    public static final DeferredRegister<FluidType> FLUID_TYPES =
            DeferredRegister.create(ForgeRegistries.Keys.FLUID_TYPES, BUContent.MODID);
    public static final DeferredRegister<net.minecraft.world.level.material.Fluid> FLUIDS =
            DeferredRegister.create(ForgeRegistries.FLUIDS, BUContent.MODID);

    /** Registered blocks by registry path, for lookup from items and features. */
    private static final Map<String, RegistryObject<? extends Block>> BY_PATH = new LinkedHashMap<>();
    /** Fluid plumbing, keyed by block registry path. */
    private static final Map<String, FluidSet> FLUID_SETS = new LinkedHashMap<>();

    /**
     * The source/flowing/block/trio Forge needs for a real liquid.
     *
     * A {@link ForgeFlowingFluid} is not one object: it is a still fluid, a
     * flowing fluid, a {@link FluidType} and a {@link LiquidBlock}, all wired
     * to each other. Registering only the block would give a solid cube that
     * happens to be called water.
     */
    private static final class FluidSet {
        private RegistryObject<FluidType> type;
        private RegistryObject<ForgeFlowingFluid.Source> source;
        private RegistryObject<ForgeFlowingFluid.Flowing> flowing;
        private RegistryObject<LiquidBlock> block;
    }

    private BUBlocks() {
    }

    public static void register(IEventBus bus) {
        registerSolids();
        registerFluids();
        FLUID_TYPES.register(bus);
        FLUIDS.register(bus);
        BLOCKS.register(bus);
    }

    // ------------------------------------------------------------------ //
    //  Solids
    // ------------------------------------------------------------------ //

    private static void registerSolids() {
        for (String id : BUContent.BLOCKS_CUBE) {
            register(id, () -> new Block(stoneProps(id)));
        }
        for (String id : BUContent.BLOCKS_GRASS) {
            register(id, () -> new Block(grassProps(id)));
        }
        for (String id : BUContent.BLOCKS_LOG) {
            register(id, () -> new RotatedPillarBlock(logProps(id)));
        }
        for (String id : BUContent.BLOCKS_ALTAR) {
            register(id, () -> new RotatedPillarBlock(altarProps()));
        }
        for (String id : BUContent.BLOCKS_ORE) {
            register(id, () -> new Block(oreProps(id)));
        }
        for (String id : BUContent.BLOCKS_MINERAL) {
            register(id, () -> new Block(mineralProps(id)));
        }
        for (String id : BUContent.BLOCKS_FLORA) {
            // Flora must not collide and must break instantly, or a field of
            // authored plants becomes an invisible wall.
            register(id, () -> new BUFloraBlock(
                    BlockBehaviour.Properties.of()
                            .mapColor(MapColor.PLANT)
                            .noCollission()
                            .instabreak()
                            .sound(SoundType.GRASS)
                            .offsetType(BlockBehaviour.OffsetType.XZ)
                            .pushReaction(PushReaction.DESTROY)));
        }
        for (String id : BUContent.BLOCKS_LANTERN) {
            register(id, () -> new Block(lanternProps()));
        }
        for (String id : BUContent.BLOCKS_PORTAL) {
            register(id, () -> new BUPortalBlock(portalProps(), destinationFor(id)));
        }
    }

    private static void register(String id, Supplier<Block> supplier) {
        BY_PATH.put(id, BLOCKS.register(id, supplier));
    }

    /**
     * Which dimension a portal block leads to.
     *
     * Derived from the block id so the block, its level stem and its dimension
     * type JSON cannot disagree: {@code hollow_deep_portal} opens onto
     * {@code hollow_deep}.
     */
    private static String destinationFor(String portalBlockId) {
        if (portalBlockId.endsWith("_portal")) {
            return portalBlockId.substring(0, portalBlockId.length() - "_portal".length());
        }
        return portalBlockId;
    }

    // ------------------------------------------------------------------ //
    //  Fluids
    // ------------------------------------------------------------------ //

    private static void registerFluids() {
        for (String id : BUContent.BLOCKS_FLUID) {
            FluidSet set = new FluidSet();
            FLUID_SETS.put(id, set);

            int tint = tintFor(id);
            set.type = FLUID_TYPES.register(id, () -> new BUFluidType(
                    FluidType.Properties.create()
                            .density(1100)
                            .viscosity(1200)
                            .lightLevel(6)
                            .motionScale(0.014D),
                    id, tint));

            ForgeFlowingFluid.Properties props = new ForgeFlowingFluid.Properties(
                    () -> set.type.get(),
                    () -> set.source.get(),
                    () -> set.flowing.get())
                    .slopeFindDistance(3)
                    .levelDecreasePerBlock(2)
                    .explosionResistance(100.0F);

            set.block = BLOCKS.register(id, () -> new LiquidBlock(
                    () -> set.source.get(),
                    BlockBehaviour.Properties.of()
                            .mapColor(tintColor(tint))
                            .noCollission()
                            .strength(100.0F)
                            .lightLevel(state -> 6)
                            .pushReaction(PushReaction.DESTROY)
                            .noLootTable()
                            .liquid()));
            props.block(() -> set.block.get());

            set.source = FLUIDS.register(id,
                    () -> new ForgeFlowingFluid.Source(props));
            set.flowing = FLUIDS.register(id + "_flowing",
                    () -> new ForgeFlowingFluid.Flowing(props));

            BY_PATH.put(id, set.block);
        }
    }

    /** Authored tint per liquid, matching the palette its texture was built from. */
    private static int tintFor(String id) {
        switch (id) {
            case "hollow_water":
                return 0xFF6FE3C4;
            case "lumen_water":
                return 0xFFC8F5A0;
            case "void_fluid":
                return 0xFF8C5CD8;
            case "aether_essence":
                return 0xFFFFE9A8;
            default:
                return 0xFFFFFFFF;
        }
    }

    private static MapColor tintColor(int tint) {
        // The map colour only affects the overview map; the fluid renders with
        // its own authored texture and tint.
        int green = (tint >> 8) & 0xFF;
        return green > 0xC0 ? MapColor.PLANT : MapColor.COLOR_PURPLE;
    }

    // ------------------------------------------------------------------ //
    //  Properties
    // ------------------------------------------------------------------ //

    private static BlockBehaviour.Properties stoneProps(String id) {
        return BlockBehaviour.Properties.of()
                .mapColor(MapColor.STONE)
                .strength(1.6F, 6.0F)
                .requiresCorrectToolForDrops()
                .sound(SoundType.STONE);
    }

    private static BlockBehaviour.Properties grassProps(String id) {
        return BlockBehaviour.Properties.of()
                .mapColor(MapColor.GRASS)
                .strength(0.7F, 2.0F)
                .sound(SoundType.GRASS);
    }

    private static BlockBehaviour.Properties logProps(String id) {
        return BlockBehaviour.Properties.of()
                .mapColor(MapColor.WOOD)
                .strength(2.0F, 4.0F)
                .sound(SoundType.WOOD);
    }

    private static BlockBehaviour.Properties altarProps() {
        return BlockBehaviour.Properties.of()
                .mapColor(MapColor.QUARTZ)
                .strength(3.5F, 12.0F)
                .requiresCorrectToolForDrops()
                .lightLevel(state -> 7)
                .sound(SoundType.DEEPSLATE);
    }

    private static BlockBehaviour.Properties oreProps(String id) {
        // Dimension ores are harder than Overworld ones: they are meant to need
        // the matching tier, which the needs_x_tool tags also encode.
        boolean dimension = id.endsWith("_ore") && isDimensionOre(id);
        return BlockBehaviour.Properties.of()
                .mapColor(dimension ? MapColor.DEEPSLATE : MapColor.STONE)
                .strength(dimension ? 4.5F : 3.0F, dimension ? 9.0F : 6.0F)
                .requiresCorrectToolForDrops()
                .sound(dimension ? SoundType.DEEPSLATE : SoundType.STONE);
    }

    private static boolean isDimensionOre(String id) {
        for (Object[] row : BUContent.ORE_GEN) {
            if (id.equals(row[0])) {
                String dimension = (String) row[6];
                return !"overworld".equals(dimension);
            }
        }
        return false;
    }

    private static BlockBehaviour.Properties mineralProps(String id) {
        return BlockBehaviour.Properties.of()
                .mapColor(MapColor.METAL)
                .strength(5.0F, 12.0F)
                .requiresCorrectToolForDrops()
                .sound(SoundType.METAL);
    }

    private static BlockBehaviour.Properties lanternProps() {
        return BlockBehaviour.Properties.of()
                .mapColor(MapColor.COLOR_YELLOW)
                .strength(1.2F, 3.0F)
                .lightLevel(state -> 15)
                .sound(SoundType.LANTERN);
    }

    private static BlockBehaviour.Properties portalProps() {
        return BlockBehaviour.Properties.of()
                .mapColor(MapColor.COLOR_LIGHT_BLUE)
                .noCollission()
                .instabreak()
                .lightLevel(state -> 11)
                .pushReaction(PushReaction.BLOCK)
                .sound(SoundType.GLASS);
    }

    // ------------------------------------------------------------------ //
    //  Accessors
    // ------------------------------------------------------------------ //

    /** The registered block for a path, or null if the mod does not add it. */
    public static Block get(String path) {
        RegistryObject<? extends Block> obj = BY_PATH.get(path);
        return obj == null ? null : obj.get();
    }

    public static RegistryObject<? extends Block> holder(String path) {
        return BY_PATH.get(path);
    }

    public static boolean contains(String path) {
        return BY_PATH.containsKey(path);
    }

    /** Every registered block, in content-table order. */
    public static java.util.Collection<RegistryObject<? extends Block>> all() {
        return BY_PATH.values();
    }

    /** The still fluid for a liquid block, or null for non-fluids. */
    public static RegistryObject<ForgeFlowingFluid.Source> source(String path) {
        FluidSet set = FLUID_SETS.get(path);
        return set == null ? null : set.source;
    }

    /** The fluid type for a liquid block, or null for non-fluids. */
    public static RegistryObject<FluidType> fluidType(String path) {
        FluidSet set = FLUID_SETS.get(path);
        return set == null ? null : set.type;
    }
}
