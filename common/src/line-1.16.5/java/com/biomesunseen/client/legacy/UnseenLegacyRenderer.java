package com.biomesunseen.client.legacy;

import net.minecraft.client.renderer.entity.EntityRendererManager;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.util.ResourceLocation;

import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * MobEntity renderer for the 1.16.5 line using the legacy box model.
 */
public class UnseenLegacyRenderer<T extends BiomesUnseenMob>
        extends MobRenderer<T, UnseenLegacyModel<T>> {

    private final String id;

    public UnseenLegacyRenderer(EntityRendererManager manager, String id) {
        super(context, new UnseenLegacyModel<T>(context.bakeLayer(UnseenLegacyModel.LAYER)), 0.5F);
        this.id = id;
    }

    @Override
    public ResourceLocation getTextureLocation(T entity) {
        return new ResourceLocation("biomesunseen", "textures/entity/" + id + ".png");
    }
}
