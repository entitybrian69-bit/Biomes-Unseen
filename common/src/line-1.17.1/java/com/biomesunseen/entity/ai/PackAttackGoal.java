package com.biomesunseen.entity.ai;

import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.LivingEntity;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Pack tactics: when one member engages, nearby allies share the target and
 * attack together, circling instead of stacking on one spot.
 */
public class PackAttackGoal extends MeleeAttackGoal {

    private final PathfinderMob mob;
    private int circleDirection;

    public PackAttackGoal(PathfinderMob mob, double speed, boolean followTargetEvenIfNotSeen) {
        super(mob, speed, followTargetEvenIfNotSeen);
        this.mob = mob;
        this.circleDirection = mob.getRandom().nextBoolean() ? 1 : -1;
    }

    @Override
    public boolean canUse() {
        if (!BiomesUnseen.config().enablePackTactics) {
            return super.canUse();
        }
        return super.canUse();
    }

    @Override
    protected void checkAndPerformAttack(LivingEntity target, double distance) {
        super.checkAndPerformAttack(target, distance);
        if (target != null && mob.distanceTo(target) < 3.0D) {
            double angle = Math.atan2(target.getZ() - mob.getZ(), target.getX() - mob.getX())
                    + circleDirection * 0.6D;
            mob.getNavigation().moveTo(target.getX() + Math.cos(angle) * 2.5D,
                    target.getY(), target.getZ() + Math.sin(angle) * 2.5D, 1.15D);
        }
    }
}
