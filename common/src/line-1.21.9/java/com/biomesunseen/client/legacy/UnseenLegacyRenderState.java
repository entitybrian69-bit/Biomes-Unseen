package com.biomesunseen.client.legacy;

/**
 * Render state for the legacy box model.  Every animation input is copied off
 * the entity in extractRenderState, so the model itself never touches live
 * entity state (which is what the 1.21.2 render-state split requires).
 */
public class UnseenLegacyRenderState
        extends net.minecraft.client.renderer.entity.state.LivingEntityRenderState {

    public float bsLimbSwing;
    public float bsLimbSwingAmount;
    public float bsAgeInTicks;
    public float bsHeadYaw;
    public float bsHeadPitch;
    public String bsClip;
    public float bsPhase;
}
