package com.biomesunseen.client.render;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.entity.boss.HeartOfTheForestEntity;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.resources.ResourceLocation;
import software.bernie.geckolib.model.DefaultedEntityGeoModel;
import software.bernie.geckolib.renderer.GeoEntityRenderer;

public class HeartOfTheForestRenderer extends GeoEntityRenderer<HeartOfTheForestEntity> {
    public HeartOfTheForestRenderer(EntityRendererProvider.Context context) {
        super(context, new DefaultedEntityGeoModel<>(new ResourceLocation(BiomesUnseen.MOD_ID, "heart_of_the_forest")));
        this.shadowRadius = 1.6F;
    }
}
