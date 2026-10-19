#!/usr/bin/env python3
"""
Biomes Unseen -- repository validator.

Runs entirely offline with no third-party dependencies (the CI runner and the
local sandbox both have nothing but a stock CPython). It is the gate that sits
in front of the Gradle build: everything it checks is cheap, and every failure
it reports is something that would otherwise surface as a confusing Minecraft
crash or a silently missing texture at runtime.

Checks performed
----------------
1.  JSON integrity      every .json under src/main/resources parses, and every
                        file is non-empty.
2.  PNG integrity       every .png decodes with our own codec and reports sane
                        dimensions (16x16, 32x32, 64x32, 64x64 ...).
3.  Texture resolution  every texture path referenced by a model, blockstate,
                        particle definition, GeckoLib model or the Java source
                        resolves to a file that actually exists. This is the
                        "no missing textures" Golden Rule, enforced statically.
4.  Registry closure    every registry name referenced from one JSON/Java file
                        (loot table -> block, recipe -> item, spawn egg -> mob,
                        structure -> biome, boss -> arena) exists.
5.  Content table sanity re-imports tools/content/* and asserts the counts and
                        cross-references the mod promises.

Exit code is 0 when clean, 1 when any ERROR was found. Notes (warnings) never
fail the build.
"""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Dict, Iterable, List, Optional, Set, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "src", "main", "resources")
ASSETS = os.path.join(RES, "assets", "biomesunseen")
DATA = os.path.join(RES, "data", "biomesunseen")
JAVA = os.path.join(ROOT, "src", "main", "java")

sys.path.insert(0, HERE)

MODID = "biomesunseen"

# Goal tokens every hostile mob and every boss must carry. These are the
# snake_case names used in tools/content/mobs.py, each of which maps to a real
# vanilla Goal subclass in BUEntityGoals (MeleeAttackGoal, HurtByTargetGoal,
# NearestAttackableTargetGoal). Absence means the entity would stand still and
# never retaliate -- the "no dead AI" Golden Rule.
REQUIRED_COMBAT_GOALS = (
    "melee_attack",
    "hurt_by_target",
    "nearest_attackable_target_player",
)

# Registry folders inside the datapack namespace, as vanilla reads them.
DATA_FOLDERS = (
    "loot_table", "loot_tables", "recipe", "recipes", "advancement",
    "advancements", "tags", "worldgen", "structure", "structures",
    "dimension", "dimension_type", "predicate", "predicates",
    "function", "functions",
)
ASSET_FOLDERS = (
    "blockstates", "models", "textures", "lang", "sounds", "geo",
    "animations", "particles", "font", "gui",
)

# Texture sizes the game accepts for the asset kinds we author. We deliberately
# keep this permissive-but-explicit: an odd size is almost always an authoring
# bug in a glyph map (a row of the wrong length), not a legitimate choice.
VALID_TEXTURE_SIZES: Dict[str, Set[Tuple[int, int]]] = {
    "textures/block": {(16, 16)},
    "textures/item": {(16, 16)},
    "textures/entity": {(64, 32), (64, 64), (32, 32)},
    "textures/entity/boss": {(64, 64)},
    "textures/particle": {(16, 16), (8, 8)},
    "textures/gui": {(16, 16), (256, 256), (182, 16)},
    "textures/gui/boss_bar": {(16, 4), (16, 2)},
}


class Report:
    """Collects errors and notes, then renders them grouped by category."""

    def __init__(self) -> None:
        self.errors: List[str] = []
        self.notes: List[str] = []
        self.checked: Dict[str, int] = {}

    def error(self, category: str, message: str) -> None:
        self.errors.append(f"[{category}] {message}")

    def note(self, category: str, message: str) -> None:
        self.notes.append(f"[{category}] {message}")

    def count(self, category: str, n: int = 1) -> None:
        self.checked[category] = self.checked.get(category, 0) + n

    def render(self) -> int:
        for category, n in sorted(self.checked.items()):
            print(f"  ok  {category:<34} {n}")
        if self.notes:
            print(f"\n{len(self.notes)} note(s):")
            for n in self.notes[:60]:
                print("   ~ " + n)
            if len(self.notes) > 60:
                print(f"   ... and {len(self.notes) - 60} more")
        if self.errors:
            print(f"\n{len(self.errors)} ERROR(S):")
            for e in self.errors[:120]:
                print("   ! " + e)
            if len(self.errors) > 120:
                print(f"   ... and {len(self.errors) - 120} more")
            return 1
        print("\nvalidation clean.")
        return 0


def walk(root: str, suffix: str) -> List[str]:
    if not os.path.isdir(root):
        return []
    out = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(suffix):
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def rel(path: str) -> str:
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


# --------------------------------------------------------------------------- #
# 1 + 2. JSON and PNG integrity
# --------------------------------------------------------------------------- #

def check_json(report: Report) -> Dict[str, object]:
    """Parse every JSON resource; return {relative path: parsed object}."""
    parsed: Dict[str, object] = {}
    for path in walk(RES, ".json"):
        text = open(path, "r", encoding="utf-8").read()
        if not text.strip():
            report.error("json", f"{rel(path)} is empty")
            continue
        try:
            parsed[rel(path)] = json.loads(text)
        except Exception as exc:  # noqa: BLE001 -- report and continue
            report.error("json", f"{rel(path)} failed to parse: {exc}")
    report.count("json files parsed", len(parsed))
    return parsed


def check_png(report: Report) -> None:
    """Decode every PNG with our own codec and verify its size is expected."""
    from png_codec import png_dimensions

    for path in walk(ASSETS, ".png"):
        r = rel(path)
        try:
            with open(path, "rb") as fh:
                blob = fh.read()
            w, h = png_dimensions(blob)
        except Exception as exc:  # noqa: BLE001
            report.error("png", f"{r} is not a decodable PNG: {exc}")
            continue
        if w <= 0 or h <= 0:
            report.error("png", f"{r} has non-positive dimensions {w}x{h}")
            continue
        # Locate the asset-kind folder to pick the allowed size set. The most
        # specific (longest) folder key must win, otherwise textures/gui swallows
        # textures/gui/boss_bar and its stricter 16x4 expectation.
        inner = f"/{r.split('assets/biomesunseen/', 1)[-1]}"
        kind = None
        for key in sorted(VALID_TEXTURE_SIZES, key=len, reverse=True):
            if f"/{key}/" in inner:
                kind = key
                break
        if kind and (w, h) not in VALID_TEXTURE_SIZES[kind]:
            report.error(
                "png",
                f"{r} is {w}x{h} but {kind} expects one of "
                f"{sorted(VALID_TEXTURE_SIZES[kind])}",
            )
        report.count("png files decoded", 1)


# --------------------------------------------------------------------------- #
# 3. Texture path resolution  (the "no missing textures" Golden Rule)
# --------------------------------------------------------------------------- #

NAMESPACE_RE = re.compile(r"^(?:([a-z0-9_.-]+):)?([a-z0-9_./-]+)$")


def existing_textures() -> Set[str]:
    """Every texture we ship, as a namespaced id: 'biomesunseen:block/stone'."""
    out: Set[str] = set()
    for path in walk(ASSETS, ".png"):
        p = rel(path)
        marker = "assets/biomesunseen/textures/"
        if marker not in p:
            continue
        ident = p.split(marker, 1)[1][:-4]  # strip .png
        out.add(f"{MODID}:{ident}")
        out.add(ident)  # allow unqualified refs inside our own namespace
    return out


def resolve_texture_ref(ref: str, have: Set[str], report: Report,
                        where: str, category: str = "texture-ref") -> None:
    """Validate a single texture reference."""
    ref = ref.strip()
    if not ref or ref.startswith("#") or ref.startswith("data:"):
        return
    m = NAMESPACE_RE.match(ref)
    if not m:
        report.error(category, f"{where}: malformed texture ref {ref!r}")
        return
    ns, path = m.group(1) or MODID, m.group(2)
    if ns != MODID:
        return  # vanilla or third-party reference -- not ours to ship
    if path not in have and f"{ns}:{path}" not in have:
        report.error(category, f"{where}: missing texture '{ns}:{path}'")


def collect_texture_refs(parsed: Dict[str, object]) -> List[Tuple[str, str]]:
    """
    Walk every parsed JSON and pull out strings that look like texture paths.

    We key off the JSON property names vanilla and GeckoLib actually use, which
    avoids false positives from arbitrary strings that merely contain a slash.
    """
    keys = {"texture", "textures", "layer0", "layer1", "layer2", "particle",
            "all", "north", "south", "east", "west", "up", "down", "front",
            "back", "side", "top", "bottom", "cross", "overlay", "texture_id"}
    out: List[Tuple[str, str]] = []

    def rec(node: object, where: str, parent_key: Optional[str]) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                rec(v, where, k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                rec(v, f"{where}[{i}]", parent_key)
        elif isinstance(node, str):
            if parent_key in keys and node and not node.startswith("#"):
                out.append((where, node))
            elif parent_key == "texture":
                out.append((where, node))

    for where, obj in parsed.items():
        rec(obj, where, None)
    return out


def check_java_texture_refs(have: Set[str], report: Report) -> None:
    """
    Scan Java sources for ResourceLocation texture strings.

    Only literal "textures/..." strings are considered; anything built by
    concatenation is reported as a note so a human can eyeball it.
    """
    lit = re.compile(r'"(textures/[a-z0-9_./-]+)"')
    built = re.compile(r'"textures/[a-z0-9_./-]*"\s*\+')
    for path in walk(JAVA, ".java"):
        text = open(path, "r", encoding="utf-8").read()

        # A concatenation prefix such as "textures/entity/" + id + ".png" is not
        # a resolvable path -- it is half of one. Collect the spans the dynamic
        # pattern covers and skip them in the literal scan, otherwise the prefix
        # is reported as a missing texture while the same span is also (correctly)
        # noted as dynamic. Only a complete literal can be resolved.
        dynamic_spans = [m.span() for m in built.finditer(text)]
        for m in built.finditer(text):
            report.note("java-texture",
                        f"{rel(path)}: dynamic texture path at {m.group(0)!r}")

        for m in lit.finditer(text):
            if any(start <= m.start() < end for start, end in dynamic_spans):
                continue
            resolve_texture_ref(m.group(1), have, report, rel(path), "java-texture")
            report.count("java texture refs", 1)


# --------------------------------------------------------------------------- #
# 4. Registry closure
# --------------------------------------------------------------------------- #

RESLOC_RE = re.compile(r"\b" + MODID + r":([a-z0-9_./-]+)")


def collect_namespaced_strings(parsed: Dict[str, object],
                              folder: str, key: Optional[str] = None) -> Set[str]:
    """Every MODID-namespaced path appearing under a datapack folder."""
    out: Set[str] = set()
    for where, obj in parsed.items():
        if folder not in where:
            continue
        if key is None:
            stack = [obj]
            while stack:
                node = stack.pop()
                if isinstance(node, dict):
                    stack.extend(node.values())
                elif isinstance(node, list):
                    stack.extend(node)
                elif isinstance(node, str):
                    for m in RESLOC_RE.finditer(node):
                        out.add(m.group(1))
        else:
            stack = [obj]
            while stack:
                node = stack.pop()
                if isinstance(node, dict):
                    for k, v in node.items():
                        if k == key and isinstance(v, str):
                            for m in RESLOC_RE.finditer(v):
                                out.add(m.group(1))
                        else:
                            stack.append(v)
                elif isinstance(node, list):
                    stack.extend(node)
    return out


def ids_from_disk(folder: str) -> Set[str]:
    """Registry ids present as files on disk under data/<modid>/<folder>."""
    base = os.path.join(DATA, folder)
    out: Set[str] = set()
    for path in walk(base, ".json"):
        r = rel(path)
        marker = f"data/{MODID}/{folder}/"
        if marker in r:
            out.add(r.split(marker, 1)[1][:-5])
    return out


def check_registry_closure(parsed: Dict[str, object], report: Report) -> None:
    """Every cross-reference between our own registries must resolve."""
    # 1.20.1 uses the plural datapack folder name: loot_tables/blocks.
    blocks = ids_from_disk("loot_tables/blocks")
    # Blocks/items are defined in Java, so we take their ids from the generated
    # registry manifest if present, else from blockstates + item models.
    manifest_path = os.path.join(ASSETS, "registry_manifest.json")
    manifest: Dict[str, List[str]] = {}
    if os.path.isfile(manifest_path):
        try:
            manifest = json.loads(open(manifest_path, encoding="utf-8").read())
        except Exception as exc:  # noqa: BLE001
            report.error("manifest", f"registry_manifest.json unreadable: {exc}")
    block_ids = set(manifest.get("blocks", []))
    item_ids = set(manifest.get("items", []))
    entity_ids = set(manifest.get("entities", []))
    biome_ids = set(manifest.get("biomes", []))
    structure_ids = set(manifest.get("structures", []))

    if manifest:
        report.count("manifest blocks", len(block_ids))
        report.count("manifest items", len(item_ids))
        report.count("manifest entities", len(entity_ids))
        report.count("manifest biomes", len(biome_ids))

        # Every block needs a blockstate and a loot table.
        bs_ids = ids_from_disk_assets("blockstates")
        for b in sorted(block_ids - bs_ids):
            report.error("closure", f"block '{b}' has no blockstate json")
        for b in sorted(block_ids - blocks):
            report.error("closure", f"block '{b}' has no block loot table")
        # Every item needs a model, and so does every block that has an item
        # form -- a BlockItem with no model renders as a missing-model cube.
        block_item_ids = set(manifest.get("block_items", []))
        report.count("manifest block items", len(block_item_ids))
        im_ids = model_item_ids()
        for i in sorted(item_ids - im_ids):
            report.error("closure", f"item '{i}' has no item model json")
        for i in sorted(block_item_ids - im_ids):
            report.error("closure", f"block item '{i}' has no item model json")

    # Loot tables referencing ids that do not exist. A reference may be either
    # a registry id (an item or block being dropped) or a nested loot-table
    # path ('chests/lore/grove'), which is valid only if that table is on disk.
    loot_paths = ids_from_disk("loot_tables")
    report.count("loot tables on disk", len(loot_paths))
    if block_ids:
        for ref in sorted(collect_namespaced_strings(parsed, "loot_tables")):
            if ref in item_ids or ref in block_ids:
                continue
            if ref in loot_paths:
                continue
            if "/" in ref:
                report.error("closure",
                             f"loot table references missing nested table '{ref}'")
            else:
                report.error("closure", f"loot table references unknown id '{ref}'")

    # Recipes referencing unknown items.
    if item_ids:
        for ref in sorted(collect_namespaced_strings(parsed, "recipe")):
            base = ref.split("/")[-1]
            if base in item_ids or base in block_ids:
                continue
            report.error("closure", f"recipe references unknown id '{ref}'")

    # Spawn eggs referencing unknown entities.
    if entity_ids:
        for item in sorted(i for i in item_ids if i.endswith("_spawn_egg")):
            mob = item[: -len("_spawn_egg")]
            if mob not in entity_ids:
                report.error("closure",
                             f"spawn egg '{item}' has no entity '{mob}'")

    # Structures referencing unknown biomes.
    if biome_ids:
        for ref in sorted(collect_namespaced_strings(parsed, "worldgen/structure")):
            if ref in biome_ids or ref in structure_ids:
                continue
            report.error("closure",
                         f"structure references unknown biome '{ref}'")


def ids_from_disk_assets(folder: str) -> Set[str]:
    base = os.path.join(ASSETS, folder)
    out: Set[str] = set()
    for path in walk(base, ".json"):
        r = rel(path)
        marker = f"assets/{MODID}/{folder}/"
        if marker in r:
            out.add(r.split(marker, 1)[1][:-5])
    return out


def model_item_ids() -> Set[str]:
    return ids_from_disk_assets("models/item")


# --------------------------------------------------------------------------- #
# 5. Content tables
# --------------------------------------------------------------------------- #

def check_content_tables(report: Report) -> None:
    """Re-import the authored content tables and assert the promised shape."""
    try:
        import content.biomes as B
        import content.ores as O
        import content.mobs as M
        import content.bosses as BS
        import content.gear as G
        import content.structures as S
    except Exception as exc:  # noqa: BLE001
        report.error("content", f"content tables failed to import: {exc}")
        return

    expectations = {
        "biomes": (len(B.ALL_BIOMES), 140),
        "ores": (len(O.ALL_ORES), 44),
        "mobs": (len(M.ALL_MOBS), 80),
        "bosses": (len(BS.ALL_BOSSES), 5),
        "tool sets": (len(G.TOOL_SETS), 10),
        "armor sets": (len(G.ARMOR_SETS), 10),
        "structures": (len(S.ALL_STRUCTURES), 115),
    }
    for name, (got, want) in expectations.items():
        if got != want:
            report.error("content", f"expected {want} {name}, found {got}")
        report.count(f"content {name}", got)

    # Biome category coverage.
    cats: Dict[str, int] = {}
    for b in B.ALL_BIOMES:
        cats[b.category] = cats.get(b.category, 0) + 1
    for c in ("ethereal", "ancient", "vibrant", "harsh", "aquatic"):
        if not cats.get(c):
            report.error("content", f"biome category '{c}' is empty")

    # Every boss must have 4 phases, each with an entry animation, at least one
    # ability and at least one extra goal -- a phase with nothing to do is dead
    # content, which the Golden Rules forbid.
    for boss in BS.ALL_BOSSES:
        if len(boss.phases) < 4:
            report.error("content", f"boss '{boss.id}' has < 4 phases")
        for ph in boss.phases:
            if not ph.entry_animation:
                report.error("content",
                             f"boss '{boss.id}' phase {ph.index} has no animation")
            if not ph.abilities and not ph.extra_goals:
                report.error("content",
                             f"boss '{boss.id}' phase '{ph.name}' is inert")
        # The boss fight itself must declare targeting + melee goals.
        boss_goals = {g for ph in boss.phases for g in ph.extra_goals}
        boss_goals |= set(boss.mob.goals)
        for goal in REQUIRED_COMBAT_GOALS:
            if goal not in boss_goals:
                report.error("content", f"boss '{boss.id}' lacks '{goal}'")

    # Every hostile mob must declare targeting + melee goals (no dead AI).
    # The tables use snake_case goal tokens; BUEntityGoals maps each to a
    # concrete net.minecraft.world.entity.ai.goal class at codegen time.
    for mob in M.ALL_MOBS:
        if not mob.hostile:
            continue
        for goal in REQUIRED_COMBAT_GOALS:
            if goal not in mob.goals:
                report.error("content",
                             f"hostile mob '{mob.id}' lacks '{goal}'")

    # Structure salt collisions would make two structures share a seed offset.
    salts: Dict[int, str] = {}
    for s in S.ALL_STRUCTURES:
        if s.salt in salts:
            report.error("content",
                         f"structures '{salts[s.salt]}' and '{s.id}' share salt")
        salts[s.salt] = s.id


# --------------------------------------------------------------------------- #

def main() -> int:
    report = Report()
    print("Biomes Unseen validator")
    print("=" * 60)

    parsed = check_json(report)
    check_png(report)

    have = existing_textures()
    report.count("textures shipped", len(have) // 2)

    for where, ref in collect_texture_refs(parsed):
        resolve_texture_ref(ref, have, report, where)
        report.count("json texture refs", 1)
    check_java_texture_refs(have, report)

    check_registry_closure(parsed, report)
    check_content_tables(report)

    return report.render()


if __name__ == "__main__":
    raise SystemExit(main())
