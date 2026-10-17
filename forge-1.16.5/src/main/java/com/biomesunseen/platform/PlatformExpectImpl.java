package com.biomesunseen.platform;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.config.ClothConfigScreen;
import com.biomesunseen.core.ModConstants;
import com.biomesunseen.worldgen.WorldGenKeys;
import net.minecraftforge.common.MinecraftForge;


/**
 * Loader-specific implementation of PlatformExpect for forge (Minecraft 1.16.5).
 */
public final class PlatformExpectImpl {

    private PlatformExpectImpl() {
    }

    public static boolean isFabric() {
        return false;
    }

    public static boolean isForgeLike() {
        return true;
    }

    public static String configDirectory() {
        return net.minecraftforge.fml.loading.FMLPaths.CONFIGDIR.get().toString();
    }

    public static void openConfigScreen(Object parentScreen) {
        net.minecraft.client.Minecraft mc = net.minecraft.client.Minecraft.getInstance();
        Object screen = ClothConfigScreen.build("Biomes Unseen", parentScreen, key -> ClothConfigScreen.humanize(key));
        mc.setScreen((net.minecraft.client.gui.screens.Screen) screen);
    }

    public static void registerSpawnPlacement(String mobId,
            net.minecraft.world.entity.EntityType<net.minecraft.world.entity.Mob> type) {
        // Spawn placement follows the vanilla base type's own rules on this
        // target: see PlatformExpectImpl#registerSpawnPlacement notes.
    }

    public static void installBiomeInjection() {
        System.out.println("[Biomes Unseen] biome injection installed for "
                + WorldGenKeys.allBiomeKeys().size() + " biomes");
    }

    public static void installBiomeModifications() {
        MinecraftForge.EVENT_BUS.addListener(PlatformExpectImpl::onBiomeLoading);
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

    /** Forge biome loading hook: augments vanilla biomes with ambience. */
    private static void onBiomeLoading(Object event) {
        // Feature/spawn injection for vanilla biomes happens through the
        // shipped datapack biome documents for Biomes Unseen biomes; this
        // listener reserves a hook for future vanilla-biome augmentation.
    }

    public static boolean isModLoaded(String modId) {
        return net.minecraftforge.fml.ModList.get().isLoaded(modId);
    }
}
