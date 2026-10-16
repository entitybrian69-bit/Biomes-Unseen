package com.biomesunseen.registry;

/**
 * Tag id strings for the pre-TagKey Minecraft lines.  Data generation writes
 * the same tag JSON documents; runtime code can resolve ids through these
 * constants.
 */
public final class ModTags {

    public static final String ORES = "c:ores";
    public static final String ORES_IN_GROUND_STONE = "c:ores_in_ground/stone";
    public static final String ORES_IN_GROUND_DEEPSLATE = "c:ores_in_ground/deepslate";
    public static final String STONES = "c:stones";
    public static final String WOODS = "c:woods";
    public static final String PLANTS = "c:plants";
    public static final String UNSEEN_ORES = "biomesunseen:ores";
    public static final String UNSEEN_TERRAIN = "biomesunseen:terrain";
    public static final String UNSEEN_PLANTS = "biomesunseen:plants";
    public static final String UNSEEN_MOBS = "biomesunseen:mobs";
    public static final String UNSEEN_BOSSES = "biomesunseen:bosses";
    public static final String TAMEABLE = "biomesunseen:tameable";
    public static final String PACK_MOBS = "biomesunseen:pack_mobs";

    private ModTags() {
    }
}
