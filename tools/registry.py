#!/usr/bin/env python3
"""
Biomes Unseen -- authoritative registry manifest.

Everything downstream (blockstates, block/item models, loot tables, recipes,
tags, lang, the worldgen JSON, and the Java DeferredRegister tables) must agree
on exactly which ids exist. Deriving that list once, here, from the content
tables plus the textures the art pass actually emitted, is what keeps those
seven consumers from drifting apart.

The art pass is treated as ground truth for *existence*: it walked every
content table and emitted a PNG for each block, item and entity the mod ships.
This module re-derives the same ids, classifies them by the model/loot/recipe
shape they need, and cross-checks both directions -- a texture with no registry
entry and a registry entry with no texture are both errors.

Public API
----------
    REGISTRY  -> Registry singleton (built on import)
    Registry.blocks / .items / .entities / .biomes
    Registry.block_kind(id) -> BlockKind
    Registry.write_manifest(path)
"""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Dict, List, Optional, Set, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import content.biomes as BIOMES        # noqa: E402
import content.bosses as BOSSES        # noqa: E402
import content.gear as GEAR            # noqa: E402
import content.mobs as MOBS            # noqa: E402
import content.ores as ORES            # noqa: E402
import content.structures as STRUCTS   # noqa: E402

MODID = "biomesunseen"
ASSETS = os.path.join(ROOT, "src", "main", "resources", "assets", MODID)
TEXTURES = os.path.join(ASSETS, "textures")

# A block texture named X_side / X_top / X_flow is a *face* of block X, not a
# block of its own. Stripping these yields the real block id list.
FACE_SUFFIX_RE = re.compile(r"_(side|top|flow)$")
# Bows ship a pulling overlay; it is a state of the bow item, not an item.
ITEM_STATE_RE = re.compile(r"_pulling_\d+$")


class BlockKind:
    """Model/loot/recipe shape a block needs."""

    CUBE_ALL = "cube_all"          # one texture on all six faces
    GRASS = "grass"                # top + side + bottom(dirt)
    LOG = "log"                    # side + top, pillar rotation
    FLUID = "fluid"                # no model; flowing block, bucket item
    PORTAL = "portal"              # no collision, translucent, no item
    CROSS = "cross"                # plant: single cross texture, cutout
    LANTERN = "lantern"            # emissive cube, lit blockstate
    ALTAR = "altar"                # cube_column (top differs)
    ORE = "ore"                    # cube_all + experience drop
    MINERAL_BLOCK = "mineral_block"  # cube_all, compact-storage recipe


KIND_ORDER = (
    BlockKind.CUBE_ALL, BlockKind.GRASS, BlockKind.LOG, BlockKind.FLUID,
    BlockKind.PORTAL, BlockKind.CROSS, BlockKind.LANTERN, BlockKind.ALTAR,
    BlockKind.ORE, BlockKind.MINERAL_BLOCK,
)


def _texture_ids(folder: str) -> Set[str]:
    d = os.path.join(TEXTURES, *folder.split("/"))
    if not os.path.isdir(d):
        return set()
    return {f[:-4] for f in os.listdir(d) if f.endswith(".png")}


class Registry:
    """Derived, classified, cross-checked id manifest for the whole mod."""

    def __init__(self) -> None:
        self.problems: List[str] = []

        block_textures = _texture_ids("block")
        item_textures = _texture_ids("item")
        entity_textures = _texture_ids("entity")
        boss_textures = _texture_ids("entity/boss")

        # ---- faces -> owning block --------------------------------------
        self.face_of: Dict[str, str] = {}
        for tex in sorted(block_textures):
            m = FACE_SUFFIX_RE.search(tex)
            if not m:
                continue
            base = FACE_SUFFIX_RE.sub("", tex)
            if base not in block_textures:
                self.problems.append(
                    f"face texture '{tex}' has no base block '{base}'")
                continue
            self.face_of.setdefault(base, []).append(m.group(1))

        # ---- blocks -----------------------------------------------------
        self.blocks: List[str] = sorted(
            t for t in block_textures if not FACE_SUFFIX_RE.search(t)
        )
        self.block_set: Set[str] = set(self.blocks)

        # ---- items ------------------------------------------------------
        self.items: List[str] = sorted(
            t for t in item_textures if not ITEM_STATE_RE.search(t)
        )
        self.item_set: Set[str] = set(self.items)

        # Every solid block also gets a BlockItem, so it needs an item model
        # even though no separate item texture exists for it -- the model
        # parents the block model. Fluids have no item form (they are placed by
        # worldgen and the portal igniter, never held), and portal blocks are
        # deliberately unobtainable so they are excluded too.
        self.block_items: List[str] = sorted(
            b for b in self.blocks
            if self._kind_of(b) not in (BlockKind.FLUID, BlockKind.PORTAL)
        )
        self.block_item_set: Set[str] = set(self.block_items)
        self.bow_states: Dict[str, List[str]] = {}
        for tex in sorted(item_textures):
            m = ITEM_STATE_RE.search(tex)
            if m:
                self.bow_states.setdefault(ITEM_STATE_RE.sub("", tex), []).append(tex)

        # ---- entities ---------------------------------------------------
        self.mobs: List[str] = [m.id for m in MOBS.ALL_MOBS]
        self.bosses: List[str] = [b.id for b in BOSSES.ALL_BOSSES]
        self.entities: List[str] = sorted(set(self.mobs) | set(self.bosses))
        self.entity_set: Set[str] = set(self.entities)

        for tex in sorted(entity_textures | boss_textures):
            if tex not in self.entity_set:
                self.problems.append(
                    f"entity texture '{tex}' has no registered entity")
        for ent in self.entities:
            if ent not in entity_textures and ent not in boss_textures:
                self.problems.append(f"entity '{ent}' has no texture")

        # ---- biomes -----------------------------------------------------
        self.biomes: List[str] = [b.id for b in BIOMES.ALL_BIOMES]
        self.biome_set: Set[str] = set(self.biomes)
        self.structures: List[str] = [s.id for s in STRUCTS.ALL_STRUCTURES]

        # ---- classification --------------------------------------------
        self._kind: Dict[str, str] = {}
        self._classify()
        self._cross_check()

    # ------------------------------------------------------------------ #
    #  Classification
    # ------------------------------------------------------------------ #

    def _kind_of(self, block: str) -> str:
        """
        Early kind lookup used while building block_items.

        _classify() has not run yet at that point, so this mirrors just the two
        kinds that matter for deciding whether a block has an item form.
        """
        if "flow" in self.face_of.get(block, []):
            return BlockKind.FLUID
        if block.endswith("_portal"):
            return BlockKind.PORTAL
        return BlockKind.CUBE_ALL

    def _classify(self) -> None:
        """Assign every block the model/loot shape it needs."""
        k = self._kind

        # Ores and their compressed storage blocks come straight from the table.
        for ore in ORES.ALL_ORES:
            if ore.ore_block in self.block_set:
                k[ore.ore_block] = BlockKind.ORE
            if ore.mineral_block in self.block_set:
                k[ore.mineral_block] = BlockKind.MINERAL_BLOCK
            ds = ore.deepslate_ore_block
            if ds and ds in self.block_set:
                k[ds] = BlockKind.ORE

        # Fluids: a flowing block with a still + flow texture pair.
        for b in self.blocks:
            if "flow" in self.face_of.get(b, []):
                k[b] = BlockKind.FLUID

        # Grass: has a _side face and is named like turf.
        for b in self.blocks:
            faces = self.face_of.get(b, [])
            if "side" in faces and b not in k:
                k[b] = BlockKind.GRASS

        # Logs: pillar with a _top face (boss_altar also has a top, handled below).
        for b in self.blocks:
            faces = self.face_of.get(b, [])
            if "top" in faces and b not in k:
                k[b] = BlockKind.LOG

        # Portals and their frames.
        for b in self.blocks:
            if b.endswith("_portal"):
                k[b] = BlockKind.PORTAL
            elif b.endswith("_portal_frame"):
                k.setdefault(b, BlockKind.CUBE_ALL)

        # Emissive / interactive specials.
        for b in self.blocks:
            if b.endswith("_lantern"):
                k[b] = BlockKind.LANTERN
            elif b == "boss_altar":
                k[b] = BlockKind.ALTAR

        # Flora: plants rendered as a cutout cross.
        for b in self.blocks:
            if b in k:
                continue
            if self._is_flora(b):
                k[b] = BlockKind.CROSS

        # Everything else is a plain cube.
        for b in self.blocks:
            k.setdefault(b, BlockKind.CUBE_ALL)

    @staticmethod
    def _is_flora(block: str) -> bool:
        """Plants authored as a single cross texture."""
        flora_suffix = (
            "_fern", "_bloom", "_blossom", "_cluster", "_spike", "_tendril",
            "_sprout", "_bush", "_sapling", "_pod", "_kelp", "_grass",
        )
        if block.endswith(flora_suffix):
            # 'X_grass_block' is turf, not flora; bare 'X_grass' is.
            if block.endswith("_grass") and not block.endswith("_grass_block"):
                return True
            return not block.endswith("_grass_block")
        return block in {"marigold", "moonpetal", "orchid_bloom", "aurora_fern",
                         "starfall_bloom", "sakura_blossom", "tide_kelp"}

    # ------------------------------------------------------------------ #
    #  Cross-checks
    # ------------------------------------------------------------------ #

    def _cross_check(self) -> None:
        """Registry entries and content-table references must agree."""
        # Every ore block the table promises must exist.
        for ore in ORES.ALL_ORES:
            for name in (ore.ore_block, ore.mineral_block, ore.deepslate_ore_block):
                if name and name not in self.block_set:
                    self.problems.append(f"ore '{ore.id}' promises missing block '{name}'")

        # Every surface material a biome names must exist (vanilla excepted).
        for biome in BIOMES.ALL_BIOMES:
            for ref in (biome.surface_top, biome.surface_filler, biome.surface_stone):
                if not ref.startswith(f"{MODID}:"):
                    continue
                path = ref.split(":", 1)[1]
                if path not in self.block_set:
                    self.problems.append(
                        f"biome '{biome.id}' names missing block '{path}'")

        # Every mob drop / gear item must exist as an item.
        for mob in MOBS.ALL_MOBS:
            for drop in mob.drops:
                ident = drop[0].split(":")[-1] if isinstance(drop, tuple) else str(drop)
                if ident and ident not in self.item_set and ":" in str(drop[0]):
                    if not str(drop[0]).startswith("minecraft:"):
                        self.problems.append(
                            f"mob '{mob.id}' drops missing item '{ident}'")

        for ts in GEAR.TOOL_SETS:
            repair = ts.repair_item.split(":")[-1] if ts.repair_item else None
            if repair and repair.startswith(MODID[:4]) is False and \
                    ts.repair_item.startswith(f"{MODID}:") and repair not in self.item_set:
                self.problems.append(
                    f"tool set '{ts.id}' repairs with missing item '{repair}'")

        # Every spawn egg must have a texture and an entity.
        for ent in self.entities:
            egg = f"{ent}_spawn_egg"
            if egg not in self.item_set:
                self.problems.append(f"entity '{ent}' has no spawn egg item")

        # Every boss arena structure must exist. BossSpec stores the arena as a
        # fully qualified id ('biomesunseen:x_arena') while the structure table
        # keys on the bare registry path, so compare on the bare path.
        structure_set = set(self.structures)
        for boss in BOSSES.ALL_BOSSES:
            arena = boss.arena_structure.split(":")[-1]
            if arena not in structure_set:
                self.problems.append(
                    f"boss '{boss.id}' arena '{arena}' is not a structure")

    # ------------------------------------------------------------------ #
    #  Accessors
    # ------------------------------------------------------------------ #

    def block_kind(self, block: str) -> str:
        return self._kind.get(block, BlockKind.CUBE_ALL)

    def blocks_of_kind(self, kind: str) -> List[str]:
        return [b for b in self.blocks if self._kind.get(b) == kind]

    def faces(self, block: str) -> List[str]:
        return list(self.face_of.get(block, []))

    def has_face(self, block: str, face: str) -> bool:
        return face in self.face_of.get(block, [])

    def summary(self) -> Dict[str, int]:
        out: Dict[str, int] = {
            "blocks": len(self.blocks),
            "items": len(self.items),
            "block_items": len(self.block_items),
            "entities": len(self.entities),
            "mobs": len(self.mobs),
            "bosses": len(self.bosses),
            "biomes": len(self.biomes),
            "structures": len(self.structures),
        }
        for kind in KIND_ORDER:
            out[f"kind:{kind}"] = len(self.blocks_of_kind(kind))
        return out

    def manifest(self) -> Dict[str, object]:
        """The JSON the validator reads to check registry closure."""
        return {
            "modid": MODID,
            "blocks": self.blocks,
            "block_kinds": {b: self._kind[b] for b in self.blocks},
            "block_faces": {b: v for b, v in self.face_of.items()},
            "items": self.items,
            "block_items": self.block_items,
            "bow_states": self.bow_states,
            "entities": self.entities,
            "mobs": self.mobs,
            "bosses": self.bosses,
            "biomes": self.biomes,
            "structures": self.structures,
        }

    def write_manifest(self, path: Optional[str] = None) -> str:
        path = path or os.path.join(ASSETS, "registry_manifest.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.manifest(), fh, indent=2, sort_keys=True)
            fh.write("\n")
        return path


REGISTRY = Registry()


def main(argv: Optional[List[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    reg = REGISTRY
    print("Biomes Unseen registry manifest")
    print("=" * 60)
    for key, val in sorted(reg.summary().items()):
        print(f"  {key:<24} {val}")
    if "--write" in argv:
        print("\nwrote " + reg.write_manifest())
    if reg.problems:
        print(f"\n{len(reg.problems)} PROBLEM(S):")
        for p in reg.problems[:80]:
            print("   ! " + p)
        if len(reg.problems) > 80:
            print(f"   ... and {len(reg.problems) - 80} more")
        return 1
    print("\nregistry consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
