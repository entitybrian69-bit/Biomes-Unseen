"""
content/mobs.py -- 55 mobs + 5 bosses.

Golden Rule #2: every entity here is rendered from a real GeckoLib `.geo.json`
model plus an `.animation.json` set. No CubeListBuilder, no ModelPart.

Golden Rule #5: every hostile entity declares its AI goal loadout explicitly.
The codegen emits `MeleeAttackGoal`, `HurtByTargetGoal` and
`NearestAttackableTargetGoal` for anything marked `hostile`, and refuses to
generate a hostile mob whose `goals` tuple is empty.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# Creature atlas families authored in pixelart/creature_maps.py
FAMILIES = ("quadruped", "arthropod", "biped", "serpent", "avian", "fungal")

# Animation clips every entity must ship (Golden Rule #2: idle breathing,
# walk cycle, attack, hit reaction, death).
REQUIRED_ANIMATIONS = (
    "animation.idle",
    "animation.walk",
    "animation.attack",
    "animation.hurt",
    "animation.death",
)

BEHAVIOUR_TAGS = (
    "herding", "tamable", "trading", "pack_tactics", "environmental_adaptation",
    "ambush", "aerial", "aquatic", "burrowing", "bioluminescent", "phase_shift",
    "summoner", "ranged", "boss",
)


@dataclass(frozen=True)
class MobSpec:
    id: str
    name: str
    family: str                    # key into pixelart.creature_maps.FAMILIES
    dimension: str                 # overworld | hollow_deep | aetherfall | void_between
    category: str                  # creature role, mirrors biome categories
    hostile: bool = False

    # --- palette -----------------------------------------------------------
    skin: str = "#8A7A6A"
    hide: str = "#5A4E44"
    accent: str = "#C8A06A"
    eye: str = "#FFE066"
    bone: str = "#E8DCC0"

    # --- species detail: hand-placed overlay ids from creature_maps.OVERLAYS
    overlays: Tuple[str, ...] = ()

    # --- attributes --------------------------------------------------------
    max_health: float = 20.0
    movement_speed: float = 0.28
    attack_damage: float = 3.0
    attack_knockback: float = 0.0
    follow_range: float = 24.0
    armour: float = 0.0
    scale: float = 1.0
    fire_immune: bool = False
    can_breathe_underwater: bool = False

    # --- AI ----------------------------------------------------------------
    goals: Tuple[str, ...] = ()
    behaviour_tags: Tuple[str, ...] = ()
    target_classes: Tuple[str, ...] = ("minecraft:player",)

    # --- model / render ----------------------------------------------------
    model_width: float = 1.0
    model_height: float = 1.0
    geo: str = ""                  # filename under geo/entity/ ; default derived
    shadow_radius: float = 0.4
    animations: Tuple[str, ...] = REQUIRED_ANIMATIONS
    render_layer: str = "cutout"   # cutout | translucent | eyes

    # --- spawns ------------------------------------------------------------
    spawn_biomes: Tuple[str, ...] = ()
    spawn_weight: int = 20
    spawn_group: Tuple[int, int] = (1, 3)
    spawn_category: str = "creature"   # creature | monster | ambient | water_creature

    # --- drops / xp --------------------------------------------------------
    drops: Tuple[Tuple[str, int, int, float], ...] = ()   # (item, min, max, chance)
    experience: int = 5

    lore: str = ""

    def __post_init__(self) -> None:
        if self.family not in FAMILIES:
            raise ValueError(f"{self.id}: unknown creature family {self.family!r}")
        if self.hostile and not self.goals:
            raise ValueError(
                f"{self.id}: Golden Rule #5 violation - a hostile mob must declare its AI goals"
            )
        missing = [a for a in REQUIRED_ANIMATIONS if a not in self.animations]
        if missing:
            raise ValueError(f"{self.id}: missing required animations {missing}")
        for tag in self.behaviour_tags:
            if tag not in BEHAVIOUR_TAGS:
                raise ValueError(f"{self.id}: unknown behaviour tag {tag!r}")

    @property
    def entity_type_id(self) -> str:
        return f"biomesunseen:{self.id}"

    @property
    def geo_path(self) -> str:
        return f"geo/entity/{self.geo or self.id}.geo.json"

    @property
    def animation_path(self) -> str:
        return f"animations/entity/{self.geo or self.id}.animation.json"

    @property
    def texture_path(self) -> str:
        return f"textures/entity/{self.id}.png"


# ---------------------------------------------------------------------------
#  Goal presets. The codegen maps each of these to a real registered Goal
#  class in com.biomesunseen.entity.ai, so a mob's behaviour is declared here
#  and *implemented* in Java -- never left as dead AI.
# ---------------------------------------------------------------------------

GOAL_HOSTILE_MELEE = (
    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
    "look_at_player", "random_look_around", "water_avoiding_random_stroll",
)
GOAL_HOSTILE_PACK = (
    "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
    "pack_call_for_help", "avoid_creeper", "look_at_player", "water_avoiding_random_stroll",
)
GOAL_HOSTILE_RANGED = (
    "float", "ranged_attack", "melee_attack", "hurt_by_target",
    "nearest_attackable_target_player", "look_at_player", "water_avoiding_random_stroll",
)
GOAL_HOSTILE_AMBUSH = (
    "float", "ambush_lie_in_wait", "melee_attack", "hurt_by_target",
    "nearest_attackable_target_player", "look_at_player", "water_avoiding_random_stroll",
)
GOAL_PASSIVE_HERD = (
    "float", "panic", "breed", "tempt", "follow_parent", "herd_follow_leader",
    "eat_block", "look_at_player", "random_look_around", "water_avoiding_random_stroll",
)
GOAL_PASSIVE_TAMABLE = (
    "float", "panic", "sit_when_ordered", "follow_owner", "owner_hurt_by_target",
    "owner_hurt_target", "breed", "tempt", "look_at_player", "water_avoiding_random_stroll",
)
GOAL_PASSIVE_TRADER = (
    "float", "trade_with_player", "look_at_trading_player", "panic", "tempt",
    "open_door", "look_at_player", "water_avoiding_random_stroll",
)
GOAL_AQUATIC = (
    "swim_random", "swim_toward_player", "melee_attack", "hurt_by_target",
    "nearest_attackable_target_player", "look_at_player", "follow_flock_leader",
)
GOAL_AERIAL = (
    "fly_random", "swoop_attack", "melee_attack", "hurt_by_target",
    "nearest_attackable_target_player", "land_on_ground", "look_at_player",
    "follow_flock_leader",
)
GOAL_ENVIRONMENTAL = (
    "float", "seek_shelter_from_sun", "seek_bioluminescence", "panic", "tempt",
    "look_at_player", "water_avoiding_random_stroll",
)

# ---------------------------------------------------------------------------
#  25 OVERWORLD MOBS
# ---------------------------------------------------------------------------

OVERWORLD_MOBS: List[MobSpec] = [
    MobSpec("glimmerwing", "Glimmerwing", "avian", "overworld", "ethereal",
            skin="#C8F5A0", hide="#8FD96A", accent="#FFF6C2", eye="#FFFFFF", bone="#F0E8C0",
            overlays=("bioluminescent_freckles", "crest"),
            max_health=8.0, movement_speed=0.34, scale=0.5,
            goals=("float", "fly_random", "tempt", "look_at_player", "follow_flock_leader"),
            behaviour_tags=("herding", "bioluminescent", "aerial"),
            render_layer="translucent", shadow_radius=0.25, model_width=0.5, model_height=0.5,
            spawn_biomes=("luminescent_grove", "starfall_glade", "glimmerleaf_woodland",
                          "glimmering_thicket", "veilwood"),
            spawn_weight=40, spawn_group=(3, 6), spawn_category="ambient",
            drops=(("biomesunseen:glimmerleaf_fiber", 0, 2, 0.6),), experience=2,
            lore="A moth the size of a hand that carries its own lamp."),

    MobSpec("mossback_hare", "Mossback Hare", "quadruped", "overworld", "ethereal",
            skin="#8FA06B", hide="#6E8355", accent="#B8C890", eye="#2A2A20", bone="#E0D8B8",
            overlays=("moss_growth",),
            max_health=6.0, movement_speed=0.4, scale=0.7,
            goals=GOAL_PASSIVE_HERD, behaviour_tags=("herding", "environmental_adaptation"),
            shadow_radius=0.3, model_width=0.6, model_height=0.6,
            spawn_biomes=("luminescent_grove", "moonpetal_meadow", "lumenshade_glade",
                          "harvest_hollows", "bloomfield"),
            spawn_weight=25, spawn_group=(2, 4),
            drops=(("minecraft:rabbit_hide", 0, 1, 0.5), ("biomesunseen:glimmerleaf_fiber", 0, 1, 0.3)),
            experience=2,
            lore="Grows moss on its back to match whatever it is hiding in."),

    MobSpec("petaldancer", "Petaldancer", "biped", "overworld", "ethereal",
            skin="#E0A8C0", hide="#C888A8", accent="#FFF0FA", eye="#5A2A4A", bone="#F8E8F0",
            overlays=("crest", "no_marking"),
            max_health=12.0, movement_speed=0.32, scale=0.9,
            goals=GOAL_PASSIVE_HERD, behaviour_tags=("herding",),
            spawn_biomes=("moonpetal_meadow", "petal_drift_flats", "sakura_highlands",
                          "bloomfield", "marigold_march"),
            spawn_weight=30, spawn_group=(2, 5),
            drops=(("biomesunseen:moonpetal", 0, 2, 0.7),), experience=3,
            lore="Dances. The petals fall where it steps. This is not a metaphor."),

    MobSpec("duskstalker", "Duskstalker", "quadruped", "overworld", "ethereal", hostile=True,
            skin="#45224C", hide="#311739", accent="#7355D1", eye="#C8B4FF", bone="#8A7AA0",
            overlays=("eyes_glowing", "claws_long"),
            max_health=24.0, movement_speed=0.33, attack_damage=5.0, armour=2.0,
            goals=GOAL_HOSTILE_AMBUSH, behaviour_tags=("ambush", "pack_tactics"),
            spawn_category="monster",
            spawn_biomes=("duskwood_hollow", "veilwood", "ghostlight_marsh", "witherwood"),
            spawn_weight=25, spawn_group=(1, 2),
            drops=(("biomesunseen:duskite_gem", 0, 1, 0.4), ("minecraft:leather", 0, 2, 0.5)),
            experience=8,
            lore="Only visible in the corner of your eye. It knows this and uses it."),

    MobSpec("sporeling", "Sporeling", "fungal", "overworld", "ethereal",
            skin="#D8E8A0", hide="#B0C870", accent="#F0E0A0", eye="#5A6A2A", bone="#E8E0C0",
            overlays=("mushroom_cap", "spore_vents"),
            max_health=10.0, movement_speed=0.24, scale=0.75,
            goals=GOAL_ENVIRONMENTAL, behaviour_tags=("herding", "bioluminescent",
                                                     "environmental_adaptation"),
            spawn_biomes=("duskwood_hollow", "whispering_mire", "sunspore_barrens",
                          "ghostlight_marsh", "rootdeep_hollow"),
            spawn_weight=35, spawn_group=(3, 6),
            drops=(("biomesunseen:sporeamber_chunk", 0, 2, 0.6),), experience=3,
            lore="A mushroom that decided to walk. It has not decided where."),

    MobSpec("mire_wisp", "Mire Wisp", "fungal", "overworld", "ethereal",
            skin="#C8FFF4", hide="#7CF0DC", accent="#FFFFFF", eye="#3FCDB4", bone="#DFFFF8",
            overlays=("bioluminescent_freckles",),
            max_health=8.0, movement_speed=0.3, scale=0.55,
            goals=("float", "fly_random", "seek_bioluminescence", "look_at_player"),
            behaviour_tags=("bioluminescent", "aerial", "environmental_adaptation"),
            render_layer="translucent", shadow_radius=0.2, fire_immune=True,
            spawn_category="ambient",
            spawn_biomes=("whispering_mire", "ghostlight_marsh", "blackwater_bog",
                          "hollowlight_basin"),
            spawn_weight=30, spawn_group=(1, 3),
            drops=(("biomesunseen:hollowite_gem", 0, 1, 0.25),), experience=2,
            lore="Leads travellers somewhere. It is not trying to help or to harm."),

    MobSpec("bogcrawler", "Bogcrawler", "arthropod", "overworld", "ethereal", hostile=True,
            skin="#4F7746", hide="#3A5A35", accent="#8FBF7A", eye="#E6FFC8", bone="#C6CBB2",
            overlays=("segment_bands", "claws_long"),
            max_health=18.0, movement_speed=0.28, attack_damage=4.0, armour=3.0,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("ambush", "aquatic",
                                                     "environmental_adaptation"),
            can_breathe_underwater=True, spawn_category="monster",
            spawn_biomes=("whispering_mire", "ghostlight_marsh", "brine_marsh",
                          "blackwater_bog", "mangrove_labyrinth"),
            spawn_weight=30, spawn_group=(1, 3),
            drops=(("biomesunseen:sporeamber_chunk", 0, 1, 0.4),), experience=6,
            lore="Half crab, half something worse, entirely at home in the mud."),

    MobSpec("aurora_stag", "Aurora Stag", "quadruped", "overworld", "ethereal",
            skin="#A8DCE8", hide="#88C0D8", accent="#E0FFFF", eye="#FFFFFF", bone="#F0FFFF",
            overlays=("antlers", "bioluminescent_freckles"),
            max_health=28.0, movement_speed=0.34, scale=1.25,
            goals=GOAL_PASSIVE_HERD, behaviour_tags=("herding", "bioluminescent", "tamable"),
            spawn_biomes=("aurora_steppe", "crystalline_tundra", "rimeforest"),
            spawn_weight=18, spawn_group=(2, 4),
            drops=(("biomesunseen:glacierite_shard", 0, 2, 0.5),), experience=6,
            lore="Its antlers show the aurora. On clear nights this is a disadvantage."),

    MobSpec("thicket_sprite", "Thicket Sprite", "biped", "overworld", "ethereal",
            skin="#B6F28C", hide="#7FD95A", accent="#FFFBE0", eye="#2A4A14", bone="#E8FFD0",
            overlays=("crest", "claws_long"),
            max_health=10.0, movement_speed=0.35, scale=0.5,
            goals=GOAL_PASSIVE_TRADER, behaviour_tags=("trading", "herding"),
            spawn_biomes=("glimmering_thicket", "luminescent_grove", "silken_canopy",
                          "glimmerleaf_woodland"),
            spawn_weight=20, spawn_group=(1, 2), spawn_category="ambient",
            drops=(("biomesunseen:glimmerleaf_fiber", 0, 3, 0.8),), experience=4,
            lore="Will trade. Wants seeds. Is extremely firm about the exchange rate."),

    MobSpec("silkweaver", "Silkweaver", "arthropod", "overworld", "ethereal", hostile=True,
            skin="#CBD8EC", hide="#A9BAD6", accent="#FFFFFF", eye="#4F5D7A", bone="#E8EFFA",
            overlays=("segment_bands",),
            max_health=16.0, movement_speed=0.26, attack_damage=3.5,
            goals=GOAL_HOSTILE_RANGED, behaviour_tags=("ranged", "ambush"),
            spawn_category="monster",
            spawn_biomes=("silken_canopy", "glimmering_thicket", "verdantheight"),
            spawn_weight=22, spawn_group=(2, 3),
            drops=(("minecraft:string", 1, 3, 0.9),), experience=5,
            lore="Weaves between branches. You notice the web after you are in it."),

    MobSpec("canopy_glider", "Canopy Glider", "quadruped", "overworld", "ethereal",
            skin="#8AA2D6", hide="#6179AE", accent="#DCE6FF", eye="#FFE066", bone="#E8E0D0",
            overlays=("wing_membrane",),
            max_health=14.0, movement_speed=0.33, scale=0.8,
            goals=GOAL_PASSIVE_HERD, behaviour_tags=("herding", "aerial"),
            spawn_biomes=("silken_canopy", "verdantheight", "mangrove_labyrinth"),
            spawn_weight=20, spawn_group=(1, 3),
            drops=(("minecraft:leather", 0, 2, 0.5),), experience=4,
            lore="A membrane between wrist and ankle and a great deal of confidence."),

    MobSpec("frostling", "Frostling", "biped", "overworld", "harsh", hostile=True,
            skin="#AFDCFA", hide="#7BB8E8", accent="#FFFFFF", eye="#2C5F8C", bone="#E8F4FF",
            overlays=("crown_shards",),
            max_health=16.0, movement_speed=0.3, attack_damage=4.0,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("pack_tactics", "environmental_adaptation"),
            spawn_category="monster",
            spawn_biomes=("crystalline_tundra", "frozen_expanse", "grave_ice_field",
                          "glacier_maw", "rimeforest", "glacial_lake"),
            spawn_weight=30, spawn_group=(2, 4),
            drops=(("biomesunseen:glacierite_shard", 0, 2, 0.6),), experience=5,
            lore="Made of the cold, and offended by anything warmer."),

    MobSpec("glacier_ox", "Glacier Ox", "quadruped", "overworld", "harsh",
            skin="#B0D0D8", hide="#90B8C0", accent="#E0F0F8", eye="#2A3A48", bone="#F0F8FF",
            overlays=("hooves_cloven", "barding"),
            max_health=40.0, movement_speed=0.24, armour=4.0, scale=1.4,
            goals=GOAL_PASSIVE_HERD, behaviour_tags=("herding", "environmental_adaptation"),
            spawn_biomes=("crystalline_tundra", "frozen_expanse", "glacier_maw"),
            spawn_weight=15, spawn_group=(2, 4),
            drops=(("minecraft:beef", 1, 3, 0.9), ("minecraft:leather", 1, 3, 0.8),
                   ("biomesunseen:glacierite_shard", 0, 1, 0.3)), experience=8,
            lore="Pulls sledges through drifts that would bury a horse."),

    MobSpec("stonehide_boar", "Stonehide Boar", "quadruped", "overworld", "ancient", hostile=True,
            skin="#9C8D7A", hide="#7E7061", accent="#B39A78", eye="#8A2A10", bone="#D8CDB8",
            overlays=("tusks", "barding"),
            max_health=26.0, movement_speed=0.32, attack_damage=5.0, armour=5.0,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("herding", "pack_tactics"),
            spawn_category="monster",
            spawn_biomes=("petrified_forest", "petrified_colossi", "old_king_road",
                          "harvest_hollows", "ironstone_ravine", "bronze_steppe"),
            spawn_weight=20, spawn_group=(2, 4),
            drops=(("minecraft:porkchop", 1, 3, 0.9), ("biomesunseen:umbrite", 0, 2, 0.4)),
            experience=7,
            lore="Hide that has gone the way of the forest it lives in."),

    MobSpec("fossil_wraith", "Fossil Wraith", "biped", "overworld", "ancient", hostile=True,
            skin="#E8DCC0", hide="#B8A98A", accent="#9A9A88", eye="#C8FFF4", bone="#F0E8D0",
            overlays=("scar", "eyes_glowing"),
            max_health=20.0, movement_speed=0.3, attack_damage=5.5,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("ambush",),
            render_layer="translucent", fire_immune=True, spawn_category="monster",
            spawn_biomes=("colossal_boneyard", "ashen_necropolis", "petrified_forest",
                          "titan_graveyard", "petrified_colossi"),
            spawn_weight=25, spawn_group=(1, 2),
            drops=(("minecraft:bone", 1, 3, 0.9), ("biomesunseen:graveamber_chunk", 0, 1, 0.15)),
            experience=8,
            lore="The skeleton is still articulated. That is the worrying part."),

    MobSpec("marrow_hound", "Marrow Hound", "quadruped", "overworld", "ancient", hostile=True,
            skin="#D8CDB8", hide="#A89A80", accent="#8A7A60", eye="#FF6A4A", bone="#F0E8D0",
            overlays=("claws_long", "tusks"),
            max_health=22.0, movement_speed=0.38, attack_damage=6.0,
            goals=GOAL_HOSTILE_PACK, behaviour_tags=("pack_tactics",),
            spawn_category="monster",
            spawn_biomes=("colossal_boneyard", "titan_graveyard", "ashen_necropolis"),
            spawn_weight=25, spawn_group=(2, 3),
            drops=(("minecraft:bone", 2, 4, 0.9),), experience=7,
            lore="Hunts in packs and coordinates. The coordination is the problem."),

    MobSpec("temple_guardian", "Temple Guardian", "biped", "overworld", "ancient", hostile=True,
            skin="#93ABD8", hide="#7189B8", accent="#FFE9A8", eye="#FFE066", bone="#D6C7A6",
            overlays=("barding", "crown_shards"),
            max_health=36.0, movement_speed=0.28, attack_damage=7.0, armour=6.0, scale=1.3,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("pack_tactics", "environmental_adaptation"),
            spawn_category="monster",
            spawn_biomes=("sunken_temple_reach", "flooded_ruins", "sunken_cathedral",
                          "monolith_shore"),
            spawn_weight=20, spawn_group=(1, 2),
            drops=(("biomesunseen:titanite_plate", 0, 2, 0.5),
                   ("biomesunseen:lore_fragment", 0, 1, 0.2)), experience=12,
            lore="Still guarding. Still on duty. Still furious about the flooding."),

    MobSpec("astral_scribe", "Astral Scribe", "biped", "overworld", "ancient",
            skin="#8471BE", hide="#5C4B94", accent="#F4F0FF", eye="#E0FFFF", bone="#D6CCF5",
            overlays=("no_marking", "scar"),
            max_health=18.0, movement_speed=0.26, scale=0.95,
            goals=GOAL_PASSIVE_TRADER, behaviour_tags=("trading",),
            spawn_biomes=("ruined_observatory", "shattered_archive", "gilded_archive",
                          "hymn_halls", "memory_vault"),
            spawn_weight=18, spawn_group=(1, 1),
            drops=(("biomesunseen:lore_fragment", 1, 2, 0.8), ("minecraft:paper", 1, 3, 0.9)),
            experience=6,
            lore="Writing something down. Has been for centuries. Is nearly finished."),

    MobSpec("moor_sentinel", "Moor Sentinel", "biped", "overworld", "ancient", hostile=True,
            skin="#7E7061", hide="#4E463D", accent="#9C8D7A", eye="#FFE066", bone="#B39A78",
            overlays=("barding", "crown_shards"),
            max_health=34.0, movement_speed=0.25, attack_damage=8.0, armour=8.0, scale=1.5,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("environmental_adaptation",),
            spawn_category="monster",
            spawn_biomes=("megalith_moor", "bronze_steppe", "old_king_road"),
            spawn_weight=12, spawn_group=(1, 1),
            drops=(("biomesunseen:umbrite", 1, 3, 0.7), ("biomesunseen:titanite_plate", 0, 1, 0.3)),
            experience=14,
            lore="One of the standing stones. There were thirty. Count them again."),

    MobSpec("slag_golem", "Slag Golem", "biped", "overworld", "harsh", hostile=True,
            skin="#6B6570", hide="#3E3943", accent="#FF8A3C", eye="#FFE0A0", bone="#524C58",
            overlays=("barding",),
            max_health=44.0, movement_speed=0.22, attack_damage=9.0, armour=10.0, scale=1.6,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("environmental_adaptation",),
            fire_immune=True, spawn_category="monster",
            spawn_biomes=("forged_waste", "obsidian_shelf", "pyroclast_fields",
                          "ashen_caldera", "sulphur_vents"),
            spawn_weight=15, spawn_group=(1, 1),
            drops=(("biomesunseen:ashen_core_fragment", 0, 1, 0.3),
                   ("minecraft:iron_nugget", 2, 6, 0.8)), experience=16,
            lore="A forge that never got shut down properly."),

    MobSpec("emberling", "Emberling", "fungal", "overworld", "harsh", hostile=True,
            skin="#FF9E5C", hide="#F26A28", accent="#FFF2B0", eye="#FFFFFF", bone="#FFD9A0",
            overlays=("bioluminescent_freckles",),
            max_health=12.0, movement_speed=0.34, attack_damage=4.0, scale=0.7,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("pack_tactics", "environmental_adaptation"),
            fire_immune=True, render_layer="translucent", spawn_category="monster",
            spawn_biomes=("pyroclast_fields", "emberfall_ridge", "cinder_dunes",
                          "sulphur_vents", "ashen_caldera", "basaltic_fissures"),
            spawn_weight=32, spawn_group=(2, 5),
            drops=(("minecraft:blaze_powder", 0, 1, 0.3), ("biomesunseen:emberquartz_shard", 0, 2, 0.5)),
            experience=5,
            lore="A coal that got ambitious."),

    MobSpec("magma_lurker", "Magma Lurker", "arthropod", "overworld", "harsh", hostile=True,
            skin="#C4421A", hide="#8E2A0F", accent="#FFE2C0", eye="#FFD35C", bone="#A8520A",
            overlays=("segment_bands", "claws_long"),
            max_health=30.0, movement_speed=0.26, attack_damage=7.0, armour=6.0, scale=1.2,
            goals=GOAL_HOSTILE_AMBUSH, behaviour_tags=("ambush", "environmental_adaptation"),
            fire_immune=True, spawn_category="monster",
            spawn_biomes=("volcanic_wasteland", "obsidian_shelf", "ashen_caldera",
                          "basaltic_fissures"),
            spawn_weight=22, spawn_group=(1, 2),
            drops=(("biomesunseen:ashen_core_fragment", 0, 2, 0.6),), experience=10,
            lore="Lives in the lava, hunts on the bank, prefers you to come to it."),

    MobSpec("canyon_skulk", "Canyon Skulk", "quadruped", "overworld", "harsh", hostile=True,
            skin="#BBA98A", hide="#9A8A6E", accent="#D6C7A6", eye="#FFE066", bone="#EFE3C6",
            overlays=("claws_long", "scar"),
            max_health=20.0, movement_speed=0.36, attack_damage=5.5,
            goals=GOAL_HOSTILE_AMBUSH, behaviour_tags=("ambush", "pack_tactics",
                                                      "environmental_adaptation"),
            spawn_category="monster",
            spawn_biomes=("hieroglyph_canyon", "sunscorch_badlands", "ironstone_ravine",
                          "scorched_glassland", "whitewater_gorge"),
            spawn_weight=24, spawn_group=(1, 3),
            drops=(("minecraft:leather", 0, 2, 0.6),), experience=7,
            lore="Colour-matched to the rock. It stays very still and is very patient."),

    MobSpec("sunscorch_vulture", "Sunscorch Vulture", "avian", "overworld", "harsh", hostile=True,
            skin="#A08B6E", hide="#7E6B52", accent="#C7B49A", eye="#FF6A4A", bone="#E8DCC0",
            overlays=("beak_hooked",),
            max_health=14.0, movement_speed=0.32, attack_damage=4.5, scale=0.9,
            goals=GOAL_AERIAL, behaviour_tags=("aerial", "pack_tactics"),
            spawn_category="monster",
            spawn_biomes=("sunscorch_badlands", "cinder_dunes", "saltflat_mirage",
                          "scorched_glassland", "colossal_boneyard"),
            spawn_weight=22, spawn_group=(1, 3),
            drops=(("minecraft:feather", 1, 3, 0.9),), experience=5,
            lore="Circles. It is very good at circles and very patient about them."),

    MobSpec("blighthound", "Blighthound", "quadruped", "overworld", "harsh", hostile=True,
            skin="#6A6A58", hide="#4A4A38", accent="#8A8A70", eye="#B0FF6A", bone="#9A9A88",
            overlays=("claws_long", "scar"),
            max_health=24.0, movement_speed=0.37, attack_damage=6.0,
            goals=GOAL_HOSTILE_PACK, behaviour_tags=("pack_tactics", "environmental_adaptation"),
            spawn_category="monster",
            spawn_biomes=("blighted_marches", "witherwood", "wither_veil"),
            spawn_weight=28, spawn_group=(2, 4),
            drops=(("biomesunseen:witherite_dust", 0, 2, 0.5),), experience=8,
            lore="Mange is the wrong word. Nothing is growing back."),

    MobSpec("rotstalker", "Rotstalker", "biped", "overworld", "harsh", hostile=True,
            skin="#6A7A40", hide="#4A5A28", accent="#8A9A50", eye="#E0FF8A", bone="#A0A850",
            overlays=("scar", "moss_growth"),
            max_health=22.0, movement_speed=0.3, attack_damage=5.5, armour=2.0,
            goals=GOAL_HOSTILE_AMBUSH, behaviour_tags=("ambush", "environmental_adaptation"),
            spawn_category="monster",
            spawn_biomes=("blighted_marches", "witherwood", "blackwater_bog"),
            spawn_weight=22, spawn_group=(1, 2),
            drops=(("biomesunseen:witherite_dust", 0, 1, 0.4),), experience=7,
            lore="Stands in the treeline and does not need to breathe."),

    MobSpec("reefglider", "Reefglider", "serpent", "overworld", "aquatic",
            skin="#79D6E8", hide="#4BACC6", accent="#EAFDFF", eye="#FFE066", bone="#B2EEF7",
            overlays=("fin_fan", "gills"),
            max_health=12.0, movement_speed=0.34, scale=0.9, can_breathe_underwater=True,
            goals=("swim_random", "follow_flock_leader", "tempt", "look_at_player"),
            behaviour_tags=("herding", "aquatic"),
            spawn_biomes=("coral_shallows", "jewel_reef", "kelp_cathedral", "tidal_flats",
                          "seagrass_meadow", "coral_atoll_ring", "pearl_beds", "orchid_lagoon"),
            spawn_weight=40, spawn_group=(3, 6), spawn_category="water_creature",
            drops=(("biomesunseen:coralite_polish", 0, 2, 0.6),), experience=3,
            lore="Flies through water the way other fish swim."),

    MobSpec("coralback_crab", "Coralback Crab", "arthropod", "overworld", "aquatic",
            skin="#F07A6C", hide="#C74E45", accent="#FFE8E0", eye="#2A0A08", bone="#FFB0A0",
            overlays=("segment_bands", "claws_long"),
            max_health=16.0, movement_speed=0.22, attack_damage=4.0, armour=8.0, scale=0.85,
            goals=("swim_random", "melee_attack", "hurt_by_target",
                   "nearest_attackable_target_player", "look_at_player"),
            behaviour_tags=("aquatic", "herding", "ambush"), hostile=True,
            can_breathe_underwater=True, spawn_category="water_creature",
            spawn_biomes=("coral_shallows", "tidal_flats", "jewel_reef", "coral_atoll_ring",
                          "pearl_beds"),
            spawn_weight=30, spawn_group=(2, 5),
            drops=(("biomesunseen:coralite_polish", 1, 3, 0.8),), experience=5,
            lore="Wears a reef. The reef is doing well."),

    MobSpec("shorelurker", "Shorelurker", "serpent", "overworld", "aquatic", hostile=True,
            skin="#4E97C4", hide="#35709B", accent="#A9DCF5", eye="#FFE066", bone="#74BEE4",
            overlays=("fin_fan", "tusks"),
            max_health=22.0, movement_speed=0.3, attack_damage=5.5, can_breathe_underwater=True,
            goals=GOAL_AQUATIC, behaviour_tags=("aquatic", "ambush"),
            spawn_category="water_creature",
            spawn_biomes=("monolith_shore", "tidal_flats", "flooded_ruins", "brine_marsh"),
            spawn_weight=20, spawn_group=(1, 2),
            drops=(("biomesunseen:tideglass_pane", 0, 2, 0.5),), experience=7,
            lore="Waits in the shallows for something to wade out."),

    MobSpec("river_lamprey", "River Lamprey", "serpent", "overworld", "aquatic", hostile=True,
            skin="#5A8A5A", hide="#3A6A3A", accent="#8AB878", eye="#FFE066", bone="#A0C890",
            overlays=("gills", "no_marking"),
            max_health=10.0, movement_speed=0.36, attack_damage=3.5, scale=0.7,
            can_breathe_underwater=True, goals=GOAL_AQUATIC, behaviour_tags=("aquatic", "pack_tactics"),
            spawn_category="water_creature",
            spawn_biomes=("river_of_lights", "whitewater_gorge", "brine_marsh",
                          "geyser_lagoon", "glacial_lake"),
            spawn_weight=25, spawn_group=(2, 4),
            drops=(("biomesunseen:petrichorite_crystal", 0, 1, 0.3),), experience=4,
            lore="Travels upstream in a straight line regardless of obstacles."),

    MobSpec("kelp_serpent", "Kelp Serpent", "serpent", "overworld", "aquatic", hostile=True,
            skin="#6CC24E", hide="#459630", accent="#D8FFC0", eye="#FFE066", bone="#9EE87E",
            overlays=("fin_fan", "gills"),
            max_health=32.0, movement_speed=0.32, attack_damage=7.0, scale=1.5,
            can_breathe_underwater=True, goals=GOAL_AQUATIC, behaviour_tags=("aquatic", "ambush"),
            spawn_category="water_creature",
            spawn_biomes=("kelp_cathedral", "mangrove_labyrinth", "seagrass_meadow"),
            spawn_weight=12, spawn_group=(1, 1),
            drops=(("biomesunseen:kelpstone_shard", 0, 3, 0.7),), experience=12,
            lore="Indistinguishable from the kelp until the kelp moves."),

    MobSpec("trench_angler", "Trench Angler", "serpent", "overworld", "aquatic", hostile=True,
            skin="#2E839E", hide="#1A566B", accent="#C8FFF4", eye="#7CF0DC", bone="#79D6E8",
            overlays=("bioluminescent_freckles", "tusks"),
            max_health=28.0, movement_speed=0.28, attack_damage=8.0, scale=1.3,
            can_breathe_underwater=True, goals=GOAL_AQUATIC,
            behaviour_tags=("aquatic", "ambush", "bioluminescent"),
            spawn_category="water_creature",
            spawn_biomes=("abyssal_trench", "sunken_cathedral", "leviathan_graveyard",
                          "luminous_sea", "pearl_depths"),
            spawn_weight=28, spawn_group=(1, 2),
            drops=(("biomesunseen:deep_pearl", 0, 1, 0.4),), experience=10,
            lore="The light is bait. You already knew that."),

    MobSpec("abyssal_leviathan", "Abyssal Leviathan", "serpent", "overworld", "aquatic", hostile=True,
            skin="#4260B8", hide="#273F8C", accent="#A8C8FF", eye="#FFFFFF", bone="#6A8FE0",
            overlays=("crown_shards", "fin_fan"),
            max_health=80.0, movement_speed=0.3, attack_damage=12.0, armour=8.0, scale=2.6,
            can_breathe_underwater=True, goals=GOAL_AQUATIC, behaviour_tags=("aquatic", "boss"),
            spawn_category="water_creature",
            spawn_biomes=("abyssal_trench", "leviathan_graveyard"),
            spawn_weight=4, spawn_group=(1, 1),
            drops=(("biomesunseen:abyssite_shard", 2, 5, 1.0), ("biomesunseen:deep_pearl", 1, 3, 0.8)),
            experience=60,
            lore="Rare. Enormous. Not a boss, technically, but you will not survive the distinction."),

    MobSpec("highland_goat", "Highland Goat", "quadruped", "overworld", "harsh",
            skin="#A89A80", hide="#7A6E58", accent="#D8CDB8", eye="#FFE066", bone="#E8DCC0",
            overlays=("horns_curved", "hooves_cloven"),
            max_health=18.0, movement_speed=0.3, armour=2.0,
            goals=GOAL_PASSIVE_HERD, behaviour_tags=("herding", "environmental_adaptation", "tamable"),
            spawn_biomes=("howling_peaks", "sakura_highlands", "harvest_hollows", "emberfall_ridge"),
            spawn_weight=22, spawn_group=(2, 5),
            drops=(("minecraft:mutton", 1, 2, 0.9), ("minecraft:leather", 0, 2, 0.6)), experience=4,
            lore="Climbs things. Headbutts things. The two are often the same thing."),

    MobSpec("gale_harrier", "Gale Harrier", "avian", "overworld", "harsh", hostile=True,
            skin="#93AED6", hide="#6580AE", accent="#F2F7FF", eye="#FFE066", bone="#C6D6EE",
            overlays=("beak_hooked", "wing_membrane"),
            max_health=18.0, movement_speed=0.34, attack_damage=5.0, scale=1.0,
            goals=GOAL_AERIAL, behaviour_tags=("aerial", "pack_tactics"),
            spawn_category="monster",
            spawn_biomes=("howling_peaks", "stormback_steppe", "whitewater_gorge",
                          "zephyr_reach", "shatterbelt"),
            spawn_weight=20, spawn_group=(1, 2),
            drops=(("minecraft:feather", 1, 3, 0.9), ("biomesunseen:skylead_ingot", 0, 1, 0.2)),
            experience=6,
            lore="Hunts in the updraft and barely has to flap."),

    MobSpec("steppe_rider", "Steppe Rider", "quadruped", "overworld", "ancient",
            skin="#C49A72", hide="#9C7250", accent="#E8C9A8", eye="#2A1A10", bone="#F5DCBB",
            overlays=("saddle", "mane_stripe"),
            max_health=32.0, movement_speed=0.4, scale=1.2,
            goals=GOAL_PASSIVE_TAMABLE, behaviour_tags=("tamable", "herding"),
            spawn_biomes=("bronze_steppe", "primal_savanna", "stormback_steppe", "old_king_road"),
            spawn_weight=20, spawn_group=(2, 4),
            drops=(("minecraft:leather", 1, 3, 0.8),), experience=6,
            lore="Fast, sure-footed, and willing to be ridden if you ask properly."),

    MobSpec("savanna_strider", "Savanna Strider", "biped", "overworld", "vibrant",
            skin="#D8C050", hide="#B8A030", accent="#F0E8A0", eye="#5A4A10", bone="#E8DCC0",
            overlays=("no_marking", "claws_long"),
            max_health=20.0, movement_speed=0.36, scale=1.35,
            goals=GOAL_PASSIVE_HERD, behaviour_tags=("herding", "environmental_adaptation"),
            spawn_biomes=("primal_savanna", "sunspore_barrens", "marigold_march"),
            spawn_weight=22, spawn_group=(3, 6),
            drops=(("minecraft:leather", 1, 2, 0.7),), experience=5,
            lore="Long legs for long grass and a permanent squint."),

    MobSpec("primal_cat", "Primal Cat", "quadruped", "overworld", "vibrant", hostile=True,
            skin="#C0A060", hide="#907840", accent="#E8D0A0", eye="#8AFF6A", bone="#F0E0C0",
            overlays=("claws_long", "mane_stripe"),
            max_health=22.0, movement_speed=0.4, attack_damage=6.0,
            goals=GOAL_HOSTILE_AMBUSH, behaviour_tags=("ambush", "tamable", "pack_tactics"),
            spawn_category="monster",
            spawn_biomes=("primal_savanna", "verdantheight", "glimmerleaf_woodland"),
            spawn_weight=18, spawn_group=(1, 2),
            drops=(("minecraft:leather", 0, 2, 0.6),), experience=8,
            lore="Can be tamed. Should be tamed carefully and with food at the ready."),

    MobSpec("orchid_mantis", "Orchid Mantis", "arthropod", "overworld", "vibrant", hostile=True,
            skin="#F58CCB", hide="#D25CA6", accent="#FFF0FA", eye="#2A0A20", bone="#FFC4E8",
            overlays=("crest", "claws_long"),
            max_health=16.0, movement_speed=0.3, attack_damage=6.5, scale=0.9,
            goals=GOAL_HOSTILE_AMBUSH, behaviour_tags=("ambush", "environmental_adaptation"),
            spawn_category="monster",
            spawn_biomes=("orchid_lagoon", "bloomfield", "mangrove_labyrinth", "chromatic_reef"),
            spawn_weight=20, spawn_group=(1, 1),
            drops=(("biomesunseen:bloomglass_pane", 0, 2, 0.5),), experience=6,
            lore="A flower that catches flies. Then a flower that catches you."),

    MobSpec("amber_sentinel", "Amber Sentinel", "biped", "overworld", "vibrant", hostile=True,
            skin="#D09A34", hide="#A26F1E", accent="#FFF0B8", eye="#FFE066", bone="#F0C86A",
            overlays=("barding", "single_horn"),
            max_health=30.0, movement_speed=0.26, attack_damage=7.0, armour=6.0, scale=1.25,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("environmental_adaptation",),
            spawn_category="monster",
            spawn_biomes=("amberwood", "sunspore_barrens", "harvest_hollows"),
            spawn_weight=14, spawn_group=(1, 1),
            drops=(("biomesunseen:sporeamber_chunk", 1, 3, 0.8),), experience=11,
            lore="Set to guard the amberwood and has taken the assignment literally."),

    MobSpec("veilmourner", "Veilmourner", "biped", "overworld", "ethereal", hostile=True,
            skin="#948AA8", hide="#6B6180", accent="#C8C0D8", eye="#FFFFFF", bone="#B8B0C8",
            overlays=("scar", "no_marking"),
            max_health=26.0, movement_speed=0.28, attack_damage=6.0, armour=3.0,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("ambush",),
            render_layer="translucent", spawn_category="monster",
            spawn_biomes=("veilwood", "ghostlight_marsh", "ashen_necropolis", "dusk_mirror"),
            spawn_weight=15, spawn_group=(1, 1),
            drops=(("biomesunseen:wraithsalt_crystal", 0, 2, 0.6),
                   ("biomesunseen:lore_fragment", 0, 1, 0.25)), experience=10,
            lore="Grieving somebody. It has been a long time and it has not improved."),

    MobSpec("roadwarden", "Roadwarden", "biped", "overworld", "ancient",
            skin="#8E6844", hide="#63452A", accent="#E0BE96", eye="#74503A", bone="#F5DCBB",
            overlays=("barding", "saddle"),
            max_health=28.0, movement_speed=0.28, armour=5.0,
            goals=GOAL_PASSIVE_TRADER, behaviour_tags=("trading", "herding"),
            spawn_biomes=("old_king_road", "marigold_march", "harvest_hollows", "bronze_steppe"),
            spawn_weight=12, spawn_group=(1, 1),
            drops=(("biomesunseen:rootiron_ingot", 0, 2, 0.5),), experience=8,
            lore="Still walking the route. Still collecting the toll. Receipts available."),

    MobSpec("rootburrower", "Rootburrower", "arthropod", "overworld", "ancient", hostile=True,
            skin="#7A6844", hide="#4B3D2A", accent="#B8A484", eye="#D8FFC0", bone="#94805F",
            overlays=("segment_bands", "claws_long"),
            max_health=20.0, movement_speed=0.28, attack_damage=5.0, armour=4.0,
            goals=GOAL_HOSTILE_AMBUSH, behaviour_tags=("ambush", "burrowing"),
            spawn_category="monster",
            spawn_biomes=("rootdeep_hollow", "ancestor_grove", "root_cathedral",
                          "amberwood"),
            spawn_weight=22, spawn_group=(1, 3),
            drops=(("biomesunseen:rootiron_ingot", 0, 2, 0.5),
                   ("biomesunseen:spiritwood_splinter", 0, 2, 0.6)), experience=7,
            lore="Comes up through the root mat. The root mat does not warn you."),

    MobSpec("grove_warden", "Grove Warden", "biped", "overworld", "ancient",
            skin="#71C255", hide="#489636", accent="#D8FFC0", eye="#FFE066", bone="#9EE87E",
            overlays=("moss_growth", "antlers"),
            max_health=38.0, movement_speed=0.26, attack_damage=7.0, armour=6.0, scale=1.4,
            goals=("float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
                   "look_at_player", "water_avoiding_random_stroll"),
            behaviour_tags=("herding", "environmental_adaptation", "tamable"), hostile=True,
            spawn_biomes=("lumenshade_glade", "ancestor_grove", "rootdeep_hollow",
                          "root_cathedral"),
            spawn_weight=18, spawn_group=(1, 2),
            drops=(("biomesunseen:root_heart_fragment", 0, 1, 0.2),
                   ("biomesunseen:spiritwood_splinter", 1, 3, 0.8)), experience=14,
            lore="Tends the grove. Will defend it. Prefers not to."),

    MobSpec("lanternkeeper", "Lanternkeeper", "biped", "overworld", "ethereal",
            skin="#F0C86A", hide="#D09A34", accent="#FFF0B8", eye="#FFE066", bone="#FFE9A8",
            overlays=("no_marking",),
            max_health=24.0, movement_speed=0.26,
            goals=GOAL_PASSIVE_TRADER, behaviour_tags=("trading",),
            spawn_biomes=("lantern_terraces", "hollow_oasis", "river_of_lights"),
            spawn_weight=12, spawn_group=(1, 1),
            drops=(("biomesunseen:hollowite_gem", 0, 1, 0.4),), experience=8,
            lore="Lights the lanterns. Every night. Has never missed one."),

    MobSpec("rime_stag", "Rime Stag", "quadruped", "overworld", "harsh",
            skin="#9AC0C8", hide="#7AA8B0", accent="#E0F0F8", eye="#7CF0DC", bone="#F0FFFF",
            overlays=("antlers", "crown_shards"),
            max_health=30.0, movement_speed=0.34, armour=3.0, scale=1.25,
            goals=GOAL_PASSIVE_HERD, behaviour_tags=("herding", "environmental_adaptation", "tamable"),
            spawn_biomes=("rimeforest", "frozen_expanse", "crystalline_tundra"),
            spawn_weight=15, spawn_group=(1, 3),
            drops=(("biomesunseen:frostbloom_bloom", 0, 2, 0.5),), experience=7,
            lore="Ice grows along its antlers and sheds every spring."),

    MobSpec("meadow_skipper", "Meadow Skipper", "arthropod", "overworld", "vibrant",
            skin="#FFD247", hide="#E8A81E", accent="#FFFAD2", eye="#5A4A10", bone="#FFEC8A",
            overlays=("crest", "wing_membrane"),
            max_health=6.0, movement_speed=0.36, scale=0.5,
            goals=("float", "fly_random", "tempt", "look_at_player", "follow_flock_leader"),
            behaviour_tags=("herding", "aerial"),
            spawn_category="ambient",
            spawn_biomes=("bloomfield", "floating_meadow", "celestial_orchard",
                          "marigold_march", "sunspire_plateau"),
            spawn_weight=32, spawn_group=(3, 6),
            drops=(("biomesunseen:sunspore_pod", 0, 1, 0.4),), experience=1,
            lore="Enormous, brightly coloured, and completely harmless."),

    MobSpec("frozen_mariner", "Frozen Mariner", "biped", "overworld", "harsh", hostile=True,
            skin="#8AB0C0", hide="#5A8090", accent="#D0E4F0", eye="#7CF0DC", bone="#E0F0F8",
            overlays=("barding", "scar"),
            max_health=28.0, movement_speed=0.26, attack_damage=6.5, armour=5.0,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("environmental_adaptation",),
            spawn_category="monster",
            spawn_biomes=("grave_ice_field", "glacial_lake", "glacier_maw"),
            spawn_weight=12, spawn_group=(1, 1),
            drops=(("biomesunseen:glacierite_shard", 0, 2, 0.6),
                   ("biomesunseen:lore_fragment", 0, 1, 0.3)), experience=10,
            lore="Still in uniform. Still aboard. The ship is ice now."),

    MobSpec("luminous_jelly", "Luminous Jelly", "fungal", "overworld", "aquatic",
            skin="#7CF0DC", hide="#3FCDB4", accent="#C8FFF4", eye="#FFFFFF", bone="#DFFFF8",
            overlays=("bioluminescent_freckles", "gills"),
            max_health=10.0, movement_speed=0.24, scale=0.8, can_breathe_underwater=True,
            goals=("swim_random", "follow_flock_leader", "look_at_player"),
            behaviour_tags=("herding", "aquatic", "bioluminescent"),
            render_layer="translucent", spawn_category="water_creature",
            spawn_biomes=("luminous_sea", "pearl_depths", "river_of_lights",
                          "kelp_cathedral", "geyser_lagoon"),
            spawn_weight=35, spawn_group=(3, 6),
            drops=(("biomesunseen:hollowite_gem", 0, 1, 0.3),), experience=3,
            lore="Drifts, glows, and has no opinion about anything."),
]

# ---------------------------------------------------------------------------
#  30 DIMENSION MOBS  (10 per dimension)
# ---------------------------------------------------------------------------

DIMENSION_MOBS: List[MobSpec] = [
    # ================= THE HOLLOW DEEP =================
    MobSpec("hollow_scout", "Hollow Scout", "biped", "hollow_deep", "ethereal",
            skin="#7CF0DC", hide="#3FCDB4", accent="#C8FFF4", eye="#FFE066", bone="#DFFFF8",
            overlays=("no_marking", "bioluminescent_freckles"),
            max_health=24.0, movement_speed=0.3, armour=2.0,
            goals=GOAL_PASSIVE_TRADER, behaviour_tags=("trading", "bioluminescent"),
            render_layer="cutout",
            spawn_biomes=("hollow_threshold", "hollow_oasis", "lantern_terraces"),
            spawn_weight=20, spawn_group=(1, 2),
            drops=(("biomesunseen:hollowite_gem", 0, 2, 0.5),), experience=8,
            lore="Maps the tunnels. Sells the maps. Both are honest work."),

    MobSpec("glowcap_grub", "Glowcap Grub", "arthropod", "hollow_deep", "ethereal",
            skin="#BEE894", hide="#93C863", accent="#E6FFC8", eye="#29441 7".replace(" ", ""),
            bone="#E6FFC8",
            overlays=("segment_bands", "bioluminescent_freckles"),
            max_health=10.0, movement_speed=0.2, scale=0.6,
            goals=("float", "panic", "tempt", "look_at_player", "water_avoiding_random_stroll"),
            behaviour_tags=("herding", "bioluminescent", "burrowing"),
            spawn_biomes=("glowcap_grotto", "fungal_forest", "chitin_warrens", "deep_bloom_reach"),
            spawn_weight=28, spawn_group=(2, 4),
            drops=(("biomesunseen:mycelium_culture", 0, 2, 0.7),), experience=2,
            lore="Fat, glowing, slow. The Hollow Deep considers it a delicacy."),

    MobSpec("gloomstalker", "Gloomstalker", "quadruped", "hollow_deep", "harsh", hostile=True,
            skin="#464460", hide="#34324A", accent="#5C5A78", eye="#C8B4FF", bone="#7355D1",
            overlays=("eyes_void", "claws_long"),
            max_health=28.0, movement_speed=0.35, attack_damage=7.0, armour=3.0,
            goals=GOAL_HOSTILE_AMBUSH, behaviour_tags=("ambush", "pack_tactics", "phase_shift"),
            spawn_category="monster",
            spawn_biomes=("gloomslate_depths", "echo_chasm", "outer_margin"),
            spawn_weight=28, spawn_group=(1, 2),
            drops=(("biomesunseen:gloomite_shard", 0, 2, 0.6),), experience=9,
            lore="You see it in the gloomslate. Then the gloomslate is where you were."),

    MobSpec("sporeling_deep", "Deep Sporeling", "fungal", "hollow_deep", "vibrant",
            skin="#B0C870", hide="#87A04C", accent="#D8E8A0", eye="#5A6A2A", bone="#E8E0C0",
            overlays=("mushroom_cap", "spore_vents"),
            max_health=12.0, movement_speed=0.24, scale=0.8,
            goals=GOAL_ENVIRONMENTAL, behaviour_tags=("herding", "bioluminescent",
                                                     "environmental_adaptation"),
            spawn_biomes=("mycelial_wastes", "spore_chalk_flats", "glowcap_grotto",
                          "chitin_warrens"),
            spawn_weight=38, spawn_group=(3, 6),
            drops=(("biomesunseen:sporeamber_chunk", 0, 2, 0.7),), experience=3,
            lore="Larger and dimmer than its surface cousins. Down here light is expensive."),

    MobSpec("mycelial_horror", "Mycelial Horror", "fungal", "hollow_deep", "harsh", hostile=True,
            skin="#6B9E42", hide="#48702B", accent="#BEE894", eye="#E6FFC8", bone="#93C863",
            overlays=("mushroom_cap", "claws_long"),
            max_health=48.0, movement_speed=0.24, attack_damage=9.0, armour=4.0, scale=1.7,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("environmental_adaptation", "summoner"),
            spawn_category="monster",
            spawn_biomes=("mycelial_wastes", "fungal_forest"),
            spawn_weight=10, spawn_group=(1, 1),
            drops=(("biomesunseen:mycelium_culture", 2, 4, 0.9),
                   ("biomesunseen:root_heart_fragment", 0, 1, 0.15)), experience=18,
            lore="One organism. It is having an argument with itself about you."),

    MobSpec("fungal_titan", "Fungal Titan", "biped", "hollow_deep", "vibrant", hostile=True,
            skin="#8FBF7A", hide="#6A9A5C", accent="#E6FFC8", eye="#FFE066", bone="#C6CBB2",
            overlays=("mushroom_cap", "barding"),
            max_health=56.0, movement_speed=0.22, attack_damage=10.0, armour=8.0, scale=2.0,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("environmental_adaptation",),
            fire_immune=True, spawn_category="monster",
            spawn_biomes=("fungal_forest", "deep_bloom_reach"),
            spawn_weight=8, spawn_group=(1, 1),
            drops=(("biomesunseen:mycelium_culture", 2, 5, 0.9),
                   ("biomesunseen:sporeamber_chunk", 1, 3, 0.8)), experience=22,
            lore="Forty blocks of fungus with a gait and a temper."),

    MobSpec("vault_keeper", "Vault Keeper", "biped", "hollow_deep", "ancient", hostile=True,
            skin="#A6AC93", hide="#838873", accent="#E4E8D2", eye="#7CF0DC", bone="#C6CBB2",
            overlays=("barding", "crown_shards"),
            max_health=34.0, movement_speed=0.26, attack_damage=8.0, armour=7.0, scale=1.2,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("environmental_adaptation",),
            spawn_category="monster",
            spawn_biomes=("crystal_vault", "luminous_sea", "sunken_hollow_city"),
            spawn_weight=15, spawn_group=(1, 1),
            drops=(("biomesunseen:echo_crystal", 0, 2, 0.5),
                   ("biomesunseen:lore_fragment", 0, 1, 0.3)), experience=14,
            lore="Keeps the vault. Has no idea what is in it. Keeps it anyway."),

    MobSpec("hollow_drowned", "Hollow Drowned", "biped", "hollow_deep", "aquatic", hostile=True,
            skin="#4E7F92", hide="#3A6273", accent="#6FA8B8", eye="#C8FFF4", bone="#A6AC93",
            overlays=("gills", "scar"),
            max_health=24.0, movement_speed=0.28, attack_damage=6.0, armour=2.0,
            can_breathe_underwater=True, goals=GOAL_AQUATIC,
            behaviour_tags=("aquatic", "pack_tactics"),
            spawn_category="water_creature",
            spawn_biomes=("sunken_hollow_city", "luminous_sea", "pearl_depths"),
            spawn_weight=26, spawn_group=(2, 4),
            drops=(("biomesunseen:deep_pearl", 0, 1, 0.3),), experience=8,
            lore="The city flooded. They did not leave. They adapted, badly."),

    MobSpec("warren_skitter", "Warren Skitter", "arthropod", "hollow_deep", "harsh", hostile=True,
            skin="#93C863", hide="#6B9E42", accent="#E6FFC8", eye="#294417", bone="#C6CBB2",
            overlays=("segment_bands", "claws_long"),
            max_health=12.0, movement_speed=0.4, attack_damage=3.0, scale=0.65,
            goals=GOAL_HOSTILE_PACK, behaviour_tags=("pack_tactics", "burrowing"),
            spawn_category="monster",
            spawn_biomes=("chitin_warrens", "glowcap_grotto", "mycelial_wastes"),
            spawn_weight=40, spawn_group=(4, 8),
            drops=(("biomesunseen:mycelium_culture", 0, 1, 0.6),), experience=3,
            lore="Harmless alone. Never alone. The warrens are one continuous animal."),

    MobSpec("echo_bat", "Echo Bat", "avian", "hollow_deep", "harsh", hostile=True,
            skin="#5C5A78", hide="#464460", accent="#9C82F0", eye="#C8B4FF", bone="#7355D1",
            overlays=("wing_membrane", "eyes_glowing"),
            max_health=10.0, movement_speed=0.36, attack_damage=3.5, scale=0.6,
            goals=GOAL_AERIAL, behaviour_tags=("aerial", "pack_tactics", "bioluminescent"),
            render_layer="translucent", spawn_category="ambient",
            spawn_biomes=("echo_chasm", "weeping_galleries", "gloomslate_depths", "hollow_echo"),
            spawn_weight=32, spawn_group=(3, 6),
            drops=(("biomesunseen:echo_crystal", 0, 1, 0.2),), experience=3,
            lore="Navigates by echo. Screams constantly. The two facts are related."),

    MobSpec("warden_acolyte", "Warden Acolyte", "biped", "hollow_deep", "ancient", hostile=True,
            skin="#524C58", hide="#3E3943", accent="#6B6570", eye="#7CF0DC", bone="#B8A98A",
            overlays=("barding", "single_horn"),
            max_health=36.0, movement_speed=0.27, attack_damage=8.5, armour=9.0, scale=1.3,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("environmental_adaptation", "pack_tactics"),
            spawn_category="monster",
            spawn_biomes=("tremor_ward", "hollow_core", "basaltic_fissures"),
            spawn_weight=18, spawn_group=(1, 2),
            drops=(("biomesunseen:basaltic_core", 0, 2, 0.5),
                   ("biomesunseen:lore_fragment", 0, 1, 0.35)), experience=15,
            lore="Worships the thing under the floor. It has good reason to."),

    # ================= AETHERFALL =================
    MobSpec("veilwing", "Veilwing", "avian", "aetherfall", "ethereal",
            skin="#A9C8FF", hide="#7399EE", accent="#DCEBFF", eye="#FFFFFF", bone="#E8F0FF",
            overlays=("wing_membrane", "crest"),
            max_health=14.0, movement_speed=0.36, scale=0.85,
            goals=("float", "fly_random", "tempt", "look_at_player", "follow_flock_leader"),
            behaviour_tags=("herding", "aerial"),
            render_layer="translucent", spawn_category="ambient",
            spawn_biomes=("dawn_landing", "aurora_bridge", "featherfall_grove",
                          "moonpetal_skyfield", "twilight_terrace"),
            spawn_weight=32, spawn_group=(2, 5),
            drops=(("biomesunseen:aetherium_ingot", 0, 1, 0.15),), experience=4,
            lore="Rides the thermals between islands and rarely flaps."),

    MobSpec("cloudfin", "Cloudfin", "serpent", "aetherfall", "aquatic",
            skin="#CBD8EC", hide="#A9BAD6", accent="#FFFFFF", eye="#FFE066", bone="#E8EFFA",
            overlays=("fin_fan", "gills"),
            max_health=14.0, movement_speed=0.34, scale=0.9,
            goals=("swim_random", "follow_flock_leader", "tempt", "look_at_player"),
            behaviour_tags=("herding", "aquatic", "aerial"),
            render_layer="translucent", spawn_category="water_creature",
            spawn_biomes=("cloud_sea", "aurora_bridge", "zephyr_reach"),
            spawn_weight=35, spawn_group=(3, 6),
            drops=(("biomesunseen:skylead_ingot", 0, 1, 0.3),), experience=3,
            lore="Swims in cloud. Nobody has established whether cloud is wet."),

    MobSpec("crown_sentinel", "Crown Sentinel", "biped", "aetherfall", "ancient", hostile=True,
            skin="#E8C86F", hide="#C7A44C", accent="#FFE9A8", eye="#FFFFFF", bone="#FFEFD9",
            overlays=("barding", "crown_shards"),
            max_health=40.0, movement_speed=0.28, attack_damage=9.0, armour=10.0, scale=1.45,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("environmental_adaptation", "ranged"),
            spawn_category="monster",
            spawn_biomes=("gilded_citadel", "skyward_steps", "crown_apex", "starfall_vault",
                          "hymn_halls"),
            spawn_weight=22, spawn_group=(1, 2),
            drops=(("biomesunseen:aetherium_ingot", 0, 2, 0.6),
                   ("biomesunseen:starfall_core", 0, 1, 0.15)), experience=18,
            lore="Gilded, hollow, and still following orders issued before the fall."),

    MobSpec("quarry_construct", "Quarry Construct", "biped", "aetherfall", "ancient", hostile=True,
            skin="#F6D7B0", hide="#E0BB8E", accent="#FFEFD9", eye="#FFE066", bone="#D6C7A6",
            overlays=("barding",),
            max_health=32.0, movement_speed=0.24, attack_damage=8.0, armour=8.0, scale=1.3,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("environmental_adaptation",),
            spawn_category="monster",
            spawn_biomes=("dawn_marble_quarry", "gilded_archive", "runeglass_fields"),
            spawn_weight=18, spawn_group=(1, 2),
            drops=(("biomesunseen:dawnshard", 0, 2, 0.6),), experience=13,
            lore="Still quarrying. The invoice it is working to was never cancelled."),

    MobSpec("rune_construct", "Rune Construct", "biped", "aetherfall", "vibrant", hostile=True,
            skin="#70D0C8", hide="#42A5A0", accent="#E8FFFF", eye="#FFFFFF", bone="#B0F0E8",
            overlays=("runes_glowing", "barding"),
            max_health=28.0, movement_speed=0.26, attack_damage=7.5, armour=6.0, scale=1.15,
            goals=GOAL_HOSTILE_RANGED, behaviour_tags=("ranged", "environmental_adaptation"),
            fire_immune=True, render_layer="cutout", spawn_category="monster",
            spawn_biomes=("runeglass_fields", "hymn_halls", "gilded_archive", "starfall_vault"),
            spawn_weight=18, spawn_group=(1, 2),
            drops=(("biomesunseen:runeglass_pane", 0, 2, 0.6),), experience=12,
            lore="A sentence made solid. It reads itself aloud at you."),

    MobSpec("stormcell_wisp", "Stormcell Wisp", "fungal", "aetherfall", "harsh", hostile=True,
            skin="#A8E8FF", hide="#5FC0F0", accent="#F2FFFF", eye="#FFFFFF", bone="#DCEBFF",
            overlays=("bioluminescent_freckles",),
            max_health=14.0, movement_speed=0.34, attack_damage=5.0, scale=0.65,
            goals=("float", "fly_random", "ranged_attack", "melee_attack",
                   "hurt_by_target", "nearest_attackable_target_player"),
            behaviour_tags=("aerial", "ranged", "pack_tactics"),
            fire_immune=True, render_layer="translucent", spawn_category="monster",
            spawn_biomes=("stormcell_spire", "zephyr_reach", "shatterbelt"),
            spawn_weight=26, spawn_group=(2, 4),
            drops=(("biomesunseen:stormcell_core", 0, 1, 0.35),), experience=6,
            lore="A small piece of the storm that got separated and is angry about it."),

    MobSpec("orchard_tender", "Orchard Tender", "biped", "aetherfall", "vibrant",
            skin="#B4C8EE", hide="#8AA2D6", accent="#DCE6FF", eye="#7FD95A", bone="#E8F0FF",
            overlays=("no_marking", "moss_growth"),
            max_health=26.0, movement_speed=0.26,
            goals=GOAL_PASSIVE_TRADER, behaviour_tags=("trading", "herding"),
            spawn_biomes=("celestial_orchard", "sunspire_plateau", "floating_meadow"),
            spawn_weight=14, spawn_group=(1, 1),
            drops=(("biomesunseen:sunspore_pod", 0, 3, 0.8),), experience=9,
            lore="Prunes, waters, harvests. Has done so since before the islands fell."),

    MobSpec("astral_scribe_aether", "Aether Scribe", "biped", "aetherfall", "ancient",
            skin="#AE9EE0", hide="#8471BE", accent="#F4F0FF", eye="#E0FFFF", bone="#D6CCF5",
            overlays=("scar", "runes_glowing"),
            max_health=20.0, movement_speed=0.26,
            goals=GOAL_PASSIVE_TRADER, behaviour_tags=("trading",),
            spawn_biomes=("gilded_archive", "hymn_halls", "gilded_citadel", "starfall_vault"),
            spawn_weight=16, spawn_group=(1, 1),
            drops=(("biomesunseen:lore_fragment", 1, 2, 0.85),), experience=7,
            lore="Recording the fall. It is a very long record."),

    MobSpec("unraveling_shard_aether", "Fallen Shard", "arthropod", "aetherfall", "ancient",
            skin="#FFD98A", hide="#E8B452", accent="#FFF0C8", eye="#FFFFFF", bone="#FFEFD9",
            overlays=("crystal_spurs", "crown_shards"),
            max_health=18.0, movement_speed=0.3, scale=0.7,
            goals=("float", "fly_random", "look_at_player", "follow_flock_leader"),
            behaviour_tags=("aerial", "bioluminescent", "herding"),
            render_layer="translucent", spawn_category="ambient",
            spawn_biomes=("starfall_vault", "crown_apex", "sunspire_plateau", "aurora_bridge"),
            spawn_weight=20, spawn_group=(2, 4),
            drops=(("biomesunseen:starfall_core", 0, 1, 0.25),), experience=5,
            lore="A piece of the Crown that fell and kept orbiting anyway."),

    MobSpec("sky_citizen", "Sky Citizen", "biped", "aetherfall", "vibrant",
            skin="#93ABD8", hide="#7189B8", accent="#DCEBFF", eye="#FFE066", bone="#E8F0FF",
            overlays=("saddle", "no_marking"),
            max_health=22.0, movement_speed=0.28,
            goals=GOAL_PASSIVE_TRADER, behaviour_tags=("trading", "herding", "aerial"),
            spawn_biomes=("floating_meadow", "celestial_orchard", "dawn_landing",
                          "moonpetal_skyfield"),
            spawn_weight=18, spawn_group=(2, 3),
            drops=(("biomesunseen:dawnshard", 0, 2, 0.5),), experience=6,
            lore="Lives up here by choice. Considers the surface a rumour."),

    # ================= THE VOID BETWEEN =================
    MobSpec("void_scout", "Void Scout", "biped", "void_between", "ethereal", hostile=True,
            skin="#5D4588", hide="#452F6B", accent="#7A5FA8", eye="#B98CFF", bone="#8A54D6",
            overlays=("scar", "eyes_void"),
            max_health=26.0, movement_speed=0.32, attack_damage=7.0, armour=3.0,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("phase_shift", "environmental_adaptation"),
            render_layer="translucent", spawn_category="monster",
            spawn_biomes=("void_threshold", "serpent_run", "dusk_mirror"),
            spawn_weight=20, spawn_group=(1, 2),
            drops=(("biomesunseen:voidsteel_ingot", 0, 2, 0.5),), experience=10,
            lore="Came here to map it. The mapping is not going well."),

    MobSpec("fracture_hound", "Fracture Hound", "quadruped", "void_between", "harsh", hostile=True,
            skin="#452F6B", hide="#31204F", accent="#7A5FA8", eye="#FF6FB5", bone="#63349F",
            overlays=("claws_long", "void_fractures"),
            max_health=30.0, movement_speed=0.37, attack_damage=8.0, armour=4.0,
            goals=GOAL_HOSTILE_PACK, behaviour_tags=("pack_tactics", "phase_shift"),
            spawn_category="monster",
            spawn_biomes=("fracture_plains", "shardfall_expanse", "serpent_run", "bleeding_spires"),
            spawn_weight=30, spawn_group=(2, 4),
            drops=(("biomesunseen:fracture_shale_shard", 0, 3, 0.7),
                   ("biomesunseen:voidsteel_ingot", 0, 1, 0.3)), experience=11,
            lore="Runs in a straight line through walls. The walls lose."),

    MobSpec("static_wraith", "Static Wraith", "biped", "void_between", "harsh", hostile=True,
            skin="#84D6C4", hide="#57AFA0", accent="#B9F5E6", eye="#FFFFFF", bone="#9DF7E4",
            overlays=("eyes_glowing", "void_fractures"),
            max_health=24.0, movement_speed=0.3, attack_damage=7.5, armour=2.0,
            goals=GOAL_HOSTILE_RANGED, behaviour_tags=("ranged", "phase_shift"),
            fire_immune=True, render_layer="translucent", spawn_category="monster",
            spawn_biomes=("static_wastes", "outer_margin", "null_sea", "recursive_fields"),
            spawn_weight=28, spawn_group=(1, 3),
            drops=(("biomesunseen:staticite_cell", 0, 2, 0.6),), experience=10,
            lore="Grain in the shape of a person. It is very loud up close."),

    MobSpec("garden_aberration", "Garden Aberration", "fungal", "void_between", "vibrant", hostile=True,
            skin="#E14A97", hide="#B32F77", accent="#FF6FB5", eye="#FFFFFF", bone="#FFC4E8",
            overlays=("mushroom_cap", "void_fractures"),
            max_health=32.0, movement_speed=0.26, attack_damage=8.0, armour=3.0, scale=1.25,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("environmental_adaptation", "summoner"),
            spawn_category="monster",
            spawn_biomes=("glitch_garden", "recursive_fields", "terminal_glade", "chromatic_reef"),
            spawn_weight=22, spawn_group=(1, 2),
            drops=(("biomesunseen:bloomglass_pane", 0, 3, 0.7),
                   ("biomesunseen:nullite_shard", 0, 1, 0.12)), experience=13,
            lore="A flower rendered wrong, three times over, all of them growing."),

    MobSpec("null_swimmer", "Null Swimmer", "serpent", "void_between", "aquatic", hostile=True,
            skin="#291739", hide="#1C0F29", accent="#4B2E63", eye="#B98CFF", bone="#63349F",
            overlays=("fin_fan", "eyes_void"),
            max_health=26.0, movement_speed=0.32, attack_damage=7.0, scale=1.1,
            can_breathe_underwater=True, goals=GOAL_AQUATIC,
            behaviour_tags=("aquatic", "phase_shift", "ambush"),
            spawn_category="water_creature",
            spawn_biomes=("null_sea", "abyssal_shelf_void", "chromatic_reef"),
            spawn_weight=30, spawn_group=(2, 4),
            drops=(("biomesunseen:nullite_shard", 0, 1, 0.3),), experience=9,
            lore="Swims in something that is not water and does not need to surface."),

    MobSpec("chrono_warden", "Chrono Warden", "biped", "void_between", "ancient", hostile=True,
            skin="#69C3C9", hide="#3E96A2", accent="#A8E8E8", eye="#E8FFFF", bone="#9DF7E4",
            overlays=("runes_glowing", "barding"),
            max_health=42.0, movement_speed=0.27, attack_damage=9.5, armour=8.0, scale=1.4,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("phase_shift", "environmental_adaptation",
                                                     "ranged"),
            fire_immune=True, spawn_category="monster",
            spawn_biomes=("chrono_shelf", "paradox_hollow", "memory_vault"),
            spawn_weight=16, spawn_group=(1, 1),
            drops=(("biomesunseen:chronosite_core", 0, 1, 0.4),
                   ("biomesunseen:lore_fragment", 1, 2, 0.7)), experience=20,
            lore="Guards the order of events. You have already disturbed it."),

    MobSpec("shardling", "Shardling", "arthropod", "void_between", "harsh", hostile=True,
            skin="#5D4588", hide="#452F6B", accent="#C8B4E8", eye="#FF6FB5", bone="#715C9C",
            overlays=("crystal_spurs", "claws_long"),
            max_health=12.0, movement_speed=0.4, attack_damage=4.0, scale=0.6,
            goals=GOAL_HOSTILE_PACK, behaviour_tags=("pack_tactics", "aerial"),
            spawn_category="monster",
            spawn_biomes=("shardfall_expanse", "fracture_plains", "bleeding_spires"),
            spawn_weight=34, spawn_group=(3, 6),
            drops=(("biomesunseen:fracture_shale_shard", 0, 2, 0.8),), experience=4,
            lore="Falling geometry that decided to keep going sideways instead."),

    MobSpec("spire_climber", "Spire Climber", "arthropod", "void_between", "harsh", hostile=True,
            skin="#2E2E37", hide="#222229", accent="#3C3C46", eye="#FF6FB5", bone="#524C58",
            overlays=("segment_bands", "claws_long"),
            max_health=20.0, movement_speed=0.34, attack_damage=6.0, armour=5.0,
            goals=GOAL_HOSTILE_AMBUSH, behaviour_tags=("ambush", "burrowing"),
            spawn_category="monster",
            spawn_biomes=("bleeding_spires", "outer_margin", "fracture_plains"),
            spawn_weight=26, spawn_group=(1, 3),
            drops=(("biomesunseen:bloodstone_gem", 0, 2, 0.5),), experience=8,
            lore="Climbs the weeping spires and eats whatever the spires produce."),

    MobSpec("mirror_walk", "Mirror Walk", "biped", "void_between", "ethereal", hostile=True,
            skin="#6F439E", hide="#4A2873", accent="#9A67C8", eye="#F0D8FF", bone="#C79CE8",
            overlays=("scar", "void_fractures"),
            max_health=28.0, movement_speed=0.3, attack_damage=7.5, armour=3.0,
            goals=GOAL_HOSTILE_MELEE, behaviour_tags=("phase_shift", "ambush"),
            render_layer="translucent", spawn_category="monster",
            spawn_biomes=("dusk_mirror", "void_threshold", "terminal_glade", "hollow_echo"),
            spawn_weight=20, spawn_group=(1, 2),
            drops=(("biomesunseen:duskite_gem", 0, 2, 0.6),), experience=11,
            lore="Arrives from the reflection side. The reflection does not come back."),

    MobSpec("unraveling_shard", "Unraveling Shard", "arthropod", "void_between", "ancient", hostile=True,
            skin="#E0309F", hide="#A81A73", accent="#FF6FD8", eye="#FFFFFF", bone="#FF9FE0",
            overlays=("crystal_spurs", "void_fractures"),
            max_health=22.0, movement_speed=0.34, attack_damage=6.5, armour=2.0, scale=0.8,
            goals=GOAL_HOSTILE_PACK, behaviour_tags=("pack_tactics", "phase_shift", "aerial"),
            fire_immune=True, render_layer="translucent", spawn_category="monster",
            spawn_biomes=("unraveling_nexus", "paradox_hollow", "recursive_fields",
                          "chromatic_reef"),
            spawn_weight=25, spawn_group=(2, 4),
            drops=(("biomesunseen:nullite_shard", 0, 1, 0.35),
                   ("biomesunseen:chronosite_core", 0, 1, 0.1)), experience=9,
            lore="A piece of the Unraveling that came off and kept the habit."),
]

ALL_MOBS: List[MobSpec] = OVERWORLD_MOBS + DIMENSION_MOBS
MOB_BY_ID: Dict[str, MobSpec] = {}
for _m in ALL_MOBS:
    if _m.id in MOB_BY_ID:
        raise ValueError(f"duplicate mob id {_m.id!r}")
    MOB_BY_ID[_m.id] = _m


def mobs_in(dimension: str) -> List[MobSpec]:
    return [m for m in ALL_MOBS if m.dimension == dimension]


def mob_by_id(mob_id: str) -> MobSpec:
    try:
        return MOB_BY_ID[mob_id]
    except KeyError:
        raise KeyError(f"unknown mob {mob_id!r}") from None
