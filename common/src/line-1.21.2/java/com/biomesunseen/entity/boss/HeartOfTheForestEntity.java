package com.biomesunseen.entity.boss;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.level.Level;


import com.biomesunseen.core.BossDef;
import com.biomesunseen.core.Content;
import com.biomesunseen.entity.BiomesUnseenMob;
import com.biomesunseen.entity.mobs.BramblebackEntity;
import com.biomesunseen.platform.PlatformExpect;
import com.biomesunseen.registry.ModItems;
import com.biomesunseen.registry.ModParticles;

import net.minecraft.world.item.ItemStack;

/**
 * The Heart of the Forest - multi-phase ancient tree-beast.
 *
 * Phases (health fractions): dormant > 75%, awakening 75-50%,
 * wrath 50-25%, final_bloom < 25%.
 * Attacks: root_slam, spore_cloud, summon_brambleback, verdant_beam,
 * regenerate, quake_stomp.  Custom music plays through PlatformExpect,
 * and every phase transition triggers its own animation.
 */
public class HeartOfTheForestEntity extends BiomesUnseenMob {

    private static final BossDef DEF = Content.boss("heart_of_the_forest");

    private int phase;
    private int attackCooldown;
    private int musicCooldown;
    private int summonCooldown;
    private int regenerateTicks;

    public HeartOfTheForestEntity(EntityType<? extends HeartOfTheForestEntity> type, Level level) {
        super(type, level, bossMobDef(DEF));
    }

    @Override
    protected void registerGoals() {
        // Boss AI is hand-driven in aiStep for deterministic phase behaviour.
    }

    public int phase() {
        return phase;
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (unseenLevel().isClientSide) {
            return;
        }
        float fraction = getHealth() / getMaxHealth();
        int newPhase = DEF.phaseForHealthFraction(fraction);
        if (newPhase != phase) {
            onPhaseChanged(newPhase);
            phase = newPhase;
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
            attackCooldown = 60 - phase * 10;
            performAttack(target);
        }
        if (phase >= 2 && --summonCooldown <= 0) {
            summonCooldown = 300;
            summonMinions();
        }
        if (phase == 3 && regenerateTicks > 0) {
            regenerateTicks--;
            heal(1.0F);
        }
    }

    private void onPhaseChanged(int newPhase) {
        triggerAnim(newPhase == 1 ? "awaken" : (newPhase == 2 ? "wrath" : "final_bloom"));
        if (newPhase >= 2) {
            regenerateTicks = 100;
        }
        playSound(SoundEvents.RAID_HORN, 2.0F, 0.8F);
    }

    private void performAttack(LivingEntity target) {
        double distance = distanceTo(target);
        int choice = getRandom().nextInt(4);
        if (choice == 0) {
            // root_slam: melee AoE
            triggerAnim("attack");
            if (distance < 6.0D) {
                target.hurt(unseenLevel().damageSources().mobAttack(this), (float) DEF.phaseAttackDamage(phase));
                target.setDeltaMovement(target.getDeltaMovement().add(0.0D, 0.6D, 0.0D));
            }
        } else if (choice == 1) {
            // spore_cloud
            triggerAnim("spore_cloud");
            if (distance < 12.0D) {
                target.hurt(unseenLevel().damageSources().mobAttack(this), 4.0F + phase * 2.0F);
                target.addEffect(new net.minecraft.world.effect.MobEffectInstance(
                        net.minecraft.world.effect.MobEffects.POISON, 80, 0));
            }
        } else if (choice == 2) {
            // verdant_beam: ranged
            triggerAnim("beam");
            if (distance < 24.0D) {
                target.hurt(unseenLevel().damageSources().mobAttack(this), 6.0F + phase * 2.0F);
                unseenLevel().broadcastEntityEvent(this, (byte) 4);
            }
        } else {
            // quake_stomp
            triggerAnim("slam");
            for (Player player : unseenLevel().getNearestPlayers(this, 10.0D, 10.0D)) {
                player.hurt(unseenLevel().damageSources().mobAttack(this), 5.0F + phase * 2.0F);
                player.setDeltaMovement(player.getDeltaMovement().add(0.0D, 0.8D, 0.0D));
            }
        }
    }

    private void summonMinions() {
        triggerAnim("summon");
        for (int i = 0; i < 2 + phase; i++) {
            BramblebackEntity minion = new BramblebackEntity(
                    com.biomesunseen.registry.ModEntities.Brambleback.get(), unseenLevel());
            minion.moveTo(blockPosition().getX() + getRandom().nextInt(7) - 3, getY(),
                    blockPosition().getZ() + getRandom().nextInt(7) - 3, 0.0F, 0.0F);
            unseenLevel().addFreshEntity(minion);
        }
    }

    @Override
    public void die(DamageSource source) {
        super.die(source);
        if (!unseenLevel().isClientSide) {
            // Boss loot: trophies, rare minerals and the boss artifact.
            spawnAtLocation(new ItemStack(ModItems.UNSEEN_SIGIL.get()));
            java.util.List<dev.architectury.registry.registries.RegistrySupplier<net.minecraft.world.item.Item>> minerals =
                    new java.util.ArrayList<>(ModItems.MINERALS.values());
            for (int i = 0; i < 4 && !minerals.isEmpty(); i++) {
                spawnAtLocation(new ItemStack(minerals.get(getRandom().nextInt(minerals.size())).get(), 2 + getRandom().nextInt(3)));
            }
            spawnAtLocation(new ItemStack(ModItems.TROPHIES.get("brambleback").get(), 3));
            if (getRandom().nextInt(4) == 0) {
                spawnAtLocation(new ItemStack(ModItems.GEAR.get("sylvanite_sword").get()));
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
