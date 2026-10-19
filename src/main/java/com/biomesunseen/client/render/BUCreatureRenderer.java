package com.biomesunseen.client.render;

import com.biomesunseen.client.model.BUCreatureModel;
import com.biomesunseen.entity.BUCreature;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import software.bernie.geckolib.renderer.GeoEntityRenderer;

/**
 * The renderer for every non-boss creature.
 *
 * A single GeckoLib renderer handles all 80 species; the model resolves the rig
 * and texture per species. Shadow radius is read from the species data so a
 * mouse-sized creature does not cast a boss-sized shadow.
 */
public class BUCreatureRenderer extends GeoEntityRenderer<BUCreature> {

    public BUCreatureRenderer(EntityRendererProvider.Context context) {
        super(context, new BUCreatureModel());
    }

    @Override
    public float getMotionAnimThreshold(BUCreature entity) {
        // Lower than GeckoLib's default so slow-moving species still transition
        // out of idle; several of the authored creatures walk at 0.2 speed.
        return 0.01F;
    }

    @Override
    protected float getDeathMaxRotation(BUCreature entity) {
        // The death animation is authored, so the renderer must not also apply
        // its own 90-degree tip-over on top of it.
        return 0.0F;
    }
}
