package com.biomesunseen.core;

/**
 * Complete definition of one decorative / palette block.
 */
public final class DecorDef {

    public final String id;
    public final String displayName;
    public final int color;
    /** glass | basalt | grass | stone | mud | wood | fungus */
    public final String sound;
    /** crystal | stone | soil | ice | wood | plant */
    public final String material;

    public DecorDef(String id, String displayName, int color, String sound, String material) {
        this.id = id;
        this.displayName = displayName;
        this.color = color;
        this.sound = sound;
        this.material = material;
    }

    public String key() {
        return ModConstants.NAMESPACE + id;
    }

    public boolean isTransparent() {
        return "glass".equals(sound) || "crystal".equals(material);
    }

    public int lightLevel() {
        return "crystal".equals(material) ? 7 : ("plant".equals(material) ? 5 : 0);
    }
}
