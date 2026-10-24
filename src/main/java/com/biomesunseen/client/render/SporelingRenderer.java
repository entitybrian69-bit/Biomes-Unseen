package com.biomesunseen.client.render;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.entity.SporelingEntity;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.resources.ResourceLocation;
import software.bernie.geckolib.model.DefaultedEntityGeoModel;
import software.bernie.geckolib.renderer.GeoEntityRenderer;

public class SporelingRenderer extends GeoEntityRenderer<SporelingEntity> {
    public SporelingRenderer(EntityRendererProvider.Context context) {
        super(context, new DefaultedEntityGeoModel<>(new ResourceLocation(BiomesUnseen.MOD_ID, "sporeling")));
        this.shadowRadius = 0.35F;
    }
}
