package com.biomesunseen.entity.ai;

import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.player.Player;


import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Fleeing behaviour: run from the nearest threat (player or attacker) and
 * play the flee animation while doing so.
 */
public class FleeDangerGoal extends ThrottledGoal {

    private final double speed;
    private net.minecraft.world.entity.player.Player threat;
    private int fleeTicks;

    public FleeDangerGoal(PathfinderMob mob, double speed) {
        super(mob);
        this.speed = speed;
        this.setFlags(java.util.EnumSet.of(Flag.MOVE));
    }

    @Override
    protected boolean throttledCanUse() {
        if (mob instanceof BiomesUnseenMob && !((BiomesUnseenMob) mob).mobDef().flees) {
            return false;
        }
        threat = com.biomesunseen.util.EntityLevels.of(mob).getNearestPlayer(mob, 8.0D);
        return threat != null;
    }

    @Override
    public boolean canContinueToUse() {
        return threat != null && threat.isAlive() && fleeTicks > 0;
    }

    @Override
    public void start() {
        fleeTicks = 100;
        if (mob instanceof BiomesUnseenMob) {
            ((BiomesUnseenMob) mob).triggerAnim("flee");
        }
    }

    @Override
    public void tick() {
        fleeTicks--;
        if (threat != null) {
            double dx = mob.getX() - threat.getX();
            double dz = mob.getZ() - threat.getZ();
            double len = Math.sqrt(dx * dx + dz * dz);
            if (len > 0.01D) {
                mob.getNavigation().moveTo(mob.getX() + dx / len * 10.0D, mob.getY(),
                        mob.getZ() + dz / len * 10.0D, speed);
            }
        }
    }

    @Override
    public void stop() {
        threat = null;
    }
}
