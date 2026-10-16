#!/usr/bin/env bash
# Dump the exact API surface of the Minecraft jar one module compiles against.
# Usage: tools/ci_probe.sh <module> [outfile]
set +e
MOD="$1"
OUT="${2:-probe-$MOD.txt}"
gradle ":$MOD:printCompileClasspath" --no-daemon -q > cp.txt 2> cp.err
MCJAR=$(grep '^CP ' cp.txt | grep -iE 'minecraft' | grep -viE 'sources' | head -1 | sed 's/^CP //')
{
  echo "MODULE=$MOD"
  echo "MCJAR=$MCJAR"
  if [ -n "$MCJAR" ]; then
    while read -r cls; do
      [ -z "$cls" ] && continue
      echo "### $cls"
      javap -p -classpath "$MCJAR" "$cls" 2>&1 | sed 's/^/    /'
    done < tools/probe_classes.txt
    echo "### CLASS-INDEX"
    unzip -l "$MCJAR" | grep -E '\.class$' | awk '{print $4}' \
      | sed 's/\.class$//; s#/#.#g' > /tmp/all_classes.txt
    while read -r probe; do
      [ -z "$probe" ] && continue
      if grep -qxF "$probe" /tmp/all_classes.txt; then
        echo "PRESENT $probe"
      else
        echo "ABSENT  $probe"
      fi
    done < tools/probe_exists.txt
  else
    echo "NO MINECRAFT JAR RESOLVED"
    tail -40 cp.err
  fi
} > "$OUT"
wc -l "$OUT"
