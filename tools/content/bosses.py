"""
content/bosses.py -- the five bosses.

Each boss declares:
  * a GeckoLib `.geo.json` model (hand-authored cube hierarchy, no ModelPart)
  * an `.animation.json` set (idle breathing, walk, attack, hurt, death,
    plus one bespoke clip per phase transition)
  * a multi-phase state machine (threshold, entry animation, new abilities)
  * an explicit AI goal loadout -- Golden Rule #5 is checked at import time:
    every boss MUST carry melee_attack, hurt_by_target and
    nearest_attackable_target_player.
  * a boss bar style, a music track, an arena structure and unique loot.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .mobs import MobSpec, GOAL_HOSTILE_MELEE

# ---------------------------------------------------------------------------
#  Phase description
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BossPhase:
    """One stage of a boss fight."""

    index: int
    name: str
    health_threshold: float          # fraction of max health at which the phase ENDS
    entry_animation: str
    description: str
    abilities: Tuple[str, ...] = ()
    extra_goals: Tuple[str, ...] = ()
    invulnerable_on_entry: bool = True
    invulnerable_ticks: int = 40


# ---------------------------------------------------------------------------
#  Boss description
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BossSpec:
    id: str
    name: str
    dimension: str
    arena_structure: str
    music: str
    boss_bar_color: str              # pink | blue | red | green | yellow | purple | white
    boss_bar_overlay: str            # progress | notched_6 | notched_10 | notched_12 | notched_20
    texture_size: int
    model_width: float
    model_height: float
    scale: float
    phases: Tuple[BossPhase, ...]
    loot_table: str
    spawn_item: str                  # the summoning artefact
    mob: MobSpec

    def __post_init__(self) -> None:
        # ---- Golden Rule #5 --------------------------------------------
        required = {"melee_attack", "hurt_by_target", "nearest_attackable_target_player"}
        have = set(self.mob.goals)
        for phase in self.phases:
            have |= set(phase.extra_goals)
        missing = required - have
        if missing:
            raise ValueError(
                f"boss {self.id!r}: Golden Rule #5 violation - missing AI goals {sorted(missing)}"
            )
        # ---- Golden Rule #2 --------------------------------------------
        for phase in self.phases:
            if phase.entry_animation not in self.mob.animations:
                raise ValueError(
                    f"boss {self.id!r}: phase {phase.index} references unregistered "
                    f"animation {phase.entry_animation!r}"
                )
        if not self.phases:
            raise ValueError(f"boss {self.id!r}: a boss must have at least one phase")
        if self.phases[0].index != 1:
            raise ValueError(f"boss {self.id!r}: phases must start at index 1")

    @property
    def entity_type_id(self) -> str:
        return f"biomesunseen:{self.id}"

    @property
    def geo_path(self) -> str:
        return f"geo/entity/boss/{self.id}.geo.json"

    @property
    def animation_path(self) -> str:
        return f"animations/entity/boss/{self.id}.animation.json"

    @property
    def texture_path(self) -> str:
        return f"textures/entity/boss/{self.id}.png"


# ---------------------------------------------------------------------------
#  Shared animation vocabulary
# ---------------------------------------------------------------------------

ANIM_IDLE = "animation.idle"
ANIM_WALK = "animation.walk"
ANIM_ATTACK = "animation.attack"
ANIM_HURT = "animation.hurt"
ANIM_DEATH = "animation.death"


def _boss_animations(*extra: str) -> Tuple[str, ...]:
    """The five mandatory clips plus any bespoke phase clips."""
    return (ANIM_IDLE, ANIM_WALK, ANIM_ATTACK, ANIM_HURT, ANIM_DEATH) + tuple(extra)


# ---------------------------------------------------------------------------
#  BOSS 1 -- THE HEART OF THE FOREST
# ---------------------------------------------------------------------------

_HEART_MOB = MobSpec(
    id="heart_of_the_forest",
    name="The Heart of the Forest",
    family="quadruped",
    dimension="overworld",
    category="ancient",
    hostile=True,
    skin="#756049", hide="#4E463D", accent="#96B83C", eye="#FFE066", bone="#B39A78",
    overlays=("moss_growth", "root_heart_glow", "antlers"),
    max_health=400.0, movement_speed=0.24, attack_damage=14.0, attack_knockback=2.0,
    follow_range=48.0, armour=12.0, scale=3.2,
    goals=(
        "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
        "look_at_player", "random_look_around", "water_avoiding_random_stroll",
    ),
    behaviour_tags=("boss", "summoner", "environmental_adaptation"),
    target_classes=("minecraft:player", "biomesunseen:grove_warden"),
    model_width=3.0, model_height=3.4, geo="heart_of_the_forest",
    shadow_radius=1.6, fire_immune=False,
    animations=_boss_animations(
        "animation.phase.summon_roots", "animation.phase.explosive_seeds",
        "animation.phase.heart_exposed", "animation.spawn",
    ),
    render_layer="cutout",
    spawn_biomes=("lumenshade_glade",), spawn_weight=0, spawn_group=(1, 1),
    spawn_category="monster",
    drops=(("biomesunseen:root_heart_fragment", 4, 8, 1.0),
           ("biomesunseen:heartwood_core", 1, 1, 1.0),
           ("biomesunseen:spiritwood_splinter", 8, 16, 1.0),
           ("biomesunseen:lore_book_heart", 1, 1, 1.0)),
    experience=500,
    lore="It was a forest once. Then it noticed us, and it stopped being only that.",
)

HEART_OF_THE_FOREST = BossSpec(
    id="heart_of_the_forest",
    name="The Heart of the Forest",
    dimension="overworld",
    arena_structure="biomesunseen:heart_of_the_forest_arena",
    music="biomesunseen:music.boss.heart_of_the_forest",
    boss_bar_color="green",
    boss_bar_overlay="notched_6",
    texture_size=64,
    model_width=3.0, model_height=3.4, scale=3.2,
    phases=(
        BossPhase(1, "Awakening", 0.75, "animation.spawn",
                  "The trunk splits open. Branch arms sweep the arena and the "
                  "floor begins to move.",
                  abilities=("branch_sweep", "stomp"),
                  extra_goals=("melee_attack",)),
        BossPhase(2, "Root Surge", 0.5, "animation.phase.summon_roots",
                  "Roots erupt from the arena floor in telegraphed lines, "
                  "immobilising anything standing on them.",
                  abilities=("root_eruption", "summon_grove_wardens", "branch_sweep"),
                  extra_goals=("summon_minions",)),
        BossPhase(3, "Seed Volley", 0.25, "animation.phase.explosive_seeds",
                  "The canopy loads. Explosive seeds arc across the arena and "
                  "detonate into a lingering sap field.",
                  abilities=("explosive_seed_volley", "root_eruption", "branch_sweep"),
                  extra_goals=("ranged_attack",)),
        BossPhase(4, "Heart Exposed", 0.0, "animation.phase.heart_exposed",
                  "The bark plates peel back and the heart-sap core is bare. "
                  "Damage taken is doubled; so is everything it does.",
                  abilities=("heart_pulse", "root_eruption", "explosive_seed_volley",
                             "branch_sweep"),
                  extra_goals=("melee_attack", "ranged_attack")),
    ),
    loot_table="biomesunseen:entities/boss/heart_of_the_forest",
    spawn_item="biomesunseen:heart_of_the_forest_seed",
    mob=_HEART_MOB,
)

# ---------------------------------------------------------------------------
#  BOSS 2 -- THE VOID SERPENT
# ---------------------------------------------------------------------------

_SERPENT_MOB = MobSpec(
    id="void_serpent",
    name="The Void Serpent",
    family="serpent",
    dimension="void_between",
    category="harsh",
    hostile=True,
    skin="#442073", hide="#2B114C", accent="#B98CFF", eye="#FF6FB5", bone="#8A54D6",
    overlays=("eyes_void", "void_fractures", "fin_fan"),
    max_health=340.0, movement_speed=0.34, attack_damage=12.0, attack_knockback=1.5,
    follow_range=56.0, armour=8.0, scale=2.6,
    goals=(
        "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
        "look_at_player", "random_look_around", "water_avoiding_random_stroll",
    ),
    behaviour_tags=("boss", "phase_shift", "ambush", "ranged"),
    target_classes=("minecraft:player",),
    model_width=2.4, model_height=1.6, geo="void_serpent",
    shadow_radius=1.4, fire_immune=True,
    animations=_boss_animations(
        "animation.phase.phase_out", "animation.phase.phase_in",
        "animation.phase.coil_slam", "animation.spawn",
    ),
    render_layer="translucent",
    spawn_biomes=("serpent_run",), spawn_weight=0, spawn_group=(1, 1),
    spawn_category="monster",
    drops=(("biomesunseen:voidsteel_ingot", 6, 12, 1.0),
           ("biomesunseen:serpent_fang", 1, 1, 1.0),
           ("biomesunseen:nullite_shard", 2, 5, 1.0),
           ("biomesunseen:lore_book_void", 1, 1, 1.0)),
    experience=500,
    lore="It does not move through the void. It edits where the void is.",
)

VOID_SERPENT = BossSpec(
    id="void_serpent",
    name="The Void Serpent",
    dimension="void_between",
    arena_structure="biomesunseen:void_serpent_arena",
    music="biomesunseen:music.boss.void_serpent",
    boss_bar_color="purple",
    boss_bar_overlay="notched_10",
    texture_size=64,
    model_width=2.4, model_height=1.6, scale=2.6,
    phases=(
        BossPhase(1, "Coiled", 0.7, "animation.spawn",
                  "The serpent circles the arena floor, striking with its head "
                  "and lashing with three body rings.",
                  abilities=("head_strike", "tail_lash"),
                  extra_goals=("melee_attack",)),
        BossPhase(2, "Phasing", 0.45, "animation.phase.phase_out",
                  "It steps out of existence for four seconds at a time and "
                  "re-enters somewhere else. Attacks pass through it while out.",
                  abilities=("phase_out", "phase_in", "head_strike", "void_spit"),
                  extra_goals=("phase_shift", "ranged_attack")),
        BossPhase(3, "Constriction", 0.2, "animation.phase.coil_slam",
                  "It coils around the arena centre and slams down, sending a "
                  "shockwave that must be jumped.",
                  abilities=("coil_slam", "phase_out", "void_spit", "head_strike"),
                  extra_goals=("melee_attack",)),
        BossPhase(4, "Unravelling", 0.0, "animation.phase.phase_in",
                  "Phase length collapses to under a second and the arena "
                  "starts losing floor. Kill it or fall.",
                  abilities=("rapid_phase", "coil_slam", "void_spit", "head_strike",
                             "arena_decay"),
                  extra_goals=("melee_attack", "ranged_attack", "phase_shift")),
    ),
    loot_table="biomesunseen:entities/boss/void_serpent",
    spawn_item="biomesunseen:void_serpent_scale",
    mob=_SERPENT_MOB,
)

# ---------------------------------------------------------------------------
#  BOSS 3 -- WARDEN OF THE HOLLOW DEEP
# ---------------------------------------------------------------------------

_WARDEN_MOB = MobSpec(
    id="warden_of_the_hollow_deep",
    name="Warden of the Hollow Deep",
    family="arthropod",
    dimension="hollow_deep",
    category="ancient",
    hostile=True,
    skin="#3E3943", hide="#2C2830", accent="#7CF0DC", eye="#C8FFF4", bone="#B8A98A",
    overlays=("carapace_ridge", "crystal_spurs", "bioluminescent_freckles"),
    max_health=460.0, movement_speed=0.22, attack_damage=16.0, attack_knockback=2.5,
    follow_range=40.0, armour=18.0, scale=3.4,
    goals=(
        "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
        "look_at_player", "random_look_around", "water_avoiding_random_stroll",
    ),
    behaviour_tags=("boss", "burrowing", "environmental_adaptation"),
    target_classes=("minecraft:player", "biomesunseen:warden_acolyte"),
    model_width=3.4, model_height=2.4, geo="warden_of_the_hollow_deep",
    shadow_radius=1.8, fire_immune=True,
    animations=_boss_animations(
        "animation.phase.burrow", "animation.phase.tremor_slam",
        "animation.phase.spire_rise", "animation.spawn",
    ),
    render_layer="cutout",
    spawn_biomes=("tremor_ward",), spawn_weight=0, spawn_group=(1, 1),
    spawn_category="monster",
    drops=(("biomesunseen:hollowite_gem", 8, 16, 1.0),
           ("biomesunseen:warden_carapace", 1, 1, 1.0),
           ("biomesunseen:basaltic_core", 4, 8, 1.0),
           ("biomesunseen:lore_book_hollow", 1, 1, 1.0)),
    experience=600,
    lore="The acolytes brace everything against the floor. Now you know why.",
)

WARDEN_OF_THE_HOLLOW_DEEP = BossSpec(
    id="warden_of_the_hollow_deep",
    name="Warden of the Hollow Deep",
    dimension="hollow_deep",
    arena_structure="biomesunseen:warden_of_the_hollow_deep_arena",
    music="biomesunseen:music.boss.warden_of_the_hollow_deep",
    boss_bar_color="blue",
    boss_bar_overlay="notched_12",
    texture_size=64,
    model_width=3.4, model_height=2.4, scale=3.4,
    phases=(
        BossPhase(1, "Burrowed", 0.75, "animation.spawn",
                  "It stays under the arena. Only the drill limbs break surface, "
                  "and tremors telegraph where.",
                  abilities=("drill_strike", "tremor_pulse"),
                  extra_goals=("melee_attack",)),
        BossPhase(2, "Tremor Slam", 0.5, "animation.phase.tremor_slam",
                  "It surfaces and slams. The shockwave travels along the floor "
                  "and must be jumped; standing on a spire is safe.",
                  abilities=("tremor_slam", "drill_strike", "carapace_guard"),
                  extra_goals=("melee_attack",)),
        BossPhase(3, "Spire Rise", 0.25, "animation.phase.spire_rise",
                  "Bioluminescent spires rise across the arena, creating high "
                  "ground and line-of-sight cover. It climbs them.",
                  abilities=("spire_rise", "tremor_slam", "drill_strike"),
                  extra_goals=("melee_attack", "summon_minions")),
        BossPhase(4, "Core Breach", 0.0, "animation.phase.burrow",
                  "The carapace cracks open along the seams and vents light. "
                  "Armour drops to zero; damage output doubles.",
                  abilities=("core_vent", "spire_rise", "tremor_slam", "drill_strike"),
                  extra_goals=("melee_attack", "ranged_attack")),
    ),
    loot_table="biomesunseen:entities/boss/warden_of_the_hollow_deep",
    spawn_item="biomesunseen:warden_of_the_hollow_deep_sigil",
    mob=_WARDEN_MOB,
)

# ---------------------------------------------------------------------------
#  BOSS 4 -- THE SKYWARD CROWN
# ---------------------------------------------------------------------------

_CROWN_MOB = MobSpec(
    id="the_skyward_crown",
    name="The Skyward Crown",
    family="avian",
    dimension="aetherfall",
    category="ancient",
    hostile=True,
    skin="#C7A44C", hide="#9E7F38", accent="#FFE9A8", eye="#FFFFFF", bone="#FFEFD9",
    overlays=("crown_shards", "beak_hooked", "wing_membrane"),
    max_health=380.0, movement_speed=0.32, attack_damage=13.0, attack_knockback=1.8,
    follow_range=64.0, armour=10.0, scale=2.8,
    goals=(
        "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
        "look_at_player", "random_look_around", "water_avoiding_random_stroll",
    ),
    behaviour_tags=("boss", "aerial", "summoner", "ranged"),
    target_classes=("minecraft:player", "biomesunseen:crown_sentinel"),
    model_width=2.8, model_height=2.6, geo="the_skyward_crown",
    shadow_radius=1.5, fire_immune=True,
    animations=_boss_animations(
        "animation.phase.aerial_dive", "animation.phase.crown_split",
        "animation.phase.shard_orbit", "animation.spawn",
    ),
    render_layer="cutout",
    spawn_biomes=("crown_apex",), spawn_weight=0, spawn_group=(1, 1),
    spawn_category="monster",
    drops=(("biomesunseen:aetherium_ingot", 8, 16, 1.0),
           ("biomesunseen:crown_shard", 3, 3, 1.0),
           ("biomesunseen:starfall_core", 2, 4, 1.0),
           ("biomesunseen:lore_book_aether", 1, 1, 1.0)),
    experience=600,
    lore="The throne at the top of the staircase is occupied. It has been for a long time.",
)

THE_SKYWARD_CROWN = BossSpec(
    id="the_skyward_crown",
    name="The Skyward Crown",
    dimension="aetherfall",
    arena_structure="biomesunseen:the_skyward_crown_arena",
    music="biomesunseen:music.boss.the_skyward_crown",
    boss_bar_color="yellow",
    boss_bar_overlay="notched_20",
    texture_size=64,
    model_width=2.8, model_height=2.6, scale=2.8,
    phases=(
        BossPhase(1, "Enthroned", 0.8, "animation.spawn",
                  "It does not leave the throne platform. Wing gusts push you "
                  "toward the arena edge and sentinels walk in.",
                  abilities=("wing_gust", "summon_crown_sentinels", "talons"),
                  extra_goals=("melee_attack", "summon_minions")),
        BossPhase(2, "Aerial Dive", 0.55, "animation.phase.aerial_dive",
                  "It takes to the air and dive-bombs the arena floor on a "
                  "telegraphed shadow marker.",
                  abilities=("aerial_dive", "wing_gust", "feather_volley", "talons"),
                  extra_goals=("melee_attack", "ranged_attack", "fly")),
        BossPhase(3, "Crown Split", 0.3, "animation.phase.crown_split",
                  "The crown detaches and splits into three orbiting shards. "
                  "The main body is invulnerable until all three are destroyed.",
                  abilities=("crown_split", "shard_orbit", "aerial_dive", "feather_volley"),
                  extra_goals=("summon_minions", "ranged_attack"),
                  invulnerable_ticks=60),
        BossPhase(4, "Coronation", 0.0, "animation.phase.shard_orbit",
                  "The shards return and fuse. Every ability fires at once and "
                  "the arena islands begin to drift apart.",
                  abilities=("coronation_burst", "aerial_dive", "crown_split",
                             "feather_volley", "wing_gust", "arena_decay"),
                  extra_goals=("melee_attack", "ranged_attack", "summon_minions")),
    ),
    loot_table="biomesunseen:entities/boss/the_skyward_crown",
    spawn_item="biomesunseen:skyward_crown_regalia",
    mob=_CROWN_MOB,
)

# ---------------------------------------------------------------------------
#  BOSS 5 -- THE UNRAVELING
# ---------------------------------------------------------------------------

_UNRAVELING_MOB = MobSpec(
    id="the_unraveling",
    name="The Unraveling",
    family="biped",
    dimension="void_between",
    category="harsh",
    hostile=True,
    skin="#A81A73", hide="#770C4F", accent="#FF6FD8", eye="#FFFFFF", bone="#E0309F",
    overlays=("void_fractures", "eyes_glowing", "crystal_spurs"),
    max_health=500.0, movement_speed=0.3, attack_damage=15.0, attack_knockback=2.0,
    follow_range=64.0, armour=6.0, scale=2.2,
    goals=(
        "float", "melee_attack", "hurt_by_target", "nearest_attackable_target_player",
        "look_at_player", "random_look_around", "water_avoiding_random_stroll",
    ),
    behaviour_tags=("boss", "phase_shift", "summoner", "ranged"),
    target_classes=("minecraft:player", "biomesunseen:unraveling_shard"),
    model_width=1.6, model_height=2.6, geo="the_unraveling",
    shadow_radius=1.2, fire_immune=True,
    animations=_boss_animations(
        "animation.form.quadruped", "animation.form.serpent", "animation.form.humanoid",
        "animation.phase.glitch_burst", "animation.spawn",
    ),
    render_layer="translucent",
    spawn_biomes=("unraveling_nexus",), spawn_weight=0, spawn_group=(1, 1),
    spawn_category="monster",
    drops=(("biomesunseen:nullite_shard", 8, 16, 1.0),
           ("biomesunseen:unraveling_core", 1, 1, 1.0),
           ("biomesunseen:chronosite_core", 3, 6, 1.0),
           ("biomesunseen:lore_book_unraveling", 1, 1, 1.0)),
    experience=800,
    lore="It is not a creature. It is the shape the dimension takes when it stops holding together.",
)

THE_UNRAVELING = BossSpec(
    id="the_unraveling",
    name="The Unraveling",
    dimension="void_between",
    arena_structure="biomesunseen:the_unraveling_arena",
    music="biomesunseen:music.boss.the_unraveling",
    boss_bar_color="pink",
    boss_bar_overlay="notched_6",
    texture_size=64,
    model_width=1.6, model_height=2.6, scale=2.2,
    phases=(
        BossPhase(1, "Quadruped", 0.75, "animation.form.quadruped",
                  "It resolves as a four-legged thing and runs. Fast, low, and "
                  "it does not stop for walls.",
                  abilities=("charge", "claw_flurry", "glitch_step"),
                  extra_goals=("melee_attack",)),
        BossPhase(2, "Serpent", 0.5, "animation.form.serpent",
                  "It elongates into a segmented coil that constricts the arena "
                  "centre and spits corruption.",
                  abilities=("constrict", "corruption_spit", "glitch_step", "claw_flurry"),
                  extra_goals=("melee_attack", "ranged_attack")),
        BossPhase(3, "Humanoid", 0.25, "animation.form.humanoid",
                  "It stands up. It is now the fastest and hardest-hitting form "
                  "and it summons shards of itself.",
                  abilities=("unraveling_slam", "summon_shards", "corruption_spit",
                             "glitch_step"),
                  extra_goals=("melee_attack", "summon_minions")),
        BossPhase(4, "Terminal", 0.0, "animation.phase.glitch_burst",
                  "All three forms at once, cycling every six seconds. The "
                  "arena stops rendering at the edges.",
                  abilities=("form_cycle", "unraveling_slam", "constrict", "charge",
                             "summon_shards", "arena_decay"),
                  extra_goals=("melee_attack", "ranged_attack", "summon_minions")),
    ),
    loot_table="biomesunseen:entities/boss/the_unraveling",
    spawn_item="biomesunseen:unraveling_paradox",
    mob=_UNRAVELING_MOB,
)

# ---------------------------------------------------------------------------
#  REGISTRY
# ---------------------------------------------------------------------------

ALL_BOSSES: List[BossSpec] = [
    HEART_OF_THE_FOREST,
    VOID_SERPENT,
    WARDEN_OF_THE_HOLLOW_DEEP,
    THE_SKYWARD_CROWN,
    THE_UNRAVELING,
]

BOSS_BY_ID: Dict[str, BossSpec] = {}
for _b in ALL_BOSSES:
    if _b.id in BOSS_BY_ID:
        raise ValueError(f"duplicate boss id {_b.id!r}")
    BOSS_BY_ID[_b.id] = _b


def bosses_in(dimension: str) -> List[BossSpec]:
    return [b for b in ALL_BOSSES if b.dimension == dimension]


def boss_by_id(boss_id: str) -> BossSpec:
    try:
        return BOSS_BY_ID[boss_id]
    except KeyError:
        raise KeyError(f"unknown boss {boss_id!r}") from None
