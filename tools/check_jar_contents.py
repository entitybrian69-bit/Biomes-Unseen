#!/usr/bin/env python3
"""Pre-flight check of what each module's jar will contain.

Guards the two launch-critical properties that are easy to break from the
generator:

  1. ``fabric.mod.json`` must only declare ``biomesunseen.mixins.json`` when the
     module actually ships that file (Fabric aborts the launch otherwise).
  2. The line's datapack tree must be wired into the module's resources, or the
     jar loads with no biomes/features/structures at all.

Usage: tools/check_jar_contents.py [module ...]     (default: every module)
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from emit_data import STYLE_DIRS, style_key            # noqa: E402
from lines import LINES, MC_TO_LINE                    # noqa: E402

ICON = "assets/biomesunseen/icon.png"
MIXIN_CONFIG = "biomesunseen.mixins.json"


def resource_roots(mod, mc):
    flags = LINES[MC_TO_LINE[mc]]
    return [
        "common/src/main/resources",
        "common/src/line-%s/resources" % MC_TO_LINE[mc],
        "common/src/%s/resources" % STYLE_DIRS[style_key(flags)],
        "%s/src/main/resources" % mod,
        "%s/src/generated/resources" % mod,
    ]


def jar_paths(mod, mc):
    found = set()
    for root in resource_roots(mod, mc):
        for dirpath, _dirs, files in os.walk(root):
            for name in files:
                found.add(os.path.relpath(os.path.join(dirpath, name), root))
    return found


def main(argv):
    modules = argv[1:] or sorted(
        os.path.dirname(p) for p in glob.glob("*/build.gradle")
        if os.path.dirname(p).split("-")[0] in ("fabric", "forge", "neoforge"))
    problems = []
    for mod in modules:
        mc = mod.split("-", 1)[1]
        paths = jar_paths(mod, mc)
        biomes = [p for p in paths if "/worldgen/biome/" in p and p.endswith(".json")]
        if ICON not in paths:
            problems.append("%s: missing %s" % (mod, ICON))
        if len(biomes) != 80:
            problems.append("%s: %d biome files (expected 80)" % (mod, len(biomes)))
        flags = LINES[MC_TO_LINE[mc]]
        style_dir = STYLE_DIRS[style_key(flags)]
        biome_style = style_key(flags)[3]
        # worldgen codec-shape gate (world-creation crash class): every biome
        # must carry the keys each line's Biome codec requires.
        bsamp = sorted(glob.glob(os.path.join(
            "common/src", style_dir,
            "resources/data/biomesunseen/worldgen/biome", "*.json")))
        if bsamp:
            b = json.load(open(bsamp[0]))
            eff = b.get("effects", {})
            for key in ("water_fog_color", "sky_color", "fog_color", "water_color"):
                if key not in eff:
                    problems.append("%s: biome effects missing %s" % (mod, key))
            if "carvers" not in b or "features" not in b:
                problems.append("%s: biome missing carvers/features" % mod)
            if biome_style == "attrs":
                if "attributes" not in b:
                    problems.append("%s: 26.x biome missing attributes" % mod)
            else:
                if "spawners" not in b or "spawn_costs" not in b:
                    problems.append("%s: biome missing spawners/spawn_costs" % mod)
            if biome_style in ("old", "new") and "precipitation" not in b:
                problems.append("%s: biome missing precipitation" % mod)
            if biome_style != "old" and "has_precipitation" not in b:
                problems.append("%s: biome missing has_precipitation" % mod)
            if biome_style in ("old", "new") and not isinstance(b.get("carvers"), dict):
                problems.append("%s: carvers must be the map form on this line" % mod)
            if biome_style in ("list", "attrs") and not isinstance(b.get("carvers"), list):
                problems.append("%s: carvers must be the list form on this line" % mod)
        if flags["structures"] == "sets":
            ssamp = sorted(glob.glob(os.path.join(
                "common/src", style_dir,
                "resources/data/biomesunseen/worldgen/structure", "*.json")))
            if ssamp:
                st = json.load(open(ssamp[0]))
                for key in ("start_pool", "size", "max_distance_from_center",
                            "use_expansion_hack", "step", "biomes"):
                    if key not in st:
                        problems.append("%s: structure missing %s" % (mod, key))
                if "config" in st:
                    problems.append("%s: structure uses the config wrapper" % mod)
                mdc = st.get("max_distance_from_center")
                if isinstance(mdc, int) and not 1 <= mdc <= 128:
                    problems.append("%s: structure max_distance_from_center %d outside [1:128]"
                                    % (mod, mdc))
            if glob.glob(os.path.join(
                    "common/src", style_dir, "resources/data/minecraft/worldgen",
                    "multi_noise_biome_source_parameter_list", "*.json")):
                problems.append("%s: ships invalid multi_noise parameter list" % mod)
        # Climate parameter range gate: Climate.Parameter is
        # intervalCodec(floatRange(-2,2)) and offset is floatRange(0,1).
        # Out-of-range values make world_preset/dimension fail to decode
        # ("Missing overworld dimension") and abort world creation.
        for pf in sorted(glob.glob(os.path.join(
                "common/src", style_dir, "resources/data", "**", "*.json"),
                recursive=True)):
            try:
                doc = json.load(open(pf))
            except Exception:
                continue
            stack = [doc]
            while stack:
                o = stack.pop()
                if isinstance(o, dict):
                    if ("temperature" in o and "offset" in o
                            and isinstance(o.get("offset"), (int, float))):
                        for ax in ("temperature", "humidity", "continentalness",
                                   "erosion", "depth", "weirdness"):
                            v = o.get(ax)
                            if isinstance(v, (int, float)) and not -2.0 <= v <= 2.0:
                                problems.append("%s: %s %s=%s outside [-2:2]"
                                                % (mod, os.path.basename(pf), ax, v))
                        off = o.get("offset")
                        if isinstance(off, (int, float)) and not 0.0 <= off <= 1.0:
                            problems.append("%s: %s offset=%s outside [0:1]"
                                            % (mod, os.path.basename(pf), off))
                    stack.extend(o.values())
                elif isinstance(o, list):
                    stack.extend(o)
        for ssp in sorted(glob.glob(os.path.join(
                "common/src", style_dir,
                "resources/data/biomesunseen/worldgen/structure_set", "*.json"))):
            try:
                doc = json.load(open(ssp))
            except Exception:
                continue
            pl = doc.get("placement", {})
            sp, sep = pl.get("spacing"), pl.get("separation")
            if isinstance(sp, int) and isinstance(sep, int) and not sp > sep:
                problems.append("%s: %s spacing %d <= separation %d"
                                % (mod, os.path.basename(ssp), sp, sep))
        if mod.startswith("fabric"):
            declared = ('"mixins"' in open(
                "%s/src/main/resources/fabric.mod.json" % mod).read())
            shipped = MIXIN_CONFIG in paths
            if declared != shipped:
                problems.append(
                    "%s: fabric.mod.json %s the mixin config but the jar %s it"
                    % (mod, "declares" if declared else "does not declare",
                       "ships" if shipped else "does not ship"))
    for mod in modules:
        print("ok   %s" % mod)
    for problem in problems:
        print("FAIL %s" % problem)
    print("%d module(s) checked, %d problem(s)" % (len(modules), len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
