package com.biomesunseen.init;

import com.biomesunseen.BiomesUnseen;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.dimension.DimensionType;
import net.minecraft.world.phys.Vec3;

/**
 * Dimension and level-stem keys.
 *
 * Like biomes, dimensions are data-driven in 1.20.1: the type lives at
 * {@code data/biomesunseen/dimension_type/<id>.json} and the stem at
 * {@code data/biomesunseen/dimension/<id>.json}. This class holds the keys the
 * portal blocks and the chunk-generator hooks point at, and owns the shared
 * "find somewhere safe to arrive" logic every portal needs.
 *
 * Three dimensions are added:
 * <ul>
 *   <li><b>hollow_deep</b> -- the AAA dimension: its own type, noise settings,
 *       fog colour, sky renderer, ambience and 20+ biomes.</li>
 *   <li><b>aetherfall</b> -- floating islands above the cloud layer.</li>
 *   <li><b>void_between</b> -- the fractured space the Unraveling lives in.</li>
 * </ul>
 */
public final class BUDimensions {

    public static final String HOLLOW_DEEP = "hollow_deep";
    public static final String AETHERFALL = "aetherfall";
    public static final String VOID_BETWEEN = "void_between";

    private BUDimensions() {
    }

    /** Build nothing eagerly: keys are pure values, so this only validates. */
    public static void init() {
        for (String dimension : BUContent.DIMENSIONS) {
            if (!dimension.equals("overworld") && !dimension.equals("the_nether")
                    && !dimension.equals("the_end")) {
                BiomesUnseen.LOGGER.debug("Biomes Unseen dimension registered: {}", dimension);
            }
        }
    }

    /** The Level key for a dimension registry path. */
    public static ResourceKey<Level> levelKey(String dimension) {
        return ResourceKey.create(Registries.DIMENSION,
                new ResourceLocation(BUContent.MODID, dimension));
    }

    /** The DimensionType key for a dimension registry path. */
    public static ResourceKey<DimensionType> typeKey(String dimension) {
        return ResourceKey.create(Registries.DIMENSION_TYPE,
                new ResourceLocation(BUContent.MODID, dimension));
    }

    /**
     * Find a safe place to put an entity arriving in a dimension.
     *
     * Portals must not drop a player inside stone, into the void, or into a
     * lava sea. This scans a small column around the world's safe spawn and
     * returns the first position with two blocks of headroom over something
     * standable, falling back to a height above the dimension's floor so the
     * arrival is never fatal.
     *
     * @param target the dimension being entered
     * @param entity the entity being moved
     */
    public static Vec3 findSafeLanding(ServerLevel target, Entity entity) {
        BlockPos origin = target.getSharedSpawnPos();
        int searchRadius = 24;

        for (int attempt = 0; attempt < 64; attempt++) {
            // Spiral outward deterministically rather than randomly, so two
            // players entering the same portal arrive in the same place and can
            // find each other.
            int angleIndex = attempt % 16;
            int ring = attempt / 16;
            double angle = angleIndex * (Math.PI * 2.0D / 16.0D);
            int x = origin.getX() + (int) Math.round(Math.cos(angle) * searchRadius * (ring + 1) / 2.0D);
            int z = origin.getZ() + (int) Math.round(Math.sin(angle) * searchRadius * (ring + 1) / 2.0D);

            BlockPos found = scanColumn(target, x, z);
            if (found != null) {
                return Vec3.atBottomCenterOf(found);
            }
        }

        // Nothing standable: put the entity above the shared spawn at a height
        // that is inside the dimension's build limits. Falling is survivable
        // with the slow-falling effect the portal applies on arrival.
        int fallbackY = Math.min(target.getMaxBuildHeight() - 8,
                Math.max(target.getMinBuildHeight() + 8, origin.getY() + 8));
        return new Vec3(origin.getX() + 0.5D, fallbackY, origin.getZ() + 0.5D);
    }

    /**
     * Scan a column for two air blocks above a standable surface.
     *
     * @return the position to place the entity at, or null if the column is unsafe
     */
    private static BlockPos scanColumn(ServerLevel target, int x, int z) {
        int floor = target.getMinBuildHeight();
        int ceiling = Math.min(target.getMaxBuildHeight(), floor + 256);
        for (int y = ceiling - 2; y > floor; y--) {
            BlockPos candidate = new BlockPos(x, y, z);
            boolean headroom = target.getBlockState(candidate).getCollisionShape(target, candidate).isEmpty()
                    && target.getBlockState(candidate.above()).getCollisionShape(target, candidate.above()).isEmpty();
            if (!headroom) {
                continue;
            }
            // The surface must hold the entity up: solid, not a fluid, not fire.
            net.minecraft.world.level.block.state.BlockState ground =
                    target.getBlockState(candidate.below());
            if (ground.isAir() || ground.getFluidState().isSource()
                    || ground.getBlock() == Blocks.LAVA || ground.getBlock() == Blocks.FIRE) {
                continue;
            }
            if (!ground.isSolidRender(target, candidate.below())) {
                continue;
            }
            return candidate;
        }
        return null;
    }
}
