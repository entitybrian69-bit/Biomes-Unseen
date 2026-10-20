#!/usr/bin/env python3
"""
generate_worldgen.py -- emit the datapack that makes the biomes real.

Until this runs, every biome in tools/content/biomes.py exists only as a Java
ResourceKey and a registry entry: the game has nothing to place, so none of the
140 biomes ever generate and the mod is a collection of items with no world.

This script turns the authored content tables into the 1.20.1 worldgen datapack:

    worldgen/biome/<id>.json
        Climate, sky/fog/water colours, authored music, ambient sound, particle
        ambience, carvers, vegetation and ore feature slots, and the spawn list.
    worldgen/configured_feature/ + placed_feature/
        One tree feature and one flora feature per authored id, plus a
        configured/placed pair per ore using that ore's real vein size, height
        range, count and air-exposure discard chance.
    dimension_type/<id>.json + dimension/<id>.json + worldgen/noise_settings/<id>.json
        + worldgen/multi_noise_biome_source_parameter_list/<id>.json
        The three new dimensions, each with its own stone surface rules built
        from the biome's authored surface_top / surface_filler / surface_stone.
    worldgen/structure/ + structure_set/ + template_pool/
        All 115 jigsaw structures with their authored spacing, separation,
        salt, terrain adaptation and start height.
    data/minecraft/tags/worldgen/biome/
        The vanilla category tags each biome belongs to, so vanilla systems
        (spawn rules, structure placement, mod compat) recognise them.
    Spawn placement needs no Forge biome modifier: each biome's own JSON carries
    its spawners, and a modifier is for editing biomes that are not ours.

Everything is derived from the content tables and the registry manifest, never
hand-listed: a biome, ore or structure added to tools/content/ appears in the
datapack on the next run with no edit here.

Surface rules are only authored for the three new dimensions. The Overworld
keeps vanilla noise settings, because overriding minecraft:overworld would
rewrite terrain shape for every other mod in the pack -- a total-conversion mod
should add biomes, not hijack the Overworld's heightmap.
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from content import biomes as B          # noqa: E402
from content import mobs as M            # noqa: E402
from content import ores as O            # noqa: E402
from content import structures as S      # noqa: E402
from registry import REGISTRY as R       # noqa: E402

MODID = "biomesunseen"
DATA = os.path.join(ROOT, "src", "main", "resources", "data")

# 1.20.1 GenerationStep.Decoration, in ordinal order. Slot meanings are fixed by
# the game, so features must go in the right one or they are placed at the wrong
# stage of chunk generation (ores after vegetation, for example, cut through it).
FEATURE_SLOTS = 11
SLOT_LOCAL_MODIFICATIONS = 2
SLOT_SURFACE_STRUCTURES = 4
SLOT_UNDERGROUND_ORES = 6
SLOT_UNDERGROUND_DECORATION = 7
SLOT_VEGETAL_DECORATION = 9
SLOT_TOP_LAYER_MODIFICATION = 10

WRITTEN = 0


ASSETS_ROOT = os.path.join(ROOT, "src", "main", "resources", "assets", MODID)


def audio_path(sound_id: str) -> str:
    """
    The .ogg a sound id would resolve to, by convention.

    "music.ethereal" -> assets/biomesunseen/sounds/music/ethereal.ogg, which is
    the path sounds.json would name for it.
    """
    bare = sound_id.split(":")[-1]
    return os.path.join(ASSETS_ROOT, "sounds", bare.replace(".", os.sep) + ".ogg")


def has_audio(sound_id: str) -> bool:
    """Whether a sound id has real audio behind it."""
    return bool(sound_id) and os.path.exists(audio_path(sound_id))


def rid(path: str) -> str:
    """Namespace a registry path, passing foreign namespaces through."""
    return path if ":" in path else f"{MODID}:{path}"


def bare(ref: str) -> str:
    """Strip the namespace from a possibly-qualified id."""
    return ref.split(":")[-1]


def write(rel: str, payload) -> None:
    """Write one JSON file under data/."""
    global WRITTEN
    dest = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=False)
        handle.write("\n")
    WRITTEN += 1


# --------------------------------------------------------------------------- #
#  Block resolution
# --------------------------------------------------------------------------- #

def block_state(name: str) -> dict:
    """A BlockState tag for a registry id."""
    return {"Name": rid(name)}


LOGS = sorted(b for b in R.blocks if b.endswith("_log"))
LEAVES = sorted(b for b in R.blocks if b.endswith("_leaves"))


def wood_pair(token: str):
    """
    Resolve a tree token to a (log, leaves) pair that actually exists.

    The content tables author 78 distinct tree feature names but only eight log
    blocks and ten leaf blocks were generated, so a name-to-block lookup has to
    fall back rather than emit a feature referencing a missing block -- which
    would make the tree feature fail to place and the biome grow nothing.
    """
    token = token.lower()
    log = None
    for candidate in LOGS:
        stem = candidate[:-4]
        if token.startswith(stem) or stem.startswith(token.split("_")[0]):
            log = candidate
            break
    if log is None:
        log = "lumen_log"
    stem = log[:-4]
    leaves = f"{stem}_leaves"
    if leaves not in LEAVES:
        leaves = LEAVES[0]
    return log, leaves


FLORA_BY_BIOME = {}


def flora_for(spec) -> list:
    """
    The flora blocks a biome scatters.

    Drawn from the cross-model blocks the registry actually contains, matched on
    the biome's own surface material so a lumen biome grows lumen flora rather
    than an arbitrary flower. Falls back to any available flora so no biome is
    left barren.
    """
    if spec.id in FLORA_BY_BIOME:
        return FLORA_BY_BIOME[spec.id]
    cross = sorted(b for b, k in R._kind.items() if "CROSS" in str(k))
    if not cross:
        cross = sorted(b for b in R.blocks if b.endswith("_sprout") or b.endswith("_bloom"))
    stem = bare(spec.surface_top).split("_")[0]
    chosen = [c for c in cross if c.startswith(stem)]
    if not chosen:
        chosen = cross[:3]
    FLORA_BY_BIOME[spec.id] = chosen[:4]
    return FLORA_BY_BIOME[spec.id]


# --------------------------------------------------------------------------- #
#  Features
# --------------------------------------------------------------------------- #

def emit_tree_feature(token: str) -> None:
    """A configured + placed feature pair for one authored tree id."""
    path = bare(token)
    log, leaves = wood_pair(path.replace("_trees", ""))
    configured = {
        "type": "minecraft:tree",
        "config": {
            "ignore_vines": True,
            "minimum_size": {"type": "minecraft:two_layers_feature_size", "limit": 1,
                             "lower_size": 0, "upper_size": 1},
            "dirt_provider": {"type": "minecraft:simple_state_provider",
                              "state": block_state("minecraft:dirt")},
            "trunk_provider": {"type": "minecraft:simple_state_provider",
                               "state": block_state(log)},
            "trunk_placer": {"type": "minecraft:straight_trunk_placer",
                             "base_height": 5, "height_rand_a": 2, "height_rand_b": 1},
            "foliage_provider": {"type": "minecraft:simple_state_provider",
                                 "state": block_state(leaves)},
            "foliage_placer": {"type": "minecraft:blob_foliage_placer",
                               "radius": 2, "offset": 0, "height": 3},
            "decorators": [],
        },
    }
    write(f"{MODID}/worldgen/configured_feature/{path}.json", configured)

    placed = {
        "feature": rid(path),
        "placement": [
            {"type": "minecraft:block_predicate_filter",
             "predicate": {"type": "minecraft:would_survive",
                           "state": {"Name": rid(log)}}},
            {"type": "minecraft:in_square"},
            {"type": "minecraft:surface_water_depth_filter", "max_water_depth": 0},
            {"type": "minecraft:heightmap", "heightmap": "OCEAN_CANOPY"},
            {"type": "minecraft:biome"},
        ],
    }
    write(f"{MODID}/worldgen/placed_feature/{path}.json", placed)


def emit_flora_feature(spec) -> None:
    """A patch feature scattering this biome's flora."""
    path = bare(spec.flora_feature)
    states = [block_state(f) for f in flora_for(spec)]
    configured = {
        "type": "minecraft:random_patch",
        "config": {
            "tries": 32,
            "xz_spread": 7,
            "y_spread": 3,
            "feature": {
                "feature": {
                    "type": "minecraft:simple_block",
                    "config": {"to_place": {
                        "type": "minecraft:weighted_state_provider",
                        "entries": [{"weight": 1, "data": s} for s in states],
                    }},
                },
                "placement": [
                    {"type": "minecraft:block_predicate_filter",
                     "predicate": {"type": "minecraft:matching_blocks",
                                   "blocks": ["minecraft:air"]}},
                ],
            },
        },
    }
    write(f"{MODID}/worldgen/configured_feature/{path}.json", configured)
    write(f"{MODID}/worldgen/placed_feature/{path}.json", {
        "feature": rid(path),
        "placement": [
            {"type": "minecraft:in_square"},
            {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"},
            {"type": "minecraft:biome"},
        ],
    })


def emit_ore_features() -> dict:
    """
    A configured + placed feature pair per ore.

    Vein size, count, height range and air-exposure discard all come from the
    authored OreSpec, so an ore's rarity in the world matches what the content
    table says rather than a flat default.
    """
    placed_by_ore = {}
    for ore in O.ALL_ORES:
        path = f"ore_{ore.base_name}"
        host = ore.host_stone
        host_block = host if host.startswith("minecraft:") or host in R.blocks \
            else f"{MODID}:{host}"
        targets = [{"target": {"predicate_type": "minecraft:tag_match",
                               "tag": "minecraft:stone_ore_replaceables"},
                    "state": block_state(ore.ore_block)}]
        if ore.dimension == "overworld" and ore.deepslate_ore_block in R.blocks:
            targets.append({"target": {"predicate_type": "minecraft:tag_match",
                                      "tag": "minecraft:deepslate_ore_replaceables"},
                            "state": block_state(ore.deepslate_ore_block)})
        if host_block not in ("minecraft:stone", f"{MODID}:stone"):
            # Dimension ores replace their own host stone, not vanilla's.
            targets = [{"target": {"predicate_type": "minecraft:block_match",
                                   "block": rid(host)},
                        "state": block_state(ore.ore_block)}]

        write(f"{MODID}/worldgen/configured_feature/{path}.json", {
            "type": "minecraft:ore",
            "config": {
                "discard_chance_on_air_exposure": ore.air_exposure,
                "size": ore.vein_size,
                "targets": targets,
            },
        })
        write(f"{MODID}/worldgen/placed_feature/{path}.json", {
            "feature": rid(path),
            "placement": [
                {"type": "minecraft:count", "count": ore.veins_per_chunk},
                {"type": "minecraft:in_square"},
                {"type": "minecraft:height_range",
                 "height": {"type": "minecraft:trapezoid",
                            "min_inclusive": {"absolute": ore.min_y},
                            "max_inclusive": {"absolute": ore.max_y}}},
                {"type": "minecraft:biome"},
            ],
        })
        placed_by_ore[ore.base_name] = rid(path)
    return placed_by_ore


# --------------------------------------------------------------------------- #
#  Biomes
# --------------------------------------------------------------------------- #

SPAWN_CATEGORY_BY_MOB = {m.id: m.spawn_category for m in M.ALL_MOBS}
SPAWN_CATEGORIES = ["monster", "creature", "ambient", "axolotls",
                    "underground_water_creature", "water_creature",
                    "water_ambient", "misc"]


def spawners_for(spec) -> dict:
    """The spawn list, grouped into the categories the game requires."""
    out = {c: [] for c in SPAWN_CATEGORIES}
    for entity_id, weight, minimum, maximum in spec.spawns:
        mob = bare(entity_id)
        category = SPAWN_CATEGORY_BY_MOB.get(mob, "creature")
        if category not in out:
            category = "creature"
        out[category].append({"type": rid(mob), "weight": weight,
                              "minCount": minimum, "maxCount": maximum})
    return out


def effects_for(spec) -> dict:
    """Sky, fog, water, music, ambience and particles."""
    effects = {
        "sky_color": spec.sky_color,
        "fog_color": spec.fog_color,
        "water_color": spec.water_color,
        "water_fog_color": spec.water_fog_color,
        "grass_color_modifier": "none",
    }
    if spec.foliage_color is not None:
        effects["foliage_color"] = spec.foliage_color
    if spec.grass_color is not None:
        effects["grass_color"] = spec.grass_color
    # Music and ambience are emitted only when the audio actually exists.
    #
    # A biome that names a SoundEvent with no sounds.json definition makes the
    # client log "Unable to play unknown soundEvent" every time it tries to start
    # the track -- which for biome music is every 12-24 seconds per player, in
    # all 140 biomes, forever. Referencing only audio that ships keeps the log
    # clean, and because the ids stay in the content tables the moment a track is
    # added and the generator re-run, every biome that authored it switches on
    # with no further edit.
    if spec.ambient_sound and has_audio(spec.ambient_sound):
        effects["ambient_sound"] = spec.ambient_sound
    if spec.music and has_audio(spec.music):
        effects["music"] = {
            "sound": spec.music,
            "min_delay": 12000,
            "max_delay": 24000,
            "replace_current_music": True,
        }
    if spec.particle:
        effects["particle"] = {
            "options": {"type": spec.particle},
            # Low enough to read as ambience rather than weather; the authored
            # particles are motes and drifting spores.
            "probability": 0.0035,
        }
    return effects


def emit_biome(spec, ore_features: dict) -> None:
    """One biome JSON."""
    features = [[] for _ in range(FEATURE_SLOTS)]

    for ore in spec.ores:
        placed = ore_features.get(ore)
        if placed:
            features[SLOT_UNDERGROUND_ORES].append(placed)

    if spec.tree_feature and spec.trees_per_chunk > 0:
        tree_path = bare(spec.tree_feature)
        # The count wrapper is its own placed feature so trees_per_chunk from the
        # content table controls density instead of every biome being identical.
        counted = f"{tree_path}_counted"
        write(f"{MODID}/worldgen/placed_feature/{counted}.json", {
            "feature": rid(tree_path),
            "placement": [
                {"type": "minecraft:count_on_every_surface",
                 "chunk_count": spec.trees_per_chunk},
                {"type": "minecraft:biome"},
            ],
        })
        features[SLOT_VEGETAL_DECORATION].append(rid(counted))

    if spec.flora_feature and spec.grass_per_chunk > 0:
        flora_path = bare(spec.flora_feature)
        counted = f"{flora_path}_counted"
        write(f"{MODID}/worldgen/placed_feature/{counted}.json", {
            "feature": rid(flora_path),
            "placement": [
                {"type": "minecraft:count", "count": spec.grass_per_chunk},
                {"type": "minecraft:biome"},
            ],
        })
        features[SLOT_VEGETAL_DECORATION].append(rid(counted))

    # Vanilla staples every biome needs: glow lichen underground, and the frost
    # / ice pass that makes water freeze where the climate says it should.
    features[SLOT_UNDERGROUND_DECORATION].append("minecraft:glow_lichen")
    features[SLOT_TOP_LAYER_MODIFICATION].append("minecraft:freeze_top_layer")

    biome = {
        "temperature": spec.temperature,
        "downfall": spec.humidity,
        "has_precipitation": spec.has_precipitation,
        "effects": effects_for(spec),
        "spawners": spawners_for(spec),
        "spawn_costs": {},
        "carvers": {"air": list(spec.carvers)},
        "features": features,
    }
    write(f"{MODID}/worldgen/biome/{spec.id}.json", biome)


# --------------------------------------------------------------------------- #
#  Biome tags
# --------------------------------------------------------------------------- #

CATEGORY_TAG = {
    "ethereal": "is_overworld",
    "ancient": "is_overworld",
    "vibrant": "is_overworld",
    "harsh": "is_overworld",
    "aquatic": "is_overworld",
}


def emit_biome_tags() -> None:
    """
    Register each biome under the vanilla worldgen tags it belongs to.

    Without these, vanilla systems that select biomes by tag -- structure
    placement, some spawn rules, and every other mod's compat layer -- cannot
    see the new biomes at all.
    """
    groups: dict[str, list] = {}
    for spec in B.ALL_BIOMES:
        if spec.dimension == "overworld":
            groups.setdefault("is_overworld", []).append(rid(spec.id))
            groups.setdefault(f"category_{spec.category}", []).append(rid(spec.id))
            if spec.temperature <= 0.15:
                groups.setdefault("is_taiga", []).append(rid(spec.id))
            if spec.temperature >= 1.2:
                groups.setdefault("is_badlands", []).append(rid(spec.id))
            if spec.category == "aquatic":
                groups.setdefault("is_ocean", []).append(rid(spec.id))
                groups.setdefault("is_deep_ocean", []).append(rid(spec.id))
        else:
            groups.setdefault(f"dimension_{spec.dimension}", []).append(rid(spec.id))
        groups.setdefault(f"has_structure_set_{spec.dimension}", []).append(rid(spec.id))

    for tag, entries in groups.items():
        namespace = "minecraft" if tag.startswith("is_") else MODID
        write(f"{namespace}/tags/worldgen/biome/{tag}.json",
              {"replace": False, "values": sorted(set(entries))})


# --------------------------------------------------------------------------- #
#  Dimensions
# --------------------------------------------------------------------------- #

DIMENSION_PROFILE = {
    "hollow_deep": {
        "has_skylight": False, "has_ceiling": True, "ultrawarm": False,
        "ambient_light": 0.08, "min_y": -64, "height": 384, "logical_height": 384,
        "natural": False, "bed_works": False, "respawn_anchor_works": True,
        "piglin_safe": False, "has_raids": False, "coordinate_scale": 1.0,
        "effects": "minecraft:the_nether", "infiniburn": "#minecraft:infiniburn_nether",
        "monster_spawn_light_level": 7,
    },
    "aetherfall": {
        "has_skylight": True, "has_ceiling": False, "ultrawarm": False,
        "ambient_light": 0.25, "min_y": 0, "height": 384, "logical_height": 384,
        "natural": True, "bed_works": True, "respawn_anchor_works": False,
        "piglin_safe": False, "has_raids": False, "coordinate_scale": 1.0,
        "effects": "minecraft:overworld", "infiniburn": "#minecraft:infiniburn_overworld",
        "monster_spawn_light_level": 0,
    },
    "void_between": {
        "has_skylight": False, "has_ceiling": False, "ultrawarm": False,
        "ambient_light": 0.05, "min_y": 0, "height": 256, "logical_height": 256,
        "natural": False, "bed_works": False, "respawn_anchor_works": True,
        "piglin_safe": True, "has_raids": False, "coordinate_scale": 1.0,
        "effects": "minecraft:the_end", "infiniburn": "#minecraft:infiniburn_end",
        "monster_spawn_light_level": 7,
    },
}


def surface_rules(dimension: str) -> dict:
    """
    Per-biome surface rules for one dimension.

    Each biome's authored surface_top / surface_filler / surface_stone becomes a
    biome-conditioned rule, so a biome of spore chalk actually has a floor of
    spore chalk rather than inheriting its dimension's default stone.
    """
    sequence = []
    for spec in B.ALL_BIOMES:
        if spec.dimension != dimension:
            continue
        sequence.append({
            "type": "minecraft:condition",
            "if_true": {"type": "minecraft:biome", "biome_is": [rid(spec.id)]},
            "then_result": {
                "type": "minecraft:sequence",
                "sequence": [
                    {"type": "minecraft:condition",
                     "if_true": {"type": "minecraft:stone_depth", "surface_type": "floor",
                                 "add_surface_depth": False, "secondary_depth_range": 0,
                                 "offset": 0},
                     "then_result": {"type": "minecraft:block",
                                     "result_state": block_state(spec.surface_top)}},
                    {"type": "minecraft:condition",
                     "if_true": {"type": "minecraft:stone_depth", "surface_type": "floor",
                                 "add_surface_depth": True, "secondary_depth_range": 0,
                                 "offset": 0},
                     "then_result": {"type": "minecraft:block",
                                     "result_state": block_state(spec.surface_filler)}},
                ],
            },
        })
    default_stone = bare(B.DIMENSION_STONES[dimension][0]) if B.DIMENSION_STONES.get(dimension) else "stone"
    sequence.append({"type": "minecraft:block",
                     "result_state": block_state(default_stone)})
    return {"type": "minecraft:sequence", "sequence": sequence}


# Density-node helpers. The noise router is a tree of nested argument maps;
# composing it through these keeps the brackets balanced by construction and
# makes each term readable, which a hand-written 40-deep literal is not.
def const(value) -> dict:
    return {"type": "minecraft:constant", "argument": value}


def add(a, b) -> dict:
    return {"type": "minecraft:add", "argument1": a, "argument2": b}


def mul(a, b) -> dict:
    return {"type": "minecraft:mul", "argument1": a, "argument2": b}


def min_of(a, b) -> dict:
    return {"type": "minecraft:min", "argument1": a, "argument2": b}


def abs_of(a) -> dict:
    return {"type": "minecraft:abs", "argument": a}


def noise(name: str, xz_scale: float, y_scale: float) -> dict:
    return {"type": "minecraft:noise", "noise": name,
            "xz_scale": xz_scale, "y_scale": y_scale}


def y_gradient(from_y: int, to_y: int, from_value: float, to_value: float) -> dict:
    return {"type": "minecraft:y_clamped_gradient", "from_y": from_y, "to_y": to_y,
            "from_value": from_value, "to_value": to_value}


def squeeze(argument) -> dict:
    return {"type": "minecraft:squeeze", "argument": argument}


def interpolated(argument) -> dict:
    return {"type": "minecraft:interpolated", "argument": argument}


def blend_density(argument) -> dict:
    return {"type": "minecraft:blend_density", "argument": argument}


def final_density(profile: dict, floating: bool) -> dict:
    """
    The terrain density field for a dimension.

    Two vertical gradients fade density in from the floor and out at the ceiling
    so the dimension has a hard bottom and top rather than trailing off into
    void. A noise term carves the interior: subtracting the absolute value of a
    noise field produces isolated blobs, which is what floating islands are, and
    adding a plain noise field produces connected caverns, which is what an
    underground dimension needs.

    Both are wrapped in the vanilla squeeze/interpolate/blend chain so chunk
    borders do not seam.
    """
    floor = profile["min_y"]
    ceiling = profile["min_y"] + profile["height"]

    base = y_gradient(floor, floor + 8, 0.0, 1.0)
    top = y_gradient(ceiling - 56, ceiling - 8, 1.0, 0.0)

    # 0.234375 and 0.5 are the constants vanilla's own noise settings use for
    # the floor/ceiling fade; matching them keeps the blend at chunk borders.
    shell = add(const(-0.234375),
                mul(base, add(const(0.234375), mul(top, const(0.5)))))

    if floating:
        # Islands: negated ridged noise leaves disconnected blobs of terrain
        # suspended in empty space, with no ground to walk on below.
        carve = add(const(0.22), mul(const(-1.0), abs_of(
            noise("minecraft:gravel", 0.55, 0.55))))
    else:
        # Cavernous: a broad noise field hollows out passages through the shell
        # so the dimension is explorable rather than solid stone.
        carve = add(const(0.18), mul(const(-0.42),
                                     noise("minecraft:cave_cheese", 0.7, 0.45)))

    density = blend_density(interpolated(add(shell, carve)))
    squeezed = squeeze(mul(const(0.64), density))
    return min_of(squeezed,
                  {"type": "minecraft:cave_surface",
                   "surface_depth_multiplier": -0.075,
                   "random_name_offset_range": 0.0})


def emit_dimension(dimension: str) -> None:
    """Dimension type, noise settings, biome source and level stem."""
    profile = DIMENSION_PROFILE[dimension]
    specs = [b for b in B.ALL_BIOMES if b.dimension == dimension]

    write(f"{MODID}/dimension_type/{dimension}.json", {
        "ultrawarm": profile["ultrawarm"],
        "natural": profile["natural"],
        "coordinate_scale": profile["coordinate_scale"],
        "has_skylight": profile["has_skylight"],
        "has_ceiling": profile["has_ceiling"],
        "ambient_light": profile["ambient_light"],
        "piglin_safe": profile["piglin_safe"],
        "bed_works": profile["bed_works"],
        "respawn_anchor_works": profile["respawn_anchor_works"],
        "has_raids": profile["has_raids"],
        "logical_height": profile["logical_height"],
        "min_y": profile["min_y"],
        "height": profile["height"],
        "infiniburn": profile["infiniburn"],
        "effects": profile["effects"],
        "monster_spawn_light_level": profile["monster_spawn_light_level"],
        "monster_spawn_block_light_limit": 0,
    })

    stones = B.DIMENSION_STONES.get(dimension) or ["stone"]
    default_stone = bare(stones[0])

    write(f"{MODID}/worldgen/noise_settings/{dimension}.json", {
        "sea_level": profile["min_y"] + 32,
        "disable_mob_generation": False,
        "aquifers_enabled": False,
        "ore_veins_enabled": False,
        "legacy_random_source": False,
        "default_block": {"Name": rid(default_stone)},
        "default_fluid": {"Name": "minecraft:water", "Properties": {"level": "0"}},
        "noise": {"min_y": profile["min_y"], "height": profile["height"],
                  "size_horizontal": 1, "size_vertical": 2},
        "noise_router": {
            "barrier": const(0),
            "fluid_level_floodedness": const(0),
            "fluid_level_spread": const(0),
            "lava": const(0),
            "temperature": {"type": "minecraft:shifted_noise",
                            "noise": "minecraft:temperature",
                            "shift_x": "minecraft:shift_x", "shift_y": 0,
                            "shift_z": "minecraft:shift_z",
                            "xz_scale": 0.25, "y_scale": 0},
            "vegetation": {"type": "minecraft:shifted_noise",
                           "noise": "minecraft:vegetation",
                           "shift_x": "minecraft:shift_x", "shift_y": 0,
                           "shift_z": "minecraft:shift_z",
                           "xz_scale": 0.25, "y_scale": 0},
            "continents": const(0),
            "erosion": const(0),
            "depth": const(0),
            "ridges": const(0),
            "initial_density_without_jaggedness": const(0),
            "final_density": final_density(profile, dimension == "aetherfall"),
            "vein_toggle": const(0),
            "vein_ridged": const(0),
            "vein_gap": const(0),
        },
        "spawn_target": [],
        "surface_rule": surface_rules(dimension),
    })

    # Multi-noise biome source: each biome sits at its authored climate
    # coordinates, so the dimension's geography follows the content tables
    # rather than a flat uniform spread.
    entries = [{
        "biome": rid(spec.id),
        "parameters": {
            "temperature": spec.temperature,
            "humidity": spec.humidity,
            "continentalness": spec.continentalness,
            "erosion": spec.erosion,
            "weirdness": spec.weirdness,
            "depth": spec.depth,
            "offset": spec.offset,
        },
    } for spec in specs]

    write(f"{MODID}/dimension/{dimension}.json", {
        "type": rid(dimension),
        "generator": {
            "type": "minecraft:noise",
            "settings": rid(dimension),
            "biome_source": {"type": "minecraft:multi_noise", "biomes": entries},
        },
    })


# --------------------------------------------------------------------------- #
#  Structures
# --------------------------------------------------------------------------- #

def emit_structures() -> None:
    """Jigsaw structures, their pools and their spread placement."""
    for spec in S.ALL_STRUCTURES:
        pool = spec.start_jigsaw_pool
        pool_path = bare(pool)
        write(f"{MODID}/worldgen/template_pool/{pool_path}.json", {
            "name": rid(pool_path),
            "fallback": "minecraft:empty",
            "elements": [{
                "weight": 1,
                "element": {
                    "element_type": "minecraft:single_pool_element",
                    "location": rid(f"{pool_path}/start"),
                    "processors": "minecraft:empty",
                    "projection": "rigid",
                },
            }],
        })

        height = spec.start_height or {"absolute": 0}
        structure = {
            "type": "minecraft:jigsaw",
            "step": spec.step,
            "spawn_overrides": {},
            "terrain_adaptation": spec.terrain_adaptation,
            "start_pool": rid(pool_path),
            "size": spec.max_depth,
            "start_height": height,
            "project_start_to_heightmap": "WORLD_SURFACE_WG"
            if spec.step == "surface_structures" else "OCEAN_FLOOR_WG",
            "max_distance_from_center": 80,
            "use_expansion_hash": spec.use_expansion_hash,
            "liquid_settings": spec.liquid_settings,
        }
        write(f"{MODID}/worldgen/structure/{spec.id}.json", structure)

        placement = {
            "type": "minecraft:random_spread",
            "spacing": spec.spacing,
            "separation": spec.separation,
            "salt": spec.salt,
        }
        if spec.use_expansion_hash:
            placement["spread_type"] = "triangular"
        write(f"{MODID}/worldgen/structure_set/{spec.id}.json", {
            "structures": [{"structure": rid(spec.id), "weight": 1}],
            "placement": placement,
        })


def emit_structure_biome_tags() -> None:
    """
    One tag per structure listing the biomes it may generate in.

    Jigsaw structures select biomes by tag; without these every structure would
    either be unplaceable or placeable everywhere, ignoring the authored
    biome list.
    """
    per_structure: dict[str, set] = {}
    for spec in B.ALL_BIOMES:
        for struct in spec.structures:
            per_structure.setdefault(bare(struct), set()).add(rid(spec.id))
    # Structures authored in structures.py also name their biomes; union both so
    # neither direction of the cross-reference is lost.
    for spec in S.ALL_STRUCTURES:
        for biome in spec.biomes:
            per_structure.setdefault(spec.id, set()).add(rid(bare(biome)))
    for struct, biomes in per_structure.items():
        write(f"{MODID}/tags/worldgen/biome/has_structure/{struct}.json",
              {"replace": False, "values": sorted(biomes)})


# --------------------------------------------------------------------------- #
#  Spawn placement
# --------------------------------------------------------------------------- #

def main() -> None:
    print("[worldgen] emitting datapack")

    trees = sorted({b.tree_feature for b in B.ALL_BIOMES if b.tree_feature})
    for token in trees:
        emit_tree_feature(token)
    print(f"[worldgen] tree features: {len(trees)}")

    for spec in B.ALL_BIOMES:
        if spec.flora_feature:
            emit_flora_feature(spec)
    print(f"[worldgen] flora features: "
          f"{len({b.flora_feature for b in B.ALL_BIOMES if b.flora_feature})}")

    ore_features = emit_ore_features()
    print(f"[worldgen] ore features: {len(ore_features)}")

    for spec in B.ALL_BIOMES:
        emit_biome(spec, ore_features)
    print(f"[worldgen] biomes: {len(B.ALL_BIOMES)}")

    emit_biome_tags()
    for dimension in ("hollow_deep", "aetherfall", "void_between"):
        emit_dimension(dimension)
    print("[worldgen] dimensions: 3")

    emit_structures()
    emit_structure_biome_tags()
    print(f"[worldgen] structures: {len(S.ALL_STRUCTURES)}")

    print(f"[worldgen] wrote {WRITTEN} files")


if __name__ == "__main__":
    main()
