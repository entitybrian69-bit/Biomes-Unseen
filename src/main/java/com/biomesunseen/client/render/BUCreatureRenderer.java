package com.biomesunseen.client.render;

import com.biomesunseen.client.model.BUCreatureModel;
import com.biomesunseen.entity.BUCreature;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import software.bernie.geckolib.renderer.GeoEntityRenderer;

/**
 * The renderer for every non-boss creature.
 *
 * A single GeckoLib renderer handles all 80 species; {@link BUCreatureModel}
 * resolves the rig and texture per species, so adding a creature needs no new
 * renderer class.
 */
public class BUCreatureRenderer extends GeoEntityRenderer<BUCreature> {

    public BUCreatureRenderer(EntityRendererProvider.Context context) {
        super(context, new BUCreatureModel());
    }


}
