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

    # ---- bones and animation channels must pair up -----------------------
    # GeckoLib ignores an animation channel naming a bone the geo does not
    # define, so the failure is silent in both directions:
    #
    #   an orphan channel drives nothing -- the part was keyframed and stays
    #   perfectly still, which reads as a broken rig rather than a missing one
    #   a geo bone no clip touches is frozen in every animation, including idle
    #
    # Neither is a load error, and both survived a green build: all five bosses
    # keyframed extra_3 and extra_4 while their rigs emitted only extra_1 and
    # extra_2, the fungal rig called its head bone "cap" while every creature
    # clip drove "head", and the biped's right arm was never keyframed at all.
    def bone_names(geo_path: str) -> set:
        doc = json.load(open(geo_path, "r", encoding="utf-8"))
        entry = doc.get("minecraft:geometry") or [{}]
        return {b.get("name") for b in entry[0].get("bones", [])}

    def animated_bones(anim_path: str) -> set:
        doc = json.load(open(anim_path, "r", encoding="utf-8"))
        used = set()
        for body in (doc.get("animations") or {}).values():
            used |= set((body.get("bones") or {}).keys())
        return used

    pairs = []
    for family in sorted(families):
        pairs.append((family,
                      os.path.join(ASSETS, "geo", "entity", family + ".geo.json"),
                      os.path.join(ASSETS, "animations", "entity", family + ".animation.json")))
    for boss in BS.ALL_BOSSES:
        pairs.append((boss.id,
                      os.path.join(ASSETS, "geo", "entity", "boss", boss.id + ".geo.json"),
                      os.path.join(ASSETS, "animations", "entity", "boss", boss.id + ".animation.json")))

    for name, geo_path, anim_path in pairs:
        if not (os.path.exists(geo_path) and os.path.exists(anim_path)):
            continue  # already reported above
        built = bone_names(geo_path)
        used = animated_bones(anim_path)
        report.count("geckolib rig bone pairings", 1)
        for orphan in sorted(used - built):
            report.error("geckolib",
                         f"rig '{name}' keyframes bone '{orphan}' that its geo does "
                         f"not define, so that track drives nothing")
        for frozen in sorted(built - used):
            report.error("geckolib",
                         f"rig '{name}' defines bone '{frozen}' that no clip "
                         f"keyframes, so that part never moves")


def check_pixelart_glyph_geometry(report: Report) -> None:
    """
    Every authored glyph map must match the band geometry that consumes it.

    boss_maps builds the 64x64 atlas out of six bands: _band8 composes the four
    8-row bands (body, body2, head, crown) and _band4 the two 16-row bands
    (limbs, extras), each from four regions that must be exactly 16 columns wide.

    Two helpers hide any deviation from that contract. _band4 and _band8 index
    range(16) and range(8), so surplus rows in a glyph are silently dropped
    rather than raising. _repair_row then ljusts any short row with transparent
    padding to reach the cell width. Together they let a mis-shaped glyph render
    as corrupted pixels with a green build and no warning: four glyphs were in
    that state, and three of them were visibly broken in game.

      _SC_HEAD_F  9 rows for an 8-row band, one row split into a lone "O", so the
                  crown's jaw rendered as a single outline pixel on a blank row
                  and its bottom outline was displaced out of the band entirely
      _WD_HEAD_F  jaw row 15 wide, leaving a transparent gap in the warden's jaw
      _UN_EXTRA_3 18 rows and ragged, two rows reduced to a lone "O"
      _WD_EXTRA_2 17 rows for a 16-row band

    Checking the authored maps directly, rather than the composed atlas, catches
    the defect where it is introduced and reports which glyph is wrong.
    """
    try:
        from pixelart import boss_maps as BM
    except Exception as exc:  # noqa: BLE001
        report.error("pixelart", f"boss_maps unavailable: {exc}")
        return

    band_rows = {"body": 8, "body2": 8, "head": 8, "crown": 8,
                 "limbs": 16, "extras": 16}
    regions = getattr(BM, "BOSSES", None) or {}
    if not regions:
        report.note("pixelart", "boss_maps.BOSSES is empty; glyph geometry not checked")
        return

    for boss_id in sorted(regions):
        table = regions[boss_id]
        for band, expected in band_rows.items():
            cells = table.get(band)
            if cells is None:
                report.error("pixelart",
                             f"boss '{boss_id}' atlas is missing its '{band}' band")
                continue
            if len(cells) != 4:
                report.error("pixelart",
                             f"boss '{boss_id}' band '{band}' has {len(cells)} regions, "
                             f"expected 4")
                continue
            report.count("pixelart glyph maps", 1)
            for index, glyph in enumerate(cells):
                rows = list(glyph)
                if len(rows) != expected:
                    report.error(
                        "pixelart",
                        f"boss '{boss_id}' {band}[{index}] is {len(rows)} rows but its "
                        f"band is {expected}; surplus rows are dropped silently and "
                        f"missing rows pad out as transparent")
                widths = {len(r) for r in rows}
                if widths != {16}:
                    report.error(
                        "pixelart",
                        f"boss '{boss_id}' {band}[{index}] has rows of width "
                        f"{sorted(widths)}, expected every row exactly 16 wide")


def check_geckolib_atlas_coverage(report: Report) -> None:
    """
    Every cube face of every rig must sample authored pixels of its own atlas.

    A cube whose uv rect falls outside texture_width/texture_height samples
    whatever the atlas happens to hold past its edge, and a cube whose rect lands
    inside a region nobody drew renders as a hole in the model. Neither is a load
    error, so both survive a green build and show up only as a creature with a
    missing face.

    This is the check that the boss extras needed: their animation channels had
    always driven extra_1..extra_4 while the geos emitted two bones, so two of the
    four authored atlas cells in the v48..63 band were never sampled by anything.
    Emitting the missing bones activated art that was already drawn -- this
    confirms that, per rig, and stops a future rig change from keyframing geometry
    over a blank band.

    Family rigs are shared by every mob in that family, so each is checked against
    all of them: a UV region authored for one species and left blank for another
    is exactly the per-species hole this is meant to catch.
    """
    if M is None or BS is None:
        report.note("geckolib", "content tables unavailable; atlas coverage not checked")
        return
    try:
        from png_codec import decode_png
    except Exception as exc:  # noqa: BLE001
        report.error("geckolib", f"png_codec unavailable: {exc}")
        return

    def uv_rects(geo_path: str):
        """(texture_width, texture_height, [(bone, face, u, v, w, h), ...])."""
        doc = json.load(open(geo_path, "r", encoding="utf-8"))
        entry = (doc.get("minecraft:geometry") or [{}])[0]
        desc = entry.get("description", {})
        tw = desc.get("texture_width") or 64
        th = desc.get("texture_height") or 64
        rects = []
        for b in entry.get("bones", []):
            for cube in b.get("cubes", []) or []:
                uv = cube.get("uv")
                faces = uv.items() if isinstance(uv, dict) else []
                for face, spec in faces:
                    if not isinstance(spec, dict):
                        continue
                    origin = spec.get("uv") or []
                    size = spec.get("uv_size") or []
                    if len(origin) < 2 or len(size) < 2:
                        continue
                    rects.append((b.get("name"), face,
                                  origin[0], origin[1], size[0], size[1]))
        return tw, th, rects

    def atlas_coverage(texture_path: str, rects):
        """Report out-of-bounds and blank rects against one decoded atlas."""
        try:
            data = open(texture_path, "rb").read()
        except OSError:
            return None, None
        w, h, px = decode_png(data)
        oob = []
        blank = []
        seen = set()
        for bone, face, u, v, uw, vh in rects:
            key = (u, v, uw, vh)
            if key in seen:
                continue
            seen.add(key)
            if u < 0 or v < 0 or u + uw > w or v + vh > h:
                oob.append((bone, face, u, v, uw, vh, w, h))
                continue
            opaque = 0
            for dy in range(int(vh)):
                row = px[int(v) + dy]
                for dx in range(int(uw)):
                    pixel = row[int(u) + dx]
                    if (pixel[3] if len(pixel) == 4 else 255) > 8:
                        opaque += 1
            if opaque == 0:
                blank.append((bone, face, u, v, uw, vh))
        return oob, blank

    # ---- boss rigs map 1:1 to their own atlas ----------------------------
    for boss in BS.ALL_BOSSES:
        geo = os.path.join(ASSETS, "geo", "entity", "boss", boss.id + ".geo.json")
        tex = os.path.join(ASSETS, "textures", "entity", "boss", boss.id + ".png")
        if not (os.path.exists(geo) and os.path.exists(tex)):
            continue
        tw, th, rects = uv_rects(geo)
        report.count("geckolib atlas faces", len(rects))
        oob, blank = atlas_coverage(tex, rects)
        if oob is None:
            report.error("geckolib", f"boss '{boss.id}' atlas is unreadable")
            continue
        for bone, face, u, v, uw, vh, w, h in oob:
            report.error("geckolib",
                         f"boss '{boss.id}' bone '{bone}' face '{face}' samples "
                         f"u{u}..{u+uw-1} v{v}..{v+vh-1} outside its {w}x{h} atlas")
        for bone, face, u, v, uw, vh in blank:
            report.error("geckolib",
                         f"boss '{boss.id}' bone '{bone}' face '{face}' samples "
                         f"u{u} v{v} {uw}x{vh}, which is blank in its atlas")
        report.count("geckolib boss atlas coverage", 1)

    # ---- family rigs are shared, so check every mob that uses one ---------
    by_family = {}
    for mob in M.ALL_MOBS:
        by_family.setdefault(mob.family, []).append(mob.id)
    for family in sorted(by_family):
        geo = os.path.join(ASSETS, "geo", "entity", family + ".geo.json")
        if not os.path.exists(geo):
            continue
        tw, th, rects = uv_rects(geo)
        report.count("geckolib atlas faces", len(rects))
        for mob_id in sorted(by_family[family]):
            tex = os.path.join(ASSETS, "textures", "entity", mob_id + ".png")
            oob, blank = atlas_coverage(tex, rects)
            if oob is None:
                report.error("geckolib",
                             f"mob '{mob_id}' has no readable atlas at "
                             f"textures/entity/{mob_id}.png")
                continue
            for bone, face, u, v, uw, vh, w, h in oob:
                report.error("geckolib",
                             f"mob '{mob_id}' ({family}) bone '{bone}' face "
                             f"'{face}' samples u{u}..{u+uw-1} v{v}..{v+vh-1} "
                             f"outside its {w}x{h} atlas")
            for bone, face, u, v, uw, vh in blank:
                report.error("geckolib",
                             f"mob '{mob_id}' ({family}) bone '{bone}' face "
                             f"'{face}' samples u{u} v{v} {uw}x{vh}, which is "
                             f"blank in its atlas")
            report.count("geckolib mob atlas coverage", 1)


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


TRANSlatable_RE = re.compile(
    r'Component\.translatable\(\s*"([a-z0-9_.]+)"')
TRANSlatable_DYN = re.compile(
    r'Component\.translatable\(\s*"[a-z0-9_.]*"\s*\+')


def check_model_and_tag_closure(report: Report) -> None:
    """
    Model parents, blockstate variants, tag members and recipe ids must resolve.

    These are the last references in the mod that nothing else checks. Each is a
    runtime-only failure with a green build:

      - a blockstate variant naming a model that does not exist renders the block
        as a missing-model cube, in world and in every inventory
      - a model whose `parent` does not resolve loses every texture and transform
        it inherits, and renders as a bare untextured box
      - a block or item tag naming an unregistered id makes Forge log an error on
        every load and silently drops the whole tag entry
      - a recipe naming an unregistered ingredient or result fails to load, so the
        crafting grid shows nothing and the ore's authored use disappears

    The existing registry closure check confirms a block HAS a blockstate and an
    item HAS a model. This confirms the contents of those files point at things
    that exist, which is the other half of the same question.
    """
    manifest = MANIFEST
    block_ids = set(manifest.get("blocks", []))
    item_ids = set(manifest.get("items", []))
    block_item_ids = set(manifest.get("block_items", []))
    known_items = item_ids | block_item_ids

    def model_exists(ref: str) -> bool:
        """Whether a model reference resolves to a file, or is vanilla's."""
        namespace, _, path = ref.partition(":")
        namespace = namespace or MODID
        if namespace == "minecraft":
            return True
        return os.path.exists(os.path.join(RES, "assets", namespace, "models",
                                          path + ".json"))

    # ---- blockstate variants -> models ------------------------------------
    states_dir = os.path.join(ASSETS, "blockstates")
    if os.path.isdir(states_dir):
        for name in sorted(os.listdir(states_dir)):
            if not name.endswith(".json"):
                continue
            doc = json.load(open(os.path.join(states_dir, name), "r",
                                 encoding="utf-8"))
            applies = []
            variants = doc.get("variants", {})
            multipart = doc.get("multipart", [])
            # An empty blockstate resolves to no model at all, and the model
            # loader reports "Exception loading blockstate variant" for it at
            # resource load. All four fluids were emitted this way, on the
            # mistaken assumption that vanilla does the same -- water.json
            # declares its default variant like any other block.
            if not variants and not multipart:
                report.error("model",
                             f"blockstate '{name[:-5]}' declares no variants and no "
                             f"multipart, so it resolves to no model")
            for value in variants.values():
                applies += value if isinstance(value, list) else [value]
            for part in multipart:
                apply = part.get("apply")
                if isinstance(apply, list):
                    applies += apply
                elif isinstance(apply, dict):
                    applies.append(apply)
            for entry in applies:
                if not isinstance(entry, dict):
                    continue
                model = entry.get("model")
                if not model:
                    continue
                if not model_exists(model):
                    report.error("model",
                                 f"blockstate '{name[:-5]}' references missing model '{model}'")
                report.count("blockstate model refs", 1)

    # ---- model parent chain ------------------------------------------------
    models_dir = os.path.join(ASSETS, "models")
    if os.path.isdir(models_dir):
        for dirpath, _dirs, files in os.walk(models_dir):
            for name in sorted(files):
                if not name.endswith(".json"):
                    continue
                path = os.path.join(dirpath, name)
                doc = json.load(open(path, "r", encoding="utf-8"))

                # Item art has to be ours. A model whose texture layer points
                # into another namespace is a vanilla sprite standing in for art
                # that was never authored -- the flat recolor the art rules
                # forbid. It is invisible to every other check precisely because
                # the reference resolves: the item renders, just as something we
                # did not draw. The fluid item model did exactly this before it
                # was removed, binding layer0 to minecraft:item/water_bucket.
                #
                # Only item models are held to this. Vanilla PARENTS are correct
                # and expected (item/generated, item/handheld), and block models
                # bind sprites through #texture placeholders rather than literal
                # layers.
                if (os.sep + "item" + os.sep) in (path + os.sep):
                    for layer, ref in (doc.get("textures") or {}).items():
                        if not isinstance(ref, str) or ref.startswith("#"):
                            continue
                        namespace = ref.partition(":")[0]
                        if namespace and namespace != MODID:
                            report.error(
                                "model",
                                f"{rel(path)} binds '{layer}' to foreign texture "
                                f"'{ref}': item art must be authored, a vanilla "
                                f"sprite is a flat-recolor placeholder")
                        report.count("item texture layers", 1)

                parent = doc.get("parent")
                if not parent:
                    continue
                if not model_exists(parent):
                    report.error("model",
                                 f"{rel(path)} has unresolvable parent '{parent}'")
                report.count("model parents", 1)

    # ---- tag membership ----------------------------------------------------
    for dirpath, _dirs, files in os.walk(os.path.join(RES, "data")):
        if os.sep + "tags" + os.sep not in dirpath + os.sep:
            continue
        normalised = dirpath.replace(os.sep, "/")
        if "/tags/blocks" in normalised:
            known, label = block_ids, "block"
        elif "/tags/items" in normalised:
            known, label = known_items, "item"
        else:
            # Biome, entity-type and function tags resolve against worldgen and
            # registry files rather than the block/item manifests, and are covered
            # by the worldgen and registry checks.
            continue
        if not known:
            continue
        for name in sorted(files):
            if not name.endswith(".json"):
                continue
            path = os.path.join(dirpath, name)
            doc = json.load(open(path, "r", encoding="utf-8"))
            for value in doc.get("values", []):
                # Nested tag references and optional entries are not id lookups.
                if isinstance(value, dict) or str(value).startswith("#"):
                    continue
                namespace, _, tag_path = str(value).partition(":")
                if namespace != MODID:
                    continue
                if tag_path not in known:
                    report.error("tags",
                                 f"{rel(path)} names unregistered {label} '{value}'")
                report.count("tag value refs", 1)

    # ---- recipes -----------------------------------------------------------
    recipes_dir = os.path.join(RES, "data", MODID, "recipes")
    if os.path.isdir(recipes_dir):
        pattern = re.compile(r'"' + MODID + r':([a-z0-9_/-]+)"')
        for dirpath, _dirs, files in os.walk(recipes_dir):
            for name in sorted(files):
                if not name.endswith(".json"):
                    continue
                path = os.path.join(dirpath, name)
                text = open(path, "r", encoding="utf-8").read()
                for reference in set(pattern.findall(text)):
                    if reference not in known_items:
                        report.error("recipes",
                                     f"{rel(path)} references unregistered item "
                                     f"'{MODID}:{reference}'")
                    report.count("recipe id refs", 1)


def check_blockstate_property_coverage(report: Report) -> None:
    """
    Every blockstate must cover exactly the property space its block declares.

    A blockstate that omits a state the block can take makes the model loader
    report "Exception loading blockstate variant" for each missing combination,
    and that block then renders as a missing-model cube in world. A blockstate
    that invents variants for properties the block does not have is the mirror
    image: the extra keys are silently ignored, so a log that looks rotatable in
    JSON actually is not, and the discrepancy survives every other check.

    The property space is fixed by which class BUBlocks instantiates:

      RotatedPillarBlock  logs and the altar, AXIS in {x, y, z}
      LiquidBlock         fluids, LEVEL 0..15 matched by the single empty key
      plain Block,
      BUFloraBlock,
      BUPortalBlock       everything else; these declare no properties, so the
                          only valid blockstate is the single empty variant

    This is derived from the manifest's block_kinds map rather than hand-listed,
    so a new log or a new plain block is covered the moment it is authored.
    """
    # block_kinds is written into the manifest by registry.py, which keeps this
    # derived from the same classification the generators use instead of
    # re-listing kinds here.
    kinds = MANIFEST.get("block_kinds") or {}
    blocks = MANIFEST.get("blocks") or []
    if not blocks or not kinds:
        report.note("blockstate",
                    "registry manifest carries no block kinds; property coverage "
                    "not checked")
        return

    states_dir = os.path.join(ASSETS, "blockstates")
    axis_keys = {"axis=x", "axis=y", "axis=z"}
    for block in sorted(blocks):
        path = os.path.join(states_dir, block + ".json")
        if not os.path.exists(path):
            report.error("blockstate",
                         f"block '{block}' has no blockstate file")
            continue
        try:
            doc = json.load(open(path, "r", encoding="utf-8"))
        except Exception:
            continue  # check_json already reported the parse failure
        keys = set(doc.get("variants", {}))
        multipart = doc.get("multipart")
        kind = kinds.get(block)
        report.count("blockstate property coverage", 1)

        if kind in ("log", "altar"):
            if keys != axis_keys:
                report.error(
                    "blockstate",
                    f"block '{block}' is a RotatedPillarBlock but its blockstate "
                    f"covers {sorted(keys) or 'nothing'} instead of axis=x/y/z")
        elif multipart:
            continue  # multipart describes its own state predicates
        elif keys == {""}:
            continue  # correct for every kind that declares no properties
        elif not keys:
            report.error("blockstate",
                         f"block '{block}' declares no variants, so every state of "
                         f"it fails to load a model")
        else:
            report.error(
                "blockstate",
                f"block '{block}' is a {kind} block with no blockstate properties "
                f"but its blockstate enumerates {sorted(keys)[:4]}")


def check_translations(report: Report) -> None:
    """
    Every translation key the Java asks for must exist in the lang file.

    A missing key does not fail anything: the client renders the raw key in place
    of the string, so a tooltip reads "biomesunseen.armor.set_requirement" to the
    player. The build is green, the JSON parses, and the only symptom is text on
    screen that no test would ever assert on.

    Only complete string literals are resolved. A key built by concatenation
    cannot be known statically, so those are counted and noted instead -- the
    caller is responsible for composing a key that exists.
    """
    lang_path = os.path.join(ASSETS, "lang", "en_us.json")
    if not os.path.isfile(lang_path):
        report.error("lang", "en_us.json is missing")
        return
    try:
        lang = json.load(open(lang_path, encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        report.error("lang", f"en_us.json unreadable: {exc}")
        return
    report.count("lang keys", len(lang))

    dynamic = 0
    for path in walk(JAVA, ".java"):
        text = open(path, "r", encoding="utf-8").read()
        for match in TRANSlatable_DYN.finditer(text):
            dynamic += 1
        dynamic_spans = [m.span() for m in TRANSlatable_DYN.finditer(text)]
        for match in TRANSlatable_RE.finditer(text):
            if any(start <= match.start() < end for start, end in dynamic_spans):
                continue
            key = match.group(1)
            if key not in lang:
                report.error("lang",
                             f"{rel(path)}: Component.translatable(\"{key}\") has no "
                             f"translation in en_us.json")
            report.count("java translation refs", 1)
    if dynamic:
        report.note("lang",
                    f"{dynamic} translation key(s) are built by concatenation and "
                    f"cannot be resolved statically")


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

    # ---- every registered entity is covered by exactly one table ----------
    # BUEntities.registerAttributes and BiomesUnseenClient.registerRenderers
    # both iterate BUContent.MOBS and BUContent.BOSSES and nothing else, so a
    # registered entity missing from both tables has no attribute supplier and
    # no renderer. The attribute half throws the moment the entity spawns
    # ("Entity has no attributes"), which compiles cleanly and survives every
    # other check here; the renderer half just makes the mob invisible.
    covered = set(entities)
    if MANIFEST_ENTITIES:
        unattributed = sorted(MANIFEST_ENTITIES - covered)
        if unattributed:
            report.error(
                "registry",
                f"{len(unattributed)} registered entity/entities appear in neither "
                f"BUContent.MOBS nor BUContent.BOSSES, so they get no attribute "
                f"supplier and no renderer: {unattributed[:6]}")
        phantom = sorted(covered - MANIFEST_ENTITIES)
        if phantom:
            report.error(
                "registry",
                f"{len(phantom)} MobData/BossData row(s) name an entity that is not "
                f"registered: {phantom[:6]}")
        report.count("entity attribute/renderer coverage",
                     len(MANIFEST_ENTITIES & covered))


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

    # Column count of the parameter table. BUOverworldRegion reads the authored
    # weight from column 8 behind a `row.length > 8` guard, so a generator that
    # stopped emitting it would not fail -- the fallback would treat every biome
    # as weight 100 and the authored frequency spread would silently collapse.
    if os.path.isfile(content):
        body = _bu_table(text, "SEEDED_OVERWORLD_PARAMETERS") or ""
        rows = re.findall(r"\{([^{}]*)\}", body)
        widths = {len([c for c in row.split(",") if c.strip()]) for row in rows}
        if widths and widths != {9}:
            report.error("placement",
                         f"SEEDED_OVERWORLD_PARAMETERS rows have column counts "
                         f"{sorted(widths)}, expected 9 (weight drives biome frequency)")
        report.count("overworld parameter row columns", len(widths))


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
    check_translations(report)
    check_model_and_tag_closure(report)
    check_blockstate_property_coverage(report)
    check_pixelart_glyph_geometry(report)
    check_geckolib_atlas_coverage(report)

    return report.render()


if __name__ == "__main__":
    raise SystemExit(main())
