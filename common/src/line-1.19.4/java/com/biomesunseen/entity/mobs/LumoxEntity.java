package com.biomesunseen.entity.mobs;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.Level;
import software.bernie.geckolib.animatable.GeoAnimatable;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animatable.manager.AnimatableManager;
import software.bernie.geckolib.animation.AnimatableManager.ControllerRegistrar;
import software.bernie.geckolib.animation.AnimationController;
import software.bernie.geckolib.animation.PlayState;
import software.bernie.geckolib.animation.RawAnimation;
import software.bernie.geckolib.animation.AnimationState;
import software.bernie.geckolib.util.GeckoLibUtil;


import com.biomesunseen.core.Content;
import com.biomesunseen.entity.BiomesUnseenMob;
import com.biomesunseen.entity.ai.FleeDangerGoal;
import com.biomesunseen.entity.ai.FlockGoal;
import com.biomesunseen.entity.ai.GrazeGoal;
import com.biomesunseen.entity.ai.HerdFollowGoal;
import com.biomesunseen.entity.ai.PackAttackGoal;
import com.biomesunseen.entity.ai.TerrainUseGoal;
import com.biomesunseen.entity.ai.WanderTradeGoal;

/**
 * Lumox - creature with behaviours: graze, follow_herd, tameable
 * Fully animated: idle, walk, run, eat, graze, sit, tame
 */
public class LumoxEntity extends BiomesUnseenMob {

    private static final net.minecraft.network.syncher.EntityDataAccessor<Boolean> TAME =
            net.minecraft.network.syncher.SynchedEntityData.defineId(LumoxEntity.class, net.minecraft.network.syncher.EntityDataSerializers.BOOLEAN);
    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
        entityData.define(TAME, false);
    }
    public LumoxEntity(EntityType<? extends LumoxEntity> type, Level level) {
        super(type, level, Content.mob("lumox"));
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new net.minecraft.world.entity.ai.goal.FloatGoal(this));
        this.goalSelector.addGoal(1, new FleeDangerGoal(this, 1.3D));
        this.goalSelector.addGoal(3, new GrazeGoal(this));
        this.goalSelector.addGoal(3, new HerdFollowGoal(this, 1.1D));
        // Tameable: sit/follow wiring handled in mobInteract/onTamedInteraction.
        this.goalSelector.addGoal(5, new net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal(this, 1.0D));
        this.goalSelector.addGoal(6, new net.minecraft.world.entity.ai.goal.LookAtPlayerGoal(this, net.minecraft.world.entity.player.Player.class, 8.0F));
        this.goalSelector.addGoal(7, new net.minecraft.world.entity.ai.goal.RandomLookAroundGoal(this));
    }

    @Override
    public boolean isPersistenceRequired() {
        return true;
    }

    @Override
    public net.minecraft.world.InteractionResult mobInteract(net.minecraft.world.entity.player.Player player,
            net.minecraft.world.InteractionHand hand) {
        net.minecraft.world.item.ItemStack stack = player.getItemInHand(hand);
        if (!isTame() && player.isShiftKeyDown() == false && !stack.isEmpty()
                && stack.is(net.minecraft.world.item.Items.EMERALD)) {
            if (!level().isClientSide) {
                if (getRandom().nextInt(3) == 0) {
                    setTame(true);
                    triggerAnim("tame");
                    setOwnerUUID(player.getUUID());
                } else {
                    triggerAnim("beg");
                }
                stack.shrink(1);
            }
            return net.minecraft.world.InteractionResult.sidedSuccess(level().isClientSide);
        }
        return super.mobInteract(player, hand);
    }

    public boolean isTame() {
        return entityData.get(TAME);
    }

    public void setTame(boolean tame) {
        entityData.set(TAME, tame);
    }

    public void setOwnerUUID(java.util.UUID uuid) {
        this.ownerUUID = uuid;
    }

    private java.util.UUID ownerUUID;

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.addAnimationController(new AnimationController<>(this, "movement", 0, this::animPredicate));
    }

    private <E extends GeoAnimatable> PlayState animPredicate(AnimationState<E> event) {
        if (getAnimOneShotTicks() > 0 && getAnimOneShot() != null) {
            event.getController().setAnimation(RawAnimation.begin()
                    .thenPlay("animation.lumox." + getAnimOneShot()));
            return PlayState.CONTINUE;
        }
        if (event.isMoving() || isMovingEntity()) {
            event.getController().setAnimation(RawAnimation.begin().thenLoop(
                    isSprintingEntity() ? "animation.lumox.run" : "animation.lumox.walk"));
            return PlayState.CONTINUE;
        }
        event.getController().setAnimation(RawAnimation.begin().thenLoop("animation.lumox.idle"));
        return PlayState.CONTINUE;
    }

    private AnimatableInstanceCache geoCache = GeckoLibUtil.createInstanceCache(this);

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return geoCache;
    }

    @Override
    public double getTick(Object object) {
        return tickCount;
    }

}
