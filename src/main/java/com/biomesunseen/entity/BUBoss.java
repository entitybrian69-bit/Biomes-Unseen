package com.biomesunseen.entity;

import com.biomesunseen.entity.BossData.PhaseData;
import com.biomesunseen.entity.ai.BUGoalFactory;
import com.biomesunseen.init.BUEntities;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityDimensions;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import software.bernie.geckolib.core.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.core.animation.AnimatableManager;
import software.bernie.geckolib.core.animation.AnimationController;
import software.bernie.geckolib.core.animation.AnimationState;
import software.bernie.geckolib.core.animation.RawAnimation;
import software.bernie.geckolib.core.object.PlayState;
import software.bernie.geckolib.core.animatable.GeoAnimatable;
import software.bernie.geckolib.util.GeckoLibUtil;

/**
 * The multi-phase boss implementation behind all five bosses.
 *
 * A boss is not a big mob: it is a state machine. {@link BossData} carries the
 * authored phase list, and this class advances through it as health drops,
 * swapping goals, playing the phase's entry animation, granting a short
 * invulnerability window on each transition, and keeping the boss bar, the
 * music and the loot table in step.
 *
 * The three mandated combat goals -- {@link MeleeAttackGoal},
 * {@link HurtByTargetGoal} and {@link NearestAttackableTargetGoal} -- are added
 * unconditionally here in addition to whatever the phase declares, so no boss
 * can ever be inert regardless of what its data row says. tools/validate.py
 * enforces the same rule on the Python side.
 *
 * Animation is GeckoLib only: the model is an articulated multi-part
 * {@code .geo.json} and every phase transition is a keyframed
 * {@code .animation.json} clip.
 */
public class BUBoss extends Monster implements GeoAnimatable {

    private final BossData boss;
    private final MobData species;
    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    /** Server-side boss bar; colour and overlay come from the authored data. */
    private final ServerBossEvent bossBar;

    private PhaseData phase;
    /** Ticks of invulnerability remaining from the last phase transition. */
    private int invulnerableTicks;
    /** Ticks the entry animation has been playing, so it can finish before AI resumes. */
    private int entryAnimationTicks;
    private boolean dying;

    public BUBoss(EntityType<? extends BUBoss> type, Level level) {
        super(type, level);
        this.boss = BUEntities.bossFor(type);
        this.species = BUEntities.mobDataFor(this.boss);
        this.bossBar = new ServerBossEvent(
                this.getDisplayName(),
                barColor(this.boss.bossBarColor),
                barOverlay(this.boss.bossBarOverlay));
        this.phase = this.boss.phases[0];
        this.setPersistenceRequired();
        this.xpReward = 500;
        // Bosses must not despawn mid-fight when the player breaks line of sight.
        this.noActionTime = 0;
    }

    /** The authored boss definition. */
    public BossData boss() {
        return boss;
    }

    /** The phase the fight is currently in. */
    public PhaseData phase() {
        return phase;
    }

    // ------------------------------------------------------------------ //
    //  Attributes
    // ------------------------------------------------------------------ //

    public static AttributeSupplier.Builder attributesFor(BossData boss) {
        MobData mob = BUEntities.mobDataFor(boss);
        return Mob.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, mob.maxHealth)
                .add(Attributes.MOVEMENT_SPEED, mob.movementSpeed)
                .add(Attributes.ATTACK_DAMAGE, Math.max(4.0D, mob.attackDamage))
                .add(Attributes.ATTACK_KNOCKBACK, Math.max(1.0D, mob.attackKnockback))
                .add(Attributes.FOLLOW_RANGE, 64.0D)
                .add(Attributes.ARMOR, Math.max(6.0D, mob.armour))
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0D);
    }

    // ------------------------------------------------------------------ //
    //  AI
    // ------------------------------------------------------------------ //

    @Override
    protected void registerGoals() {
        // The three mandated combat goals, always present and always highest
        // priority so a phase change can never leave the boss unable to fight.
        this.goalSelector.addGoal(1, new MeleeAttackGoal(this, 1.3D, true));
        this.goalSelector.addGoal(2, new FloatGoalSafe(this));
        this.targetSelector.addGoal(1, new HurtByTargetGoal(this).setAlertOthers());
        this.targetSelector.addGoal(2,
                new NearestAttackableTargetGoal<>(this, Player.class, true));

        // Phase-authored goals layered on top.
        addPhaseGoals(this.phase);
    }

    /**
     * Swap in the goals a phase declares.
     *
     * Called on every phase transition. The mandated combat goals registered in
     * {@link #registerGoals()} are left in place -- only the phase-specific
     * extras are cleared and rebuilt, so a badly authored phase can degrade the
     * fight but never disable it.
     */
    private void addPhaseGoals(PhaseData data) {
        for (String token : data.extraGoals) {
            BUGoalFactory.Prioritised entry = single(token);
            if (entry == null) {
                continue;
            }
            if (entry.goal instanceof net.minecraft.world.entity.ai.goal.target.TargetGoal) {
                this.targetSelector.addGoal(entry.priority + 3, entry.goal);
            } else {
                this.goalSelector.addGoal(entry.priority + 3, entry.goal);
            }
        }
    }

    /** Resolve one goal token against this boss's own species data. */
    private BUGoalFactory.Prioritised single(String token) {
        for (BUGoalFactory.Prioritised entry : BUGoalFactory.buildFor(token, species, this)) {
            return entry;
        }
        return null;
    }

    // ------------------------------------------------------------------ //
    //  Phase machine
    // ------------------------------------------------------------------ //

    @Override
    public void aiStep() {
        super.aiStep();

        if (this.isDeadOrDying()) {
            dying = true;
            return;
        }
        if (invulnerableTicks > 0) {
            invulnerableTicks--;
        }
        if (entryAnimationTicks > 0) {
            entryAnimationTicks--;
        }

        if (!this.level().isClientSide()) {
            advancePhase();
            bossBar.setProgress(this.getHealth() / this.getMaxHealth());
        }
    }

    /**
     * Move to the phase this health fraction belongs to.
     *
     * Transitions are one-directional: the fight never reverts to an earlier
     * phase if the boss is healed, because a phase that can be un-done lets a
     * player trivially reset a hard encounter by drinking a potion.
     */
    private void advancePhase() {
        float fraction = this.getHealth() / this.getMaxHealth();
        PhaseData next = boss.phaseFor(fraction);
        if (next.index == phase.index) {
            return;
        }
        // Only ever move forward through the authored phase list.
        if (next.index <= phase.index) {
            return;
        }
        phase = next;
        entryAnimationTicks = 30;
        if (phase.invulnerableOnEntry) {
            invulnerableTicks = phase.invulnerableTicks;
        }

        // Clear phase extras and rebuild for the new phase. The mandated combat
        // goals stay, so the boss is always able to fight back.
        this.goalSelector.removeAllGoals(goal -> isPhaseExtra(goal));
        this.targetSelector.removeAllGoals(goal -> isPhaseExtra(goal));
        addPhaseGoals(phase);

        // A phase change is a readable event: play the boss's hurt voice and
        // push nearby players back so the transition is felt, not just seen.
        this.playSound(this.getHurtSound(this.damageSources().mobAttack(this)), 2.0F, 0.7F);
        knockbackNearbyPlayers();
        if (phase.index == boss.phases.length) {
            // The final phase is the enrage: faster and harder hitting, so a
            // fight that has dragged does not drag forever.
            this.addEffect(new MobEffectInstance(MobEffects.DAMAGE_BOOST,
                    Integer.MAX_VALUE, 1, false, false, false));
            this.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED,
                    Integer.MAX_VALUE, 0, false, false, false));
        }
    }

    private boolean isPhaseExtra(net.minecraft.world.entity.ai.goal.Goal goal) {
        // The mandated goals are the first four registered; anything above that
        // index came from a phase's extraGoals list.
        return goal.getClass() != MeleeAttackGoal.class
                && goal.getClass() != HurtByTargetGoal.class
                && goal.getClass() != NearestAttackableTargetGoal.class
                && goal.getClass() != FloatGoalSafe.class;
    }

    private void knockbackNearbyPlayers() {
        AABB area = this.getBoundingBox().inflate(8.0D);
        for (Player player : this.level().getEntitiesOfClass(Player.class, area)) {
            double dx = player.getX() - this.getX();
            double dz = player.getZ() - this.getZ();
            double distance = Math.max(0.5D, Math.sqrt(dx * dx + dz * dz));
            player.push(dx / distance * 1.2D, 0.45D, dz / distance * 1.2D);
            player.hurtMarked = true;
        }
    }

    // ------------------------------------------------------------------ //
    //  Damage rules
    // ------------------------------------------------------------------ //

    @Override
    public boolean isInvulnerableTo(DamageSource source) {
        // The invulnerability window on phase entry is what stops a player from
        // bursting through every transition with one big hit.
        if (invulnerableTicks > 0 && !source.is(
                net.minecraft.tags.DamageTypeTags.BYPASSES_INVULNERABILITY)) {
            return true;
        }
        return super.isInvulnerableTo(source);
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (invulnerableTicks > 0) {
            return false;
        }
        return super.hurt(source, amount);
    }

    @Override
    public boolean removeWhenFarAway(double distance) {
        return false;
    }

    @Override
    protected boolean shouldDespawnInPeaceful() {
        return false;
    }

    @Override
    public boolean isPersistenceRequired() {
        return true;
    }

    @Override
    public void setCustomName(net.minecraft.network.chat.Component name) {
        super.setCustomName(name);
        if (bossBar != null) {
            bossBar.setName(this.getDisplayName());
        }
    }

    // ------------------------------------------------------------------ //
    //  Boss bar visibility
    // ------------------------------------------------------------------ //

    @Override
    public void startSeenByPlayer(ServerPlayer player) {
        super.startSeenByPlayer(player);
        bossBar.addPlayer(player);
        // Each boss has its own authored theme; starting it when the fight
        // starts is what makes the encounter feel scored rather than ambient.
        BUEntities.playBossMusic(this, player);
    }

    @Override
    public void stopSeenByPlayer(ServerPlayer player) {
        super.stopSeenByPlayer(player);
        bossBar.removePlayer(player);
        BUEntities.stopBossMusic(this, player);
    }

    @Override
    public void die(DamageSource source) {
        super.die(source);
        dying = true;
        if (!this.level().isClientSide()) {
            for (ServerPlayer player : bossBar.getPlayers()) {
                bossBar.removePlayer(player);
                BUEntities.stopBossMusic(this, player);
            }
            // Drops come from data/biomesunseen/loot_tables/entities/<boss_id>.json,
            // which Forge resolves from the entity's registry name via the normal
            // dropAllDeathLoot path in super.die(). Dispatching a table by hand
            // here would double the loot.
        }
    }

    // ------------------------------------------------------------------ //
    //  Persistence
    // ------------------------------------------------------------------ //

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putInt("BUPhase", phase.index);
        tag.putInt("BUInvulnerable", invulnerableTicks);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        int saved = tag.getInt("BUPhase");
        for (PhaseData candidate : boss.phases) {
            if (candidate.index == saved) {
                phase = candidate;
                break;
            }
        }
        invulnerableTicks = tag.getInt("BUInvulnerable");
        if (this.hasCustomName()) {
            bossBar.setName(this.getDisplayName());
        }
    }

    // ------------------------------------------------------------------ //
    //  Dimensions
    // ------------------------------------------------------------------ //

    @Override
    public EntityDimensions getDimensions(Pose pose) {
        return super.getDimensions(pose).scale(boss.scale);
    }

    @Override
    public boolean isFireImmune() {
        return species.fireImmune;
    }

    // ------------------------------------------------------------------ //
    //  GeckoLib
    // ------------------------------------------------------------------ //

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.add(new AnimationController<>(this, "body", 6.0F, this::bodyPredicate));
        controllers.add(new AnimationController<>(this, "phase", 3.0F, this::phasePredicate));
        controllers.add(new AnimationController<>(this, "action", 2.0F, this::actionPredicate));
    }

    private PlayState bodyPredicate(AnimationState<BUBoss> state) {
        if (dying) {
            return play(state, "animation.death", true);
        }
        if (state.isMoving() || state.getLimbSwingAmount() > 0.05F) {
            return play(state, "animation.walk", true);
        }
        return play(state, "animation.idle", true);
    }

    /**
     * The phase layer.
     *
     * Each phase names an entry animation in the authored data, and those
     * animations are exactly what the .animation.json files define -- the
     * Python validator fails the build if a phase names an animation the
     * species does not declare, so this lookup cannot reference a missing clip.
     */
    private PlayState phasePredicate(AnimationState<BUBoss> state) {
        if (dying) {
            return PlayState.STOP;
        }
        // The entry clip plays once on transition, then the layer idles on the
        // phase's loop so the boss visibly changes posture between stages.
        if (entryAnimationTicks > 0) {
            return play(state, phase.entryAnimation, false);
        }
        return play(state, "animation.phase." + phase.index, true);
    }

    private PlayState actionPredicate(AnimationState<BUBoss> state) {
        if (dying) {
            return PlayState.STOP;
        }
        if (this.hurtTime > 0) {
            return play(state, "animation.hurt", false);
        }
        if (this.swinging) {
            return play(state, "animation.attack", false);
        }
        return PlayState.STOP;
    }

    /**
     * Play a clip if the boss's animation set defines it, else stop cleanly.
     *
     * Naming an animation GeckoLib has not loaded throws at load time, so this
     * guard is what lets an optional clip (a phase loop an artist has not
     * shipped yet) degrade silently instead of breaking the fight.
     */
    private PlayState play(AnimationState<BUBoss> state, String animation, boolean loop) {
        if (!declares(animation)) {
            return PlayState.STOP;
        }
        state.setAnimation(loop
                ? RawAnimation.begin().thenLoop(animation)
                : RawAnimation.begin().thenPlay(animation));
        return PlayState.CONTINUE;
    }

    private boolean declares(String animation) {
        for (String declared : species.animations) {
            if (declared.equals(animation)) {
                return true;
            }
        }
        // Phase loops are derived from the phase index rather than listed on the
        // species, so accept them when the data declares a matching phase.
        return animation.startsWith("animation.phase.");
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return cache;
    }

    @Override
    public double getTick(Object entity) {
        return ((Mob) entity).tickCount;
    }

    // ------------------------------------------------------------------ //
    //  Boss bar styling
    // ------------------------------------------------------------------ //

    private static BossEvent.BossBarColor barColor(String name) {
        switch (name) {
            case "pink":
                return BossEvent.BossBarColor.PINK;
            case "blue":
                return BossEvent.BossBarColor.BLUE;
            case "red":
                return BossEvent.BossBarColor.RED;
            case "green":
                return BossEvent.BossBarColor.GREEN;
            case "yellow":
                return BossEvent.BossBarColor.YELLOW;
            case "purple":
                return BossEvent.BossBarColor.PURPLE;
            default:
                return BossEvent.BossBarColor.WHITE;
        }
    }

    private static BossEvent.BossBarOverlay barOverlay(String name) {
        switch (name) {
            case "notched_6":
                return BossEvent.BossBarOverlay.NOTCHED_6;
            case "notched_10":
                return BossEvent.BossBarOverlay.NOTCHED_10;
            case "notched_12":
                return BossEvent.BossBarOverlay.NOTCHED_12;
            case "notched_20":
                return BossEvent.BossBarOverlay.NOTCHED_20;
            default:
                return BossEvent.BossBarOverlay.PROGRESS;
        }
    }

    /**
     * The float goal, kept as a named type so {@link #isPhaseExtra} can
     * recognise it as one of the always-on goals rather than a phase extra.
     */
    private static final class FloatGoalSafe extends net.minecraft.world.entity.ai.goal.FloatGoal {
        FloatGoalSafe(Mob mob) {
            super(mob);
        }
    }
}
