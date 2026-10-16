package com.biomesunseen.client.render;

import net.minecraft.client.renderer.entity.EntityRendererProvider;

import software.bernie.geckolib.renderer.GeoEntityRenderer;

import com.biomesunseen.client.model.BiomesUnseenGeoModel;

/**
 * Generic animated renderer shared by all 25 mobs.
 */
public class BiomesUnseenGeoRenderer<T extends software.bernie.geckolib.animatable.GeoAnimatable>
        extends GeoEntityRenderer<T> {

    public BiomesUnseenGeoRenderer(EntityRendererProvider.Context context, String id) {
        super(context, new BiomesUnseenGeoModel<>(id));
        this.shadowRadius = 0.5F;
    }
}
