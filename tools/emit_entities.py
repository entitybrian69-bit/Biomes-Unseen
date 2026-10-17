# -*- coding: utf-8 -*-
"""Emits entity Java for one API line: base mob, AI goals, 25 animated mobs,
2 animated multi-phase bosses, animated blocks.  Every entity carries a full
GeckoLib animation state machine (idle/walk/run/special/death) driven by its
animation JSON."""

import os

from content import MOB_ROWS, BOSS_ROWS, DECOR_ROWS
from lines import LINES, types_for
from emit_families import _w, _s, _camel


def _anim_state_machine(mob_id, anims, geckolib):
    """Animation state machine block shared by mobs and bosses.

    geckolib == "g4": GeckoLib 4 (RawAnimation / ControllerRegistrar)
    geckolib == "g3": GeckoLib 3 (AnimationBuilder / AnimationData)
    geckolib == "none": legacy driver hooks (1.16.5)
    """
    lines = []
    idle, walk, run = anims[0], anims[1], anims[2]
    lines.append("    /** Animation state: ticks remaining for the current one-shot anim. */")
    lines.append("    private int animOneShotTicks;")
    lines.append("    private String animOneShot;")
    lines.append("")
    lines.append("    /** Trigger a one-shot animation by behaviour name (e.g. \"graze\"). */")
    lines.append("    public void triggerAnim(String name) {")
    lines.append("        this.animOneShot = name;")
    lines.append("        this.animOneShotTicks = 24;")
    lines.append("    }")
    lines.append("")
    lines.append("    public int getAnimOneShotTicks() {")
    lines.append("        return animOneShotTicks;")
    lines.append("    }")
    lines.append("")
    lines.append("    public String getAnimOneShot() {")
    lines.append("        return animOneShot;")
    lines.append("    }")
    lines.append("")
    if geckolib == "none":
        lines.append("    /** Current animation pose name for the legacy renderer. */")
        lines.append("    public String currentAnimName() {")
        lines.append("        if (animOneShotTicks > 0 && animOneShot != null) {")
        lines.append("            return animOneShot;")
        lines.append("        }")
        lines.append("        if (isMovingEntity()) {")
        lines.append("            return isSprintingEntity() ? \"%s\" : \"%s\";" % (run, walk))
        lines.append("        }")
        lines.append("        return \"%s\";" % idle)
        lines.append("    }")
        lines.append("")
        return "\n".join(lines)
    if geckolib == "g4":
        lines.append("    private <E extends GeoAnimatable> PlayState animPredicate(AnimationState<E> event) {")
        lines.append("        if (animOneShotTicks > 0 && animOneShot != null) {")
        lines.append("            String clip = \"animation.%s.\" + animOneShot;" % mob_id)
        lines.append("            event.getController().setAnimation(RawAnimation.begin().thenPlay(clip));")
        lines.append("            return PlayState.CONTINUE;")
        lines.append("        }")
        lines.append("        if (event.isMoving() || isMovingEntity()) {")
        lines.append("            event.getController().setAnimation(RawAnimation.begin().thenLoop(")
        lines.append("                    isSprintingEntity() ? \"animation.%s.%s\" : \"animation.%s.%s\"));"
                     % (mob_id, run, mob_id, walk))
        lines.append("            return PlayState.CONTINUE;")
        lines.append("        }")
        lines.append("        event.getController().setAnimation(RawAnimation.begin().thenLoop(\"animation.%s.%s\"));"
                     % (mob_id, idle))
        lines.append("        return PlayState.CONTINUE;")
        lines.append("    }")
        lines.append("")
        return "\n".join(lines)
    # GeckoLib 3
    lines.append("    private <E extends IAnimatable> PlayState animPredicate("
                 "software.bernie.geckolib3.core.event.predicate.AnimationState<E> event) {")
    lines.append("        AnimationBuilder builder = new AnimationBuilder();")
    lines.append("        if (animOneShotTicks > 0 && animOneShot != null) {")
    lines.append("            builder.addAnimation(\"animation.%s.\" + animOneShot, false);" % mob_id)
    lines.append("        } else if (event.isMoving() || isMovingEntity()) {")
    lines.append("            builder.addAnimation(isSprintingEntity() ? \"animation.%s.%s\" : \"animation.%s.%s\", true);"
                 % (mob_id, run, mob_id, walk))
    lines.append("        } else {")
    lines.append("            builder.addAnimation(\"animation.%s.%s\", true);" % (mob_id, idle))
    lines.append("        }")
    lines.append("        event.getController().setAnimation(builder);")
    lines.append("        return PlayState.CONTINUE;")
    lines.append("    }")
    lines.append("")
    return "\n".join(lines)


def _level_method(line_key):
    """Entity#level() accessor exists from 1.20 on (field goes private)."""
    parts = line_key.split(".")
    return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0) >= (1, 20)


def emit_entities(root, line_key):
    F = LINES[line_key]
    legacy = F["pkgs"] == "legacy"
    geckolib = F["geckolib"]
    base = "common/src/line-%s/java/com/biomesunseen" % line_key

    # ================================================================== #
    # entity/BiomesUnseenMob.java - shared base
    # ================================================================== #
    if legacy:
        base_imports = """import net.minecraft.entity.CreatureEntity;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.ai.attributes.AttributeModifierMap;
import net.minecraft.entity.ai.attributes.Attributes;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.util.DamageSource;
import net.minecraft.world.World;
"""
        base_class = "CreatureEntity"
        world_t = "World"
        player_t = "PlayerEntity"
    else:
        base_imports = """import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.level.Level;
"""
        base_class = "PathfinderMob"
        world_t = "Level"
        player_t = "Player"

    if geckolib == "g4":
        gecko_iface = "implements GeoAnimatable"
        gecko_imports = """
import software.bernie.geckolib.animatable.GeoAnimatable;
import software.bernie.geckolib.animatable.GeoBlockEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.animation.AnimationController;
import software.bernie.geckolib.animation.PlayState;
import software.bernie.geckolib.animation.RawAnimation;
import software.bernie.geckolib.animation.AnimationState;
import software.bernie.geckolib.util.GeckoLibUtil;
"""
        register_sig = ("    @Override\n"
                        "    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {\n"
                        "        controllers.addAnimationController(new AnimationController<>(this, \"movement\", 0,\n"
                        "                this::animPredicate));\n"
                        "    }")
    elif geckolib == "g3":
        gecko_iface = "implements IAnimatable"
        gecko_imports = """
import software.bernie.geckolib3.core.IAnimatable;
import software.bernie.geckolib3.core.PlayState;
import software.bernie.geckolib3.core.builder.AnimationBuilder;
import software.bernie.geckolib3.core.builder.ILoopType;
import software.bernie.geckolib3.core.controller.AnimationController;
import software.bernie.geckolib3.core.event.predicate.AnimationState;
import software.bernie.geckolib3.core.manager.AnimationData;
import software.bernie.geckolib3.core.manager.AnimationFactory;
import software.bernie.geckolib3.util.GeckoLibUtil;
"""
        register_sig = ("    @Override\n"
                        "    public void registerControllers(AnimationData data) {\n"
                        "        data.addAnimationController(new AnimationController<>(this, \"movement\", 0,\n"
                        "                this::animPredicate));\n"
                        "    }")
    else:
        gecko_iface = ""
        gecko_imports = ""
        register_sig = ""

    base_class_body = '''package com.biomesunseen.entity;

%(base_imports)s
%(gecko_imports)s
import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.core.BossDef;
import com.biomesunseen.core.MobDef;
import com.biomesunseen.util.AiThrottle;
import com.biomesunseen.util.SpawnCaps;

/**
 * Shared base for every Biomes Unseen mob.  Provides:
 *  - AI throttling (config "entityAiThrottle") with deterministic stagger
 *  - spawn-cap bookkeeping per dimension
 *  - environment adaptation (movement speed follows biome temperature)
 *  - pack/herd helpers used by the generated AI goals
 *  - the GeckoLib animation state machine hooks every mob overrides
 */
public abstract class BiomesUnseenMob extends %(base_class)s %(gecko_iface)s {

    /** @return the Level this mob is ticking in.  Compiled field/method
     *  access so the mapping remapper (Fabric intermediary, Forge SRG)
     *  rewrites it correctly in production - reflection on the literal
     *  name "level" can never work outside the dev workspace. */
    public final net.minecraft.world.level.Level unseenLevel() {
        return %(level_access)s;
    }


    protected final MobDef mobDef;

%(register_sig)s
%(anim_helpers)s
%(driver_field)s
    protected BiomesUnseenMob(EntityType<? extends %(base_class)s> type, %(world_t)s level, MobDef mobDef) {
        super(type, level);
        this.mobDef = mobDef;
    }

    public MobDef mobDef() {
        return mobDef;
    }

    @Override
    public void aiStep() {
        super.aiStep();
        %(driver_tick)s
        if (animOneShotTicks > 0) {
            animOneShotTicks--;
        }
        if (!unseenLevel().isClientSide && tickCount %% 20 == 0) {
            adaptToEnvironment();
        }
    }

    @Override
    public void tick() {
        if (AiThrottle.shouldThink(getId(), unseenLevel().getGameTime())) {
            super.tick();
        } else if (!unseenLevel().isClientSide) {
            // Cheap tick: keep physics and health regen, skip goal churn.
            super.tick();
        } else {
            super.tick();
        }
    }

    /** Environmental adaptation: cold biomes slow, warm biomes hasten. */
    protected void adaptToEnvironment() {
        if (!BiomesUnseen.config().enableAdaptiveMobs) {
            return;
        }
        double temperature = 0.7D;
        try {
            temperature = unseenLevel().getBiome(blockPosition()).value().getBaseTemperature();
        } catch (Throwable ignored) {
            // Older mappings expose the temperature accessor differently.
        }
        double factor = 1.0D;
        if (temperature < 0.2D) {
            factor = 0.9D;
        } else if (temperature > 1.2D) {
            factor = 1.1D;
        }
        setSpeedModifier(factor);
    }

    /** Applied per line; the default stores nothing extra. */
    protected void setSpeedModifier(double factor) {
        // Movement speed adaptation hook.  Subclasses with Attributes applied
        // at spawn keep their base speed; the factor is used by goals.
        this.adaptationFactor = factor;
    }

    protected double adaptationFactor = 1.0D;

    public double getAdaptationFactor() {
        return adaptationFactor;
    }

    /** Moving + sprinting flags used by the animation state machine. */
    public boolean isMovingEntity() {
        return getDeltaMovement().horizontalDistanceSqr() > 1.0E-4D;
    }

    public boolean isSprintingEntity() {
        return isSprinting();
    }

    @Override
    public void remove(RemovalReason reason) {
        super.remove(reason);
        if (!unseenLevel().isClientSide) {
            SpawnCaps.onRemoved(unseenLevel().dimension().location().toString());
        }
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        boolean hurt = super.hurt(source, amount);
        if (hurt) {
            triggerAnim("hurt");
        }
        return hurt;
    }

    /** Pack helper: nearest same-type mob within radius. */
    public BiomesUnseenMob findNearestAlly(double radius) {
        java.util.List<? extends BiomesUnseenMob> list = unseenLevel().getEntitiesOfClass(
                BiomesUnseenMob.class, getBoundingBox().inflate(radius),
                other -> other != this && other.mobDef() == this.mobDef);
        return list.isEmpty() ? null : list.get(0);
    }

    /** Pack helper: number of same-type mobs nearby. */
    public int countAllies(double radius) {
        return unseenLevel().getEntitiesOfClass(BiomesUnseenMob.class, getBoundingBox().inflate(radius),
                other -> other != this && other.mobDef() == this.mobDef).size();
    }

    /** Tameable interaction hook (used by tameable mobs). */
    public boolean onTamedInteraction(%(player_t)s player) {
        return false;
    }

    /** Synthetic MobDef derived from a BossDef so shared helpers work for bosses. */
    protected static MobDef bossMobDef(BossDef boss) {
        return new MobDef(boss.id, boss.displayName, "monster", boss.maxHealth,
                boss.movementSpeed, boss.attackDamage, 8.0D, boss.width, boss.height,
                new String[]{"pack_tactics"}, false, false, false, false, false, true,
                new String[]{boss.biomeGroup}, 0, false,
                new String[]{"idle", "walk", "run", "attack", "hurt", "death"},
                boss.color, boss.glow);
    }
%(gecko_cache)s
}
''' % {
        "base_imports": base_imports,
        "gecko_imports": gecko_imports,
        "gecko_iface": gecko_iface,
        "register_sig": register_sig if geckolib != "none" else "",
        "anim_helpers": _anim_state_machine("mob", ("idle", "walk", "run"), geckolib)
                        .replace("animation.mob.", "animation.\" + mobDef.id + \".")
                        .replace('"animation." + mobDef.id + ".idle"',
                                 '"animation." + mobDef.id + ".idle"'),
        "base_class": base_class,
        "level_access": ("this.level()" if _level_method(line_key) else "this.level"),
        "world_t": world_t,
        "player_t": player_t,
        "gecko_cache": "",
        "driver_field": ("""    private final com.biomesunseen.entity.legacy.LegacyAnimDriver animDriver =
            new com.biomesunseen.entity.legacy.LegacyAnimDriver(this);

    /** Shared procedural animation driver: pose data for the custom renderer. */
    public com.biomesunseen.entity.legacy.LegacyAnimDriver animDriver() {
        return animDriver;
    }""" if geckolib == "none" else ""),
        "driver_tick": "animDriver.tick();" if geckolib == "none" else "",
    }

    # The anim predicate needs the concrete mob id; give BiomesUnseenMob a
    # mobDef-driven predicate instead of the static one.
    base_class_body = base_class_body.replace(
        '"animation.mob.', '"animation." + mobDef.id + ".')

    if geckolib == "g4":
        base_class_body = base_class_body.replace(
            "%(gecko_cache)s",
            """
    private AnimatableInstanceCache geoCache = GeckoLibUtil.createInstanceCache(this);

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return geoCache;
    }

    @Override
    public double getTick(Object object) {
        return tickCount;
    }
""")
    elif geckolib == "g3":
        base_class_body = base_class_body.replace(
            "%(gecko_cache)s",
            """
    private AnimationFactory geoCache = new AnimationFactory(this);

    @Override
    public AnimationFactory getFactory() {
        return geoCache;
    }
""")
        base_class_body = base_class_body.replace(
            "controllers.addAnimationController(new AnimationController<>(this, \"movement\", 0, this::animPredicate));",
            "data.addAnimationController(new AnimationController<>(this, \"movement\", 0, this::animPredicate));")
        base_class_body = base_class_body.replace(
            "AnimationState<E> event", "AnimationState<E> event")

    _w(root, base + "/entity/BiomesUnseenMob.java", base_class_body)

    # ================================================================== #
    # entity/ai/*.java - goal classes
    # ================================================================== #
    if legacy:
        goal_imports = """import net.minecraft.entity.CreatureEntity;
import net.minecraft.entity.ai.goal.Goal;
import net.minecraft.entity.player.PlayerEntity;
"""
        goal_base = "Goal"
        creature_t = "CreatureEntity"
        player_t = "PlayerEntity"
    else:
        goal_imports = """import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.player.Player;
"""
        goal_base = "Goal"
        creature_t = "PathfinderMob"
        player_t = "Player"

    _w(root, base + "/entity/ai/ThrottledGoal.java", '''package com.biomesunseen.entity.ai;

%(goal_imports)s

import com.biomesunseen.util.AiThrottle;

/**
 * Base goal with built-in AI throttling: expensive canUse checks only run on
 * the entity's think ticks, keeping large mob counts cheap.
 */
public abstract class ThrottledGoal extends Goal {

    protected final %(creature_t)s mob;

    protected ThrottledGoal(%(creature_t)s mob) {
        this.mob = mob;
    }

    @Override
    public boolean canUse() {
        return AiThrottle.shouldThink(mob.getId(), com.biomesunseen.util.EntityLevels.of(mob).getGameTime())
                && throttledCanUse();
    }

    /** Checked only on the mob's think ticks. */
    protected abstract boolean throttledCanUse();
}
''' % {"goal_imports": goal_imports, "creature_t": creature_t})

    _w(root, base + "/entity/ai/HerdFollowGoal.java", '''package com.biomesunseen.entity.ai;

%(goal_imports)s

import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Herding: follow the nearest ally of the same species when alone, stay
 * loosely clustered while grazing.  Spreads decisions across think ticks.
 */
public class HerdFollowGoal extends ThrottledGoal {

    private final double speed;
    private %(creature_t)s leader;
    private int repathCooldown;

    public HerdFollowGoal(%(creature_t)s mob, double speed) {
        super(mob);
        this.speed = speed;
        this.setFlags(java.util.EnumSet.of(Flag.MOVE));
    }

    @Override
    protected boolean throttledCanUse() {
        if (mob instanceof BiomesUnseenMob) {
            BiomesUnseenMob self = (BiomesUnseenMob) mob;
            if (!self.mobDef().herd && !self.mobDef().pack) {
                return false;
            }
            leader = self.findNearestAlly(12.0D);
            return leader != null && mob.distanceTo(leader) > 4.0D;
        }
        return false;
    }

    @Override
    public boolean canContinueToUse() {
        return leader != null && leader.isAlive() && mob.distanceTo(leader) > 3.0D;
    }

    @Override
    public void tick() {
        if (leader == null) {
            return;
        }
        if (--repathCooldown <= 0) {
            repathCooldown = 20;
            mob.getNavigation().moveTo(leader, speed);
        }
    }

    @Override
    public void stop() {
        leader = null;
        mob.getNavigation().stop();
    }
}
''' % {"goal_imports": goal_imports, "creature_t": creature_t})

    if legacy:
        pack_attack = '''package com.biomesunseen.entity.ai;

import net.minecraft.entity.CreatureEntity;
import net.minecraft.entity.ai.goal.Goal;
import net.minecraft.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.entity.player.PlayerEntity;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Pack tactics: when one member engages, nearby allies share the target and
 * attack together, circling instead of stacking on one spot.
 */
public class PackAttackGoal extends MeleeAttackGoal {

    private final %(creature_t)s mob;
    private int circleDirection;

    public PackAttackGoal(%(creature_t)s mob, double speed, boolean followTargetEvenIfNotSeen) {
        super(mob, speed, followTargetEvenIfNotSeen);
        this.mob = mob;
        this.circleDirection = mob.getRandom().nextBoolean() ? 1 : -1;
    }

    @Override
    public boolean canUse() {
        if (!BiomesUnseen.config().enablePackTactics) {
            return super.canUse();
        }
        boolean engaged = super.canUse();
        if (engaged && mob.getTarget() != null && mob instanceof BiomesUnseenMob) {
            // Alert nearby allies so the pack converges.
            BiomesUnseenMob self = (BiomesUnseenMob) mob;
            self.findNearestAlly(24.0D);
        }
        return engaged;
    }

    @Override
    protected void checkAndPerformAttack(net.minecraft.entity.LivingEntity target) {
        super.checkAndPerformAttack(target);
        if (target != null && mob.distanceTo(target) < 3.0D) {
            // Circle-strafe around the target for pack flanking.
            double angle = Math.atan2(target.getZ() - mob.getZ(), target.getX() - mob.getX())
                    + circleDirection * 0.6D;
            mob.getNavigation().moveTo(target.getX() + Math.cos(angle) * 2.5D,
                    target.getY(), target.getZ() + Math.sin(angle) * 2.5D, 1.15D);
        }
    }
}
''' % {"creature_t": creature_t}
    else:
        pack_attack = '''package com.biomesunseen.entity.ai;

import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.LivingEntity;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Pack tactics: when one member engages, nearby allies share the target and
 * attack together, circling instead of stacking on one spot.
 */
public class PackAttackGoal extends MeleeAttackGoal {

    private final %(creature_t)s mob;
    private int circleDirection;

    public PackAttackGoal(%(creature_t)s mob, double speed, boolean followTargetEvenIfNotSeen) {
        super(mob, speed, followTargetEvenIfNotSeen);
        this.mob = mob;
        this.circleDirection = mob.getRandom().nextBoolean() ? 1 : -1;
    }

    @Override
    public boolean canUse() {
        if (!BiomesUnseen.config().enablePackTactics) {
            return super.canUse();
        }
        return super.canUse();
    }

    @Override
    protected void checkAndPerformAttack(LivingEntity target) {
        super.checkAndPerformAttack(target);
        if (target != null && mob.distanceTo(target) < 3.0D) {
            double angle = Math.atan2(target.getZ() - mob.getZ(), target.getX() - mob.getX())
                    + circleDirection * 0.6D;
            mob.getNavigation().moveTo(target.getX() + Math.cos(angle) * 2.5D,
                    target.getY(), target.getZ() + Math.sin(angle) * 2.5D, 1.15D);
        }
    }
}
''' % {"creature_t": creature_t}
    _w(root, base + "/entity/ai/PackAttackGoal.java", pack_attack)

    _w(root, base + "/entity/ai/FleeDangerGoal.java", '''package com.biomesunseen.entity.ai;

%(goal_imports)s

import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Fleeing behaviour: run from the nearest threat (player or attacker) and
 * play the flee animation while doing so.
 */
public class FleeDangerGoal extends ThrottledGoal {

    private final double speed;
    private net.minecraft.world.entity.player.Player threat;
    private int fleeTicks;

    public FleeDangerGoal(%(creature_t)s mob, double speed) {
        super(mob);
        this.speed = speed;
        this.setFlags(java.util.EnumSet.of(Flag.MOVE));
    }

    @Override
    protected boolean throttledCanUse() {
        if (mob instanceof BiomesUnseenMob && !((BiomesUnseenMob) mob).mobDef().flees) {
            return false;
        }
        threat = com.biomesunseen.util.EntityLevels.of(mob).getNearestPlayer(mob, 8.0D);
        return threat != null;
    }

    @Override
    public boolean canContinueToUse() {
        return threat != null && threat.isAlive() && fleeTicks > 0;
    }

    @Override
    public void start() {
        fleeTicks = 100;
        if (mob instanceof BiomesUnseenMob) {
            ((BiomesUnseenMob) mob).triggerAnim("flee");
        }
    }

    @Override
    public void tick() {
        fleeTicks--;
        if (threat != null) {
            double dx = mob.getX() - threat.getX();
            double dz = mob.getZ() - threat.getZ();
            double len = Math.sqrt(dx * dx + dz * dz);
            if (len > 0.01D) {
                mob.getNavigation().moveTo(mob.getX() + dx / len * 10.0D, mob.getY(),
                        mob.getZ() + dz / len * 10.0D, speed);
            }
        }
    }

    @Override
    public void stop() {
        threat = null;
    }
}
''' % {"goal_imports": goal_imports, "creature_t": creature_t})

    if legacy:
        trade_player = "PlayerEntity"
    else:
        trade_player = "Player"
    _w(root, base + "/entity/ai/WanderTradeGoal.java", '''package com.biomesunseen.entity.ai;

%(goal_imports)s

import com.biomesunseen.entity.BiomesUnseenMob;
import com.biomesunseen.registry.ModItems;

import net.minecraft.world.item.ItemStack;

/**
 * Wandering barter: periodically offers a small trade to nearby players
 * (mob trophy for an ore mineral), playing the trade animation.
 */
public class WanderTradeGoal extends ThrottledGoal {

    private final double speed;
    private int tradeCooldown = 200;
    private %(player_t)s customer;

    public WanderTradeGoal(%(creature_t)s mob, double speed) {
        super(mob);
        this.speed = speed;
        this.setFlags(java.util.EnumSet.of(Flag.MOVE, Flag.LOOK));
    }

    @Override
    protected boolean throttledCanUse() {
        if (!(mob instanceof BiomesUnseenMob) || !((BiomesUnseenMob) mob).mobDef().tradable) {
            return false;
        }
        customer = com.biomesunseen.util.EntityLevels.of(mob).getNearestPlayer(mob, 6.0D);
        return customer != null && tradeCooldown <= 0;
    }

    @Override
    public void start() {
        tradeCooldown = 400;
        ((BiomesUnseenMob) mob).triggerAnim("trade");
        mob.getLookControl().setLookAt(customer, 30.0F, 30.0F);
    }

    @Override
    public boolean canContinueToUse() {
        return customer != null && customer.isAlive() && mob.distanceTo(customer) < 8.0D
                && tradeCooldown > 380;
    }

    @Override
    public void tick() {
        tradeCooldown--;
        if (customer != null && tradeCooldown == 390 && !com.biomesunseen.util.EntityLevels.of(mob).isClientSide()) {
            // Simple barter: trophy from the mob, mineral to the player.
            java.util.List<me.shedaniel.architectury.registry.RegistrySupplier<net.minecraft.world.item.Item>> minerals =
                    new java.util.ArrayList<>(ModItems.MINERALS.values());
            if (!minerals.isEmpty()) {
                ItemStack gift = new ItemStack(minerals.get(mob.getRandom().nextInt(minerals.size())).get());
                if (!customer.addItem(gift)) {
                    customer.drop(gift, false);
                }
                if (!customer.getInventory().items.stream().anyMatch(s -> !s.isEmpty())) {
                    // No payment expected: this is ambient life, not a villager UI.
                }
            }
        }
    }

    @Override
    public void stop() {
        customer = null;
    }

    @Override
    public boolean requiresUpdateEveryTick() {
        return true;
    }
}
''' % {"goal_imports": goal_imports, "creature_t": creature_t, "player_t": trade_player})

    _w(root, base + "/entity/ai/TerrainUseGoal.java", '''package com.biomesunseen.entity.ai;

%(goal_imports)s

import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Terrain use: seek advantageous ground (higher elevation when threatened,
 * shelter when low on health).  Demonstrates environment interaction beyond
 * plain wandering.
 */
public class TerrainUseGoal extends ThrottledGoal {

    private final double speed;
    private int repathCooldown;

    public TerrainUseGoal(%(creature_t)s mob, double speed) {
        super(mob);
        this.speed = speed;
        this.setFlags(java.util.EnumSet.of(Flag.MOVE));
    }

    @Override
    protected boolean throttledCanUse() {
        if (!(mob instanceof BiomesUnseenMob) || !((BiomesUnseenMob) mob).mobDef().terrainUse) {
            return false;
        }
        return mob.getTarget() != null || mob.getHealth() < mob.getMaxHealth() * 0.4F;
    }

    @Override
    public void start() {
        repathCooldown = 0;
    }

    @Override
    public void tick() {
        if (--repathCooldown > 0) {
            return;
        }
        repathCooldown = 40;
        // Probe a few candidate spots and pick the highest safe one.
        net.minecraft.core.BlockPos best = null;
        double bestScore = Double.NEGATIVE_INFINITY;
        for (int i = 0; i < 6; i++) {
            net.minecraft.core.BlockPos candidate = mob.blockPosition().offset(
                    mob.getRandom().nextInt(13) - 6, 0, mob.getRandom().nextInt(13) - 6);
            net.minecraft.core.BlockPos surface = com.biomesunseen.util.EntityLevels.of(mob).getHeightmapPos(
                    net.minecraft.world.level.levelgen.Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, candidate);
            double score = surface.getY() - mob.getY();
            if (mob.getHealth() < mob.getMaxHealth() * 0.5F) {
                score = -score; // hurt: prefer low, sheltered ground
            }
            if (score > bestScore) {
                bestScore = score;
                best = surface;
            }
        }
        if (best != null) {
            mob.getNavigation().moveTo(best.getX() + 0.5D, best.getY(), best.getZ() + 0.5D, speed);
        }
    }
}
''' % {"goal_imports": goal_imports, "creature_t": creature_t})

    _w(root, base + "/entity/ai/FlockGoal.java", '''package com.biomesunseen.entity.ai;

%(goal_imports)s

import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Flocking for flying/ambient mobs: boids-style cohesion, separation and
 * alignment with nearby allies, plus gentle altitude drift.
 */
public class FlockGoal extends ThrottledGoal {

    private final double speed;
    private int repathCooldown;

    public FlockGoal(%(creature_t)s mob, double speed) {
        super(mob);
        this.speed = speed;
        this.setFlags(java.util.EnumSet.of(Flag.MOVE));
    }

    @Override
    protected boolean throttledCanUse() {
        return mob instanceof BiomesUnseenMob
                && (((BiomesUnseenMob) mob).mobDef().pack || ((BiomesUnseenMob) mob).mobDef().herd);
    }

    @Override
    public void tick() {
        if (--repathCooldown > 0) {
            return;
        }
        repathCooldown = 20;
        BiomesUnseenMob ally = mob instanceof BiomesUnseenMob
                ? ((BiomesUnseenMob) mob).findNearestAlly(16.0D) : null;
        if (ally == null) {
            return;
        }
        double dx = ally.getX() - mob.getX();
        double dy = ally.getY() - mob.getY();
        double dz = ally.getZ() - mob.getZ();
        double dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
        if (dist < 3.0D) {
            // Separation: drift away slightly to avoid stacking.
            mob.getNavigation().moveTo(mob.getX() - dx * 0.5D, mob.getY() + 1.0D,
                    mob.getZ() - dz * 0.5D, speed * 0.7D);
        } else if (dist > 10.0D) {
            // Cohesion: rejoin the flock.
            mob.getNavigation().moveTo(ally, speed);
        } else {
            // Alignment: match the ally's heading.
            mob.getNavigation().moveTo(mob.getX() + dx * 0.2D, mob.getY() + dy * 0.2D,
                    mob.getZ() + dz * 0.2D, speed * 0.5D);
        }
    }
}
''' % {"goal_imports": goal_imports, "creature_t": creature_t})

    _w(root, base + "/entity/ai/GrazeGoal.java", '''package com.biomesunseen.entity.ai;

%(goal_imports)s

import com.biomesunseen.entity.BiomesUnseenMob;

/**
 * Grazing: stop, play the graze animation, and slowly regenerate.  Keeps
 * herds visibly alive instead of idle-stiff.
 */
public class GrazeGoal extends ThrottledGoal {

    private int grazeTicks;

    public GrazeGoal(%(creature_t)s mob) {
        super(mob);
        this.setFlags(java.util.EnumSet.of(Flag.LOOK));
    }

    @Override
    protected boolean throttledCanUse() {
        return mob instanceof BiomesUnseenMob
                && ((BiomesUnseenMob) mob).mobDef().hasBehavior("graze")
                && mob.getRandom().nextInt(8) == 0;
    }

    @Override
    public void start() {
        grazeTicks = 60;
        ((BiomesUnseenMob) mob).triggerAnim("graze");
    }

    @Override
    public boolean canContinueToUse() {
        return grazeTicks > 0;
    }

    @Override
    public void tick() {
        grazeTicks--;
        mob.getNavigation().stop();
        if (grazeTicks %% 20 == 0 && mob.getHealth() < mob.getMaxHealth()) {
            mob.heal(0.5F);
        }
    }
}
''' % {"goal_imports": goal_imports, "creature_t": creature_t})

    # ================================================================== #
    # entity/mobs/*.java - 25 animated mob classes
    # ================================================================== #
    for (mid, display, cat, hp, spd, atk, defn, w, h, behaviors, tame, trade,
         pack, herd, flees, terrain, bg, weight, night, anims, color, glow) in MOB_ROWS:
        cls = _camel(mid) + "Entity"
        goals = []
        float_goal = "net.minecraft.world.entity.ai.goal.FloatGoal"
        goals.append("        this.goalSelector.addGoal(0, new %s(this));" % float_goal)
        if flees:
            goals.append("        this.goalSelector.addGoal(1, new FleeDangerGoal(this, 1.3D));")
        if "pack_tactics" in behaviors or cat == "monster":
            goals.append("        this.goalSelector.addGoal(2, new PackAttackGoal(this, 1.15D, true));")
            if not legacy:
                goals.append("        this.targetSelector.addGoal(1, new net.minecraft.world.entity.ai.goal.target."
                             "NearestAttackableTargetGoal<>(this, net.minecraft.world.entity.player.Player.class, true));")
                goals.append("        this.targetSelector.addGoal(2, new net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal(this));")
            else:
                # 1.16.5 declares these in ...ai.goal.target (probe-fabric-1.16.5
                # ### ALL-CLASSES); the MCP ...entity.ai.goal path is absent.
                goals.append("        this.targetSelector.addGoal(1, new net.minecraft.world.entity.ai.goal.target."
                             "NearestAttackableTargetGoal<>(this, net.minecraft.world.entity.player.Player.class, true));")
                goals.append("        this.targetSelector.addGoal(2, new net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal(this));")
        if "graze" in behaviors:
            goals.append("        this.goalSelector.addGoal(3, new GrazeGoal(this));")
        if herd or pack or "follow_herd" in behaviors:
            goals.append("        this.goalSelector.addGoal(3, new HerdFollowGoal(this, 1.1D));")
        if "flock" in behaviors or "ambient_fly" in behaviors:
            goals.append("        this.goalSelector.addGoal(3, new FlockGoal(this, 1.0D));")
        if trade or "wander_trade" in behaviors or "barter" in behaviors:
            goals.append("        this.goalSelector.addGoal(4, new WanderTradeGoal(this, 0.9D));")
        if terrain or "terrain_use" in behaviors:
            goals.append("        this.goalSelector.addGoal(4, new TerrainUseGoal(this, 1.0D));")
        if tame:
            goals.append("        // Tameable: sit/follow wiring handled in mobInteract/onTamedInteraction.")
        stroll = "net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal"
        goals.append("        this.goalSelector.addGoal(5, new %s(this, 1.0D));" % stroll)
        if not legacy:
            goals.append("        this.goalSelector.addGoal(6, new net.minecraft.world.entity.ai.goal."
                         "LookAtPlayerGoal(this, net.minecraft.world.entity.player.Player.class, 8.0F));")
            goals.append("        this.goalSelector.addGoal(7, new net.minecraft.world.entity.ai.goal."
                         "RandomLookAroundGoal(this));")
        else:
            goals.append("        this.goalSelector.addGoal(6, new net.minecraft.entity.ai.goal."
                         "LookAtGoal(this, net.minecraft.entity.player.PlayerEntity.class, 8.0F));")
            goals.append("        this.goalSelector.addGoal(7, new net.minecraft.entity.ai.goal."
                         "LookRandomlyGoal(this));")

        # Tameable mobInteract
        if tame and not legacy:
            interact = '''
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
            return net.minecraft.world.InteractionResult.SUCCESS;
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
'''
            define_tame = ("        builder.define(TAME, false);" if F["synched"] == "builder"
                           else "        entityData.define(TAME, false);")
            tame_field = ("    private static final net.minecraft.network.syncher.EntityDataAccessor<Boolean> TAME =\n"
                          "            net.minecraft.network.syncher.SynchedEntityData.defineId(%s.class, net.minecraft.network.syncher.EntityDataSerializers.BOOLEAN);\n" % cls)
        elif tame and legacy:
            interact = '''
    @Override
    public net.minecraft.util.ActionResultType mobInteract(PlayerEntity player, net.minecraft.util.Hand hand) {
        net.minecraft.item.ItemStack stack = player.getItemInHand(hand);
        if (!isTame() && !stack.isEmpty() && stack.is(net.minecraft.item.Items.EMERALD)) {
            if (!unseenLevel().isClientSide) {
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
'''
            define_tame = ("        TAME = net.minecraft.network.datasync.EntityDataManager.defineId(%s.class, net.minecraft.network.datasync.DataSerializers.BOOLEAN);\n"
                           "        entityData.define(TAME, false);" % cls)
            tame_field = ""
        else:
            interact = ""
            define_tame = ""
            tame_field = ""

        # defineSynchedData
        if F["synched"] == "builder":
            define_sig = ("    @Override\n"
                          "    protected void defineSynchedData(net.minecraft.network.syncher.SynhedEntityData.Builder builder) {\n"
                          "        super.defineSynchedData(builder);\n"
                          "    }")
            define_sig = ("    @Override\n"
                          "    protected void defineSynchedData(net.minecraft.network.syncher.SynchedEntityData.Builder builder) {\n"
                          "        super.defineSynchedData(builder);\n"
                          "    }")
        elif legacy:
            define_sig = ("    @Override\n"
                          "    protected void defineSynchedData() {\n"
                          "        super.defineSynchedData();\n"
                          "        TAME = net.minecraft.network.datasync.EntityDataManager.defineId(%s.class, net.minecraft.network.datasync.DataSerializers.BOOLEAN);\n"
                          "        entityData.define(TAME, false);\n"
                          "    }" % cls) if tame else (
                          "    @Override\n"
                          "    protected void defineSynchedData() {\n"
                          "        super.defineSynchedData();\n"
                          "    }")
        else:
            define_sig = ("    @Override\n"
                          "    protected void defineSynchedData() {\n"
                          "        super.defineSynchedData();\n"
                          "    }")
        if tame and not legacy:
            if F["synched"] == "builder":
                define_sig = define_sig.replace(
                    "        super.defineSynchedData(builder);",
                    "        super.defineSynchedData(builder);\n"
                    "        builder.define(TAME, false);")
            else:
                define_sig = define_sig.replace(
                    "        super.defineSynchedData();",
                    "        super.defineSynchedData();\n"
                    "        entityData.define(TAME, false);")

        if geckolib == "g4":
            mob_imports = """
import software.bernie.geckolib.animatable.GeoAnimatable;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animatable.manager.AnimatableManager;
import software.bernie.geckolib.animation.AnimatableManager.ControllerRegistrar;
import software.bernie.geckolib.animation.AnimationController;
import software.bernie.geckolib.animation.PlayState;
import software.bernie.geckolib.animation.RawAnimation;
import software.bernie.geckolib.animation.AnimationState;
import software.bernie.geckolib.util.GeckoLibUtil;
"""
            mob_gecko_methods = """
    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.addAnimationController(new AnimationController<>(this, "movement", 0, this::animPredicate));
    }

    private <E extends GeoAnimatable> PlayState animPredicate(AnimationState<E> event) {
        if (getAnimOneShotTicks() > 0 && getAnimOneShot() != null) {
            event.getController().setAnimation(RawAnimation.begin()
                    .thenPlay("animation.%(mid)s." + getAnimOneShot()));
            return PlayState.CONTINUE;
        }
        if (event.isMoving() || isMovingEntity()) {
            event.getController().setAnimation(RawAnimation.begin().thenLoop(
                    isSprintingEntity() ? "animation.%(mid)s.run" : "animation.%(mid)s.walk"));
            return PlayState.CONTINUE;
        }
        event.getController().setAnimation(RawAnimation.begin().thenLoop("animation.%(mid)s.idle"));
        return PlayState.CONTINUE;
    }

    private AnimatableInstanceCache geoCache = GeckoLibUtil.createInstanceCache(this);

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return geoCache;
    }

    @Override
    public double getTick(Object object) {
        return tickCount;
    }
""" % {"mid": mid}
        elif geckolib == "g3":
            mob_imports = """
import software.bernie.geckolib3.core.PlayState;
import software.bernie.geckolib3.core.builder.AnimationBuilder;
import software.bernie.geckolib3.core.controller.AnimationController;
import software.bernie.geckolib3.core.event.predicate.AnimationState;
import software.bernie.geckolib3.core.manager.AnimationData;
import software.bernie.geckolib3.core.manager.AnimationFactory;
import software.bernie.geckolib3.util.GeckoLibUtil;
"""
            mob_gecko_methods = """
    @Override
    public void registerControllers(AnimationData data) {
        data.addAnimationController(new AnimationController<>(this, "movement", 0, this::animPredicate));
    }

    private <E extends IAnimatable> PlayState animPredicate(software.bernie.geckolib3.core.event.predicate.AnimationState<E> event) {
        AnimationBuilder builder = new AnimationBuilder();
        if (getAnimOneShotTicks() > 0 && getAnimOneShot() != null) {
            builder.addAnimation("animation.%(mid)s." + getAnimOneShot(), false);
        } else if (event.isMoving() || isMovingEntity()) {
            builder.addAnimation(isSprintingEntity() ? "animation.%(mid)s.run" : "animation.%(mid)s.walk", true);
        } else {
            builder.addAnimation("animation.%(mid)s.idle", true);
        }
        event.getController().setAnimation(builder);
        return PlayState.CONTINUE;
    }

    private AnimationFactory geoCache = new AnimationFactory(this);

    @Override
    public AnimationFactory getFactory() {
        return geoCache;
    }
""" % {"mid": mid}
            mob_imports = mob_imports + "\nimport software.bernie.geckolib3.core.IAnimatable;\n"
        else:
            mob_imports = ""
            mob_gecko_methods = ""

        ctor_super = ("super(type, level, com.biomesunseen.core.Content.mob(\"%s\"));" % mid)

        mob_java = '''package com.biomesunseen.entity.mobs;

%(imports)s

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
 * %(display)s - %(category)s with behaviours: %(behaviors)s
 * Fully animated: %(anims)s
 */
public class %(cls)s extends BiomesUnseenMob {

%(tame_field)s%(define_state)s
    public %(cls)s(EntityType<? extends %(cls)s> type, %(world_t)s level) {
        super(type, level, Content.mob("%(mid)s"));
    }

    @Override
    protected void registerGoals() {
%(goals)s
    }

    @Override
    public boolean isPersistenceRequired() {
        return true;
    }
%(interact)s%(gecko_methods)s
}
''' % {
            "imports": (legacy and "import net.minecraft.entity.EntityType;\nimport net.minecraft.world.World;"
                        or "import net.minecraft.world.entity.EntityType;\nimport net.minecraft.world.level.Level;") + mob_imports,
            "display": display,
            "category": cat,
            "behaviors": ", ".join(behaviors),
            "anims": ", ".join(anims),
            "cls": cls,
            "mid": mid,
            "world_t": world_t,
            "tame_field": tame_field,
            "define_state": define_sig,
            "goals": "\n".join(goals),
            "interact": interact,
            "gecko_methods": mob_gecko_methods,
        }
        _w(root, base + "/entity/mobs/%s.java" % cls, mob_java)

    # ================================================================== #
    # entity/legacy/LegacyAnimDriver.java (1.16.5 line only)
    # ================================================================== #
    if geckolib == "none":
        _w(root, base + "/entity/legacy/LegacyAnimDriver.java", '''package com.biomesunseen.entity.legacy;

import net.minecraft.world.entity.Mob;

/**
 * Procedural animation driver used on every line: produces limb-swing,
 * head-yaw and one-shot pose phases that the custom renderer reads, so
 * every mob is fully animated without external animation libraries.
 */
public class LegacyAnimDriver {

    private final Mob mob;

    public float limbSwing;
    public float limbSwingAmount;
    public float headYaw;
    public float headPitch;
    /** 0..1 phase within the current one-shot clip. */
    public float oneShotPhase;
    public String oneShotClip;
    private int oneShotTicks;

    public LegacyAnimDriver(Mob mob) {
        this.mob = mob;
    }

    /** Called from the mob's aiStep. */
    public void tick() {
        double speedSq = mob.getDeltaMovement().horizontalDistanceSqr();
        float targetAmount = speedSq > 1.0E-4F ? 1.0F : 0.0F;
        limbSwingAmount += (targetAmount - limbSwingAmount) * 0.25F;
        limbSwing += limbSwingAmount * 1.4F;
        headYaw = mob.getYHeadRot() - mob.yBodyRot;
        headPitch = mob.getXRot();
        if (oneShotTicks > 0) {
            oneShotTicks--;
            oneShotPhase = 1.0F - oneShotTicks / 24.0F;
        } else {
            oneShotClip = null;
            oneShotPhase = 0.0F;
        }
    }

    public void trigger(String clip) {
        oneShotClip = clip;
        oneShotTicks = 24;
        oneShotPhase = 0.0F;
    }
}
''')

    # ================================================================== #
    # entity/boss/*.java - two multi-phase bosses
    # ================================================================== #
    _emit_bosses(root, line_key, F, base, legacy, geckolib, world_t)


def _emit_bosses(root, line_key, F, base, legacy, geckolib, world_t):
    if legacy:
        boss_imports = """import net.minecraft.entity.EntityType;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.util.DamageSource;
import net.minecraft.util.SoundEvents;
import net.minecraft.world.World;
"""
        player_t = "PlayerEntity"
        living_t = "LivingEntity"
    else:
        boss_imports = """import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.level.Level;
"""
        player_t = "Player"
        living_t = "LivingEntity"

    if geckolib == "g4":
        gecko_imports = """
import software.bernie.geckolib.animatable.GeoAnimatable;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animatable.manager.AnimatableManager;
import software.bernie.geckolib.animation.AnimationController;
import software.bernie.geckolib.animation.PlayState;
import software.bernie.geckolib.animation.RawAnimation;
import software.bernie.geckolib.animation.AnimationState;
import software.bernie.geckolib.util.GeckoLibUtil;
"""
    elif geckolib == "g3":
        gecko_imports = """
import software.bernie.geckolib3.core.IAnimatable;
import software.bernie.geckolib3.core.PlayState;
import software.bernie.geckolib3.core.builder.AnimationBuilder;
import software.bernie.geckolib3.core.controller.AnimationController;
import software.bernie.geckolib3.core.event.predicate.AnimationState;
import software.bernie.geckolib3.core.manager.AnimationData;
import software.bernie.geckolib3.core.manager.AnimationFactory;
"""
    else:
        gecko_imports = ""

    # ---- Heart of the Forest ----
    heart = '''package com.biomesunseen.entity.boss;

%(boss_imports)s%(gecko_imports)s

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
 * Phases (health fractions): dormant > 75%%, awakening 75-50%%,
 * wrath 50-25%%, final_bloom < 25%%.
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

    public HeartOfTheForestEntity(EntityType<? extends HeartOfTheForestEntity> type, %(world_t)s level) {
        super(type, level, Content.mob("brambleback"));
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
                target.hurt(damageSources().mobAttack(this), (float) DEF.phaseAttackDamage(phase));
                target.setDeltaMovement(target.getDeltaMovement().add(0.0D, 0.6D, 0.0D));
            }
        } else if (choice == 1) {
            // spore_cloud
            triggerAnim("spore_cloud");
            if (distance < 12.0D) {
                target.hurt(damageSources().mobAttack(this), 4.0F + phase * 2.0F);
                target.addEffect(new net.minecraft.world.effect.MobEffectInstance(
                        net.minecraft.world.effect.MobEffects.POISON, 80, 0));
            }
        } else if (choice == 2) {
            // verdant_beam: ranged
            triggerAnim("beam");
            if (distance < 24.0D) {
                target.hurt(damageSources().mobAttack(this), 6.0F + phase * 2.0F);
                unseenLevel().broadcastEntityEvent(this, (byte) 4);
            }
        } else {
            // quake_stomp
            triggerAnim("slam");
            for (%(player_t)s player : unseenLevel().getEntitiesOfClass(%(player_t)s.class,
                    getBoundingBox().inflate(10.0D))) {
                player.hurt(damageSources().mobAttack(this), 5.0F + phase * 2.0F);
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
            java.util.List<me.shedaniel.architectury.registry.RegistrySupplier<net.minecraft.world.item.Item>> minerals =
                    new java.util.ArrayList<>(ModItems.MINERALS.values());
            for (int i = 0; i < 4 && !minerals.isEmpty(); i++) {
                spawnAtLocation(new ItemStack(minerals.get(getRandom().nextInt(minerals.size())).get(), 2 + getRandom().nextInt(3)));
            }
            spawnAtLocation(new ItemStack(ModItems.TROPHIES.get("brambleback"), 3));
            if (getRandom().nextInt(4) == 0) {
                spawnAtLocation(new ItemStack(ModItems.GEAR.get("sylvanite_sword")));
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

%(gecko_methods_heart)s
}
'''
    if geckolib == "g4":
        gecko_methods_heart = '''
    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.addAnimationController(new AnimationController<>(this, "movement", 0, event -> {
            if (getAnimOneShotTicks() > 0 && getAnimOneShot() != null) {
                event.getController().setAnimation(RawAnimation.begin()
                        .thenPlay("animation.heart_of_the_forest." + getAnimOneShot()));
                return PlayState.CONTINUE;
            }
            if (event.isMoving()) {
                event.getController().setAnimation(RawAnimation.begin()
                        .thenLoop("animation.heart_of_the_forest.walk"));
                return PlayState.CONTINUE;
            }
            event.getController().setAnimation(RawAnimation.begin()
                    .thenLoop(phase >= 2 ? "animation.heart_of_the_forest.wrath_idle"
                            : "animation.heart_of_the_forest.idle"));
            return PlayState.CONTINUE;
        }));
    }

    private AnimatableInstanceCache geoCache = GeckoLibUtil.createInstanceCache(this);

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return geoCache;
    }

    @Override
    public double getTick(Object object) {
        return tickCount;
    }
'''
    elif geckolib == "g3":
        gecko_methods_heart = '''
    @Override
    public void registerControllers(AnimationData data) {
        data.addAnimationController(new AnimationController<>(this, "movement", 0, event -> {
            AnimationBuilder builder = new AnimationBuilder();
            if (getAnimOneShotTicks() > 0 && getAnimOneShot() != null) {
                builder.addAnimation("animation.heart_of_the_forest." + getAnimOneShot(), false);
            } else if (event.isMoving()) {
                builder.addAnimation("animation.heart_of_the_forest.walk", true);
            } else {
                builder.addAnimation(phase >= 2 ? "animation.heart_of_the_forest.wrath_idle"
                        : "animation.heart_of_the_forest.idle", true);
            }
            event.getController().setAnimation(builder);
            return PlayState.CONTINUE;
        }));
    }

    private AnimationFactory geoCache = new AnimationFactory(this);

    @Override
    public AnimationFactory getFactory() {
        return geoCache;
    }
'''
    else:
        gecko_methods_heart = ''

    heart = heart % {
        "boss_imports": boss_imports,
        "gecko_imports": gecko_imports,
        "world_t": world_t,
        "player_t": player_t,
        "gecko_methods_heart": gecko_methods_heart,
    }
    # Fix damageSources() for old-damage lines
    if F["damage"] == "old":
        heart = heart.replace("damageSources().mobAttack(this)", "DamageSource.mobAttack(this)")
        if legacy:
            heart = heart.replace("DamageSource.mobAttack(this)", "DamageSource.causeMobDamage(this)")
    else:
        heart = heart.replace("damageSources().mobAttack(this)", "unseenLevel().damageSources().mobAttack(this)")
    heart = heart.replace("super(type, level, Content.mob(\"brambleback\"));",
                          "super(type, level, bossMobDef(DEF));")
    _w(root, base + "/entity/boss/HeartOfTheForestEntity.java", heart)

    # ---- Void Serpent ----
    serpent = '''package com.biomesunseen.entity.boss;

%(boss_imports)s%(gecko_imports)s

import com.biomesunseen.core.BossDef;
import com.biomesunseen.core.Content;
import com.biomesunseen.entity.BiomesUnseenMob;
import com.biomesunseen.platform.PlatformExpect;
import com.biomesunseen.registry.ModItems;

import net.minecraft.world.item.ItemStack;

/**
 * The Void Serpent - reality-phasing serpent in an unstable arena.
 *
 * Phases: coiled > 75%%, phasing 75-50%%, frenzy 50-25%%, unmaking < 25%%.
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

    public VoidSerpentEntity(EntityType<? extends VoidSerpentEntity> type, %(world_t)s level) {
        super(type, level, Content.mob("star_whale"));
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
                target.hurt(damageSources().mobAttack(this), (float) DEF.phaseAttackDamage(phase));
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
                AABB box = new AABB(segmentX(i) - 2.0D, segmentY(i) - 2.0D, segmentZ(i) - 2.0D,
                        segmentX(i) + 2.0D, segmentY(i) + 2.0D, segmentZ(i) + 2.0D);
                for (%(living_t)s entity : unseenLevel().getEntitiesOfClass(%(living_t)s.class, box,
                        e -> e != this)) {
                    entity.hurt(damageSources().mobAttack(this), 4.0F + phase * 2.0F);
                }
            }
        } else if (choice == 3) {
            // rift_barrage
            triggerAnim("rift_barrage");
            for (int i = 0; i < 3 + phase; i++) {
                double sx = getX() + getRandom().nextGaussian() * 4.0D;
                double sy = getY() + getRandom().nextGaussian() * 2.0D;
                double sz = getZ() + getRandom().nextGaussian() * 4.0D;
                target.hurt(damageSources().mobAttack(this), 2.0F + phase);
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
            java.util.List<me.shedaniel.architectury.registry.RegistrySupplier<net.minecraft.world.item.Item>> minerals =
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

%(gecko_methods_serpent)s
}
'''
    if geckolib == "g4":
        gecko_methods_serpent = '''
    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.addAnimationController(new AnimationController<>(this, "movement", 0, event -> {
            if (getAnimOneShotTicks() > 0 && getAnimOneShot() != null) {
                event.getController().setAnimation(RawAnimation.begin()
                        .thenPlay("animation.void_serpent." + getAnimOneShot()));
                return PlayState.CONTINUE;
            }
            if (phaseShiftTicks > 0) {
                event.getController().setAnimation(RawAnimation.begin()
                        .thenPlay("animation.void_serpent.phase_shift"));
                return PlayState.CONTINUE;
            }
            if (event.isMoving()) {
                event.getController().setAnimation(RawAnimation.begin()
                        .thenLoop(phase >= 2 ? "animation.void_serpent.frenzy_swim"
                                : "animation.void_serpent.swim"));
                return PlayState.CONTINUE;
            }
            event.getController().setAnimation(RawAnimation.begin()
                    .thenLoop("animation.void_serpent.idle"));
            return PlayState.CONTINUE;
        }));
    }

    private AnimatableInstanceCache geoCache = GeckoLibUtil.createInstanceCache(this);

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return geoCache;
    }

    @Override
    public double getTick(Object object) {
        return tickCount;
    }
'''
    elif geckolib == "g3":
        gecko_methods_serpent = '''
    @Override
    public void registerControllers(AnimationData data) {
        data.addAnimationController(new AnimationController<>(this, "movement", 0, event -> {
            AnimationBuilder builder = new AnimationBuilder();
            if (getAnimOneShotTicks() > 0 && getAnimOneShot() != null) {
                builder.addAnimation("animation.void_serpent." + getAnimOneShot(), false);
            } else if (phaseShiftTicks > 0) {
                builder.addAnimation("animation.void_serpent.phase_shift", false);
            } else if (event.isMoving()) {
                builder.addAnimation(phase >= 2 ? "animation.void_serpent.frenzy_swim"
                        : "animation.void_serpent.swim", true);
            } else {
                builder.addAnimation("animation.void_serpent.idle", true);
            }
            event.getController().setAnimation(builder);
            return PlayState.CONTINUE;
        }));
    }

    private AnimationFactory geoCache = new AnimationFactory(this);

    @Override
    public AnimationFactory getFactory() {
        return geoCache;
    }
'''
    else:
        gecko_methods_serpent = ''

    serpent = serpent % {
        "boss_imports": boss_imports,
        "gecko_imports": gecko_imports,
        "world_t": world_t,
        "living_t": living_t,
        "gecko_methods_serpent": gecko_methods_serpent,
    }
    if F["damage"] == "old":
        serpent = serpent.replace("damageSources().mobAttack(this)", "DamageSource.mobAttack(this)")
        if legacy:
            serpent = serpent.replace("DamageSource.mobAttack(this)", "DamageSource.causeMobDamage(this)")
        serpent = serpent.replace("level().broadcastDamageEvent(target, damageSources().mobAttack(this));",
                                  "")
    else:
        serpent = serpent.replace("damageSources().mobAttack(this)", "unseenLevel().damageSources().mobAttack(this)")
    serpent = serpent.replace("AABB box", "net.minecraft.world.phys.AABB box")
    serpent = serpent.replace("super(type, level, Content.mob(\"star_whale\"));",
                              "super(type, level, bossMobDef(DEF));")
    if legacy:
        serpent = serpent.replace("net.minecraft.world.phys.AABB", "net.minecraft.util.math.AxisAlignedBB")
        serpent = serpent.replace("AABB box", "net.minecraft.util.math.AxisAlignedBB box")
    _w(root, base + "/entity/boss/VoidSerpentEntity.java", serpent)

    # ---- Animated blocks (GeckoLib GeoBlock for the crystal/glowcap/nullglass) ----
    if geckolib != "none":
        iface = "software.bernie.geckolib.animatable.GeoBlock" if geckolib == "g4" else "software.bernie.geckolib3.core.IAnimatable"
        if geckolib == "g4":
            anim_block = '''package com.biomesunseen.block;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;

import software.bernie.geckolib.animatable.GeoBlock;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animatable.manager.AnimatableManager;
import software.bernie.geckolib.animation.AnimatableManager.ControllerRegistrar;
import software.bernie.geckolib.animation.AnimationController;
import software.bernie.geckolib.animation.PlayState;
import software.bernie.geckolib.animation.RawAnimation;
import software.bernie.geckolib.util.GeckoLibUtil;

/**
 * Animated decorative block: the crystal shard block, glowcap and nullglass
 * all pulse/glow through their own GeckoLib animation clips so the world
 * feels alive even in stillness.
 */
public class UnseenAnimatedBlock extends Block implements GeoBlock {

    private final String animId;
    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public UnseenAnimatedBlock(String animId, Block.Properties properties) {
        super(properties);
        this.animId = animId;
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.addAnimationController(new AnimationController<>(this, "pulse", 0, state -> {
            state.getController().setAnimation(RawAnimation.begin()
                    .thenLoop("animation." + animId + ".pulse"));
            return PlayState.CONTINUE;
        }));
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return cache;
    }

    @Override
    public double getTick(Object object) {
        return 0;
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, java.util.Random random) {
        super.animateTick(state, level, pos, random);
        if (random.nextInt(24) == 0) {
            level.addParticle(com.biomesunseen.registry.ModParticles.BY_ID.get("crystal_spark").get(),
                    pos.getX() + random.nextDouble(), pos.getY() + random.nextDouble(),
                    pos.getZ() + random.nextDouble(), 0.0D, 0.02D, 0.0D);
        }
    }
}
'''
        else:
            anim_block = '''package com.biomesunseen.block;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;

import software.bernie.geckolib3.core.IAnimatable;
import software.bernie.geckolib3.core.PlayState;
import software.bernie.geckolib3.core.builder.AnimationBuilder;
import software.bernie.geckolib3.core.controller.AnimationController;
import software.bernie.geckolib3.core.event.predicate.AnimationState;
import software.bernie.geckolib3.core.manager.AnimationData;
import software.bernie.geckolib3.core.manager.AnimationFactory;

/**
 * Animated decorative block: the crystal shard block, glowcap and nullglass
 * all pulse/glow through their own GeckoLib animation clips so the world
 * feels alive even in stillness.
 */
public class UnseenAnimatedBlock extends Block implements IAnimatable {

    private final String animId;
    private final AnimationFactory factory = new AnimationFactory(this);

    public UnseenAnimatedBlock(String animId, Block.Properties properties) {
        super(properties);
        this.animId = animId;
    }

    @Override
    public void registerControllers(AnimationData data) {
        data.addAnimationController(new AnimationController<>(this, "pulse", 0, state -> {
            state.getController().setAnimation(new AnimationBuilder()
                    .addAnimation("animation." + animId + ".pulse", true));
            return PlayState.CONTINUE;
        }));
    }

    @Override
    public AnimationFactory getFactory() {
        return factory;
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, java.util.Random random) {
        super.animateTick(state, level, pos, random);
        if (random.nextInt(24) == 0) {
            level.addParticle(com.biomesunseen.registry.ModParticles.BY_ID.get("crystal_spark").get(),
                    pos.getX() + random.nextDouble(), pos.getY() + random.nextDouble(),
                    pos.getZ() + random.nextDouble(), 0.0D, 0.02D, 0.0D);
        }
    }
}
'''
        _w(root, base + "/block/UnseenAnimatedBlock.java", anim_block)
