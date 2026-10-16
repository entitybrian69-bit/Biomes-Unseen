package com.biomesunseen.client.legacy;

import com.mojang.blaze3d.matrix.MatrixStack;
import net.minecraft.client.renderer.vertex.IVertexBuilder;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.ModelRenderer;

import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Box model for the 1.16.5 line: head, body and four limbs, animated from
 * the entity's LegacyAnimDriver (limb swing, head yaw, one-shot poses).
 */
public class UnseenLegacyModel<T extends BiomesUnseenMob> extends EntityModel<T> {

    private final ModelPart head;
    private final ModelPart body;
    private final ModelPart leg0;
    private final ModelPart leg1;
    private final ModelPart leg2;
    private final ModelPart leg3;

    public UnseenLegacyModel() {
        head = new ModelRenderer(this, 0, 0);
        head.addBox(-4.0F, -8.0F, -4.0F, 8.0F, 8.0F, 8.0F, 0.0F);
        head.setPos(0.0F, 4.0F, -4.0F);
        body = new ModelRenderer(this, 16, 16);
        body.addBox(-5.0F, -10.0F, -7.0F, 10.0F, 16.0F, 8.0F, 0.0F);
        body.setPos(0.0F, 5.0F, 2.0F);
        leg0 = new ModelRenderer(this, 0, 16);
        leg0.addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, 0.0F);
        leg0.setPos(-3.0F, 12.0F, 7.0F);
        leg1 = new ModelRenderer(this, 0, 16);
        leg1.addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, 0.0F);
        leg1.setPos(3.0F, 12.0F, 7.0F);
        leg2 = new ModelRenderer(this, 0, 16);
        leg2.addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, 0.0F);
        leg2.setPos(-3.0F, 12.0F, -5.0F);
        leg3 = new ModelRenderer(this, 0, 16);
        leg3.addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, 0.0F);
        leg3.setPos(3.0F, 12.0F, -5.0F);
    }

    @Override
    public void setupAnim(T entity, float limbSwing, float limbSwingAmount,
                          float ageInTicks, float netHeadYaw, float headPitch) {
        head.yRot = netHeadYaw * ((float) Math.PI / 180.0F);
        head.xRot = headPitch * ((float) Math.PI / 180.0F);
        leg0.xRot = (float) Math.cos(limbSwing * 0.6662F) * 1.4F * limbSwingAmount;
        leg1.xRot = (float) Math.cos(limbSwing * 0.6662F + (float) Math.PI) * 1.4F * limbSwingAmount;
        leg2.xRot = (float) Math.cos(limbSwing * 0.6662F + (float) Math.PI) * 1.4F * limbSwingAmount;
        leg3.xRot = (float) Math.cos(limbSwing * 0.6662F) * 1.4F * limbSwingAmount;
        if (entity.animDriver().oneShotClip != null) {
            float phase = entity.animDriver().oneShotPhase;
            if ("attack".equals(entity.animDriver().oneShotClip)
                    || "slam".equals(entity.animDriver().oneShotClip)) {
                body.xRot = (float) Math.sin(phase * (float) Math.PI) * 0.4F;
            } else if ("graze".equals(entity.animDriver().oneShotClip)) {
                head.xRot = (float) Math.sin(phase * (float) Math.PI) * 0.9F;
            } else if ("flee".equals(entity.animDriver().oneShotClip)) {
                body.xRot = -0.2F;
            }
        }
    }

    @Override
    public void render(com.mojang.blaze3d.matrix.MatrixStack matrixStack,
            net.minecraft.client.renderer.vertex.IVertexBuilder buffer,
            int packedLight, int packedOverlay, float red, float green, float blue, float alpha) {
        head.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
        body.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
        leg0.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
        leg1.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
        leg2.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
        leg3.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
    }
}
