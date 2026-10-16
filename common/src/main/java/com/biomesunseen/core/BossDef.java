package com.biomesunseen.core;

/**
 * Complete definition of one multi-phase boss encounter.
 */
public final class BossDef {

    public final String id;
    public final String displayName;
    public final double maxHealth;
    public final double movementSpeed;
    public final double attackDamage;
    public final double width;
    public final double height;
    public final String arenaStructureId;
    public final String musicSoundEvent;
    public final String[] phases;
    public final String[] attacks;
    public final String lootTablePath;
    public final String biomeGroup;
    public final int color;
    public final boolean glow;

    public BossDef(String id, String displayName, double maxHealth,
                   double movementSpeed, double attackDamage, double width,
                   double height, String arenaStructureId, String musicSoundEvent,
                   String[] phases, String[] attacks, String lootTablePath,
                   String biomeGroup, int color, boolean glow) {
        this.id = id;
        this.displayName = displayName;
        this.maxHealth = maxHealth;
        this.movementSpeed = movementSpeed;
        this.attackDamage = attackDamage;
        this.width = width;
        this.height = height;
        this.arenaStructureId = arenaStructureId;
        this.musicSoundEvent = musicSoundEvent;
        this.phases = phases;
        this.attacks = attacks;
        this.lootTablePath = lootTablePath;
        this.biomeGroup = biomeGroup;
        this.color = color;
        this.glow = glow;
    }

    public String key() {
        return ModConstants.NAMESPACE + id;
    }

    /** Phase index for a given health fraction in [0,1]. */
    public int phaseForHealthFraction(float fraction) {
        int n = phases.length;
        if (fraction > 0.75F) {
            return 0;
        }
        if (fraction > 0.5F) {
            return Math.min(1, n - 1);
        }
        if (fraction > 0.25F) {
            return Math.min(2, n - 1);
        }
        return n - 1;
    }

    /** Attack damage scaled by phase so later phases hit harder. */
    public double phaseAttackDamage(int phase) {
        double factor = 1.0 + 0.25 * phase;
        return attackDamage * factor;
    }
}
