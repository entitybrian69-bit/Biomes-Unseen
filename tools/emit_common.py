# -*- coding: utf-8 -*-
"""Emits common/src/main/java - pure-Java core compiled into every module.

These classes never touch Minecraft APIs so a single tree serves every target
from 1.16.5 (Java 8) through 26.3 (Java 25).  Java 8 syntax only.
"""

import os

from content import (BIOME_GROUPS, BIOME_ROWS, ORE_ROWS, DECOR_ROWS, PLANT_ROWS,
                     STRUCTURE_ROWS, MOB_ROWS, BOSS_ROWS, CONFIG_ROWS,
                     PARTICLE_TYPES, SOUND_EVENTS, ADVANCEMENT_ROWS, MOD_ID)


def _w(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


JAVA_CORE = "common/src/main/java/com/biomesunseen/core"


def _s(v):
    """Java string literal."""
    return '"%s"' % str(v).replace("\\", "\\\\").replace('"', '\\"')


def _f(v):
    return ("%g" % v) if isinstance(v, float) else str(v)


def emit(root):
    # ------------------------------------------------------------------ #
    _w(root, JAVA_CORE + "/ModConstants.java", '''package com.biomesunseen.core;

/**
 * Immutable mod metadata shared by every loader and Minecraft version.
 */
public final class ModConstants {

    public static final String MOD_ID = %(id)s;
    public static final String MOD_NAME = %(name)s;
    public static final String MOD_VERSION = %(version)s;
    public static final String MOD_DESCRIPTION = %(desc)s;
    public static final String MOD_LICENSE = %(license)s;
    public static final String MOD_AUTHORS = %(authors)s;

    /** Root resource namespace, e.g. "biomesunseen:crystal_spire_reach". */
    public static final String NAMESPACE = MOD_ID + ":";

    /** Config file name used by the JSON config store. */
    public static final String CONFIG_FILE = "biomesunseen.json";

    private ModConstants() {
    }
}
''' % {
        "id": _s("biomesunseen"),
        "name": _s("Biomes Unseen"),
        "version": _s("1.0.0"),
        "desc": _s("A massive world-generation, adventure, biome, structure, ore, mob and boss mod."),
        "license": _s("MIT"),
        "authors": _s("Biomes Unseen Team"),
    })

    # ------------------------------------------------------------------ #
    _w(root, JAVA_CORE + "/BiomeDef.java", '''package com.biomesunseen.core;

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
''')

    _w(root, JAVA_CORE + "/OreDef.java", '''package com.biomesunseen.core;

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
''')

    _w(root, JAVA_CORE + "/StructureDef.java", '''package com.biomesunseen.core;

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
''')

    _w(root, JAVA_CORE + "/MobDef.java", '''package com.biomesunseen.core;

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
''')

    _w(root, JAVA_CORE + "/BossDef.java", '''package com.biomesunseen.core;

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
''')

    _w(root, JAVA_CORE + "/PlantDef.java", '''package com.biomesunseen.core;

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
''')

    _w(root, JAVA_CORE + "/DecorDef.java", '''package com.biomesunseen.core;

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
''')

    # ------------------------------------------------------------------ #
    # Content.java - every content entry as real Java data
    # ------------------------------------------------------------------ #
    biome_lines = []
    for (bid, display, group, depth, scale, temp, downfall, rarity, weather) in BIOME_ROWS:
        g = BIOME_GROUPS[group]
        biome_lines.append(
            '        new BiomeDef(%s, %s, %s, 0x%06X, 0x%06X, 0x%06X, 0x%06X, 0x%06X, '
            '%s, %s, %s, %s, %s, %d, %s, %s, %s)'
            % (_s(bid), _s(display), _s(group), g["grass"], g["foliage"], g["water"],
               g["sky"], g["fog"], _f(temp), _f(downfall), _s(g["category"]),
               _f(depth), _f(scale), rarity, _s(weather),
               _s(g["ambient"]), _s(g["music"])))
    ore_lines = []
    for row in ORE_ROWS:
        (oid, display, color, pcolor, miny, maxy, vsize, vchunk, rarity, grp,
         stone, glow, tool, potion, tier) = row
        dur, lvl, spd, dmg, ench = tool
        ore_lines.append(
            '        new OreDef(%s, %s, 0x%06X, 0x%06X, %d, %d, %d, %d, %s, %s, %s, %s, '
            '%d, %d, %s, %s, %d, %s, %d)'
            % (_s(oid), _s(display), color, pcolor, miny, maxy, vsize, vchunk,
               _f(rarity), _s(grp) if grp else "null", _s(stone),
               "true" if glow else "false", dur, lvl, _f(spd), _f(dmg), ench,
               _s(potion), tier))
    decor_lines = []
    for (did, display, color, sound, material) in DECOR_ROWS:
        decor_lines.append(
            '        new DecorDef(%s, %s, 0x%06X, %s, %s)'
            % (_s(did), _s(display), color, _s(sound), _s(material)))
    plant_lines = []
    for (pid, display, color, height, pottable, flower) in PLANT_ROWS:
        plant_lines.append(
            '        new PlantDef(%s, %s, 0x%06X, %d, %s, %s)'
            % (_s(pid), _s(display), color, height,
               "true" if pottable else "false", "true" if flower else "false"))
    struct_lines = []
    for row in STRUCTURE_ROWS:
        (sid, display, grp, cat, spacing, sep, rarity, maxd, hasboss, bossid,
         pool, bg, tier, lore) = row
        struct_lines.append(
            '        new StructureDef(%s, %s, %s, %s, %d, %d, %s, %d, %s, %s, %s, '
            'new String[]{%s}, %d, %s)'
            % (_s(sid), _s(display), _s(grp), _s(cat), spacing, sep, _f(rarity),
               maxd, "true" if hasboss else "false",
               _s(bossid) if bossid else "null", _s(pool),
               ", ".join(_s(g) for g in bg), tier, _s(lore)))
    mob_lines = []
    for row in MOB_ROWS:
        (mid, display, cat, hp, spd, atk, defn, w, h, behaviors, tame, trade,
         pack, herd, flees, terrain, bg, weight, night, anims, color, glow) = row
        mob_lines.append(
            '        new MobDef(%s, %s, %s, %s, %s, %s, %s, %s, %s, '
            'new String[]{%s}, %s, %s, %s, %s, %s, %s, new String[]{%s}, %d, %s, '
            'new String[]{%s}, 0x%06X, %s)'
            % (_s(mid), _s(display), _s(cat), _f(hp), _f(spd), _f(atk), _f(defn),
               _f(w), _f(h), ", ".join(_s(b) for b in behaviors),
               "true" if tame else "false", "true" if trade else "false",
               "true" if pack else "false", "true" if herd else "false",
               "true" if flees else "false", "true" if terrain else "false",
               ", ".join(_s(g) for g in bg), weight,
               "true" if night else "false", ", ".join(_s(an) for an in anims),
               color, "true" if glow else "false"))
    boss_lines = []
    for row in BOSS_ROWS:
        (bid, display, hp, spd, atk, w, h, arena, music, phases, attacks, loot,
         grp, color, glow) = row
        boss_lines.append(
            '        new BossDef(%s, %s, %s, %s, %s, %s, %s, %s, %s, '
            'new String[]{%s}, new String[]{%s}, %s, %s, 0x%06X, %s)'
            % (_s(bid), _s(display), _f(hp), _f(spd), _f(atk), _f(w), _f(h),
               _s(arena), _s(music), ", ".join(_s(p) for p in phases),
               ", ".join(_s(a) for a in attacks), _s(loot), _s(grp), color,
               "true" if glow else "false"))

    content_java = '''package com.biomesunseen.core;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The complete Biomes Unseen content catalog: 80 biomes, 20 ores, 12 palette
 * blocks, 10 plants, 30 structures, 25 mobs and 2 bosses.  Pure Java so every
 * version family can read the exact same definitions.
 */
public final class Content {

    public static final List<BiomeDef> BIOMES = Collections.unmodifiableList(Arrays.asList(new BiomeDef[]{
%(biomes)s
    }));

    public static final List<OreDef> ORES = Collections.unmodifiableList(Arrays.asList(new OreDef[]{
%(ores)s
    }));

    public static final List<DecorDef> DECOR = Collections.unmodifiableList(Arrays.asList(new DecorDef[]{
%(decor)s
    }));

    public static final List<PlantDef> PLANTS = Collections.unmodifiableList(Arrays.asList(new PlantDef[]{
%(plants)s
    }));

    public static final List<StructureDef> STRUCTURES = Collections.unmodifiableList(Arrays.asList(new StructureDef[]{
%(structures)s
    }));

    public static final List<MobDef> MOBS = Collections.unmodifiableList(Arrays.asList(new MobDef[]{
%(mobs)s
    }));

    public static final List<BossDef> BOSSES = Collections.unmodifiableList(Arrays.asList(new BossDef[]{
%(bosses)s
    }));

    private static final Map<String, BiomeDef> BIOME_BY_ID = indexBiomes();
    private static final Map<String, OreDef> ORE_BY_ID = indexOres();
    private static final Map<String, MobDef> MOB_BY_ID = indexMobs();
    private static final Map<String, BossDef> BOSS_BY_ID = indexBosses();
    private static final Map<String, StructureDef> STRUCTURE_BY_ID = indexStructures();

    private Content() {
    }

    private static Map<String, BiomeDef> indexBiomes() {
        Map<String, BiomeDef> map = new LinkedHashMap<String, BiomeDef>();
        for (int i = 0; i < BIOMES.size(); i++) {
            BiomeDef def = BIOMES.get(i);
            map.put(def.id, def);
        }
        return Collections.unmodifiableMap(map);
    }

    private static Map<String, OreDef> indexOres() {
        Map<String, OreDef> map = new LinkedHashMap<String, OreDef>();
        for (int i = 0; i < ORES.size(); i++) {
            OreDef def = ORES.get(i);
            map.put(def.id, def);
        }
        return Collections.unmodifiableMap(map);
    }

    private static Map<String, MobDef> indexMobs() {
        Map<String, MobDef> map = new LinkedHashMap<String, MobDef>();
        for (int i = 0; i < MOBS.size(); i++) {
            MobDef def = MOBS.get(i);
            map.put(def.id, def);
        }
        return Collections.unmodifiableMap(map);
    }

    private static Map<String, BossDef> indexBosses() {
        Map<String, BossDef> map = new LinkedHashMap<String, BossDef>();
        for (int i = 0; i < BOSSES.size(); i++) {
            BossDef def = BOSSES.get(i);
            map.put(def.id, def);
        }
        return Collections.unmodifiableMap(map);
    }

    private static Map<String, StructureDef> indexStructures() {
        Map<String, StructureDef> map = new LinkedHashMap<String, StructureDef>();
        for (int i = 0; i < STRUCTURES.size(); i++) {
            StructureDef def = STRUCTURES.get(i);
            map.put(def.id, def);
        }
        return Collections.unmodifiableMap(map);
    }

    public static BiomeDef biome(String id) {
        return BIOME_BY_ID.get(id);
    }

    public static OreDef ore(String id) {
        return ORE_BY_ID.get(id);
    }

    public static MobDef mob(String id) {
        return MOB_BY_ID.get(id);
    }

    public static BossDef boss(String id) {
        return BOSS_BY_ID.get(id);
    }

    public static StructureDef structure(String id) {
        return STRUCTURE_BY_ID.get(id);
    }

    /** Biome ids belonging to a group, in catalog order. */
    public static List<String> biomeIdsInGroup(String group) {
        List<String> out = new ArrayList<String>();
        for (int i = 0; i < BIOMES.size(); i++) {
            BiomeDef def = BIOMES.get(i);
            if (def.group.equals(group)) {
                out.add(def.id);
            }
        }
        return out;
    }

    /** Ore ids, in catalog order. */
    public static List<String> allOreIds() {
        List<String> out = new ArrayList<String>();
        for (int i = 0; i < ORES.size(); i++) {
            out.add(ORES.get(i).id);
        }
        return out;
    }

    /** Mob ids, in catalog order. */
    public static List<String> allMobIds() {
        List<String> out = new ArrayList<String>();
        for (int i = 0; i < MOBS.size(); i++) {
            out.add(MOBS.get(i).id);
        }
        return out;
    }

    /** Structure ids, in catalog order. */
    public static List<String> allStructureIds() {
        List<String> out = new ArrayList<String>();
        for (int i = 0; i < STRUCTURES.size(); i++) {
            out.add(STRUCTURES.get(i).id);
        }
        return out;
    }

    /** Biome ids, in catalog order. */
    public static List<String> allBiomeIds() {
        List<String> out = new ArrayList<String>();
        for (int i = 0; i < BIOMES.size(); i++) {
            out.add(BIOMES.get(i).id);
        }
        return out;
    }

    /** Stable pseudo-random 0..255 noise used by texture/particle jitter. */
    public static int stableHash(String key) {
        int h = 0;
        for (int i = 0; i < key.length(); i++) {
            h = 31 * h + key.charAt(i);
        }
        return (h ^ (h >>> 16)) & 0xFF;
    }
}
''' % {
        "biomes": ",\n".join(biome_lines),
        "ores": ",\n".join(ore_lines),
        "decor": ",\n".join(decor_lines),
        "plants": ",\n".join(plant_lines),
        "structures": ",\n".join(struct_lines),
        "mobs": ",\n".join(mob_lines),
        "bosses": ",\n".join(boss_lines),
    }
    _w(root, JAVA_CORE + "/Content.java", content_java)

    # ------------------------------------------------------------------ #
    config_fields = []
    config_parses = []
    config_defaults = []
    for (key, typ, default, comment) in CONFIG_ROWS:
        if typ == "double":
            jtype = "double"
            parse = "Double.parseDouble(value)"
            lit = default
        elif typ == "int":
            jtype = "int"
            parse = "Integer.parseInt(value)"
            lit = default
        else:
            jtype = "boolean"
            parse = "Boolean.parseBoolean(value)"
            lit = default
        config_fields.append(
            "    /** %s */\n    public %s %s = %s;" % (comment, jtype, key, lit))
        config_parses.append(
            '            if (key.equals(%s)) {\n'
            '                %s = %s;\n'
            '            }' % (_s(key), key, parse))
        config_defaults.append('        map.put(%s, String.valueOf(%s));' % (_s(key), key))

    _w(root, JAVA_CORE + "/ConfigKeys.java", '''package com.biomesunseen.core;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Configuration model shared by every platform.  Backed by JSON
 * (config/biomesunseen.json) and editable through Cloth Config.  Defaults
 * enable all content so the world generates full of life out of the box.
 */
public final class ConfigKeys {

%(fields)s

    /** Serialise every field to a stable key/value map. */
    public Map<String, String> toMap() {
        Map<String, String> map = new LinkedHashMap<String, String>();
%(defaults)s
        return map;
    }

    /** Apply values from a key/value map; unknown keys are ignored. */
    public void apply(Map<String, String> values) {
        for (Map.Entry<String, String> entry : values.entrySet()) {
            String key = entry.getKey();
            String value = entry.getValue();
            try {
%(parses)s
            } catch (NumberFormatException ignored) {
                // Keep the previous value when a config entry is malformed.
            }
        }
    }

    /** Fresh instance with stock defaults. */
    public static ConfigKeys defaults() {
        return new ConfigKeys();
    }
}
''' % {
        "fields": "\n\n".join(config_fields),
        "defaults": "\n".join(config_defaults),
        "parses": "\n".join(config_parses),
    })

    # ------------------------------------------------------------------ #
    _w(root, JAVA_CORE + "/ColorUtil.java", '''package com.biomesunseen.core;

/**
 * Integer color helpers used by particles, spawn eggs and biome tinting.
 */
public final class ColorUtil {

    private ColorUtil() {
    }

    public static int red(int color) {
        return (color >> 16) & 0xFF;
    }

    public static int green(int color) {
        return (color >> 8) & 0xFF;
    }

    public static int blue(int color) {
        return color & 0xFF;
    }

    /** Pack r/g/b (0..255) into a 0xRRGGBB int. */
    public static int rgb(int r, int g, int b) {
        return ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF);
    }

    /** Scale a colour toward white (factor > 1) or black (factor < 1). */
    public static int shade(int color, double factor) {
        int r = clamp((int) (red(color) * factor));
        int g = clamp((int) (green(color) * factor));
        int b = clamp((int) (blue(color) * factor));
        return rgb(r, g, b);
    }

    /** Linearly interpolate two packed colours; t in [0,1]. */
    public static int lerp(int a, int b, double t) {
        int r = (int) (red(a) + (red(b) - red(a)) * t);
        int g = (int) (green(a) + (green(b) - green(a)) * t);
        int bl = (int) (blue(a) + (blue(b) - blue(a)) * t);
        return rgb(r, g, bl);
    }

    /** Stable hue jitter derived from a string key, in [0,1). */
    public static double jitter(String key) {
        return Content.stableHash(key) / 255.0;
    }

    private static int clamp(int v) {
        return v < 0 ? 0 : (v > 255 ? 255 : v);
    }
}
''')

    _w(root, JAVA_CORE + "/MathUtil.java", '''package com.biomesunseen.core;

/**
 * Small numeric helpers shared by worldgen and entity AI code.
 */
public final class MathUtil {

    private MathUtil() {
    }

    public static double clamp(double v, double min, double max) {
        return v < min ? min : (v > max ? max : v);
    }

    public static int clamp(int v, int min, int max) {
        return v < min ? min : (v > max ? max : v);
    }

    /** Smoothstep in [0,1] for a value in [edge0, edge1]. */
    public static double smoothstep(double edge0, double edge1, double x) {
        double t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0);
        return t * t * (3.0 - 2.0 * t);
    }

    /** Deterministic 2D value noise in [0,1] (cached-free, cheap). */
    public static double valueNoise2d(int x, int y, int seed) {
        int n = x * 374761393 + y * 668265263 + seed * 1274126177;
        n = (n ^ (n >> 13)) * 1274126177;
        n = n ^ (n >> 16);
        return ((n & 0x7FFFFFFF) / (double) 0x7FFFFFFF);
    }

    /** Weighted pick using cumulative weights; indexWeights must be non-empty. */
    public static int weightedPick(double[] cumulativeWeights, double roll) {
        for (int i = 0; i < cumulativeWeights.length; i++) {
            if (roll <= cumulativeWeights[i]) {
                return i;
            }
        }
        return cumulativeWeights.length - 1;
    }
}
''')

    # ------------------------------------------------------------------ #
    # Core registries of static metadata used by datagen and platforms.
    # ------------------------------------------------------------------ #
    particle_list = ",\n".join("            %s" % _s(p) for p in PARTICLE_TYPES)
    sound_list = ",\n".join("            %s" % _s(s) for s in SOUND_EVENTS)
    _w(root, JAVA_CORE + "/CoreRegistries.java", '''package com.biomesunseen.core;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * Static id tables for particles, sound events and advancements.  The
 * platform registries and datagen providers consume these so ids never drift.
 */
public final class CoreRegistries {

    /** Particle type ids (without namespace). */
    public static final List<String> PARTICLE_IDS = Collections.unmodifiableList(Arrays.asList(new String[]{
%(particles)s
    }));

    /** Sound event ids (full "event.path" form used by sounds.json). */
    public static final List<String> SOUND_EVENT_IDS = Collections.unmodifiableList(Arrays.asList(new String[]{
%(sounds)s
    }));

    /** Advancement ids in unlock order. */
    public static final List<String> ADVANCEMENT_IDS = Collections.unmodifiableList(Arrays.asList(new String[]{
%(advancements)s
    }));

    private CoreRegistries() {
    }

    public static String particleKey(String id) {
        return ModConstants.NAMESPACE + id;
    }
}
''' % {
        "particles": particle_list,
        "sounds": sound_list,
        "advancements": ",\n".join(
            "            %s" % _s(a[0]) for a in ADVANCEMENT_ROWS),
    })
