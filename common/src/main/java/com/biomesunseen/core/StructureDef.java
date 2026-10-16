package com.biomesunseen.core;

/**
 * Complete definition of one jigsaw structure: spacing, spawn biomes, boss
 * linkage and lore theme.
 */
public final class StructureDef {

    public final String id;
    public final String displayName;
    public final String group;
    /** ruin | tower | temple | fortress | tomb | shrine | dungeon | portal |
     *  forge | house | camp | palace | pyramid | boss_arena */
    public final String category;
    public final int spacing;
    public final int separation;
    public final double rarity;
    public final int maxDistanceFromCenter;
    public final boolean hasBoss;
    public final String bossId;
    public final String startPool;
    public final String[] biomeGroups;
    public final int lootTier;
    public final String loreTheme;

    public StructureDef(String id, String displayName, String group, String category,
                        int spacing, int separation, double rarity,
                        int maxDistanceFromCenter, boolean hasBoss, String bossId,
                        String startPool, String[] biomeGroups, int lootTier,
                        String loreTheme) {
        this.id = id;
        this.displayName = displayName;
        this.group = group;
        this.category = category;
        this.spacing = spacing;
        this.separation = separation;
        this.rarity = rarity;
        this.maxDistanceFromCenter = maxDistanceFromCenter;
        this.hasBoss = hasBoss;
        this.bossId = bossId;
        this.startPool = startPool;
        this.biomeGroups = biomeGroups;
        this.lootTier = lootTier;
        this.loreTheme = loreTheme;
    }

    public String key() {
        return ModConstants.NAMESPACE + id;
    }

    public int effectiveSpacing(double multiplier) {
        double v = spacing * multiplier;
        if (v < 1.0) {
            v = 1.0;
        }
        return (int) Math.round(v);
    }

    public int effectiveSeparation(double multiplier) {
        int sp = effectiveSpacing(multiplier);
        int sep = (int) Math.round(separation * multiplier);
        return sep >= sp ? sp - 1 : sep;
    }

    public boolean spawnsInGroup(String biomeGroup) {
        for (int i = 0; i < biomeGroups.length; i++) {
            if (biomeGroups[i].equals(biomeGroup)) {
                return true;
            }
        }
        return false;
    }
}
