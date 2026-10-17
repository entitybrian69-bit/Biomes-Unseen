package com.biomesunseen.entity.boss;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.level.Level;


import com.biomesunseen.core.BossDef;
import com.biomesunseen.core.Content;
import com.biomesunseen.platform.PlatformExpect;
import com.biomesunseen.registry.ModItems;

import net.minecraft.world.item.ItemStack;

/**
 * The Skyward Crown - a crowned raptor that rules the floating isles
 *
 * <p>Health-gated four-phase encounter.  Phase transitions fire their own
 * GeckoLib one-shot, the attack rotation re-arms per phase, and the boss
 * announces every phase through its own music track.</p>
 */
public class TheSkywardCrownEntity extends BiomesUnseenMob {

    private static final BossDef DEF = Content.boss("the_skyward_crown");

    private int phase;
    private int attackCooldown;
    private int musicCooldown;

    public TheSkywardCrownEntity(EntityType<? extends TheSkywardCrownEntity> type, Level level) {
        super(type, level, bossMobDef(DEF));
    }

    @Override
    protected void registerGoals() {
        // Driven from aiStep for deterministic phase behaviour.
    }

    public int phase() {
        return phase;
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (unseenLevel().isClientSide()) {
            return;
        }
        float fraction = getHealth() / getMaxHealth();
        int next = DEF.phaseForHealthFraction(fraction);
        if (next != phase) {
            onPhaseChanged(next);
            phase = next;
        }
        if (--musicCooldown <= 0) {
            musicCooldown = 600;
            PlatformExpect.playBossMusic((net.minecraft.server.level.ServerLevel) unseenLevel(),
                    blockPosition(), DEF.musicSoundEvent, 48);
        }
        LivingEntity target = getTarget();
        if (target == null) {
            return;
        }
        getLookControl().setLookAt(target, 30.0F, 30.0F);
        if (--attackCooldown <= 0) {
            attackCooldown = 70 - phase * 10;
            performAttack(target);
        }
    }

    private void onPhaseChanged(int next) {
        if (next == 1) {
            triggerAnim("haloed");
        } else if (next == 2) {
            triggerAnim("shardfall");
        } else if (next >= 3) {
            triggerAnim("last_light");
        }
        playSound(SoundEvents.RAID_HORN, 2.0F, 0.8F);
    }

    private void performAttack(LivingEntity target) {
        double distance = distanceTo(target);
        int choice = (getRandom().nextInt(4) + phase) % 4;
        if (choice == 0) {
            triggerAnim("aerial_dive");
            if (distance < 6.0D) {
                target.hurt(DamageSource.mobAttack(this), (float) DEF.phaseAttackDamage(phase));
            }
        } else if (choice == 1) {
            triggerAnim("gust_knockback");
            if (distance < 18.0D) {
                target.hurt(DamageSource.mobAttack(this), 5.0F + phase * 2.0F);
            }
        } else if (choice == 2) {
            triggerAnim("sunbeam");
            setPos(target.getX(), target.getY(), target.getZ());
            if (distance < 4.0D) {
                target.hurt(DamageSource.mobAttack(this), 3.0F + phase);
            }
        } else {
            triggerAnim("sunbeam");
            for (Player player : unseenLevel().getEntitiesOfClass(Player.class,
                    getBoundingBox().inflate(10.0D))) {
                player.hurt(DamageSource.mobAttack(this), 5.0F + phase * 2.0F);
                player.setDeltaMovement(player.getDeltaMovement().add(0.0D, 0.8D, 0.0D));
            }
        }
    }

    @Override
    public void die(DamageSource source) {
        super.die(source);
        if (!unseenLevel().isClientSide()) {
            // Guaranteed unique relic plus the shared sigil and mineral cache.
            spawnAtLocation(new ItemStack(ModItems.BOSS_RELICS.get("the_skyward_crown").get()));
            spawnAtLocation(new ItemStack(ModItems.UNSEEN_SIGIL.get()));
            for (int i = 0; i < 3; i++) {
                java.util.List<me.shedaniel.architectury.registry.RegistrySupplier<net.minecraft.world.item.Item>> minerals =
                        new java.util.ArrayList<>(ModItems.MINERALS.values());
                if (minerals.isEmpty()) {
                    break;
                }
                spawnAtLocation(new ItemStack(
                        minerals.get(getRandom().nextInt(minerals.size())).get(), 3));
            }
        }
    }

    @Override
    public boolean removeWhenFarAway(double distance) {
        return false;
    }

    @Override
    public boolean requiresCustomPersistence() {
        return true;
    }

}
