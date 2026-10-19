package com.biomesunseen.entity;

/**
 * Immutable definition of one boss, including its full phase machine.
 *
 * Instances are generated into {@code BUContent.BOSSES} from
 * {@code tools/content/bosses.py}.
 */
public final class BossData {

    /**
     * One stage of the fight.
     *
     * {@code healthThreshold} is the fraction of max health at which the phase
     * ENDS, so phases are ordered descending and the fight advances when the
     * boss drops below each threshold.
     */
    public static final class PhaseData {

        public final int index;
        public final String name;
        public final float healthThreshold;
        public final String entryAnimation;
        public final String[] abilities;
        public final String[] extraGoals;
        public final boolean invulnerableOnEntry;
        public final int invulnerableTicks;

        public PhaseData(int index, String name, float healthThreshold,
                         String entryAnimation, String[] abilities,
                         String[] extraGoals, boolean invulnerableOnEntry,
                         int invulnerableTicks) {
            this.index = index;
            this.name = name;
            this.healthThreshold = healthThreshold;
            this.entryAnimation = entryAnimation;
            this.abilities = abilities;
            this.extraGoals = extraGoals;
            this.invulnerableOnEntry = invulnerableOnEntry;
            this.invulnerableTicks = invulnerableTicks;
        }
    }

    public final String id;
    public final String name;
    public final String dimension;
    public final String music;
    public final String bossBarColor;
    public final String bossBarOverlay;
    public final float scale;
    public final int textureSize;
    public final int textureHeight;
    public final String spawnItem;
    public final String lootTable;
    public final String arenaStructure;
    public final PhaseData[] phases;

    public BossData(String id, String name, String dimension, String music,
                    String bossBarColor, String bossBarOverlay, float scale,
                    int textureSize, int textureHeight, String spawnItem,
                    String lootTable, String arenaStructure, PhaseData[] phases) {
        this.id = id;
        this.name = name;
        this.dimension = dimension;
        this.music = music;
        this.bossBarColor = bossBarColor;
        this.bossBarOverlay = bossBarOverlay;
        this.scale = scale;
        this.textureSize = textureSize;
        this.textureHeight = textureHeight;
        this.spawnItem = spawnItem;
        this.lootTable = lootTable;
        this.arenaStructure = arenaStructure;
        this.phases = phases;
    }

    /** The phase that should be active at a given health fraction. */
    public PhaseData phaseFor(float healthFraction) {
        PhaseData current = phases[0];
        for (PhaseData phase : phases) {
            if (healthFraction <= phase.healthThreshold) {
                current = phase;
            }
        }
        return current;
    }
}
