package com.biomesunseen.event;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.registry.ModBlocks;
import com.biomesunseen.registry.ModItems;
import com.biomesunseen.registry.ModSounds;
import com.biomesunseen.spec.Specs;
import com.biomesunseen.worldgen.ModDimensions;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureSet;
import net.minecraftforge.event.server.ServerStartedEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/** Logs what actually loaded from the world's dynamic registries at server startup. */
@Mod.EventBusSubscriber(modid = BiomesUnseen.MOD_ID, bus = Mod.EventBusSubscriber.Bus.FORGE)
public final class WorldgenAudit {
    private static final int EXPECTED_STRUCTURES = 115;
    private static final int EXPECTED_STRUCTURE_SETS = 23;

    private WorldgenAudit() {
    }

    @SubscribeEvent
    public static void onServerStarted(ServerStartedEvent event) {
        Registry<Biome> biomes = event.getServer().registryAccess().registryOrThrow(Registries.BIOME);
        Registry<Structure> structures = event.getServer().registryAccess().registryOrThrow(Registries.STRUCTURE);
        Registry<StructureSet> structureSets =
                event.getServer().registryAccess().registryOrThrow(Registries.STRUCTURE_SET);
        long biomeCount = countModEntries(biomes);
        long structureCount = countModEntries(structures);
        long structureSetCount = countModEntries(structureSets);
        int expectedBiomes = Specs.overworld().size() + Specs.dimensionBiomes().size();
        boolean dimensionLoaded = event.getServer().getLevel(ModDimensions.HOLLOW_DEEP_LEVEL) != null;
        boolean portalRegistered = ModBlocks.HOLLOW_PORTAL.isPresent()
                && ModItems.HOLLOW_PORTAL.isPresent() && ModSounds.HOLLOW_GATE_TRAVEL.isPresent();
        boolean weaponsRegistered = ModItems.HOLLOWITE_SWORD.isPresent()
                && ModItems.HOLLOWITE_BATTLEAXE.isPresent()
                && ModItems.ORE_SWORDS.size() == Specs.ores().size()
                && ModItems.ORE_SWORDS.values().stream().allMatch(item -> item.isPresent());
        boolean guideAndSigilRegistered = ModItems.FIELD_GUIDE.isPresent() && ModItems.HOLLOW_SIGIL.isPresent();
        boolean recipesLoaded = hasRecipe(event, "hollow_portal") && hasRecipe(event, "hollow_sigil")
                && hasRecipe(event, "field_guide") && hasRecipe(event, "hollowite_sword")
                && hasRecipe(event, "hollowite_battleaxe")
                && hasRecipe(event, Specs.ores().get(0).id() + "_sword");
        if (biomeCount < expectedBiomes || structureCount < EXPECTED_STRUCTURES
                || structureSetCount < EXPECTED_STRUCTURE_SETS || !dimensionLoaded
                || !portalRegistered || !weaponsRegistered || !guideAndSigilRegistered || !recipesLoaded) {
            BiomesUnseen.LOGGER.error("Worldgen/gameplay check FAILED: loaded {}/{} biomes, {}/{} structures, "
                            + "{}/{} structure sets; Hollow Deep loaded={}, portal registered={}, weapons registered={}, "
                            + "guide/sigil registered={}, core recipes loaded={}", biomeCount, expectedBiomes,
                    structureCount, EXPECTED_STRUCTURES, structureSetCount, EXPECTED_STRUCTURE_SETS,
                    dimensionLoaded, portalRegistered, weaponsRegistered, guideAndSigilRegistered, recipesLoaded);
            return;
        }
        BiomesUnseen.LOGGER.info("Biomes Unseen worldgen ready: {} biomes, {} structures, {} structure sets; "
                        + "Hollow Deep, portal, guide, sigil, weapon items and core recipes loaded",
                biomeCount, structureCount, structureSetCount);
    }

    private static boolean hasRecipe(ServerStartedEvent event, String path) {
        return event.getServer().getRecipeManager()
                .byKey(new ResourceLocation(BiomesUnseen.MOD_ID, path)).isPresent();
    }

    private static long countModEntries(Registry<?> registry) {
        return registry.keySet().stream().filter(WorldgenAudit::isModEntry).count();
    }

    private static boolean isModEntry(ResourceLocation id) {
        return BiomesUnseen.MOD_ID.equals(id.getNamespace());
    }
}
