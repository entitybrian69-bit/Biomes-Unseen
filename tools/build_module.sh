#!/usr/bin/env bash
# Build one CI matrix module and write the diagnostics the collect job commits.
#
#   tools/build_module.sh <module>
#
# Writes ci-errors/<module>.txt with:
#   * the NeoForge pin that was used (the pin script rewrites the module's
#     gradle.properties in the runner, which is otherwise invisible),
#   * every compiler error with its full javac detail (symbol/location/required/
#     found), up to 200 sites,
#   * configuration-failure diagnostics for the loader/provider bugs.
#
# NeoForge modules retry once with an older NeoForge build when the failure is a
# Gradle *configuration* failure (the binary patcher rejects some builds).
set -uo pipefail

MOD="${1:?usage: build_module.sh <module>}"
OUT="ci-errors/$MOD.txt"
mkdir -p ci-errors
: > pin.log

pin_is_neoforge=false
case "$MOD" in
  neoforge-*) pin_is_neoforge=true ;;
esac

if [ "$pin_is_neoforge" = true ]; then
  bash tools/pin_neoforge.sh "$MOD" 0 >> pin.log 2>&1 || true
else
  echo "not a neoforge module, nothing to pin" >> pin.log
fi

attempt=0
while :; do
  gradle ":$MOD:build" -x test --no-daemon --stacktrace 2>&1 | tee build.log
  code=${PIPESTATUS[0]}
  if [ "$code" -eq 0 ]; then
    break
  fi
  attempt=$((attempt + 1))
  # One retry only, and only for a NeoForge configuration failure: a compile
  # failure will not be fixed by a different NeoForge build.
  if [ "$pin_is_neoforge" != true ] || [ "$attempt" -ge 2 ]; then
    break
  fi
  if ! grep -q "A problem occurred configuring project" build.log; then
    break
  fi
  echo "=== configuration failure; retrying with NeoForge candidate $attempt ===" >> pin.log
  bash tools/pin_neoforge.sh "$MOD" "$attempt" >> pin.log 2>&1 || true
done

: > "$OUT"
{
  echo "=== PIN ==="
  cat pin.log
  echo "=== MODULE PROPERTIES ==="
  grep -E "^(minecraft_version|neoforge_version|forge_version|architectury_version)=" \
      "$MOD/gradle.properties" 2>/dev/null
} >> "$OUT"

grep -n -E "error:|Execution failed|What went wrong|FAILED" build.log > hits.txt
cut -d: -f1 hits.txt | head -200 | while read -r ln; do
  sed -n "$((ln)),$((ln + 6))p" build.log >> "$OUT"
  echo "---" >> "$OUT"
done

{
  echo "=== CONFIG DIAGNOSTICS ==="
  grep -nE "A problem occurred configuring|Patcher|ConsoleTool|binarypatcher|Could not resolve|No such file|Failed to (setup|provide|apply)|Exception in thread" build.log | head -60
  echo "=== STACKTRACE ==="
  grep -E "Caused by:|^\tat (net\.fabricmc|dev\.architectury|net\.neoforged|net\.minecraftforge)\." build.log | head -60
  echo "=== WHAT WENT WRONG ==="
  sed -n "/\* What went wrong:/,/^\* Try:/p" build.log | head -60
  echo "=== LAST 40 ==="
  tail -40 build.log
} >> "$OUT"

echo "captured $(wc -l < "$OUT") lines (exit $code)"
exit "$code"
