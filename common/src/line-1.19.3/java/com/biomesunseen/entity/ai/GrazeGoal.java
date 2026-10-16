package com.biomesunseen.entity.ai;

import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.player.Player;


import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Grazing: stop, play the graze animation, and slowly regenerate.  Keeps
 * herds visibly alive instead of idle-stiff.
 */
public class GrazeGoal extends ThrottledGoal {

    private int grazeTicks;

    public GrazeGoal(PathfinderMob mob) {
        super(mob);
        this.setFlags(java.util.EnumSet.of(Flag.LOOK));
    }

    @Override
    protected boolean throttledCanUse() {
        return mob instanceof BiomesUnseenMob
                && ((BiomesUnseenMob) mob).mobDef().hasBehavior("graze")
                && mob.getRandom().nextInt(8) == 0;
    }

    @Override
    public void start() {
        grazeTicks = 60;
        ((BiomesUnseenMob) mob).triggerAnim("graze");
    }

    @Override
    public boolean canContinueToUse() {
        return grazeTicks > 0;
    }

    @Override
    public void tick() {
        grazeTicks--;
        mob.getNavigation().stop();
        if (grazeTicks % 20 == 0 && mob.getHealth() < mob.getMaxHealth()) {
            mob.heal(0.5F);
        }
    }
}
