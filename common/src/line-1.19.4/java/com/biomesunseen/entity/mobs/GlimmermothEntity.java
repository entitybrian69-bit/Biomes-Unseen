package com.biomesunseen.entity.mobs;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.Level;
import software.bernie.geckolib3.core.PlayState;
import software.bernie.geckolib3.core.builder.AnimationBuilder;
import software.bernie.geckolib3.core.controller.AnimationController;
import software.bernie.geckolib3.core.event.predicate.AnimationState;
import software.bernie.geckolib3.core.manager.AnimationData;
import software.bernie.geckolib3.core.manager.AnimationFactory;
import software.bernie.geckolib3.util.GeckoLibUtil;

import software.bernie.geckolib3.core.IAnimatable;


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
 * Glimmermoth - creature with behaviours: flock, swarm, ambient_fly, attracted_to_light
 * Fully animated: idle, fly, flutter, land, hurt, death
 */
public class GlimmermothEntity extends BiomesUnseenMob {

    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
    }
    public GlimmermothEntity(EntityType<? extends GlimmermothEntity> type, Level level) {
        super(type, level, Content.mob("glimmermoth"));
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new net.minecraft.world.entity.ai.goal.FloatGoal(this));
        this.goalSelector.addGoal(1, new FleeDangerGoal(this, 1.3D));
        this.goalSelector.addGoal(3, new HerdFollowGoal(this, 1.1D));
        this.goalSelector.addGoal(3, new FlockGoal(this, 1.0D));
        this.goalSelector.addGoal(5, new net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal(this, 1.0D));
        this.goalSelector.addGoal(6, new net.minecraft.world.entity.ai.goal.LookAtPlayerGoal(this, net.minecraft.world.entity.player.Player.class, 8.0F));
        this.goalSelector.addGoal(7, new net.minecraft.world.entity.ai.goal.RandomLookAroundGoal(this));
    }

    @Override
    public boolean isPersistenceRequired() {
        return true;
    }

    @Override
    public void registerControllers(AnimationData data) {
        data.addAnimationController(new AnimationController<>(this, "movement", 0, this::animPredicate));
    }

    private <E extends IAnimatable> PlayState animPredicate(software.bernie.geckolib3.core.event.predicate.AnimationState<E> event) {
        AnimationBuilder builder = new AnimationBuilder();
        if (getAnimOneShotTicks() > 0 && getAnimOneShot() != null) {
            builder.addAnimation("animation.glimmermoth." + getAnimOneShot(), false);
        } else if (event.isMoving() || isMovingEntity()) {
            builder.addAnimation(isSprintingEntity() ? "animation.glimmermoth.run" : "animation.glimmermoth.walk", true);
        } else {
            builder.addAnimation("animation.glimmermoth.idle", true);
        }
        event.getController().setAnimation(builder);
        return PlayState.CONTINUE;
    }

    private AnimationFactory geoCache = new AnimationFactory(this);

    @Override
    public AnimationFactory getFactory() {
        return geoCache;
    }

}
