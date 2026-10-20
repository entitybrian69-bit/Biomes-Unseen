package com.biomesunseen.client.particle;

import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.particle.Particle;
import net.minecraft.client.particle.ParticleProvider;
import net.minecraft.client.particle.ParticleRenderType;
import net.minecraft.client.particle.SpriteSet;
import net.minecraft.client.particle.TextureSheetParticle;
import net.minecraft.core.particles.SimpleParticleType;
import net.minecraft.util.Mth;

/**
 * A drifting ambient mote: the visual behind every biome particle this mod adds.
 *
 * Registered against each {@code SimpleParticleType} in
 * {@link com.biomesunseen.init.BUParticles} through Forge's
 * {@code RegisterParticleProvidersEvent}. That binding is what makes the eleven
 * hand-authored sprites under {@code textures/particle} reachable at all: a
 * registered particle type with no provider cannot be instantiated, so the
 * client logs "Could not create particle" and spawns nothing -- and because 63
 * biomes name one of these in their effects block, that warning would repeat for
 * as long as the player stood in any of them.
 *
 * The motion is authored rather than inherited from a vanilla puff. These read as
 * pollen, spores, embers and aurora ribbon, so they need to hang in the air and
 * sway instead of falling: buoyancy is a small constant upward acceleration, the
 * horizontal drift is a sine sway offset by a per-particle phase so a field of
 * motes does not pulse in lockstep, and velocity is damped each tick so they
 * settle instead of accelerating away.
 *
 * Alpha follows a fade-in / hold / fade-out envelope over the particle's life.
 * Without it every mote pops into existence at full opacity, which reads as
 * flicker when a biome is spawning them continuously.
 */
public class BUAmbientParticle extends TextureSheetParticle {

    /** Sway rate in radians per tick. Slow enough to read as drifting air. */
    private static final double SWAY_RATE = 0.12D;

    /** Horizontal acceleration applied per tick by the sway. */
    private static final double SWAY_STRENGTH = 0.0016D;

    /** Velocity retained per tick; the rest is bled off as drag. */
    private static final double DRAG = 0.96D;

    /** Fraction of life spent fading in, and the fraction spent fading out. */
    private static final float FADE_IN = 0.2F;
    private static final float FADE_OUT_START = 0.7F;

    private final SpriteSet sprites;

    /** Per-particle phase offset so neighbouring motes do not sway together. */
    private final float driftPhase;

    /** Upward acceleration, randomised per particle so motes separate over time. */
    private final float buoyancy;

    /** Peak opacity for this particle, randomised so a swarm has depth. */
    private final float baseAlpha;

    public BUAmbientParticle(SpriteSet sprites, ClientLevel level,
                             double x, double y, double z,
                             double xd, double yd, double zd) {
        super(level, x, y, z, xd, yd, zd);
        this.sprites = sprites;
        this.setSpriteFromAge(sprites);

        this.driftPhase = level.random.nextFloat() * ((float) Math.PI * 2.0F);
        this.buoyancy = 0.0012F + level.random.nextFloat() * 0.0016F;
        this.baseAlpha = 0.55F + level.random.nextFloat() * 0.45F;

        // Small motes: these are ambience, not weather, so they must never
        // obscure the terrain they are drifting through.
        this.quadSize = 0.09F + level.random.nextFloat() * 0.07F;
        this.lifetime = 90 + level.random.nextInt(90);

        // Motes pass through geometry rather than settling on it, and ignore
        // gravity so the authored buoyancy is the only vertical force.
        this.hasPhysics = false;
        this.gravity = 0.0F;

        // Jitter the spawn velocity so a burst does not move as one sheet.
        this.xd = xd + (level.random.nextDouble() - 0.5D) * 0.01D;
        this.yd = yd + level.random.nextDouble() * 0.004D;
        this.zd = zd + (level.random.nextDouble() - 0.5D) * 0.01D;

        // Start invisible; tick() fades in over the first fifth of the life.
        this.alpha = 0.0F;
    }

    @Override
    public void tick() {
        this.xo = this.x;
        this.yo = this.y;
        this.zo = this.z;
        if (this.age++ >= this.lifetime) {
            this.remove();
            return;
        }

        this.setSpriteFromAge(this.sprites);

        double phase = (this.age + this.driftPhase) * SWAY_RATE;
        this.xd += Math.cos(phase) * SWAY_STRENGTH;
        this.zd += Math.sin(phase) * SWAY_STRENGTH;
        this.yd += this.buoyancy;

        this.move(this.xd, this.yd, this.zd);
        this.xd *= DRAG;
        this.yd *= DRAG;
        this.zd *= DRAG;

        float progress = (float) this.age / (float) this.lifetime;
        float envelope;
        if (progress < FADE_IN) {
            envelope = progress / FADE_IN;
        } else if (progress > FADE_OUT_START) {
            envelope = (1.0F - progress) / (1.0F - FADE_OUT_START);
        } else {
            envelope = 1.0F;
        }
        this.alpha = this.baseAlpha * Mth.clamp(envelope, 0.0F, 1.0F);
    }

    /**
     * Translucent rather than lit, because the alpha envelope above needs to be
     * honoured and several of these sprites are emissive art that should not be
     * darkened by the block light at their position.
     */
    @Override
    public ParticleRenderType getRenderType() {
        return ParticleRenderType.PARTICLE_SHEET_TRANSLUCENT;
    }

    /**
     * Binds one particle type to this class through its authored sprite set.
     *
     * Written as a named class rather than a nested lambda because
     * {@code registerSpriteSet} takes a {@code SpriteParticleRegistration} whose
     * single method returns a {@code ParticleProvider} -- a lambda returning a
     * lambda gives the compiler no target type for the inner one. As a method
     * reference this reads as {@code BUAmbientParticle.Provider::new} at the call
     * site and every type is explicit.
     *
     * The sprite set comes from the type's descriptor under
     * {@code assets/biomesunseen/particles}, which is why
     * {@code registerSpriteSet} is the right Forge entry point: it is the
     * json-based variant, and Forge raises a missing-texture-list error at load
     * if the descriptor is absent.
     */
    public static class Provider implements ParticleProvider<SimpleParticleType> {

        private final SpriteSet sprites;

        public Provider(SpriteSet sprites) {
            this.sprites = sprites;
        }

        @Override
        public Particle createParticle(SimpleParticleType options, ClientLevel level,
                                       double x, double y, double z,
                                       double xd, double yd, double zd) {
            return new BUAmbientParticle(this.sprites, level, x, y, z, xd, yd, zd);
        }
    }
}
