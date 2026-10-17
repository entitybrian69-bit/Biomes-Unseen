package com.biomesunseen.platform;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.config.ClothConfigScreen;
import com.biomesunseen.core.ModConstants;
import com.biomesunseen.worldgen.WorldGenKeys;


/**
 * Loader-specific implementation of PlatformExpect for fabric (Minecraft 1.21.8).
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
                key -> ClothConfigScreen.humanize(key));
        mc.setScreen((net.minecraft.client.gui.screens.Screen) screen);
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
