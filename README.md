# Biomes Unseen

A Minecraft 1.20.1 Forge mod (Forge 47.x, Java 17) built on GeckoLib 4 and TerraBlender.

| Content | Count | Where it comes from |
|---|---|---|
| Overworld biomes | 80 | `tools/spec/biomes.py` (10 groups x 8), injected through TerraBlender |
| Hollow Deep biomes | 60 | `tools/spec/biomes.py` (12 themes x 5), multi-noise dimension |
| Mobs | 85 | 5 hand-written Java mobs + 80 from `tools/spec/mobs.py` (plus the boss) |
| Structures | 115 | the boss arena + 114 from `tools/spec/structures.py` |
| Ores | 44 | hollowite + 43 from `tools/spec/ores.py` |

> Status: source written, **not compiled or run in game**. `tools/validate.py` checks that the
> generated files are consistent with each other; it cannot check that Minecraft accepts them.
> Lines marked `// VERIFY:` use the safest documented form of an API that could not be confirmed.

## How it fits together

Hand-written Java: registries, `BaseHollowMob`, five mobs, the boss (`HeartOfTheForestEntity`), DataGen,
TerraBlender region and surface rules. The scale-out content is **data-driven**. The generators write
spec JSON into `src/main/resources/data/biomesunseen/specs/`, and the Java registries read it at startup
(`com.biomesunseen.spec.Specs`). If a spec file is missing the mod still loads, with only the hand-written content.

| Generator | Writes |
|---|---|
| `gen_biomes.py` | 140 biome JSON files, dimension + noise settings, biome tags, per-theme spawn modifiers, `overworld.json` |
| `gen_models.py` | geo + animation JSON, loot tables, texture sheets and `mobs.json` for 80 mobs |
| `gen_ores.py` | ore block + item sprites, `ores.json`, configured/placed features and biome modifiers for 44 ores |
| `gen_structure_set.py` | 114 structure templates (`.nbt`), template pools, structures, structure sets, biome tags |
| `gen_structures.py` | the Heart of the Forest boss arena template |
| `gen_textures.py` | every PNG, from the literal hex matrices in `tools/texdata/*.py` |
| `gen_audio.py` | silent placeholder OGGs for every entry in `sounds.json` |
| `validate.py` | cross-checks everything above |

## Build order

1. `python tools/gen_all.py` — runs every generator in dependency order, then the validator.
2. `gradlew runData` — block states, models, loot, recipes, tags and lang into `src/generated/resources`. Needs the textures from step 1.
3. `gradlew build` — produces the jar. No Gradle wrapper is included; use Gradle 8.1.1 or newer, or add a wrapper.

The generators use only the Python standard library and run on Termux or Pydroid.
Run `gen_biomes.py` before `gen_ores.py`: Hollow Deep ores target the `hollow_deep` biome tag that `gen_biomes.py` writes.
`gen_biomes.py` regenerates the dimension, noise settings and the original five biome files.

## Changing content

Every entry is one row in a spec table. Edit the row, re-run `python tools/gen_all.py`, re-run `runData`.
Mob rows pick an archetype (biped, brute, crawler, quad, floater, blob, serpent), palette, glow colour, tile
templates, stats, on-hit effect and drop. Ore rows pick a host stone, vein layout, item style, tier and spawn range.

## Trying it

- Overworld: the 80 biomes blend in through TerraBlender (region weight 3, `ModTerraBlender.REGION_WEIGHT`).
- Hollow Deep has no portal. In a creative world with cheats: `/execute in biomesunseen:hollow_deep run tp @s 0 100 0`.
- Every mob has a spawn egg in the **Biomes Unseen** creative tab.

## Boss: The Heart of the Forest

| Phase | Health | Behaviour |
|---|---|---|
| 1 | above 66% | Melee inside 7 blocks, poison thorn arrows beyond 5 |
| 2 | 33-66% | Shockwave on entry, +15% speed, +25% damage, 3-arrow volleys |
| 3 | below 33% | Shockwave, +35% speed, +60% damage, 5-arrow volleys, summons Sporelings, red bar with screen darkening |

## Known limits

- Overworld surface rules are one top and one under block per biome; Hollow Deep surfaces are per theme.
- Structures are single-piece jigsaw templates with no jigsaw blocks. Structures in the Hollow Deep sit on a
  fixed floor height (y 26), so they may sink into or hover over uneven ground.
- Biome feature ids are vanilla 1.20.1 ids from a whitelist in `tools/validate.py`. A wrong id would stop a world from loading.
- All sounds are silent placeholders. There is no Hollow Deep portal.
