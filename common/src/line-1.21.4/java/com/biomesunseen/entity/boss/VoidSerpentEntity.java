package com.biomesunseen.entity.boss;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;


import com.biomesunseen.core.BossDef;
import com.biomesunseen.core.Content;
import com.biomesunseen.entity.BiomesUnseenMob;
import com.biomesunseen.platform.PlatformExpect;
import com.biomesunseen.registry.ModItems;

import net.minecraft.world.item.ItemStack;

/**
 * The Void Serpent - reality-phasing serpent in an unstable arena.
 *
 * Phases: coiled > 75%, phasing 75-50%, frenzy 50-25%, unmaking < 25%.
 * Attacks: void_beam, phase_shift (invulnerable blink), tail_sweep,
 * rift_barrage, devour (pull), gravity_well.  Teleports through the arena
 * and shifts out of reality between volleys.
 */
public class VoidSerpentEntity extends BiomesUnseenMob {

    private static final BossDef DEF = Content.boss("void_serpent");

    private int phase;
    private int attackCooldown;
    private int musicCooldown;
    private int phaseShiftTicks;
    private int bodySegments = 8;
    private final double[] segmentX = new double[8];
    private final double[] segmentY = new double[8];
    private final double[] segmentZ = new double[8];

    public VoidSerpentEntity(EntityType<? extends VoidSerpentEntity> type, Level level) {
        super(type, level, bossMobDef(DEF));
        setNoGravity(true);
    }

    @Override
    protected void registerGoals() {
        // Boss AI is hand-driven in aiStep for deterministic phase behaviour.
    }

    public int phase() {
        return phase;
    }

    public int phaseShiftTicks() {
        return phaseShiftTicks;
    }

    /** Segment positions for the animated segmented body model. */
    public double segmentX(int i) {
        return segmentX[Math.max(0, Math.min(i, bodySegments - 1))];
    }

    public double segmentY(int i) {
        return segmentY[Math.max(0, Math.min(i, bodySegments - 1))];
    }

    public double segmentZ(int i) {
        return segmentZ[Math.max(0, Math.min(i, bodySegments - 1))];
    }

    @Override
    public void aiStep() {
        super.aiStep();
        // Slithering body follow: each segment trails the previous one.
        double px = getX(), py = getY(), pz = getZ();
        for (int i = 0; i < bodySegments; i++) {
            double dx = px - segmentX[i];
            double dy = py - segmentY[i];
            double dz = pz - segmentZ[i];
            double dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
            if (dist > 1.2D) {
                double scale = (dist - 1.2D) / dist;
                segmentX[i] += dx * scale;
                segmentY[i] += dy * scale;
                segmentZ[i] += dz * scale;
            }
            px = segmentX[i];
            py = segmentY[i];
            pz = segmentZ[i];
        }
        if (unseenLevel().isClientSide) {
            return;
        }
        if (phaseShiftTicks > 0) {
            phaseShiftTicks--;
            return;
        }
        float fraction = getHealth() / getMaxHealth();
        int newPhase = DEF.phaseForHealthFraction(fraction);
        if (newPhase != phase) {
            phase = newPhase;
            triggerAnim("phase_shift");
            phaseShiftTicks = 30;
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
        // Keep airborne and circle the target.
        double angle = tickCount * 0.02D + phase;
        double radius = 8.0D + phase * 2.0D;
        getNavigation().moveTo(target.getX() + Math.cos(angle) * radius,
                target.getY() + 3.0D, target.getZ() + Math.sin(angle) * radius, 1.2D);
        if (--attackCooldown <= 0) {
            attackCooldown = 50 - phase * 8;
            performAttack(target);
        }
    }

    private void performAttack(LivingEntity target) {
        int choice = getRandom().nextInt(5);
        if (choice == 0) {
            // void_beam
            triggerAnim("beam");
            if (distanceTo(target) < 32.0D) {
                target.hurt(level().damageSources().mobAttack(this), (float) DEF.phaseAttackDamage(phase));
            }
        } else if (choice == 1) {
            // phase_shift: blink behind the target, invulnerable during
            triggerAnim("phase_shift");
            phaseShiftTicks = 25;
            moveTo(target.getX() + getRandom().nextInt(7) - 3, target.getY() + 2.0D,
                    target.getZ() + getRandom().nextInt(7) - 3, 0.0F, 0.0F);
        } else if (choice == 2) {
            // tail_sweep: AoE around body segments
            triggerAnim("tail_sweep");
            for (int i = 0; i < bodySegments; i += 2) {
                net.minecraft.world.phys.AABB box = new AABB(segmentX(i) - 2.0D, segmentY(i) - 2.0D, segmentZ(i) - 2.0D,
                        segmentX(i) + 2.0D, segmentY(i) + 2.0D, segmentZ(i) + 2.0D);
                for (LivingEntity entity : unseenLevel().getEntitiesOfClass(LivingEntity.class, box,
                        e -> e != this)) {
                    entity.hurt(level().damageSources().mobAttack(this), 4.0F + phase * 2.0F);
                }
            }
        } else if (choice == 3) {
            // rift_barrage
            triggerAnim("rift_barrage");
            for (int i = 0; i < 3 + phase; i++) {
                double sx = getX() + getRandom().nextGaussian() * 4.0D;
                double sy = getY() + getRandom().nextGaussian() * 2.0D;
                double sz = getZ() + getRandom().nextGaussian() * 4.0D;
                unseenLevel().broadcastDamageEvent(target, level().damageSources().mobAttack(this));
                target.hurt(level().damageSources().mobAttack(this), 2.0F + phase);
            }
        } else {
            // devour: pull the target in
            triggerAnim("devour");
            double dx = getX() - target.getX();
            double dy = getY() - target.getY();
            double dz = getZ() - target.getZ();
            target.setDeltaMovement(target.getDeltaMovement().add(
                    dx * 0.15D, -dy * 0.05D + 0.1D, dz * 0.15D));
        }
    }

    @Override
    public boolean isInvulnerableTo(DamageSource source) {
        return phaseShiftTicks > 0 || super.isInvulnerableTo(source);
    }

    @Override
    public void die(DamageSource source) {
        super.die(source);
        if (!unseenLevel().isClientSide) {
            spawnAtLocation(new ItemStack(ModItems.UNSEEN_SIGIL.get()));
            java.util.List<dev.architectury.registry.registries.RegistrySupplier<net.minecraft.world.item.Item>> minerals =
                    new java.util.ArrayList<>(ModItems.MINERALS.values());
            for (int i = 0; i < 5 && !minerals.isEmpty(); i++) {
                spawnAtLocation(new ItemStack(minerals.get(getRandom().nextInt(minerals.size())).get(), 3 + getRandom().nextInt(4)));
            }
            spawnAtLocation(new ItemStack(ModItems.TROPHIES.get("star_whale"), 3));
            if (getRandom().nextInt(4) == 0) {
                spawnAtLocation(new ItemStack(ModItems.GEAR.get("voidshard_sword")));
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
