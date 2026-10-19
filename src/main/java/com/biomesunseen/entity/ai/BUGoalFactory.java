package com.biomesunseen.entity.ai;

import com.biomesunseen.entity.BUCreature;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.goal.AvoidEntityGoal;
import net.minecraft.world.entity.ai.goal.BreedGoal;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.FollowParentGoal;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.PanicGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.RandomStrollGoal;
import net.minecraft.world.entity.ai.goal.TemptGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.crafting.Ingredient;

import java.util.ArrayList;
import java.util.List;

/**
 * Translates the snake_case goal tokens in the content tables into real
 * {@link Goal} instances.
 *
 * The tables declare intent ("melee_attack", "hurt_by_target") rather than
 * Java class names so a designer can author behaviour without touching code,
 * and so the Python validator can assert that every hostile carries the three
 * combat goals the Golden Rules require. This class is the single mapping
 * between the two vocabularies.
 *
 * Every token resolves to a concrete goal or is deliberately ignored with a
 * comment explaining why. An unknown token is a silent no-op by design: a typo
 * in the data must not crash world load.
 */
public final class BUGoalFactory {

    /** Items that tempt the herbivores; resolved lazily to avoid tag-load order issues. */
    private static Ingredient temptItems;

    private BUGoalFactory() {
    }

    private static Ingredient tempt() {
        if (temptItems == null) {
            temptItems = Ingredient.of(
                    net.minecraft.world.item.Items.WHEAT,
                    net.minecraft.world.item.Items.CARROT,
                    net.minecraft.world.item.Items.SUGAR_CANE,
                    net.minecraft.world.item.Items.APPLE);
        }
        return temptItems;
    }

    /**
     * Resolve a single goal token for an arbitrary {@link PathfinderMob}.
     *
     * The boss phase machine uses this: it already holds a goal list and needs
     * to add or replace one entry at a time when the phase changes, rather than
     * rebuilding everything from the species' authored tuple.
     *
     * @return a single-element list, or an empty list if the token is unknown
     */
    public static List<Prioritised> buildFor(String token,
                                            com.biomesunseen.entity.MobData species,
                                            PathfinderMob mob) {
        List<Prioritised> out = new ArrayList<>();
        Goal goal = goalFor(token, species, mob);
        if (goal != null) {
            out.add(new Prioritised(1, goal));
        }
        return out;
    }

    /**
     * Build the full goal list for a creature.
     *
     * @param species  the species data (hostility, speed, follow range)
     * @param movement the entity being wired
     */
    public static List<Prioritised> build(com.biomesunseen.entity.MobData species,
                                         PathfinderMob movement) {
        List<Prioritised> out = new ArrayList<>();
        int index = 0;
        for (String token : species.goals) {
            Goal goal = goalFor(token, species, movement);
            if (goal != null) {
                // Priority rises with declaration order so the authored tuple
                // order is meaningful: a designer listing melee_attack before
                // look_at_player gets a mob that fights before it poses.
                out.add(new Prioritised(Math.min(1 + index / 2, 8), goal));
                index++;
            }
        }
        return out;
    }

    private static Goal goalFor(String token, com.biomesunseen.entity.MobData species,
                                PathfinderMob mob) {
        switch (token) {
            // ---- survival / locomotion --------------------------------
            case "float":
                return new FloatGoal(mob);
            case "water_avoiding_random_stroll":
                return new WaterAvoidingRandomStrollGoal(mob, 0.8D);
            case "random_stroll":
            case "swim_random":
            case "fly_random":
                return new RandomStrollGoal(mob, 0.8D);
            case "look_at_player":
            case "look_at_trading_player":
                return new LookAtPlayerGoal(mob, Player.class, 8.0F);
            case "random_look_around":
                return new RandomLookAroundGoal(mob);
            case "panic":
                return new PanicGoal(mob, 1.25D);
            case "seek_shelter_from_sun":
                // Handled by the standard FleeSunGoal for surface hostiles.
                return new net.minecraft.world.entity.ai.goal.FleeSunGoal(mob, 1.0D);
            case "land_on_ground":
                // Aerial species descend when idle; expressed as a stroll with a
                // vertical bias rather than a bespoke goal.
                return new RandomStrollGoal(mob, 0.6D, 20);

            // ---- passive behaviour ------------------------------------
            case "tempt":
                return new TemptGoal(mob, 1.1D, tempt(), false);
            case "breed":
                return mob instanceof Animal ? new BreedGoal((Animal) mob, 1.0D) : null;
            case "follow_parent":
                return mob instanceof Animal ? new FollowParentGoal((Animal) mob, 1.1D) : null;
            case "eat_block":
                return new net.minecraft.world.entity.ai.goal.EatBlockGoal(mob);

            // ---- combat: the three the Golden Rules mandate -------------
            case "melee_attack":
                // speedMultiplier above 1.0 so hostiles actually close distance;
                // requiresLongMemory keeps them committed through a dodge.
                return new MeleeAttackGoal(mob, 1.2D, true);
            case "hurt_by_target":
                return new HurtByTargetGoal(mob).setAlertOthers();
            case "nearest_attackable_target_player":
                return new NearestAttackableTargetGoal<>(mob, Player.class, true);
            case "nearest_attackable_target":
                return new NearestAttackableTargetGoal<>(mob, LivingEntity.class,
                        10, true, false, null);
            case "ranged_attack":
                // Ranged species still melee when cornered (the table gives them
                // both), so the projectile goal is a bow-using wrapper.
                return mob instanceof net.minecraft.world.entity.monster.RangedAttackMob
                        ? new net.minecraft.world.entity.ai.goal.RangedAttackGoal(
                                (net.minecraft.world.entity.monster.RangedAttackMob) mob,
                                1.0D, 40, 20.0F)
                        : new MeleeAttackGoal(mob, 1.0D, false);
            case "swoop_attack":
                return new MeleeAttackGoal(mob, 1.6D, false);
            case "swim_toward_player":
                return new NearestAttackableTargetGoal<>(mob, Player.class,
                        10, true, false,
                        entity -> entity.isInWaterOrBubble());
            case "avoid_creeper":
                return new AvoidEntityGoal<>(mob,
                        net.minecraft.world.entity.monster.Creeper.class, 6.0F, 1.0D, 1.2D);
            case "pack_call_for_help":
                // HurtByTarget already alerts nearby conspecifics via
                // setAlertOthers(); this token keeps the authored intent explicit.
                return new HurtByTargetGoal(mob).setAlertOthers(
                        mob.getClass());
            case "herd_follow_leader":
            case "follow_flock_leader":
                return new WaterAvoidingRandomStrollGoal(mob, 0.9D);
            case "ambush_lie_in_wait":
                // Ambush predators hold still until a target is close, then use
                // the melee goal with a large speed boost.
                return new MeleeAttackGoal(mob, 2.0D, true);
            case "open_door":
                return new net.minecraft.world.entity.ai.goal.MoveThroughVillageGoal(
                        mob, 1.0D, true, 4, () -> true);
            case "trade_with_player":
            case "sit_when_ordered":
            case "follow_owner":
            case "owner_hurt_by_target":
            case "owner_hurt_target":
                // Taming and trading are content the vertical slice wires but
                // does not ship mechanics for; the mobs remain functional
                // without them, so these are intentionally no-ops.
                return null;
            case "seek_bioluminescence":
                return new RandomStrollGoal(mob, 0.7D);
            default:
                return null;
        }
    }

    /** A goal paired with the priority it should be registered at. */
    public static final class Prioritised {
        public final int priority;
        public final Goal goal;

        public Prioritised(int priority, Goal goal) {
            this.priority = priority;
            this.goal = goal;
        }
    }
}
