package com.biomesunseen.entity.boss;

import com.biomesunseen.registry.ModEntities;
import com.biomesunseen.registry.ModSounds;
import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.world.Difficulty;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.RangedAttackMob;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RangedAttackGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.AbstractArrow;
import net.minecraft.world.entity.projectile.Arrow;
import net.minecraft.world.level.Level;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.core.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.core.animation.AnimatableManager;
import software.bernie.geckolib.core.animation.AnimationController;
import software.bernie.geckolib.core.animation.RawAnimation;
import software.bernie.geckolib.core.object.PlayState;
import software.bernie.geckolib.util.GeckoLibUtil;

import java.util.UUID;

/** The Heart of the Forest: three-phase boss with ranged thorn volleys and a phase-aware boss bar. */
public class HeartOfTheForestEntity extends Monster implements GeoEntity, RangedAttackMob {
    private static final EntityDataAccessor<Integer> DATA_PHASE =
            SynchedEntityData.defineId(HeartOfTheForestEntity.class, EntityDataSerializers.INT);
    private static final UUID PHASE_SPEED_ID = UUID.fromString("5b0d6c1e-3f7a-4c52-9a41-0c6f1a2b7d11");
    private static final UUID PHASE_DAMAGE_ID = UUID.fromString("a2e94b7d-81c3-4f60-b5d2-6e3c9f0a4b22");
    private static final String ANIM = "animation.heart_of_the_forest.";

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);
    private final HeartBossBar bossEvent = new HeartBossBar(this.getDisplayName());
    private int transitionTicks;
    private int minionCooldown = 200;

    public HeartOfTheForestEntity(EntityType<? extends HeartOfTheForestEntity> type, Level level) {
        super(type, level);
        this.xpReward = 500;
        this.setPersistenceRequired();
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 300.0D)
                .add(Attributes.ARMOR, 8.0D)
                .add(Attributes.ATTACK_DAMAGE, 12.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.25D)
                .add(Attributes.FOLLOW_RANGE, 48.0D)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0D);
    }

    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
        this.entityData.define(DATA_PHASE, 1);
    }

    public int getPhase() {
        return this.entityData.get(DATA_PHASE);
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new FloatGoal(this));
        this.goalSelector.addGoal(1, new MeleeAttackGoal(this, 1.15D, false) {
            @Override
            public boolean canUse() {
                LivingEntity target = HeartOfTheForestEntity.this.getTarget();
                return super.canUse() && target != null
                        && HeartOfTheForestEntity.this.distanceToSqr(target) < 49.0D;
            }
        });
        this.goalSelector.addGoal(2, new RangedAttackGoal(this, 1.0D, 40, 18.0F) {
            @Override
            public boolean canUse() {
                LivingEntity target = HeartOfTheForestEntity.this.getTarget();
                return super.canUse() && target != null
                        && HeartOfTheForestEntity.this.distanceToSqr(target) >= 25.0D;
            }
        });
        this.goalSelector.addGoal(5, new WaterAvoidingRandomStrollGoal(this, 0.6D));
        this.goalSelector.addGoal(6, new LookAtPlayerGoal(this, Player.class, 16.0F));
        this.targetSelector.addGoal(1, new HurtByTargetGoal(this));
        this.targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        float fraction = this.getHealth() / this.getMaxHealth();
        this.bossEvent.setProgress(fraction);
        int wanted = fraction > 0.66F ? 1 : (fraction > 0.33F ? 2 : 3);
        if (wanted > this.getPhase()) {
            this.enterPhase(wanted);
        }
        if (this.transitionTicks > 0) {
            this.transitionTicks--;
        }
        if (this.getPhase() == 3 && this.getTarget() != null && --this.minionCooldown <= 0) {
            this.summonMinions();
            this.minionCooldown = 300;
        }
    }

    private void enterPhase(int phase) {
        this.entityData.set(DATA_PHASE, phase);
        this.applyPhaseModifiers(phase);
        this.bossEvent.applyPhase(phase);
        this.transitionTicks = 40;
        this.playSound(ModSounds.HEART_PHASE.get(), 3.0F, 1.0F);
        this.triggerAnim("action", "phase_shift");
        for (Player player : this.level().getEntitiesOfClass(Player.class, this.getBoundingBox().inflate(8.0D))) {
            player.knockback(1.5D, this.getX() - player.getX(), this.getZ() - player.getZ());
            player.hurtMarked = true;
        }
    }

    private void applyPhaseModifiers(int phase) {
        double speed = phase == 1 ? 0.0D : (phase == 2 ? 0.15D : 0.35D);
        double damage = phase == 1 ? 0.0D : (phase == 2 ? 0.25D : 0.6D);
        replaceModifier(this.getAttribute(Attributes.MOVEMENT_SPEED), PHASE_SPEED_ID, "phase_speed", speed);
        replaceModifier(this.getAttribute(Attributes.ATTACK_DAMAGE), PHASE_DAMAGE_ID, "phase_damage", damage);
    }

    private static void replaceModifier(AttributeInstance attribute, UUID id, String name, double amount) {
        if (attribute == null) {
            return;
        }
        attribute.removeModifier(id);
        if (amount > 0.0D) {
            attribute.addPermanentModifier(
                    new AttributeModifier(id, name, amount, AttributeModifier.Operation.MULTIPLY_BASE));
        }
    }

    private void summonMinions() {
        if (!(this.level() instanceof ServerLevel server)) {
            return;
        }
        for (int i = 0; i < 2; i++) {
            BlockPos pos = this.blockPosition().offset(this.random.nextInt(7) - 3, 0, this.random.nextInt(7) - 3);
            var minion = ModEntities.SPORELING.get().spawn(server, pos, MobSpawnType.MOB_SUMMONED);
            if (minion != null) {
                minion.setTarget(this.getTarget());
            }
        }
    }

    @Override
    public void performRangedAttack(LivingEntity target, float power) {
        int volley = this.getPhase() * 2 - 1;
        for (int i = 0; i < volley; i++) {
            Arrow arrow = new Arrow(this.level(), this);
            double dx = target.getX() - this.getX();
            double dy = target.getEyeY() - arrow.getY();
            double dz = target.getZ() - this.getZ();
            double flat = Math.sqrt(dx * dx + dz * dz);
            arrow.shoot(dx, dy + flat * 0.2D, dz, 1.6F, 6.0F + volley * 2.0F);
            arrow.setBaseDamage(2.0D + this.getPhase());
            arrow.addEffect(new MobEffectInstance(MobEffects.POISON, 80));
            arrow.pickup = AbstractArrow.Pickup.DISALLOWED;
            this.level().addFreshEntity(arrow);
        }
        this.playSound(ModSounds.HEART_SHOOT.get(), 2.0F, 1.0F);
        this.triggerAnim("action", "shoot");
    }

    @Override
    public boolean isInvulnerableTo(DamageSource source) {
        return (this.transitionTicks > 0 && !source.is(DamageTypeTags.BYPASSES_INVULNERABILITY))
                || super.isInvulnerableTo(source);
    }

    @Override
    public void checkDespawn() {
        if (this.level().getDifficulty() == Difficulty.PEACEFUL && this.shouldDespawnInPeaceful()) {
            this.discard();
        } else {
            this.noActionTime = 0;
        }
    }

    @Override
    public boolean removeWhenFarAway(double distanceSqr) {
        return false;
    }

    @Override
    public boolean canChangeDimensions() {
        return false;
    }

    @Override
    public void startSeenByPlayer(ServerPlayer player) {
        super.startSeenByPlayer(player);
        this.bossEvent.addPlayer(player);
    }

    @Override
    public void stopSeenByPlayer(ServerPlayer player) {
        super.stopSeenByPlayer(player);
        this.bossEvent.removePlayer(player);
    }

    @Override
    public void setCustomName(Component name) {
        super.setCustomName(name);
        this.bossEvent.setName(this.getDisplayName());
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putInt("Phase", this.getPhase());
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        int phase = Math.max(1, Math.min(3, tag.getInt("Phase")));
        this.entityData.set(DATA_PHASE, phase);
        this.applyPhaseModifiers(phase);
        this.bossEvent.applyPhase(phase);
        if (this.hasCustomName()) {
            this.bossEvent.setName(this.getDisplayName());
        }
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.add(new AnimationController<>(this, "move", 5, state -> state.setAndContinue(
                RawAnimation.begin().thenLoop(ANIM + (state.isMoving() ? "walk" : "idle")))));
        controllers.add(new AnimationController<>(this, "attack", 3, state -> {
            if (this.swinging) {
                return state.setAndContinue(RawAnimation.begin().thenPlay(ANIM + "attack"));
            }
            state.getController().forceAnimationReset();
            return PlayState.STOP;
        }));
        // VERIFY: triggerableAnim / triggerAnim availability in the GeckoLib version used.
        controllers.add(new AnimationController<>(this, "action", 0, state -> PlayState.STOP)
                .triggerableAnim("shoot", RawAnimation.begin().thenPlay(ANIM + "shoot"))
                .triggerableAnim("phase_shift", RawAnimation.begin().thenPlay(ANIM + "phase_shift")));
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return cache;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return ModSounds.HEART.ambient().get();
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return ModSounds.HEART.hurt().get();
    }

    @Override
    protected SoundEvent getDeathSound() {
        return ModSounds.HEART.death().get();
    }
}
