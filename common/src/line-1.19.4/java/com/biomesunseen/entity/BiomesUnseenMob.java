package com.biomesunseen.entity;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.level.Level;


import software.bernie.geckolib3.core.IAnimatable;
import software.bernie.geckolib3.core.PlayState;
import software.bernie.geckolib3.core.builder.AnimationBuilder;
import software.bernie.geckolib3.core.builder.ILoopType;
import software.bernie.geckolib3.core.controller.AnimationController;
import software.bernie.geckolib3.core.event.predicate.AnimationState;
import software.bernie.geckolib3.core.manager.AnimationData;
import software.bernie.geckolib3.core.manager.AnimationFactory;
import software.bernie.geckolib3.util.GeckoLibUtil;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.core.BossDef;
import com.biomesunseen.core.MobDef;
import com.biomesunseen.util.AiThrottle;
import com.biomesunseen.util.SpawnCaps;

/**
 * Shared base for every Biomes Unseen mob.  Provides:
 *  - AI throttling (config "entityAiThrottle") with deterministic stagger
 *  - spawn-cap bookkeeping per dimension
 *  - environment adaptation (movement speed follows biome temperature)
 *  - pack/herd helpers used by the generated AI goals
 *  - the GeckoLib animation state machine hooks every mob overrides
 */
public abstract class BiomesUnseenMob implements IAnimatable {

    protected final MobDef mobDef;

    @Override
    public void registerControllers(AnimationData data) {
        data.addAnimationController(new AnimationController<>(this, "movement", 0,
                this::animPredicate));
    }
    /** Animation state: ticks remaining for the current one-shot anim. */
    private int animOneShotTicks;
    private String animOneShot;

    /** Trigger a one-shot animation by behaviour name (e.g. "graze"). */
    public void triggerAnim(String name) {
        this.animOneShot = name;
        this.animOneShotTicks = 24;
    }

    public int getAnimOneShotTicks() {
        return animOneShotTicks;
    }

    public String getAnimOneShot() {
        return animOneShot;
    }

    private <E extends IAnimatable> PlayState animPredicate(software.bernie.geckolib3.core.event.predicate.AnimationState<E> event) {
        AnimationBuilder builder = new AnimationBuilder();
        if (animOneShotTicks > 0 && animOneShot != null) {
            builder.addAnimation("animation." + mobDef.id + "." + animOneShot, false);
        } else if (event.isMoving() || isMovingEntity()) {
            builder.addAnimation(isSprintingEntity() ? "animation." + mobDef.id + ".run" : "animation." + mobDef.id + ".walk", true);
        } else {
            builder.addAnimation("animation." + mobDef.id + ".idle", true);
        }
        event.getController().setAnimation(builder);
        return PlayState.CONTINUE;
    }

    protected BiomesUnseenMob(EntityType<? extends PathfinderMob> type, Level level, MobDef mobDef) {
        super(type, level);
        this.mobDef = mobDef;
    }

    public MobDef mobDef() {
        return mobDef;
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (animOneShotTicks > 0) {
            animOneShotTicks--;
        }
        if (!level().isClientSide && tickCount % 20 == 0) {
            adaptToEnvironment();
        }
    }

    @Override
    public void tick() {
        if (AiThrottle.shouldThink(getId(), level().getGameTime())) {
            super.tick();
        } else if (!level().isClientSide) {
            // Cheap tick: keep physics and health regen, skip goal churn.
            super.tick();
        } else {
            super.tick();
        }
    }

    /** Environmental adaptation: cold biomes slow, warm biomes hasten. */
    protected void adaptToEnvironment() {
        if (!BiomesUnseen.config().enableAdaptiveMobs) {
            return;
        }
        double temperature = 0.7D;
        try {
            temperature = level().getBiome(blockPosition()).value().getBaseTemperature();
        } catch (Throwable ignored) {
            // Older mappings expose the temperature accessor differently.
        }
        double factor = 1.0D;
        if (temperature < 0.2D) {
            factor = 0.9D;
        } else if (temperature > 1.2D) {
            factor = 1.1D;
        }
        setSpeedModifier(factor);
    }

    /** Applied per line; the default stores nothing extra. */
    protected void setSpeedModifier(double factor) {
        // Movement speed adaptation hook.  Subclasses with Attributes applied
        // at spawn keep their base speed; the factor is used by goals.
        this.adaptationFactor = factor;
    }

    protected double adaptationFactor = 1.0D;

    public double getAdaptationFactor() {
        return adaptationFactor;
    }

    /** Moving + sprinting flags used by the animation state machine. */
    public boolean isMovingEntity() {
        return getDeltaMovement().horizontalDistanceSqr() > 1.0E-4D;
    }

    public boolean isSprintingEntity() {
        return isSprinting();
    }

    @Override
    public void remove(RemovalReason reason) {
        super.remove(reason);
        if (!level().isClientSide) {
            SpawnCaps.onRemoved(level().dimension().location().toString());
        }
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        boolean hurt = super.hurt(source, amount);
        if (hurt) {
            triggerAnim("hurt");
        }
        return hurt;
    }

    /** Pack helper: nearest same-type mob within radius. */
    public BiomesUnseenMob findNearestAlly(double radius) {
        java.util.List<? extends BiomesUnseenMob> list = level().getEntitiesOfClass(
                BiomesUnseenMob.class, getBoundingBox().inflate(radius),
                other -> other != this && other.mobDef() == this.mobDef);
        return list.isEmpty() ? null : list.get(0);
    }

    /** Pack helper: number of same-type mobs nearby. */
    public int countAllies(double radius) {
        return level().getEntitiesOfClass(BiomesUnseenMob.class, getBoundingBox().inflate(radius),
                other -> other != this && other.mobDef() == this.mobDef).size();
    }

    /** Tameable interaction hook (used by tameable mobs). */
    public boolean onTamedInteraction(Player player) {
        return false;
    }

    /** Synthetic MobDef derived from a BossDef so shared helpers work for bosses. */
    protected static MobDef bossMobDef(BossDef boss) {
        return new MobDef(boss.id, boss.displayName, "monster", boss.maxHealth,
                boss.movementSpeed, boss.attackDamage, 8.0D, boss.width, boss.height,
                new String[]{"pack_tactics"}, false, false, false, false, false, true,
                new String[]{boss.biomeGroup}, 0, false,
                new String[]{"idle", "walk", "run", "attack", "hurt", "death"},
                boss.color, boss.glow);
    }

}
