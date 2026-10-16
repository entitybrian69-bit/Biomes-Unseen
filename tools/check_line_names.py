#!/usr/bin/env python3
"""Check every net.minecraft.* name used by one generated line against the jar.

Usage:  python3 tools/check_line_names.py <line-key> [probe-report]

The CI probe job dumps, for the four Mojang-mapped legacy targets, the complete
class index of the Minecraft jar it compiles against ("### ALL-CLASSES").  This
script reads that index and reports every Minecraft type referenced by the
matching common/src/line-* tree (plus the two loader modules for that line) that
does not exist in that jar, which is exactly the class of error that made the
legacy targets red.

Names that are only referenced as "Package.Member" (constants, statics) are
resolved to the longest class prefix that does exist, so only genuine misses are
printed.
"""

import os
import re
import sys

LINE_MODULE = {
    "1.16.5": ["fabric-1.16.5", "forge-1.16.5"],
    "1.17.1": ["fabric-1.17.1", "forge-1.17.1"],
    "1.18.1": ["fabric-1.18.1", "forge-1.18.1"],
    "1.18": ["fabric-1.18.2", "forge-1.18.2"],
}

# net.minecraft.X.Y.Z references inside source text
_RE_FQN = re.compile(r'\bnet\.minecraft\.[A-Za-z0-9_.$]+')


_RE_BARE_CLASS = re.compile(r'^net\.minecraft\.[A-Za-z0-9_$.]+$')


def load_index(path):
    """Class names from the probe's ### ALL-CLASSES section (if present)."""
    classes = set()
    in_section = False
    for line in open(path, encoding="utf-8", errors="replace"):
        stripped = line.strip()
        if stripped.startswith("### "):
            in_section = stripped == "### ALL-CLASSES"
            continue
        if in_section and _RE_BARE_CLASS.match(stripped):
            classes.add(stripped)
    return classes


def source_files(root, line_key, modules):
    dirs = [os.path.join(root, "common/src/line-%s" % line_key, "java")]
    for mod in modules:
        dirs.append(os.path.join(root, mod, "src/main/java"))
    for d in dirs:
        if not os.path.isdir(d):
            continue
        for r, _dirs, files in os.walk(d):
            for f in files:
                if f.endswith(".java"):
                    yield os.path.join(r, f)


def resolve(fqn, classes, allow_prefix=True):
    """Longest prefix of fqn that is a real class (nested classes use $)."""
    parts = fqn.split(".")
    while len(parts) > 3:
        candidate = ".".join(parts)
        if candidate in classes:
            return candidate
        # nested class written with dots
        nested = "$".join([".".join(parts[:len(parts) - 1]), parts[-1]])
        if nested in classes:
            return nested
        parts.pop()
    return None


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    line_key = sys.argv[1] if len(sys.argv) > 1 else "1.16.5"
    modules = LINE_MODULE.get(line_key, [])
    probe = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        root, "docs/api-probe", "probe-%s.txt" % (modules[0] if modules else line_key))
    if not os.path.isfile(probe):
        print("no probe report at %s" % probe)
        return 2
    classes = load_index(probe)
    if not classes:
        print("%s has no ### ALL-CLASSES section yet" % probe)
        return 2

    misses = {}
    for path in source_files(root, line_key, modules):
        text = open(path, encoding="utf-8", errors="replace").read()
        for fqn in set(_RE_FQN.findall(text)):
            if resolve(fqn, classes) is None:
                misses.setdefault(fqn, []).append(path)
    print("=== %s: %d unknown Minecraft type reference(s) ===" % (line_key, len(misses)))
    for fqn in sorted(misses, key=lambda f: (-len(misses[f]), f)):
        where = sorted({p.replace(root + "/", "") for p in misses[fqn]})
        print("  %-70s %s" % (fqn, where[0] + (" (+%d)" % (len(where) - 1) if len(where) > 1 else "")))
    return 1 if misses else 0


if __name__ == "__main__":
    sys.exit(main())
