package com.biomesunseen.client.render;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.entity.SpecMobEntity;
import com.biomesunseen.spec.MobSpec;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.resources.ResourceLocation;
import software.bernie.geckolib.model.DefaultedEntityGeoModel;
import software.bernie.geckolib.renderer.GeoEntityRenderer;

/** One renderer for every spec mob; model, animation and texture are found by the mob id. */
public class SpecMobRenderer extends GeoEntityRenderer<SpecMobEntity> {
    public SpecMobRenderer(EntityRendererProvider.Context context, MobSpec spec) {
        super(context, new DefaultedEntityGeoModel<>(new ResourceLocation(BiomesUnseen.MOD_ID, spec.id())));
        this.shadowRadius = Math.max(0.25F, spec.width() * 0.5F);
    }
}
