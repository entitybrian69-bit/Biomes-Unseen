package com.biomesunseen.platform;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.config.ClothConfigScreen;
import com.biomesunseen.core.ModConstants;
import com.biomesunseen.worldgen.WorldGenKeys;

/**
 * Loader-specific implementation of PlatformExpect for fabric (Minecraft 1.19.1).
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
        net.minecraft.client.Minecraft mc = net.minecraft.client.Minecraft.getInstance();
        Object screen = ClothConfigScreen.build("Biomes Unseen", parentScreen,
                key -> key);
        mc.setScreen((net.minecraft.client.gui.screens.Screen) screen);
    }

    public static void registerSpawnPlacement(String mobId,
            net.minecraft.world.entity.EntityType<net.minecraft.world.entity.Mob> type) {
        net.fabricmc.fabric.api.entity.event.v1.SpawnRestriction.register(
                type,
                net.fabricmc.fabric.api.entity.event.v1.SpawnRestriction.Type.ON_GROUND,
                net.minecraft.world.level.levelgen.Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                (entityType, level, spawnType, pos, random) -> true);
    }

    public static void installBiomeInjection() {
        // Modern lines: the shipped datapack overrides
        // multi_noise_biome_source_parameter_list/overworld.json which inserts
        // every Biomes Unseen biome into the overworld climate system.
        // Legacy lines: the BiomeProvider mixin performs insertion.
        System.out.println("[Biomes Unseen] biome injection installed for "
                + WorldGenKeys.allBiomeKeys().size() + " biomes");
    }

    public static void installBiomeModifications() {
        net.fabricmc.fabric.api.biome.v1.BiomeModifications.addSpawn(
                net.fabricmc.fabric.api.biome.v1.BiomeSelectors.foundInOverworld(),
                net.minecraft.world.entity.MobCategory.CREATURE,
                com.biomesunseen.registry.ModEntities.MOB_TYPES.get("lumox").get(), 12, 2, 4);
    }

    public static void playBossMusic(net.minecraft.server.level.ServerLevel level,
            net.minecraft.core.BlockPos center, String soundEventId, int radius) {
        net.minecraft.sounds.SoundEvent sound = com.biomesunseen.registry.ModSounds.byId(soundEventId);
        if (sound == null) {
            return;
        }
        for (net.minecraft.world.entity.player.Player player :
                level.getPlayers(p -> p.distanceToSqr(center.getX(), center.getY(), center.getZ()) < radius * radius)) {
            player.playNotifySound(sound, net.minecraft.sounds.SoundSource.MUSIC, 1.0F, 1.0F);
        }
    }

    public static boolean isModLoaded(String modId) {
        return net.fabricmc.loader.api.FabricLoader.getInstance().isModLoaded(modId);
    }
}
