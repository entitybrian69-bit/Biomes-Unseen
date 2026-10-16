package com.biomesunseen.entity.ai;

import net.minecraft.entity.CreatureEntity;
import net.minecraft.entity.ai.goal.Goal;
import net.minecraft.entity.player.PlayerEntity;


import com.biomesunseen.util.AiThrottle;

/**
 * Base goal with built-in AI throttling: expensive canUse checks only run on
 * the entity's think ticks, keeping large mob counts cheap.
 */
public abstract class ThrottledGoal extends Goal {

    protected final CreatureEntity mob;

    protected ThrottledGoal(CreatureEntity mob) {
        this.mob = mob;
    }

    @Override
    public boolean canUse() {
        return AiThrottle.shouldThink(mob.getId(), mob.level.getGameTime())
                && throttledCanUse();
    }

    /** Checked only on the mob's think ticks. */
    protected abstract boolean throttledCanUse();
}
