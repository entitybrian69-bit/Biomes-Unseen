"""
content/gear.py -- tool and armour sets derived from the ore table.

Golden Rule #3: no flat colour swaps. Each set picks a *distinct silhouette*
from pixelart.gear_maps (the Void sword is serrated, the Hollow pickaxe is an
ancient flared bowl, the Chronos weapon is a floating-ring focus) and a
curated ramp from pixelart.palettes.GEAR_RAMPS. Sets that share a material
family share a silhouette only where that is the correct art direction.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Tool classes -> the gear_maps table that holds their silhouettes.
TOOL_CLASSES = ("sword", "pickaxe", "axe", "shovel", "hoe")
ARMOR_PIECES = ("helmet", "chestplate", "leggings", "boots")

# Which silhouette each material family uses per tool class.
# This is the art-direction table: it is what stops a Void sword from being
# a recoloured iron sword.
SILHOUETTES: Dict[str, Dict[str, str]] = {
    "lumenshade": {"sword": "straight",     "pickaxe": "standard",      "axe": "broad",
                   "helmet": "closed_helm"},
    "voidstone":  {"sword": "jagged_void",  "pickaxe": "void_hook",     "axe": "void_cleaver",
                   "helmet": "crowned_helm"},
    "aetherium":  {"sword": "celestial_estoc", "pickaxe": "winged",     "axe": "aether_hatchet",
                   "helmet": "crowned_helm"},
    "chronos":    {"sword": "celestial_estoc", "pickaxe": "standard",   "axe": "broad",
                   "helmet": "crowned_helm"},
    "pyroclast":  {"sword": "molten_cleaver", "pickaxe": "molten_block", "axe": "broad",
                   "helmet": "closed_helm"},
    "hollowite":  {"sword": "ancient_hollow", "pickaxe": "ancient_flared", "axe": "crescent",
                   "helmet": "closed_helm"},
    "rootiron":   {"sword": "straight",      "pickaxe": "standard",      "axe": "broad",
                   "helmet": "closed_helm"},
    "gloomsteel": {"sword": "jagged_void",   "pickaxe": "void_hook",     "axe": "crescent",
                   "helmet": "crowned_helm"},
    "nullite":    {"sword": "jagged_void",   "pickaxe": "molten_block",  "axe": "void_cleaver",
                   "helmet": "crowned_helm"},
    "starforged": {"sword": "celestial_estoc", "pickaxe": "winged",      "axe": "aether_hatchet",
                   "helmet": "crowned_helm"},
}

# Boss artefact weapons (the five staves) are one-off hero items.
ARTEFACT_WEAPONS: Dict[str, str] = {
    "heart_of_the_forest": "heart_of_forest_staff",
    "void_serpent": "void_serpent_fang",
    "warden_of_the_hollow_deep": "hollow_tremor_maul",
    "the_skyward_crown": "skyward_sceptre",
    "the_unraveling": "unraveling_conduit",
}


@dataclass(frozen=True)
class ToolSetSpec:
    id: str                     # material family id, matches a GEAR_RAMPS key
    name: str
    ramp: str                   # key into pixelart.palettes.GEAR_RAMPS
    tier: int                   # harvest level
    durability: int
    speed: float
    attack_damage_bonus: float
    enchantment_value: int
    repair_item: str
    tools: Tuple[str, ...] = TOOL_CLASSES
    has_bow: bool = False
    has_shield: bool = False
    lore: str = ""

    @property
    def silhouettes(self) -> Dict[str, str]:
        return SILHOUETTES.get(self.id, SILHOUETTES["rootiron"])

    def tool_id(self, tool_class: str) -> str:
        return f"biomesunseen:{self.id}_{tool_class}"


@dataclass(frozen=True)
class ArmorSetSpec:
    id: str
    name: str
    ramp: str
    durability_multiplier: int
    protection: Tuple[int, int, int, int]   # boots, leggings, chest, helmet
    toughness: float
    knockback_resistance: float
    pieces: Tuple[str, ...] = ARMOR_PIECES
    repair_item: str = ""
    helmet_silhouette: str = "closed_helm"
    set_bonus: str = ""
    lore: str = ""

    def piece_id(self, piece: str) -> str:
        return f"biomesunseen:{self.id}_{piece}"


# ---------------------------------------------------------------------------
#  10 TOOL SETS
# ---------------------------------------------------------------------------

TOOL_SETS: List[ToolSetSpec] = [
    ToolSetSpec("lumenshade", "Lumenshade", "lumenshade", 4, 1840, 11.0, 4.0, 26,
                "biomesunseen:lumenshade_ingot", has_bow=True,
                lore="Light and shadow in one seam. The tools settle the argument in favour of neither."),
    ToolSetSpec("voidstone", "Voidstone", "voidstone", 5, 2480, 13.0, 6.0, 30,
                "biomesunseen:voidsteel_ingot", has_bow=True, has_shield=True,
                lore="The blade is serrated because a clean edge would let the cut heal."),
    ToolSetSpec("aetherium", "Aetherium", "aetherium", 4, 1560, 15.0, 4.0, 34,
                "biomesunseen:aetherium_ingot", has_bow=True,
                lore="Almost weightless. Swings faster than the arm that swings it."),
    ToolSetSpec("chronos", "Chronos", "chronos", 5, 2100, 12.0, 5.0, 40,
                "biomesunseen:chronosite_core", has_bow=True, has_shield=True,
                lore="The focus ring is not attached to the haft. It has never been attached."),
    ToolSetSpec("pyroclast", "Pyroclast", "pyroclast", 4, 1980, 10.0, 7.0, 18,
                "biomesunseen:ashen_core_fragment", has_shield=True,
                lore="Heavy, hot, and it keeps whatever it cuts on fire for a while."),
    ToolSetSpec("hollowite", "Hollowite", "hollowite", 4, 2260, 9.0, 5.0, 22,
                "biomesunseen:hollowite_gem", has_bow=True,
                lore="Ancient flared bowl head. Chipped by something older than the chipping."),
    ToolSetSpec("rootiron", "Rootiron", "rootiron", 3, 890, 8.0, 3.0, 14,
                "biomesunseen:rootiron_ingot", has_bow=True, has_shield=True,
                lore="Iron with the grain still in it. Smiths prefer it and will tell you why."),
    ToolSetSpec("gloomsteel", "Gloomsteel", "gloomsteel", 4, 1720, 11.0, 5.0, 20,
                "biomesunseen:gloomite_shard", has_shield=True,
                lore="Absorbs light. A gloomsteel lantern is a very good way to hide."),
    ToolSetSpec("nullite", "Nullite", "nullite", 5, 3120, 14.0, 8.0, 12,
                "biomesunseen:nullite_shard", has_bow=True, has_shield=True,
                lore="Deletes what it touches, slowly, in one direction. Aim carefully."),
    ToolSetSpec("starforged", "Starforged", "starforged", 5, 2640, 14.0, 6.0, 36,
                "biomesunseen:starfall_core", has_bow=True, has_shield=True,
                lore="Forged from something that fell. It is still slightly warm from the fall."),
]

# ---------------------------------------------------------------------------
#  10 ARMOUR SETS
# ---------------------------------------------------------------------------

ARMOR_SETS: List[ArmorSetSpec] = [
    ArmorSetSpec("lumenshade", "Lumenshade", "lumenshade", 42, (3, 6, 8, 3), 2.0, 0.0,
                 repair_item="biomesunseen:lumenshade_ingot", helmet_silhouette="closed_helm",
                 set_bonus="lumenshade_glow",
                 lore="Wearer emits a low light. Useful, and impossible to hide with."),
    ArmorSetSpec("voidstone", "Voidstone", "voidstone", 48, (4, 7, 9, 4), 3.0, 0.1,
                 repair_item="biomesunseen:voidsteel_ingot", helmet_silhouette="crowned_helm",
                 set_bonus="voidstone_phase",
                 lore="The crown points backward. It is not a mistake and it is not decoration."),
    ArmorSetSpec("aetherium", "Aetherium", "aetherium", 36, (3, 6, 8, 3), 2.5, 0.0,
                 repair_item="biomesunseen:aetherium_ingot", helmet_silhouette="crowned_helm",
                 set_bonus="aetherium_flight_assist",
                 lore="So light the wearer has to remember they are wearing it."),
    ArmorSetSpec("chronos", "Chronos", "chronos", 44, (4, 7, 9, 4), 3.0, 0.15,
                 repair_item="biomesunseen:chronosite_core", helmet_silhouette="crowned_helm",
                 set_bonus="chronos_haste",
                 lore="Wearing it makes you slightly early. Slightly. Do not rely on it."),
    ArmorSetSpec("pyroclast", "Pyroclast", "pyroclast", 46, (4, 7, 9, 4), 3.5, 0.0,
                 repair_item="biomesunseen:ashen_core_fragment", helmet_silhouette="closed_helm",
                 set_bonus="pyroclast_fire_aura",
                 lore="Fireproof, and it makes the surrounding air share the opinion."),
    ArmorSetSpec("hollowite", "Hollowite", "hollowite", 50, (4, 8, 10, 4), 4.0, 0.1,
                 repair_item="biomesunseen:hollowite_gem", helmet_silhouette="closed_helm",
                 set_bonus="hollowite_night_vision",
                 lore="Made for total darkness. Every seam is lit so the wearer can be found."),
    ArmorSetSpec("rootiron", "Rootiron", "rootiron", 30, (2, 5, 7, 2), 1.0, 0.0,
                 repair_item="biomesunseen:rootiron_ingot", helmet_silhouette="closed_helm",
                 set_bonus="rootiron_regeneration",
                 lore="Cheap, tough, and every village smith can repair it. That is the point."),
    ArmorSetSpec("gloomsteel", "Gloomsteel", "gloomsteel", 40, (3, 6, 8, 3), 2.5, 0.1,
                 repair_item="biomesunseen:gloomite_shard", helmet_silhouette="crowned_helm",
                 set_bonus="gloomsteel_invisibility",
                 lore="Wearer is difficult to see. Also difficult for their own team to see."),
    ArmorSetSpec("nullite", "Nullite", "nullite", 54, (4, 8, 10, 4), 4.5, 0.2,
                 repair_item="biomesunseen:nullite_shard", helmet_silhouette="crowned_helm",
                 set_bonus="nullite_wither_aura",
                 lore="Best armour in the mod. It is also slowly deleting the wearer. Trade-off."),
    ArmorSetSpec("starforged", "Starforged", "starforged", 52, (4, 8, 10, 4), 4.0, 0.15,
                 repair_item="biomesunseen:starfall_core", helmet_silhouette="crowned_helm",
                 set_bonus="starforged_luck",
                 lore="Still warm. Still falling, in a sense nobody has managed to define."),
]

TOOL_SET_BY_ID: Dict[str, ToolSetSpec] = {t.id: t for t in TOOL_SETS}
ARMOR_SET_BY_ID: Dict[str, ArmorSetSpec] = {a.id: a for a in ARMOR_SETS}

ALL_TOOL_IDS: List[str] = [
    t.tool_id(c) for t in TOOL_SETS for c in t.tools
]
ALL_ARMOR_IDS: List[str] = [
    a.piece_id(p) for a in ARMOR_SETS for p in a.pieces
]
ARTEFACT_IDS: List[str] = [f"biomesunseen:{boss}_artefact" for boss in ARTEFACT_WEAPONS]


def tool_set(gear_id: str) -> ToolSetSpec:
    try:
        return TOOL_SET_BY_ID[gear_id]
    except KeyError:
        raise KeyError(f"unknown tool set {gear_id!r}") from None


def armor_set(gear_id: str) -> ArmorSetSpec:
    try:
        return ARMOR_SET_BY_ID[gear_id]
    except KeyError:
        raise KeyError(f"unknown armor set {gear_id!r}") from None
