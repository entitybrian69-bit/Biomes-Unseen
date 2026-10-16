package com.biomesunseen.client.particle;

import net.minecraft.client.particle.Particle;
import net.minecraft.client.particle.ParticleProvider;
import net.minecraft.client.particle.TextureSheetParticle;
import net.minecraft.client.particle.ParticleRenderType;
import net.minecraft.client.particle.SpriteSet;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.core.particles.SimpleParticleType;

/**
 * Generic animated particle used by all 8 particle types: sprite-animated,
 * gently rising, fading out.  Ambience for crystal sparks, embers, void
 * motes, spores, frost, storm arcs, petals and heal glows.
 */
public class UnseenParticle extends TextureSheetParticle {

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
    public static class Provider implements ParticleProvider<SimpleParticleType> {
        private final SpriteSet sprites;

        public Provider(SpriteSet sprites) {
            this.sprites = sprites;
        }

        @Override
        public Particle createParticle(SimpleParticleType type, ClientWorld level,
                double x, double y, double z, double xSpeed, double ySpeed, double zSpeed) {
            return new UnseenParticle(level, x, y, z, xSpeed, ySpeed, zSpeed, sprites);
        }
    }
}
