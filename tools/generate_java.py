#!/usr/bin/env python3
"""
Biomes Unseen -- Java data table generator.

Emits src/main/java/com/biomesunseen/init/BUContent.java: the single source of
truth the Java registries loop over. Everything in it is derived from
tools/content/* and tools/registry.py, so the Java can never disagree with the
JSON resources or the textures about which ids exist.

Why generate rather than hand-write: 264 blocks, 285 items and 85 entities would
be thousands of lines of registration boilerplate that has to stay in sync with
the content tables by hand. A generated table plus a handful of hand-written
registration loops is both smaller and impossible to drift.

The emitted file is plain data -- no logic. All behaviour lives in the
hand-written classes that read it.
"""

from __future__ import annotations

import os
import sys
from typing import Dict, List, Optional, Sequence, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import content.biomes as BIOMES        # noqa: E402
import content.bosses as BOSSES        # noqa: E402
import content.gear as GEAR            # noqa: E402
import content.mobs as MOBS            # noqa: E402
import content.ores as ORES            # noqa: E402
import content.structures as STRUCTS   # noqa: E402
import registry as REG                 # noqa: E402

MODID = REG.MODID
R = REG.REGISTRY
OUT = os.path.join(ROOT, "src", "main", "java", "com", "biomesunseen", "init",
                   "BUContent.java")

PACKAGE = "com.biomesunseen.init"

TOOL_SET_BY_ID: Dict[str, object] = {t.id: t for t in GEAR.TOOL_SETS}
ARMOR_SET_BY_ID: Dict[str, object] = {a.id: a for a in GEAR.ARMOR_SETS}
MOB_BY_ID: Dict[str, object] = {m.id: m for m in MOBS.ALL_MOBS}
BOSS_BY_ID: Dict[str, object] = {b.id: b for b in BOSSES.ALL_BOSSES}

# Blocks that Forge models as a real flowing liquid rather than a solid cube.
FLUID_BLOCKS: Tuple[str, ...] = ("hollow_water", "lumen_water", "void_fluid",
                                 "aether_essence")

# Authored GeckoLib atlas dimensions. Every non-boss creature shares the 64x32
# family atlas layout; every boss uses its own 64x64 atlas. These must match
# tools/pixelart/creature_maps.py and boss_maps.py exactly or the UVs skew.
MOB_TEX_W = 64
# 64 rather than 32: the atlas grew a band so the tail has room of its own. At 32
# rows every band was spoken for and the tail was composed over the front-right
# and back-left limb cells, corrupting two legs to gain one tail.
MOB_TEX_H = 64
BOSS_TEX_W = 64
BOSS_TEX_H = 64


def q(s: str) -> str:
    """Java string literal."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def jarray(items: Sequence[str], indent: str = "            ",
           as_arg: bool = False) -> str:
    """
    Render a Java String array literal.

    A bare initialiser ("{\"a\", \"b\"}") is only legal in a declaration or
    assignment. Java rejects it as a method argument, so constructor calls must
    use the explicit "new String[] {...}" form -- hence `as_arg`.
    """
    prefix = "new String[] " if as_arg else ""
    if not items:
        return prefix + "{}"
    parts = [q(i) for i in items]
    # Pack several per line for readability without exploding the file.
    lines: List[str] = []
    cur: List[str] = []
    width = 0
    for p in parts:
        if width + len(p) + 2 > 100:
            lines.append(indent + ", ".join(cur) + ",")
            cur, width = [], 0
        cur.append(p)
        width += len(p) + 2
    if cur:
        lines.append(indent + ", ".join(cur))
    return prefix + "{\n" + "\n".join(lines) + "\n        }"


def string_array_decl(name: str, values: Sequence[str], comment: str) -> str:
    return (f"    /** {comment} */\n"
            f"    public static final String[] {name} = {jarray(values)};\n")


# --------------------------------------------------------------------------- #
#  Blocks
# --------------------------------------------------------------------------- #

def block_section() -> str:
    out: List[str] = []
    out.append("    // ------------------------------------------------------------------")
    out.append("    //  BLOCKS")
    out.append("    // ------------------------------------------------------------------")

    kinds: Dict[str, List[str]] = {}
    for block in R.blocks:
        if block in FLUID_BLOCKS:
            continue
        kinds.setdefault(R.block_kind(block), []).append(block)

    comments = {
        REG.BlockKind.CUBE_ALL: "Plain six-faced cubes: stone, loam, planks, ore hosts.",
        REG.BlockKind.GRASS: "Turf blocks: authored top over an authored side/substrate.",
        REG.BlockKind.LOG: "Pillars with a distinct end grain (axis-property blockstates).",
        REG.BlockKind.PORTAL: "Dimension gates: no collision, translucent, no item form.",
        REG.BlockKind.CROSS: "Flora: single cutout cross, no collision.",
        REG.BlockKind.LANTERN: "Emissive cubes that light their surroundings.",
        REG.BlockKind.ALTAR: "Pillar-shaped interactive block (boss summoning).",
        REG.BlockKind.ORE: "Ore blocks: Fortune-aware drop, Silk Touch alternative.",
        REG.BlockKind.MINERAL_BLOCK: "Compressed storage blocks (9x material recipe).",
    }
    order = [REG.BlockKind.CUBE_ALL, REG.BlockKind.GRASS, REG.BlockKind.LOG,
             REG.BlockKind.ORE, REG.BlockKind.MINERAL_BLOCK, REG.BlockKind.CROSS,
             REG.BlockKind.PORTAL, REG.BlockKind.LANTERN, REG.BlockKind.ALTAR]
    const_names = {
        REG.BlockKind.CUBE_ALL: "BLOCKS_CUBE",
        REG.BlockKind.GRASS: "BLOCKS_GRASS",
        REG.BlockKind.LOG: "BLOCKS_LOG",
        REG.BlockKind.ORE: "BLOCKS_ORE",
        REG.BlockKind.MINERAL_BLOCK: "BLOCKS_MINERAL",
        REG.BlockKind.CROSS: "BLOCKS_FLORA",
        REG.BlockKind.PORTAL: "BLOCKS_PORTAL",
        REG.BlockKind.LANTERN: "BLOCKS_LANTERN",
        REG.BlockKind.ALTAR: "BLOCKS_ALTAR",
    }
    for kind in order:
        values = sorted(kinds.get(kind, []))
        if not values:
            continue
        out.append(string_array_decl(const_names[kind], values, comments[kind]))
        out.append("")

    # Grass -> substrate, needed by the grass BlockBehaviour and its colour handler.
    out.append("    /** Grass block -> the substrate it shows underneath and drops. */")
    out.append("    public static final String[][] GRASS_SUBSTRATE = {")
    for block in sorted(kinds.get(REG.BlockKind.GRASS, [])):
        out.append(f"            {{ {q(block)}, {q(grass_substrate(block))} }},")
    out.append("    };")
    out.append("")

    # Log -> plank conversions drive the axe-stripping and crafting hooks.
    planks = sorted(b for b in R.blocks if b.endswith("_planks"))
    out.append("    /** Log block -> the planks it crafts into. */")
    out.append("    public static final String[][] LOG_TO_PLANKS = {")
    for log in sorted(kinds.get(REG.BlockKind.LOG, [])):
        base = log[:-4] if log.endswith("_log") else log
        target = f"{base}_planks"
        if target in set(planks):
            out.append(f"            {{ {q(log)}, {q(target)} }},")
    out.append("    };")
    out.append("")

    out.append("    /** Fluid blocks, registered with a real ForgeFlowingFluid. */")
    out.append(f"    public static final String[] BLOCKS_FLUID = {jarray(sorted(FLUID_BLOCKS))};")
    out.append("")
    return "\n".join(out)


def grass_substrate(block: str) -> str:
    for biome in BIOMES.ALL_BIOMES:
        top = biome.surface_top.split(":")[-1]
        fill = biome.surface_filler.split(":")[-1]
        if top == block and fill in R.block_set:
            return fill
    return block.replace("grass_block", "dirt")


# --------------------------------------------------------------------------- #
#  Items
# --------------------------------------------------------------------------- #

def refined_material(ore) -> Optional[str]:
    ts = TOOL_SET_BY_ID.get(ore.base_name)
    if ts and ts.repair_item.startswith(f"{MODID}:"):
        cand = ts.repair_item.split(":")[-1]
        if cand in R.item_set:
            return cand
    for suffix in ("_ingot", "_refined", "_gem"):
        cand = f"{ore.base_name}{suffix}"
        if cand in R.item_set:
            return cand
    return None


def item_section() -> str:
    out: List[str] = []
    out.append("    // ------------------------------------------------------------------")
    out.append("    //  ITEMS")
    out.append("    // ------------------------------------------------------------------")

    tool_items = set()
    for ts in GEAR.TOOL_SETS:
        for tool in ts.tools:
            tool_items.add(f"{ts.id}_{tool}")
        if ts.has_bow:
            tool_items.add(f"{ts.id}_bow")
        if ts.has_shield:
            tool_items.add(f"{ts.id}_shield")
    artefacts = set(GEAR.ARTEFACT_WEAPONS.values())

    armour_items = set()
    for aset in GEAR.ARMOR_SETS:
        for piece in aset.pieces:
            armour_items.add(f"{aset.id}_{piece}")

    eggs = {i for i in R.items if i.endswith("_spawn_egg")}
    lore_books = {i for i in R.items if i.startswith("lore_book")}
    block_items = set(R.blocks)

    accounted = (tool_items | artefacts | armour_items | eggs | lore_books
                 | block_items | set(FLUID_BLOCKS))
    plain = sorted(i for i in R.items if i not in accounted)

    out.append(string_array_decl("ITEMS_MATERIALS", plain,
                                 "Crafting materials: ore drops, refined ingots, mob drops, boss components."))
    out.append("")
    out.append(string_array_decl("ITEMS_TOOLS", sorted(tool_items),
                                 "Tools, bows and shields; the tier comes from GEAR_TIER via the set prefix."))
    out.append("")
    out.append(string_array_decl("ITEMS_ARTEFACTS", sorted(artefacts),
                                 "Boss artefact weapons, crafted from a boss core."))
    out.append("")
    out.append(string_array_decl("ITEMS_LORE_BOOKS", sorted(lore_books),
                                 "Written lore books; each opens a GUI page of authored text."))
    out.append("")

    # Armour needs its slot, so it is a table rather than a flat list.
    out.append("    /** Armour items as {itemId, setId, slot}. */")
    out.append("    public static final String[][] ARMOUR_ITEMS = {")
    for item in sorted(armour_items):
        set_id, _, piece = item.rpartition("_")
        out.append(f"            {{ {q(item)}, {q(set_id)}, {q(piece)} }},")
    out.append("    };")
    out.append("")

    out.append("    /** Spawn eggs as {itemId, entityId}; the texture is per-species. */")
    out.append("    public static final String[][] SPAWN_EGGS = {")
    for egg in sorted(eggs):
        ent = egg[: -len("_spawn_egg")]
        out.append(f"            {{ {q(egg)}, {q(ent)} }},")
    out.append("    };")
    out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------- #
#  Gear stat tables
# --------------------------------------------------------------------------- #

def gear_section() -> str:
    out: List[str] = []
    out.append("    // ------------------------------------------------------------------")
    out.append("    //  GEAR STATS")
    out.append("    // ------------------------------------------------------------------")

    out.append("    /**")
    out.append("     * Tool sets as {setId, tierLevel, uses, speed, attackDamageBonus,")
    out.append("     * enchantmentValue, repairItem}.")
    out.append("     *")
    out.append("     * tierLevel is the harvest level (1 stone .. 5 netherite-plus) and")
    out.append("     * drives both the Tier and the needs_x_tool tag the blocks use.")
    out.append("     */")
    out.append("    public static final Object[][] GEAR_TIER = {")
    for ts in GEAR.TOOL_SETS:
        repair = ts.repair_item.split(":")[-1] if ts.repair_item else ""
        out.append(
            f"            {{ {q(ts.id)}, {int(ts.tier)}, {int(ts.durability)}f, "
            f"{float(ts.speed)}f, {float(ts.attack_damage_bonus)}f, "
            f"{int(ts.enchantment_value)}, {q(repair)} }},"
        )
    out.append("    };")
    out.append("")

    out.append("    /**")
    out.append("     * Armour sets as {setId, durabilityMultiplier, boots, leggings,")
    out.append("     * chestplate, helmet, toughness, knockbackResistance, repairItem,")
    out.append("     * setBonus}.")
    out.append("     *")
    out.append("     * The four defence values are emitted in ArmorItem.Type ordinal order")
    out.append("     * (BOOTS, LEGGINGS, CHESTPLATE, HELMET), which is the order")
    out.append("     * BUArmorMaterial.getDefenseForType indexes them by. That matches")
    out.append("     * ArmorSetSpec.protection, authored boots-first, so the row is a direct")
    out.append("     * copy of the tuple with no reordering anywhere in the chain.")
    out.append("     */")
    out.append("    public static final Object[][] GEAR_ARMOUR = {")
    for aset in GEAR.ARMOR_SETS:
        prot = aset.protection
        repair = aset.repair_item.split(":")[-1] if aset.repair_item else ""
        # Authored boots-first, emitted boots-first. A dict is accepted for the
        # same four named slots so a future spec can spell them explicitly.
        if isinstance(prot, dict):
            ordered = [prot["boots"], prot["leggings"], prot["chestplate"], prot["helmet"]]
        else:
            ordered = list(prot)
        assert len(ordered) == 4, f"{aset.id}: protection must have four slots"
        out.append(
            f"            {{ {q(aset.id)}, {int(aset.durability_multiplier)}, "
            f"{int(ordered[0])}, {int(ordered[1])}, {int(ordered[2])}, {int(ordered[3])}, "
            f"{float(aset.toughness)}f, {float(aset.knockback_resistance)}f, "
            f"{q(repair)}, {q(aset.set_bonus)} }},"
        )
    out.append("    };")
    out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------- #
#  Entities
# --------------------------------------------------------------------------- #

def entity_section() -> str:
    out: List[str] = []
    out.append("    // ------------------------------------------------------------------")
    out.append("    //  ENTITIES")
    out.append("    // ------------------------------------------------------------------")

    out.append("    /**")
    out.append("     * The 80 non-boss creatures, as MobData records.")
    out.append("     *")
    out.append("     * Field order matches com.biomesunseen.entity.MobData exactly; the")
    out.append("     * goal tokens are resolved to real Goal instances by BUGoalFactory.")
    out.append("     */")
    out.append("    public static final MobData[] MOBS = {")
    for mob in MOBS.ALL_MOBS:
        out.append("            new MobData(")
        out.append(f"                    {q(mob.id)}, {q(mob.family)}, {q(mob.dimension)},")
        out.append(f"                    {str(bool(mob.hostile)).lower()}, "
                   f"{float(mob.max_health)}f, {float(mob.movement_speed)}f,")
        out.append(f"                    {float(mob.attack_damage)}f, "
                   f"{float(mob.attack_knockback)}f, {float(mob.follow_range)}f,")
        out.append(f"                    {float(mob.armour)}f, {float(mob.scale)}f,")
        out.append(f"                    {str(bool(mob.fire_immune)).lower()}, "
                   f"{str(bool(mob.can_breathe_underwater)).lower()}, "
                   f"{q(mob.render_layer)},")
        out.append(f"                    {float(mob.shadow_radius)}f, "
                   f"{MOB_TEX_W}, {MOB_TEX_H},")
        out.append(f"                    {jarray(list(mob.goals), ' ' * 20, as_arg=True)},")
        out.append(f"                    {jarray(list(mob.target_classes), ' ' * 20, as_arg=True)},")
        out.append(f"                    {q(mob.spawn_category)}, {int(mob.spawn_weight)}, "
                   f"{int(mob.spawn_group[0])}, {int(mob.spawn_group[1])},")
        out.append(f"                    {int(mob.experience)},")
        out.append(f"                    {jarray(list(mob.animations), ' ' * 20, as_arg=True)},")
        # The unscaled collision box. Kept separate from scale so the EntityType
        # can be sized with it and getDimensions can apply scale exactly once --
        # folding scale into both compounded it for the 50 species whose scale is
        # not 1.0.
        out.append(f"                    {float(mob.model_width)}f, {float(mob.model_height)}f")
        out.append("            ),")
    out.append("    };")
    out.append("")

    out.append("    /** The 5 bosses, as BossData records with their phase machines. */")
    out.append("    public static final BossData[] BOSSES = {")
    for boss in BOSSES.ALL_BOSSES:
        mob = boss.mob
        out.append("            new BossData(")
        out.append(f"                    {q(boss.id)}, {q(boss.name)}, {q(boss.dimension)},")
        out.append(f"                    {q(boss.music)}, {q(boss.boss_bar_color)},")
        out.append(f"                    {q(boss.boss_bar_overlay)}, {float(boss.scale)}f,")
        out.append(f"                    {int(boss.texture_size)}, {BOSS_TEX_H},")
        out.append(f"                    {q(boss.spawn_item)}, {q(boss.loot_table)},")
        out.append(f"                    {q(boss.arena_structure.split(':')[-1])},")
        out.append(f"                    new PhaseData[] {{")
        for ph in boss.phases:
            out.append("                        new PhaseData(")
            out.append(f"                                {int(ph.index)}, {q(ph.name)}, "
                       f"{float(ph.health_threshold)}f,")
            out.append(f"                                {q(ph.entry_animation)},")
            out.append(f"                                {jarray(list(ph.abilities), ' ' * 32, as_arg=True)},")
            out.append(f"                                {jarray(list(ph.extra_goals), ' ' * 32, as_arg=True)},")
            out.append(f"                                {str(bool(ph.invulnerable_on_entry)).lower()}, "
                       f"{int(ph.invulnerable_ticks)}")
            out.append("                        ),")
        out.append("                    },")
        # The unscaled collision box, exactly as for mobs: sized() takes these and
        # getDimensions applies scale once, so the two never compound.
        out.append(f"                    {float(boss.model_width)}f, {float(boss.model_height)}f")
        out.append("            ),")
    out.append("    };")
    out.append("")

    # Mob -> atlas dimensions, needed by the GeckoLib model lookup. Creature
    # atlases are 64x32; boss atlases are 64x64 (both authored layouts).
    out.append("    /** Entity id -> {textureWidth, textureHeight} in pixels. */")
    out.append("    public static final Object[][] ENTITY_TEXTURE_SIZE = {")
    for ent in R.entities:
        if ent in BOSS_BY_ID:
            size = int(BOSS_BY_ID[ent].texture_size)
            out.append(f"            {{ {q(ent)}, {size}, {size} }},")
        else:
            out.append(f"            {{ {q(ent)}, {MOB_TEX_W}, {MOB_TEX_H} }},")
    out.append("    };")
    out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------- #
#  Biomes, dimensions, sounds, particles
# --------------------------------------------------------------------------- #

def biome_section() -> str:
    out: List[str] = []
    out.append("    // ------------------------------------------------------------------")
    out.append("    //  BIOMES / DIMENSIONS / AMBIENCE")
    out.append("    // ------------------------------------------------------------------")

    dims = sorted({b.dimension for b in BIOMES.ALL_BIOMES})
    out.append(string_array_decl("DIMENSIONS", dims,
                                 "Every dimension the mod adds biomes to."))
    out.append("")

    out.append("    /** Biome ids per dimension, for the biome source parameter lists. */")
    out.append("    public static final String[][] DIMENSION_BIOMES = {")
    for dim in dims:
        ids = sorted(b.id for b in BIOMES.ALL_BIOMES if b.dimension == dim)
        out.append(f"            {{ {q(dim)},")
        out.append(f"              {q(','.join(ids))} }},")
    out.append("    };")
    out.append("")

    # Every Overworld biome, with the climate parameters TerraBlender needs to
    # place it. This used to be the 12 highest-weight biomes, on the assumption
    # that only a hand-picked slice could be spliced into the vanilla preset.
    # TerraBlender's region API blends a whole region against vanilla, so all 80
    # are now emitted and all 80 generate.
    seeded = sorted(b.id for b in BIOMES.ALL_BIOMES if b.dimension == "overworld")
    out.append("    /**")
    out.append("     * Every Overworld biome the mod adds.")
    out.append("     *")
    out.append("     * Bound to the TerraBlender Overworld region by BUOverworldRegion,")
    out.append("     * which blends their authored climate parameters against vanilla so")
    out.append("     * they generate in normal Overworld play without replacing any")
    out.append("     * vanilla biome.")
    out.append("     */")
    out.append(string_array_decl("SEEDED_OVERWORLD_BIOMES", seeded,
                                 "Placed by the TerraBlender Overworld region."))
    out.append("")

    # Noise parameters for all of them, straight from the authored table.
    out.append("    /**")
    out.append("     * Multi-noise parameters for SEEDED_OVERWORLD_BIOMES as")
    out.append("     * {biomeId, temperature, humidity, continentalness, erosion,")
    out.append("     * depth, weirdness, offset, weight}.")
    out.append("     */")
    out.append("    public static final Object[][] SEEDED_OVERWORLD_PARAMETERS = {")
    for bid in seeded:
        b = BIOMES.BY_ID[bid] if hasattr(BIOMES, "BY_ID") else next(
            x for x in BIOMES.ALL_BIOMES if x.id == bid)
        out.append(
            f"            {{ {q(bid)}, {float(b.temperature)}f, {float(b.humidity)}f, "
            f"{float(b.continentalness)}f, {float(b.erosion)}f, {float(b.depth)}f, "
            f"{float(b.weirdness)}f, {float(b.offset)}f, {int(b.weight)} }},"
        )
    out.append("    };")
    out.append("")

    # Surface materials for the Overworld biomes, as {biomeId, top, filler}.
    #
    # Our own dimensions carry surface rules in their noise_settings JSON, but
    # the Overworld's rules come from vanilla's noise settings, which a datapack
    # cannot extend per biome. TerraBlender's SurfaceRuleManager is the supported
    # hook, and it is Java-side, so the materials have to be available here.
    out.append("    /**")
    out.append("     * Surface materials for SEEDED_OVERWORLD_BIOMES as")
    out.append("     * {biomeId, surfaceTop, surfaceFiller}.")
    out.append("     *")
    out.append("     * Consumed by BUOverworldSurfaceRules, which registers biome-gated")
    out.append("     * surface rules through TerraBlender so each biome gets its authored")
    out.append("     * crust without those materials bleeding into vanilla biomes.")
    out.append("     */")
    out.append("    public static final Object[][] OVERWORLD_SURFACES = {")
    for bid in seeded:
        b = BIOMES.BY_ID[bid] if hasattr(BIOMES, "BY_ID") else next(
            x for x in BIOMES.ALL_BIOMES if x.id == bid)
        out.append(
            f"            {{ {q(bid)}, {q(b.surface_top)}, {q(b.surface_filler)} }},"
        )
    out.append("    };")
    out.append("")

    # Sounds: music tracks and ambience referenced by biomes.
    music = sorted({b.music.split(":")[-1] for b in BIOMES.ALL_BIOMES if b.music})
    ambient = sorted({b.ambient_sound.split(":")[-1]
                      for b in BIOMES.ALL_BIOMES if b.ambient_sound})
    boss_music = sorted({b.music.split(":")[-1] for b in BOSSES.ALL_BOSSES if b.music})
    sounds = sorted(set(music) | set(ambient) | set(boss_music))
    out.append(string_array_decl("SOUNDS", sounds,
                                 "Every SoundEvent the mod registers (music, ambience, boss themes)."))
    out.append("")

    # Which of those actually have audio behind them. A SoundEvent with no
    # sounds.json definition logs "Unable to play unknown soundEvent" when
    # started, so playback is gated on this list rather than on registration:
    # registering an id is harmless, playing an undefined one is not. Adding a
    # track is a data change -- drop the .ogg in and re-run the generators -- and
    # every caller switches on with no Java edit.
    with_audio = sorted(
        sid for sid in sounds
        if os.path.exists(os.path.join(
            ROOT, "src", "main", "resources", "assets", MODID,
            "sounds", sid.replace(".", os.sep) + ".ogg"))
    )
    out.append(string_array_decl("SOUNDS_WITH_AUDIO", with_audio,
                                 "Subset of SOUNDS that ship real audio; playback is gated on this."))
    out.append("")

    particles = sorted({b.particle.split(":")[-1] for b in BIOMES.ALL_BIOMES if b.particle})
    out.append(string_array_decl("PARTICLES", particles,
                                 "Ambient biome particle types."))
    out.append("")

    # Ores: id, dimension, host stone, y-range, vein size, count, experience.
    out.append("    /**")
    out.append("     * Ore generation parameters as {oreBlock, hostStone, minY, maxY,")
    out.append("     * veinSize, veinsPerChunk, dimension, experience}.")
    out.append("     */")
    out.append("    public static final Object[][] ORE_GEN = {")
    for ore in ORES.ALL_ORES:
        exp = ore.experience
        exp_lo = int(exp[0]) if isinstance(exp, (tuple, list)) else int(exp or 0)
        out.append(
            f"            {{ {q(ore.ore_block)}, {q(ore.host_stone)}, {int(ore.min_y)}, "
            f"{int(ore.max_y)}, {int(ore.vein_size)}, {int(ore.veins_per_chunk)}, "
            f"{q(ore.dimension)}, {exp_lo} }},"
        )
        if ore.deepslate_ore_block:
            out.append(
                f"            {{ {q(ore.deepslate_ore_block)}, {q('deepslate')}, "
                f"{int(ore.min_y)}, {int(ore.max_y)}, {int(ore.vein_size)}, "
                f"{int(ore.veins_per_chunk)}, {q(ore.dimension)}, {exp_lo} }},"
            )
    out.append("    };")
    out.append("")

    # Structures the Java side needs to know about (portals + arenas).
    portals = sorted(s.id for s in STRUCTS.ALL_STRUCTURES if s.id.endswith("_portal"))
    arenas = sorted(s.id for s in STRUCTS.ALL_STRUCTURES if s.is_boss_arena)
    out.append(string_array_decl("PORTAL_STRUCTURES", portals,
                                 "Portal structures; the portal block is placed by these."))
    out.append("")
    out.append(string_array_decl("BOSS_ARENAS", arenas,
                                 "Boss arena structures; entering one can trigger the fight."))
    out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------- #

HEADER = '''package com.biomesunseen.init;

import com.biomesunseen.entity.BossData;
import com.biomesunseen.entity.BossData.PhaseData;
import com.biomesunseen.entity.MobData;

/**
 * GENERATED FILE -- do not edit by hand.
 *
 * Produced by tools/generate_java.py from tools/content/* and tools/registry.py.
 * Regenerate with:  python3 tools/generate_java.py
 *
 * This class is pure data. It is the single source of truth the Java
 * registries loop over, so the registries, the JSON resources and the emitted
 * textures can never disagree about which ids exist. Adding a biome, ore, mob
 * or gear set to the content tables makes it appear here on the next run, and
 * the registration loops in BUBlocks / BUItems / BUEntities pick it up with no
 * further code changes.
 */
public final class BUContent {

    public static final String MODID = "biomesunseen";

    private BUContent() {
    }

'''

FOOTER = '''
    /** Every block id the mod registers, across all kinds. */
    public static String[] allBlocks() {
        java.util.List<String> all = new java.util.ArrayList<>();
        all.addAll(java.util.Arrays.asList(BLOCKS_CUBE));
        all.addAll(java.util.Arrays.asList(BLOCKS_GRASS));
        all.addAll(java.util.Arrays.asList(BLOCKS_LOG));
        all.addAll(java.util.Arrays.asList(BLOCKS_ORE));
        all.addAll(java.util.Arrays.asList(BLOCKS_MINERAL));
        all.addAll(java.util.Arrays.asList(BLOCKS_FLORA));
        all.addAll(java.util.Arrays.asList(BLOCKS_PORTAL));
        all.addAll(java.util.Arrays.asList(BLOCKS_LANTERN));
        all.addAll(java.util.Arrays.asList(BLOCKS_ALTAR));
        all.addAll(java.util.Arrays.asList(BLOCKS_FLUID));
        return all.toArray(new String[0]);
    }
}
'''


def main(argv: Optional[List[str]] = None) -> int:
    body = "\n".join([
        block_section(),
        item_section(),
        gear_section(),
        entity_section(),
        biome_section(),
    ])
    text = HEADER + body + FOOTER
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    lines = text.count("\n")
    print(f"[java] wrote {os.path.relpath(OUT, ROOT)} ({lines} lines)")
    print(f"[java] blocks={len(R.blocks)} items={len(R.items)} "
          f"entities={len(R.entities)} biomes={len(R.biomes)} "
          f"structures={len(R.structures)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
