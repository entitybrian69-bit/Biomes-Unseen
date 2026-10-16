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
 * Cinder Pup - creature with behaviours: pack_tactics, tameable, flee_when_alone
 * Fully animated: idle, walk, run, attack, beg, sit, tame
 */
public class CinderPupEntity extends BiomesUnseenMob {

    private static final net.minecraft.network.syncher.EntityDataAccessor<Boolean> TAME =
            net.minecraft.network.syncher.SynchedEntityData.defineId(CinderPupEntity.class, net.minecraft.network.syncher.EntityDataSerializers.BOOLEAN);
    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
        entityData.define(TAME, false);
    }
    public CinderPupEntity(EntityType<? extends CinderPupEntity> type, Level level) {
        super(type, level, Content.mob("cinder_pup"));
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new net.minecraft.world.entity.ai.goal.FloatGoal(this));
        this.goalSelector.addGoal(1, new FleeDangerGoal(this, 1.3D));
        this.goalSelector.addGoal(2, new PackAttackGoal(this, 1.15D, true));
        this.targetSelector.addGoal(1, new net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal<>(this, net.minecraft.world.entity.player.Player.class, true));
        this.targetSelector.addGoal(2, new net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal(this));
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
            if (!unseenLevel().isClientSide) {
                if (getRandom().nextInt(3) == 0) {
                    setTame(true);
                    triggerAnim("tame");
                    setOwnerUUID(player.getUUID());
                } else {
                    triggerAnim("beg");
                }
                stack.shrink(1);
            }
            return net.minecraft.world.InteractionResult.sidedSuccess(unseenLevel().isClientSide);
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

}
