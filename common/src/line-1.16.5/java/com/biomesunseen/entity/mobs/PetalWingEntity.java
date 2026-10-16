package com.biomesunseen.entity.mobs;

import net.minecraft.entity.EntityType;
import net.minecraft.world.World;
import com.biomesunseen.entity.legacy.LegacyAnimDriver;


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
 * Petal Wing - creature with behaviours: pollinate, flock, flee, attracted_to_flowers
 * Fully animated: idle, fly, flutter, pollinate, hurt, death
 */
public class PetalWingEntity extends BiomesUnseenMob {

    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
    }
    public PetalWingEntity(EntityType<? extends PetalWingEntity> type, World level) {
        super(type, level, Content.mob("petal_wing"));
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new net.minecraft.entity.ai.goal.SwimGoal(this));
        this.goalSelector.addGoal(1, new FleeDangerGoal(this, 1.3D));
        this.goalSelector.addGoal(3, new HerdFollowGoal(this, 1.1D));
        this.goalSelector.addGoal(3, new FlockGoal(this, 1.0D));
        this.goalSelector.addGoal(5, new net.minecraft.entity.ai.goal.WaterAvoidingRandomWalkingGoal(this, 1.0D));
        this.goalSelector.addGoal(6, new net.minecraft.entity.ai.goal.LookAtGoal(this, net.minecraft.entity.player.PlayerEntity.class, 8.0F));
        this.goalSelector.addGoal(7, new net.minecraft.entity.ai.goal.LookRandomlyGoal(this));
    }

    @Override
    public boolean isPersistenceRequired() {
        return true;
    }

    private final LegacyAnimDriver animDriver = new LegacyAnimDriver(this);

    @Override
    public void aiStep() {
        super.aiStep();
        animDriver.tick();
    }

    /** Legacy animation driver (no GeckoLib on 1.16.5): exposes pose data. */
    public LegacyAnimDriver animDriver() {
        return animDriver;
    }

}
