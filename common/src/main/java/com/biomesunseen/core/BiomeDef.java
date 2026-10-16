package com.biomesunseen.core;

/**
 * Complete definition of one custom biome.  Pure data: the worldgen layer of
 * each Minecraft-version family turns these into real biome registries.
 */
public final class BiomeDef {

    public final String id;
    public final String displayName;
    public final String group;
    public final int grassColor;
    public final int foliageColor;
    public final int waterColor;
    public final int skyColor;
    public final int fogColor;
    public final double temperature;
    public final double downfall;
    public final String category;
    public final double depth;
    public final double scale;
    public final int rarity;
    public final String weather;
    public final String ambientSound;
    public final String music;

    public BiomeDef(String id, String displayName, String group,
                    int grassColor, int foliageColor, int waterColor,
                    int skyColor, int fogColor,
                    double temperature, double downfall, String category,
                    double depth, double scale, int rarity, String weather,
                    String ambientSound, String music) {
        this.id = id;
        this.displayName = displayName;
        this.group = group;
        this.grassColor = grassColor;
        this.foliageColor = foliageColor;
        this.waterColor = waterColor;
        this.skyColor = skyColor;
        this.fogColor = fogColor;
        this.temperature = temperature;
        this.downfall = downfall;
        this.category = category;
        this.depth = depth;
        this.scale = scale;
        this.rarity = rarity;
        this.weather = weather;
        this.ambientSound = ambientSound;
        this.music = music;
    }

    /** Registry id, e.g. "biomesunseen:crystal_spire_reach". */
    public String key() {
        return ModConstants.NAMESPACE + id;
    }

    /** True when this biome group should generate in the given climate band. */
    public boolean matchesTemperatureBand(double minInclusive, double maxExclusive) {
        return temperature >= minInclusive && temperature < maxExclusive;
    }

    /** Effective rarity after the user-configurable multiplier is applied. */
    public double effectiveRarity(double multiplier) {
        double v = rarity * multiplier;
        return v < 0.0 ? 0.0 : v;
    }
}
