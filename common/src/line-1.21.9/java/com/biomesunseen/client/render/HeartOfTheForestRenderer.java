package com.biomesunseen.client.render;

import net.minecraft.client.renderer.entity.EntityRendererProvider;

import com.biomesunseen.entity.boss.HeartOfTheForestEntity;

/**
 * Animated boss renderer for heart_of_the_forest.  Scales the generic GeckoLib model up
 * to boss size and keeps the health bar anchored above the model.
 */
public class HeartOfTheForestRenderer extends com.biomesunseen.client.render.BiomesUnseenGeoRenderer<HeartOfTheForestEntity> {

    public HeartOfTheForestRenderer(EntityRendererProvider.Context context) {
        super(context, "heart_of_the_forest");
        this.shadowRadius = 1.2F;
    }
}
