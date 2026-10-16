#!/usr/bin/env bash
# Resolve an exact NeoForge version pin for one module.
#
# Why this exists: the modules declared dynamic ranges ("21.1.+").  Architectury
# Loom turns the neoForge dependency into "<dep>:userdev" (ForgeProvider.provide)
# and resolves that separately, so a range that lands on a NeoForge build without
# a published -userdev.jar dies with:
#   Failed to provide net.neoforged:neoforge:21.1.+ :
#     java.lang.RuntimeException: Could not resolve Forge userdev
# Rather than guess pins, ask maven.neoforged.net which versions exist and keep
# the newest one that actually publishes the userdev artifact.
#
# Usage: tools/pin_neoforge.sh <module-dir>
# Rewrites neoforge_version= in <module-dir>/gradle.properties.  Exits non-zero
# only if no usable version can be found, so the build still reports something.
set -uo pipefail

MOD="${1:?usage: pin_neoforge.sh <module-dir> [candidate-index]}"
# 0 (default) picks the newest usable build; higher indexes walk back through
# the candidate list so a build can retry when one build cannot be patched.
IDX="${2:-0}"
PROPS="$MOD/gradle.properties"
[ -f "$PROPS" ] || { echo "pin_neoforge: no $PROPS"; exit 1; }

MC="$(sed -n 's/^minecraft_version=//p' "$PROPS" | head -1)"
[ -n "$MC" ] || { echo "pin_neoforge: no minecraft_version in $PROPS"; exit 1; }

# MC 1.20.2 -> 20.2 ; MC 1.21 -> 21.0 ; MC 1.21.10 -> 21.10 ; MC 26.1 -> 26.1
SERIES="${MC#1.}"
case "$SERIES" in
  *.*) ;;
  *)   SERIES="$SERIES.0" ;;
esac

BASE="https://maven.neoforged.net/releases/net/neoforged/neoforge"
META="$(mktemp)"
if ! curl -sfL --retry 3 --max-time 60 "$BASE/maven-metadata.xml" -o "$META"; then
  echo "pin_neoforge: could not fetch $BASE/maven-metadata.xml (keeping existing pin)"
  rm -f "$META"; exit 0
fi

# Newest first, restricted to this MC series.
mapfile -t CANDIDATES < <(
  grep -oE '<version>[^<]+</version>' "$META" \
    | sed -e 's#</\?version>##g' \
    | grep -E "^${SERIES//./\\.}\\.[0-9]+(\\.[0-9]+)?(-[A-Za-z0-9.]+)?$" \
    | sort -t. -k1,1n -k2,2n -k3,3n -k4,4n -r
)
rm -f "$META"

if [ "${#CANDIDATES[@]}" -eq 0 ]; then
  echo "pin_neoforge: metadata has no ${SERIES}.x versions (keeping existing pin)"
  exit 0
fi

# An exact pin that the metadata actually lists is authoritative: it is the
# version this line was tested against.  Re-resolving a *published* exact pin
# walks down to early builds whose binpatches no longer match the shipped
# Minecraft jar and dies in the NeoForm patcher ("Patch expected <class> to
# have the checksum ..."), while an unpublished pin (a stale guess) still has
# to be resolved.
CURRENT="$(sed -n 's/^neoforge_version=//p' "$PROPS" | head -1)"
if [ -n "$CURRENT" ] && [ "${CURRENT}" != *"+"* ]; then
  for v in "${CANDIDATES[@]}"; do
    if [ "$v" = "$CURRENT" ]; then
      echo "pin_neoforge: $MOD already pinned to published $CURRENT"
      exit 0
    fi
  done
  echo "pin_neoforge: $CURRENT is not published for ${SERIES}.x; resolving"
fi

PICK=""
for v in "${CANDIDATES[@]:$IDX}"; do
  # Prefer a build that really publishes the userdev jar Loom asks for.
  if curl -sfI --max-time 30 "$BASE/$v/neoforge-$v-userdev.jar" >/dev/null 2>&1; then
    PICK="$v"; break
  fi
done

if [ -z "$PICK" ]; then
  # Nothing publishes userdev under a HEAD probe; fall back to the newest listed.
  PICK="${CANDIDATES[$IDX]:-${CANDIDATES[0]}}"
  echo "pin_neoforge: no userdev jar confirmed for ${SERIES}.x; falling back to $PICK"
fi

OLD="$(sed -n 's/^neoforge_version=//p' "$PROPS" | head -1)"
if [ "$OLD" = "$PICK" ]; then
  echo "pin_neoforge: $MOD already pinned to $PICK"
else
  sed -i "s#^neoforge_version=.*#neoforge_version=${PICK}#" "$PROPS"
  echo "pin_neoforge: $MOD neoforge_version ${OLD:-<unset>} -> ${PICK}"
fi
