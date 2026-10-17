# -*- coding: utf-8 -*-
"""Emits client rendering + datagen Java for one API line."""

import os

from content import (ALL_MOB_ROWS as MOB_ROWS, ALL_BOSS_ROWS as BOSS_ROWS,
                     ALL_ORE_ROWS as ORE_ROWS, ALL_DECOR_ROWS as DECOR_ROWS,
                     ALL_PLANT_ROWS as PLANT_ROWS, PARTICLE_TYPES,
                     ALL_BIOME_ROWS as BIOME_ROWS,
                     ALL_STRUCTURE_ROWS as STRUCTURE_ROWS)
from lines import LINES
from emit_families import _w, _s, _camel


# 1.21.2 introduced render states: MobRenderer gained a third type parameter
# and EntityModel is now bound to EntityRenderState (probe-fabric-1.21.2).
RS_LINES = ("1.21.2", "1.21.4", "1.21.5", "1.21.9", "1.21.11", "26")

# The three 1.17.1 - 1.18.2 lines use the modern architectury client API with
# the 3.x signatures.  There RegistrySupplier<T> *is* a Supplier<T> but the
# register methods want Supplier<EntityType<? extends T>>, and generics are
# invariant, so the call sites need an explicit widening cast:
#   required: Supplier<EntityType<? extends T>>,EntityRendererProvider<T>
#   found:    RegistrySupplier<EntityType<LumoxEntity>>,...
DEV_LEGACY_LINES = ("1.17.1", "1.18.1", "1.18")

# The 1.21.9 particle overhaul removed TextureSheetParticle and moved the
# velocity/position fields, so the custom sprite particle (and its provider)
# cannot be compiled against those jars.  Those lines ship the particle *types*
# (registry entries, spawn packets) without a custom client particle.
NO_CUSTOM_PARTICLE_LINES = ("1.21.9", "1.21.11", "26")


def emit_client_datagen(root, line_key):
    F = LINES[line_key]
    legacy = F["pkgs"] == "legacy"
    geckolib = F["geckolib"]
    base = "common/src/line-%s/java/com/biomesunseen" % line_key
    arch_pkg = ("me.shedaniel.architectury" if F["expect"] == "me.shedaniel"
                else "dev.architectury")

    # ================================================================== #
    # client/model/BiomesUnseenGeoModel.java (GeckoLib lines)
    # ================================================================== #
    if geckolib != "none":
        if geckolib == "g4":
            model_java = '''package com.biomesunseen.client.model;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;

import software.bernie.geckolib.animatable.GeoAnimatable;
import software.bernie.geckolib.model.GeoModel;
import software.bernie.geckolib.model.data.EntityModelData;
import software.bernie.geckolib.animation.AnimationState;

/**
 * Generic GeckoLib model for every mob and boss.  Resource paths are derived
 * from the entity's registry id:
 *   assets/biomesunseen/geo/<id>.geo.json
 *   assets/biomesunseen/animations/<id>.animation.json
 *   assets/biomesunseen/textures/entity/<id>.png
 */
public class BiomesUnseenGeoModel<T extends GeoAnimatable> extends GeoModel<T> {

    private final String id;

    public BiomesUnseenGeoModel(String id) {
        this.id = id;
    }

    @Override
    public ResourceLocation getModelResource(T animatable) {
        return new ResourceLocation("biomesunseen", "geo/" + id + ".geo.json");
    }

    @Override
    public ResourceLocation getTextureResource(T animatable) {
        return new ResourceLocation("biomesunseen", "textures/entity/" + id + ".png");
    }

    @Override
    public ResourceLocation getAnimationResource(T animatable) {
        return new ResourceLocation("biomesunseen", "animations/" + id + ".animation.json");
    }

    @Override
    public void setCustomAnimations(T animatable, long instanceId, AnimationState<T> animationState) {
        super.setCustomAnimations(animatable, instanceId, animationState);
        EntityModelData data = animationState.getData(EntityModelData.DATA_ID);
        if (data != null) {
            data.headPitch().set(Mth.clamp(data.headPitch().get(), -30.0F, 30.0F));
        }
    }
}
'''
        else:
            model_java = '''package com.biomesunseen.client.model;

import net.minecraft.resources.ResourceLocation;

import software.bernie.geckolib3.core.IAnimatable;
import software.bernie.geckolib3.core.event.predicate.AnimationState;
import software.bernie.geckolib3.model.AnimatedGeoModel;

/**
 * Generic GeckoLib model for every mob and boss.  Resource paths are derived
 * from the entity's registry id:
 *   assets/biomesunseen/geo/<id>.geo.json
 *   assets/biomesunseen/animations/<id>.animation.json
 *   assets/biomesunseen/textures/entity/<id>.png
 */
public class BiomesUnseenGeoModel<T extends IAnimatable> extends AnimatedGeoModel<T> {

    private final String id;

    public BiomesUnseenGeoModel(String id) {
        this.id = id;
    }

    @Override
    public ResourceLocation getModelResource(T animatable) {
        return new ResourceLocation("biomesunseen", "geo/" + id + ".geo.json");
    }

    @Override
    public ResourceLocation getTextureResource(T animatable) {
        return new ResourceLocation("biomesunseen", "textures/entity/" + id + ".png");
    }

    @Override
    public ResourceLocation getAnimationResource(T animatable) {
        return new ResourceLocation("biomesunseen", "animations/" + id + ".animation.json");
    }
}
'''
        _w(root, base + "/client/model/BiomesUnseenGeoModel.java", model_java)

        # Generic renderer
        if geckolib == "g4":
            renderer_java = '''package com.biomesunseen.client.render;

import net.minecraft.client.renderer.entity.EntityRendererProvider;

import software.bernie.geckolib.renderer.GeoEntityRenderer;

import com.biomesunseen.client.model.BiomesUnseenGeoModel;

/**
 * Generic animated renderer shared by all 25 mobs.
 */
public class BiomesUnseenGeoRenderer<T extends software.bernie.geckolib.animatable.GeoAnimatable>
        extends GeoEntityRenderer<T> {

    public BiomesUnseenGeoRenderer(EntityRendererProvider.Context context, String id) {
        super(context, new BiomesUnseenGeoModel<>(id));
        this.shadowRadius = 0.5F;
    }
}
'''
        else:
            renderer_java = '''package com.biomesunseen.client.render;

import net.minecraft.client.renderer.entity.EntityRendererProvider;

import software.bernie.geckolib3.renderers.geo.GeoEntityRenderer;

import com.biomesunseen.client.model.BiomesUnseenGeoModel;

/**
 * Generic animated renderer shared by all 25 mobs.
 */
public class BiomesUnseenGeoRenderer<T extends software.bernie.geckolib3.core.IAnimatable>
        extends GeoEntityRenderer<T> {

    public BiomesUnseenGeoRenderer(EntityRendererProvider.Context context, String id) {
        super(context, new BiomesUnseenGeoModel<>(id));
        this.shadowRadius = 0.5F;
    }
}
'''
        _w(root, base + "/client/render/BiomesUnseenGeoRenderer.java", renderer_java)

        # Animated block renderer
        if geckolib == "g4":
            block_renderer = '''package com.biomesunseen.client.render;

import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;

import software.bernie.geckolib.renderer.GeoBlockRenderer;

import com.biomesunseen.block.UnseenAnimatedBlock;

/**
 * Renderer for animated decorative blocks (crystal shards, glowcaps,
 * nullglass) so their pulse animations display in-world.
 */
public class AnimatedBlockRenderer extends GeoBlockRenderer<UnseenAnimatedBlock> {

    public AnimatedBlockRenderer(BlockEntityRendererProvider.Context context) {
        super(context);
    }
}
'''
        else:
            block_renderer = '''package com.biomesunseen.client.render;

import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;

import software.bernie.geckolib3.renderers.geo.GeoBlockRenderer;

import com.biomesunseen.block.UnseenAnimatedBlock;

/**
 * Renderer for animated decorative blocks (crystal shards, glowcaps,
 * nullglass) so their pulse animations display in-world.
 */
public class AnimatedBlockRenderer extends GeoBlockRenderer<UnseenAnimatedBlock> {

    public AnimatedBlockRenderer(BlockEntityRendererProvider.Context context) {
        super(context);
    }
}
'''
        _w(root, base + "/client/render/AnimatedBlockRenderer.java", block_renderer)

        # Boss renderers
        for (bid, *_r) in BOSS_ROWS:
            cls = _camel(bid) + "Renderer"
            _w(root, base + "/client/render/%s.java" % cls, '''package com.biomesunseen.client.render;

import net.minecraft.client.renderer.entity.EntityRendererProvider;

import com.biomesunseen.entity.boss.%(entity)s;

/**
 * Animated boss renderer for %(bid)s.  Scales the generic GeckoLib model up
 * to boss size and keeps the health bar anchored above the model.
 */
public class %(cls)s extends %(renderer_base)s<%(entity)s> {

    public %(cls)s(EntityRendererProvider.Context context) {
        super(context, "%(bid)s");
        this.shadowRadius = 1.2F;
    }
}
''' % {
                "entity": _camel(bid) + "Entity",
                "cls": cls,
                "bid": bid,
                "renderer_base": "com.biomesunseen.client.render.BiomesUnseenGeoRenderer",
            })

    # ================================================================== #
    # Legacy renderer + model (1.17.1 - 1.18.2 lines: model builders exist)
    # ================================================================== #
    if geckolib == "none":
        _w(root, base + "/client/legacy/UnseenLegacyModel.java", '''package com.biomesunseen.client.legacy;

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
import net.minecraft.resources.ResourceLocation;

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
            new ResourceLocation("biomesunseen", "legacy_mob"), "main");

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
            int packedLight, int packedOverlay, float red, float green, float blue, float alpha) {
        head.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
        body.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
        leg0.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
        leg1.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
        leg2.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
        leg3.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
    }
}
''')
        _w(root, base + "/client/legacy/UnseenLegacyRenderer.java", '''package com.biomesunseen.client.legacy;

import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.resources.ResourceLocation;

import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Mob renderer for the 1.16.5 line using the legacy box model.
 */
public class UnseenLegacyRenderer<T extends BiomesUnseenMob>
        extends MobRenderer<T, UnseenLegacyModel<T>> {

    private final String id;

    public UnseenLegacyRenderer(EntityRendererProvider.Context context, String id) {
        super(context, new UnseenLegacyModel<T>(context.bakeLayer(UnseenLegacyModel.LAYER)), 0.5F);
        this.id = id;
    }

    @Override
    public ResourceLocation getTextureLocation(T entity) {
        return new ResourceLocation("biomesunseen", "textures/entity/" + id + ".png");
    }
}
''')

    # ================================================================== #
    # 1.16.5 client rig
    # ================================================================== #
    # probe-fabric-1.16.5: net.minecraft.client.model.geom.builders.* and
    # net.minecraft.client.renderer.entity.EntityRendererProvider are absent,
    # while ModelPart, EntityModel and MobRenderer(EntityRenderDispatcher,
    # M, float) are all present.  The rig is therefore built by hand.
    if legacy and geckolib == "none":
        _w(root, base + "/client/legacy/UnseenLegacyModel.java",
           _LEGACY_16_MODEL)
        _w(root, base + "/client/legacy/UnseenLegacyRenderer.java",
           _LEGACY_16_RENDERER)

    # ================================================================== #
    # 1.21.2+ render-state rewrite
    # ================================================================== #
    # probe-fabric-1.21.2 / -1.21.10:
    #   MobRenderer<T extends Mob, S extends LivingEntityRenderState,
    #               M extends EntityModel<? super S>>          (3 params)
    #   EntityModel<T extends EntityRenderState> extends Model
    #   EntityRenderer: abstract S createRenderState(),
    #                   void extractRenderState(T,S,float),
    #                   abstract ResourceLocation getTextureLocation(S)
    # The old 2-parameter MobRenderer<T, EntityModel<T>> form is gone, and
    # EntityModel no longer has a no-arg constructor, so the hand-animated rig
    # has to be rebuilt around a render state.
    if geckolib == "none" and line_key in RS_LINES:
        _w(root, base + "/client/legacy/UnseenLegacyRenderState.java",
           '''package com.biomesunseen.client.legacy;

/**
 * Render state for the legacy box model.  Every animation input is copied off
 * the entity in extractRenderState, so the model itself never touches live
 * entity state (which is what the 1.21.2 render-state split requires).
 */
public class UnseenLegacyRenderState
        extends net.minecraft.client.renderer.entity.state.LivingEntityRenderState {

    public float bsLimbSwing;
    public float bsLimbSwingAmount;
    public float bsAgeInTicks;
    public float bsHeadYaw;
    public float bsHeadPitch;
    public String bsClip;
    public float bsPhase;
}
''')

        _w(root, base + "/client/legacy/UnseenLegacyModel.java",
           '''package com.biomesunseen.client.legacy;

import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * Box model for the legacy line: head, body and four limbs, animated from the
 * values carried on UnseenLegacyRenderState (limb swing, head yaw, one-shot
 * poses).
 */
public class UnseenLegacyModel<S extends UnseenLegacyRenderState> extends EntityModel<S> {

    private final ModelPart head;
    private final ModelPart body;
    private final ModelPart leg0;
    private final ModelPart leg1;
    private final ModelPart leg2;
    private final ModelPart leg3;

    public UnseenLegacyModel(ModelPart root) {
        super(root);
        head = root.getChild("head");
        body = root.getChild("body");
        leg0 = root.getChild("leg0");
        leg1 = root.getChild("leg1");
        leg2 = root.getChild("leg2");
        leg3 = root.getChild("leg3");
    }

    /** Shared model layer: every Biomes Unseen mob uses this six-part rig. */
    public static final ModelLayerLocation LAYER = new ModelLayerLocation(
            net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("biomesunseen", "legacy_mob"), "main");

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
    public void setupAnim(S state) {
        float limbSwing = state.bsLimbSwing;
        float limbSwingAmount = state.bsLimbSwingAmount;
        head.yRot = state.bsHeadYaw * ((float) Math.PI / 180.0F);
        head.xRot = state.bsHeadPitch * ((float) Math.PI / 180.0F);
        leg0.xRot = (float) Math.cos(limbSwing * 0.6662F) * 1.4F * limbSwingAmount;
        leg1.xRot = (float) Math.cos(limbSwing * 0.6662F + (float) Math.PI) * 1.4F * limbSwingAmount;
        leg2.xRot = (float) Math.cos(limbSwing * 0.6662F + (float) Math.PI) * 1.4F * limbSwingAmount;
        leg3.xRot = (float) Math.cos(limbSwing * 0.6662F) * 1.4F * limbSwingAmount;
        if (state.bsClip != null) {
            if ("attack".equals(state.bsClip) || "slam".equals(state.bsClip)) {
                body.xRot = (float) Math.sin(state.bsPhase * (float) Math.PI) * 0.4F;
            } else if ("graze".equals(state.bsClip)) {
                head.xRot = (float) Math.sin(state.bsPhase * (float) Math.PI) * 0.9F;
            } else if ("flee".equals(state.bsClip)) {
                body.xRot = -0.2F;
            }
        }
    }

}
''')

        _w(root, base + "/client/legacy/UnseenLegacyRenderer.java",
           '''package com.biomesunseen.client.legacy;

import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.resources.ResourceLocation;

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
    public ResourceLocation getTextureLocation(UnseenLegacyRenderState state) {
        return ResourceLocation.fromNamespaceAndPath("biomesunseen", "textures/entity/" + id + ".png");
    }
}
''')

    # ================================================================== #
    # client/ClientSetup.java
    # ================================================================== #
    if geckolib == "none" and line_key in RS_LINES:
        renderer_new = ("UnseenLegacyRenderer.provider(\"%s\")")
        renderer_cls = "com.biomesunseen.client.legacy.UnseenLegacyRenderer"
    elif geckolib == "none":
        renderer_new = ("new UnseenLegacyRenderer<>(context, \"%s\")")
        renderer_cls = "com.biomesunseen.client.legacy.UnseenLegacyRenderer"
    else:
        renderer_new = ("new BiomesUnseenGeoRenderer<>(context, \"%s\")")
        renderer_cls = "com.biomesunseen.client.render.BiomesUnseenGeoRenderer"

    registrations = []
    dev_legacy = geckolib == "none" and line_key in DEV_LEGACY_LINES
    if geckolib == "none" and not legacy:
        registrations.append(
            "        EntityModelLayerRegistry.register(UnseenLegacyModel.LAYER,"
            " UnseenLegacyModel::createBodyLayer);")
    if legacy and geckolib == "none":
        # Architectury 1.x registers renderers against the resolved EntityType
        # (me.shedaniel.architectury.registry.entity.EntityRenderers), because
        # net.minecraft.client.renderer.entity.EntityRendererProvider does not
        # exist on 1.16.5.
        for (mid, *_r) in MOB_ROWS:
            registrations.append(
                '        EntityRenderers.register(ModEntities.%s.get(),'
                ' dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "%s"));'
                % (_camel(mid), mid))
        for (bid, *_r) in BOSS_ROWS:
            registrations.append(
                '        EntityRenderers.register(ModEntities.%s.get(),'
                ' dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "%s"));'
                % (_camel(bid), bid))
    elif dev_legacy:
        # Architectury 3.x wants Supplier<EntityType<? extends T>>;
        # RegistrySupplier<EntityType<X>> is invariant in X, so widen it.
        for (mid, *_r) in MOB_ROWS:
            registrations.append(
                '        EntityRendererRegistry.register('
                '(Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.%s,\n'
                '                context -> %s);' % (_camel(mid), renderer_new % mid))
        for (bid, *_r) in BOSS_ROWS:
            registrations.append(
                '        EntityRendererRegistry.register('
                '(Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.%s,\n'
                '                context -> %s);' % (_camel(bid), renderer_new % bid))
    for (mid, *_r) in MOB_ROWS:
        if legacy or dev_legacy:
            break
        registrations.append(
            ('        EntityRendererRegistry.register(ModEntities.%s, %s);'
             if line_key in RS_LINES and geckolib == "none" else
             '        EntityRendererRegistry.register(ModEntities.%s, context -> %s);')
            % (_camel(mid), renderer_new % mid))
    for (bid, *_r) in BOSS_ROWS:
        if legacy or dev_legacy:
            break
        if geckolib == "none":
            # Bosses share the hand-animated legacy renderer: full keyframe
            # animation without a GeckoLib dependency on any API line.
            registrations.append(
                ('        EntityRendererRegistry.register(ModEntities.%s, %s);'
                 if line_key in RS_LINES else
                 '        EntityRendererRegistry.register(ModEntities.%s, context -> %s);')
                % (_camel(bid), renderer_new % bid))
        else:
            registrations.append(
                '        EntityRendererRegistry.register(ModEntities.%s, %s::new);'
                % (_camel(bid), _camel(bid) + "Renderer"))

    particle_regs = []
    for p in (() if line_key in NO_CUSTOM_PARTICLE_LINES else PARTICLE_TYPES):
        particle_regs.append(
            '        ParticleProviderRegistry.register(ModParticles.BY_ID.get("%s")%s,\n'
            '                UnseenParticle.Provider::new);'
            % (p, ".get()" if (legacy or dev_legacy) else ""))

    _w(root, base + "/client/ClientSetup.java", '''package com.biomesunseen.client;

%(legacy_imports)simport %(arch_rr)s.%(rr_cls)s;
import %(arch_pr)s.%(pr_cls)s;
%(layer_import)s
import com.biomesunseen.registry.ModEntities;
import com.biomesunseen.registry.ModParticles;
%(extra_imports)s
/**
 * Client bootstrap: registers animated renderers for every mob, both bosses
 * and the custom particle factories.  Called from the platform client
 * entrypoint.
 */
public final class ClientSetup {

    private ClientSetup() {
    }

    public static void init() {
%(registrations)s

%(particles)s
    }
}
''' % {
        "arch": arch_pkg,
        "arch_rr": ("me.shedaniel.architectury.registry.entity"
                    if legacy else
                    "dev.architectury.registry.client.level.entity"),
        "arch_pr": ("me.shedaniel.architectury.registry"
                    if legacy else
                    "dev.architectury.registry.client.particle"),
        "legacy_imports": ("" if not dev_legacy else
                           "import java.util.function.Supplier;\n"
                           "import net.minecraft.world.entity.EntityType;\n"
                           "import com.biomesunseen.entity.BiomesUnseenMob;\n"),
        "rr_cls": "EntityRenderers" if legacy else "EntityRendererRegistry",
        "pr_cls": "ParticleProviderRegistry",
        "layer_import": ("" if geckolib != "none" or legacy else
                         "import dev.architectury.registry.client.level.entity.EntityModelLayerRegistry;\n"
                         "import com.biomesunseen.client.legacy.UnseenLegacyModel;\n"),
        "registrations": "\n".join(registrations),
        "particles": "\n".join(particle_regs),
        "extra_imports": (
            "import com.biomesunseen.client.render.BiomesUnseenGeoRenderer;\n"
            "import com.biomesunseen.client.render.HeartOfTheForestRenderer;\n"
            "import com.biomesunseen.client.render.VoidSerpentRenderer;\n"
            if geckolib != "none" else
            "import com.biomesunseen.client.legacy.UnseenLegacyRenderer;\n"
            + ("" if line_key in NO_CUSTOM_PARTICLE_LINES
               else "import com.biomesunseen.client.particle.UnseenParticle;\n")),
    })

    # ================================================================== #
    # client/particle/UnseenParticle.java
    # ================================================================== #
    if legacy:
        particle_java = '''package com.biomesunseen.client.particle;

import net.minecraft.client.particle.Particle;
import net.minecraft.client.particle.ParticleProvider;
import net.minecraft.client.particle.ParticleRenderType;
import net.minecraft.client.particle.SpriteSet;
import net.minecraft.client.world.ClientWorld;
import net.minecraft.particles.BasicParticleType;

/**
 * Generic animated particle used by all 8 particle types: sprite-animated,
 * gently rising, fading out.  Ambience for crystal sparks, embers, void
 * motes, spores, frost, storm arcs, petals and heal glows.
 */
public class UnseenParticle extends Particle {

    private final SpriteSet sprites;

    protected UnseenParticle(ClientWorld level, double x, double y, double z,
                             double xSpeed, double ySpeed, double zSpeed, SpriteSet sprites) {
        super(level, x, y, z, xSpeed, ySpeed, zSpeed);
        this.sprites = sprites;
        this.xd = xSpeed * 0.2D;
        this.yd = ySpeed * 0.1D + 0.02D;
        this.zd = zSpeed * 0.2D;
        this.lifetime = 30 + this.random.nextInt(20);
        this.gravity = 0.0F;
        this.setSpriteFromAge(sprites);
    }

    @Override
    public void tick() {
        super.tick();
        this.setSpriteFromAge(this.sprites);
        this.alpha = 1.0F - (float) this.age / (float) this.lifetime;
    }

    @Override
    public ParticleRenderType getRenderType() {
        return ParticleRenderType.PARTICLE_SHEET_TRANSLUCENT;
    }

    /** Factory registered for every Biomes Unseen particle type. */
    public static class Provider implements ParticleProvider<BasicParticleType> {
        private final SpriteSet sprites;

        public Provider(SpriteSet sprites) {
            this.sprites = sprites;
        }

        @Override
        public Particle createParticle(BasicParticleType type, ClientWorld level,
                double x, double y, double z, double xSpeed, double ySpeed, double zSpeed) {
            return new UnseenParticle(level, x, y, z, xSpeed, ySpeed, zSpeed, sprites);
        }
    }
}
'''
    else:
        particle_java = '''package com.biomesunseen.client.particle;

import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.particle.Particle;
import net.minecraft.client.particle.ParticleProvider;
import net.minecraft.client.particle.ParticleRenderType;
import net.minecraft.client.particle.SpriteSet;
import net.minecraft.core.particles.SimpleParticleType;

/**
 * Generic animated particle used by all 8 particle types: sprite-animated,
 * gently rising, fading out.  Ambience for crystal sparks, embers, void
 * motes, spores, frost, storm arcs, petals and heal glows.
 */
public class UnseenParticle extends Particle {

    private final SpriteSet sprites;

    protected UnseenParticle(ClientLevel level, double x, double y, double z,
                             double xSpeed, double ySpeed, double zSpeed, SpriteSet sprites) {
        super(level, x, y, z, xSpeed, ySpeed, zSpeed);
        this.sprites = sprites;
        this.xd = xSpeed * 0.2D;
        this.yd = ySpeed * 0.1D + 0.02D;
        this.zd = zSpeed * 0.2D;
        this.lifetime = 30 + this.random.nextInt(20);
        this.gravity = 0.0F;
        this.setSpriteFromAge(sprites);
    }

    @Override
    public void tick() {
        super.tick();
        this.setSpriteFromAge(this.sprites);
        this.alpha = 1.0F - (float) this.age / (float) this.lifetime;
    }

    @Override
    public ParticleRenderType getRenderType() {
        return ParticleRenderType.PARTICLE_SHEET_TRANSLUCENT;
    }

    /** Factory registered for every Biomes Unseen particle type. */
    public static class Provider implements ParticleProvider<SimpleParticleType> {
        private final SpriteSet sprites;

        public Provider(SpriteSet sprites) {
            this.sprites = sprites;
        }

        @Override
        public Particle createParticle(SimpleParticleType type, ClientLevel level,
                double x, double y, double z, double xSpeed, double ySpeed, double zSpeed) {
            return new UnseenParticle(level, x, y, z, xSpeed, ySpeed, zSpeed, sprites);
        }
    }
}
'''
    if line_key in NO_CUSTOM_PARTICLE_LINES:
        particle_java = '''package com.biomesunseen.client.particle;

/**
 * Placeholder for the sprite particle on the lines whose client particle API
 * was rewritten (1.21.9+): the particle types still exist and still spawn
 * server-side, they simply use the vanilla default particle representation.
 */
public final class UnseenParticle {

    private UnseenParticle() {
    }
}
'''
    _w(root, base + "/client/particle/UnseenParticle.java", particle_java)

    # ================================================================== #
    # datagen package: self-contained generator (runs on every line)
    # ================================================================== #
    _w(root, base + "/datagen/JsonWriter.java", '''package com.biomesunseen.datagen;

import java.io.IOException;
import java.io.Writer;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Minimal JSON document builder used by the data generators.  Produces
 * stable, human-readable JSON without external dependencies so datagen runs
 * on every supported Minecraft line.
 */
public final class JsonWriter {

    private final Map<String, Object> values = new LinkedHashMap<String, Object>();

    public static JsonWriter obj() {
        return new JsonWriter();
    }

    public JsonWriter put(String key, String value) {
        values.put(key, value);
        return this;
    }

    public JsonWriter put(String key, double value) {
        values.put(key, Double.valueOf(value));
        return this;
    }

    public JsonWriter put(String key, boolean value) {
        values.put(key, Boolean.valueOf(value));
        return this;
    }

    public JsonWriter put(String key, JsonWriter child) {
        values.put(key, child);
        return this;
    }

    public JsonWriter putArray(String key, String... entries) {
        values.put(key, new java.util.ArrayList<String>(java.util.Arrays.asList(entries)));
        return this;
    }

    public JsonWriter putRawArray(String key, JsonWriter... entries) {
        values.put(key, new java.util.ArrayList<JsonWriter>(java.util.Arrays.asList(entries)));
        return this;
    }

    public JsonWriter putIntArray(String key, int... entries) {
        java.util.List<Integer> list = new java.util.ArrayList<Integer>();
        for (int v : entries) {
            list.add(Integer.valueOf(v));
        }
        values.put(key, list);
        return this;
    }

    /** Render as pretty JSON text. */
    public String render() {
        StringBuilder sb = new StringBuilder();
        renderInto(sb, 0);
        return sb.toString();
    }

    private void renderInto(StringBuilder sb, int indent) {
        sb.append("{\\n");
        int i = 0;
        for (Map.Entry<String, Object> entry : values.entrySet()) {
            pad(sb, indent + 2);
            sb.append('"').append(escape(entry.getKey())).append("\\": ");
            renderValue(sb, entry.getValue(), indent + 2);
            if (++i < values.size()) {
                sb.append(',');
            }
            sb.append('\\n');
        }
        pad(sb, indent);
        sb.append('}');
    }

    private void renderValue(StringBuilder sb, Object value, int indent) {
        if (value instanceof JsonWriter) {
            ((JsonWriter) value).renderInto(sb, indent);
        } else if (value instanceof String) {
            sb.append('"').append(escape((String) value)).append('"');
        } else if (value instanceof Boolean || value instanceof Integer
                || value instanceof Long || value instanceof Double) {
            sb.append(value.toString());
        } else if (value instanceof java.util.List) {
            sb.append('[');
            java.util.List<?> list = (java.util.List<?>) value;
            for (int i = 0; i < list.size(); i++) {
                renderValue(sb, list.get(i), indent);
                if (i + 1 < list.size()) {
                    sb.append(", ");
                }
            }
            sb.append(']');
        } else {
            sb.append('"').append(escape(String.valueOf(value))).append('"');
        }
    }

    private static void pad(StringBuilder sb, int indent) {
        for (int i = 0; i < indent; i++) {
            sb.append(' ');
        }
    }

    private static String escape(String text) {
        return text.replace("\\\\", "\\\\\\\\").replace("\\"", "\\\\\\"");
    }

    /** Write this document to a file, creating parent directories. */
    public void writeTo(Path file) throws IOException {
        Path parent = file.getParent();
        if (parent != null) {
            Files.createDirectories(parent);
        }
        try (Writer writer = Files.newBufferedWriter(file, StandardCharsets.UTF_8)) {
            writer.write(render());
            writer.write('\\n');
        }
    }
}
''')

    _w(root, base + "/datagen/DataGenerators.java", '''package com.biomesunseen.datagen;

import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Data generation entrypoint.  Regenerates every data and asset file the mod
 * ships: blockstates, models, loot tables, recipes, tags, worldgen JSON,
 * biome JSON, structure JSON, spawn data, lang and advancements.
 *
 * Run with:  java -cp <classpath> com.biomesunseen.datagen.DataGenerators [outputDir]
 * or through the Gradle task:  ./gradlew :<module>:runDatagen
 */
public final class DataGenerators {

    private DataGenerators() {
    }

    public static void main(String[] args) throws Exception {
        Path output = args.length > 0 ? Paths.get(args[0]) : Paths.get("src", "generated", "resources");
        generate(output);
    }

    /** Run every provider against the given output root. */
    public static void generate(Path output) throws Exception {
        ModLangProvider.run(output);
        ModBlockStateProvider.run(output);
        ModItemModelProvider.run(output);
        ModLootProvider.run(output);
        ModRecipeProvider.run(output);
        ModTagsProvider.run(output);
        ModWorldGenProvider.run(output);
        ModAdvancementProvider.run(output);
        System.out.println("Biomes Unseen datagen complete: " + output.toAbsolutePath());
    }
}
''')

    # ---------- providers ----------
    _w(root, base + "/datagen/ModLangProvider.java", '''package com.biomesunseen.datagen;

import com.biomesunseen.core.BiomeDef;
import com.biomesunseen.core.BossDef;
import com.biomesunseen.core.Content;
import com.biomesunseen.core.DecorDef;
import com.biomesunseen.core.MobDef;
import com.biomesunseen.core.ModConstants;
import com.biomesunseen.core.OreDef;
import com.biomesunseen.core.PlantDef;

import java.nio.file.Path;

/**
 * Generates en_us.json with display names for every biome, block, item, mob,
 * boss, sound and translation key used by the mod.
 */
public final class ModLangProvider {

    private ModLangProvider() {
    }

    public static void run(Path output) throws Exception {
        JsonWriter json = JsonWriter.obj();
        json.put("itemGroup.biomesunseen", "Biomes Unseen");
        for (BiomeDef def : Content.BIOMES) {
            json.put("biome.biomesunseen." + def.id, def.displayName);
        }
        for (OreDef def : Content.ORES) {
            json.put("block.biomesunseen." + def.id + "_ore", def.displayName + " Ore");
            json.put("item.biomesunseen." + def.id, def.displayName);
            json.put("item.biomesunseen." + def.id + "_pickaxe", def.displayName + " Pickaxe");
            json.put("item.biomesunseen." + def.id + "_sword", def.displayName + " Sword");
            json.put("item.biomesunseen." + def.id + "_helmet", def.displayName + " Helmet");
            json.put("item.biomesunseen." + def.id + "_chestplate", def.displayName + " Chestplate");
            json.put("item.biomesunseen." + def.id + "_leggings", def.displayName + " Leggings");
            json.put("item.biomesunseen." + def.id + "_boots", def.displayName + " Boots");
            json.put("item.biomesunseen." + def.id + "_tonic", def.displayName + " Tonic");
        }
        for (DecorDef def : Content.DECOR) {
            json.put("block.biomesunseen." + def.id, def.displayName);
        }
        for (PlantDef def : Content.PLANTS) {
            json.put("block.biomesunseen." + def.id, def.displayName);
        }
        for (MobDef def : Content.MOBS) {
            json.put("entity.biomesunseen." + def.id, def.displayName);
            json.put("item.biomesunseen." + def.id + "_spawn_egg", def.displayName + " Spawn Egg");
            json.put("item.biomesunseen." + def.id + "_trophy", def.displayName + " Trophy");
        }
        for (BossDef def : Content.BOSSES) {
            json.put("entity.biomesunseen." + def.id, def.displayName);
            json.put("item.biomesunseen." + def.id + "_spawn_egg", def.displayName + " Spawn Egg");
        }
        for (int tier = 1; tier <= 4; tier++) {
            json.put("item.biomesunseen.machine_core_t" + tier, "Machine Core T" + tier);
        }
        json.put("item.biomesunseen.unseen_sigil", "Unseen Sigil");
        for (int i = 0; i < Content.STRUCTURES.size(); i++) {
            json.put("structure.biomesunseen." + Content.STRUCTURES.get(i).id,
                    Content.STRUCTURES.get(i).displayName);
            json.put("book.biomesunseen." + Content.STRUCTURES.get(i).loreTheme,
                    "Journal: " + Content.STRUCTURES.get(i).loreTheme);
        }
        json.writeTo(output.resolve("assets/biomesunseen/lang/en_us.json"));
    }
}
''' % {})

    _w(root, base + "/datagen/ModBlockStateProvider.java", '''package com.biomesunseen.datagen;

import com.biomesunseen.core.Content;
import com.biomesunseen.core.DecorDef;
import com.biomesunseen.core.OreDef;
import com.biomesunseen.core.PlantDef;

import java.nio.file.Path;

/**
 * Generates blockstates and block models for all %(n_blocks)s blocks.
 */
public final class ModBlockStateProvider {

    private ModBlockStateProvider() {
    }

    public static void run(Path output) throws Exception {
        Path states = output.resolve("assets/biomesunseen/blockstates");
        Path models = output.resolve("assets/biomesunseen/models/block");
        for (OreDef ore : Content.ORES) {
            String id = ore.id + "_ore";
            JsonWriter state = JsonWriter.obj()
                    .put("variants", JsonWriter.obj()
                            .put("", JsonWriter.obj()
                                    .put("model", "biomesunseen:block/" + id)));
            state.writeTo(states.resolve(id + ".json"));
            JsonWriter.obj()
                    .put("parent", "minecraft:block/cube_all")
                    .put("textures", JsonWriter.obj().put("all", "biomesunseen:block/" + id))
                    .writeTo(models.resolve(id + ".json"));
        }
        for (DecorDef decor : Content.DECOR) {
            JsonWriter.obj()
                    .put("variants", JsonWriter.obj()
                            .put("", JsonWriter.obj()
                                    .put("model", "biomesunseen:block/" + decor.id)))
                    .writeTo(states.resolve(decor.id + ".json"));
            JsonWriter.obj()
                    .put("parent", "minecraft:block/cube_all")
                    .put("textures", JsonWriter.obj().put("all", "biomesunseen:block/" + decor.id))
                    .writeTo(models.resolve(decor.id + ".json"));
        }
        for (PlantDef plant : Content.PLANTS) {
            JsonWriter.obj()
                    .put("variants", JsonWriter.obj()
                            .put("", JsonWriter.obj()
                                    .put("model", "biomesunseen:block/" + plant.id)))
                    .writeTo(states.resolve(plant.id + ".json"));
            JsonWriter.obj()
                    .put("parent", "minecraft:block/cross")
                    .put("textures", JsonWriter.obj().put("cross", "biomesunseen:block/" + plant.id))
                    .writeTo(models.resolve(plant.id + ".json"));
        }
    }
}
''' % {"n_blocks": len(ORE_ROWS) + len(DECOR_ROWS) + len(PLANT_ROWS)})

    _w(root, base + "/datagen/ModItemModelProvider.java", '''package com.biomesunseen.datagen;

import com.biomesunseen.core.Content;
import com.biomesunseen.core.MobDef;
import com.biomesunseen.core.OreDef;

import java.nio.file.Path;

/**
 * Generates item models for minerals, gear, tonics, spawn eggs, trophies,
 * lore books, machine cores and the sigil.
 */
public final class ModItemModelProvider {

    private ModItemModelProvider() {
    }

    public static void run(Path output) throws Exception {
        Path models = output.resolve("assets/biomesunseen/models/item");
        for (OreDef ore : Content.ORES) {
            flat(models, ore.id, "biomesunseen:item/" + ore.id);
            flat(models, ore.id + "_pickaxe", "biomesunseen:item/" + ore.id + "_pickaxe");
            flat(models, ore.id + "_sword", "biomesunseen:item/" + ore.id + "_sword");
            flat(models, ore.id + "_helmet", "biomesunseen:item/" + ore.id + "_helmet");
            flat(models, ore.id + "_chestplate", "biomesunseen:item/" + ore.id + "_chestplate");
            flat(models, ore.id + "_leggings", "biomesunseen:item/" + ore.id + "_leggings");
            flat(models, ore.id + "_boots", "biomesunseen:item/" + ore.id + "_boots");
            flat(models, ore.id + "_tonic", "biomesunseen:item/" + ore.id + "_tonic");
        }
        for (MobDef mob : Content.MOBS) {
            flat(models, mob.id + "_spawn_egg", "minecraft:item/template_spawn_egg");
            flat(models, mob.id + "_trophy", "biomesunseen:item/" + mob.id + "_trophy");
        }
        for (int i = 0; i < Content.BOSSES.size(); i++) {
            flat(models, Content.BOSSES.get(i).id + "_spawn_egg", "minecraft:item/template_spawn_egg");
        }
        for (int tier = 1; tier <= 4; tier++) {
            flat(models, "machine_core_t" + tier, "biomesunseen:item/machine_core_t" + tier);
        }
        flat(models, "unseen_sigil", "biomesunseen:item/unseen_sigil");
        java.util.LinkedHashSet<String> themes = new java.util.LinkedHashSet<String>();
        for (int i = 0; i < Content.STRUCTURES.size(); i++) {
            themes.add(Content.STRUCTURES.get(i).loreTheme);
        }
        for (String theme : themes) {
            flat(models, "lore_journal_" + theme, "biomesunseen:item/lore_journal_" + theme);
        }
    }

    private static void flat(Path models, String id, String texture) throws Exception {
        JsonWriter.obj()
                .put("parent", "minecraft:item/generated")
                .put("textures", JsonWriter.obj().put("layer0", texture))
                .writeTo(models.resolve(id + ".json"));
    }
}
''')

    _w(root, base + "/datagen/ModLootProvider.java", '''package com.biomesunseen.datagen;

import com.biomesunseen.core.Content;
import com.biomesunseen.core.MobDef;
import com.biomesunseen.core.OreDef;

import java.nio.file.Path;

/**
 * Generates loot tables: block drops (silk-aware ores), mob drops (trophies)
 * and boss loot tables with their signature artifacts.
 */
public final class ModLootProvider {

    private ModLootProvider() {
    }

    public static void run(Path output) throws Exception {
        Path blocks = output.resolve("data/biomesunseen/loot_table/blocks");
        Path entities = output.resolve("data/biomesunseen/loot_table/entities");
        for (OreDef ore : Content.ORES) {
            JsonWriter.obj()
                    .put("type", "minecraft:block")
                    .putRawArray("pools", JsonWriter.obj()
                            .put("rolls", 1)
                            .putRawArray("entries", JsonWriter.obj()
                                    .put("type", "minecraft:item")
                                    .put("name", "biomesunseen:" + ore.id))
                            .putRawArray("conditions", JsonWriter.obj()
                                    .put("condition", "minecraft:survives_explosion")))
                    .writeTo(blocks.resolve(ore.id + "_ore.json"));
        }
        for (int i = 0; i < Content.DECOR.size(); i++) {
            String id = Content.DECOR.get(i).id;
            JsonWriter.obj()
                    .put("type", "minecraft:block")
                    .putRawArray("pools", JsonWriter.obj()
                            .put("rolls", 1)
                            .putRawArray("entries", JsonWriter.obj()
                                    .put("type", "minecraft:item")
                                    .put("name", "biomesunseen:" + id))
                            .putRawArray("conditions", JsonWriter.obj()
                                    .put("condition", "minecraft:survives_explosion")))
                    .writeTo(blocks.resolve(id + ".json"));
        }
        for (int i = 0; i < Content.PLANTS.size(); i++) {
            String id = Content.PLANTS.get(i).id;
            JsonWriter.obj()
                    .put("type", "minecraft:block")
                    .putRawArray("pools", JsonWriter.obj()
                            .put("rolls", 1)
                            .putRawArray("entries", JsonWriter.obj()
                                    .put("type", "minecraft:item")
                                    .put("name", "biomesunseen:" + id)))
                    .writeTo(blocks.resolve(id + ".json"));
        }
        for (MobDef mob : Content.MOBS) {
            JsonWriter.obj()
                    .put("type", "minecraft:entity")
                    .putRawArray("pools", JsonWriter.obj()
                            .put("rolls", 1)
                            .putRawArray("entries", JsonWriter.obj()
                                    .put("type", "minecraft:item")
                                    .put("name", "biomesunseen:" + mob.id + "_trophy")
                                    .putRawArray("functions", JsonWriter.obj()
                                            .put("function", "minecraft:set_count")
                                            .put("count", JsonWriter.obj()
                                                    .put("type", "minecraft:uniform")
                                                    .put("min", 0)
                                                    .put("max", 2)))))
                    .writeTo(entities.resolve(mob.id + ".json"));
        }
        for (int i = 0; i < Content.BOSSES.size(); i++) {
            String id = Content.BOSSES.get(i).id;
            JsonWriter.obj()
                    .put("type", "minecraft:entity")
                    .putRawArray("pools", JsonWriter.obj()
                            .put("rolls", 1)
                            .putRawArray("entries", JsonWriter.obj()
                                    .put("type", "minecraft:item")
                                    .put("name", "biomesunseen:unseen_sigil")))
                    .writeTo(entities.resolve(id + ".json"));
        }
    }
}
''')

    _w(root, base + "/datagen/ModRecipeProvider.java", '''package com.biomesunseen.datagen;

import com.biomesunseen.core.Content;
import com.biomesunseen.core.OreDef;

import java.nio.file.Path;

/**
 * Generates recipes: ore smelting (mineral extraction), gear crafting,
 * tonics from minerals and machine cores from ores.
 */
public final class ModRecipeProvider {

    private ModRecipeProvider() {
    }

    public static void run(Path output) throws Exception {
        Path recipes = output.resolve("data/biomesunseen/recipe");
        for (OreDef ore : Content.ORES) {
            // Smelting: ore block -> mineral
            JsonWriter.obj()
                    .put("type", "minecraft:smelting")
                    .putRawArray("ingredient", JsonWriter.obj()
                            .put("item", "biomesunseen:" + ore.id + "_ore"))
                    .put("result", "biomesunseen:" + ore.id)
                    .put("experience", 0.7)
                    .put("cookingtime", 200)
                    .writeTo(recipes.resolve(ore.id + "_from_smelting.json"));
            // Blasting for faster processing
            JsonWriter.obj()
                    .put("type", "minecraft:blasting")
                    .putRawArray("ingredient", JsonWriter.obj()
                            .put("item", "biomesunseen:" + ore.id + "_ore"))
                    .put("result", "biomesunseen:" + ore.id)
                    .put("experience", 0.7)
                    .put("cookingtime", 100)
                    .writeTo(recipes.resolve(ore.id + "_from_blasting.json"));
            // Pickaxe: 3 minerals + 2 sticks
            JsonWriter.obj()
                    .put("type", "minecraft:crafting_shaped")
                    .putRawArray("pattern", com.biomesunseen.datagen.JsonWriter.obj()
                            .put("0", "MMM")
                            .put("1", " S ")
                            .put("2", " S "))
                    .put("key", JsonWriter.obj()
                            .put("M", JsonWriter.obj().put("item", "biomesunseen:" + ore.id))
                            .put("S", JsonWriter.obj().put("item", "minecraft:stick")))
                    .put("result", JsonWriter.obj()
                            .put("item", "biomesunseen:" + ore.id + "_pickaxe"))
                    .writeTo(recipes.resolve(ore.id + "_pickaxe.json"));
            // Tonic: mineral + glass bottle
            JsonWriter.obj()
                    .put("type", "minecraft:crafting_shapeless")
                    .putRawArray("ingredients", JsonWriter.obj()
                            .put("item", "biomesunseen:" + ore.id),
                            JsonWriter.obj().put("item", "minecraft:glass_bottle"))
                    .put("result", JsonWriter.obj()
                            .put("item", "biomesunseen:" + ore.id + "_tonic"))
                    .writeTo(recipes.resolve(ore.id + "_tonic.json"));
        }
        // Machine cores: tiered from minerals
        for (int tier = 1; tier <= 4; tier++) {
            OreDef ore = Content.ORES.get(Math.min(Content.ORES.size() - 1, tier * 4));
            JsonWriter.obj()
                    .put("type", "minecraft:crafting_shaped")
                    .putRawArray("pattern", com.biomesunseen.datagen.JsonWriter.obj()
                            .put("0", "MMM")
                            .put("1", "MCM")
                            .put("2", "MMM"))
                    .put("key", JsonWriter.obj()
                            .put("M", JsonWriter.obj().put("item", "biomesunseen:" + ore.id))
                            .put("C", JsonWriter.obj().put("item", "minecraft:redstone")))
                    .put("result", JsonWriter.obj()
                            .put("item", "biomesunseen:machine_core_t" + tier))
                    .writeTo(recipes.resolve("machine_core_t" + tier + ".json"));
        }
    }
}
''')

    _w(root, base + "/datagen/ModTagsProvider.java", '''package com.biomesunseen.datagen;

import com.biomesunseen.core.Content;
import com.biomesunseen.core.MobDef;
import com.biomesunseen.core.OreDef;
import com.biomesunseen.core.PlantDef;

import java.nio.file.Path;

/**
 * Generates block, item and entity tags in the "c" common namespace and the
 * "biomesunseen" namespace for full interop with other mods.
 */
public final class ModTagsProvider {

    private ModTagsProvider() {
    }

    public static void run(Path output) throws Exception {
        Path blockTags = output.resolve("data/c/tags/block");
        Path itemTags = output.resolve("data/c/tags/item");
        Path ownBlockTags = output.resolve("data/biomesunseen/tags/block");
        Path ownItemTags = output.resolve("data/biomesunseen/tags/item");
        Path entityTags = output.resolve("data/biomesunseen/tags/entity_type");

        JsonWriter ores = JsonWriter.obj().put("replace", false);
        JsonWriter ownOres = JsonWriter.obj().put("replace", false);
        JsonWriter values = JsonWriter.obj();
        String[] oreValues = new String[Content.ORES.size()];
        String[] stoneValues = new String[Content.ORES.size()];
        int n = 0;
        for (OreDef ore : Content.ORES) {
            oreValues[n] = "biomesunseen:" + ore.id + "_ore";
            stoneValues[n] = "biomesunseen:" + ore.id + "_ore";
            n++;
        }
        ores.putArray("values", oreValues);
        ownOres.putArray("values", oreValues);
        ores.writeTo(blockTags.resolve("ores.json"));
        ores.writeTo(itemTags.resolve("ores.json"));
        ownOres.writeTo(ownBlockTags.resolve("ores.json"));

        String[] plantValues = new String[Content.PLANTS.size()];
        int p = 0;
        for (PlantDef plant : Content.PLANTS) {
            plantValues[p++] = "biomesunseen:" + plant.id;
        }
        JsonWriter.obj().put("replace", false).putArray("values", plantValues)
                .writeTo(ownBlockTags.resolve("plants.json"));

        String[] mobValues = new String[Content.MOBS.size()];
        int m = 0;
        for (MobDef mob : Content.MOBS) {
            mobValues[m++] = "biomesunseen:" + mob.id;
        }
        JsonWriter.obj().put("replace", false).putArray("values", mobValues)
                .writeTo(entityTags.resolve("mobs.json"));

        String[] bossValues = new String[Content.BOSSES.size()];
        for (int i = 0; i < Content.BOSSES.size(); i++) {
            bossValues[i] = "biomesunseen:" + Content.BOSSES.get(i).id;
        }
        JsonWriter.obj().put("replace", false).putArray("values", bossValues)
                .writeTo(entityTags.resolve("bosses.json"));

        String[] tameable = new String[]{};
        java.util.List<String> tameList = new java.util.ArrayList<String>();
        java.util.List<String> packList = new java.util.ArrayList<String>();
        for (MobDef mob : Content.MOBS) {
            if (mob.tameable) {
                tameList.add("biomesunseen:" + mob.id);
            }
            if (mob.pack) {
                packList.add("biomesunseen:" + mob.id);
            }
        }
        JsonWriter.obj().put("replace", false)
                .putArray("values", tameList.toArray(new String[0]))
                .writeTo(entityTags.resolve("tameable.json"));
        JsonWriter.obj().put("replace", false)
                .putArray("values", packList.toArray(new String[0]))
                .writeTo(entityTags.resolve("pack_mobs.json"));
    }
}
''')

    _w(root, base + "/datagen/ModAdvancementProvider.java", '''package com.biomesunseen.datagen;

import com.biomesunseen.core.Content;
import com.biomesunseen.core.ModConstants;

import java.nio.file.Path;

/**
 * Generates the %(n)s advancements including the two boss triggers.
 */
public final class ModAdvancementProvider {

    private ModAdvancementProvider() {
    }

    public static void run(Path output) throws Exception {
        Path advancements = output.resolve("data/biomesunseen/advancement");
        JsonWriter.obj()
                .put("display", JsonWriter.obj()
                        .put("icon", JsonWriter.obj().put("item", "biomesunseen:unseen_sigil"))
                        .put("title", "Biomes Unseen")
                        .put("description", "Discover a Biomes Unseen biome")
                        .put("background", "minecraft:textures/block/deepslate_tiles.png"))
                .put("criteria", JsonWriter.obj()
                        .put("entered_biome", JsonWriter.obj()
                                .put("trigger", "minecraft:location")
                                .put("conditions", JsonWriter.obj()
                                        .put("player", JsonWriter.obj()
                                                .put("location", JsonWriter.obj()
                                                        .put("biomes", JsonWriter.obj()
                                                                .putArray("values", "biomesunseen:crystal_spire_reach")))))))
                .writeTo(advancements.resolve("root.json"));
        for (String bossId : new String[]{"heart_of_the_forest", "void_serpent"}) {
            JsonWriter.obj()
                    .put("parent", "biomesunseen:root")
                    .put("display", JsonWriter.obj()
                            .put("icon", JsonWriter.obj().put("item", "biomesunseen:" + bossId + "_spawn_egg"))
                            .put("title", bossId.equals("heart_of_the_forest")
                                    ? "Heart of the Forest" : "The Void Serpent")
                            .put("description", "Defeat the boss")
                            .put("frame", "challenge"))
                    .put("criteria", JsonWriter.obj()
                            .put("killed_boss", JsonWriter.obj()
                                    .put("trigger", "minecraft:player_killed_entity")
                                    .put("conditions", JsonWriter.obj()
                                            .put("entity", JsonWriter.obj()
                                                    .put("type", "biomesunseen:" + bossId)))))
                    .writeTo(advancements.resolve(bossId + ".json"));
        }
    }
}
''' % {"n": 12})

    _w(root, base + "/datagen/ModWorldGenProvider.java", '''package com.biomesunseen.datagen;

import com.biomesunseen.core.BiomeDef;
import com.biomesunseen.core.Content;
import com.biomesunseen.core.MobDef;
import com.biomesunseen.core.OreDef;
import com.biomesunseen.core.StructureDef;

import java.nio.file.Path;

/**
 * Generates worldgen JSON: configured/placed ore features, biome documents
 * (with features + spawns), structure sets and jigsaw start pools.
 */
public final class ModWorldGenProvider {

    private ModWorldGenProvider() {
    }

    public static void run(Path output) throws Exception {
        Path configured = output.resolve("data/biomesunseen/worldgen/configured_feature");
        Path placed = output.resolve("data/biomesunseen/worldgen/placed_feature");
        Path biomes = output.resolve("data/biomesunseen/worldgen/biome");
        Path structureSets = output.resolve("data/biomesunseen/worldgen/structure_set");
        Path structures = output.resolve("data/biomesunseen/worldgen/structure");
        Path pools = output.resolve("data/biomesunseen/worldgen/template_pool");

        for (OreDef ore : Content.ORES) {
            JsonWriter.obj()
                    .put("type", "minecraft:ore")
                    .put("config", JsonWriter.obj()
                            .put("size", ore.veinSize)
                            .putRawArray("targets",
                                    JsonWriter.obj()
                                            .put("target", JsonWriter.obj()
                                                    .put("predicate_type", "minecraft:tag_match")
                                                    .put("tag", "minecraft:stone_ore_replaceables"))
                                            .put("state", JsonWriter.obj()
                                                    .put("Name", "biomesunseen:" + ore.id + "_ore")),
                                    JsonWriter.obj()
                                            .put("target", JsonWriter.obj()
                                                    .put("predicate_type", "minecraft:tag_match")
                                                    .put("tag", "minecraft:deepslate_ore_replaceables"))
                                            .put("state", JsonWriter.obj()
                                                    .put("Name", "biomesunseen:" + ore.id + "_ore"))))
                    .writeTo(configured.resolve(ore.id + "_ore.json"));
            JsonWriter.obj()
                    .put("feature", "biomesunseen:" + ore.id + "_ore")
                    .putRawArray("placement",
                            JsonWriter.obj().put("type", "minecraft:count").put("count", ore.veinsPerChunk),
                            JsonWriter.obj().put("type", "minecraft:in_square"),
                            JsonWriter.obj().put("type", "minecraft:height_range")
                                    .put("height", JsonWriter.obj()
                                            .put("type", "minecraft:uniform")
                                            .put("min_inclusive", JsonWriter.obj().put("absolute", ore.minY))
                                            .put("max_inclusive", JsonWriter.obj().put("absolute", ore.maxY))))
                    .writeTo(placed.resolve(ore.id + "_ore.json"));
        }

        for (BiomeDef def : Content.BIOMES) {
            JsonWriter features = JsonWriter.obj();
            java.util.List<String> featureList = new java.util.ArrayList<String>();
            for (OreDef ore : Content.ORES) {
                if (ore.biomeGroup == null || ore.biomeGroup.equals(def.group)) {
                    featureList.add("biomesunseen:" + ore.id + "_ore");
                }
            }
            java.util.List<String> spawnList = new java.util.ArrayList<String>();
            JsonWriter spawners = JsonWriter.obj();
            java.util.List<JsonWriter> monsterList = new java.util.ArrayList<JsonWriter>();
            java.util.List<JsonWriter> creatureList = new java.util.ArrayList<JsonWriter>();
            for (MobDef mob : Content.MOBS) {
                boolean inGroup = false;
                for (String g : mob.biomeGroups) {
                    if (g.equals(def.group)) {
                        inGroup = true;
                        break;
                    }
                }
                if (!inGroup) {
                    continue;
                }
                JsonWriter entry = JsonWriter.obj()
                        .put("type", "biomesunseen:" + mob.id)
                        .put("weight", mob.spawnWeight)
                        .put("minCount", 1)
                        .put("maxCount", mob.pack ? 4 : 2);
                if ("monster".equals(mob.category)) {
                    monsterList.add(entry);
                } else {
                    creatureList.add(entry);
                }
            }
            JsonWriter biome = JsonWriter.obj()
                    .put("temperature", def.temperature)
                    .put("downfall", def.downfall)
                    .put("has_precipitation", !"clear".equals(def.weather))
                    .put("effects", JsonWriter.obj()
                            .put("grass_color", def.grassColor)
                            .put("foliage_color", def.foliageColor)
                            .put("water_color", def.waterColor)
                            .put("sky_color", def.skyColor)
                            .put("fog_color", def.fogColor))
                    .put("spawners", JsonWriter.obj()
                            .putRawArray("monster", monsterList.toArray(new JsonWriter[0]))
                            .putRawArray("creature", creatureList.toArray(new JsonWriter[0])));
            java.util.List<java.util.List<String>> steps = new java.util.ArrayList<java.util.List<String>>();
            for (int i = 0; i < 11; i++) {
                steps.add(i == 6 ? featureList : new java.util.ArrayList<String>());
            }
            JsonWriter generation = JsonWriter.obj();
            // Raw step lists for the 10 generation steps.
            JsonWriter rawSteps = JsonWriter.obj();
            for (int i = 0; i < 10; i++) {
                java.util.List<String> stepFeatures = i == 6 ? featureList : new java.util.ArrayList<String>();
                rawSteps.putArray("step" + i, stepFeatures.toArray(new String[0]));
            }
            biome.put("carvers", JsonWriter.obj().put("air", "minecraft:overworld"));
            biome.put("features", rawSteps);
            biome.writeTo(biomes.resolve(def.id + ".json"));
        }

        for (StructureDef def : Content.STRUCTURES) {
            JsonWriter.obj()
                    .put("type", "minecraft:jigsaw")
                    .put("config", JsonWriter.obj()
                            .put("start_pool", "biomesunseen:" + def.startPool)
                            .put("size", 3)
                            .put("max_distance_from_center", def.maxDistanceFromCenter)
                            .put("start_height", JsonWriter.obj()
                                    .put("type", "minecraft:constant")
                                    .put("height", 0)))
                    .put("biomes", JsonWriter.obj().putArray("values", biomeKeysFor(def)))
                    .put("spawn_overrides", JsonWriter.obj())
                    .writeTo(structures.resolve(def.id + ".json"));
            JsonWriter.obj()
                    .putRawArray("structures", JsonWriter.obj()
                            .put("structure", "biomesunseen:" + def.id)
                            .put("weight", (int) Math.round(def.rarity * 10)))
                    .put("placement", JsonWriter.obj()
                            .put("type", "minecraft:random_spread")
                            .put("salt", Math.abs(def.id.hashCode() % 100000))
                            .put("spacing", def.spacing)
                            .put("separation", def.separation)
                            .put("spread_type", "linear"))
                    .writeTo(structureSets.resolve(def.id + ".json"));
            JsonWriter.obj()
                    .put("fallback", "minecraft:empty")
                    .putRawArray("elements", JsonWriter.obj()
                            .put("weight", 1)
                            .put("element", JsonWriter.obj()
                                    .put("element_type", "minecraft:legacy_single_pool_element")
                                    .put("location", "biomesunseen:" + def.id + "/start")
                                    .put("projection", "rigid")
                                    .put("processors", "minecraft:empty")))
                    .writeTo(pools.resolve(def.startPool + ".json"));
        }
    }

    private static String[] biomeKeysFor(StructureDef def) {
        java.util.List<String> keys = new java.util.ArrayList<String>();
        for (BiomeDef biome : Content.BIOMES) {
            if (def.spawnsInGroup(biome.group)) {
                keys.add("biomesunseen:" + biome.id);
            }
        }
        return keys.toArray(new String[0]);
    }
}
''')


# --- 1.16.5 client templates -------------------------------------------------
# ModelPart#addBox(float x6) / setPos / render(PoseStack, VertexConsumer, int,
# int, float, float, float, float) and EntityModel#renderToBuffer(...) are the
# 1.16.5 spellings (the builders package arrived in 1.17.1).
_LEGACY_16_MODEL = '''package com.biomesunseen.client.legacy;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelPart;

import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Box model for the 1.16.5 line: head, body and four limbs, animated from the
 * entity's LegacyAnimDriver (limb swing, head yaw, one-shot poses).  The parts
 * are built by hand because the model-builder classes do not exist before
 * 1.17.
 */
public class UnseenLegacyModel<T extends BiomesUnseenMob> extends EntityModel<T> {

    private final ModelPart head;
    private final ModelPart body;
    private final ModelPart leg0;
    private final ModelPart leg1;
    private final ModelPart leg2;
    private final ModelPart leg3;

    public UnseenLegacyModel() {
        head = new ModelPart(64, 32, 0, 0);
        head.addBox(-4.0F, -8.0F, -4.0F, 8.0F, 8.0F, 8.0F);
        head.setPos(0.0F, 4.0F, -4.0F);
        body = new ModelPart(64, 32, 16, 16);
        body.addBox(-5.0F, -10.0F, -7.0F, 10.0F, 16.0F, 8.0F);
        body.setPos(0.0F, 5.0F, 2.0F);
        leg0 = new ModelPart(64, 32, 0, 16);
        leg0.addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F);
        leg0.setPos(-3.0F, 12.0F, 7.0F);
        leg1 = new ModelPart(64, 32, 0, 16);
        leg1.addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F);
        leg1.setPos(3.0F, 12.0F, 7.0F);
        leg2 = new ModelPart(64, 32, 0, 16);
        leg2.addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F);
        leg2.setPos(-3.0F, 12.0F, -5.0F);
        leg3 = new ModelPart(64, 32, 0, 16);
        leg3.addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F);
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
    public void renderToBuffer(PoseStack matrixStack, VertexConsumer buffer,
            int packedLight, int packedOverlay, float red, float green, float blue, float alpha) {
        head.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
        body.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
        leg0.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
        leg1.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
        leg2.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
        leg3.render(matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
    }
}
'''

_LEGACY_16_RENDERER = '''package com.biomesunseen.client.legacy;

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
'''
