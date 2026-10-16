package com.biomesunseen.core;

/**
 * Complete definition of one custom mob: stats, behaviour flags, spawn
 * parameters and animation list.
 */
public final class MobDef {

    public final String id;
    public final String displayName;
    /** creature | monster */
    public final String category;
    public final double maxHealth;
    public final double movementSpeed;
    public final double attackDamage;
    public final double armor;
    public final double width;
    public final double height;
    public final String[] behaviors;
    public final boolean tameable;
    public final boolean tradable;
    public final boolean pack;
    public final boolean herd;
    public final boolean flees;
    public final boolean terrainUse;
    public final String[] biomeGroups;
    public final int spawnWeight;
    public final boolean nightOnly;
    public final String[] animations;
    public final int baseColor;
    public final boolean glow;

    public MobDef(String id, String displayName, String category,
                  double maxHealth, double movementSpeed, double attackDamage,
                  double armor, double width, double height, String[] behaviors,
                  boolean tameable, boolean tradable, boolean pack, boolean herd,
                  boolean flees, boolean terrainUse, String[] biomeGroups,
                  int spawnWeight, boolean nightOnly, String[] animations,
                  int baseColor, boolean glow) {
        this.id = id;
        this.displayName = displayName;
        this.category = category;
        this.maxHealth = maxHealth;
        this.movementSpeed = movementSpeed;
        this.attackDamage = attackDamage;
        this.armor = armor;
        this.width = width;
        this.height = height;
        this.behaviors = behaviors;
        this.tameable = tameable;
        this.tradable = tradable;
        this.pack = pack;
        this.herd = herd;
        this.flees = flees;
        this.terrainUse = terrainUse;
        this.biomeGroups = biomeGroups;
        this.spawnWeight = spawnWeight;
        this.nightOnly = nightOnly;
        this.animations = animations;
        this.baseColor = baseColor;
        this.glow = glow;
    }

    public String key() {
        return ModConstants.NAMESPACE + id;
    }

    public boolean hasBehavior(String behavior) {
        for (int i = 0; i < behaviors.length; i++) {
            if (behaviors[i].equals(behavior)) {
                return true;
            }
        }
        return false;
    }

    public int effectiveSpawnWeight(double multiplier) {
        double v = spawnWeight * multiplier;
        if (v < 0.0) {
            v = 0.0;
        }
        return (int) Math.round(v);
    }
}
