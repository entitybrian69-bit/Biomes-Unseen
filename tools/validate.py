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

    # Structures referencing unknown biomes, template pools or biome tags.
    #
    # A structure JSON names three kinds of thing, and only the first is a
    # registry id: its biome selection (usually a tag reference,
    # "#biomesunseen:has_structure/grove_shrine"), and its start_pool
    # ("structures/grove_shrine"). Both of the latter are nested resource paths,
    # so judging them against the biome list reports every structure as broken.
    # They are resolved against the files on disk instead, by trying each valid
    # location a path of that shape could occupy.
    if biome_ids:
        nested_roots = (
            os.path.join("worldgen", "template_pool"),
            os.path.join("tags", "worldgen", "biome"),
        )
        for ref in sorted(collect_namespaced_strings(parsed, "worldgen/structure")):
            if ref in biome_ids or ref in structure_ids:
                continue
            if "/" in ref:
                # ref is already namespace-stripped by collect_namespaced_strings,
                # so it is the resource path itself.
                if any(os.path.exists(os.path.join(RES, "data", MODID, root,
                                                   ref + ".json"))
                       for root in nested_roots):
                    continue
            report.error("closure",
                         f"structure references unknown biome, template pool or "
                         f"biome tag '{ref}'")


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
    """Assert the authored content tables still have the promised shape."""
    if B is None:
        report.error("content",
                     f"content tables failed to import: {CONTENT_IMPORT_ERROR}")
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


# --------------------------------------------------------------------------- #
# 6. Worldgen and GeckoLib closure
# --------------------------------------------------------------------------- #

# Content tables are imported at module scope because several checks need them.
# A table that fails to import leaves these as None, and the checks below skip
# rather than raise, so check_content_tables still reports the real cause.
try:
    import content.biomes as B          # noqa: E402
    import content.ores as O            # noqa: E402
    import content.mobs as M            # noqa: E402
    import content.bosses as BS         # noqa: E402
    import content.gear as G            # noqa: E402
    import content.structures as S      # noqa: E402
    CONTENT_IMPORT_ERROR: Optional[str] = None
except Exception as _exc:  # noqa: BLE001
    B = O = M = BS = G = S = None
    CONTENT_IMPORT_ERROR = str(_exc)


def _manifest() -> Dict[str, List[str]]:
    """The generated registry manifest, or an empty mapping if absent."""
    path = os.path.join(ASSETS, "registry_manifest.json")
    if not os.path.isfile(path):
        return {}
    try:
        return json.loads(open(path, encoding="utf-8").read())
    except Exception:  # noqa: BLE001
        return {}


MANIFEST = _manifest()
MANIFEST_BLOCKS = set(MANIFEST.get("blocks", []))
MANIFEST_ENTITIES = set(MANIFEST.get("entities", []))


def check_worldgen(report: Report) -> None:
    """
    Every biome, feature, structure and rig the content tables promise exists.

    These are the references Java cannot check at compile time: a biome is a
    ResourceKey whose JSON lives in the datapack, a feature is a string in a
    biome's feature slot, and a GeckoLib rig is a path built at runtime from the
    species id. A typo in any of them is a silent hole in the world -- a biome
    that never generates, a tree that never grows, a mob that renders as a
    missing model -- so they are all closed here.
    """
    if B is None or S is None:
        report.error("worldgen",
                     f"content tables unavailable, worldgen not checked: {CONTENT_IMPORT_ERROR}")
        return
    data = os.path.join(RES, "data")
    assets = ASSETS

    def data_file(namespace: str, *parts: str) -> str:
        return os.path.join(data, namespace, *parts)

    def asset_file(*parts: str) -> str:
        return os.path.join(assets, *parts)

    def has_data(namespace: str, folder: str, name: str) -> bool:
        # Only the final segment is a file; the folder must stay intact or every
        # lookup fails and the check reports a thousand phantom missing biomes.
        return os.path.exists(os.path.join(data, namespace, folder, name + ".json"))

    def split_ref(ref: str):
        # An unqualified path is one of ours: the content tables author template
        # pools as "boss/<id>" with no namespace. Defaulting those to minecraft
        # sends the lookup into vanilla's datapack folder and reports all 115
        # pools as missing.
        return ref.split(":", 1) if ":" in ref else (MODID, ref)

    # ---- biomes ----------------------------------------------------------
    for spec in B.ALL_BIOMES:
        if not has_data(MODID, "worldgen/biome", spec.id):
            report.error("worldgen", f"biome '{spec.id}' has no worldgen JSON")
        report.count("worldgen biomes", 1)

        path = data_file(MODID, "worldgen/biome", spec.id + ".json")
        if not os.path.exists(path):
            continue
        doc = json.load(open(path, "r", encoding="utf-8"))

        # Every feature slot must point at a placed feature that exists.
        for slot in doc.get("features", []):
            for ref in slot:
                namespace, feature = split_ref(ref)
                if namespace == "minecraft":
                    continue
                if not has_data(namespace, "worldgen/placed_feature", feature):
                    report.error("worldgen",
                                 f"biome '{spec.id}' references missing placed feature '{ref}'")
                report.count("worldgen feature refs", 1)

        # Spawn entries must name a registered entity.
        for category, entries in doc.get("spawners", {}).items():
            for entry in entries:
                namespace, entity = split_ref(entry.get("type", ""))
                if namespace == "minecraft":
                    continue
                if entity not in MANIFEST_ENTITIES:
                    report.error("worldgen",
                                 f"biome '{spec.id}' spawns unregistered entity '{entry.get('type')}'")

    # ---- placed -> configured features -----------------------------------
    placed_dir = data_file(MODID, "worldgen/placed_feature")
    if os.path.isdir(placed_dir):
        for name in sorted(os.listdir(placed_dir)):
            doc = json.load(open(os.path.join(placed_dir, name), "r", encoding="utf-8"))
            namespace, configured = split_ref(doc.get("feature", ""))
            if namespace == "minecraft":
                continue
            if not has_data(namespace, "worldgen/configured_feature", configured):
                report.error("worldgen",
                             f"placed feature '{name[:-5]}' references missing configured feature '{doc.get('feature')}'")

    # ---- configured features must reference real blocks -------------------
    configured_dir = data_file(MODID, "worldgen/configured_feature")
    if os.path.isdir(configured_dir):
        for name in sorted(os.listdir(configured_dir)):
            text = open(os.path.join(configured_dir, name), "r", encoding="utf-8").read()
            for ref in set(re.findall(r'"Name"\s*:\s*"([^"]+)"', text)):
                namespace, block = split_ref(ref)
                if namespace == "minecraft":
                    continue
                if block not in MANIFEST_BLOCKS:
                    report.error("worldgen",
                                 f"configured feature '{name[:-5]}' uses unregistered block '{ref}'")

    # ---- structures -------------------------------------------------------
    for spec in S.ALL_STRUCTURES:
        for kind, folder in (("structure", "worldgen/structure"),
                             ("structure_set", "worldgen/structure_set")):
            if not has_data(MODID, folder, spec.id):
                report.error("worldgen",
                             f"structure '{spec.id}' has no {kind} JSON")
        pool_ns, pool = split_ref(spec.start_jigsaw_pool)
        if not has_data(pool_ns, "worldgen/template_pool", pool):
            report.error("worldgen",
                         f"structure '{spec.id}' references missing template pool '{spec.start_jigsaw_pool}'")

        # Codec shape. Both of these were wrong for all 115 structures at once,
        # and both are invisible to every other check: the JSON parses, the ids
        # resolve, and the build passes, because the 1.20.1 structure codec only
        # complains when the game reads the datapack at world load.
        struct_path = data_file(MODID, "worldgen/structure", spec.id + ".json")
        if os.path.exists(struct_path):
            doc = json.load(open(struct_path, "r", encoding="utf-8"))

            # `biomes` is mandatory. Without it the structure is rejected by the
            # codec, and even if it loaded it would have nowhere to generate.
            biomes_ref = doc.get("biomes")
            if not biomes_ref:
                report.error("worldgen",
                             f"structure '{spec.id}' has no 'biomes' field, so the "
                             f"1.20.1 codec rejects it")
            elif str(biomes_ref).startswith("#"):
                tag_ns, _, tag_path = str(biomes_ref)[1:].partition(":")
                tag_file = os.path.join(data, tag_ns, "tags", "worldgen", "biome",
                                        tag_path + ".json")
                if not os.path.exists(tag_file):
                    report.error("worldgen",
                                 f"structure '{spec.id}' selects biomes via "
                                 f"'{biomes_ref}', which does not exist")
                else:
                    tag_doc = json.load(open(tag_file, "r", encoding="utf-8"))
                    if not tag_doc.get("values"):
                        report.error("worldgen",
                                     f"structure '{spec.id}' selects biomes via "
                                     f"'{biomes_ref}', which is empty")
                    report.count("structure biome tags resolved", 1)

            # `start_height` is a HeightProvider object, never a bare int. The
            # content tables author an integer for every structure, so emitting it
            # raw produced "start_height": 64 and the codec rejected the file.
            height = doc.get("start_height")
            if not isinstance(height, dict):
                report.error("worldgen",
                             f"structure '{spec.id}' has start_height={height!r}; "
                             f"1.20.1 requires a height provider object")
            report.count("worldgen structures", 1)

    # ---- template pools must point at a real structure template -----------
    pool_dir = data_file(MODID, "worldgen/template_pool")
    if os.path.isdir(pool_dir):
        for root, _dirs, files in os.walk(pool_dir):
            for name in sorted(files):
                doc = json.load(open(os.path.join(root, name), "r", encoding="utf-8"))
                for element in doc.get("elements", []):
                    location = element.get("element", {}).get("location")
                    if not location:
                        continue
                    namespace, template = split_ref(location)
                    nbt = os.path.join(data, namespace, "structures", template + ".nbt")
                    if not os.path.exists(nbt):
                        report.error("worldgen",
                                     f"template pool '{name[:-5]}' references missing structure template '{location}'")
                    report.count("worldgen pool elements", 1)

    # ---- dimensions -------------------------------------------------------
    for dimension in ("hollow_deep", "aetherfall", "void_between"):
        for folder in ("dimension_type", "dimension", "worldgen/noise_settings"):
            if not has_data(MODID, folder, dimension):
                report.error("worldgen",
                             f"dimension '{dimension}' has no {folder.rsplit('/', 1)[-1]} JSON")
        report.count("worldgen dimensions", 1)


def check_geckolib(report: Report) -> None:
    """
    Every GeckoLib rig and animation clip the Java model classes resolve exists.

    BUCreatureModel builds geo/entity/<family>.geo.json and
    textures/entity/<id>.png from the species data, and BUBossModel builds
    geo/entity/boss/<id>.geo.json. BUBoss additionally starts a clip named by
    each phase's entry_animation, and GeckoLib throws when a controller starts a
    clip the animation file does not define -- so a phase naming an animation
    that was never authored would break the fight at runtime, not at build time.
    """
    if M is None or BS is None:
        report.error("geckolib",
                     f"content tables unavailable, rigs not checked: {CONTENT_IMPORT_ERROR}")
        return
    families = set()
    for mob in M.ALL_MOBS:
        families.add(mob.family)
        geo = os.path.join(ASSETS, "geo", "entity", mob.family + ".geo.json")
        anim = os.path.join(ASSETS, "animations", "entity", mob.family + ".animation.json")
        if not os.path.exists(geo):
            report.error("geckolib", f"mob '{mob.id}' family '{mob.family}' has no geo.json")
        if not os.path.exists(anim):
            report.error("geckolib", f"mob '{mob.id}' family '{mob.family}' has no animation.json")

    # Creature clips: every animation a species declares must exist in its rig.
    for family in sorted(families):
        path = os.path.join(ASSETS, "animations", "entity", family + ".animation.json")
        if not os.path.exists(path):
            continue
        clips = set(json.load(open(path, "r", encoding="utf-8")).get("animations", {}))
        report.count("geckolib family rigs", 1)
        for mob in M.ALL_MOBS:
            if mob.family != family:
                continue
            for animation in mob.animations:
                if animation not in clips:
                    report.error("geckolib",
                                 f"mob '{mob.id}' declares clip '{animation}' missing from {family}.animation.json")

    # Boss clips: base set plus every authored phase entry animation.
    for boss in BS.ALL_BOSSES:
        geo = os.path.join(ASSETS, "geo", "entity", "boss", boss.id + ".geo.json")
        path = os.path.join(ASSETS, "animations", "entity", "boss", boss.id + ".animation.json")
        if not os.path.exists(geo):
            report.error("geckolib", f"boss '{boss.id}' has no geo.json")
        if not os.path.exists(path):
            report.error("geckolib", f"boss '{boss.id}' has no animation.json")
            continue
        clips = set(json.load(open(path, "r", encoding="utf-8")).get("animations", {}))
        report.count("geckolib boss rigs", 1)
        needed = set(BUEntities_BOSS_ANIMATIONS)
        for phase in boss.phases:
            if phase.entry_animation:
                needed.add(phase.entry_animation)
            needed.add(f"animation.phase.{phase.index}")
        for animation in sorted(needed):
            if animation not in clips:
                report.error("geckolib",
                             f"boss '{boss.id}' needs clip '{animation}' which {boss.id}.animation.json does not define")


# Must match BUEntities.BOSS_ANIMATIONS: the clips every boss rig is required to
# define regardless of what its phases name.
BUEntities_BOSS_ANIMATIONS = {
    "animation.idle", "animation.walk", "animation.attack",
    "animation.hurt", "animation.death", "animation.spawn",
    "animation.phase.1", "animation.phase.2", "animation.phase.3",
    "animation.phase.4",
}



def check_structure_templates(report: Report) -> None:
    """
    Decode every structure template and verify it is well formed.

    Templates are the mod's only binary asset, so nothing else in this validator
    can see inside them. A template that is truncated, mis-typed, or written for
    the wrong Minecraft data version places nothing in game and logs only a
    warning at world load -- which reads as "the structure never spawned" rather
    than as a bug. Checking them here makes that failure a build failure.
    """
    try:
        from nbt_codec import read_gzip
    except Exception as exc:  # noqa: BLE001
        report.error("nbt", f"nbt_codec unavailable: {exc}")
        return

    root = os.path.join(RES, "data")
    if not os.path.isdir(root):
        return

    manifest = MANIFEST
    block_ids = set(manifest.get("blocks", []))
    checked = 0
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            if not name.endswith(".nbt"):
                continue
            path = os.path.join(dirpath, name)
            relative = os.path.relpath(path, RES)
            try:
                _root_name, doc = read_gzip(path)
            except Exception as exc:  # noqa: BLE001
                report.error("nbt", f"{relative}: undecodable ({exc})")
                continue

            for key in ("size", "palette", "blocks", "DataVersion"):
                if key not in doc:
                    report.error("nbt", f"{relative}: missing '{key}' tag")
                    break
            else:
                # 1.20.1. A template written for another version is upgraded or
                # rejected on load, so pinning it here catches a stale constant.
                if doc["DataVersion"] != 3465:
                    report.error("nbt",
                                 f"{relative}: DataVersion {doc['DataVersion']} is not 1.20.1 (3465)")

                size = doc["size"]
                if len(size) != 3 or any(v <= 0 for v in size):
                    report.error("nbt", f"{relative}: invalid size {size}")
                else:
                    palette = doc["palette"]
                    for entry in palette:
                        block = entry.get("Name", "")
                        namespace, _, block_path = block.partition(":")
                        if namespace == MODID and block_ids and block_path not in block_ids:
                            report.error("nbt",
                                         f"{relative}: palette names unregistered block '{block}'")
                    for block in doc["blocks"]:
                        position = block.get("pos", [])
                        if len(position) != 3 or not all(
                                0 <= position[axis] < size[axis] for axis in range(3)):
                            report.error("nbt",
                                         f"{relative}: block at {position} is outside size {size}")
                            break
                        if not 0 <= block.get("state", -1) < len(palette):
                            report.error("nbt",
                                         f"{relative}: block state index {block.get('state')} "
                                         f"outside palette of {len(palette)}")
                            break
                    checked += 1

    report.count("structure templates decoded", checked)



def _bu_table(text: str, name: str) -> Optional[str]:
    """
    The body of a generated BUContent table, however it is indented.

    Written as a scanner rather than a single regex: these tables are emitted in
    two shapes (String[] on one line-wrapped block, String[][] and Object[][] as
    one row per line) and a pattern tuned for one silently matches nothing for
    the other, which reads as "no duplicates found" when nothing was checked.
    """
    marker = f"{name} = {{"
    start = text.find(marker)
    if start < 0:
        return None
    body_start = start + len(marker)
    depth = 1
    index = body_start
    while index < len(text) and depth:
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        index += 1
    return text[body_start:index - 1]


BLOCK_TABLES = ("BLOCKS_CUBE", "BLOCKS_GRASS", "BLOCKS_LOG", "BLOCKS_ORE",
                "BLOCKS_MINERAL", "BLOCKS_FLORA", "BLOCKS_PORTAL",
                "BLOCKS_LANTERN", "BLOCKS_ALTAR", "BLOCKS_FLUID")
ITEM_TABLES = ("ITEMS_MATERIALS", "ITEMS_TOOLS", "ITEMS_ARTEFACTS",
               "ITEMS_LORE_BOOKS")


# Registry `type` vocabularies, verified against the vanilla and Forge 1.20.1
# codecs. Each entry lists every `type` value that may appear anywhere inside that
# category of file -- including nested config objects, since a configured_feature
# carries types for its feature, its foliage placer, its state providers and its
# block predicates all in one document.
#
# This exists because a generated biome modifier declared "forge:none", which is
# not a registered Forge biome modifier type at all (the real ones are
# add_features, remove_features, add_spawns and remove_spawns). All four files
# failed to deserialize at world load. Nothing else caught it: the JSON parsed,
# every id resolved, and the build was green, because a datapack codec error is
# only reported by the game at runtime.
VALID_TYPES = {
    "configured_feature": {
        "minecraft:tree", "minecraft:ore", "minecraft:random_patch",
        "minecraft:simple_block",
        "minecraft:straight_trunk_placer", "minecraft:blob_foliage_placer",
        "minecraft:two_layers_feature_size",
        "minecraft:simple_state_provider", "minecraft:weighted_state_provider",
        "minecraft:block_predicate_filter", "minecraft:would_survive",
        "minecraft:matching_blocks",
    },
    "placed_feature": {
        "minecraft:count", "minecraft:count_on_every_surface",
        "minecraft:in_square", "minecraft:heightmap", "minecraft:height_range",
        "minecraft:surface_water_depth_filter", "minecraft:biome",
        "minecraft:block_predicate_filter", "minecraft:would_survive",
        "minecraft:matching_blocks", "minecraft:trapezoid", "minecraft:uniform",
        "minecraft:constant",
    },
    "structure": {"minecraft:jigsaw"},
    "template_pool": {
        "minecraft:single_pool_element", "minecraft:list_pool_element",
        "minecraft:feature_pool_element", "minecraft:empty_pool_element",
        "minecraft:legacy_single_pool_element",
        # Processor references appear in the same documents.
        "minecraft:empty", "minecraft:protected_blocks",
        "minecraft:block_ignore", "minecraft:block_rot", "minecraft:gravity",
        "minecraft:jigsaw_replacement", "minecraft:lava_submerged_block",
        "minecraft:nop", "minecraft:rule",
    },
    "noise_settings": {
        "minecraft:constant", "minecraft:noise", "minecraft:shifted_noise",
        "minecraft:add", "minecraft:mul", "minecraft:min", "minecraft:max",
        "minecraft:abs", "minecraft:squeeze", "minecraft:interpolated",
        "minecraft:blend_density", "minecraft:y_clamped_gradient",
        "minecraft:cave_surface", "minecraft:sequence", "minecraft:condition",
        "minecraft:biome", "minecraft:stone_depth", "minecraft:block",
        "minecraft:not", "minecraft:hole", "minecraft:water",
        "minecraft:above_preliminary_surface", "minecraft:vertical_gradient",
        "minecraft:spline", "minecraft:range_choice", "minecraft:flat_cache",
        "minecraft:cache_2d", "minecraft:cache_all_in_cell",
        "minecraft:old_blended_noise", "minecraft:end_islands",
        "minecraft:beard",
    },
    "biome_modifier": {
        "forge:add_features", "forge:remove_features",
        "forge:add_spawns", "forge:remove_spawns",
    },
    "loot_tables": {
        "minecraft:block", "minecraft:chest", "minecraft:entity",
        "minecraft:empty", "minecraft:gift", "minecraft:advancement",
        "minecraft:barter", "minecraft:selector", "minecraft:fishing",
        "minecraft:generic",
        "minecraft:item", "minecraft:loot_table", "minecraft:alternatives",
        "minecraft:group", "minecraft:sequence", "minecraft:dynamic",
        "minecraft:tag", "minecraft:uniform", "minecraft:constant",
        "minecraft:binomial", "minecraft:score",
    },
    "recipes": {"minecraft:crafting_shaped", "minecraft:crafting_shapeless",
                "minecraft:smelting", "minecraft:blasting",
                "minecraft:smoking", "minecraft:campfire_cooking",
                "minecraft:stonecutting", "minecraft:smithing_transform",
                "minecraft:smithing_trim"},
}


def check_datapack_types(report: Report) -> None:
    """
    Every registry `type` string must be one the game can actually deserialize.

    A bad type is invisible to every other check here: the JSON parses, the ids
    resolve, the build passes. It fails only when the game reads the datapack, at
    world load, as a codec error naming the file. Checking the vocabulary offline
    turns that into a build failure.
    """
    root = os.path.join(RES, "data")
    if not os.path.isdir(root):
        return

    def category(relative: str) -> Optional[str]:
        if "worldgen/configured_feature" in relative:
            return "configured_feature"
        if "worldgen/placed_feature" in relative:
            return "placed_feature"
        if "worldgen/structure/" in relative:
            return "structure"
        if "worldgen/template_pool" in relative:
            return "template_pool"
        if "worldgen/noise_settings" in relative:
            return "noise_settings"
        if "biome_modifier" in relative:
            return "biome_modifier"
        if "loot_tables" in relative:
            return "loot_tables"
        if "recipes" in relative:
            return "recipes"
        return None

    # Keys that carry a registry type id. Template pool elements use
    # "element_type" rather than "type", and structure/pool processors use
    # "processor_type", so all three are collected -- looking only at "type"
    # reported zero values for the whole template_pool category, which passed
    # because nothing was examined.
    type_keys = ("type", "element_type", "processor_type")

    def collect_types(node, out: Set[str]) -> None:
        if isinstance(node, dict):
            for key in type_keys:
                value = node.get(key)
                if isinstance(value, str):
                    out.add(value)
            for child in node.values():
                collect_types(child, out)
        elif isinstance(node, list):
            for child in node:
                collect_types(child, out)

    seen: Dict[str, Set[str]] = {}
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            if not name.endswith(".json"):
                continue
            path = os.path.join(dirpath, name)
            relative = os.path.relpath(path, RES)
            kind = category(relative)
            if kind is None:
                continue
            try:
                doc = json.load(open(path, "r", encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue  # check_json already reported the parse failure
            found: Set[str] = set()
            collect_types(doc, found)
            allowed = VALID_TYPES[kind]
            for value in sorted(found - allowed):
                report.error("datapack",
                             f"{relative}: unknown '{kind}' type '{value}'")
            seen.setdefault(kind, set()).update(found)
            report.count(f"datapack {kind} files", 1)

    for kind, values in sorted(seen.items()):
        report.count(f"datapack {kind} types", len(values))


def check_registration_uniqueness(report: Report) -> None:
    """
    No id may be registered twice in the same registry.

    Forge throws RegistryException on a duplicate registration, and it throws at
    mod construction -- before any world exists -- so the failure is a crash on
    launch that compiles perfectly cleanly. Nothing else in this validator can
    see it, because each registration site is individually valid; only the union
    of all of them is wrong.

    BUItems registers four disjoint-looking sets into the one item registry: a
    BlockItem per solid block, then the materials, tools, artefacts, lore books,
    armour pieces and spawn eggs from the content tables. Those are authored in
    different places, so an id landing in two of them is easy to do and
    impossible to spot by reading either.

    Blocks and items may legitimately share a path -- a BlockItem is registered
    under its block's own id, in a different registry -- so only collisions
    inside one registry are errors.
    """
    path = os.path.join(JAVA, "com", "biomesunseen", "init", "BUContent.java")
    if not os.path.isfile(path):
        report.error("registry", "BUContent.java is missing")
        return
    text = open(path, encoding="utf-8").read()

    def ids(table: str) -> List[str]:
        body = _bu_table(text, table)
        if body is None:
            report.error("registry", f"BUContent.{table} not found")
            return []
        return re.findall(r'"([a-z0-9_/.-]+)"', body)

    # ---- blocks ----------------------------------------------------------
    blocks: List[str] = []
    for table in BLOCK_TABLES:
        blocks += ids(table)
    for duplicate in sorted({b for b in blocks if blocks.count(b) > 1}):
        report.error("registry", f"block '{duplicate}' is registered twice")
    report.count("block registrations unique", len(blocks))

    # ---- items -----------------------------------------------------------
    fluids = set(ids("BLOCKS_FLUID"))
    portals = {b for b in blocks if b.endswith("_portal")}
    # Mirrors BUItems.registerBlockItems: fluids and portals have no item form.
    block_items = [b for b in blocks if b not in fluids and b not in portals]

    items: List[str] = []
    sources: Dict[str, List[str]] = {"block_item": block_items}
    for table in ITEM_TABLES:
        sources[table] = ids(table)

    armour_body = _bu_table(text, "ARMOUR_ITEMS")
    sources["ARMOUR_ITEMS"] = re.findall(
        r'\{\s*"([a-z0-9_]+)"\s*,', armour_body) if armour_body else []

    egg_body = _bu_table(text, "SPAWN_EGGS")
    sources["SPAWN_EGGS"] = re.findall(
        r'\{\s*"([a-z0-9_]+_spawn_egg)"\s*,', egg_body) if egg_body else []

    for name, values in sources.items():
        if not values and name != "block_item":
            report.error("registry", f"no item ids parsed from {name}")
        items += values

    seen: Dict[str, List[str]] = {}
    for name, values in sources.items():
        for value in values:
            seen.setdefault(value, []).append(name)
    for item_id, origin in sorted(seen.items()):
        if len(origin) > 1:
            report.error("registry",
                         f"item '{item_id}' is registered by {sorted(set(origin))}")
    report.count("item registrations unique", len(items))

    # ---- entities --------------------------------------------------------
    mobs = re.findall(r'new MobData\(\s*"([a-z0-9_]+)"', text)
    bosses = re.findall(r'new BossData\(\s*"([a-z0-9_]+)"', text)
    entities = mobs + bosses
    for duplicate in sorted({e for e in entities if entities.count(e) > 1}):
        report.error("registry", f"entity '{duplicate}' is registered twice")
    for overlap in sorted(set(mobs) & set(bosses)):
        report.error("registry",
                     f"'{overlap}' is registered as both a creature and a boss")
    report.count("entity registrations unique", len(entities))


def check_audio(report: Report) -> None:
    """
    Every sound id either ships audio or is referenced by nothing.

    A SoundEvent with no sounds.json definition is harmless while it stays
    unplayed, but the moment a biome or a boss starts it the client logs "Unable
    to play unknown soundEvent" -- and biome music retries every 12-24 seconds
    per player, in every biome that authored a track. So the rule is not "all
    audio must exist", it is "nothing may reference audio that does not".

    The generators enforce that by emitting music and ambience only for sounds
    with a real .ogg, and this checks the result: no biome JSON may name a sound
    that has no audio, and sounds.json may only declare files that exist. The
    remaining gap -- authored tracks with no audio yet -- is reported as a count
    so it is visible rather than silent, since it is a content hole and not a
    defect.
    """
    assets = os.path.join(RES, "assets", MODID)
    authored = set()
    for spec in B.ALL_BIOMES:
        for field in ("music", "ambient_sound"):
            value = getattr(spec, field, None)
            if value:
                authored.add(value.split(":")[-1])
    for spec in BS.ALL_BOSSES:
        if spec.music:
            authored.add(spec.music.split(":")[-1])

    shipped = set()
    for sound_id in sorted(authored):
        if os.path.exists(os.path.join(assets, "sounds",
                                       sound_id.replace(".", os.sep) + ".ogg")):
            shipped.add(sound_id)

    missing = authored - shipped
    report.count("authored sound ids", len(authored))
    report.count("sound ids with audio", len(shipped))
    if missing:
        report.note("audio",
                    f"{len(missing)} authored sound(s) have no .ogg and are therefore "
                    f"referenced by nothing: e.g. {sorted(missing)[:3]}. Biome music, "
                    f"ambience and boss themes stay silent until the tracks are added; "
                    f"re-running the generators switches them on with no code change.")

    # Nothing may reference audio that does not exist.
    biome_dir = os.path.join(RES, "data", MODID, "worldgen", "biome")
    if os.path.isdir(biome_dir):
        for name in sorted(os.listdir(biome_dir)):
            doc = json.load(open(os.path.join(biome_dir, name), "r",
                                 encoding="utf-8"))
            effects = doc.get("effects", {})
            refs = []
            if effects.get("ambient_sound"):
                refs.append(effects["ambient_sound"])
            music = effects.get("music")
            if isinstance(music, dict) and music.get("sound"):
                refs.append(music["sound"])
            for ref in refs:
                bare = ref.split(":")[-1]
                if bare not in shipped:
                    report.error("audio",
                                 f"biome '{name[:-5]}' references sound '{ref}' which has no audio")
                report.count("biome audio refs", 1)

    # sounds.json, if present, must only declare files that exist.
    sounds_json = os.path.join(assets, "sounds.json")
    if os.path.isfile(sounds_json):
        doc = json.load(open(sounds_json, "r", encoding="utf-8"))
        for sound_id, definition in doc.items():
            for entry in definition.get("sounds", []):
                path = entry.get("name") if isinstance(entry, dict) else entry
                if not path:
                    continue
                relative = str(path).split(":")[-1]
                if not os.path.exists(os.path.join(assets, "sounds",
                                                   relative + ".ogg")):
                    report.error("audio",
                                 f"sounds.json declares '{sound_id}' -> '{path}' but no .ogg exists")
                report.count("sounds.json definitions", 1)


def check_biome_placement(report: Report) -> None:
    """
    Every authored biome must be reachable by some biome source.

    A biome can be fully authored -- climate, colours, surface rules, features,
    spawns, structures, loot -- and still never appear in a world, because being
    defined is not the same as being placed. Nothing else in this validator can
    see that distinction, so it is checked here.

    Dimension biomes are placed by their own dimension's multi_noise source,
    which is pure data and is verified directly against the emitted JSON.

    Overworld biomes cannot be placed by data alone: 1.20.1 samples a fixed
    climate parameter list built inside
    MultiNoiseBiomeSourceParameterList.Preset.OVERWORLD, and no datapack can
    append to it. They are placed through TerraBlender instead, which is the same
    hook Biomes O' Plenty and Oh The Biomes You've Gone use, so our biomes blend
    with other biome mods rather than competing with them. That makes the binding
    a three-part contract, and all three parts are checked: the dependency must
    be declared, the region must exist, and every Overworld biome must appear in
    both generated tables the region and the surface rules read.
    """
    placed = set()
    dimension_dir = os.path.join(RES, "data", MODID, "dimension")
    if os.path.isdir(dimension_dir):
        for name in sorted(os.listdir(dimension_dir)):
            doc = json.load(open(os.path.join(dimension_dir, name), "r",
                                 encoding="utf-8"))
            source = doc.get("generator", {}).get("biome_source", {})
            for entry in source.get("biomes", []):
                placed.add(entry.get("biome", "").split(":")[-1])

    overworld = [b for b in B.ALL_BIOMES if b.dimension == "overworld"]
    dimension = [b for b in B.ALL_BIOMES if b.dimension != "overworld"]

    for spec in dimension:
        if spec.id not in placed:
            report.error("placement",
                         f"dimension biome '{spec.id}' ({spec.dimension}) is placed by no biome source")
        report.count("biomes placed by a dimension source", 1)

    # ---- the TerraBlender contract ---------------------------------------
    mods_toml = os.path.join(RES, "META-INF", "mods.toml")
    declared = False
    if os.path.isfile(mods_toml):
        declared = 'modId = "terrablender"' in open(mods_toml, encoding="utf-8").read()
    if not declared:
        report.error("placement",
                     "mods.toml does not declare a terrablender dependency, so the "
                     "Overworld region cannot load")

    region = os.path.join(JAVA, "com", "biomesunseen", "world", "BUOverworldRegion.java")
    if not os.path.isfile(region):
        report.error("placement", "BUOverworldRegion.java is missing")

    # Both generated tables are consumed by Java, so verify the ids rather than
    # trusting the generator: a biome absent from either is registered but never
    # placed, or placed but wearing the vanilla grass crust.
    content = os.path.join(JAVA, "com", "biomesunseen", "init", "BUContent.java")
    parameters = set()
    surfaces = set()
    if os.path.isfile(content):
        text = open(content, encoding="utf-8").read()
        parameters = _table_ids(text, "SEEDED_OVERWORLD_PARAMETERS")
        surfaces = _table_ids(text, "OVERWORLD_SURFACES")
    else:
        report.error("placement", "BUContent.java is missing")

    for spec in overworld:
        if spec.id not in parameters:
            report.error("placement",
                         f"Overworld biome '{spec.id}' has no climate parameter row, "
                         f"so the TerraBlender region cannot place it")
        if spec.id not in surfaces:
            report.error("placement",
                         f"Overworld biome '{spec.id}' has no surface material row, "
                         f"so it would grow the vanilla grass crust")
        report.count("overworld biomes bound to the TerraBlender region", 1)


def _table_ids(text: str, table: str) -> set:
    """The leading string id of every row in a generated Object[][] table."""
    marker = f"{table} = {{"
    start = text.find(marker)
    if start < 0:
        return set()
    end = text.find("\n    };", start)
    body = text[start:end if end > 0 else len(text)]
    return set(re.findall(r'\{\s*"([a-z0-9_]+)"', body))


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
    check_worldgen(report)
    check_geckolib(report)
    check_structure_templates(report)
    check_biome_placement(report)
    check_audio(report)
    check_registration_uniqueness(report)
    check_datapack_types(report)

    return report.render()


if __name__ == "__main__":
    raise SystemExit(main())
