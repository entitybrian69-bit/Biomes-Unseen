package com.biomesunseen.core;

/**
 * Complete definition of one decorative plant block.
 */
public final class PlantDef {

    public final String id;
    public final String displayName;
    public final int color;
    public final int height;
    public final boolean pottable;
    public final boolean flower;

    public PlantDef(String id, String displayName, int color, int height,
                    boolean pottable, boolean flower) {
        this.id = id;
        this.displayName = displayName;
        this.color = color;
        this.height = height;
        this.pottable = pottable;
        this.flower = flower;
    }

    public String key() {
        return ModConstants.NAMESPACE + id;
    }
}
