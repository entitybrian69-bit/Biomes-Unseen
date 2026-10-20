# Biomes Unseen

A total-conversion worldgen expansion for **Minecraft 1.20.1 (Forge)**.

Biomes Unseen adds 140 hand-authored biomes across four dimensions, three new
dimensions of its own, 85 creatures driven by articulated GeckoLib models, five
multi-phase bosses with bespoke arenas, 44 ores that each have a use, and ten
gear families with real set bonuses.

Every texture is hand-authored pixel art. Every structure is a real jigsaw
template. Every hostile has working targeting and melee AI. Nothing in the mod is
a placeholder that compiles and then does nothing.

---

## Contents

| | Count | Notes |
|---|---|---|
| Biomes | **140** | 80 Overworld (16 in each of 5 categories) + 20 per new dimension |
| Dimensions | **3** | The Hollow Deep, Aetherfall, The Void Between |
| Creatures | **80** | 52 hostile, 28 passive, across 6 rig families |
| Bosses | **5** | 4 phases each, bespoke arena, own music track |
| Structures | **115** | Jigsaw, including 5 hand-authored boss arenas |
| Ores | **44** | 20 Overworld + 24 dimensional, each with a use |
| Gear families | **10** | 5 tools + 4 armour pieces + bow/shield, with set bonuses |
| Blocks | **264** | 64 ores, 44 mineral blocks, 27 flora, 13 grass, 8 logs, 4 fluids, 3 portals |
| Items | **285** | Plus a BlockItem for each of the 257 solid blocks |
| Textures | **684 PNG** | Hand-authored glyph matrices, never procedurally drawn |
| GeckoLib rigs | **22** | 6 family + 5 boss geo/animation pairs |
| Structure templates | **115 NBT** | 46,573 blocks, 227 loot-bearing chests |

The five Overworld biome categories are **Ethereal**, **Ancient**, **Vibrant**,
**Harsh** and **Aquatic**.

The five bosses are **The Heart of the Forest** (Overworld), **The Void Serpent**
(The Void Between), **The Warden of the Hollow Deep** (The Hollow Deep), **The
Skyward Crown** (Aetherfall) and **The Unraveling** (The Void Between).

---

## Requirements

| | |
|---|---|
| Minecraft | 1.20.1 |
| Forge | 47.2.20 or newer |
| Java | 17 (exactly — ForgeGradle 6 breaks on newer toolchains) |
| [GeckoLib](https://github.com/bernie-g/geckolib) | 4.4.7 or newer — required |
| [TerraBlender](https://github.com/Glitchfiend/TerraBlender) | 3.0.0 or newer — required |

GeckoLib provides the animation system; no creature in this mod uses
`CubeListBuilder` or `ModelPart`. TerraBlender blends the 80 Overworld biomes
into vanilla's climate parameters — see
[Why TerraBlender](#why-terrablender-for-overworld-biomes).

---

## Building

```bash
gradle build
```

The jar lands in `build/libs/`. There is no Gradle wrapper in this repository:
the wrapper jar is a binary blob that cannot be generated from source here, so
Gradle **8.1.1** is expected on `PATH` (CI provisions it via
`gradle/actions/setup-gradle`).

`processResources` runs the art pipeline and the validator, so a build fails if
the shipped assets do not match the content tables.

Python 3.11+ is needed for the generators but **not** to play the mod — every
generated asset is committed, so the jar never depends on Python at runtime.

---

## How the mod is built

This repository is unusual in that almost none of it is written by hand twice.
The content is authored once, in Python dataclasses, and everything the game
loads is generated from that.

```
tools/content/          the authored source of truth
  biomes.py               140 BiomeSpec records (40 fields each)
  mobs.py                 80 MobSpec records
  bosses.py               5 BossSpec records with their phase machines
  ores.py                 44 OreSpec records
  gear.py                 10 tool sets, 10 armour sets, 5 artefacts
  structures.py           115 StructureSpec records

tools/pixelart/         hand-authored pixel matrices (glyph maps + palettes)
tools/png_codec.py      dependency-free RGBA PNG encoder/decoder
tools/nbt_codec.py      dependency-free NBT writer/reader for structure templates

        │  generators, run in this order
        ▼
tools/registry.py             derives the block/item/entity id sets, writes the manifest
tools/generate_textures.py    684 PNG
tools/generate_resources.py   blockstates, models, loot, recipes, tags, lang, mods.toml
tools/generate_worldgen.py    biomes, features, dimensions, structures, biome tags
tools/generate_structures.py  115 NBT templates (reads the pools worldgen emitted)
tools/generate_geckolib.py    22 geo/animation rigs
tools/generate_java.py        init/BUContent.java — the table Java loops over

        ▼
tools/validate.py             offline closure checks over everything above
```

To regenerate everything:

```bash
python3 tools/registry.py --write
python3 tools/generate_textures.py
python3 tools/generate_resources.py
python3 tools/generate_worldgen.py
python3 tools/generate_structures.py
python3 tools/generate_geckolib.py
python3 tools/generate_java.py
python3 tools/validate.py
```

Order matters in two places: `generate_structures.py` reads the template pools
that `generate_worldgen.py` emits, and `validate.py` must run last because it
checks the union of everything.

### The Java side

`BUContent.java` is generated and is the single table the registries loop over.
Rather than thousands of `RegistryObject` fields, the mod registers content in
loops keyed by `Map<String, RegistryObject<...>>`.

That is why there are only **28 Java classes for 140 biomes and 85 creatures**:

- `BUCreature` backs all 80 species. Each is its own `EntityType` — own id, own
  spawn egg, own attributes, own loot table — but they share one class and are
  parameterised by their generated `MobData` row.
- `BUBoss` backs all five bosses as a phase state machine driven by `BossData`.
- `BUBlocks` registers all 264 blocks by kind; `BUItems` all 546 item
  registrations; one `GeoModel`/`GeoEntityRenderer` pair resolves rig and texture
  by species id.
- Biomes, dimensions and structures are data-driven: Java holds only the
  `ResourceKey`s, and the objects come from the datapack JSON.

Adding a species, a biome or a structure is a change to `tools/content/`, not to
Java. See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).

### Why TerraBlender for Overworld biomes

1.20.1 chooses an Overworld biome by sampling a fixed list of climate parameter
points built inside `MultiNoiseBiomeSourceParameterList.Preset.OVERWORLD`. That
list is not exposed for extension, and no datapack can append to it — so a biome
can be registered, fully authored, and still never appear in a world.

`BUOverworldRegion` contributes the 80 biomes through TerraBlender's
`VanillaParameterOverlayBuilder`, which **overlays** our points onto vanilla's
rather than replacing the list. Vanilla biomes keep generating exactly as before,
and because Biomes O' Plenty and Oh The Biomes You've Gone use the same hook,
this mod coexists with them instead of competing for the same climate space.

`BUOverworldSurfaceRules` registers the matching surface rules, gated per biome
with `SurfaceRules.isBiome`. Without that gate our stones would bleed into
vanilla biomes and into every other mod's biomes too.

---

## Continuous integration

[`.github/workflows/build.yml`](.github/workflows/build.yml) runs two jobs.

**validate** — fast and JVM-free. Regenerates textures, resources, worldgen,
templates, rigs and the Java table, then **fails if the result differs from what
is committed**. That catches the drift that matters most: an edited content table
with uncommitted generated output. Then runs `tools/registry.py` and
`tools/validate.py`.

**build** — installs JDK 17 and Gradle 8.1.1 and compiles with ForgeGradle,
uploading the jar. On failure, [`tools/ci_report.py`](tools/ci_report.py)
republishes javac's `file:line: error:` diagnostics and Gradle's *What went
wrong* block as check-run annotations.

That reporter exists because Actions serves job logs and artifacts from blob
hosts that are not reachable from every development environment. Annotations are
readable through the ordinary REST API, so a red build stays diagnosable without
log access — which is what makes a fix-compile-push loop possible.

---

## Validation

`tools/validate.py` is the offline equivalent of launching the game. It exits
non-zero on any error and currently checks:

- every JSON parses and every PNG decodes
- every texture reference resolves to a file that exists
- registry closure: every block has a blockstate, model and loot table; every
  item and block item has a model; every loot reference resolves
- **registration uniqueness** — no id registered twice in one registry, which is
  a `RegistryException` crash at launch that compiles cleanly
- worldgen closure: every biome, feature, structure, template pool and dimension
  reference resolves, and every spawn names a registered entity
- **biome placement** — every biome is reachable by a biome source, which is a
  separate question from being defined
- GeckoLib closure: every rig exists, and every animation clip a species or boss
  phase declares is actually defined
- **structure templates decode**: all 115 NBT files parse, carry DataVersion
  3465, keep every block inside their declared size, and name only registered
  blocks
- audio: nothing references a sound that has no `.ogg`
- **particles**: every registered particle type has a sprite descriptor and a
  texture, and every biome that names one names a registered type — a
  `registerSpriteSet` call with no `particles/<id>.json` is a load-time error
- **fluid render layers**: every registered liquid is given a translucent layer
  from an `FMLClientSetupEvent` handler on the mod bus, since Forge defaults an
  unregistered fluid to `RenderType.solid()` and it then renders opaque
- **GeckoLib rigs**: every bone an animation channel names exists in the geo, and
  every bone in the geo is animated, so nothing renders frozen or waves a limb
  that is not there
- **atlas coverage**: every cube face of every rig lands inside its texture and
  samples at least one opaque pixel — 546 faces across 85 atlases
- **pixel-art glyph geometry**: every authored glyph is the rectangle the atlas
  layout says it is, which is what stops a ragged row from being silently padded
  into a blank band
- **entity coverage**: every registered entity has attributes and a renderer
- **armour slot ordering**: defence values reach the slot they were authored for,
  which depends on `ArmorItem.Type` running BOOTS, LEGGINGS, CHESTPLATE, HELMET
- **blockstate properties**: every property a block declares is enumerated in its
  blockstate, and nothing enumerates a property the block does not have
- **ore uses**: every ore reaches the player through the shipped data, and every
  use it declares is either realised or reported as a known gap
- translations: every registry entry has a name key and every name key has an
  entry, in both directions

Several of these exist because a real bug was found and then made impossible to
repeat. See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for the full list.

---

## Known gaps

Recorded rather than hidden, because each is checked by the validator and
reported on every run.

**No audio ships.** 29 sound ids are authored and registered — eight biome music
tracks, sixteen ambience tracks and the five boss themes — but there are no
`.ogg` files, so biome music, ambience and boss themes are all silent. Composing
and encoding 29 tracks is outside what this pipeline can do.

The integration is complete and gated on the audio existing, so adding it is a
data change with no code edit: drop a track at
`assets/biomesunseen/sounds/music/ethereal.ogg`, re-run the generators, and its
`sounds.json` entry is written, every biome that authored it switches on, and it
is added to the generated table that gates boss playback. Until then nothing
references the missing audio, so there is no log spam.

**Three ore uses have no subsystem.** `OreSpec.uses` records what an ore is meant
to be spent on, but nothing in the pipeline consumes the field, so it is checked
against the shipped data instead. Twenty ores declare `device`, eighteen `potion`
and four `currency`; none of the three can be delivered, because there are no
block entities or menus for a device, no `MobEffect` or brewing recipe for a
potion, and no villager trade for a currency. Reported as counted notes on every
run, in the same shape as the audio gap.

`tools`, `armor` and `boss` are shipped categories but only partly wired: ten
tool sets and ten armour sets cannot cover forty-four ores, so thirteen ores
declare `tools` and six declare `boss` without a set behind them.

What is enforced is narrower and absolute: **no ore may be a dead end**. All
forty-four reach the player through their mineral block, craftable from and back
into nine of their drop — wiring that was missing for thirty-nine of them until it
was found and fixed.

---

## Repository layout

```
build.gradle, settings.gradle, gradle.properties
src/main/java/com/biomesunseen/
  BiomesUnseen.java          mod entry point
  init/                      registries (BUContent.java is generated)
  block/ item/ entity/       parameterised content classes
  entity/ai/                 goal-token -> vanilla Goal mapping
  client/                    GeckoLib models and renderers
  world/                     TerraBlender region and surface rules
src/main/resources/
  assets/biomesunseen/       textures, models, blockstates, geo, animations, lang
  data/biomesunseen/         worldgen, loot tables, recipes, tags, structures
  data/minecraft/tags/       vanilla worldgen biome tags
tools/                       generators, codecs, content tables, validator
.github/workflows/build.yml  CI
docs/CONTRIBUTING.md         authoring guide
```

## Licence

All Rights Reserved. See `gradle.properties`.
