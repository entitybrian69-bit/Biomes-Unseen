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
 * Mosshorn - creature with behaviours: wander_trade, graze, barter
 * Fully animated: idle, walk, run, eat, trade, graze
 */
public class MosshornEntity extends BiomesUnseenMob {

    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
    }
    public MosshornEntity(EntityType<? extends MosshornEntity> type, Level level) {
        super(type, level, Content.mob("mosshorn"));
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new net.minecraft.world.entity.ai.goal.FloatGoal(this));
        this.goalSelector.addGoal(3, new GrazeGoal(this));
        this.goalSelector.addGoal(3, new HerdFollowGoal(this, 1.1D));
        this.goalSelector.addGoal(4, new WanderTradeGoal(this, 0.9D));
        this.goalSelector.addGoal(5, new net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal(this, 1.0D));
        this.goalSelector.addGoal(6, new net.minecraft.world.entity.ai.goal.LookAtPlayerGoal(this, net.minecraft.world.entity.player.Player.class, 8.0F));
        this.goalSelector.addGoal(7, new net.minecraft.world.entity.ai.goal.RandomLookAroundGoal(this));
    }

    @Override
    public boolean isPersistenceRequired() {
        return true;
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.addAnimationController(new AnimationController<>(this, "movement", 0, this::animPredicate));
    }

    private <E extends GeoAnimatable> PlayState animPredicate(AnimationState<E> event) {
        if (getAnimOneShotTicks() > 0 && getAnimOneShot() != null) {
            event.getController().setAnimation(RawAnimation.begin()
                    .thenPlay("animation.mosshorn." + getAnimOneShot()));
            return PlayState.CONTINUE;
        }
        if (event.isMoving() || isMovingEntity()) {
            event.getController().setAnimation(RawAnimation.begin().thenLoop(
                    isSprintingEntity() ? "animation.mosshorn.run" : "animation.mosshorn.walk"));
            return PlayState.CONTINUE;
        }
        event.getController().setAnimation(RawAnimation.begin().thenLoop("animation.mosshorn.idle"));
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
