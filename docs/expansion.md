# Biomes Unseen 1.0.3 — dimensions and bosses

This document describes the content added by the "three dimensions, five
bosses" expansion. Everything below is generated from `tools/content.py`, so
it is identical on every one of the 66 modules; the only differences between
modules are the Minecraft API calls, which come from `tools/lines.py`.

## Catalog

| Table | Count |
| --- | --- |
| Biomes | 140 (80 overworld + 20 per dimension) |
| Ores | 44 (20 overworld + 8 per dimension) |
| Palette blocks | 30 (12 decorative + 15 dimension stones + 3 portals) |
| Plants | 10 |
| Mobs | 55 (25 overworld + 10 per dimension) |
| Bosses | 5 |
| Structures | 48 (30 overworld + 5 per dimension + 3 portal gates) |
| Sound events | 62 |
| Particle types | 11 |
| Advancements | 19 |

## The dimensions

Each dimension ships a `data/biomesunseen/dimension/<id>.json` file built the
same way as the overworld replacement: a `minecraft:noise` generator whose
`multi_noise` biome source lists that dimension's 20 biomes plus one vanilla
fallback, so every climate point resolves. Vanilla dimension types are reused
(`the_nether`, `overworld`, `the_end`) because custom `dimension_type` codecs
changed fields three times between 1.16.5 and 26.x; the sky and fog identity
of each dimension comes from its biome `effects` instead, which every one of
those versions reads.

### The Hollow Deep (`biomesunseen:hollow_deep`)

* Subterranean, no sky: `minecraft:the_nether` dimension type, `caves` noise
  settings (overworld settings on 1.16.5/1.17.1, where `caves` does not exist).
* Stones: hollowstone, deepslate marrow, glowgabbro, emberlimestone,
  fossilshale.
* Ores: lumenshard, deep iron, biolumite, hollow crystal, embercoal,
  fungisteel, abyss opal, corestone.
* Mobs: glowmoth, tunnel hound, crystal beetle, magma snail, echo bat, root
  gnawer, deep lurker, lantern jelly, stoneback, mycopath.
* Structures: Warden's Spire Arena, Glowroot Shrine, Fossil Vault, Ember
  Siphon, Mycelium Circle.
* Boss: **Warden of the Hollow Deep** (620 HP, `wardens_spire_arena`).

### Aetherfall (`biomesunseen:aetherfall`)

* Floating islands under a skylit, `overworld`-typed sky; `floating_islands`
  noise settings on 1.18+, plain overworld settings before that.
* Stones: skyglass, cloudstone, dawnquartzite, windslate, starfall basalt.
* Ores: skyiron, dawnsilver, windquartz, cloudite, sunforged, starfall ore,
  aurorite, aetherglass.
* Mobs: skyray, cloud heron, zephyr pup, island tortoise, dawnfinch, storm jay,
  summit ram, mistgraz, star serpent, windlark.
* Structures: Crown's Eyrie, Skyglass Temple, Windward Beacon, Starfall
  Observatory, Halo Gatehouse.
* Boss: **The Skyward Crown** (560 HP, `crowns_eyrie`).

### The Void Between (`biomesunseen:void_between`)

* `the_end` dimension type: no skylight, end sky, near-zero ambient light.
* Stones: voidstone, nullslate, paradox granite, echoeslate, static breccia.
* Ores: nullite, glitchstone, paradox shard, entropy crystal, void ember,
  mirrorshard, static ore, finality.
* Mobs: glitchling, null stalker, mirror wisp, paradox beast, static crawler,
  dream eater, shardwing, inverse grazer, echo husk, unravel spawn.
* Structures: Unraveling Nexus, Paradox Arch, Mirror Vault, Static Ziggurat,
  Forgotten Library.
* Boss: **The Unraveling** (700 HP, `unraveling_nexus`).

## Reaching a dimension

1. Each dimension's key drops from one of its own mobs —
   `hollow_heart_key` (glowmoth), `aetherfall_key` (dawnfinch),
   `void_between_key` (glitchling).
2. The key is also craftable: 4x the dimension's stone, 4x Unseen Sigil and
   1x the key ore's tonic (`SGS / GKG / SGS`).
3. Right-clicking with a key enters its dimension; right-clicking with it
   while inside returns the player to the exact spot they left the overworld.
4. `UnseenTravel` finds the destination by comparing
   `Level#dimension().location()` against every level returned by
   `MinecraftServer#getAllLevels()`, and lays a 3x3 landing pad with the
   4-argument `setBlock` — the one block-write signature present on all 33
   probed versions.

## Bosses

| Boss | HP | Arena | Phases |
| --- | --- | --- | --- |
| The Heart of the Forest | 480 | Cradle of Roots | dormant, awakening, wrath, final bloom |
| The Void Serpent | 520 | Rift Basin | coiled, uncoiling, devouring, unbound |
| Warden of the Hollow Deep | 620 | Warden's Spire Arena | buried, awakens, spire risen, collapse |
| The Skyward Crown | 560 | Crown's Eyrie | descending, haloed, shardfall, last light |
| The Unraveling | 700 | Unraveling Nexus | quadruped, serpent, humanoid, unmade |

All five are health-gated four-phase encounters driven from `aiStep`, with a
GeckoLib animation set (`idle`, `walk`, per-phase one-shots, per-attack
one-shots, `hurt`, `death`), per-phase boss music, a guaranteed unique relic
drop plus Unseen Sigil and a mineral cache, and `removeWhenFarAway` /
`requiresCustomPersistence` overrides so they stay put.

## Animation coverage

* 55 mobs: geometry is quadruped or bird shaped, scaled per mob, with the
  animation dictionary generated from each mob's behaviour list — graze,
  herd, fly/flutter/glide/dive, swim/surface, burrow/emerge, trade/offer/
  accept, tame/sit/beg, charge/headbutt, lunge/attack, hurt and death.
* 5 bosses: serpent geometry for the Void Serpent and The Unraveling, a
  crowned raptor for The Skyward Crown, a trunk-and-heart rig for The Heart
  of the Forest, and a heavy quadruped for the Warden.
* 30 palette blocks include three animated portal blocks.
