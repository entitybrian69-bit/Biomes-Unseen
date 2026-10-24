package com.biomesunseen.entity;

import com.biomesunseen.registry.ModSounds;
import com.biomesunseen.spec.MobSpec;
import com.biomesunseen.spec.Specs;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.Level;
import net.minecraftforge.registries.ForgeRegistries;

/** Data-driven hostile mob: stats, effect and sounds come from its MobSpec. All AI goals are inherited. */
public class SpecMobEntity extends BaseHollowMob {
    private static final MobSpec FALLBACK = new MobSpec("unknown", "Unknown", "biped", "heartwood",
            0.7F, 2.0F, 20, 4, 0.26, 0, 0, 5, "none", 0, 0, 0x444444, 0xFFFFFF);

    private final MobSpec spec;

    public SpecMobEntity(EntityType<? extends SpecMobEntity> type, Level level) {
        super(type, level);
        ResourceLocation key = ForgeRegistries.ENTITY_TYPES.getKey(type);
        MobSpec found = key == null ? null : Specs.mobById(key.getPath());
        this.spec = found == null ? FALLBACK : found;
        this.xpReward = this.spec.xp();
    }

    public static AttributeSupplier.Builder attributes(MobSpec spec) {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, spec.health())
                .add(Attributes.MOVEMENT_SPEED, spec.speed())
                .add(Attributes.ATTACK_DAMAGE, spec.damage())
                .add(Attributes.ARMOR, spec.armor())
                .add(Attributes.FOLLOW_RANGE, 28.0D)
                .add(Attributes.KNOCKBACK_RESISTANCE, spec.knockback());
    }

    @Override
    protected String animName() {
        return spec.id();
    }

    @Override
    protected ModSounds.MobSet sounds() {
        return ModSounds.GENERIC.get(spec.archetype());
    }

    @Override
    public boolean causeFallDamage(float distance, float multiplier, net.minecraft.world.damagesource.DamageSource source) {
        return !"floater".equals(spec.archetype()) && super.causeFallDamage(distance, multiplier, source);
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof LivingEntity living) {
            applyEffect(living);
        }
        return hit;
    }

    private void applyEffect(LivingEntity victim) {
        int ticks = spec.effectTicks();
        int amp = spec.effectAmp();
        switch (spec.effect()) {
            case "poison" -> give(victim, MobEffects.POISON, ticks, amp);
            case "slow" -> give(victim, MobEffects.MOVEMENT_SLOWDOWN, ticks, amp);
            case "blind" -> give(victim, MobEffects.BLINDNESS, ticks, amp);
            case "wither" -> give(victim, MobEffects.WITHER, ticks, amp);
            case "weak" -> give(victim, MobEffects.WEAKNESS, ticks, amp);
            case "hunger" -> give(victim, MobEffects.HUNGER, ticks, amp);
            case "nausea" -> give(victim, MobEffects.CONFUSION, ticks, amp);
            case "levitate" -> give(victim, MobEffects.LEVITATION, ticks, amp);
            case "dark" -> give(victim, MobEffects.DARKNESS, ticks, amp);
            case "fire" -> victim.setSecondsOnFire(ticks);
            case "freeze" -> victim.setTicksFrozen(Math.max(victim.getTicksFrozen(), ticks));
            case "knock" -> {
                victim.knockback(1.3D, this.getX() - victim.getX(), this.getZ() - victim.getZ());
                victim.hurtMarked = true;
            }
            default -> {
            }
        }
    }

    private void give(LivingEntity victim, MobEffect effect, int ticks, int amp) {
        victim.addEffect(new MobEffectInstance(effect, ticks, amp), this);
    }
}
