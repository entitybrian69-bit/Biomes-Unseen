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
