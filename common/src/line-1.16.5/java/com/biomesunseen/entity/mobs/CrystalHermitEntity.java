package com.biomesunseen.entity.mobs;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.Level;

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
 * Crystal Hermit - creature with behaviours: fortify, terrain_use, shell
 * Fully animated: idle, walk, shell, fortify, hurt, death
 */
public class CrystalHermitEntity extends BiomesUnseenMob {

    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
    }
    public CrystalHermitEntity(EntityType<? extends CrystalHermitEntity> type, Level level) {
        super(type, level, Content.mob("crystal_hermit"));
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new net.minecraft.world.entity.ai.goal.FloatGoal(this));
        this.goalSelector.addGoal(1, new FleeDangerGoal(this, 1.3D));
        this.goalSelector.addGoal(4, new TerrainUseGoal(this, 1.0D));
        this.goalSelector.addGoal(5, new net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal(this, 1.0D));
        this.goalSelector.addGoal(6, new net.minecraft.world.entity.ai.goal.LookAtGoal(this, net.minecraft.world.entity.player.Player.class, 8.0F));
        this.goalSelector.addGoal(7, new net.minecraft.world.entity.ai.goal.LookRandomlyGoal(this));
    }

    @Override
    public boolean isPersistenceRequired() {
        return true;
    }

}
