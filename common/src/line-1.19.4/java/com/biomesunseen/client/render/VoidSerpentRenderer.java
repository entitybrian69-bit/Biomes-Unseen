package com.biomesunseen.client.render;

import net.minecraft.client.renderer.entity.EntityRendererProvider;

import com.biomesunseen.entity.boss.VoidSerpentEntity;

/**
 * Animated boss renderer for void_serpent.  Scales the generic GeckoLib model up
 * to boss size and keeps the health bar anchored above the model.
 */
public class VoidSerpentRenderer extends com.biomesunseen.client.render.BiomesUnseenGeoRenderer<VoidSerpentEntity> {

    public VoidSerpentRenderer(EntityRendererProvider.Context context) {
        super(context, "void_serpent");
        this.shadowRadius = 1.2F;
    }
}
