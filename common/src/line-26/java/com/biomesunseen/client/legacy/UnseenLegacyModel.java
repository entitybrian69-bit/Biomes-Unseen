package com.biomesunseen.client.legacy;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.resources.Identifier;

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

    public UnseenLegacyModel(ModelPart root) {
        head = root.getChild("head");
        body = root.getChild("body");
        leg0 = root.getChild("leg0");
        leg1 = root.getChild("leg1");
        leg2 = root.getChild("leg2");
        leg3 = root.getChild("leg3");
    }

    /** Shared model layer: every Biomes Unseen mob uses this six-part rig. */
    public static final ModelLayerLocation LAYER = new ModelLayerLocation(
            net.minecraft.resources.Identifier.fromNamespaceAndPath("biomesunseen", "legacy_mob"), "main");

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("head", CubeListBuilder.create().texOffs(0, 0)
                .addBox(-4.0F, -8.0F, -4.0F, 8.0F, 8.0F, 8.0F),
                PartPose.offset(0.0F, 4.0F, -4.0F));
        root.addOrReplaceChild("body", CubeListBuilder.create().texOffs(16, 16)
                .addBox(-5.0F, -10.0F, -7.0F, 10.0F, 16.0F, 8.0F),
                PartPose.offset(0.0F, 5.0F, 2.0F));
        root.addOrReplaceChild("leg0", CubeListBuilder.create().texOffs(0, 16)
                .addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F),
                PartPose.offset(-3.0F, 12.0F, 7.0F));
        root.addOrReplaceChild("leg1", CubeListBuilder.create().texOffs(0, 16)
                .addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F),
                PartPose.offset(3.0F, 12.0F, 7.0F));
        root.addOrReplaceChild("leg2", CubeListBuilder.create().texOffs(0, 16)
                .addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F),
                PartPose.offset(-3.0F, 12.0F, -5.0F));
        root.addOrReplaceChild("leg3", CubeListBuilder.create().texOffs(0, 16)
                .addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F),
                PartPose.offset(3.0F, 12.0F, -5.0F));
        return LayerDefinition.create(mesh, 64, 32);
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
    public void renderToBuffer(com.mojang.blaze3d.vertex.PoseStack matrixStack,
            com.mojang.blaze3d.vertex.VertexConsumer buffer,
            int packedLight, int packedOverlay, int packedColor) {
        head.render(matrixStack, buffer, packedLight, packedOverlay, packedColor);
        body.render(matrixStack, buffer, packedLight, packedOverlay, packedColor);
        leg0.render(matrixStack, buffer, packedLight, packedOverlay, packedColor);
        leg1.render(matrixStack, buffer, packedLight, packedOverlay, packedColor);
        leg2.render(matrixStack, buffer, packedLight, packedOverlay, packedColor);
        leg3.render(matrixStack, buffer, packedLight, packedOverlay, packedColor);
    }
}
