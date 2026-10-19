package com.biomesunseen.client.model;

import com.biomesunseen.entity.BUBoss;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.resources.ResourceLocation;
import software.bernie.geckolib.model.GeoModel;

/**
 * The GeckoLib model for the five bosses.
 *
 * Each boss has its own 64x64 atlas and its own multi-part articulated rig:
 * body, head, four limbs and the boss-specific extras (the Heart's root
 * tendrils, the Warden's drill, the Serpent's coils, the Crown's regalia, the
 * Unraveling's unstable shell). Nothing here is shared with the creature model,
 * because a boss fight has to read as a different order of thing.
 */
public class BUBossModel implements GeoModel<BUBoss> {

    @Override
    public ResourceLocation getModelResource(BUBoss entity) {
        return new ResourceLocation("biomesunseen",
                "geo/entity/boss/" + entity.boss().id + ".geo.json");
    }

    @Override
    public ResourceLocation getTextureResource(BUBoss entity) {
        return new ResourceLocation("biomesunseen",
                "textures/entity/boss/" + entity.boss().id + ".png");
    }

    @Override
    public ResourceLocation getAnimationResource(BUBoss entity) {
        return new ResourceLocation("biomesunseen",
                "animations/entity/boss/" + entity.boss().id + ".animation.json");
    }

    @Override
    public RenderType getRenderType(BUBoss entity, ResourceLocation texture) {
        // Bosses are large enough that cutout is required to keep the authored
        // silhouette crisp at distance; translucency would sort badly against
        // the arena geometry.
        return RenderType.entityCutoutNoCull(texture);
    }
}
