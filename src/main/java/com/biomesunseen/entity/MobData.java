package com.biomesunseen.entity;

/**
 * Immutable stat block for one creature species.
 *
 * Instances are generated into {@code BUContent.MOBS} from
 * {@code tools/content/mobs.py}. Field order there matches this constructor
 * exactly, so changing the order here breaks codegen -- keep them in sync.
 *
 * The class deliberately carries data and no behaviour: attribute suppliers,
 * goal wiring and render setup all read from it, which is what lets a single
 * {@link BUCreature} class back all 80 species instead of 80 near-identical
 * subclasses.
 */
public final class MobData {

    public final String id;
    public final String family;
    public final String dimension;
    public final boolean hostile;
    public final float maxHealth;
    public final float movementSpeed;
    public final float attackDamage;
    public final float attackKnockback;
    public final float followRange;
    public final float armour;
    public final float scale;
    public final boolean fireImmune;
    public final boolean canBreatheUnderwater;
    public final String renderLayer;
    public final float shadowRadius;
    public final int textureWidth;
    public final int textureHeight;
    public final String[] goals;
    public final String[] targetClasses;
    public final String spawnCategory;
    public final int spawnWeight;
    public final int spawnGroupMin;
    public final int spawnGroupMax;
    public final int experience;
    /** Animation ids the species' .animation.json must define. */
    public final String[] animations;
    /**
     * The unscaled collision box, in blocks.
     *
     * Kept separate from {@code scale} on purpose: the EntityType is sized with
     * these, and getDimensions applies the scale once on top. Folding scale into
     * both compounds it -- a species authored at 2.6 would come out 6.76x.
     */
    public final float modelWidth;
    public final float modelHeight;

    public MobData(String id, String family, String dimension, boolean hostile,
                   float maxHealth, float movementSpeed, float attackDamage,
                   float attackKnockback, float followRange, float armour,
                   float scale, boolean fireImmune, boolean canBreatheUnderwater,
                   String renderLayer, float shadowRadius,
                   int textureWidth, int textureHeight,
                   String[] goals, String[] targetClasses,
                   String spawnCategory, int spawnWeight,
                   int spawnGroupMin, int spawnGroupMax, int experience,
                   String[] animations, float modelWidth, float modelHeight) {
        this.id = id;
        this.family = family;
        this.dimension = dimension;
        this.hostile = hostile;
        this.maxHealth = maxHealth;
        this.movementSpeed = movementSpeed;
        this.attackDamage = attackDamage;
        this.attackKnockback = attackKnockback;
        this.followRange = followRange;
        this.armour = armour;
        this.scale = scale;
        this.fireImmune = fireImmune;
        this.canBreatheUnderwater = canBreatheUnderwater;
        this.renderLayer = renderLayer;
        this.shadowRadius = shadowRadius;
        this.textureWidth = textureWidth;
        this.textureHeight = textureHeight;
        this.goals = goals;
        this.targetClasses = targetClasses;
        this.spawnCategory = spawnCategory;
        this.spawnWeight = spawnWeight;
        this.spawnGroupMin = spawnGroupMin;
        this.spawnGroupMax = spawnGroupMax;
        this.experience = experience;
        this.animations = animations;
        this.modelWidth = modelWidth;
        this.modelHeight = modelHeight;
    }
}
