package com.biomesunseen.client.legacy;

import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.resources.Identifier;

import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Mob renderer for the hand-animated box rig.  Three type parameters are
 * mandatory from 1.21.2 (MobRenderer gained the render-state parameter), so the
 * state and model are fixed here and only the entity type stays generic: that
 * keeps diamond inference working at the registration site.
 */
public class UnseenLegacyRenderer<T extends BiomesUnseenMob>
        extends MobRenderer<T, UnseenLegacyRenderState, UnseenLegacyModel<UnseenLegacyRenderState>> {

    private final String id;

    public UnseenLegacyRenderer(EntityRendererProvider.Context context, String id) {
        super(context, new UnseenLegacyModel<UnseenLegacyRenderState>(
                context.bakeLayer(UnseenLegacyModel.LAYER)), 0.5F);
        this.id = id;
    }

    /** Renderer provider factory used by ClientSetup. */
    public static <E extends BiomesUnseenMob> EntityRendererProvider<E> provider(String id) {
        return context -> new UnseenLegacyRenderer<E>(context, id);
    }

    @Override
    public UnseenLegacyRenderState createRenderState() {
        return new UnseenLegacyRenderState();
    }

    @Override
    public void extractRenderState(T entity, UnseenLegacyRenderState state, float partialTick) {
        super.extractRenderState(entity, state, partialTick);
        state.bsLimbSwing = entity.tickCount + partialTick;
        state.bsLimbSwingAmount = (float) entity.getDeltaMovement().horizontalDistance();
        state.bsAgeInTicks = entity.tickCount + partialTick;
        state.bsHeadYaw = entity.getYRot();
        state.bsHeadPitch = entity.getXRot();
        state.bsClip = entity.animDriver().oneShotClip;
        state.bsPhase = entity.animDriver().oneShotPhase;
    }

    @Override
    public Identifier getTextureLocation(UnseenLegacyRenderState state) {
        return Identifier.fromNamespaceAndPath("biomesunseen", "textures/entity/" + id + ".png");
    }
}
