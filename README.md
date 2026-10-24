# Biomes Unseen

A Minecraft 1.20.1 Forge mod with new Overworld biomes, a separately explorable dimension, hostile creatures, ores, weapons, and structures.

## Content

| Content | Count | Details |
|---|---:|---|
| Overworld biomes | 80 | Ten families; blended into new Overworld terrain by TerraBlender |
| Hollow Deep biomes | 60 | Twelve themes in the Hollow Deep dimension |
| Mobs | 86 | 80 generated creatures, five hand-written mobs, and the Heart of the Forest boss |
| Ores | 44 | Ore blocks/materials with worldgen, drops, and smelting/blasting recipes |
| Structures | 115 | 114 biome-specific structures plus the boss arena |
| Weapons | 45 | 44 material swords plus the Hollowite Battleaxe |
| Guide/travel items | 2 | Field Guide and reusable Hollow Sigil |

## Install and start

1. Use **Minecraft 1.20.1** with **Forge 47.x**, **GeckoLib 4**, and **TerraBlender for 1.20.1** installed on both client and server.
2. Install the Biomes Unseen jar in `mods/` and restart Minecraft.
3. **Create a new world** for the complete world-generation setup. Already-generated chunks are never reshaped by adding a mod later.
4. In Survival, craft the **Biomes Unseen Field Guide** from a book, paper, and compass. Right-click it for in-game help. Craft a **Hollow Sigil** from vanilla materials to travel to and from the Hollow Deep.

The guide is also available in the **Biomes Unseen** creative tab. The sigil only works in the Overworld and Hollow Deep.

## Finding content

Use commands (with cheats enabled) to verify or locate content in a newly created world:

```text
/locate biome biomesunseen:amber_meadow
/locate structure biomesunseen:windmill_ruin
/execute in biomesunseen:hollow_deep run tp @s 0 100 0
```

The first two commands search for natural world-generation targets; they do not force a new feature into already-generated chunks. The Hollow Sigil is the intended two-way dimension travel item; the command is a backup/debug route.

## Build

1. `python tools/gen_all.py` — generates biomes, mobs, ores, structures, textures, recipes/models/tags, and validates the resource tree.
2. `gradle build --no-daemon` with JDK 17 and Gradle 8.1.1 or newer.

There is no Gradle wrapper in this project. The CI workflow builds the reobfuscated jar and performs a dedicated-server startup/worldgen-registry smoke test. It does not launch a graphical client, so rendering and extended gameplay still need in-game testing.

## Known limitations

- The Hollow Deep portal block is not implemented; the reusable Hollow Sigil is the travel mechanism.
- Sounds are silent placeholders.
- Structures are compact single-piece jigsaw templates; some can intersect uneven terrain.
- A newly generated world is required for a reliable worldgen test. Use `/locate` commands before assuming features are missing.
