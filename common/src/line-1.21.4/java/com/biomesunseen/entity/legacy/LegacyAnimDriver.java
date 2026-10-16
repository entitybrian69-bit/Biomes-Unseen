package com.biomesunseen.entity.legacy;

import net.minecraft.entity.MobEntity;

/**
 * Procedural animation driver for the 1.16.5 line where GeckoLib is
 * unavailable.  Produces limb-swing, head-yaw and one-shot pose phases that
 * the legacy renderer reads, so every mob is still fully animated.
 */
public class LegacyAnimDriver {

    private final MobEntity mob;

    public float limbSwing;
    public float limbSwingAmount;
    public float headYaw;
    public float headPitch;
    /** 0..1 phase within the current one-shot clip. */
    public float oneShotPhase;
    public String oneShotClip;
    private int oneShotTicks;

    public LegacyAnimDriver(MobEntity mob) {
        this.mob = mob;
    }

    /** Called from the mob's aiStep. */
    public void tick() {
        double speedSq = mob.getDeltaMovement().horizontalDistanceSqr();
        float targetAmount = speedSq > 1.0E-4F ? 1.0F : 0.0F;
        limbSwingAmount += (targetAmount - limbSwingAmount) * 0.25F;
        limbSwing += limbSwingAmount * 1.4F;
        headYaw = mob.yHeadRot - mob.yBodyRot;
        headPitch = mob.xRot;
        if (oneShotTicks > 0) {
            oneShotTicks--;
            oneShotPhase = 1.0F - oneShotTicks / 24.0F;
        } else {
            oneShotClip = null;
            oneShotPhase = 0.0F;
        }
    }

    public void trigger(String clip) {
        oneShotClip = clip;
        oneShotTicks = 24;
        oneShotPhase = 0.0F;
    }
}
