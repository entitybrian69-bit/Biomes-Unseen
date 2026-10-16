package com.biomesunseen.entity.ai;

import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.player.Player;


import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Terrain use: seek advantageous ground (higher elevation when threatened,
 * shelter when low on health).  Demonstrates environment interaction beyond
 * plain wandering.
 */
public class TerrainUseGoal extends ThrottledGoal {

    private final double speed;
    private int repathCooldown;

    public TerrainUseGoal(PathfinderMob mob, double speed) {
        super(mob);
        this.speed = speed;
        this.setFlags(java.util.EnumSet.of(Flag.MOVE));
    }

    @Override
    protected boolean throttledCanUse() {
        if (!(mob instanceof BiomesUnseenMob) || !((BiomesUnseenMob) mob).mobDef().terrainUse) {
            return false;
        }
        return mob.getTarget() != null || mob.getHealth() < mob.getMaxHealth() * 0.4F;
    }

    @Override
    public void start() {
        repathCooldown = 0;
    }

    @Override
    public void tick() {
        if (--repathCooldown > 0) {
            return;
        }
        repathCooldown = 40;
        // Probe a few candidate spots and pick the highest safe one.
        net.minecraft.core.BlockPos best = null;
        double bestScore = Double.NEGATIVE_INFINITY;
        for (int i = 0; i < 6; i++) {
            net.minecraft.core.BlockPos candidate = mob.blockPosition().offset(
                    mob.getRandom().nextInt(13) - 6, 0, mob.getRandom().nextInt(13) - 6);
            net.minecraft.core.BlockPos surface = com.biomesunseen.util.EntityLevels.of(mob).getHeightmapPos(
                    net.minecraft.world.level.levelgen.Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, candidate);
            double score = surface.getY() - mob.getY();
            if (mob.getHealth() < mob.getMaxHealth() * 0.5F) {
                score = -score; // hurt: prefer low, sheltered ground
            }
            if (score > bestScore) {
                bestScore = score;
                best = surface;
            }
        }
        if (best != null) {
            mob.getNavigation().moveTo(best.getX() + 0.5D, best.getY(), best.getZ() + 0.5D, speed);
        }
    }
}
