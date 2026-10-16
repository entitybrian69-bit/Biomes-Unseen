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
 * Lumox - creature with behaviours: graze, follow_herd, tameable
 * Fully animated: idle, walk, run, eat, graze, sit, tame
 */
public class LumoxEntity extends BiomesUnseenMob {

    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
        TAME = net.minecraft.network.datasync.EntityDataManager.defineId(LumoxEntity.class, net.minecraft.network.datasync.DataSerializers.BOOLEAN);
        entityData.define(TAME, false);
    }
    public LumoxEntity(EntityType<? extends LumoxEntity> type, World level) {
        super(type, level, Content.mob("lumox"));
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new net.minecraft.entity.ai.goal.SwimGoal(this));
        this.goalSelector.addGoal(1, new FleeDangerGoal(this, 1.3D));
        this.goalSelector.addGoal(3, new GrazeGoal(this));
        this.goalSelector.addGoal(3, new HerdFollowGoal(this, 1.1D));
        // Tameable: sit/follow wiring handled in mobInteract/onTamedInteraction.
        this.goalSelector.addGoal(5, new net.minecraft.entity.ai.goal.WaterAvoidingRandomWalkingGoal(this, 1.0D));
        this.goalSelector.addGoal(6, new net.minecraft.entity.ai.goal.LookAtGoal(this, net.minecraft.entity.player.PlayerEntity.class, 8.0F));
        this.goalSelector.addGoal(7, new net.minecraft.entity.ai.goal.LookRandomlyGoal(this));
    }

    @Override
    public boolean isPersistenceRequired() {
        return true;
    }

    @Override
    public net.minecraft.util.ActionResultType mobInteract(PlayerEntity player, net.minecraft.util.Hand hand) {
        net.minecraft.item.ItemStack stack = player.getItemInHand(hand);
        if (!isTame() && !stack.isEmpty() && stack.is(net.minecraft.item.Items.EMERALD)) {
            if (!level.isClientSide) {
                if (getRandom().nextInt(3) == 0) {
                    setTame(true);
                    triggerAnim("tame");
                } else {
                    triggerAnim("beg");
                }
                stack.shrink(1);
            }
            return net.minecraft.util.ActionResultType.SUCCESS;
        }
        return super.mobInteract(player, hand);
    }

    public boolean isTame() {
        return entityData.get(TAME);
    }

    public void setTame(boolean tame) {
        entityData.set(TAME, tame);
    }

    private net.minecraft.network.datasync.DataParameter<Boolean> TAME;

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
