package com.biomesunseen.event;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.block.HollowPortalBlock;
import com.biomesunseen.registry.ModBlocks;
import com.biomesunseen.registry.ModItems;
import com.biomesunseen.worldgen.ModDimensions;
import com.mojang.authlib.GameProfile;
import net.minecraft.core.BlockPos;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraftforge.common.util.FakePlayer;
import net.minecraftforge.common.util.FakePlayerFactory;
import net.minecraftforge.event.server.ServerStartedEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

import java.nio.charset.StandardCharsets;
import java.util.UUID;

/** Optional server-side gameplay smoke test, enabled only by the CI JVM property. */
@Mod.EventBusSubscriber(modid = BiomesUnseen.MOD_ID, bus = Mod.EventBusSubscriber.Bus.FORGE)
public final class HollowTravelSmokeTest {
    private static final String OVERWORLD_PORTAL_KEY = "BiomesUnseenOverworldPortal";
    private static final BlockPos HOLLOW_RETURN_PORTAL = new BlockPos(0, 100, 2);
    private static final int[][] EXIT_DIRECTIONS = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

    private HollowTravelSmokeTest() {
    }

    @SubscribeEvent
    public static void onServerStarted(ServerStartedEvent event) {
        if (!Boolean.getBoolean("biomesunseen.smokeTravel")) {
            return;
        }

        MinecraftServer server = event.getServer();
        ServerLevel overworld = server.getLevel(Level.OVERWORLD);
        ServerLevel hollow = server.getLevel(ModDimensions.HOLLOW_DEEP_LEVEL);
        require(overworld != null, "Overworld was not loaded");
        require(hollow != null, "Hollow Deep was not loaded");

        testPortalRoundTrip(overworld, hollow);
        testSigilRoundTrip(overworld, hollow);
        BiomesUnseen.LOGGER.info("Hollow travel smoke passed: portal round trip and sigil round trip");
    }

    private static void testPortalRoundTrip(ServerLevel overworld, ServerLevel hollow) {
        PortalSite site = findPortalSite(overworld);
        HollowPortalBlock portal = (HollowPortalBlock) ModBlocks.HOLLOW_PORTAL.get();
        overworld.setBlockAndUpdate(site.portal(), ModBlocks.HOLLOW_PORTAL.get().defaultBlockState());

        FakePlayer outbound = fakePlayer(overworld, "BUTravelOut");
        outbound.setPos(site.portal().getX() + 0.5D, site.portal().getY(), site.portal().getZ() + 0.5D);
        portal.entityInside(overworld.getBlockState(site.portal()), overworld, site.portal(), outbound);
        require(outbound.level() == hollow, "Walking into the portal did not transfer the player to Hollow Deep");
        require(outbound.blockPosition().equals(new BlockPos(0, 100, 0)),
                "Portal arrival did not use the prepared Hollow Deep landing");
        require(hollow.getBlockState(HOLLOW_RETURN_PORTAL).is(ModBlocks.HOLLOW_PORTAL.get()),
                "Hollow Deep landing did not create the return portal");
        int[] storedPortal = outbound.getPersistentData().getIntArray(OVERWORLD_PORTAL_KEY);
        require(storedPortal.length == 3 && storedPortal[0] == site.portal().getX()
                        && storedPortal[1] == site.portal().getY() && storedPortal[2] == site.portal().getZ(),
                "The source portal position was not saved on the traveler");

        FakePlayer returning = fakePlayer(hollow, "BUTravelBack");
        returning.getPersistentData().merge(outbound.getPersistentData());
        returning.setPos(HOLLOW_RETURN_PORTAL.getX() + 0.5D, HOLLOW_RETURN_PORTAL.getY(),
                HOLLOW_RETURN_PORTAL.getZ() + 0.5D);
        portal.entityInside(hollow.getBlockState(HOLLOW_RETURN_PORTAL), hollow, HOLLOW_RETURN_PORTAL, returning);
        require(returning.level() == overworld, "Walking into the return gate did not return to the Overworld");
        require(returning.blockPosition().equals(site.expectedExit()),
                "The return gate did not place the player beside the original portal");
        require(!returning.getPersistentData().contains(OVERWORLD_PORTAL_KEY),
                "The consumed source portal position was not cleared after returning");

        overworld.setBlockAndUpdate(site.portal(), Blocks.AIR.defaultBlockState());
    }

    private static void testSigilRoundTrip(ServerLevel overworld, ServerLevel hollow) {
        FakePlayer outbound = fakePlayer(overworld, "BUSigilOut");
        outbound.setItemInHand(InteractionHand.MAIN_HAND, ModItems.HOLLOW_SIGIL.get().getDefaultInstance());
        ModItems.HOLLOW_SIGIL.get().use(overworld, outbound, InteractionHand.MAIN_HAND);
        require(outbound.level() == hollow, "Using the Hollow Sigil did not transfer the player to Hollow Deep");

        FakePlayer returning = fakePlayer(hollow, "BUSigilBack");
        returning.setItemInHand(InteractionHand.MAIN_HAND, ModItems.HOLLOW_SIGIL.get().getDefaultInstance());
        ModItems.HOLLOW_SIGIL.get().use(hollow, returning, InteractionHand.MAIN_HAND);
        require(returning.level() == overworld, "Using the Hollow Sigil in Hollow Deep did not return to the Overworld");
    }

    private static FakePlayer fakePlayer(ServerLevel level, String profileName) {
        UUID id = UUID.nameUUIDFromBytes(profileName.getBytes(StandardCharsets.UTF_8));
        return FakePlayerFactory.get(level, new GameProfile(id, profileName));
    }

    private static PortalSite findPortalSite(ServerLevel level) {
        BlockPos spawn = level.getSharedSpawnPos();
        for (int radius = 2; radius <= 96; radius++) {
            for (int dx = -radius; dx <= radius; dx++) {
                for (int dz = -radius; dz <= radius; dz++) {
                    if (Math.max(Math.abs(dx), Math.abs(dz)) != radius) {
                        continue;
                    }
                    int x = spawn.getX() + dx;
                    int z = spawn.getZ() + dz;
                    int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z);
                    BlockPos portal = new BlockPos(x, y, z);
                    if (!level.getBlockState(portal.below()).blocksMotion()
                            || !level.getBlockState(portal).isAir()
                            || !level.getBlockState(portal.above()).isAir()) {
                        continue;
                    }
                    BlockPos exit = findSafeExit(level, portal);
                    if (exit != null) {
                        return new PortalSite(portal, exit);
                    }
                }
            }
        }
        throw new IllegalStateException("Could not find a safe Overworld site for the portal travel smoke test");
    }

    private static BlockPos findSafeExit(ServerLevel level, BlockPos portal) {
        for (int[] direction : EXIT_DIRECTIONS) {
            BlockPos feet = portal.offset(direction[0], 0, direction[1]);
            if (level.getBlockState(feet.below()).blocksMotion()
                    && !level.getBlockState(feet).blocksMotion()
                    && !level.getBlockState(feet.above()).blocksMotion()) {
                return feet;
            }
        }
        return null;
    }

    private static void require(boolean condition, String message) {
        if (!condition) {
            throw new IllegalStateException("Hollow travel smoke failed: " + message);
        }
    }

    private record PortalSite(BlockPos portal, BlockPos expectedExit) {
    }
}
