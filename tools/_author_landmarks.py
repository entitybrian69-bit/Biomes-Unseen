#!/usr/bin/env python3
"""
One-shot authoring pass: emit the 81 landmark structures that the biome table
references but that had no StructureSpec.

Each is written as a literal StructureSpec(...) into tools/content/structures.py
so the table stays self-contained and reviewable. Placement rules, terrain
adaptation, lore book and loot theme are derived from the dimension and
category of the biome(s) that reference the structure -- which is exactly the
information a level designer would use -- and then the lore line is authored by
hand per structure.

Deterministic: sorted by id, salts allocated from a reserved band.
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import content.biomes as B          # noqa: E402
import content.structures as S      # noqa: E402

SALT_BASE = 9001        # reserved band; existing specs use 5101..8806

# Underground landmarks: enclosed, so they get a burying terrain adaptation and
# a deeper root. Everything else is a surface or underwater landmark.
UNDERGROUND_TOKENS = ("cave", "chamber", "vault", "crypt", "warren", "tunnel",
                      "pit", "rootdeep")

# Per-dimension placement profile: (step, terrain_adaptation, start_height,
# spacing, separation, max_depth, lore_book, lore_theme)
DIMENSION_PROFILE = {
    "hollow_deep": ("underground_structures", "encasing", -40, 30, 15, 4,
                    "lore_book_hollow", "hollow"),
    "aetherfall": ("surface_structures", "none", 128, 28, 14, 4,
                   "lore_book_aether", "aether"),
    "void_between": ("surface_structures", "none", 48, 26, 13, 4,
                     "lore_book_void", "void"),
}

# Overworld profiles keyed by biome category.
CATEGORY_PROFILE = {
    "ethereal": ("surface_structures", "beard_thin", 68, 34, 17, 3,
                 "lore_book_star", "star"),
    "ancient": ("surface_structures", "bury", 66, 30, 15, 4,
                "lore_book_ancient", "ancient"),
    "vibrant": ("surface_structures", "beard_thin", 64, 26, 13, 3,
                "lore_book_road", "road"),
    "harsh": ("surface_structures", "beard_box", 70, 32, 16, 3,
              "lore_book_ash", "ash"),
    "aquatic": ("surface_structures", "none", 54, 28, 14, 3,
                "lore_book_tide", "tide"),
}

# Hand-authored lore, one line per landmark. These surface in the structure's
# lore book, so they are written as observations rather than descriptions.
LORE = {
    "abyssal_vent": "The water here is warm. Nothing that lives in it should be.",
    "amberwood_hollow": "A tree fell over a long time ago and something moved in.",
    "ancestor_shrine": "Names are cut into it. Some of the names are still in use.",
    "aurora_bridge": "It only looks solid while you are not looking at your feet.",
    "barrens_obelisk": "One stone, standing, for no reason anyone has agreed on.",
    "blackwater_shack": "Somebody lived here. The door was locked from the inside.",
    "bleeding_spire_field": "They grow toward the sound of water and away from light.",
    "blight_pit": "The edge is soft. Do not test how soft.",
    "bone_colossus": "A ribcage you can walk into, and something has already walked in.",
    "brine_hut": "Salt-cured timber, salt-cured rope, salt-cured occupant.",
    "bronze_barrow": "Green with age and still, somehow, warm to the touch.",
    "chitin_warren": "Every tunnel is exactly wide enough. That is the problem.",
    "chromatic_reef_arch": "The colour shifts as you swim through. So do you.",
    "chrono_ruin": "Ruined, but the ruin happened later than the building.",
    "cinder_oasis": "Water in a place that should have boiled it off centuries ago.",
    "coral_arch": "Grown, not built. The symmetry is the unsettling part.",
    "dusk_mirror_hall": "Every surface reflects. Not all of them reflect the room.",
    "echo_chasm_span": "Drop a stone and you will hear it land twice.",
    "emberfall_watchtower": "Still lit. Nobody has climbed it in a hundred years.",
    "fallen_forge": "The forge is cold and the last casting was never finished.",
    "fissure_bridge": "Planks over a crack that is still widening.",
    "flooded_temple": "The altar is under two metres of clear, still water.",
    "frozen_waystation": "Provisioned for a party that never arrived.",
    "fungal_forest_hollow": "A cap the size of a roof, and it is load-bearing.",
    "geyser_ring": "Stones arranged in a circle that always stays dry.",
    "gilded_archive": "Catalogued, indexed, and every entry has been redacted.",
    "glacial_pier": "Built out over ice that has since moved forty metres.",
    "glacier_cave_mouth": "Breathes. Cold in, warmer out, roughly every minute.",
    "glassland_spire": "Translucent from the base up, and you can see the stairs.",
    "glitch_garden_maze": "The hedges repeat. The repeats do not match.",
    "gorge_bridge": "Rope, timber, and a drop nobody has ever measured.",
    "grave_ice_shipwreck": "Frozen upright. The manifest is legible.",
    "harvest_barn": "Full. Whatever was stored here was never collected.",
    "hieroglyph_wall": "A mile of carving that stops mid-sentence.",
    "hollow_core_vault": "The door is on the inside of the vault.",
    "hollow_harbour": "Mooring posts for boats that could not have floated here.",
    "jewel_reef_arch": "Worth a fortune and structurally load-bearing.",
    "kelp_cathedral_arch": "Nave, aisle, altar. All kelp. All still growing.",
    "lagoon_platform": "Stilts over water clear enough to see the bottom move.",
    "lantern_terrace_shrine": "Every lantern is lit and none of them have fuel.",
    "mangrove_platform": "Built into the roots rather than on top of them.",
    "marble_quarry": "Abandoned mid-cut, with the tools still racked.",
    "march_watchtower": "Sighted along a road that no longer exists.",
    "meadow_windmill": "Turns on days with no wind at all.",
    "monolith_row": "Seven stones, evenly spaced, aligned to nothing overhead.",
    "null_sea_wreck": "A hull with no water inside it, below the surface.",
    "obsidian_shelf_spire": "Glass-black, and it hums when struck.",
    "orchard_pavilion": "Shade for a harvest that has not been gathered.",
    "paradox_chamber": "The room is bigger from the inside by exactly one room.",
    "peak_aerie": "Nest material, arranged. Something is still maintaining it.",
    "pearl_bed_pavilion": "An oyster farm with the oysters left in place.",
    "pearl_depth_shrine": "Offerings weighted to sink, and they have.",
    "pyroclast_vent": "A chimney that vents straight through the crust.",
    "ravine_bridge": "Older than the ravine, which is the only explanation.",
    "recursive_farm": "Furrowed in a pattern that contains the same pattern.",
    "rimeforest_shrine": "Ice grown into a shape the trees were persuaded toward.",
    "river_lantern_pier": "Lanterns set to guide boats up a river with no boats.",
    "rootdeep_chamber": "Roots form the walls, the ceiling, and the furniture.",
    "sakura_torii": "Painted, repainted, and the paint is still wet.",
    "saltflat_caravan": "Wagons in a line, wheels sunk, cargo intact.",
    "seagrass_buoy_line": "Buoys marking a channel that has silted shut.",
    "shatterbelt_crossing": "Stepping stones that are not quite where they look.",
    "shattered_archive": "Every scroll is in fragments and every fragment is filed.",
    "skyward_stair": "A staircase with no building attached to it.",
    "starfall_vault": "Lined with something that fell, and it is still warm.",
    "stormback_lightning_scar": "Glass where the sand was. It branches.",
    "stormcell_spire": "A rod, deliberately, on the highest thing for miles.",
    "sulphur_vent_cluster": "Yellow crust, bad smell, worse footing.",
    "sunken_cathedral": "Bell tower still above the waterline at low tide.",
    "sunscorch_outpost": "Shaded on every side and still unbearably hot.",
    "sunspire_obelisk": "Catches the first light and holds it too long.",
    "terminal_glade_shrine": "The last green thing, kept that way on purpose.",
    "tidal_weir": "Works. Somebody is still maintaining the sluice.",
    "tideglass_pavilion": "Floor panes over the reef, and the reef is watching.",
    "titan_remains": "A hand, a shoulder, and a great deal of distance between.",
    "twilight_terrace_shrine": "Terraced for a sun that sets and stays set.",
    "verdantheight_ruin": "Overgrown so thoroughly the walls are optional.",
    "volcanic_vent_field": "Hundreds of vents, all quiet at the same time.",
    "witherwood_gallows": "A frame in dead wood. Nothing is hanging from it.",
    "woodland_cairn": "Stacked stones, each one carried a long way.",
    "zephyr_pylon": "Anchored against a wind that only blows upward.",
}


def profile(biome, structure_id: str):
    """Placement profile for a landmark, from its biome and its own id."""
    dim = biome.dimension
    if dim in DIMENSION_PROFILE:
        step, adapt, height, spacing, sep, depth, book, theme = \
            DIMENSION_PROFILE[dim]
    else:
        step, adapt, height, spacing, sep, depth, book, theme = \
            CATEGORY_PROFILE[biome.category]

    # Enclosed Overworld landmarks sit below the surface and get buried in.
    if dim == "overworld" and any(t in structure_id for t in UNDERGROUND_TOKENS):
        step, adapt, height, depth = "underground_structures", "beard_thin", 24, 4

    # Aquatic landmarks anchor relative to the biome's own water level.
    if dim == "overworld" and biome.category == "aquatic":
        height = max(38, biome.sea_level - 10)

    return step, adapt, height, spacing, sep, depth, book, theme


def sibling_biomes(biome, taken, limit=2):
    """Up to `limit` other biomes of the same dimension and category."""
    out = []
    for cand in B.ALL_BIOMES:
        if len(out) >= limit:
            break
        if cand.id in taken or cand.id == biome.id:
            continue
        if cand.dimension == biome.dimension and cand.category == biome.category:
            out.append(cand.id)
    return out


def titleize(ident: str) -> str:
    return " ".join(w.capitalize() for w in ident.split("_"))


def main() -> int:
    have = {s.id for s in S.ALL_STRUCTURES}
    refs = {}
    for biome in B.ALL_BIOMES:
        for sid in biome.structures:
            bare = sid.split(":")[-1]
            if bare in have:
                continue
            refs.setdefault(bare, []).append(biome)

    missing = sorted(refs)
    unauthored = [m for m in missing if m not in LORE]
    if unauthored:
        print("ERROR: no authored lore for:")
        for u in unauthored:
            print("   ", u)
        return 1

    lines = []
    lines.append("")
    lines.append("# ---------------------------------------------------------------------------")
    lines.append("#  BIOME LANDMARKS")
    lines.append("#")
    lines.append("#  Every biome in the table names the landmark that spawns inside it. These")
    lines.append("#  are those landmarks: derived from the biome that references them, so their")
    lines.append("#  placement rules, terrain adaptation and lore theme match the place they")
    lines.append("#  actually generate in. No biome may reference a structure that does not")
    lines.append("#  exist -- a dangling worldgen reference silently drops the structure.")
    lines.append("# ---------------------------------------------------------------------------")
    lines.append("")
    lines.append("BIOME_LANDMARKS: List[StructureSpec] = [")

    for index, sid in enumerate(missing):
        biomes = refs[sid]
        primary = biomes[0]
        step, adapt, height, spacing, sep, depth, book, theme = \
            profile(primary, sid)

        biome_ids = [b.id for b in biomes]
        for extra in sibling_biomes(primary, set(biome_ids)):
            if extra not in biome_ids:
                biome_ids.append(extra)
        biome_ids = biome_ids[:4]

        salt = SALT_BASE + index
        lore = LORE[sid]
        btuple = ", ".join(f'"{b}"' for b in biome_ids)

        lines.append(f'    StructureSpec("{sid}", "{titleize(sid)}", '
                     f'"{primary.dimension}", "jigsaw",')
        lines.append(f'                  "{step}", "{adapt}", '
                     f'{spacing}, {sep}, {salt}, {height},')
        lines.append(f'                  "structures/{sid}", {depth},')
        lines.append(f'                  ({btuple},),')
        lines.append(f'                  ("biomesunseen:chests/{sid}", '
                     f'"biomesunseen:chests/lore/{theme}"),')
        lines.append(f'                  "biomesunseen:{book}",')
        lines.append(f'                  lore={lore!r}),')

    lines.append("]")
    lines.append("")

    block = "\n".join(lines) + "\n"

    path = os.path.join(HERE, "content", "structures.py")
    src = open(path, "r", encoding="utf-8").read()

    # Insert the new list just before ALL_STRUCTURES and fold it in.
    anchor = "ALL_STRUCTURES: List[StructureSpec] = BOSS_ARENAS + PORTAL_STRUCTURES + WORLD_STRUCTURES"
    assert anchor in src, "ALL_STRUCTURES anchor missing"
    new_all = ("ALL_STRUCTURES: List[StructureSpec] = (BOSS_ARENAS + PORTAL_STRUCTURES\n"
               "                                    + WORLD_STRUCTURES + BIOME_LANDMARKS)")
    src = src.replace(anchor, block + "\n" + new_all, 1)

    src = src.replace('"""\ncontent/structures.py -- 34 structures.',
                      '"""\ncontent/structures.py -- 115 structures.', 1)

    open(path, "w", encoding="utf-8").write(src)
    print(f"appended {len(missing)} BIOME_LANDMARKS to content/structures.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
