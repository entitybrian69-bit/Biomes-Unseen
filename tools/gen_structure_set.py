#!/usr/bin/env python3
"""Generates the 114 structures from tools/spec/structures.py (standard library only).

Per structure: structures/gen/<id>.nbt, worldgen/template_pool/gen/<id>.json, worldgen/structure/<id>.json.
Per scope (12 Hollow Deep themes + 10 Overworld groups): one structure_set and a has_structure biome tag.
Run tools/gen_biomes.py and tools/gen_models.py first (biome ids and guard mobs come from their specs).
Usage: python tools/gen_structure_set.py
"""
import os
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from jsonfmt import write  # noqa: E402
from spec.biomes import DIM_BIOMES, OW_BIOMES  # noqa: E402
from spec.mobs import MOBS  # noqa: E402
from spec.structures import PALETTES, STRUCTURES  # noqa: E402
from structkit import BUILDERS, assemble  # noqa: E402

ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "src", "main", "resources", "data", "biomesunseen")
NS = "biomesunseen:"


def guard_for(theme):
    mobs = [m for m in MOBS if m[13] == theme]
    brutes = [m for m in mobs if m[2] == "brute"]
    return NS + (brutes or mobs)[0][0] if mobs else ""


def structure_json(scope, base, tag):
    common = {"type": "minecraft:jigsaw", "biomes": "#biomesunseen:has_structure/" + tag, "spawn_overrides": {},
              "size": 1, "max_distance_from_center": 80, "use_expansion_hack": False}
    if scope.startswith("ow:"):
        common.update({"step": "surface_structures", "terrain_adaptation": "beard_thin",
                       "project_start_to_heightmap": "WORLD_SURFACE_WG", "start_height": {"absolute": -base}})
    else:
        common.update({"step": "underground_structures", "terrain_adaptation": "none",
                       "start_height": {"absolute": 26 - base}})
    return common


def main():
    scopes = {}
    for sid, name, arch, a, b, pal, scope in STRUCTURES:
        assert arch in BUILDERS and pal in PALETTES, sid
        overworld = scope.startswith("ow:")
        base = 3 if overworld else 6
        guard = "" if overworld else guard_for(scope)
        size, data, count = assemble(arch, PALETTES[pal], a, b, base, guard)
        path = os.path.join(DATA, "structures", "gen", sid + ".nbt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(data)
        tag = scope.replace(":", "_")
        write(os.path.join(DATA, "worldgen", "template_pool", "gen", sid + ".json"), {
            "name": NS + "gen/" + sid, "fallback": "minecraft:empty",
            "elements": [{"weight": 1, "element": {"element_type": "minecraft:single_pool_element",
                          "location": NS + "gen/" + sid, "processors": "minecraft:empty", "projection": "rigid"}}]})
        write(os.path.join(DATA, "worldgen", "structure", sid + ".json"), {
            **structure_json(scope, base, tag), "start_pool": NS + "gen/" + sid}, width=140)
        scopes.setdefault(scope, []).append(sid)
    for scope, ids in scopes.items():
        tag = scope.replace(":", "_")
        if scope.startswith("ow:"):
            biomes = [NS + b[0] for b in OW_BIOMES if b[2] == scope[3:]]
            spacing, separation = 16, 6
        else:
            biomes = [NS + b for b in DIM_BIOMES[scope]]
            spacing, separation = 12, 5
        write(os.path.join(DATA, "tags", "worldgen", "biome", "has_structure", tag + ".json"),
              {"replace": False, "values": biomes})
        write(os.path.join(DATA, "worldgen", "structure_set", "gen_" + tag + ".json"), {
            "structures": [{"structure": NS + i, "weight": 1} for i in ids],
            "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": separation,
                          "salt": zlib.crc32(scope.encode()) & 0x7FFFFFFF}})
    print("generated %d structures in %d sets" % (len(STRUCTURES), len(scopes)))


if __name__ == "__main__":
    main()
