package com.biomesunseen.registry;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.spec.OreSpec;
import com.biomesunseen.spec.Specs;
import net.minecraft.util.valueproviders.UniformInt;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.DropExperienceBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

import java.util.LinkedHashMap;
import java.util.Map;

public final class ModBlocks {
    public static final DeferredRegister<Block> BLOCKS =
            DeferredRegister.create(ForgeRegistries.BLOCKS, BiomesUnseen.MOD_ID);

    public static final RegistryObject<Block> HOLLOWITE_ORE = BLOCKS.register("hollowite_ore",
            () -> new DropExperienceBlock(
                    BlockBehaviour.Properties.copy(Blocks.DEEPSLATE_IRON_ORE)
                            .mapColor(MapColor.COLOR_CYAN)
                            .strength(4.0F, 6.0F)
                            .requiresCorrectToolForDrops(),
                    UniformInt.of(2, 5)));

    /** Generated ore blocks from specs/ores.json, keyed by ore id. */
    public static final Map<String, RegistryObject<Block>> ORES = new LinkedHashMap<>();

    static {
        for (OreSpec spec : Specs.ores()) {
            ORES.put(spec.id(), BLOCKS.register(spec.blockId(), () -> oreBlock(spec)));
        }
    }

    private static Block oreBlock(OreSpec spec) {
        BlockBehaviour.Properties props = BlockBehaviour.Properties.copy(Blocks.DEEPSLATE_IRON_ORE)
                .mapColor(MapColor.STONE)
                .strength(spec.hardness(), spec.hardness() + 2.0F)
                .requiresCorrectToolForDrops();
        if (spec.light() > 0) {
            props = props.lightLevel(state -> spec.light());
        }
        return new DropExperienceBlock(props, UniformInt.of(spec.xpMin(), spec.xpMax()));
    }

    private ModBlocks() {
    }

    public static void register(IEventBus bus) {
        BLOCKS.register(bus);
    }
}
