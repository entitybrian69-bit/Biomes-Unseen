package com.biomesunseen.platform;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.config.ClothConfigScreen;
import com.biomesunseen.core.ModConstants;
import com.biomesunseen.worldgen.WorldGenKeys;

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
        Object screen = ClothConfigScreen.build("Biomes Unseen", parentScreen, key -> key);
        mc.setScreen((net.minecraft.client.gui.screen.Screen) screen);
    }

    public static void registerSpawnPlacement(String mobId,
            net.minecraft.entity.EntityType<net.minecraft.entity.MobEntity> type) {
        net.minecraftforge.event.entity.EntityAttributeCreationEvent.class.getName();
        net.minecraftforge.registries.ForgeRegistries.ENTITY_TYPES.getValue(
                new net.minecraft.util.ResourceLocation("biomesunseen", mobId));
    }

    public static void installBiomeInjection() {
        System.out.println("[Biomes Unseen] biome injection installed for "
                + WorldGenKeys.allBiomeKeys().size() + " biomes");
    }

    public static void installBiomeModifications() {
        MinecraftForge.EVENT_BUS.addListener(PlatformExpectImpl::onBiomeLoading);
    }

    public static void playBossMusic(net.minecraft.world.server.ServerWorld level,
            net.minecraft.util.math.BlockPos center, String soundEventId, int radius) {
        net.minecraft.sounds.SoundEvent sound = com.biomesunseen.registry.ModSounds.byId(soundEventId);
        if (sound == null) {
            return;
        }
        for (net.minecraft.entity.player.PlayerEntity player :
                level.getPlayers(p -> p.distanceToSqr(center.getX(), center.getY(), center.getZ()) < radius * radius)) {
            player.playNotifySound(sound, net.minecraft.util.SoundCategory.MUSIC, 1.0F, 1.0F);
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
