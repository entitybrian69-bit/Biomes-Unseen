package com.biomesunseen.client.render;

import com.biomesunseen.client.model.BUBossModel;
import com.biomesunseen.entity.BUBoss;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import software.bernie.geckolib.renderer.GeoEntityRenderer;

/**
 * The renderer for the five bosses.
 *
 * Bosses get their own renderer because they resolve a different model and
 * texture root from creatures: each has a bespoke multi-part rig and its own
 * 64x64 atlas rather than sharing a family rig.
 */
public class BUBossRenderer extends GeoEntityRenderer<BUBoss> {

    public BUBossRenderer(EntityRendererProvider.Context context) {
        super(context, new BUBossModel());
    }


}
