package com.biomesunseen.client.render;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.entity.GloomCrawlerEntity;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.resources.ResourceLocation;
import software.bernie.geckolib.model.DefaultedEntityGeoModel;
import software.bernie.geckolib.renderer.GeoEntityRenderer;

public class GloomCrawlerRenderer extends GeoEntityRenderer<GloomCrawlerEntity> {
    public GloomCrawlerRenderer(EntityRendererProvider.Context context) {
        super(context, new DefaultedEntityGeoModel<>(new ResourceLocation(BiomesUnseen.MOD_ID, "gloom_crawler")));
        this.shadowRadius = 0.6F;
    }
}
