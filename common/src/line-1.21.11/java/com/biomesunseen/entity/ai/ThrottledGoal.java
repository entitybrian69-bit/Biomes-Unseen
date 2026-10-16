package com.biomesunseen.entity.ai;

import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.player.Player;


import com.biomesunseen.util.AiThrottle;

/**
 * Base goal with built-in AI throttling: expensive canUse checks only run on
 * the entity's think ticks, keeping large mob counts cheap.
 */
public abstract class ThrottledGoal extends Goal {

    protected final PathfinderMob mob;

    protected ThrottledGoal(PathfinderMob mob) {
        this.mob = mob;
    }

    @Override
    public boolean canUse() {
        return AiThrottle.shouldThink(mob.getId(), com.biomesunseen.util.EntityLevels.of(mob).getGameTime())
                && throttledCanUse();
    }

    /** Checked only on the mob's think ticks. */
    protected abstract boolean throttledCanUse();
}
