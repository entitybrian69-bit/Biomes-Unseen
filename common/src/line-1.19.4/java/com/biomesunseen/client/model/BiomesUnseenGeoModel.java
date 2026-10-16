package com.biomesunseen.client.model;

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
