"""
content/biomes.py -- the full 140-biome table.

80 Overworld biomes across the five mandated categories (Ethereal, Ancient,
Vibrant, Harsh, Aquatic) plus 20 biomes in each of the three dimensions.

Every entry is a BiomeSpec. The spec carries the climate points used by the
custom MultiNoiseBiomeSource, the surface block set, the feature loadout and
the spawn table -- so a biome declared here is genuinely playable, not a stub.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
#  Categories (the five mandated Overworld families + the three dimensions)
# ---------------------------------------------------------------------------

CATEGORIES: Tuple[str, ...] = ("ethereal", "ancient", "vibrant", "harsh", "aquatic")

DIMENSIONS: Tuple[str, ...] = ("overworld", "hollow_deep", "aetherfall", "void_between")

CATEGORY_DESCRIPTION: Dict[str, str] = {
    "ethereal": "Dreamlike light, floating spores, luminous flora. Low contrast, high bloom.",
    "ancient":  "Petrified, ruined, colossal. Old-growth silhouettes and weathered stone.",
    "vibrant":  "Saturated, high-energy, densely featured. The showcase biomes.",
    "harsh":    "Extreme climate, sparse cover, high danger. Volcanic, frozen, blighted.",
    "aquatic":  "Water-dominant: rivers, reefs, abyssal trenches, flooded ruins.",
}


@dataclass(frozen=True)
class BiomeSpec:
    """Full authoring spec for one biome."""

    id: str
    name: str
    dimension: str
    category: str

    # --- MultiNoiseBiomeSource climate points ------------------------------
    temperature: float = 0.5
    humidity: float = 0.5
    continentalness: float = 0.3
    erosion: float = 0.3
    depth: float = 0.0
    weirdness: float = 0.0
    offset: float = 0.0

    # --- Sky / fog / water -------------------------------------------------
    sky_color: int = 0x78A7FF
    fog_color: int = 0xC0D8FF
    water_color: int = 0x3F76E4
    water_fog_color: int = 0x050533
    foliage_color: Optional[int] = None
    grass_color: Optional[int] = None
    has_precipitation: bool = True

    # --- Surface -----------------------------------------------------------
    surface_top: str = "minecraft:grass_block"
    surface_filler: str = "minecraft:dirt"
    surface_stone: str = "minecraft:stone"
    sea_level: int = 63

    # --- Terrain -----------------------------------------------------------
    base_height: float = 0.1
    height_variation: float = 0.2
    terrain_type: str = "default"

    # --- Content -----------------------------------------------------------
    trees_per_chunk: int = 4
    tree_feature: Optional[str] = None
    grass_per_chunk: int = 8
    flora_feature: Optional[str] = None
    ores: Tuple[str, ...] = ()
    structures: Tuple[str, ...] = ()
    carvers: Tuple[str, ...] = ("minecraft:cave", "minecraft:cave_extra_underground")
    music: Optional[str] = None
    ambient_sound: Optional[str] = None
    particle: Optional[str] = None

    # --- Spawns: (entity_id, weight, min_group, max_group) ------------------
    spawns: Tuple[Tuple[str, int, int, int], ...] = ()
    creature_spawn_probability: float = 0.1

    # --- Presentation ------------------------------------------------------
    weight: int = 100
    edge_of: Tuple[str, ...] = ()
    lore: str = ""

    @property
    def resource_key(self) -> str:
        return f"biomesunseen:{self.id}"

    @property
    def noise_params(self) -> Tuple[float, ...]:
        """(temperature, humidity, continentalness, erosion, depth, weirdness, offset)."""
        return (
            self.temperature, self.humidity, self.continentalness,
            self.erosion, self.depth, self.weirdness, self.offset,
        )


def _ow(
    id: str, name: str, category: str, *,
    temperature: float, humidity: float, continentalness: float, erosion: float,
    weirdness: float = 0.0, depth: float = 0.0, offset: float = 0.0,
    **kw,
) -> BiomeSpec:
    """Overworld biome constructor with the shared defaults applied."""
    return BiomeSpec(
        id=id, name=name, dimension="overworld", category=category,
        temperature=temperature, humidity=humidity,
        continentalness=continentalness, erosion=erosion,
        weirdness=weirdness, depth=depth, offset=offset, **kw,
    )


def _dim(id: str, name: str, dimension: str, category: str, *, depth: float, weirdness: float,
         stone: str, top: str, filler: str, **kw) -> BiomeSpec:
    """Dimension biome constructor: no sky, deep noise bands, custom stone."""
    return BiomeSpec(
        id=id, name=name, dimension=dimension, category=category,
        depth=depth, weirdness=weirdness,
        surface_stone=stone, surface_top=top, surface_filler=filler,
        has_precipitation=False, **kw,
    )


# ===========================================================================
#  THE OVERWORLD -- 80 BIOMES
#  16 per category. Climate points are spread across the vanilla parameter
#  space so the custom MultiNoiseBiomeSource interleaves them with vanilla
#  terrain instead of replacing it wholesale.
# ===========================================================================

OVERWORLD_BIOMES: List[BiomeSpec] = [
    # ---------------------------------------------------------------------
    #  ETHEREAL (16)
    # ---------------------------------------------------------------------
    _ow("luminescent_grove", "Luminescent Grove", "ethereal",
        temperature=0.65, humidity=0.85, continentalness=0.25, erosion=0.15,
        surface_top="biomesunseen:lumen_grass_block",
        surface_filler="biomesunseen:lumen_dirt",
        sky_color=0x2A1B4A, fog_color=0x6E4FB8, water_color=0x7A5FD6,
        grass_color=0x8FD96A, foliage_color=0x82CC5C,
        trees_per_chunk=10, tree_feature="biomesunseen:lumen_trees",
        grass_per_chunk=20, flora_feature="biomesunseen:lumen_flora",
        ores=("lumenite", "glimmerleaf", "sporeamber"),
        structures=("biomesunseen:grove_shrine",),
        particle="biomesunseen:lumen_mote",
        music="biomesunseen:music.ethereal",
        spawns=(("biomesunseen:glimmerwing", 40, 2, 5), ("biomesunseen:mossback_hare", 20, 2, 4)),
        lore="A grove that never learned the difference between dusk and dawn."),

    _ow("moonpetal_meadow", "Moonpetal Meadow", "ethereal",
        temperature=0.55, humidity=0.7, continentalness=0.2, erosion=0.4,
        surface_top="biomesunseen:lumen_grass_block",
        sky_color=0x1B2447, fog_color=0x5A6FB0, water_color=0x4A6FD0,
        grass_color=0x9FE0A8, foliage_color=0x74C08A,
        trees_per_chunk=1, tree_feature="biomesunseen:moonpetal_trees",
        grass_per_chunk=28, flora_feature="biomesunseen:moonpetal_flora",
        ores=("moonpetal", "lumenite"),
        particle="biomesunseen:moonpetal_drift",
        music="biomesunseen:music.ethereal",
        spawns=(("biomesunseen:petaldancer", 30, 2, 4),),
        lore="The petals only open when nothing is watching them."),

    _ow("duskwood_hollow", "Duskwood Hollow", "ethereal",
        temperature=0.5, humidity=0.8, continentalness=0.3, erosion=0.2,
        surface_top="biomesunseen:spore_grass_block",
        sky_color=0x3A2A55, fog_color=0x6B4E8A, water_color=0x5A4A9A,
        grass_color=0x87A04C, foliage_color=0x6E8A3C,
        trees_per_chunk=12, tree_feature="biomesunseen:duskwood_trees",
        grass_per_chunk=14, flora_feature="biomesunseen:duskwood_flora",
        ores=("duskite", "sporeamber", "graveamber"),
        structures=("biomesunseen:hollow_hut",),
        music="biomesunseen:music.ethereal",
        spawns=(("biomesunseen:duskstalker", 25, 1, 2), ("biomesunseen:sporeling", 30, 3, 6)),
        lore="Every tree here grew around something it refused to let go of."),

    _ow("starfall_glade", "Starfall Glade", "ethereal",
        temperature=0.4, humidity=0.5, continentalness=0.1, erosion=0.5,
        surface_top="biomesunseen:lumen_grass_block",
        sky_color=0x0E1430, fog_color=0x3A4A8A, water_color=0x2A3A7A,
        grass_color=0xB0D08A, foliage_color=0x90B870,
        trees_per_chunk=3, tree_feature="biomesunseen:starfall_trees",
        grass_per_chunk=22, flora_feature="biomesunseen:starfall_flora",
        ores=("starfall", "lumenite", "moonpetal"),
        structures=("biomesunseen:starfall_crater",),
        particle="biomesunseen:starfall_ember",
        music="biomesunseen:music.ethereal",
        spawns=(("biomesunseen:glimmerwing", 35, 2, 5),),
        lore="The craters are warm. Something is still falling."),

    _ow("whispering_mire", "Whispering Mire", "ethereal",
        temperature=0.6, humidity=0.95, continentalness=0.4, erosion=0.6,
        surface_top="biomesunseen:spore_grass_block",
        sky_color=0x2A3A3A, fog_color=0x5A7A6A, water_color=0x3A5A4A,
        grass_color=0x6E9A5A, foliage_color=0x5A8348,
        trees_per_chunk=4, tree_feature="biomesunseen:mire_trees",
        grass_per_chunk=18, flora_feature="biomesunseen:mire_flora",
        ores=("sporeamber", "graveamber", "wraithsalt"),
        music="biomesunseen:music.ethereal",
        ambient_sound="biomesunseen:ambient.whisper",
        spawns=(("biomesunseen:mire_wisp", 30, 1, 3), ("biomesunseen:bogcrawler", 20, 1, 2)),
        lore="It repeats the last thing you said, in your own voice, a half-second late."),

    _ow("aurora_steppe", "Aurora Steppe", "ethereal",
        temperature=0.25, humidity=0.3, continentalness=0.5, erosion=0.3,
        surface_top="biomesunseen:crystal_grass_block",
        sky_color=0x1A3A5A, fog_color=0x4A8AB0, water_color=0x3A6A9A,
        grass_color=0x8AC8C0, foliage_color=0x6AB0A8,
        trees_per_chunk=1, tree_feature="biomesunseen:aurora_trees",
        grass_per_chunk=24, flora_feature="biomesunseen:aurora_flora",
        ores=("frostvein", "lumenite", "echo_crystal"),
        particle="biomesunseen:aurora_ribbon",
        music="biomesunseen:music.ethereal",
        spawns=(("biomesunseen:aurora_stag", 20, 2, 4),),
        lore="The light moves like grass. The grass moves like light."),

    _ow("dreaming_atoll", "Dreaming Atoll", "ethereal",
        temperature=0.85, humidity=0.9, continentalness=-0.2, erosion=0.4,
        surface_top="biomesunseen:lumen_sand",
        sky_color=0x3A6AB0, fog_color=0x8AB0D8, water_color=0x4AC8D8,
        grass_color=0xA0E0B0, foliage_color=0x80C898,
        trees_per_chunk=5, tree_feature="biomesunseen:atoll_palm",
        grass_per_chunk=12, flora_feature="biomesunseen:atoll_flora",
        ores=("tideglass", "coralite", "deep_pearl"),
        structures=("biomesunseen:atoll_ruin",),
        music="biomesunseen:music.ethereal",
        spawns=(("biomesunseen:reefglider", 25, 2, 4),),
        lore="The tide comes in twice a day and forgets something each time."),

    _ow("glimmering_thicket", "Glimmering Thicket", "ethereal",
        temperature=0.7, humidity=0.8, continentalness=0.35, erosion=0.25,
        surface_top="biomesunseen:lumen_grass_block",
        sky_color=0x2A2A5A, fog_color=0x6A6AB8, water_color=0x5A5AA8,
        grass_color=0x9AD87A, foliage_color=0x7AC05A,
        trees_per_chunk=14, tree_feature="biomesunseen:thicket_trees",
        grass_per_chunk=26, flora_feature="biomesunseen:thicket_flora",
        ores=("glimmerleaf", "lumenite", "sporeamber"),
        particle="biomesunseen:lumen_mote",
        music="biomesunseen:music.ethereal",
        spawns=(("biomesunseen:glimmerwing", 45, 3, 6), ("biomesunseen:thicket_sprite", 20, 1, 2)),
        lore="Dense enough that the light has to ask permission."),

    _ow("silken_canopy", "Silken Canopy", "ethereal",
        temperature=0.75, humidity=0.85, continentalness=0.3, erosion=0.1,
        surface_top="biomesunseen:lumen_grass_block",
        sky_color=0x4A6A8A, fog_color=0x8AAAB8, water_color=0x4A8A9A,
        grass_color=0xA8D898, foliage_color=0x88C078,
        trees_per_chunk=16, tree_feature="biomesunseen:canopy_trees",
        grass_per_chunk=10, flora_feature="biomesunseen:canopy_flora",
        ores=("spiritwood", "glimmerleaf"),
        structures=("biomesunseen:canopy_walk",),
        music="biomesunseen:music.ethereal",
        spawns=(("biomesunseen:silkweaver", 25, 2, 4), ("biomesunseen:canopy_glider", 20, 1, 3)),
        lore="The floor of this forest is a rumour. Nobody has confirmed it."),

    _ow("crystalline_tundra", "Crystalline Tundra", "ethereal",
        temperature=0.05, humidity=0.4, continentalness=0.45, erosion=0.35,
        surface_top="biomesunseen:crystal_grass_block",
        surface_filler="biomesunseen:crystal_dirt",
        surface_stone="biomesunseen:glacierite_block",
        sky_color=0x8AB8D8, fog_color=0xC8E0F0, water_color=0x6AAAC8,
        grass_color=0xA8DCE8, foliage_color=0x88C0D8,
        trees_per_chunk=1, tree_feature="biomesunseen:crystal_spike_trees",
        grass_per_chunk=8, flora_feature="biomesunseen:crystal_flora",
        ores=("glacierite", "frostbloom", "echo_crystal", "frostvein"),
        structures=("biomesunseen:crystal_spire_field",),
        music="biomesunseen:music.ethereal",
        spawns=(("biomesunseen:frostling", 25, 1, 3), ("biomesunseen:glacier_ox", 15, 2, 4)),
        lore="The ice here grew rather than froze. You can see where it branched."),

    _ow("petal_drift_flats", "Petal Drift Flats", "ethereal",
        temperature=0.6, humidity=0.6, continentalness=0.55, erosion=0.55,
        surface_top="biomesunseen:lumen_grass_block",
        sky_color=0x6A8AB8, fog_color=0xC0D0E8, water_color=0x5A9AD0,
        grass_color=0xC8E0A8, foliage_color=0xA8C888,
        trees_per_chunk=0, tree_feature=None,
        grass_per_chunk=30, flora_feature="biomesunseen:petal_drift_flora",
        ores=("moonpetal", "sunspore"),
        particle="biomesunseen:moonpetal_drift",
        music="biomesunseen:music.ethereal",
        spawns=(("biomesunseen:petaldancer", 40, 3, 6),),
        lore="Flat for a hundred miles and never once still."),

    _ow("hollowlight_basin", "Hollowlight Basin", "ethereal",
        temperature=0.45, humidity=0.75, continentalness=0.15, erosion=0.45,
        surface_top="biomesunseen:spore_grass_block",
        sky_color=0x2A4A4A, fog_color=0x5A9A8A, water_color=0x3A8A7A,
        grass_color=0x7AC8A0, foliage_color=0x5AB088,
        trees_per_chunk=6, tree_feature="biomesunseen:basin_trees",
        grass_per_chunk=20, flora_feature="biomesunseen:basin_flora",
        ores=("hollowite", "lumenshade", "deep_pearl"),
        structures=("biomesunseen:hollow_deep_portal",),
        music="biomesunseen:music.ethereal",
        spawns=(("biomesunseen:mire_wisp", 20, 1, 2),
                ("biomesunseen:aurora_stag", 12, 2, 3)),
        lore="The light pools here the way water pools. It does not drain."),

    _ow("veilwood", "Veilwood", "ethereal",
        temperature=0.55, humidity=0.85, continentalness=0.28, erosion=0.2,
        surface_top="biomesunseen:lumen_grass_block",
        sky_color=0x3A3A5A, fog_color=0x8A8AB8, water_color=0x5A5A8A,
        grass_color=0x9AC0B8, foliage_color=0x7AA8A0,
        trees_per_chunk=13, tree_feature="biomesunseen:veilwood_trees",
        grass_per_chunk=16, flora_feature="biomesunseen:veilwood_flora",
        ores=("duskite", "wraithsalt", "moonpetal"),
        music="biomesunseen:music.ethereal",
        spawns=(("biomesunseen:veilmourner", 15, 1, 1), ("biomesunseen:glimmerwing", 25, 2, 4)),
        lore="You can see the far treeline. You never get any closer to it."),

    _ow("lumenshade_glade", "Lumenshade Glade", "ethereal",
        temperature=0.6, humidity=0.8, continentalness=0.22, erosion=0.3,
        surface_top="biomesunseen:lumen_grass_block",
        sky_color=0x4A6A4A, fog_color=0x9AB88A, water_color=0x5A9A6A,
        grass_color=0xB8E088, foliage_color=0x98C868,
        trees_per_chunk=8, tree_feature="biomesunseen:lumenshade_trees",
        grass_per_chunk=24, flora_feature="biomesunseen:lumenshade_flora",
        ores=("lumenshade", "root_heart", "glimmerleaf"),
        structures=("biomesunseen:heart_of_the_forest_arena",),
        music="biomesunseen:music.ethereal",
        spawns=(("biomesunseen:grove_warden", 20, 1, 2), ("biomesunseen:mossback_hare", 25, 2, 4)),
        lore="The Heart sleeps under this clearing. It dreams in root and sap."),

    _ow("ghostlight_marsh", "Ghostlight Marsh", "ethereal",
        temperature=0.65, humidity=1.0, continentalness=0.38, erosion=0.65,
        surface_top="biomesunseen:spore_grass_block",
        sky_color=0x1A2A2A, fog_color=0x4A7A6A, water_color=0x2A5A4A,
        grass_color=0x6A9A78, foliage_color=0x588866,
        trees_per_chunk=2, tree_feature="biomesunseen:marsh_trees",
        grass_per_chunk=20, flora_feature="biomesunseen:marsh_flora",
        ores=("wraithsalt", "graveamber", "sporeamber"),
        music="biomesunseen:music.ethereal",
        ambient_sound="biomesunseen:ambient.whisper",
        spawns=(("biomesunseen:mire_wisp", 40, 2, 4), ("biomesunseen:bogcrawler", 25, 1, 3)),
        lore="The lights lead somewhere. They have never once led anywhere good."),

    _ow("aetherveil_reach", "Aetherveil Reach", "ethereal",
        temperature=0.3, humidity=0.4, continentalness=0.6, erosion=0.1,
        surface_top="biomesunseen:aether_grass_block",
        surface_stone="biomesunseen:aetherstone",
        sky_color=0x9AB8E8, fog_color=0xD8E4F8, water_color=0x7AA8E0,
        grass_color=0xB0C8F0, foliage_color=0x90B0E0,
        trees_per_chunk=2, tree_feature="biomesunseen:aetherveil_trees",
        grass_per_chunk=14, flora_feature="biomesunseen:aetherveil_flora",
        ores=("aetherium", "dawnshard", "skylead"),
        structures=("biomesunseen:aetherfall_portal",),
        particle="biomesunseen:aetherveil_mote",
        music="biomesunseen:music.ethereal",
        spawns=(("biomesunseen:veilwing", 25, 1, 3),),
        lore="The ground thins out here. Above it, something is falling upward."),
]


# ===========================================================================
#  COMPACT AUTHORING TABLE
#  The 16 Ethereal biomes above are written long-form as the reference
#  exemplars. The remaining 124 are authored in the same detail but in a
#  compact positional form so the whole table stays auditable in one file.
#
#  Field order:
#    0 id                  8  water_fog
#    1 display name        9  grass colour      (None = vanilla tint)
#    2 temperature        10  foliage colour    (None = vanilla tint)
#    3 humidity           11  surface top
#    4 continentalness    12  surface filler
#    5 erosion            13  surface stone
#    6 depth              14  trees per chunk
#    7 weirdness          15  tree feature
#   16 grass per chunk   24  structures
#   17 flora feature     25  music
#   18 offset            26  ambient sound
#   19 sky colour        27  particle
#   20 fog colour        28  spawns
#   21 water colour      29  lore
#   22 base_height       30  weight
#   23 height_variation
# ===========================================================================

_OW_COMPACT_FIELDS = (
    "id name temperature humidity continentalness erosion depth weirdness offset "
    "sky_color fog_color water_color water_fog_color grass_color foliage_color "
    "surface_top surface_filler surface_stone trees_per_chunk tree_feature "
    "grass_per_chunk flora_feature base_height height_variation structures music "
    "ambient_sound particle spawns lore weight"
).split()

# --- ANCIENT (16) ---------------------------------------------------------
# Petrified, ruined, colossal. Old-growth silhouettes, weathered stone.
_OW_ANCIENT = [
    ("petrified_forest", "Petrified Forest", 0.5, 0.35, 0.35, 0.25, 0.0, 0.1, 0.0,
     0x8A9AA8, 0xC0CCD8, 0x5A7A9A, 0x1A2A3A, 0x9A9A88, 0x7A7A68,
     "biomesunseen:petrified_grass_block", "biomesunseen:petrified_dirt", "biomesunseen:petrified_wood_stone",
     12, "biomesunseen:petrified_trees", 6, "biomesunseen:petrified_flora",
     0.15, 0.25, ("biomesunseen:petrified_colossus",), "biomesunseen:music.ancient",
     None, None, (("biomesunseen:stonehide_boar", 20, 2, 4), ("biomesunseen:fossil_wraith", 15, 1, 1)),
     "A forest that stopped being alive a long time ago and never got the message.", 100),

    ("colossal_boneyard", "Colossal Boneyard", 0.4, 0.2, 0.5, 0.4, 0.0, 0.15, 0.0,
     0x9AA8A0, 0xD0D8CC, 0x6A8A7A, 0x1A2A22, 0xA0A890, 0x808870,
     "biomesunseen:ash_grass_block", "biomesunseen:ashen_dirt", "biomesunseen:ashen_stone",
     0, None, 10, "biomesunseen:boneyard_flora",
     0.1, 0.3, ("biomesunseen:bone_colossus",), "biomesunseen:music.ancient",
     None, None, (("biomesunseen:fossil_wraith", 30, 1, 2), ("biomesunseen:marrow_hound", 20, 2, 3)),
     "Ribcages the size of cathedrals. Something ate whatever built them.", 100),

    ("sunken_temple_reach", "Sunken Temple Reach", 0.75, 0.9, -0.1, 0.5, 0.0, -0.1, 0.0,
     0x4A7A8A, 0x8AB8C0, 0x3A7A8A, 0x0A2A32, 0x6A9A88, 0x4A8070,
     "biomesunseen:tidegrass_block", "biomesunseen:wet_silt", "biomesunseen:sunken_stone",
     2, "biomesunseen:temple_palms", 12, "biomesunseen:temple_flora",
     -0.05, 0.2, ("biomesunseen:sunken_temple",), "biomesunseen:music.ancient",
     None, None, (("biomesunseen:temple_guardian", 20, 1, 1), ("biomesunseen:reefglider", 25, 2, 4)),
     "The altar is still above the waterline. That is the only reason it still works.", 100),

    ("ruined_observatory", "Ruined Observatory", 0.35, 0.3, 0.55, 0.2, 0.05, 0.2, 0.0,
     0x2A3A6A, 0x5A6AA0, 0x3A4A8A, 0x0A1230, 0x7888B0, 0x586898,
     "biomesunseen:crystal_grass_block", "biomesunseen:crystal_dirt", "biomesunseen:twilight_shale",
     1, "biomesunseen:observatory_pillars", 8, "biomesunseen:observatory_flora",
     0.2, 0.35, ("biomesunseen:ruined_observatory",), "biomesunseen:music.ancient",
     None, "biomesunseen:starfall_ember",
     (("biomesunseen:astral_scribe", 15, 1, 1), ("biomesunseen:glimmerwing", 20, 2, 4)),
     "The lens cracked, but it is still pointed at something.", 100),

    ("megalith_moor", "Megalith Moor", 0.45, 0.55, 0.45, 0.35, 0.0, 0.05, 0.0,
     0x6A7A88, 0xA8B8C0, 0x4A6A7A, 0x12202A, 0x7A9A70, 0x5A8050,
     "biomesunseen:mossy_umber_grass", "biomesunseen:umber_dirt", "biomesunseen:umberstone",
     1, "biomesunseen:moor_standing_stones", 18, "biomesunseen:moor_flora",
     0.12, 0.22, ("biomesunseen:megalith_circle",), "biomesunseen:music.ancient",
     "biomesunseen:ambient.wind_low", None,
     (("biomesunseen:moor_sentinel", 18, 1, 1), ("biomesunseen:mossback_hare", 20, 2, 4)),
     "Thirty stones. Thirty-one shadows. It is fine. It is always fine.", 100),

    ("forged_waste", "Forged Waste", 0.8, 0.15, 0.5, 0.45, 0.0, 0.1, 0.0,
     0xA08A6A, 0xD0BC98, 0x8A6A4A, 0x2A1A0A, 0xA89A70, 0x887A50,
     "biomesunseen:ash_grass_block", "biomesunseen:ashen_dirt", "biomesunseen:slag_stone",
     0, None, 4, "biomesunseen:forged_flora",
     0.08, 0.18, ("biomesunseen:fallen_forge",), "biomesunseen:music.ancient",
     None, None, (("biomesunseen:slag_golem", 22, 1, 2),),
     "An armoury that outlived the war, the kingdom, and the reason.", 100),

    ("ancestor_grove", "Ancestor Grove", 0.6, 0.75, 0.3, 0.2, 0.0, 0.0, 0.0,
     0x5A7A5A, 0x9AB890, 0x4A7A5A, 0x0A200A, 0x8AB878, 0x6AA058,
     "biomesunseen:lumen_grass_block", "biomesunseen:lumen_dirt", "biomesunseen:spiritwood_stone",
     9, "biomesunseen:ancestor_trees", 14, "biomesunseen:ancestor_flora",
     0.1, 0.2, ("biomesunseen:ancestor_shrine",), "biomesunseen:music.ancient",
     None, None, (("biomesunseen:grove_warden", 20, 1, 2), ("biomesunseen:fossil_wraith", 25, 2, 4)),
     "Every tree was planted by someone who is buried under it.", 100),

    ("titan_graveyard", "Titan Graveyard", 0.3, 0.25, 0.55, 0.5, 0.05, 0.25, 0.0,
     0x7A8A90, 0xB0BCC0, 0x5A7A8A, 0x142028, 0x8A9A8A, 0x6A7A6A,
     "biomesunseen:ash_grass_block", "biomesunseen:titanite_gravel", "biomesunseen:titanite_block",
     0, None, 6, "biomesunseen:titan_flora",
     0.15, 0.4, ("biomesunseen:titan_remains",), "biomesunseen:music.ancient",
     "biomesunseen:ambient.wind_low", None,
     (("biomesunseen:marrow_hound", 25, 2, 3), ("biomesunseen:fossil_wraith", 20, 1, 2)),
     "The vertebrae are used as shelters now. Nobody comments on the scale.", 100),

    ("old_king_road", "Old King Road", 0.5, 0.4, 0.4, 0.3, 0.0, 0.0, 0.0,
     0x8A98A0, 0xC0C8CC, 0x5A7A8A, 0x141E28, 0x8AA078, 0x6A8858,
     "biomesunseen:umber_grass_block", "biomesunseen:umber_dirt", "biomesunseen:umberstone",
     3, "biomesunseen:roadside_trees", 12, "biomesunseen:road_flora",
     0.1, 0.15, ("biomesunseen:kings_road_ruin", "biomesunseen:waystation"),
     "biomesunseen:music.ancient", None, None,
     (("biomesunseen:roadwarden", 15, 1, 1), ("biomesunseen:stonehide_boar", 20, 2, 4)),
     "Still paved. Still patrolled. The patrol has been dead for four hundred years.", 100),

    ("petrified_colossi", "Petrified Colossi", 0.4, 0.2, 0.5, 0.35, 0.1, 0.2, 0.0,
     0x9A9080, 0xC8BCA8, 0x6A6A5A, 0x1A1810, 0x9A9478, 0x7A7458,
     "biomesunseen:petrified_grass_block", "biomesunseen:petrified_dirt", "biomesunseen:petrified_wood_stone",
     2, "biomesunseen:colossi_petrified_trees", 5, "biomesunseen:colossi_flora",
     0.3, 0.5, ("biomesunseen:petrified_colossus",), "biomesunseen:music.ancient",
     None, None, (("biomesunseen:stonehide_boar", 18, 2, 4), ("biomesunseen:fossil_wraith", 20, 1, 2)),
     "They were walking when it happened. They are still walking, slowly.", 100),

    ("hieroglyph_canyon", "Hieroglyph Canyon", 0.7, 0.15, 0.6, 0.7, -0.1, 0.1, 0.0,
     0xB09878, 0xD8C4A0, 0x7A8A6A, 0x201A0A, 0xA09070, 0x807050,
     "biomesunseen:sunbleached_sand", "biomesunseen:sunbleached_stone", "biomesunseen:sunbleached_stone",
     0, None, 3, "biomesunseen:canyon_flora",
     -0.2, 0.6, ("biomesunseen:hieroglyph_wall",), "biomesunseen:music.ancient",
     None, None, (("biomesunseen:canyon_skulk", 22, 1, 2),),
     "The carvings are a warning. The warning is repeated, increasingly urgently.", 100),

    ("bronze_steppe", "Bronze Steppe", 0.55, 0.3, 0.55, 0.4, 0.0, 0.05, 0.0,
     0xB0A078, 0xD8CCA8, 0x7A8A6A, 0x1A1808, 0xB0A870, 0x908850,
     "biomesunseen:umber_grass_block", "biomesunseen:umber_dirt", "biomesunseen:rootiron_stone",
     1, "biomesunseen:steppe_scrub", 20, "biomesunseen:steppe_flora",
     0.1, 0.2, ("biomesunseen:bronze_barrow",), "biomesunseen:music.ancient",
     "biomesunseen:ambient.wind_low", None,
     (("biomesunseen:steppe_rider", 20, 2, 4), ("biomesunseen:stonehide_boar", 15, 2, 3)),
     "Grass to the horizon and bronze under every spadeful of it.", 100),

    ("shattered_archive", "Shattered Archive", 0.45, 0.35, 0.35, 0.45, 0.05, 0.3, 0.0,
     0x6A6A8A, 0xA0A0C0, 0x4A4A7A, 0x10102A, 0x8888A8, 0x686888,
     "biomesunseen:ash_grass_block", "biomesunseen:parchment_silt", "biomesunseen:gloomslate",
     0, None, 8, "biomesunseen:archive_flora",
     0.05, 0.35, ("biomesunseen:shattered_archive",), "biomesunseen:music.ancient",
     None, "biomesunseen:page_drift",
     (("biomesunseen:astral_scribe", 25, 1, 2),),
     "Every book in the realm, buried in one bad afternoon.", 100),

    ("rootdeep_hollow", "Rootdeep Hollow", 0.55, 0.8, 0.25, 0.55, -0.15, 0.1, 0.0,
     0x3A4A3A, 0x6A7A60, 0x2A4A3A, 0x08140A, 0x5A8A48, 0x3A6A28,
     "biomesunseen:spore_grass_block", "biomesunseen:root_loam", "biomesunseen:rootiron_stone",
     14, "biomesunseen:rootdeep_trees", 12, "biomesunseen:rootdeep_flora",
     -0.1, 0.4, ("biomesunseen:rootdeep_chamber",), "biomesunseen:music.ancient",
     None, None, (("biomesunseen:rootburrower", 22, 1, 3), ("biomesunseen:grove_warden", 15, 1, 1)),
     "The roots came first. The forest is just what they grew to hold.", 100),

    ("ashen_necropolis", "Ashen Necropolis", 0.35, 0.2, 0.45, 0.4, 0.0, 0.2, 0.0,
     0x5A5A5A, 0x8A8A88, 0x3A4A4A, 0x0A0E0E, 0x6A6A60, 0x4A4A40,
     "biomesunseen:ash_grass_block", "biomesunseen:ashen_dirt", "biomesunseen:ashen_stone",
     1, "biomesunseen:necropolis_cypress", 4, "biomesunseen:necropolis_flora",
     0.12, 0.28, ("biomesunseen:necropolis_gate", "biomesunseen:crypt"),
     "biomesunseen:music.ancient", "biomesunseen:ambient.ash_wind", None,
     (("biomesunseen:fossil_wraith", 35, 1, 3), ("biomesunseen:marrow_hound", 25, 2, 4)),
     "It is not haunted. Haunting implies somebody is still trying.", 100),

    ("monolith_shore", "Monolith Shore", 0.5, 0.75, -0.3, 0.3, 0.0, -0.05, 0.0,
     0x7A9AB0, 0xB0C8D8, 0x3A6A8A, 0x0A1A2A, 0x7A9A80, 0x5A8060,
     "biomesunseen:tidegrass_block", "biomesunseen:wet_silt", "biomesunseen:sunken_stone",
     0, None, 8, "biomesunseen:shore_flora",
     0.0, 0.15, ("biomesunseen:monolith_row",), "biomesunseen:music.ancient",
     "biomesunseen:ambient.surf", None,
     (("biomesunseen:shorelurker", 20, 1, 2), ("biomesunseen:reefglider", 20, 2, 4)),
     "Standing stones at the tideline, arranged to be read from the sea.", 100),
]

# --- VIBRANT (16) ---------------------------------------------------------
# Saturated, high-energy, densely featured. The showcase biomes.
_OW_VIBRANT = [
    ("primal_savanna", "Primal Savanna", 0.95, 0.15, 0.55, 0.4, 0.0, 0.0, 0.0,
     0x8AC0E8, 0xD8E8F0, 0x4A90C0, 0x0A2030, 0xC8B060, 0xA89040,
     "biomesunseen:sunbleached_grass_block", "biomesunseen:sunbleached_dirt", "biomesunseen:sunbleached_stone",
     3, "biomesunseen:savanna_acacia_giants", 24, "biomesunseen:savanna_flora",
     0.1, 0.2, ("biomesunseen:savanna_baobab_village",), "biomesunseen:music.vibrant",
     None, None, (("biomesunseen:savanna_strider", 25, 3, 6), ("biomesunseen:primal_cat", 20, 1, 3)),
     "Grass the colour of old brass and predators in all of it.", 120),

    ("bloomfield", "Bloomfield", 0.75, 0.7, 0.3, 0.45, 0.0, -0.05, 0.0,
     0x7AB8E8, 0xC8E0F0, 0x4A90D0, 0x0A1E30, 0x90D070, 0x70B850,
     "biomesunseen:lumen_grass_block", "biomesunseen:lumen_dirt", "biomesunseen:verdant_stone",
     2, "biomesunseen:bloomfield_oaks", 32, "biomesunseen:bloomfield_flora",
     0.08, 0.15, ("biomesunseen:bloomfield_farmstead",), "biomesunseen:music.vibrant",
     None, "biomesunseen:pollen_drift",
     (("biomesunseen:petaldancer", 35, 3, 6), ("biomesunseen:mossback_hare", 25, 2, 4)),
     "Flowers that out-compete the grass and then each other.", 120),

    ("coral_shallows", "Coral Shallows", 0.85, 0.95, -0.25, 0.5, -0.05, -0.1, 0.0,
     0x6AB8D8, 0xB0E0E8, 0x3AB8D0, 0x083040, 0x70C898, 0x50B078,
     "biomesunseen:tidegrass_block", "biomesunseen:wet_silt", "biomesunseen:coralite_block",
     1, "biomesunseen:shallows_palm", 14, "biomesunseen:coral_flora",
     -0.1, 0.15, ("biomesunseen:coral_arch",), "biomesunseen:music.vibrant",
     "biomesunseen:ambient.surf", None,
     (("biomesunseen:reefglider", 40, 3, 6), ("biomesunseen:coralback_crab", 25, 2, 4)),
     "Water clear enough to read the reef like a page.", 120),

    ("amberwood", "Amberwood", 0.65, 0.6, 0.35, 0.25, 0.0, 0.05, 0.0,
     0xB09858, 0xE0C888, 0x7A8A4A, 0x1A1A08, 0xC0A850, 0xA08830,
     "biomesunseen:umber_grass_block", "biomesunseen:amber_loam", "biomesunseen:sporeamber_stone",
     11, "biomesunseen:amberwood_trees", 12, "biomesunseen:amberwood_flora",
     0.12, 0.22, ("biomesunseen:amberwood_hollow",), "biomesunseen:music.vibrant",
     None, "biomesunseen:pollen_drift",
     (("biomesunseen:amber_sentinel", 18, 1, 2), ("biomesunseen:mossback_hare", 25, 2, 4)),
     "Sap runs gold here and the whole forest smells of it.", 120),

    ("sunscorch_badlands", "Sunscorch Badlands", 1.1, 0.05, 0.6, 0.55, 0.05, 0.1, 0.0,
     0xC8A878, 0xE8D0A0, 0x8A9A6A, 0x201808, 0xB09858, 0x907838,
     "biomesunseen:sunbleached_sand", "biomesunseen:sunscorch_hardpan", "biomesunseen:sunscorch_stone",
     0, None, 2, "biomesunseen:badlands_flora",
     0.15, 0.35, ("biomesunseen:sunscorch_outpost",), "biomesunseen:music.vibrant",
     None, "biomesunseen:heat_shimmer",
     (("biomesunseen:canyon_skulk", 25, 1, 2), ("biomesunseen:sunscorch_vulture", 20, 1, 3)),
     "The heat makes the horizon lie to you. It is extremely good at it.", 120),

    ("orchid_lagoon", "Orchid Lagoon", 0.85, 1.0, -0.1, 0.6, 0.0, -0.05, 0.0,
     0x7AC0D8, 0xC0E8F0, 0x40B0C8, 0x083848, 0x80D098, 0x60B878,
     "biomesunseen:tidegrass_block", "biomesunseen:wet_silt", "biomesunseen:bloomglass_stone",
     4, "biomesunseen:lagoon_mangrove", 26, "biomesunseen:orchid_flora",
     -0.05, 0.2, ("biomesunseen:lagoon_platform",), "biomesunseen:music.vibrant",
     "biomesunseen:ambient.surf", "biomesunseen:pollen_drift",
     (("biomesunseen:reefglider", 30, 2, 5), ("biomesunseen:orchid_mantis", 20, 1, 1)),
     "Every colour the game knows, arguing in one shallow bay.", 120),

    ("verdantheight", "Verdantheight", 0.6, 0.85, 0.2, 0.75, 0.15, 0.1, 0.0,
     0x6AB0D8, 0xB0D8E8, 0x3A8AC0, 0x0A2438, 0x70C868, 0x50A848,
     "biomesunseen:lumen_grass_block", "biomesunseen:lumen_dirt", "biomesunseen:verdant_stone",
     13, "biomesunseen:verdantheight_jungle", 30, "biomesunseen:verdantheight_flora",
     0.35, 0.55, ("biomesunseen:verdantheight_ruin",), "biomesunseen:music.vibrant",
     None, None, (("biomesunseen:canopy_glider", 25, 2, 4), ("biomesunseen:silkweaver", 20, 2, 3)),
     "Terraced jungle so steep the rain arrives sideways.", 120),

    ("marigold_march", "Marigold March", 0.7, 0.65, 0.45, 0.35, 0.0, 0.0, 0.0,
     0x8AC0E0, 0xD0E4F0, 0x4A90C8, 0x0A2030, 0xD8C050, 0xB8A030,
     "biomesunseen:lumen_grass_block", "biomesunseen:lumen_dirt", "biomesunseen:umberstone",
     2, "biomesunseen:march_oaks", 34, "biomesunseen:marigold_flora",
     0.1, 0.18, ("biomesunseen:march_watchtower",), "biomesunseen:music.vibrant",
     None, "biomesunseen:pollen_drift",
     (("biomesunseen:petaldancer", 30, 3, 6), ("biomesunseen:roadwarden", 12, 1, 1)),
     "A borderland that grew flowers over the argument.", 120),

    ("pyroclast_fields", "Pyroclast Fields", 1.3, 0.1, 0.5, 0.5, 0.05, 0.15, 0.0,
     0x6A3A2A, 0xA05A38, 0x8A3A1A, 0x280A02, 0x8A5A38, 0x6A4028,
     "biomesunseen:ash_grass_block", "biomesunseen:ashen_dirt", "biomesunseen:pyroclast_stone",
     0, None, 3, "biomesunseen:pyroclast_flora",
     0.1, 0.4, ("biomesunseen:pyroclast_vent",), "biomesunseen:music.vibrant",
     "biomesunseen:ambient.ember", "biomesunseen:ember_drift",
     (("biomesunseen:emberling", 30, 2, 4), ("biomesunseen:slag_golem", 15, 1, 1)),
     "Cracked basalt, and something under every crack that is still hot.", 120),

    ("tideglass_bay", "Tideglass Bay", 0.8, 0.9, -0.35, 0.4, 0.0, -0.1, 0.0,
     0x70B8D8, 0xB8E0E8, 0x38B8D0, 0x083444, 0x78C898, 0x58B078,
     "biomesunseen:tide_sand", "biomesunseen:wet_silt", "biomesunseen:tideglass_block",
     1, "biomesunseen:bay_palm", 10, "biomesunseen:bay_flora",
     -0.08, 0.12, ("biomesunseen:tideglass_pavilion",), "biomesunseen:music.vibrant",
     "biomesunseen:ambient.surf", None,
     (("biomesunseen:reefglider", 35, 3, 6), ("biomesunseen:shorelurker", 18, 1, 2)),
     "The sand has fused to glass in sheets. The tide polishes it daily.", 120),

    ("glimmerleaf_woodland", "Glimmerleaf Woodland", 0.7, 0.8, 0.28, 0.22, 0.0, 0.05, 0.0,
     0x6AA878, 0xA8D8A8, 0x3A8A5A, 0x082414, 0x90D070, 0x70B850,
     "biomesunseen:lumen_grass_block", "biomesunseen:lumen_dirt", "biomesunseen:glimmerleaf_stone",
     12, "biomesunseen:glimmerleaf_trees", 20, "biomesunseen:glimmerleaf_flora",
     0.12, 0.24, ("biomesunseen:woodland_cairn",), "biomesunseen:music.vibrant",
     None, "biomesunseen:lumen_mote",
     (("biomesunseen:glimmerwing", 45, 3, 6), ("biomesunseen:thicket_sprite", 20, 1, 2)),
     "Leaves that hold light for an hour after sunset.", 120),

    ("sakura_highlands", "Sakura Highlands", 0.6, 0.65, 0.5, 0.3, 0.1, 0.05, 0.0,
     0x8AB8E0, 0xD8E4F0, 0x4A90C8, 0x0A2030, 0xE0A8C0, 0xC888A8,
     "biomesunseen:lumen_grass_block", "biomesunseen:lumen_dirt", "biomesunseen:bloomglass_stone",
     10, "biomesunseen:sakura_trees", 18, "biomesunseen:sakura_flora",
     0.25, 0.4, ("biomesunseen:sakura_torii",), "biomesunseen:music.vibrant",
     None, "biomesunseen:moonpetal_drift",
     (("biomesunseen:petaldancer", 30, 2, 5), ("biomesunseen:highland_goat", 20, 2, 4)),
     "Pink for six weeks a year and unforgettable for the other forty-six.", 120),

    ("sunspore_barrens", "Sunspore Barrens", 1.0, 0.25, 0.55, 0.45, 0.0, 0.05, 0.0,
     0xC0A868, 0xE0D098, 0x8A8A4A, 0x1A1808, 0xB8A848, 0x988828,
     "biomesunseen:spore_grass_block", "biomesunseen:spore_sand", "biomesunseen:sunspore_stone",
     1, "biomesunseen:barrens_scrub", 16, "biomesunseen:sunspore_flora",
     0.1, 0.25, ("biomesunseen:barrens_obelisk",), "biomesunseen:music.vibrant",
     None, "biomesunseen:pollen_drift",
     (("biomesunseen:sporeling", 35, 3, 6), ("biomesunseen:sunscorch_vulture", 18, 1, 3)),
     "Spore-drifts deep enough to lose a boot in, and the boot.", 120),

    ("emberfall_ridge", "Emberfall Ridge", 0.9, 0.3, 0.65, 0.7, 0.2, 0.2, 0.0,
     0x8A5A3A, 0xC08A58, 0x6A5A3A, 0x1A0E04, 0xA07A40, 0x805A20,
     "biomesunseen:ash_grass_block", "biomesunseen:ashen_dirt", "biomesunseen:emberquartz_stone",
     1, "biomesunseen:emberfall_pines", 6, "biomesunseen:emberfall_flora",
     0.4, 0.6, ("biomesunseen:emberfall_watchtower",), "biomesunseen:music.vibrant",
     None, "biomesunseen:ember_drift",
     (("biomesunseen:emberling", 28, 2, 4), ("biomesunseen:canyon_skulk", 18, 1, 2)),
     "Autumn that caught fire and has been burning ever since.", 120),

    ("jewel_reef", "Jewel Reef", 0.8, 1.0, -0.4, 0.5, -0.1, -0.15, 0.0,
     0x60B0D8, 0xA8E0E8, 0x30B0D0, 0x063040, 0x70D0A0, 0x50B880,
     "biomesunseen:tide_sand", "biomesunseen:wet_silt", "biomesunseen:coralite_block",
     0, None, 8, "biomesunseen:jewel_reef_flora",
     -0.2, 0.2, ("biomesunseen:jewel_reef_arch",), "biomesunseen:music.vibrant",
     "biomesunseen:ambient.underwater", None,
     (("biomesunseen:reefglider", 45, 4, 8), ("biomesunseen:coralback_crab", 30, 2, 5)),
     "So much colour the fish have started matching it on purpose.", 120),

    ("harvest_hollows", "Harvest Hollows", 0.65, 0.6, 0.4, 0.4, 0.0, 0.0, 0.0,
     0x8AC0E0, 0xD0E0E8, 0x4A90C0, 0x0A2030, 0xC0B060, 0xA09040,
     "biomesunseen:umber_grass_block", "biomesunseen:umber_dirt", "biomesunseen:rootiron_stone",
     4, "biomesunseen:hollows_orchard", 26, "biomesunseen:harvest_flora",
     0.1, 0.2, ("biomesunseen:harvest_barn", "biomesunseen:waystation"),
     "biomesunseen:music.vibrant", None, None,
     (("biomesunseen:highland_goat", 25, 2, 5), ("biomesunseen:stonehide_boar", 20, 2, 4)),
     "Terraced, planted, and abandoned mid-harvest. The crop is still coming in.", 120),
]

# --- HARSH (16) -----------------------------------------------------------
# Extreme climate, sparse cover, high danger.
_OW_HARSH = [
    ("volcanic_wasteland", "Volcanic Wasteland", 1.6, 0.05, 0.5, 0.6, 0.1, 0.2, 0.0,
     0x4A1A0A, 0x8A3A18, 0x8A2A0A, 0x280802, 0x6A3A20, 0x4A2410,
     "biomesunseen:ash_grass_block", "biomesunseen:ashen_dirt", "biomesunseen:pyroclast_stone",
     0, None, 1, "biomesunseen:volcanic_flora",
     0.2, 0.6, ("biomesunseen:volcanic_vent_field",), "biomesunseen:music.harsh",
     "biomesunseen:ambient.ember", "biomesunseen:ember_drift",
     (("biomesunseen:emberling", 35, 2, 5), ("biomesunseen:magma_lurker", 25, 1, 2)),
     "The sky is the ground here. Both of them are on fire.", 100),

    ("frozen_expanse", "Frozen Expanse", -0.6, 0.3, 0.6, 0.3, 0.0, 0.0, 0.0,
     0xA8D0E8, 0xE0F0F8, 0x5A9AC8, 0x0A2038, 0xB0D0D8, 0x90B8C0,
     "biomesunseen:crystal_grass_block", "biomesunseen:frost_silt", "biomesunseen:glacierite_block",
     0, None, 2, "biomesunseen:frozen_flora",
     0.08, 0.2, ("biomesunseen:frozen_waystation",), "biomesunseen:music.harsh",
     "biomesunseen:ambient.wind_high", None,
     (("biomesunseen:frostling", 30, 2, 4), ("biomesunseen:glacier_ox", 18, 2, 5)),
     "Flat, white, and completely without places to hide.", 100),

    ("scorched_glassland", "Scorched Glassland", 1.4, 0.02, 0.55, 0.5, 0.0, 0.15, 0.0,
     0xB8A898, 0xE0D8C8, 0x8A8A7A, 0x1A1810, 0xA09878, 0x807858,
     "biomesunseen:tideglass_sand", "biomesunseen:scorched_hardpan", "biomesunseen:tideglass_block",
     0, None, 0, "biomesunseen:glassland_flora",
     0.05, 0.25, ("biomesunseen:glassland_spire",), "biomesunseen:music.harsh",
     None, "biomesunseen:heat_shimmer",
     (("biomesunseen:canyon_skulk", 28, 1, 2), ("biomesunseen:sunscorch_vulture", 22, 1, 3)),
     "Sand fused to a mirror by something that passed overhead once.", 100),

    ("blighted_marches", "Blighted Marches", 0.5, 0.85, 0.35, 0.55, -0.05, 0.1, 0.0,
     0x4A5A3A, 0x7A8A60, 0x3A5A3A, 0x0A140A, 0x6A7A40, 0x4A5A28,
     "biomesunseen:blight_grass_block", "biomesunseen:blight_loam", "biomesunseen:witherite_stone",
     2, "biomesunseen:blighted_trees", 8, "biomesunseen:blight_flora",
     0.0, 0.3, ("biomesunseen:blight_pit",), "biomesunseen:music.harsh",
     "biomesunseen:ambient.blight", None,
     (("biomesunseen:blighthound", 30, 1, 3), ("biomesunseen:rotstalker", 22, 1, 2)),
     "The plants are not dead. That would be simpler.", 100),

    ("howling_peaks", "Howling Peaks", 0.1, 0.35, 0.75, 0.85, 0.35, 0.25, 0.0,
     0x7A98B0, 0xB8CCD8, 0x4A7A9A, 0x0A1A28, 0x7A9878, 0x5A7858,
     "biomesunseen:ash_grass_block", "biomesunseen:titanite_gravel", "biomesunseen:titanite_block",
     0, None, 2, "biomesunseen:peak_flora",
     0.6, 0.8, ("biomesunseen:peak_aerie",), "biomesunseen:music.harsh",
     "biomesunseen:ambient.wind_high", None,
     (("biomesunseen:highland_goat", 25, 2, 4), ("biomesunseen:gale_harrier", 20, 1, 2)),
     "The wind has cut the rock into shapes that sound like voices.", 100),

    ("saltflat_mirage", "Saltflat Mirage", 1.15, 0.05, 0.6, 0.25, 0.0, 0.05, 0.0,
     0xC8D0D8, 0xE8EEF0, 0x8AA0B0, 0x182028, 0xB0B8A8, 0x909888,
     "biomesunseen:salt_crust", "biomesunseen:salt_flat_hardpan", "biomesunseen:wraithsalt_block",
     0, None, 0, "biomesunseen:saltflat_flora",
     0.0, 0.05, ("biomesunseen:saltflat_caravan",), "biomesunseen:music.harsh",
     None, "biomesunseen:heat_shimmer",
     (("biomesunseen:sunscorch_vulture", 25, 1, 3),),
     "Water on the horizon for eleven days. There is no water.", 100),

    ("grave_ice_field", "Grave Ice Field", -0.8, 0.4, 0.5, 0.45, 0.0, 0.1, 0.0,
     0x90B0C8, 0xD0E4F0, 0x4A8AB8, 0x0A1E30, 0x9AB8C0, 0x7A9AA8,
     "biomesunseen:crystal_grass_block", "biomesunseen:frost_silt", "biomesunseen:glacierite_block",
     0, None, 1, "biomesunseen:graveice_flora",
     0.1, 0.25, ("biomesunseen:grave_ice_shipwreck",), "biomesunseen:music.harsh",
     "biomesunseen:ambient.wind_high", None,
     (("biomesunseen:frostling", 30, 2, 4), ("biomesunseen:frozen_mariner", 12, 1, 1)),
     "Ships, intact, held upright, going nowhere, permanently.", 100),

    ("sulphur_vents", "Sulphur Vents", 1.25, 0.35, 0.45, 0.55, 0.0, 0.2, 0.0,
     0x9AA058, 0xC8C878, 0x7A8A3A, 0x1A1C08, 0xA0A850, 0x808830,
     "biomesunseen:ash_grass_block", "biomesunseen:sulphur_crust", "biomesunseen:pyroclast_stone",
     0, None, 2, "biomesunseen:sulphur_flora",
     0.05, 0.35, ("biomesunseen:sulphur_vent_cluster",), "biomesunseen:music.harsh",
     "biomesunseen:ambient.ember", "biomesunseen:heat_shimmer",
     (("biomesunseen:emberling", 30, 2, 4), ("biomesunseen:magma_lurker", 20, 1, 2)),
     "The ground breathes out and everything within a hundred blocks knows it.", 100),

    ("witherwood", "Witherwood", 0.45, 0.5, 0.3, 0.3, 0.0, 0.15, 0.0,
     0x5A5A60, 0x8A8A90, 0x3A4A4A, 0x0A0E12, 0x6A6A58, 0x4A4A38,
     "biomesunseen:blight_grass_block", "biomesunseen:blight_loam", "biomesunseen:witherite_stone",
     10, "biomesunseen:witherwood_trees", 3, "biomesunseen:witherwood_flora",
     0.1, 0.25, ("biomesunseen:witherwood_gallows",), "biomesunseen:music.harsh",
     "biomesunseen:ambient.blight", None,
     (("biomesunseen:blighthound", 28, 1, 3), ("biomesunseen:rotstalker", 25, 1, 2)),
     "Standing deadwood, black, and every branch points at you.", 100),

    ("ironstone_ravine", "Ironstone Ravine", 0.5, 0.25, 0.55, 0.85, -0.2, 0.2, 0.0,
     0x8A7A6A, 0xB8A898, 0x5A6A7A, 0x141A20, 0x8A8060, 0x6A6040,
     "biomesunseen:umber_grass_block", "biomesunseen:umber_dirt", "biomesunseen:rootiron_stone",
     1, "biomesunseen:ravine_pines", 5, "biomesunseen:ravine_flora",
     -0.3, 0.7, ("biomesunseen:ravine_bridge",), "biomesunseen:music.harsh",
     "biomesunseen:ambient.wind_low", None,
     (("biomesunseen:canyon_skulk", 28, 1, 2), ("biomesunseen:stonehide_boar", 18, 2, 3)),
     "Cut straight down for two hundred blocks by water that has since given up.", 100),

    ("cinder_dunes", "Cinder Dunes", 1.35, 0.03, 0.5, 0.4, 0.0, 0.1, 0.0,
     0x6A4A3A, 0xA07A5A, 0x5A4A3A, 0x140C06, 0x7A5A3A, 0x5A3A20,
     "biomesunseen:cinder_sand", "biomesunseen:cinder_sand", "biomesunseen:ashen_core_stone",
     0, None, 1, "biomesunseen:cinder_flora",
     0.15, 0.3, ("biomesunseen:cinder_oasis",), "biomesunseen:music.harsh",
     None, "biomesunseen:ember_drift",
     (("biomesunseen:emberling", 30, 2, 4), ("biomesunseen:sunscorch_vulture", 20, 1, 3)),
     "Ash drifted into dunes that move like sand and burn like coals.", 100),

    ("glacier_maw", "Glacier Maw", -0.7, 0.5, 0.65, 0.8, -0.15, 0.15, 0.0,
     0x80A8C8, 0xC0DCE8, 0x3A7AA8, 0x082038, 0x8AB0C0, 0x6A90A8,
     "biomesunseen:crystal_grass_block", "biomesunseen:frost_silt", "biomesunseen:glacierite_block",
     0, None, 1, "biomesunseen:glacier_flora",
     -0.1, 0.65, ("biomesunseen:glacier_cave_mouth",), "biomesunseen:music.harsh",
     "biomesunseen:ambient.wind_high", None,
     (("biomesunseen:frostling", 32, 2, 5), ("biomesunseen:glacier_ox", 15, 2, 4)),
     "A cave mouth that exhales. It is warm air. It should not be warm air.", 100),

    ("stormback_steppe", "Stormback Steppe", 0.55, 0.55, 0.6, 0.3, 0.0, -0.1, 0.0,
     0x5A6A7A, 0x90A0B0, 0x3A5A7A, 0x0A1420, 0x7A9A6A, 0x5A7A4A,
     "biomesunseen:umber_grass_block", "biomesunseen:umber_dirt", "biomesunseen:stormcell_stone",
     1, "biomesunseen:steppe_scrub", 18, "biomesunseen:stormback_flora",
     0.12, 0.22, ("biomesunseen:stormback_lightning_scar",), "biomesunseen:music.harsh",
     "biomesunseen:ambient.wind_low", None,
     (("biomesunseen:steppe_rider", 22, 2, 5), ("biomesunseen:gale_harrier", 18, 1, 2)),
     "The storm arrives every afternoon and leaves by dark. It has a schedule.", 100),

    ("obsidian_shelf", "Obsidian Shelf", 0.9, 0.2, -0.15, 0.5, 0.0, 0.2, 0.0,
     0x2A2A32, 0x4A4A55, 0x1A2A3A, 0x060A12, 0x4A4A48, 0x2A2A28,
     "biomesunseen:ash_grass_block", "biomesunseen:obsidian_grit", "biomesunseen:null_basalt",
     0, None, 0, "biomesunseen:obsidian_flora",
     0.0, 0.35, ("biomesunseen:obsidian_shelf_spire",), "biomesunseen:music.harsh",
     "biomesunseen:ambient.wind_low", None,
     (("biomesunseen:magma_lurker", 25, 1, 2), ("biomesunseen:slag_golem", 18, 1, 1)),
     "New land, still black, still sharp, still cooling.", 100),

    ("ashen_caldera", "Ashen Caldera", 1.5, 0.15, 0.4, 0.7, 0.25, 0.25, 0.0,
     0x5A3A2A, 0x9A6A48, 0x6A4A2A, 0x180C04, 0x7A5A30, 0x5A3A18,
     "biomesunseen:ash_grass_block", "biomesunseen:ashen_dirt", "biomesunseen:ashen_core_stone",
     0, None, 1, "biomesunseen:caldera_flora",
     0.45, 0.7, ("biomesunseen:caldera_arena",), "biomesunseen:music.harsh",
     "biomesunseen:ambient.ember", "biomesunseen:ember_drift",
     (("biomesunseen:emberling", 32, 2, 5), ("biomesunseen:magma_lurker", 25, 1, 3)),
     "The crater of something that erupted once and has been waiting since.", 100),

    ("rimeforest", "Rimeforest", -0.4, 0.55, 0.4, 0.25, 0.0, 0.05, 0.0,
     0x90B8D0, 0xD0E8F0, 0x5A98C0, 0x0A2438, 0x9AC0C8, 0x7AA8B0,
     "biomesunseen:crystal_grass_block", "biomesunseen:frost_silt", "biomesunseen:frostvein_stone",
     11, "biomesunseen:rimeforest_pines", 4, "biomesunseen:rime_flora",
     0.15, 0.3, ("biomesunseen:rimeforest_shrine",), "biomesunseen:music.harsh",
     "biomesunseen:ambient.wind_high", None,
     (("biomesunseen:frostling", 28, 2, 4), ("biomesunseen:rime_stag", 15, 1, 3)),
     "Every needle coated in ice, and the forest is somehow still growing.", 100),
]

# --- AQUATIC (16) ---------------------------------------------------------
# Water-dominant: rivers, reefs, trenches, flooded ruins.
_OW_AQUATIC = [
    ("abyssal_trench", "Abyssal Trench", 0.3, 1.0, -0.6, 0.7, -0.6, -0.2, 0.0,
     0x10203A, 0x1A3050, 0x0A1830, 0x02060E, 0x2A5A5A, 0x1A4A4A,
     "biomesunseen:abyssal_silt", "biomesunseen:abyssal_silt", "biomesunseen:abyssite_block",
     0, None, 3, "biomesunseen:abyssal_flora",
     -0.6, 0.4, ("biomesunseen:abyssal_vent",), "biomesunseen:music.aquatic",
     "biomesunseen:ambient.deep_water", None,
     (("biomesunseen:trench_angler", 30, 1, 2), ("biomesunseen:abyssal_leviathan", 5, 1, 1)),
     "Deeper than the map is willing to admit.", 90),

    ("kelp_cathedral", "Kelp Cathedral", 0.7, 1.0, -0.3, 0.5, -0.2, -0.1, 0.0,
     0x3A7A6A, 0x6AB098, 0x2A7A6A, 0x062420, 0x50A878, 0x308858,
     "biomesunseen:tide_sand", "biomesunseen:wet_silt", "biomesunseen:kelpstone_block",
     0, None, 6, "biomesunseen:kelp_cathedral_flora",
     -0.25, 0.25, ("biomesunseen:kelp_cathedral_arch",), "biomesunseen:music.aquatic",
     "biomesunseen:ambient.underwater", None,
     (("biomesunseen:reefglider", 35, 3, 6), ("biomesunseen:kelp_serpent", 12, 1, 1)),
     "Kelp forty blocks tall, in rows, like columns. It was not planted.", 100),

    ("tidal_flats", "Tidal Flats", 0.75, 0.95, -0.2, 0.3, 0.0, -0.05, 0.0,
     0x8AB8D0, 0xC8E0E8, 0x4A98C0, 0x0A2434, 0x8AB898, 0x6A9878,
     "biomesunseen:tide_sand", "biomesunseen:wet_silt", "biomesunseen:tideglass_block",
     0, None, 5, "biomesunseen:tidal_flora",
     -0.05, 0.08, ("biomesunseen:tidal_weir",), "biomesunseen:music.aquatic",
     "biomesunseen:ambient.surf", None,
     (("biomesunseen:coralback_crab", 35, 2, 5), ("biomesunseen:shorelurker", 22, 1, 2)),
     "Twice a day the sea gives it back, and twice a day it is a different shape.", 110),

    ("river_of_lights", "River of Lights", 0.6, 0.9, -0.05, 0.4, 0.0, 0.0, 0.0,
     0x2A4A6A, 0x5A8AB0, 0x2A7AB0, 0x061A30, 0x70B0A0, 0x509080,
     "biomesunseen:tide_sand", "biomesunseen:wet_silt", "biomesunseen:petrichorite_stone",
     2, "biomesunseen:riverside_willows", 14, "biomesunseen:river_flora",
     -0.05, 0.1, ("biomesunseen:river_lantern_pier",), "biomesunseen:music.aquatic",
     "biomesunseen:ambient.stream", "biomesunseen:lumen_mote",
     (("biomesunseen:reefglider", 30, 2, 5), ("biomesunseen:river_lamprey", 20, 2, 4)),
     "The water glows at night and nobody has ever found out why.", 110),

    ("flooded_ruins", "Flooded Ruins", 0.7, 0.95, -0.15, 0.55, -0.05, -0.05, 0.0,
     0x5A8A9A, 0x90BCC8, 0x3A7A8A, 0x08202A, 0x70A088, 0x508068,
     "biomesunseen:tidegrass_block", "biomesunseen:wet_silt", "biomesunseen:sunken_stone",
     1, "biomesunseen:ruins_palm", 8, "biomesunseen:flooded_flora",
     -0.15, 0.25, ("biomesunseen:flooded_temple", "biomesunseen:sunken_temple"),
     "biomesunseen:music.aquatic", "biomesunseen:ambient.underwater", None,
     (("biomesunseen:temple_guardian", 22, 1, 2), ("biomesunseen:reefglider", 25, 2, 4)),
     "A city that lost an argument with the sea and is losing slowly.", 100),

    ("coral_atoll_ring", "Coral Atoll Ring", 0.85, 1.0, -0.45, 0.35, 0.0, -0.15, 0.0,
     0x70C0D8, 0xB8E8F0, 0x38B8D0, 0x083848, 0x78D0A0, 0x58B880,
     "biomesunseen:tide_sand", "biomesunseen:wet_silt", "biomesunseen:coralite_block",
     3, "biomesunseen:atoll_palm", 10, "biomesunseen:atoll_ring_flora",
     -0.1, 0.12, ("biomesunseen:atoll_ruin", "biomesunseen:coral_arch"),
     "biomesunseen:music.aquatic", "biomesunseen:ambient.surf", None,
     (("biomesunseen:reefglider", 40, 3, 6), ("biomesunseen:coralback_crab", 28, 2, 5)),
     "A perfect ring of reef around a perfect circle of nothing.", 100),

    ("brine_marsh", "Brine Marsh", 0.8, 1.0, -0.1, 0.65, -0.05, 0.05, 0.0,
     0x5A7A6A, 0x90B0A0, 0x3A6A5A, 0x0A1E18, 0x6A9A70, 0x4A7A50,
     "biomesunseen:tidegrass_block", "biomesunseen:brine_mud", "biomesunseen:wraithsalt_block",
     1, "biomesunseen:marsh_trees", 16, "biomesunseen:brine_flora",
     -0.05, 0.15, ("biomesunseen:brine_hut",), "biomesunseen:music.aquatic",
     "biomesunseen:ambient.stream", None,
     (("biomesunseen:bogcrawler", 30, 2, 4), ("biomesunseen:river_lamprey", 22, 2, 4)),
     "Too salty to drink, too shallow to sail, too deep to walk.", 100),

    ("glacial_lake", "Glacial Lake", 0.0, 0.6, -0.2, 0.3, 0.05, 0.0, 0.0,
     0x90B8D0, 0xD0E8F0, 0x4A90C0, 0x0A2438, 0x8AB0B8, 0x6A9098,
     "biomesunseen:crystal_grass_block", "biomesunseen:frost_silt", "biomesunseen:glacierite_block",
     1, "biomesunseen:glacial_pines", 8, "biomesunseen:glacial_lake_flora",
     0.05, 0.2, ("biomesunseen:glacial_pier",), "biomesunseen:music.aquatic",
     "biomesunseen:ambient.wind_high", None,
     (("biomesunseen:frostling", 25, 2, 4), ("biomesunseen:river_lamprey", 18, 2, 3)),
     "Clear to the bottom, and the bottom is a very long way down.", 100),

    ("mangrove_labyrinth", "Mangrove Labyrinth", 0.9, 1.0, -0.2, 0.5, 0.0, 0.0, 0.0,
     0x4A7A5A, 0x80B088, 0x2A6A4A, 0x061A10, 0x60A060, 0x408040,
     "biomesunseen:tidegrass_block", "biomesunseen:brine_mud", "biomesunseen:spiritwood_stone",
     15, "biomesunseen:mangrove_trees", 12, "biomesunseen:mangrove_flora",
     -0.05, 0.2, ("biomesunseen:mangrove_platform",), "biomesunseen:music.aquatic",
     "biomesunseen:ambient.stream", None,
     (("biomesunseen:bogcrawler", 28, 2, 4), ("biomesunseen:orchid_mantis", 18, 1, 1)),
     "Roots in every direction and no two of them the same shape.", 100),

    ("sunken_cathedral", "Sunken Cathedral", 0.55, 1.0, -0.4, 0.6, -0.35, -0.1, 0.0,
     0x2A4A5A, 0x4A7A8A, 0x1A4A5A, 0x04141C, 0x4A8078, 0x2A6058,
     "biomesunseen:abyssal_silt", "biomesunseen:abyssal_silt", "biomesunseen:sunken_stone",
     0, None, 2, "biomesunseen:sunken_cathedral_flora",
     -0.35, 0.35, ("biomesunseen:sunken_cathedral",), "biomesunseen:music.aquatic",
     "biomesunseen:ambient.deep_water", None,
     (("biomesunseen:temple_guardian", 25, 1, 2), ("biomesunseen:trench_angler", 20, 1, 2)),
     "Vaulting still intact, bell still hanging, service still technically running.", 90),

    ("whitewater_gorge", "Whitewater Gorge", 0.5, 0.8, 0.3, 0.9, -0.1, 0.15, 0.0,
     0x7AA8C0, 0xB0D4E0, 0x3A88B8, 0x08283C, 0x70A880, 0x508860,
     "biomesunseen:umber_grass_block", "biomesunseen:river_gravel", "biomesunseen:titanite_block",
     2, "biomesunseen:gorge_pines", 10, "biomesunseen:gorge_flora",
     -0.15, 0.7, ("biomesunseen:gorge_bridge",), "biomesunseen:music.aquatic",
     "biomesunseen:ambient.rapids", None,
     (("biomesunseen:river_lamprey", 25, 2, 4), ("biomesunseen:gale_harrier", 15, 1, 2)),
     "The river arrives at the gorge at speed and does not slow down for anything.", 100),

    ("pearl_beds", "Pearl Beds", 0.8, 1.0, -0.35, 0.35, -0.1, -0.1, 0.0,
     0x78C0D8, 0xC0E8F0, 0x40B8D0, 0x083444, 0x80C8A8, 0x60B088,
     "biomesunseen:tide_sand", "biomesunseen:wet_silt", "biomesunseen:deep_pearl_block",
     0, None, 4, "biomesunseen:pearl_bed_flora",
     -0.12, 0.15, ("biomesunseen:pearl_bed_pavilion",), "biomesunseen:music.aquatic",
     "biomesunseen:ambient.underwater", None,
     (("biomesunseen:reefglider", 32, 3, 6), ("biomesunseen:coralback_crab", 26, 2, 4)),
     "Nacre on the seabed in drifts, and something has been harvesting it.", 100),

    ("blackwater_bog", "Blackwater Bog", 0.65, 1.0, -0.15, 0.6, -0.05, 0.1, 0.0,
     0x2A3A32, 0x4A6A58, 0x14241E, 0x020806, 0x4A6A48, 0x2A4A28,
     "biomesunseen:blight_grass_block", "biomesunseen:brine_mud", "biomesunseen:graveamber_stone",
     3, "biomesunseen:bog_cypress", 14, "biomesunseen:blackwater_flora",
     -0.05, 0.2, ("biomesunseen:blackwater_shack",), "biomesunseen:music.aquatic",
     "biomesunseen:ambient.blight", None,
     (("biomesunseen:bogcrawler", 32, 2, 4), ("biomesunseen:mire_wisp", 25, 1, 3)),
     "The water is the colour of strong tea and about as transparent.", 100),

    ("seagrass_meadow", "Seagrass Meadow", 0.75, 1.0, -0.3, 0.3, -0.08, -0.05, 0.0,
     0x60B0C8, 0xA0E0E0, 0x30A8C0, 0x083040, 0x70C898, 0x50B078,
     "biomesunseen:tide_sand", "biomesunseen:wet_silt", "biomesunseen:kelpstone_block",
     0, None, 7, "biomesunseen:seagrass_flora",
     -0.1, 0.1, ("biomesunseen:seagrass_buoy_line",), "biomesunseen:music.aquatic",
     "biomesunseen:ambient.underwater", None,
     (("biomesunseen:reefglider", 38, 4, 8), ("biomesunseen:coralback_crab", 24, 2, 4)),
     "Underwater pasture, and something has been grazing it.", 110),

    ("geyser_lagoon", "Geyser Lagoon", 0.95, 0.9, -0.25, 0.55, 0.0, 0.1, 0.0,
     0x70B8D0, 0xB8E4E8, 0x38B0C8, 0x083444, 0x80C8A0, 0x60B080,
     "biomesunseen:tidegrass_block", "biomesunseen:wet_silt", "biomesunseen:petrichorite_stone",
     2, "biomesunseen:lagoon_mangrove", 12, "biomesunseen:geyser_flora",
     -0.08, 0.3, ("biomesunseen:geyser_ring",), "biomesunseen:music.aquatic",
     "biomesunseen:ambient.rapids", "biomesunseen:heat_shimmer",
     (("biomesunseen:reefglider", 30, 2, 5), ("biomesunseen:emberling", 15, 1, 3)),
     "Warm water, cold air, and a geyser on a fourteen-minute cycle.", 100),

    ("leviathan_graveyard", "Leviathan Graveyard", 0.4, 1.0, -0.55, 0.65, -0.5, -0.15, 0.0,
     0x14283A, 0x2A4A60, 0x0A1E30, 0x020810, 0x2A5A5A, 0x1A4040,
     "biomesunseen:abyssal_silt", "biomesunseen:abyssal_silt", "biomesunseen:abyssite_block",
     0, None, 1, "biomesunseen:leviathan_flora",
     -0.5, 0.35, ("biomesunseen:leviathan_ribcage",), "biomesunseen:music.aquatic",
     "biomesunseen:ambient.deep_water", None,
     (("biomesunseen:trench_angler", 32, 1, 3), ("biomesunseen:abyssal_leviathan", 4, 1, 1)),
     "Bones the size of hulls. Several of them are hulls.", 80),
]


# ===========================================================================
#  DIMENSION BIOME TABLE
#  Field order (22):
#    0 id            8  surface_filler   16 music
#    1 name          9  trees_per_chunk  17 ambient_sound
#    2 category     10  tree_feature     18 particle
#    3 temperature  11  grass_per_chunk  19 spawns
#    4 humidity     12  flora_feature    20 lore
#    5 depth        13  ores             21 weight
#    6 weirdness    14  structures
#    7 surface_top  15  surface_stone
# ===========================================================================

_DIM_FIELDS = (
    "id name category temperature humidity depth weirdness surface_top surface_filler "
    "trees_per_chunk tree_feature grass_per_chunk flora_feature ores structures "
    "surface_stone music ambient_sound particle spawns lore weight"
).split()

_HOLLOW_STONES = ("hollow_stone", "gloomslate", "mycelial_slimestone", "spore_chalk", "basaltic_hollowstone")
_AETHER_STONES = ("aetherstone", "dawn_marble", "cloudstone", "twilight_shale", "gilded_aetherstone")
_VOID_STONES   = ("voidstone", "fracture_shale", "static_stone", "glitch_concrete", "null_basalt")

_HOLLOW_ORES = ("hollowite", "mycelium_ore", "gloomite", "deep_pearl", "sporeamber", "echo_crystal", "root_heart", "wraithsalt")
_AETHER_ORES = ("aetherium", "dawnshard", "skylead", "starfall", "stormcell", "runeglass", "moonpetal", "sunspore")
_VOID_ORES   = ("voidsteel", "nullite", "staticite", "chronosite", "duskite", "glacierite", "witherite", "bloodstone")

# ---------------------------------------------------------------------------
#  THE HOLLOW DEEP -- subterranean, bioluminescent. 20 biomes, 5 stones, 8 ores
# ---------------------------------------------------------------------------
_HOLLOW_DEEP = [
    ("hollow_threshold", "Hollow Threshold", "ethereal", 0.4, 0.9, 0.6, 0.0,
     "biomesunseen:hollow_grass_block", "biomesunseen:hollow_loam", 4, "biomesunseen:hollow_threshold_trees",
     16, "biomesunseen:hollow_flora", ("hollowite", "deep_pearl"), ("biomesunseen:hollow_deep_portal",),
     "hollow_stone", "biomesunseen:music.hollow_deep", None, "biomesunseen:lumen_mote",
     (("biomesunseen:hollow_scout", 20, 1, 2),), "Where the tunnel stops pretending to be natural.", 120),

    ("glowcap_grotto", "Glowcap Grotto", "ethereal", 0.5, 1.0, 0.8, 0.1,
     "biomesunseen:mycelial_slimestone", "biomesunseen:spore_loam", 0, None,
     24, "biomesunseen:glowcap_flora", ("hollowite", "sporeamber", "mycelium_ore"), (),
     "mycelial_slimestone", "biomesunseen:music.hollow_deep", "biomesunseen:ambient.drip",
     "biomesunseen:spore_drift", (("biomesunseen:sporeling", 40, 3, 6), ("biomesunseen:glowcap_grub", 25, 2, 4)),
     "Caps the size of roofs, and every one of them breathing.", 130),

    ("luminous_sea", "Luminous Sea", "aquatic", 0.45, 1.0, 1.0, -0.1,
     "biomesunseen:hollow_silt", "biomesunseen:hollow_silt", 0, None,
     4, "biomesunseen:luminous_sea_flora", ("deep_pearl", "tideglass"), ("biomesunseen:hollow_harbour",),
     "hollow_stone", "biomesunseen:music.hollow_deep", "biomesunseen:ambient.deep_water", None,
     (("biomesunseen:trench_angler", 30, 1, 3), ("biomesunseen:luminous_jelly", 35, 3, 6)),
     "A lake that lights itself so the things in it can see each other.", 110),

    ("crystal_vault", "Crystal Vault", "vibrant", 0.3, 0.5, 0.7, 0.2,
     "biomesunseen:spore_chalk", "biomesunseen:spore_chalk", 0, None,
     6, "biomesunseen:crystal_vault_flora", ("echo_crystal", "gloomite"), ("biomesunseen:crystal_vault_chamber",),
     "spore_chalk", "biomesunseen:music.hollow_deep", None, "biomesunseen:lumen_mote",
     (("biomesunseen:vault_keeper", 18, 1, 1),), "Geodes the size of houses, split open by something methodical.", 100),

    ("mycelial_wastes", "Mycelial Wastes", "harsh", 0.55, 0.7, 0.5, 0.0,
     "biomesunseen:mycelial_slimestone", "biomesunseen:spore_loam", 1, "biomesunseen:waste_fungal_columns",
     20, "biomesunseen:mycelial_waste_flora", ("mycelium_ore", "sporeamber"), (),
     "mycelial_slimestone", "biomesunseen:music.hollow_deep", None, "biomesunseen:spore_drift",
     (("biomesunseen:sporeling", 45, 3, 8), ("biomesunseen:mycelial_horror", 12, 1, 1)),
     "One organism, eleven square miles, no obvious opinion about you.", 120),

    ("gloomslate_depths", "Gloomslate Depths", "harsh", 0.3, 0.4, 1.1, 0.3,
     "biomesunseen:gloomslate", "biomesunseen:gloomslate", 0, None,
     2, "biomesunseen:gloomslate_flora", ("gloomite", "voidsteel"), (),
     "gloomslate", "biomesunseen:music.hollow_deep", "biomesunseen:ambient.wind_low", None,
     (("biomesunseen:gloomstalker", 30, 1, 2),), "Slate that drinks the torchlight and does not give it back.", 110),

    ("root_cathedral", "Root Cathedral", "ancient", 0.5, 0.8, 0.65, 0.05,
     "biomesunseen:hollow_grass_block", "biomesunseen:root_loam", 8, "biomesunseen:root_cathedral_trees",
     10, "biomesunseen:root_cathedral_flora", ("root_heart", "hollowite"), ("biomesunseen:root_cathedral",),
     "hollow_stone", "biomesunseen:music.hollow_deep", None, "biomesunseen:lumen_mote",
     (("biomesunseen:rootburrower", 25, 1, 3), ("biomesunseen:grove_warden", 15, 1, 1)),
     "The roots of the surface forest, arriving here as pillars.", 120),

    ("sunken_hollow_city", "Sunken Hollow City", "ancient", 0.45, 0.85, 0.9, -0.05,
     "biomesunseen:hollow_silt", "biomesunseen:hollow_silt", 1, "biomesunseen:hollow_city_palms",
     5, "biomesunseen:sunken_hollow_flora", ("deep_pearl", "wraithsalt"),
     ("biomesunseen:sunken_hollow_city", "biomesunseen:hollow_deep_portal"),
     "basaltic_hollowstone", "biomesunseen:music.hollow_deep", "biomesunseen:ambient.deep_water", None,
     (("biomesunseen:hollow_drowned", 30, 2, 4), ("biomesunseen:vault_keeper", 12, 1, 1)),
     "They built it underground and it flooded anyway.", 90),

    ("spore_chalk_flats", "Spore Chalk Flats", "vibrant", 0.5, 0.6, 0.55, -0.15,
     "biomesunseen:spore_chalk", "biomesunseen:spore_chalk", 0, None,
     8, "biomesunseen:chalk_flat_flora", ("sporeamber", "sunspore"), (),
     "spore_chalk", "biomesunseen:music.hollow_deep", None, "biomesunseen:spore_drift",
     (("biomesunseen:sporeling", 35, 3, 6),), "White chalk, green dust, and footprints that were not yours.", 120),

    ("basaltic_fissures", "Basaltic Fissures", "harsh", 0.9, 0.3, 0.75, 0.25,
     "biomesunseen:basaltic_hollowstone", "biomesunseen:basaltic_hollowstone", 0, None,
     1, "biomesunseen:fissure_flora", ("pyroclast", "ashen_core"), ("biomesunseen:fissure_bridge",),
     "basaltic_hollowstone", "biomesunseen:music.hollow_deep", "biomesunseen:ambient.ember",
     "biomesunseen:ember_drift", (("biomesunseen:emberling", 32, 2, 5), ("biomesunseen:magma_lurker", 22, 1, 2)),
     "The only warm place down here, and it is not warm for pleasant reasons.", 100),

    ("weeping_galleries", "Weeping Galleries", "ethereal", 0.4, 1.0, 0.85, 0.0,
     "biomesunseen:hollow_stone", "biomesunseen:hollow_loam", 2, "biomesunseen:gallery_pillars",
     12, "biomesunseen:weeping_gallery_flora", ("hollowite", "tideglass"), (),
     "hollow_stone", "biomesunseen:music.hollow_deep", "biomesunseen:ambient.drip", None,
     (("biomesunseen:luminous_jelly", 30, 2, 5),), "Water down every wall, and something has arranged it in lines.", 120),

    ("fungal_forest", "Fungal Forest", "vibrant", 0.55, 0.95, 0.7, 0.1,
     "biomesunseen:mycelial_slimestone", "biomesunseen:spore_loam", 14, "biomesunseen:fungal_forest_trees",
     18, "biomesunseen:fungal_forest_flora", ("mycelium_ore", "sporeamber", "root_heart"),
     ("biomesunseen:fungal_forest_hollow",),
     "mycelial_slimestone", "biomesunseen:music.hollow_deep", None, "biomesunseen:spore_drift",
     (("biomesunseen:fungal_titan", 8, 1, 1), ("biomesunseen:sporeling", 35, 3, 6)),
     "Trees, but fungal, and forty blocks tall, and aware.", 110),

    ("echo_chasm", "Echo Chasm", "harsh", 0.35, 0.5, 1.2, 0.35,
     "biomesunseen:gloomslate", "biomesunseen:gloomslate", 0, None,
     2, "biomesunseen:echo_chasm_flora", ("echo_crystal", "gloomite"), ("biomesunseen:echo_chasm_span",),
     "gloomslate", "biomesunseen:music.hollow_deep", "biomesunseen:ambient.wind_low", None,
     (("biomesunseen:gloomstalker", 28, 1, 2), ("biomesunseen:echo_bat", 30, 3, 6)),
     "Say something. Wait four seconds. It is not your voice that answers.", 100),

    ("pearl_depths", "Pearl Depths", "aquatic", 0.4, 1.0, 1.05, -0.2,
     "biomesunseen:hollow_silt", "biomesunseen:hollow_silt", 0, None,
     5, "biomesunseen:pearl_depth_flora", ("deep_pearl", "wraithsalt"), ("biomesunseen:pearl_depth_shrine",),
     "spore_chalk", "biomesunseen:music.hollow_deep", "biomesunseen:ambient.deep_water", None,
     (("biomesunseen:luminous_jelly", 40, 3, 6), ("biomesunseen:trench_angler", 25, 1, 2)),
     "Nacre on the ceiling, dripping up. Nobody has explained this.", 100),

    ("tremor_ward", "Tremor Ward", "ancient", 0.6, 0.5, 0.8, 0.15,
     "biomesunseen:basaltic_hollowstone", "biomesunseen:basaltic_hollowstone", 0, None,
     3, "biomesunseen:tremor_ward_flora", ("hollowite", "titanite"),
     ("biomesunseen:warden_of_the_hollow_deep_arena",),
     "basaltic_hollowstone", "biomesunseen:music.hollow_deep", "biomesunseen:ambient.tremor", None,
     (("biomesunseen:warden_acolyte", 20, 1, 2),), "Everything here is braced. Everything here is braced against the floor.", 80),

    ("hollow_oasis", "Hollow Oasis", "vibrant", 0.6, 0.9, 0.6, -0.1,
     "biomesunseen:hollow_grass_block", "biomesunseen:hollow_loam", 6, "biomesunseen:oasis_palms",
     22, "biomesunseen:hollow_oasis_flora", ("hollowite", "root_heart"), ("biomesunseen:hollow_oasis_camp",),
     "hollow_stone", "biomesunseen:music.hollow_deep", "biomesunseen:ambient.stream", "biomesunseen:lumen_mote",
     (("biomesunseen:hollow_scout", 22, 2, 4), ("biomesunseen:glowcap_grub", 20, 2, 3)),
     "Warm water, green light, and the only safe camp for three hundred blocks.", 130),

    ("chitin_warrens", "Chitin Warrens", "harsh", 0.65, 0.6, 0.7, 0.2,
     "biomesunseen:mycelial_slimestone", "biomesunseen:spore_loam", 0, None,
     6, "biomesunseen:warren_flora", ("mycelium_ore", "graveamber"), ("biomesunseen:chitin_warren",),
     "mycelial_slimestone", "biomesunseen:music.hollow_deep", None, None,
     (("biomesunseen:warren_skitter", 45, 4, 8), ("biomesunseen:glowcap_grub", 25, 2, 4)),
     "Tunnels lined with shell, all the same diameter, all the same height.", 110),

    ("lantern_terraces", "Lantern Terraces", "ethereal", 0.5, 0.85, 0.75, 0.0,
     "biomesunseen:hollow_grass_block", "biomesunseen:hollow_loam", 5, "biomesunseen:terrace_trees",
     20, "biomesunseen:lantern_terrace_flora", ("hollowite", "lumenshade"), ("biomesunseen:lantern_terrace_shrine",),
     "hollow_stone", "biomesunseen:music.hollow_deep", None, "biomesunseen:lumen_mote",
     (("biomesunseen:lanternkeeper", 15, 1, 1), ("biomesunseen:glimmerwing", 25, 2, 5)),
     "Stepped terraces, and a light on every one of them, still lit.", 120),

    ("deep_bloom_reach", "Deep Bloom Reach", "vibrant", 0.55, 0.9, 0.65, 0.05,
     "biomesunseen:hollow_grass_block", "biomesunseen:spore_loam", 7, "biomesunseen:bloom_reach_trees",
     26, "biomesunseen:deep_bloom_flora", ("bloomglass", "mycelium_ore"), (),
     "spore_chalk", "biomesunseen:music.hollow_deep", None, "biomesunseen:spore_drift",
     (("biomesunseen:petaldancer", 28, 2, 5), ("biomesunseen:sporeling", 30, 3, 6)),
     "Flowers that evolved in total darkness and glow instead.", 120),

    ("hollow_core", "Hollow Core", "ancient", 0.8, 0.4, 1.3, 0.4,
     "biomesunseen:basaltic_hollowstone", "biomesunseen:basaltic_hollowstone", 0, None,
     1, "biomesunseen:hollow_core_flora", ("hollowite", "titanite", "ashen_core"),
     ("biomesunseen:hollow_core_vault",),
     "basaltic_hollowstone", "biomesunseen:music.hollow_deep", "biomesunseen:ambient.tremor",
     "biomesunseen:ember_drift", (("biomesunseen:warden_acolyte", 25, 1, 3), ("biomesunseen:magma_lurker", 20, 1, 2)),
     "The bottom. It is warmer than the middle. It is not supposed to be warmer.", 70),
]

# ---------------------------------------------------------------------------
#  AETHERFALL -- floating islands, celestial twilight. 20 biomes
# ---------------------------------------------------------------------------
_AETHERFALL = [
    ("dawn_landing", "Dawn Landing", "ethereal", 0.55, 0.5, 0.0, 0.0,
     "biomesunseen:aether_grass_block", "biomesunseen:aether_loam", 5, "biomesunseen:dawn_landing_trees",
     18, "biomesunseen:dawn_landing_flora", ("aetherium", "dawnshard"), ("biomesunseen:aetherfall_portal",),
     "aetherstone", "biomesunseen:music.aetherfall", None, "biomesunseen:aetherveil_mote",
     (("biomesunseen:veilwing", 30, 2, 4),), "The first island you land on, and the last one you trust.", 130),

    ("cloud_sea", "Cloud Sea", "aquatic", 0.5, 0.8, -0.1, 0.1,
     "biomesunseen:cloudstone", "biomesunseen:cloudstone", 0, None,
     4, "biomesunseen:cloud_sea_flora", ("skylead", "stormcell"), (),
     "cloudstone", "biomesunseen:music.aetherfall", "biomesunseen:ambient.wind_high",
     "biomesunseen:aetherveil_mote", (("biomesunseen:cloudfin", 35, 3, 6),),
     "Not water. It behaves like water. Do not test the difference.", 120),

    ("gilded_citadel", "Gilded Citadel", "ancient", 0.5, 0.4, 0.15, 0.2,
     "biomesunseen:gilded_aetherstone", "biomesunseen:dawn_marble", 2, "biomesunseen:citadel_pillars",
     8, "biomesunseen:citadel_flora", ("aetherium", "starfall"),
     ("biomesunseen:sky_citadel", "biomesunseen:the_skyward_crown_arena"),
     "gilded_aetherstone", "biomesunseen:music.aetherfall", None, None,
     (("biomesunseen:crown_sentinel", 25, 1, 2), ("biomesunseen:astral_scribe", 15, 1, 1)),
     "Still staffed. The staff are not people any more.", 90),

    ("twilight_terrace", "Twilight Terrace", "ethereal", 0.4, 0.6, 0.1, -0.1,
     "biomesunseen:aether_grass_block", "biomesunseen:twilight_shale", 4, "biomesunseen:terrace_trees_aether",
     16, "biomesunseen:twilight_terrace_flora", ("duskite", "moonpetal"), ("biomesunseen:twilight_terrace_shrine",),
     "twilight_shale", "biomesunseen:music.aetherfall", None, "biomesunseen:moonpetal_drift",
     (("biomesunseen:petaldancer", 25, 2, 4), ("biomesunseen:veilwing", 22, 1, 3)),
     "Stepped terraces where the light arrives at an angle it should not.", 120),

    ("dawn_marble_quarry", "Dawn Marble Quarry", "ancient", 0.55, 0.3, 0.2, 0.25,
     "biomesunseen:dawn_marble", "biomesunseen:dawn_marble", 0, None,
     2, "biomesunseen:quarry_flora", ("dawnshard", "aetherium"), ("biomesunseen:marble_quarry",),
     "dawn_marble", "biomesunseen:music.aetherfall", None, None,
     (("biomesunseen:quarry_construct", 22, 1, 2),), "Cut blocks, stacked, counted, and abandoned mid-invoice.", 110),

    ("floating_meadow", "Floating Meadow", "vibrant", 0.6, 0.7, 0.0, -0.05,
     "biomesunseen:aether_grass_block", "biomesunseen:aether_loam", 3, "biomesunseen:meadow_trees_aether",
     30, "biomesunseen:floating_meadow_flora", ("sunspore", "moonpetal"), ("biomesunseen:meadow_windmill",),
     "aetherstone", "biomesunseen:music.aetherfall", None, "biomesunseen:pollen_drift",
     (("biomesunseen:petaldancer", 35, 3, 6), ("biomesunseen:meadow_skipper", 28, 2, 5)),
     "Grass, flowers, and forty blocks of nothing underneath.", 130),

    ("stormcell_spire", "Stormcell Spire", "harsh", 0.45, 0.9, 0.3, 0.3,
     "biomesunseen:twilight_shale", "biomesunseen:twilight_shale", 0, None,
     1, "biomesunseen:stormcell_flora", ("stormcell", "skylead"), ("biomesunseen:stormcell_spire",),
     "twilight_shale", "biomesunseen:music.aetherfall", "biomesunseen:ambient.storm", None,
     (("biomesunseen:gale_harrier", 30, 1, 3), ("biomesunseen:stormcell_wisp", 25, 2, 4)),
     "The lightning here strikes upward on a four-second cycle.", 100),

    ("starfall_vault", "Starfall Vault", "ancient", 0.35, 0.4, 0.25, 0.15,
     "biomesunseen:aetherstone", "biomesunseen:dawn_marble", 1, "biomesunseen:vault_pillars_aether",
     6, "biomesunseen:starfall_vault_flora", ("starfall", "aetherium"), ("biomesunseen:starfall_vault",),
     "aetherstone", "biomesunseen:music.aetherfall", None, "biomesunseen:starfall_ember",
     (("biomesunseen:crown_sentinel", 20, 1, 2), ("biomesunseen:astral_scribe", 18, 1, 1)),
     "Something fell here and was immediately built over.", 100),

    ("aurora_bridge", "Aurora Bridge", "ethereal", 0.35, 0.6, 0.05, 0.0,
     "biomesunseen:cloudstone", "biomesunseen:cloudstone", 0, None,
     3, "biomesunseen:aurora_bridge_flora", ("skylead", "runeglass"), ("biomesunseen:aurora_bridge",),
     "cloudstone", "biomesunseen:music.aetherfall", None, "biomesunseen:aurora_ribbon",
     (("biomesunseen:veilwing", 28, 2, 4),), "A span of solid light between two islands that no longer exist.", 110),

    ("celestial_orchard", "Celestial Orchard", "vibrant", 0.6, 0.75, 0.05, -0.1,
     "biomesunseen:aether_grass_block", "biomesunseen:aether_loam", 12, "biomesunseen:orchard_trees_aether",
     20, "biomesunseen:celestial_orchard_flora", ("sunspore", "dawnshard"), ("biomesunseen:orchard_pavilion",),
     "aetherstone", "biomesunseen:music.aetherfall", None, "biomesunseen:pollen_drift",
     (("biomesunseen:meadow_skipper", 30, 2, 5), ("biomesunseen:orchard_tender", 12, 1, 1)),
     "Fruit that ripens whether or not anybody is going to pick it.", 120),

    ("runeglass_fields", "Runeglass Fields", "vibrant", 0.5, 0.5, 0.15, 0.1,
     "biomesunseen:dawn_marble", "biomesunseen:runeglass_grit", 0, None,
     5, "biomesunseen:runeglass_flora", ("runeglass", "dawnshard"), ("biomesunseen:runeglass_henge",),
     "dawn_marble", "biomesunseen:music.aetherfall", None, "biomesunseen:lumen_mote",
     (("biomesunseen:rune_construct", 20, 1, 2),), "Glass panes with writing on them, planted like crops.", 110),

    ("skyward_steps", "Skyward Steps", "ancient", 0.45, 0.5, 0.35, 0.25,
     "biomesunseen:gilded_aetherstone", "biomesunseen:dawn_marble", 1, "biomesunseen:steps_pillars",
     4, "biomesunseen:skyward_steps_flora", ("aetherium", "skylead"), ("biomesunseen:skyward_stair",),
     "gilded_aetherstone", "biomesunseen:music.aetherfall", "biomesunseen:ambient.wind_high", None,
     (("biomesunseen:crown_sentinel", 22, 1, 2),), "A staircase going up for six hundred blocks with no top.", 100),

    ("featherfall_grove", "Featherfall Grove", "ethereal", 0.6, 0.8, -0.05, -0.1,
     "biomesunseen:aether_grass_block", "biomesunseen:aether_loam", 9, "biomesunseen:featherfall_trees",
     22, "biomesunseen:featherfall_flora", ("moonpetal", "aetherium"), (),
     "aetherstone", "biomesunseen:music.aetherfall", None, "biomesunseen:moonpetal_drift",
     (("biomesunseen:veilwing", 32, 2, 5), ("biomesunseen:meadow_skipper", 25, 2, 4)),
     "The leaves fall slowly here. Everything falls slowly here.", 130),

    ("shatterbelt", "Shatterbelt", "harsh", 0.4, 0.3, 0.2, 0.35,
     "biomesunseen:twilight_shale", "biomesunseen:twilight_shale", 0, None,
     1, "biomesunseen:shatterbelt_flora", ("stormcell", "duskite"), ("biomesunseen:shatterbelt_crossing",),
     "twilight_shale", "biomesunseen:music.aetherfall", "biomesunseen:ambient.wind_high", None,
     (("biomesunseen:gale_harrier", 32, 1, 3),), "Island gravel in a slow orbit. Mind the gaps. All of them.", 100),

    ("hymn_halls", "Hymn Halls", "ancient", 0.4, 0.5, 0.1, 0.05,
     "biomesunseen:dawn_marble", "biomesunseen:dawn_marble", 0, None,
     3, "biomesunseen:hymn_hall_flora", ("runeglass", "starfall"), ("biomesunseen:hymn_hall",),
     "dawn_marble", "biomesunseen:music.aetherfall", "biomesunseen:ambient.hymn", None,
     (("biomesunseen:astral_scribe", 25, 1, 2), ("biomesunseen:crown_sentinel", 15, 1, 1)),
     "A hall tuned so that walking through it produces a chord.", 90),

    ("zephyr_reach", "Zephyr Reach", "harsh", 0.5, 0.4, 0.0, 0.3,
     "biomesunseen:cloudstone", "biomesunseen:cloudstone", 0, None,
     2, "biomesunseen:zephyr_flora", ("skylead", "stormcell"), ("biomesunseen:zephyr_pylon",),
     "cloudstone", "biomesunseen:music.aetherfall", "biomesunseen:ambient.wind_high", None,
     (("biomesunseen:gale_harrier", 35, 2, 4),), "Wind that has been blowing in one direction for a very long time.", 110),

    ("gilded_archive", "Gilded Archive", "ancient", 0.45, 0.45, 0.2, 0.1,
     "biomesunseen:gilded_aetherstone", "biomesunseen:dawn_marble", 1, "biomesunseen:archive_pillars",
     5, "biomesunseen:gilded_archive_flora", ("aetherium", "runeglass"), ("biomesunseen:gilded_archive",),
     "gilded_aetherstone", "biomesunseen:music.aetherfall", None, None,
     (("biomesunseen:astral_scribe", 30, 1, 3),), "Every expedition that ever came up here, catalogued.", 100),

    ("sunspire_plateau", "Sunspire Plateau", "vibrant", 0.7, 0.5, 0.3, 0.15,
     "biomesunseen:aether_grass_block", "biomesunseen:dawn_marble", 4, "biomesunseen:plateau_trees_aether",
     18, "biomesunseen:sunspire_flora", ("sunspore", "starfall", "dawnshard"), ("biomesunseen:sunspire_obelisk",),
     "dawn_marble", "biomesunseen:music.aetherfall", None, "biomesunseen:starfall_ember",
     (("biomesunseen:meadow_skipper", 28, 2, 5), ("biomesunseen:orchard_tender", 12, 1, 1)),
     "The highest flat ground in the dimension and the light never leaves it.", 110),

    ("moonpetal_skyfield", "Moonpetal Skyfield", "ethereal", 0.4, 0.7, -0.1, -0.15,
     "biomesunseen:aether_grass_block", "biomesunseen:aether_loam", 2, "biomesunseen:skyfield_trees",
     28, "biomesunseen:moonpetal_skyfield_flora", ("moonpetal", "runeglass"), (),
     "aetherstone", "biomesunseen:music.aetherfall", None, "biomesunseen:moonpetal_drift",
     (("biomesunseen:petaldancer", 38, 3, 6),), "Petals drifting between islands, connecting them like a sentence.", 130),

    ("crown_apex", "Crown Apex", "ancient", 0.5, 0.4, 0.5, 0.4,
     "biomesunseen:gilded_aetherstone", "biomesunseen:gilded_aetherstone", 0, None,
     2, "biomesunseen:crown_apex_flora", ("aetherium", "starfall", "skylead"),
     ("biomesunseen:the_skyward_crown_arena",),
     "gilded_aetherstone", "biomesunseen:music.aetherfall", "biomesunseen:ambient.hymn",
     "biomesunseen:starfall_ember", (("biomesunseen:crown_sentinel", 30, 2, 3),),
     "The top of the staircase. There is a throne. It is occupied.", 60),
]

# ---------------------------------------------------------------------------
#  THE VOID BETWEEN -- glitchy, surreal, fractured reality. 20 biomes
# ---------------------------------------------------------------------------
_VOID_BETWEEN = [
    ("void_threshold", "Void Threshold", "ethereal", 0.3, 0.3, 0.6, 0.0,
     "biomesunseen:void_grass_block", "biomesunseen:void_loam", 3, "biomesunseen:void_threshold_trees",
     10, "biomesunseen:void_flora", ("voidsteel", "duskite"), ("biomesunseen:void_portal",),
     "voidstone", "biomesunseen:music.void_between", None, "biomesunseen:void_fracture",
     (("biomesunseen:void_scout", 20, 1, 2),), "The last place in this dimension that behaves.", 130),

    ("fracture_plains", "Fracture Plains", "harsh", 0.25, 0.2, 0.5, 0.15,
     "biomesunseen:fracture_shale", "biomesunseen:fracture_shale", 0, None,
     2, "biomesunseen:fracture_flora", ("voidsteel", "staticite"), (),
     "fracture_shale", "biomesunseen:music.void_between", None, "biomesunseen:void_fracture",
     (("biomesunseen:fracture_hound", 32, 1, 3),), "Flat, cracked, and the cracks are in the wrong directions.", 120),

    ("static_wastes", "Static Wastes", "harsh", 0.35, 0.25, 0.55, 0.2,
     "biomesunseen:static_stone", "biomesunseen:static_stone", 0, None,
     1, "biomesunseen:static_flora", ("staticite", "nullite"), (),
     "static_stone", "biomesunseen:music.void_between", "biomesunseen:ambient.static", None,
     (("biomesunseen:static_wraith", 30, 1, 2),), "The air has grain. You can see through it badly.", 110),

    ("glitch_garden", "Glitch Garden", "vibrant", 0.4, 0.6, 0.45, -0.1,
     "biomesunseen:void_grass_block", "biomesunseen:glitch_loam", 6, "biomesunseen:glitch_garden_trees",
     24, "biomesunseen:glitch_garden_flora", ("nullite", "bloomglass"), ("biomesunseen:glitch_garden_maze",),
     "glitch_concrete", "biomesunseen:music.void_between", None, "biomesunseen:void_fracture",
     (("biomesunseen:garden_aberration", 22, 1, 2), ("biomesunseen:petaldancer", 18, 2, 4)),
     "Flowers rendered in three colours that are not the flower.", 120),

    ("null_sea", "Null Sea", "aquatic", 0.3, 0.5, 1.0, -0.2,
     "biomesunseen:null_basalt", "biomesunseen:null_basalt", 0, None,
     2, "biomesunseen:null_sea_flora", ("nullite", "abyssite"), ("biomesunseen:null_sea_wreck",),
     "null_basalt", "biomesunseen:music.void_between", "biomesunseen:ambient.static", None,
     (("biomesunseen:null_swimmer", 30, 2, 4),), "Liquid that is not wet. Do not use this to test anything.", 100),

    ("unraveling_nexus", "Unraveling Nexus", "ancient", 0.3, 0.3, 0.7, 0.45,
     "biomesunseen:glitch_concrete", "biomesunseen:null_basalt", 0, None,
     1, "biomesunseen:nexus_flora", ("nullite", "voidsteel", "chronosite"),
     ("biomesunseen:the_unraveling_arena",),
     "null_basalt", "biomesunseen:music.void_between", "biomesunseen:ambient.static",
     "biomesunseen:void_fracture", (("biomesunseen:unraveling_shard", 25, 1, 3),),
     "The centre of the error. It has a shape, and the shape keeps changing its mind.", 60),

    ("chrono_shelf", "Chrono Shelf", "ancient", 0.35, 0.35, 0.6, 0.1,
     "biomesunseen:fracture_shale", "biomesunseen:chrono_grit", 1, "biomesunseen:chrono_pillars",
     4, "biomesunseen:chrono_shelf_flora", ("chronosite", "echo_crystal"), ("biomesunseen:chrono_ruin",),
     "fracture_shale", "biomesunseen:music.void_between", None, "biomesunseen:lumen_mote",
     (("biomesunseen:chrono_warden", 18, 1, 1),), "Events here happen in the order they are remembered.", 100),

    ("dusk_mirror", "Dusk Mirror", "ethereal", 0.3, 0.45, 0.5, -0.15,
     "biomesunseen:void_grass_block", "biomesunseen:void_loam", 4, "biomesunseen:dusk_mirror_trees",
     14, "biomesunseen:dusk_mirror_flora", ("duskite", "runeglass"), ("biomesunseen:dusk_mirror_hall",),
     "voidstone", "biomesunseen:music.void_between", None, "biomesunseen:void_fracture",
     (("biomesunseen:mirror_walk", 20, 1, 2),), "Reflections arrive a half-second after the thing they reflect.", 110),

    ("shardfall_expanse", "Shardfall Expanse", "harsh", 0.25, 0.25, 0.65, 0.3,
     "biomesunseen:fracture_shale", "biomesunseen:shard_grit", 0, None,
     1, "biomesunseen:shardfall_flora", ("voidsteel", "fracture_shale_ore"), (),
     "fracture_shale", "biomesunseen:music.void_between", None, "biomesunseen:void_fracture",
     (("biomesunseen:fracture_hound", 30, 1, 3), ("biomesunseen:shardling", 28, 2, 4)),
     "It is raining geometry. Take cover behind something that exists.", 110),

    ("paradox_hollow", "Paradox Hollow", "ancient", 0.3, 0.4, 0.55, 0.05,
     "biomesunseen:glitch_concrete", "biomesunseen:glitch_loam", 3, "biomesunseen:paradox_trees",
     6, "biomesunseen:paradox_flora", ("chronosite", "nullite"), ("biomesunseen:paradox_chamber",),
     "glitch_concrete", "biomesunseen:music.void_between", None, None,
     (("biomesunseen:chrono_warden", 22, 1, 2),), "A room that is bigger from outside. Both measurements are correct.", 90),

    ("bleeding_spires", "Bleeding Spires", "harsh", 0.4, 0.3, 0.75, 0.35,
     "biomesunseen:null_basalt", "biomesunseen:null_basalt", 0, None,
     1, "biomesunseen:bleeding_spire_flora", ("bloodstone", "voidsteel"), ("biomesunseen:bleeding_spire_field",),
     "null_basalt", "biomesunseen:music.void_between", "biomesunseen:ambient.static", None,
     (("biomesunseen:spire_climber", 28, 1, 2),), "Spires that weep something dark and warm and definitely not water.", 100),

    ("wither_veil", "Wither Veil", "harsh", 0.3, 0.35, 0.5, 0.1,
     "biomesunseen:void_grass_block", "biomesunseen:blight_loam", 2, "biomesunseen:wither_veil_trees",
     4, "biomesunseen:wither_veil_flora", ("witherite", "graveamber"), (),
     "voidstone", "biomesunseen:music.void_between", "biomesunseen:ambient.blight", None,
     (("biomesunseen:blighthound", 30, 1, 3), ("biomesunseen:static_wraith", 20, 1, 2)),
     "Everything here is already dead and has not stopped moving.", 110),

    ("recursive_fields", "Recursive Fields", "vibrant", 0.4, 0.5, 0.45, 0.0,
     "biomesunseen:static_stone", "biomesunseen:glitch_loam", 5, "biomesunseen:recursive_trees",
     20, "biomesunseen:recursive_flora", ("staticite", "bloomglass"), ("biomesunseen:recursive_farm",),
     "static_stone", "biomesunseen:music.void_between", None, "biomesunseen:void_fracture",
     (("biomesunseen:garden_aberration", 25, 2, 3),), "The same field, seven times, at seven slightly different scales.", 120),

    ("abyssal_shelf_void", "Abyssal Shelf", "aquatic", 0.3, 0.5, 1.1, -0.25,
     "biomesunseen:null_basalt", "biomesunseen:null_basalt", 0, None,
     1, "biomesunseen:abyssal_shelf_flora", ("abyssite", "nullite"), (),
     "null_basalt", "biomesunseen:music.void_between", "biomesunseen:ambient.deep_water", None,
     (("biomesunseen:null_swimmer", 32, 2, 4), ("biomesunseen:trench_angler", 20, 1, 2)),
     "The edge of the dimension, and then a long way down.", 90),

    ("memory_vault", "Memory Vault", "ancient", 0.35, 0.4, 0.6, 0.2,
     "biomesunseen:fracture_shale", "biomesunseen:chrono_grit", 0, None,
     3, "biomesunseen:memory_vault_flora", ("chronosite", "echo_crystal", "runeglass"),
     ("biomesunseen:memory_vault",),
     "fracture_shale", "biomesunseen:music.void_between", None, "biomesunseen:lumen_mote",
     (("biomesunseen:astral_scribe", 25, 1, 2), ("biomesunseen:chrono_warden", 15, 1, 1)),
     "Shelves of things that happened. Some of them are still on loan.", 100),

    ("chromatic_reef", "Chromatic Reef", "vibrant", 0.45, 0.7, 0.4, -0.05,
     "biomesunseen:glitch_concrete", "biomesunseen:glitch_loam", 0, None,
     8, "biomesunseen:chromatic_reef_flora", ("bloomglass", "coralite", "nullite"),
     ("biomesunseen:chromatic_reef_arch",),
     "glitch_concrete", "biomesunseen:music.void_between", "biomesunseen:ambient.underwater",
     "biomesunseen:void_fracture", (("biomesunseen:null_swimmer", 30, 3, 5),),
     "A reef growing in nothing, in colours that have no names yet.", 120),

    ("serpent_run", "Serpent Run", "harsh", 0.3, 0.3, 0.7, 0.25,
     "biomesunseen:voidstone", "biomesunseen:void_loam", 1, "biomesunseen:serpent_run_obelisks",
     2, "biomesunseen:serpent_run_flora", ("voidsteel", "duskite"),
     ("biomesunseen:void_serpent_arena",),
     "voidstone", "biomesunseen:music.void_between", None, "biomesunseen:void_fracture",
     (("biomesunseen:fracture_hound", 25, 1, 2), ("biomesunseen:void_scout", 15, 1, 1)),
     "A corridor three hundred blocks long with scratch marks along all of it.", 70),

    ("hollow_echo", "Hollow Echo", "ethereal", 0.35, 0.45, 0.5, 0.0,
     "biomesunseen:void_grass_block", "biomesunseen:void_loam", 4, "biomesunseen:hollow_echo_trees",
     12, "biomesunseen:hollow_echo_flora", ("echo_crystal", "wraithsalt"), (),
     "voidstone", "biomesunseen:music.void_between", "biomesunseen:ambient.wind_low", None,
     (("biomesunseen:echo_bat", 35, 3, 6), ("biomesunseen:mire_wisp", 22, 1, 3)),
     "The Hollow Deep, remembered imperfectly, at a distance.", 110),

    ("terminal_glade", "Terminal Glade", "ethereal", 0.4, 0.6, 0.45, -0.1,
     "biomesunseen:void_grass_block", "biomesunseen:glitch_loam", 8, "biomesunseen:terminal_glade_trees",
     18, "biomesunseen:terminal_glade_flora", ("bloomglass", "root_heart"), ("biomesunseen:terminal_glade_shrine",),
     "glitch_concrete", "biomesunseen:music.void_between", None, "biomesunseen:lumen_mote",
     (("biomesunseen:garden_aberration", 20, 1, 2), ("biomesunseen:thicket_sprite", 22, 1, 3)),
     "The calmest place in the error. That is what makes it frightening.", 120),

    ("outer_margin", "Outer Margin", "harsh", 0.2, 0.2, 0.8, 0.5,
     "biomesunseen:null_basalt", "biomesunseen:null_basalt", 0, None,
     0, "biomesunseen:outer_margin_flora", ("nullite", "voidsteel"), (),
     "null_basalt", "biomesunseen:music.void_between", "biomesunseen:ambient.static", None,
     (("biomesunseen:static_wraith", 35, 1, 3),), "Where the dimension stops rendering and keeps going anyway.", 80),
]


# ===========================================================================
#  PARSER + ASSEMBLED REGISTRIES
# ===========================================================================

def _spec_from_compact(row, category: str, dimension: str = "overworld") -> BiomeSpec:
    """Build a BiomeSpec from one row of the compact Overworld table."""
    if len(row) != len(_OW_COMPACT_FIELDS):
        raise ValueError(
            f"biome {row[0]!r}: expected {len(_OW_COMPACT_FIELDS)} fields, got {len(row)}"
        )
    kw = dict(zip(_OW_COMPACT_FIELDS, row))
    kw["ores"] = tuple(kw.pop("ores", ()))
    return BiomeSpec(dimension=dimension, category=category, **kw)


def _spec_from_dim(row, dimension: str) -> BiomeSpec:
    """Build a BiomeSpec from one row of the dimension table."""
    if len(row) != len(_DIM_FIELDS):
        raise ValueError(
            f"dimension biome {row[0]!r}: expected {len(_DIM_FIELDS)} fields, got {len(row)}"
        )
    kw = dict(zip(_DIM_FIELDS, row))
    # Dimension biomes carry no sky/precipitation and reuse the category colour.
    kw["has_precipitation"] = False
    kw["ores"] = tuple(kw.pop("ores", ()))
    return BiomeSpec(dimension=dimension, **kw)


_CATEGORY_BY_TABLE = {
    "_OW_ANCIENT": "ancient",
    "_OW_VIBRANT": "vibrant",
    "_OW_HARSH": "harsh",
    "_OW_AQUATIC": "aquatic",
}

ALL_BIOMES: List[BiomeSpec] = list(OVERWORLD_BIOMES)
for _tbl, _cat in _CATEGORY_BY_TABLE.items():
    for _row in globals()[_tbl]:
        ALL_BIOMES.append(_spec_from_compact(_row, _cat))
for _row in _HOLLOW_DEEP:
    ALL_BIOMES.append(_spec_from_dim(_row, "hollow_deep"))
for _row in _AETHERFALL:
    ALL_BIOMES.append(_spec_from_dim(_row, "aetherfall"))
for _row in _VOID_BETWEEN:
    ALL_BIOMES.append(_spec_from_dim(_row, "void_between"))

BY_ID: Dict[str, BiomeSpec] = {}
for _b in ALL_BIOMES:
    if _b.id in BY_ID:
        raise ValueError(f"duplicate biome id {_b.id!r}")
    BY_ID[_b.id] = _b

OVERWORLD: List[BiomeSpec] = [b for b in ALL_BIOMES if b.dimension == "overworld"]
HOLLOW_DEEP: List[BiomeSpec] = [b for b in ALL_BIOMES if b.dimension == "hollow_deep"]
AETHERFALL: List[BiomeSpec] = [b for b in ALL_BIOMES if b.dimension == "aetherfall"]
VOID_BETWEEN: List[BiomeSpec] = [b for b in ALL_BIOMES if b.dimension == "void_between"]

DIMENSION_STONES: Dict[str, Tuple[str, ...]] = {
    "hollow_deep": _HOLLOW_STONES,
    "aetherfall": _AETHER_STONES,
    "void_between": _VOID_STONES,
}
DIMENSION_ORES: Dict[str, Tuple[str, ...]] = {
    "hollow_deep": _HOLLOW_ORES,
    "aetherfall": _AETHER_ORES,
    "void_between": _VOID_ORES,
}


def biome_by_id(biome_id: str) -> BiomeSpec:
    try:
        return BY_ID[biome_id]
    except KeyError:
        raise KeyError(f"unknown biome {biome_id!r}") from None
