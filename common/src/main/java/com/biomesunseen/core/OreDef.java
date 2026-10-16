package com.biomesunseen.core;

/**
 * Complete definition of one custom ore: texture colors, generation window,
 * tool material statistics and gameplay hooks.
 */
public final class OreDef {

    public final String id;
    public final String displayName;
    public final int color;
    public final int particleColor;
    public final int minY;
    public final int maxY;
    public final int veinSize;
    public final int veinsPerChunk;
    public final double rarity;
    /** biome group id or null for "any biome" */
    public final String biomeGroup;
    /** "stone" or "deepslate" */
    public final String stoneTag;
    public final boolean glows;
    public final int toolDurability;
    public final int toolMiningLevel;
    public final double toolSpeed;
    public final double toolAttackDamage;
    public final int toolEnchantability;
    /** vanilla potion effect name applied by derived gear */
    public final String potionEffect;
    /** machine tier 1..4 */
    public final int machineTier;

    public OreDef(String id, String displayName, int color, int particleColor,
                  int minY, int maxY, int veinSize, int veinsPerChunk,
                  double rarity, String biomeGroup, String stoneTag, boolean glows,
                  int toolDurability, int toolMiningLevel, double toolSpeed,
                  double toolAttackDamage, int toolEnchantability,
                  String potionEffect, int machineTier) {
        this.id = id;
        this.displayName = displayName;
        this.color = color;
        this.particleColor = particleColor;
        this.minY = minY;
        this.maxY = maxY;
        this.veinSize = veinSize;
        this.veinsPerChunk = veinsPerChunk;
        this.rarity = rarity;
        this.biomeGroup = biomeGroup;
        this.stoneTag = stoneTag;
        this.glows = glows;
        this.toolDurability = toolDurability;
        this.toolMiningLevel = toolMiningLevel;
        this.toolSpeed = toolSpeed;
        this.toolAttackDamage = toolAttackDamage;
        this.toolEnchantability = toolEnchantability;
        this.potionEffect = potionEffect;
        this.machineTier = machineTier;
    }

    public String key() {
        return ModConstants.NAMESPACE + id;
    }

    public int effectiveVeinsPerChunk(double multiplier) {
        double v = veinsPerChunk * multiplier;
        if (v < 0.0) {
            v = 0.0;
        }
        return (int) Math.round(v);
    }

    /** Rough ore value used by recipe balancing and villager trades. */
    public int valueScore() {
        return toolMiningLevel * 32 + (int) (toolDurability / 8.0) + machineTier * 16;
    }
}
