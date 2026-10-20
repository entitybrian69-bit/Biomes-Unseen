"""
content/ores.py -- 44 ores: 20 Overworld + 24 across the three dimensions.

Every ore declares a unique use (Golden Rule: no ore exists just to exist), a
mineral ramp from pixelart.palettes, a hand-authored vein composition from
pixelart.base_maps.ORE_MAPS, the stone it replaces, and its generation band.

The `uses` tuple drives which gear sets, devices and potions the codegen
emits for the ore, so adding an ore here automatically wires its content.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# Vein compositions available in pixelart.base_maps.ORE_MAPS
VEIN_FORMS = ("cluster_large", "spire", "speckle", "vein", "nodule", "banded", "dendrite", "shard")

# What an ore can be spent on.
#
# This is authored design intent, and nothing in the pipeline consumes it: no
# generator and no Java class reads OreSpec.uses, so a declaration here does not
# by itself make anything true in game. validate.py's check_ore_uses holds the
# field honest instead, by testing whether each declared use is realised in the
# shipped data and reporting the gap where it is not.
USE_TOOLS = "tools"
USE_ARMOR = "armor"
USE_DEVICE = "device"
USE_POTION = "potion"
USE_BLOCK = "block"
USE_CURRENCY = "currency"
USE_CRAFTING = "crafting"
USE_BOSS = "boss"

# Uses with no subsystem behind them at all. A `device` ore would need a block
# entity and a menu; a `potion` ore needs MobEffects and brewing recipes; a
# `currency` ore needs trades. None of the three exists, so every ore declaring
# one is promising content the mod cannot deliver. These are roadmap rather than
# shipped, and check_ore_uses reports them as a known gap the way check_audio
# reports the silent sound ids -- not silently, and not as a build failure, since
# adding the subsystems is new scope rather than a defect in what is here.
ROADMAP_USES = frozenset({USE_DEVICE, USE_POTION, USE_CURRENCY})

# Uses the mod ships a subsystem for, so a declaration here is a promise the
# data is expected to keep:
#   block     the ore's compact-storage block, craftable from nine of its drop
#   crafting  the drop or its refined form appearing as a recipe ingredient
#   tools     a tool set named after the ore
#   armor     an armour set named after it, or repairing with its drop
#   boss      a boss arena or boss gear that consumes it
# Not every ore realises every one of these -- ten armour sets and ten tool sets
# cannot cover forty-four ores -- so check_ore_uses reports the shortfalls per
# category rather than requiring all five. What it does require is that the
# categories themselves are spelled correctly: ROADMAP_USES and SHIPPED_USES must
# together account for every declared use, so a typo such as "devic" is an error
# instead of being silently read as a shipped category the data then fails.
SHIPPED_USES = frozenset({USE_BLOCK, USE_CRAFTING, USE_TOOLS, USE_ARMOR, USE_BOSS})


@dataclass(frozen=True)
class OreSpec:
    id: str
    name: str
    dimension: str
    ramp: str                      # key into pixelart.palettes.MINERAL_RAMPS
    vein_form: str                 # key into pixelart.base_maps.ORE_MAPS
    host_stone: str                # block id the ore replaces (no namespace)
    uses: Tuple[str, ...]
    tier: int                      # required harvest level: 1 wood .. 5 netherite+
    drop: Optional[str] = None     # item id dropped; None -> drops itself
    drop_count: Tuple[int, int] = (1, 1)
    experience: Tuple[int, int] = (0, 0)
    # generation band, in world Y
    min_y: int = -64
    max_y: int = 64
    vein_size: int = 8
    veins_per_chunk: int = 8
    air_exposure: float = 0.0      # 0.0 = normal, 1.0 = only exposed to air
    rare: bool = False
    lore: str = ""

    @property
    def base_name(self) -> str:
        """
        The ore id with any authored trailing '_ore' stripped.

        Two entries in the table were authored as 'mycelium_ore' and
        'fracture_shale_ore' because those names read naturally, but every
        derived registry name appends its own suffix. Normalising here keeps a
        single source of truth and makes 'mycelium_ore_ore' impossible.
        """
        return self.id[: -len("_ore")] if self.id.endswith("_ore") else self.id

    @property
    def ore_block(self) -> str:
        """Registry path of the ore block, e.g. 'lumenite_ore'."""
        return f"{self.base_name}_ore"

    @property
    def mineral_block(self) -> str:
        """Registry path of the compressed mineral block, e.g. 'lumenite_block'."""
        return f"{self.base_name}_block"

    @property
    def block_id(self) -> str:
        return f"biomesunseen:{self.ore_block}"

    @property
    def mineral_block_id(self) -> str:
        return f"biomesunseen:{self.mineral_block}"

    @property
    def deepslate_ore_block(self) -> Optional[str]:
        """Registry path of the deepslate-hosted variant, if any."""
        if self.dimension != "overworld":
            return None
        return f"deepslate_{self.ore_block}"

    @property
    def deepslate_variant(self) -> Optional[str]:
        """Overworld ores additionally generate a deepslate-hosted variant."""
        path = self.deepslate_ore_block
        return None if path is None else f"biomesunseen:{path}"


# ---------------------------------------------------------------------------
#  20 OVERWORLD ORES
# ---------------------------------------------------------------------------

OVERWORLD_ORES: List[OreSpec] = [
    OreSpec("lumenite", "Lumenite", "overworld", "lumenite", "cluster_large", "stone",
            (USE_TOOLS, USE_ARMOR, USE_DEVICE, USE_BLOCK), 3,
            drop="lumenite_shard", drop_count=(2, 5), experience=(3, 7),
            min_y=-32, max_y=48, vein_size=7, veins_per_chunk=9,
            lore="Stores daylight. Miners carry a lump of it as a lamp and it works, badly."),
    OreSpec("umbrite", "Umbrite", "overworld", "umbrite", "speckle", "stone",
            (USE_CRAFTING, USE_BLOCK), 2, experience=(1, 3),
            min_y=-48, max_y=32, vein_size=9, veins_per_chunk=10,
            lore="Common, dull, and load-bearing. Half the old roads are made of it."),
    OreSpec("petrichorite", "Petrichorite", "overworld", "petrichorite", "nodule", "stone",
            (USE_POTION, USE_DEVICE), 3, drop="petrichorite_crystal", experience=(2, 6),
            min_y=-24, max_y=56, vein_size=6, veins_per_chunk=7,
            lore="Smells of rain even when dry. Especially when dry."),
    OreSpec("sunscorch", "Sunscorch", "overworld", "sunscorch", "banded", "stone",
            (USE_TOOLS, USE_ARMOR, USE_DEVICE), 4, drop="sunscorch_ingot", experience=(4, 9),
            min_y=-56, max_y=16, vein_size=5, veins_per_chunk=6,
            lore="Warm to the touch at any depth. Nobody has found a cold seam yet."),
    OreSpec("glimmerleaf", "Glimmerleaf", "overworld", "glimmerleaf", "dendrite", "stone",
            (USE_POTION, USE_CRAFTING), 2, drop="glimmerleaf_fiber", experience=(1, 4),
            min_y=-16, max_y=64, vein_size=8, veins_per_chunk=11,
            lore="A mineral that grew the shape of a leaf and never stopped."),
    OreSpec("tideglass", "Tideglass", "overworld", "tideglass", "vein", "stone",
            (USE_BLOCK, USE_DEVICE), 2, drop="tideglass_pane", experience=(1, 3),
            min_y=-32, max_y=48, vein_size=10, veins_per_chunk=8,
            lore="Transparent, unbreakable by water, and always slightly wet."),
    OreSpec("emberquartz", "Emberquartz", "overworld", "emberquartz", "shard", "stone",
            (USE_TOOLS, USE_DEVICE), 3, drop="emberquartz_shard", drop_count=(1, 4), experience=(3, 8),
            min_y=-60, max_y=8, vein_size=6, veins_per_chunk=7,
            lore="Holds an ember that never consumes the crystal around it."),
    OreSpec("frostbloom", "Frostbloom", "overworld", "frostbloom", "spire", "stone",
            (USE_POTION, USE_ARMOR), 3, drop="frostbloom_bloom", experience=(2, 6),
            min_y=-40, max_y=40, vein_size=5, veins_per_chunk=6,
            lore="Blooms in cold, wilts in warmth, and never melts."),
    OreSpec("sporeamber", "Spore Amber", "overworld", "sporeamber", "nodule", "stone",
            (USE_POTION, USE_CRAFTING, USE_BLOCK), 2, drop="sporeamber_chunk", experience=(1, 5),
            min_y=-24, max_y=56, vein_size=7, veins_per_chunk=9,
            lore="Something is inside most of them. Something is moving inside some."),
    OreSpec("rootiron", "Rootiron", "overworld", "rootiron", "dendrite", "stone",
            (USE_TOOLS, USE_ARMOR, USE_CURRENCY), 2, drop="rootiron_ingot", experience=(2, 5),
            min_y=-56, max_y=40, vein_size=8, veins_per_chunk=12,
            lore="Iron that grew along a root and kept the grain. Smiths prefer it."),
    OreSpec("graveamber", "Grave Amber", "overworld", "graveamber", "cluster_large", "stone",
            (USE_POTION, USE_BOSS), 3, drop="graveamber_chunk", experience=(3, 7),
            min_y=-64, max_y=-8, vein_size=4, veins_per_chunk=4, rare=True,
            lore="Only found under barrows. Only ever under barrows."),
    OreSpec("wraithsalt", "Wraithsalt", "overworld", "wraithsalt", "speckle", "stone",
            (USE_POTION, USE_CRAFTING), 2, drop="wraithsalt_crystal", experience=(1, 4),
            min_y=-48, max_y=24, vein_size=9, veins_per_chunk=10,
            lore="Preserves meat indefinitely and ruins it completely at the same time."),
    OreSpec("bloodstone", "Bloodstone", "overworld", "bloodstone", "vein", "stone",
            (USE_TOOLS, USE_POTION), 4, drop="bloodstone_gem", experience=(4, 8),
            min_y=-64, max_y=0, vein_size=5, veins_per_chunk=5, rare=True,
            lore="The vein always runs toward the surface. Always. Dig along it if you like."),
    OreSpec("coralite", "Coralite", "overworld", "coralite", "cluster_large", "stone",
            (USE_ARMOR, USE_BLOCK), 2, drop="coralite_polish", experience=(1, 4),
            min_y=-24, max_y=48, vein_size=7, veins_per_chunk=8,
            lore="A reef that learned to grow in rock instead of water."),
    OreSpec("kelpstone", "Kelpstone", "overworld", "kelpstone", "banded", "stone",
            (USE_CRAFTING, USE_BLOCK), 1, experience=(0, 2),
            min_y=-16, max_y=56, vein_size=10, veins_per_chunk=9,
            lore="Stratified with pressed kelp. Each band is one season."),
    OreSpec("stormcell", "Stormcell", "overworld", "stormcell", "shard", "stone",
            (USE_TOOLS, USE_DEVICE), 4, drop="stormcell_core", experience=(4, 9),
            min_y=-48, max_y=24, vein_size=4, veins_per_chunk=4, rare=True,
            lore="A captured thunderhead, mineralised. Handle at arm's length."),
    OreSpec("glacierite", "Glacierite", "overworld", "glacierite", "spire", "stone",
            (USE_ARMOR, USE_BLOCK), 3, drop="glacierite_shard", experience=(2, 6),
            min_y=-40, max_y=40, vein_size=6, veins_per_chunk=6,
            lore="Cold enough to frost the air around it, permanently."),
    OreSpec("ashen_core", "Ashen Core", "overworld", "ashen_core", "nodule", "stone",
            (USE_TOOLS, USE_DEVICE, USE_BOSS), 4, drop="ashen_core_fragment", experience=(5, 10),
            min_y=-64, max_y=-16, vein_size=4, veins_per_chunk=4, rare=True,
            lore="The inside of a volcano that never quite finished erupting."),
    OreSpec("spiritwood", "Spiritwood Ore", "overworld", "spiritwood", "dendrite", "stone",
            (USE_CRAFTING, USE_POTION, USE_BLOCK), 2, drop="spiritwood_splinter", experience=(2, 5),
            min_y=-32, max_y=48, vein_size=7, veins_per_chunk=8,
            lore="Wood, in stone, still flexible. It bends. Do not think about it too long."),
    OreSpec("titanite", "Titanite", "overworld", "titanite", "banded", "stone",
            (USE_ARMOR, USE_CURRENCY, USE_BLOCK), 3, drop="titanite_plate", experience=(3, 7),
            min_y=-64, max_y=8, vein_size=6, veins_per_chunk=7,
            lore="Dense beyond reason. A single plate weighs as much as a door."),
]

# ---------------------------------------------------------------------------
#  24 DIMENSION ORES (8 per dimension)
# ---------------------------------------------------------------------------

DIMENSION_ORES: List[OreSpec] = [
    # ---- The Hollow Deep --------------------------------------------------
    OreSpec("hollowite", "Hollowite", "hollow_deep", "hollowite", "cluster_large", "hollow_stone",
            (USE_TOOLS, USE_ARMOR, USE_DEVICE, USE_BLOCK), 4,
            drop="hollowite_gem", experience=(4, 9), min_y=-56, max_y=48, vein_size=6, veins_per_chunk=8,
            lore="Glows brightest in total darkness, which is the only place to find it."),
    OreSpec("mycelium_ore", "Mycelium Ore", "hollow_deep", "mycelium_ore", "dendrite", "mycelial_slimestone",
            (USE_POTION, USE_CRAFTING), 3, drop="mycelium_culture", experience=(2, 6),
            min_y=-48, max_y=56, vein_size=8, veins_per_chunk=10,
            lore="Alive. The vein grows back if you leave it half-mined."),
    OreSpec("gloomite", "Gloomite", "hollow_deep", "gloomite", "shard", "gloomslate",
            (USE_TOOLS, USE_DEVICE), 4, drop="gloomite_shard", experience=(4, 8),
            min_y=-64, max_y=8, vein_size=5, veins_per_chunk=6,
            lore="Absorbs light. A lamp made of it is a very good lantern for hiding."),
    OreSpec("deep_pearl", "Deep Pearl", "hollow_deep", "deep_pearl", "nodule", "spore_chalk",
            (USE_ARMOR, USE_POTION, USE_CURRENCY), 3, drop="deep_pearl", experience=(3, 7),
            min_y=-40, max_y=32, vein_size=4, veins_per_chunk=5,
            lore="Grown, not mined. The Hollow Deep farms these and does not discuss it."),
    OreSpec("echo_crystal", "Echo Crystal", "hollow_deep", "echo_crystal", "spire", "gloomslate",
            (USE_DEVICE, USE_POTION), 4, drop="echo_crystal", experience=(4, 9),
            min_y=-64, max_y=0, vein_size=5, veins_per_chunk=5, rare=True,
            lore="Repeats the last sound it heard, once, about a minute later."),
    OreSpec("root_heart", "Root Heart", "hollow_deep", "root_heart", "cluster_large", "hollow_stone",
            (USE_BOSS, USE_POTION, USE_CRAFTING), 5, drop="root_heart_fragment", experience=(6, 12),
            min_y=-32, max_y=24, vein_size=3, veins_per_chunk=3, rare=True,
            lore="A knot of sap and stone that pulses. The Heart of the Forest feels every one you take."),
    OreSpec("lumenshade", "Lumenshade", "hollow_deep", "lumenshade", "vein", "hollow_stone",
            (USE_TOOLS, USE_ARMOR), 4, drop="lumenshade_ingot", experience=(4, 9),
            min_y=-56, max_y=32, vein_size=6, veins_per_chunk=7,
            lore="Light and shadow in the same seam, and neither one is winning."),
    OreSpec("basaltic_hollow_core", "Basaltic Hollow Core", "hollow_deep", "ashen_core", "banded", "basaltic_hollowstone",
            (USE_DEVICE, USE_BLOCK), 4, drop="basaltic_core", experience=(4, 8),
            min_y=-64, max_y=-8, vein_size=7, veins_per_chunk=6,
            lore="The only warm rock in a cold dimension, and it is warm all the way through."),

    # ---- Aetherfall -------------------------------------------------------
    OreSpec("aetherium", "Aetherium", "aetherfall", "aetherium", "cluster_large", "aetherstone",
            (USE_TOOLS, USE_ARMOR, USE_DEVICE, USE_BLOCK), 5,
            drop="aetherium_ingot", experience=(6, 12), min_y=-32, max_y=96, vein_size=5, veins_per_chunk=6,
            lore="Lighter than it should be. Armour made from it weighs almost nothing."),
    OreSpec("dawnshard", "Dawnshard", "aetherfall", "dawnshard", "shard", "dawn_marble",
            (USE_TOOLS, USE_CURRENCY), 4, drop="dawnshard", drop_count=(1, 4), experience=(4, 8),
            min_y=-16, max_y=112, vein_size=6, veins_per_chunk=8,
            lore="Splinters off the first light of the day, which up here lasts forever."),
    OreSpec("skylead", "Skylead", "aetherfall", "skylead", "speckle", "cloudstone",
            (USE_ARMOR, USE_BLOCK), 3, drop="skylead_ingot", experience=(2, 6),
            min_y=-24, max_y=120, vein_size=9, veins_per_chunk=10,
            lore="Lead that floats. Ballast for the sky citadels, in reverse."),
    OreSpec("starfall", "Starfall Ore", "aetherfall", "starfall", "nodule", "aetherstone",
            (USE_TOOLS, USE_DEVICE, USE_BOSS), 5, drop="starfall_core", experience=(6, 14),
            min_y=16, max_y=128, vein_size=4, veins_per_chunk=4, rare=True,
            lore="Impact glass with a core still warm from the fall. Still falling, some say."),
    OreSpec("stormcell_aether", "Aether Stormcell", "aetherfall", "stormcell", "vein", "twilight_shale",
            (USE_DEVICE, USE_TOOLS), 4, drop="stormcell_core", experience=(4, 9),
            min_y=-32, max_y=96, vein_size=5, veins_per_chunk=5,
            lore="The same mineral as below, and clearly not the same weather."),
    OreSpec("runeglass", "Runeglass", "aetherfall", "runeglass", "banded", "dawn_marble",
            (USE_DEVICE, USE_POTION, USE_CRAFTING), 4, drop="runeglass_pane", experience=(3, 8),
            min_y=-16, max_y=112, vein_size=7, veins_per_chunk=7,
            lore="Written in, not on. The runes are inside the glass, at depth."),
    OreSpec("moonpetal", "Moonpetal Ore", "aetherfall", "moonpetal", "dendrite", "aetherstone",
            (USE_POTION, USE_CRAFTING), 3, drop="moonpetal", experience=(2, 6),
            min_y=-8, max_y=120, vein_size=8, veins_per_chunk=9,
            lore="A flower that mineralised and kept opening anyway."),
    OreSpec("sunspore", "Sunspore", "aetherfall", "sunspore", "cluster_large", "gilded_aetherstone",
            (USE_POTION, USE_DEVICE), 4, drop="sunspore_pod", experience=(4, 8),
            min_y=0, max_y=128, vein_size=6, veins_per_chunk=7,
            lore="Drifts out of the seam and settles on anything warm. Including you."),

    # ---- The Void Between -------------------------------------------------
    OreSpec("voidsteel", "Voidsteel", "void_between", "voidsteel", "shard", "voidstone",
            (USE_TOOLS, USE_ARMOR, USE_DEVICE), 5, drop="voidsteel_ingot", experience=(6, 14),
            min_y=-64, max_y=64, vein_size=5, veins_per_chunk=6,
            lore="An alloy that was never made. It arrives already mixed."),
    OreSpec("nullite", "Nullite", "void_between", "nullite", "cluster_large", "null_basalt",
            (USE_TOOLS, USE_ARMOR, USE_BOSS), 5, drop="nullite_shard", experience=(6, 15),
            min_y=-64, max_y=48, vein_size=4, veins_per_chunk=4, rare=True,
            lore="Deletes what touches it, slowly, and only in one direction."),
    OreSpec("staticite", "Staticite", "void_between", "staticite", "speckle", "static_stone",
            (USE_DEVICE, USE_POTION), 4, drop="staticite_cell", experience=(4, 9),
            min_y=-48, max_y=64, vein_size=8, veins_per_chunk=9,
            lore="Hums. Gets louder near other staticite. Do not carry two pieces."),
    OreSpec("chronosite", "Chronosite", "void_between", "chronosite", "nodule", "fracture_shale",
            (USE_TOOLS, USE_DEVICE, USE_BOSS), 5, drop="chronosite_core", experience=(7, 16),
            min_y=-64, max_y=32, vein_size=3, veins_per_chunk=3, rare=True,
            lore="The seam is older at one end than the other. Both ends are the same age."),
    OreSpec("duskite", "Duskite", "void_between", "duskite", "vein", "voidstone",
            (USE_ARMOR, USE_POTION), 4, drop="duskite_gem", experience=(4, 9),
            min_y=-56, max_y=56, vein_size=6, veins_per_chunk=7,
            lore="Twilight, mineralised. It is dark near it even at noon."),
    OreSpec("witherite", "Witherite", "void_between", "witherite", "banded", "fracture_shale",
            (USE_TOOLS, USE_POTION), 4, drop="witherite_dust", experience=(4, 8),
            min_y=-64, max_y=16, vein_size=7, veins_per_chunk=8,
            lore="Everything near it ages. The ore itself does not."),
    OreSpec("fracture_shale_ore", "Fracture Shale Ore", "void_between", "fracture_shale", "spire", "fracture_shale",
            (USE_BLOCK, USE_CRAFTING), 3, drop="fracture_shale_shard", experience=(2, 5),
            min_y=-48, max_y=64, vein_size=9, veins_per_chunk=11,
            lore="Breaks along planes that are not in the rock."),
    OreSpec("glacierite_void", "Null Glacierite", "void_between", "glacierite", "cluster_large", "null_basalt",
            (USE_ARMOR, USE_DEVICE), 4, drop="glacierite_shard", experience=(4, 9),
            min_y=-64, max_y=8, vein_size=5, veins_per_chunk=6,
            lore="Cold that arrived from somewhere else and has no intention of leaving."),
]

ALL_ORES: List[OreSpec] = OVERWORLD_ORES + DIMENSION_ORES
ORE_BY_ID: Dict[str, OreSpec] = {}
for _o in ALL_ORES:
    if _o.id in ORE_BY_ID:
        raise ValueError(f"duplicate ore id {_o.id!r}")
    ORE_BY_ID[_o.id] = _o


def ores_in(dimension: str) -> List[OreSpec]:
    return [o for o in ALL_ORES if o.dimension == dimension]


def ore_by_id(ore_id: str) -> OreSpec:
    try:
        return ORE_BY_ID[ore_id]
    except KeyError:
        raise KeyError(f"unknown ore {ore_id!r}") from None
