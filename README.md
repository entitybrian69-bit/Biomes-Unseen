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
| Guide and travel items | 3 | Field Guide, reusable Hollow Sigil, and craftable Hollow Portal block |
| Sound effects | 42 | Original synthesized Ogg/Vorbis creature, boss, and portal sounds |

## Install and start

1. Use **Minecraft 1.20.1** with **Forge 47.x**, **GeckoLib 4**, and **TerraBlender for 1.20.1** installed on both client and server.
2. Install the Biomes Unseen jar in `mods/` and restart Minecraft.
3. **Create a new world** for the complete world-generation setup. Already-generated chunks are never reshaped by adding a mod later.
4. Craft the **Biomes Unseen Field Guide** from a book, paper, and compass; right-click it for in-game help.
5. For two-way dimension travel, craft either the reusable **Hollow Sigil** or a **Hollow Portal** block. Place the portal and walk into it; a return gate is created on the Hollow Deep landing pad. If the Overworld portal is still intact, entering the return gate brings you back beside it; otherwise you arrive at Overworld spawn. The sigil provides travel without placing a block.

The Hollow Portal recipe uses 4 obsidian (`O`), 4 amethyst shards (`A`), and an ender eye (`E`):

```text
O A O
A E A
O A O
```

The guide is also available in the **Biomes Unseen** creative tab. Both travel methods work only between the Overworld and Hollow Deep.

## Finding content

Use commands (with cheats enabled) to verify or locate content in a newly created world:

```text
/locate biome biomesunseen:amber_meadow
/locate structure biomesunseen:windmill_ruin
/execute in biomesunseen:hollow_deep run tp @s 0 100 0
```

The first two commands search for natural world-generation targets; they do not force a new feature into already-generated chunks. The Hollow Sigil and Portal are the intended two-way travel methods; the command is a backup/debug route.

## Build

1. Use JDK 17 and Gradle 8.1.1 or newer.
2. Install the pinned audio-generator dependencies: `python -m pip install -r tools/requirements-audio.txt`.
3. Run `python tools/gen_all.py` to generate biomes, mobs, ores, structures, textures, audio, recipes/models/tags, and validate the resource tree.
4. Run `gradle build --no-daemon`.

There is no Gradle wrapper in this project. CI builds the reobfuscated jar and runs a dedicated server. It force-loads located chunks and inspects saved Anvil data for an actual custom biome palette and structure start, and checks the Hollow Deep, portal registration/recipe, portal block placement, guide, sigil, and weapon recipes. It does not launch a graphical client or simulate a player walking through the portal or fighting mobs, so rendering and end-to-end client gameplay still need in-game testing.

## Known limitations

- Structure templates are intentionally compact, single-piece builds; a few may intersect uneven terrain. Their density and placement still need in-game tuning.
- The seven secondary locales translate the Field Guide and core gameplay items; most biome, mob, and structure names remain English.
- The sound effects are original procedural synths rather than recorded performances.
- A newly generated world is required for reliable worldgen testing. Existing chunks do not regenerate.
