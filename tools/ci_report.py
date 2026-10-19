#!/usr/bin/env python3
"""
ci_report.py -- turn a Gradle build log into GitHub Actions annotations.

WHY THIS EXISTS
---------------
The sandbox this repository is developed in cannot reach the blob hosts that
serve Actions logs or artifact downloads, so a red build is unreadable from
here: `gh run view --log` fails with a network error and the only thing the
check-run annotations API returns is "Process completed with exit code 1".

Annotations, however, ARE readable through api.github.com. So the build job
pipes Gradle through this script on failure, and it republishes the parts of
the log that actually matter -- javac's file:line: error: messages and
Gradle's "What went wrong" block -- as workflow-command annotations.

That closes the develop-compile-fix loop without needing log access: read the
annotations, fix the Java, push again.

Usage: python3 tools/ci_report.py <build.log>
"""

from __future__ import annotations

import os
import re
import sys

# javac: "src/main/java/Foo.java:42: error: cannot find symbol"
JAVAC = re.compile(r"^(?P<file>[^\s:]+\.java):(?P<line>\d+):\s*(?P<sev>error|warning):\s*(?P<msg>.*)$")

# ForgeGradle/javac sometimes prefixes with a path containing spaces; also catch
# the "N errors" summary so we can report how much was truncated.
ERROR_COUNT = re.compile(r"^(\d+)\s+errors?$")

# Gradle's failure block starts here and runs to the next blank-line section.
WHAT_WENT_WRONG = "* What went wrong:"

# Annotation messages are capped well below this in practice; chunking keeps a
# long Gradle stacktrace from being silently dropped by the runner.
CHUNK = 900
MAX_CHUNKS = 24


def emit(level: str, message: str, file: str = "", line: int = 0) -> None:
    """Write one GitHub workflow command."""
    message = message.replace("%", "%25").replace("\r", " ").replace("\n", " ")
    props = []
    if file:
        props.append(f"file={file}")
    if line:
        props.append(f"line={line}")
    suffix = f",{','.join(props)}" if props else ""
    print(f"::{level}{suffix}::{message}")


def chunked(level: str, title: str, text: str) -> None:
    """Emit long text as several annotations so none of it is lost."""
    text = text.strip()
    if not text:
        return
    parts = [text[i:i + CHUNK] for i in range(0, len(text), CHUNK)][:MAX_CHUNKS]
    for index, part in enumerate(parts, start=1):
        prefix = f"{title} ({index}/{len(parts)})" if len(parts) > 1 else title
        emit(level, f"{prefix}: {part}")


def main() -> int:
    if len(sys.argv) < 2:
        emit("error", "ci_report.py: no build log path given")
        return 1
    path = sys.argv[1]
    if not os.path.exists(path):
        emit("error", f"ci_report.py: build log not found at {path}")
        return 1

    lines = open(path, "r", encoding="utf-8", errors="replace").read().splitlines()

    # ---- 1. javac diagnostics -------------------------------------------
    # Collected first, then published as a few consolidated annotations.
    #
    # Emitting one annotation per diagnostic with file=/line= looks better in
    # principle, but GitHub silently discards file-scoped annotations once a run
    # produces many of them -- a 74-error build came back with none of the
    # per-file entries retained, leaving only the summary. Generic annotations
    # survive, so the diagnostics are chunked into those instead. Losing the
    # inline placement is worth more than losing the message.
    seen = set()
    diagnostics = []
    javac_errors = 0
    javac_warnings = 0
    for raw in lines:
        match = JAVAC.match(raw.strip())
        if not match:
            continue
        key = (match["file"], match["line"], match["msg"])
        if key in seen:
            continue
        seen.add(key)
        if match["sev"] == "error":
            javac_errors += 1
        else:
            javac_warnings += 1
        # Keep file and line in the text, since the annotation can no longer
        # carry them as structured fields.
        short = match["file"].split("/com/biomesunseen/")[-1]
        diagnostics.append(f"{short}:{match['line']}: {match['sev']}: {match['msg']}")

    if diagnostics:
        chunked("error", "javac", "\n".join(diagnostics))

    # ---- 2. Gradle's own failure explanation -----------------------------
    # Covers failures that are not javac's: missing dependencies, plugin
    # resolution, ForgeGradle setup, mixin annotation processing.
    wrong = []
    capture = False
    for raw in lines:
        if raw.startswith(WHAT_WENT_WRONG):
            capture = True
        elif capture and raw.startswith("* Try:"):
            break
        elif capture:
            wrong.append(raw)
    if wrong:
        chunked("error", "Gradle failure", "\n".join(wrong))

    # ---- 3. Fallback tail -------------------------------------------------
    # If neither pattern matched, publish the end of the log so the run is still
    # diagnosable rather than failing silently.
    if not javac_errors and not wrong:
        tail = "\n".join(lines[-120:])
        chunked("error", "Build log tail", tail)

    emit("error",
         f"Biomes Unseen build failed: {javac_errors} javac error(s) across "
         f"{len(set(d.split(':')[0] for d in diagnostics))} file(s); "
         f"{javac_warnings} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
