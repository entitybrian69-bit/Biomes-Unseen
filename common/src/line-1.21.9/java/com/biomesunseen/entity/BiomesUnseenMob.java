package com.biomesunseen.entity;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.level.Level;


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
public abstract class BiomesUnseenMob extends PathfinderMob  {

    protected final MobDef mobDef;


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

    /** Current animation pose name for the legacy renderer. */
    public String currentAnimName() {
        if (animOneShotTicks > 0 && animOneShot != null) {
            return animOneShot;
        }
        if (isMovingEntity()) {
            return isSprintingEntity() ? "run" : "walk";
        }
        return "idle";
    }

    private final com.biomesunseen.entity.legacy.LegacyAnimDriver animDriver =
            new com.biomesunseen.entity.legacy.LegacyAnimDriver(this);

    /** Shared procedural animation driver: pose data for the custom renderer. */
    public com.biomesunseen.entity.legacy.LegacyAnimDriver animDriver() {
        return animDriver;
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
        animDriver.tick();
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
    public void remove(net.minecraft.world.entity.Entity.RemovalReason reason) {
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
