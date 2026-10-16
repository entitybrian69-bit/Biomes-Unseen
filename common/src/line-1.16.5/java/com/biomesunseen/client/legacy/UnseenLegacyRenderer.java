package com.biomesunseen.client.legacy;

import net.minecraft.client.renderer.entity.EntityRenderDispatcher;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.resources.ResourceLocation;

import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Mob renderer for the 1.16.5 line: the renderer takes the dispatcher directly
 * (EntityRendererProvider does not exist yet) and the texture is resolved once.
 */
public class UnseenLegacyRenderer<T extends BiomesUnseenMob>
        extends MobRenderer<T, UnseenLegacyModel<T>> {

    private final ResourceLocation texture;

    public UnseenLegacyRenderer(EntityRenderDispatcher dispatcher, String id) {
        super(dispatcher, new UnseenLegacyModel<T>(), 0.5F);
        this.texture = new ResourceLocation("biomesunseen", "textures/entity/" + id + ".png");
    }

    @Override
    public ResourceLocation getTextureLocation(T entity) {
        return this.texture;
    }
}
