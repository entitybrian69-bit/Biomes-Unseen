package com.biomesunseen.entity.ai;

import net.minecraft.entity.CreatureEntity;
import net.minecraft.entity.ai.goal.Goal;
import net.minecraft.entity.player.PlayerEntity;


import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Herding: follow the nearest ally of the same species when alone, stay
 * loosely clustered while grazing.  Spreads decisions across think ticks.
 */
public class HerdFollowGoal extends ThrottledGoal {

    private final double speed;
    private CreatureEntity leader;
    private int repathCooldown;

    public HerdFollowGoal(CreatureEntity mob, double speed) {
        super(mob);
        this.speed = speed;
        this.setFlags(java.util.EnumSet.of(Flag.MOVE));
    }

    @Override
    protected boolean throttledCanUse() {
        if (mob instanceof BiomesUnseenMob) {
            BiomesUnseenMob self = (BiomesUnseenMob) mob;
            if (!self.mobDef().herd && !self.mobDef().pack) {
                return false;
            }
            leader = self.findNearestAlly(12.0D);
            return leader != null && mob.distanceTo(leader) > 4.0D;
        }
        return false;
    }

    @Override
    public boolean canContinueToUse() {
        return leader != null && leader.isAlive() && mob.distanceTo(leader) > 3.0D;
    }

    @Override
    public void tick() {
        if (leader == null) {
            return;
        }
        if (--repathCooldown <= 0) {
            repathCooldown = 20;
            mob.getNavigation().moveTo(leader, speed);
        }
    }

    @Override
    public void stop() {
        leader = null;
        mob.getNavigation().stop();
    }
}
