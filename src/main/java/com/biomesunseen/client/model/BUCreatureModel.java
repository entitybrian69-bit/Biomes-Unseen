package com.biomesunseen.client.model;

import com.biomesunseen.entity.BUCreature;
import com.biomesunseen.entity.MobData;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.resources.ResourceLocation;
import software.bernie.geckolib.model.GeoModel;

/**
 * The GeckoLib model for every non-boss creature.
 *
 * One model class serves all 80 species: it resolves the {@code .geo.json},
 * {@code .animation.json} and texture from the species id at lookup time. That
 * is what makes the roster data-driven -- a new species needs an atlas and two
 * JSON files, not a new model class.
 *
 * Models are shared per <i>family</i> (avian, arthropod, biped, quadruped,
 * serpent, fungal) because every member of a family uses the same articulated
 * rig and the same authored atlas band layout; what differs between species is
 * the texture and the overlays baked into it.
 */
public class BUCreatureModel implements GeoModel<BUCreature> {

    @Override
    public ResourceLocation getModelResource(BUCreature entity) {
        return new ResourceLocation("biomesunseen",
                "geo/entity/" + entity.species().family + ".geo.json");
    }

    @Override
    public ResourceLocation getTextureResource(BUCreature entity) {
        // Each species has its own authored atlas, so the texture is per-species
        // even though the rig is per-family.
        return new ResourceLocation("biomesunseen",
                "textures/entity/" + entity.species().id + ".png");
    }

    @Override
    public ResourceLocation getAnimationResource(BUCreature entity) {
        return new ResourceLocation("biomesunseen",
                "animations/entity/" + entity.species().family + ".animation.json");
    }

    /**
     * The render type for this species.
     *
     * Authored per species rather than fixed: bioluminescent and ghostly
     * creatures need translucency to read correctly, and the rest use cutout so
     * the authored silhouette keeps its transparent corners.
     */
    @Override
    public RenderType getRenderType(BUCreature entity, ResourceLocation texture) {
        if ("translucent".equals(entity.species().renderLayer)) {
            return RenderType.entityTranslucent(texture);
        }
        if ("eyes".equals(entity.species().renderLayer)) {
            return RenderType.entityCutoutNoCull(texture);
        }
        return RenderType.entityCutoutNoCull(texture);
    }
}
