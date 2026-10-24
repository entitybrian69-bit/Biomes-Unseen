# Biomes Unseen — Quick Start

## Requirements

- Minecraft Java Edition 1.20.1
- Forge 47.x
- GeckoLib 4 for Forge 1.20.1
- TerraBlender for Forge 1.20.1
- The Biomes Unseen jar

Install all four mods in the same `mods/` folder. Start Minecraft once to confirm the mod is loaded, then create a **new world**. New biomes and structures affect world generation; existing chunks do not change.

## Explore the world

In Survival, make a Field Guide with a book, paper, and compass. Right-click it for the in-game instructions. With cheats enabled, the vanilla locator commands can check whether worldgen is active:

```text
/locate biome biomesunseen:amber_meadow
/locate structure biomesunseen:windmill_ruin
```

Travel to the Hollow Deep by crafting a Hollow Sigil from obsidian, ender pearls, glowstone dust, and paper. Use it in the Overworld to enter; use it again in the Hollow Deep to return to the Overworld spawn. The sigil builds a small safe landing pad at the dimension arrival point. A command route is available as a backup:

```text
/execute in biomesunseen:hollow_deep run tp @s 0 100 0
```

## Weapons

Ore materials can be crafted into matching swords with two material items and one stick. Their strength follows the material's ore tier. Hollowite also has a sword and a higher-damage battleaxe. Hollowite is found in the Hollow Deep; the travel sigil uses vanilla materials so you do not need Hollowite to enter the dimension.

## Troubleshooting

- **No new biomes/structures:** confirm TerraBlender is installed, restart the game, create a new world, and use `/locate biome` or `/locate structure` in unexplored terrain.
- **Hollow Deep does not load:** use a world created with Biomes Unseen installed; check `latest.log` for the startup message `Biomes Unseen worldgen ready`.
- **No guide/weapon items:** check the Biomes Unseen creative tab and confirm the installed jar is the latest build. Dependencies must be present for the mod to load.
