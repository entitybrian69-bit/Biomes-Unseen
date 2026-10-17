# Biomes Unseen

> A massive world-generation, adventure, biome, structure, ore, mob and boss mod: 80 biomes, 20 ores, 30 structures, 25 mobs and 2 multi-phase bosses.

**Mod id:** `biomesunseen` &nbsp;|&nbsp; **Version:** 1.0.3 &nbsp;|&nbsp; **License:** MIT

## Content

- **80** unique biomes (8 families: Crystal, Ember, Verdant, Frost, Storm, Mire, Sky, Void)
- **20** ores with unique textures, particles, mining sounds, tool/armor/material tiers and worldgen conditions
- **30** jigsaw structures including 2 massive boss arenas, lore books, journals and murals
- **25** mobs with GeckoLib animations, goal-based AI, herding, taming, trading, fleeing, pack tactics and terrain use
- **2** multi-phase bosses: *The Heart of the Forest* and *The Void Serpent*
- Full tag support (wood, stone, ores, plants, mobs) for inter-mod compatibility
- Cloth Config integration: biome rarity, ore rates, structure spacing, mob caps, feature toggles
- DataGen for blockstates, models, loot tables, recipes, tags, worldgen, biome, structure and spawn data

## Project layout

```
common/            shared content definitions, registries, worldgen, datagen, assets
fabric-<mc>/       Fabric entrypoint for Minecraft <mc>
forge-<mc>/        Forge entrypoint (1.16.5 - 1.20.1)
neoforge-<mc>/     NeoForge entrypoint (1.20.2+)
tools/             the project generator that stamps every module
```

Every target in the 1.16.5 - 26.3 matrix exists as its own Gradle subproject.
The shared code under `common/` is compiled into each module against that
module's exact Minecraft/loader toolchain (Architectury Loom, Mojang mappings).

## Requirements

- **JDK** matching the target (8 for 1.16.5, 16 for 1.17.1, 17 for 1.18-1.20.4,
  21 for 1.20.5-1.21.11, 25 for 26.x). Gradle toolchains download missing JDKs automatically.
- **Gradle 9.8.1** (or run `gradle wrapper --gradle-version 9.8.1` once; `gradlew` does this automatically if a system Gradle is on PATH).
- Internet access to Fabric / Forge / NeoForge / Architectury / GeckoLib / Shedaniel maven hosts.

## Building

Build **one** target (recommended):

```bash
./gradlew :fabric-1.21.1:build          # Fabric for Minecraft 1.21.1
./gradlew :neoforge-1.21.1:build       # NeoForge for Minecraft 1.21.1
./gradlew :forge-1.20.1:build          # Forge for Minecraft 1.20.1
```

The jar lands in `<module>/build/libs/`.

Build **all** targets (slow, resolves every Minecraft version):

```bash
./gradlew build
```

Run datagen for a target (regenerates blockstates/models/loot/recipes/tags/worldgen):

```bash
./gradlew :fabric-1.21.1:runDatagen
```

See **BUILD.md** for the full per-target build matrix, output paths and
dependency-bump instructions.

## Configuration

Everything (biome rarity, ore rates, structure spacing, mob caps, per-feature
toggles) is configurable through Cloth Config (`Config` -> `Biomes Unseen`) or
by editing `config/biomesunseen.json`. Defaults generate all content in the world.

## Credits

Biomes Unseen Team. Licensed under MIT.
