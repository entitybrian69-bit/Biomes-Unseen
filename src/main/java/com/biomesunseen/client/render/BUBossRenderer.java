package com.biomesunseen.client.render;

import com.biomesunseen.client.model.BUBossModel;
import com.biomesunseen.entity.BUBoss;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import software.bernie.geckolib.renderer.GeoEntityRenderer;

/**
 * The renderer for the five bosses.
 *
 * Bosses scale up the model by their authored scale and never apply the default
 * death tip-over, because each has a hand-authored death sequence that is the
 * payoff of the fight.
 */
public class BUBossRenderer extends GeoEntityRenderer<BUBoss> {

    public BUBossRenderer(EntityRendererProvider.Context context) {
        super(context, new BUBossModel());
    }

    @Override
    public float getMotionAnimThreshold(BUBoss entity) {
        return 0.01F;
    }

    @Override
    protected float getDeathMaxRotation(BUBoss entity) {
        return 0.0F;
    }
}
