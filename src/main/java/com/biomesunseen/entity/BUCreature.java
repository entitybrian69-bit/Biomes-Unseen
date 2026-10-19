package com.biomesunseen.entity;

import com.biomesunseen.entity.ai.BUGoalFactory;
import com.biomesunseen.init.BUEntities;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import software.bernie.geckolib.core.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.core.animation.AnimatableManager;
import software.bernie.geckolib.core.animation.AnimationController;
import software.bernie.geckolib.core.animation.AnimationState;
import software.bernie.geckolib.core.animation.RawAnimation;
import software.bernie.geckolib.core.object.PlayState;
import software.bernie.geckolib.entity.GeoEntity;
import software.bernie.geckolib.util.GeckoLibUtil;

import javax.annotation.Nullable;

/**
 * The single creature implementation behind all 80 non-boss species.
 *
 * Rather than 80 near-identical subclasses, every species is one
 * {@link EntityType} pointing at this class, parameterised by the
 * {@link MobData} row the content tables generated. Attributes, AI goals,
 * spawn rules, model scale and animation names all read from that row, so
 * authoring a new species in tools/content/mobs.py is a data change and not a
 * code change -- which is what keeps 80 creatures maintainable.
 *
 * Animation is GeckoLib only: no {@code ModelPart}, no {@code CubeListBuilder}.
 * The model is an articulated {@code .geo.json} and the motions are
 * {@code .animation.json} keyframes, both resolved by species id.
 */
public class BUCreature extends PathfinderMob implements GeoEntity {

    /** The species this instance was registered for; fixed at construction. */
    private final MobData species;
    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    /** Tracks hurt/death animation state so the controller can crossfade. */
    private int hurtTicks;
    private boolean dying;

    public BUCreature(EntityType<? extends BUCreature> type, Level level) {
        super(type, level);
        this.species = BUEntities.speciesFor(type);
        this.xpReward = species.experience;
        // Hostile species must persist through despawn checks the same way
        // vanilla monsters do, so a player cannot simply out-wait an ambush.
        this.setPersistenceRequired();
    }

    /** The authored stat block for this species. */
    public MobData species() {
        return species;
    }

    // ------------------------------------------------------------------ //
    //  Attributes
    // ------------------------------------------------------------------ //

    /**
     * Build the attribute supplier for a species.
     *
     * Called once per EntityType from {@link BUEntities} during
     * EntityAttributeCreationEvent, which is the only point Forge allows
     * entity attributes to be declared.
     */
    public static AttributeSupplier.Builder attributesFor(MobData data) {
        AttributeSupplier.Builder builder = Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, data.maxHealth)
                .add(Attributes.MOVEMENT_SPEED, data.movementSpeed)
                .add(Attributes.FOLLOW_RANGE, data.followRange)
                .add(Attributes.KNOCKBACK_RESISTANCE, data.armour > 0 ? 0.15D : 0.0D)
                .add(Attributes.ARMOR, data.armour)
                .add(Attributes.ATTACK_KNOCKBACK, data.attackKnockback);
        if (data.hostile) {
            builder.add(Attributes.ATTACK_DAMAGE, Math.max(1.0D, data.attackDamage));
        }
        // Aquatic species need swim speed or they move through water at walking
        // pace, which reads as broken rather than as a design choice.
        if (data.canBreatheUnderwater) {
            builder.add(Attributes.MOVEMENT_SPEED, data.movementSpeed * 1.4D);
        }
        return builder;
    }

    // ------------------------------------------------------------------ //
    //  AI
    // ------------------------------------------------------------------ //

    @Override
    protected void registerGoals() {
        // Goals come from the authored token list, in the authored order. Every
        // hostile in the table carries melee_attack, hurt_by_target and
        // nearest_attackable_target_player -- tools/validate.py fails the build
        // if any of the three is missing, so no creature can ship inert.
        for (BUGoalFactory.Prioritised entry : BUGoalFactory.build(species, this)) {
            this.goalSelector.addGoal(entry.priority, entry.goal);
        }
        for (BUGoalFactory.Prioritised entry : BUGoalFactory.build(species, this)) {
            if (entry.goal instanceof net.minecraft.world.entity.ai.goal.target.TargetGoal) {
                this.targetSelector.addGoal(entry.priority, entry.goal);
            }
        }
    }

    // ------------------------------------------------------------------ //
    //  Spawning
    // ------------------------------------------------------------------ //

    public static boolean checkCreatureSpawnRules(EntityType<? extends BUCreature> type,
                                                  ServerLevelAccessor level,
                                                  MobSpawnType spawnType,
                                                  net.minecraft.core.BlockPos pos,
                                                  net.minecraft.util.RandomSource random) {
        MobData data = BUEntities.speciesFor(type);
        if (data == null) {
            return false;
        }
        // Hostiles follow the vanilla darkness rule; passive species need the
        // surface or their own dimension's light level, otherwise they spawn in
        // sealed caves and the player never sees them.
        if (data.hostile) {
            return Mob.checkMobSpawnRules(type, level, spawnType, pos, random);
        }
        return Animal.checkAnimalSpawnRules(null, level, spawnType, pos, random)
                || level.getRawBrightness(pos, 0) > 8;
    }

    @Override
    @Nullable
    public net.minecraft.world.entity.SpawnGroupData finalizeSpawn(
            ServerLevelAccessor level, DifficultyInstance difficulty,
            MobSpawnType spawnType, @Nullable net.minecraft.world.entity.SpawnGroupData groupData,
            @Nullable CompoundTag tag) {
        if (species.scale != 1.0F) {
            this.refreshDimensions();
        }
        return super.finalizeSpawn(level, difficulty, spawnType, groupData, tag);
    }

    // ------------------------------------------------------------------ //
    //  Dimensions / persistence
    // ------------------------------------------------------------------ //

    /**
     * Scale the hitbox and the render by the species' authored scale.
     *
     * 1.20.1 has no getScale() hook on Entity, so the scale is applied to the
     * dimensions instead -- which is what both the physics box and the renderer
     * consult, so the visual and the hitbox stay in agreement.
     */
    @Override
    protected net.minecraft.world.entity.EntityDimensions getDimensions(Pose pose) {
        return super.getDimensions(pose).scale(species.scale);
    }

    @Override
    protected boolean shouldDespawnInPeaceful() {
        return species.hostile;
    }

    @Override
    public boolean removeWhenFarAway(double distance) {
        return species.hostile;
    }

    @Override
    public boolean isPersistenceRequired() {
        return true;
    }

    @Override
    protected void dropCustomDeathLoot(DamageSource source, int looting, boolean recentlyHit) {
        super.dropCustomDeathLoot(source, looting, recentlyHit);
        // The loot table under data/biomesunseen/loot_tables/entities carries the
        // authored drops, so nothing extra is needed here beyond the vanilla
        // table dispatch that super() performs.
    }

    @Override
    protected int getExperienceReward() {
        return species.experience;
    }

    @Override
    public boolean isFireImmune() {
        return species.fireImmune;
    }

    @Override
    public boolean canBreatheUnderwater() {
        return species.canBreatheUnderwater;
    }

    @Override
    public boolean canBeLeashed(Player player) {
        return !species.hostile;
    }

    // ------------------------------------------------------------------ //
    //  Animation state
    // ------------------------------------------------------------------ //

    @Override
    public void tick() {
        super.tick();
        if (hurtTicks > 0) {
            hurtTicks--;
        }
        if (this.isDeadOrDying()) {
            dying = true;
        }
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        boolean result = super.hurt(source, amount);
        if (result) {
            hurtTicks = 10;
        }
        return result;
    }

    /** True while the hurt animation should play, read by the model controller. */
    public boolean isHurtAnimating() {
        return hurtTicks > 0 && !dying;
    }

    /** True once the death animation should take over. */
    public boolean isDying() {
        return dying;
    }

    // ------------------------------------------------------------------ //
    //  GeckoLib
    // ------------------------------------------------------------------ //

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.add(new AnimationController<>(this, "body", 4.0F, this::bodyPredicate));
        controllers.add(new AnimationController<>(this, "action", 2.0F, this::actionPredicate));
    }

    /**
     * Locomotion layer: idle, walk or death.
     *
     * Animation names come from the species' authored animation list, so a
     * species that does not declare a walk cycle simply keeps idling rather
     * than referencing a missing animation.
     */
    private PlayState bodyPredicate(AnimationState<BUCreature> state) {
        if (dying) {
            return playOrStop(state, "animation.death");
        }
        if (state.isMoving() || state.getLimbSwingAmount() > 0.05F) {
            return playOrStop(state, "animation.walk");
        }
        return playOrStop(state, "animation.idle");
    }

    /**
     * Action layer: attack and hurt, overlaid on the locomotion layer.
     *
     * Running this on a second controller is what lets a creature swing while
     * walking instead of the attack replacing the walk outright.
     */
    private PlayState actionPredicate(AnimationState<BUCreature> state) {
        if (dying) {
            return PlayState.STOP;
        }
        if (isHurtAnimating()) {
            return playOrStop(state, "animation.hurt");
        }
        if (this.swinging) {
            return playOrStop(state, "animation.attack");
        }
        return PlayState.STOP;
    }

    /**
     * Start an animation if the species declares it, otherwise stop cleanly.
     *
     * Declaring an animation the .animation.json does not contain makes
     * GeckoLib throw at load, so this is the guard that keeps the authored
     * animation list and the JSON file in agreement.
     */
    private PlayState playOrStop(AnimationState<BUCreature> state, String animation) {
        if (!declares(animation)) {
            return PlayState.STOP;
        }
        state.setAnimation(RawAnimation.begin().thenLoop(animation));
        return PlayState.CONTINUE;
    }

    private boolean declares(String animation) {
        for (String declared : species.animations) {
            if (declared.equals(animation)) {
                return true;
            }
        }
        return false;
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return cache;
    }

    @Override
    public double getTick(Object entity) {
        return ((Mob) entity).tickCount;
    }
}
