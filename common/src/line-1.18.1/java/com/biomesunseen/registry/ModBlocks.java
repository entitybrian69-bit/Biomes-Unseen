package com.biomesunseen.registry;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;

import com.biomesunseen.block.UnseenDecorBlock;
import com.biomesunseen.block.UnseenOreBlock;
import com.biomesunseen.block.UnseenPlantBlock;
import com.biomesunseen.core.Content;
import com.biomesunseen.core.DecorDef;
import com.biomesunseen.core.OreDef;
import com.biomesunseen.core.PlantDef;

import me.shedaniel.architectury.registry.RegistrySupplier;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * All 42 blocks: 20 ores, 12 palette blocks and
           10 plants.
 */
public final class ModBlocks {

    /** ore id (e.g. "azurethril") -> "<id>_ore" block */
    public static final Map<String, RegistrySupplier<Block>> ORES =
            new LinkedHashMap<String, RegistrySupplier<Block>>();
    /** decor id -> block */
    public static final Map<String, RegistrySupplier<Block>> DECOR =
            new LinkedHashMap<String, RegistrySupplier<Block>>();
    /** plant id -> block */
    public static final Map<String, RegistrySupplier<Block>> PLANTS =
            new LinkedHashMap<String, RegistrySupplier<Block>>();

    static {
        for (int i = 0; i < Content.ORES.size(); i++) {
            OreDef ore = Content.ORES.get(i);
            ORES.put(ore.id, ModRegistry.BLOCK_REGISTRYS.register(ore.id + "_ore",
                    () -> new UnseenOreBlock(ore)));
        }
        for (int i = 0; i < Content.DECOR.size(); i++) {
            DecorDef decor = Content.DECOR.get(i);
            DECOR.put(decor.id, ModRegistry.BLOCK_REGISTRYS.register(decor.id,
                    () -> new UnseenDecorBlock(decor)));
        }
        for (int i = 0; i < Content.PLANTS.size(); i++) {
            PlantDef plant = Content.PLANTS.get(i);
            PLANTS.put(plant.id, ModRegistry.BLOCK_REGISTRYS.register(plant.id,
                    () -> new UnseenPlantBlock(plant)));
        }
    }

    private ModBlocks() {
    }

    /** Triggers static initialization (called by ModRegistries). */
    public static void registerContent() {
        // Static initializers populate the maps above.
    }

    public static RegistrySupplier<Block> oreBlock(String oreId) {
        return ORES.get(oreId);
    }

    public static Map<String, RegistrySupplier<Block>> allOres() {
        return Collections.unmodifiableMap(ORES);
    }

    public static Map<String, RegistrySupplier<Block>> allDecor() {
        return Collections.unmodifiableMap(DECOR);
    }

    public static Map<String, RegistrySupplier<Block>> allPlants() {
        return Collections.unmodifiableMap(PLANTS);
    }
}
