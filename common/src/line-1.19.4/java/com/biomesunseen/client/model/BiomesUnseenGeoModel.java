package com.biomesunseen.client.model;

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
