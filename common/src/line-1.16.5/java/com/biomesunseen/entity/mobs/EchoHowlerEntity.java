package com.biomesunseen.entity.mobs;

import net.minecraft.entity.EntityType;
import net.minecraft.world.World;

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
 * Echo Howler - monster with behaviours: call_pack, intimidate, pack_tactics
 * Fully animated: idle, walk, run, howl, attack, hurt, death
 */
public class EchoHowlerEntity extends BiomesUnseenMob {

    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
    }
    public EchoHowlerEntity(EntityType<? extends EchoHowlerEntity> type, World level) {
        super(type, level, Content.mob("echo_howler"));
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new net.minecraft.entity.ai.goal.SwimGoal(this));
        this.goalSelector.addGoal(2, new PackAttackGoal(this, 1.15D, true));
        this.targetSelector.addGoal(1, new net.minecraft.entity.ai.goal.NearestAttackableTargetGoal<>(this, net.minecraft.entity.player.PlayerEntity.class, true));
        this.targetSelector.addGoal(2, new net.minecraft.entity.ai.goal.HurtByTargetGoal(this));
        this.goalSelector.addGoal(3, new HerdFollowGoal(this, 1.1D));
        this.goalSelector.addGoal(4, new TerrainUseGoal(this, 1.0D));
        this.goalSelector.addGoal(5, new net.minecraft.entity.ai.goal.WaterAvoidingRandomWalkingGoal(this, 1.0D));
        this.goalSelector.addGoal(6, new net.minecraft.entity.ai.goal.LookAtGoal(this, net.minecraft.entity.player.PlayerEntity.class, 8.0F));
        this.goalSelector.addGoal(7, new net.minecraft.entity.ai.goal.LookRandomlyGoal(this));
    }

    @Override
    public boolean isPersistenceRequired() {
        return true;
    }

}
