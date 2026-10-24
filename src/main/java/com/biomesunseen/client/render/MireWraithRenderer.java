package com.biomesunseen.client.render;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.entity.MireWraithEntity;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.resources.ResourceLocation;
import software.bernie.geckolib.model.DefaultedEntityGeoModel;
import software.bernie.geckolib.renderer.GeoEntityRenderer;

public class MireWraithRenderer extends GeoEntityRenderer<MireWraithEntity> {
    public MireWraithRenderer(EntityRendererProvider.Context context) {
        super(context, new DefaultedEntityGeoModel<>(new ResourceLocation(BiomesUnseen.MOD_ID, "mire_wraith")));
        this.shadowRadius = 0.4F;
    }
}
