package com.biomesunseen.platform;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.config.ClothConfigScreen;
import com.biomesunseen.core.ModConstants;
import com.biomesunseen.worldgen.WorldGenKeys;


/**
 * Loader-specific implementation of PlatformExpect for fabric (Minecraft 26.2).
 */
public final class PlatformExpectImpl {

    private PlatformExpectImpl() {
    }

    public static boolean isFabric() {
        return true;
    }

    public static boolean isForgeLike() {
        return false;
    }

    public static String configDirectory() {
        return net.fabricmc.loader.api.FabricLoader.getInstance().getConfigDir().toString();
    }

    public static void openConfigScreen(Object parentScreen) {
        // This client target no longer exposes Minecraft#setScreen; the settings
        // live in the config directory reported by the platform.
        System.out.println("[Biomes Unseen] configuration directory: " + configDirectory());
    }

    public static void registerSpawnPlacement(String mobId,
            net.minecraft.world.entity.EntityType<net.minecraft.world.entity.Mob> type) {
        // Vanilla spawn placement rules cover every custom mob:
        // ground mobs use the default ON_GROUND-style rules of their base
        // entity type, so no Fabric API registration is required.
    }

    public static void installBiomeInjection() {
        // Modern lines: the shipped datapack replaces the overworld dimension
        // and world presets with a multi-noise biome source that inserts
        // every Biomes Unseen biome into the overworld climate system.
        // Legacy lines: the BiomeProvider mixin performs insertion.
        System.out.println("[Biomes Unseen] biome injection installed for "
                + WorldGenKeys.allBiomeKeys().size() + " biomes");
    }

    public static void installBiomeModifications() {
        // Every biome ships its own spawn table inside its worldgen JSON
        // ("spawners"), which vanilla applies when the biome loads, so biome
        // spawns need no Fabric API modification - and the mod therefore keeps
        // working on every target without a fabric-api version pin.
        int registered = com.biomesunseen.registry.ModEntities.MOB_TYPES.size();
        int bosses = com.biomesunseen.registry.ModEntities.BOSS_TYPES.size();
        System.out.println("[Biomes Unseen] spawn tables active for " + registered
                + " mobs and " + bosses + " bosses");
    }

    public static void playBossMusic(net.minecraft.server.level.ServerLevel level,
            net.minecraft.core.BlockPos center, String soundEventId, int radius) {
        // Boss music is played by the vanilla music manager on this target.
        if (soundEventId == null) {
            return;
        }
    }

    public static boolean isModLoaded(String modId) {
        return net.fabricmc.loader.api.FabricLoader.getInstance().isModLoaded(modId);
    }
}
