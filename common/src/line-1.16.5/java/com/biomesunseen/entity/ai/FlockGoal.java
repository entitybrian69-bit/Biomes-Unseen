package com.biomesunseen.entity.ai;

import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.player.Player;


import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Flocking for flying/ambient mobs: boids-style cohesion, separation and
 * alignment with nearby allies, plus gentle altitude drift.
 */
public class FlockGoal extends ThrottledGoal {

    private final double speed;
    private int repathCooldown;

    public FlockGoal(PathfinderMob mob, double speed) {
        super(mob);
        this.speed = speed;
        this.setFlags(java.util.EnumSet.of(Flag.MOVE));
    }

    @Override
    protected boolean throttledCanUse() {
        return mob instanceof BiomesUnseenMob
                && (((BiomesUnseenMob) mob).mobDef().pack || ((BiomesUnseenMob) mob).mobDef().herd);
    }

    @Override
    public void tick() {
        if (--repathCooldown > 0) {
            return;
        }
        repathCooldown = 20;
        BiomesUnseenMob ally = mob instanceof BiomesUnseenMob
                ? ((BiomesUnseenMob) mob).findNearestAlly(16.0D) : null;
        if (ally == null) {
            return;
        }
        double dx = ally.getX() - mob.getX();
        double dy = ally.getY() - mob.getY();
        double dz = ally.getZ() - mob.getZ();
        double dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
        if (dist < 3.0D) {
            // Separation: drift away slightly to avoid stacking.
            mob.getNavigation().moveTo(mob.getX() - dx * 0.5D, mob.getY() + 1.0D,
                    mob.getZ() - dz * 0.5D, speed * 0.7D);
        } else if (dist > 10.0D) {
            // Cohesion: rejoin the flock.
            mob.getNavigation().moveTo(ally, speed);
        } else {
            // Alignment: match the ally's heading.
            mob.getNavigation().moveTo(mob.getX() + dx * 0.2D, mob.getY() + dy * 0.2D,
                    mob.getZ() + dz * 0.2D, speed * 0.5D);
        }
    }
}
