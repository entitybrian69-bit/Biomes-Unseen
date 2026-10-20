# Audio

Every sound the mod registers, where its file goes, and what it is meant to sound
like. This is the replacement checklist: all 29 tracks currently ship as
**silent one-second placeholders**, so the audio path is wired end to end and
verified, but nothing is audible yet.

The placeholders were minted by `tools/gen_audio.py`. Replacing one is a data
change with no code edit anywhere — see [Replacing a track](#replacing-a-track).

---

## Current state

| | |
| --- | --- |
| Registered `SoundEvent`s | 29 |
| Tracks with audio on disk | 29 (all silent placeholders) |
| Tracks that are real recordings | **0** |
| `sounds.json` definitions | 29 (generated) |
| Biomes with music | 140 / 140 |
| Biomes with ambience | 68 / 140 |
| Boss themes | 5 / 5 |

`validate.py` reports the placeholder count as a note on every run, so this gap
cannot quietly close or quietly reopen. The files themselves are parsed as Ogg
Vorbis — capture pattern, page chain, all three header packets, identification
fields and framing bit, final granule — because a file that merely exists at the
right path can still be an MP3 renamed, a Git LFS pointer, or a partial download,
and each of those fails in game rather than in the build.

---

## Format requirements

Minecraft 1.20.1 decodes through a Vorbis decoder reading an Ogg container.
There is no substitute format: a `.wav` at these paths would sit unused, or be
declared and fail to decode.

| | required |
| --- | --- |
| Container / codec | Ogg Vorbis (`.ogg`) |
| Sample rate | 44100 Hz recommended (the engine resamples, but 44.1 avoids it) |
| Channels | mono or stereo; **stereo for music**, mono is fine for ambience |
| Music length | minutes, not seconds — a short track restarts audibly |
| Ambience length | a seamless loop; it repeats continuously while the player is in the biome |
| Loudness | normalise to roughly vanilla's music level; `volume` is already 1.0 |
| Licensing | royalty-free or licensed for redistribution **inside a mod jar** |

The generator declares each track in `sounds.json` automatically:

- `music.*` → `"category": "music"`, `"stream": true`. Streaming matters: these
  are long tracks, and loading them into memory up front would stall world join.
- `ambient.*` → `"category": "ambient"`, `"stream": false`.

Do not hand-edit `sounds.json`; it is generated.

---

## Replacing a track

1. Put the real `.ogg` at the path listed below, overwriting the placeholder.
2. Re-run the generators (`registry.py --write`, then `generate_resources.py`,
   `generate_worldgen.py`, `generate_java.py`).
3. Commit the `.ogg` **and** the regenerated files.
4. `python3 tools/validate.py` — the new file is parsed, and the placeholder note
   drops by one.

Nothing else changes. `BUSounds.hasAudio()` gates playback on the file existing,
`SOUNDS_WITH_AUDIO` is derived from which files are on disk, and every biome that
authored the track already names it.

`tools/gen_audio.py` is idempotent and leaves valid files untouched, so re-running
it will not overwrite a real recording. Use `--verify-only` to check the set
without an encoder installed — structural verification needs no audio library,
only minting does.

---

## Music — 8 tracks

Five serve the Overworld biome categories (16 biomes each), three serve the
dimensions (20 biomes each).

| Sound id | Path | Serves | Intended track |
| --- | --- | --- | --- |
| `music.ethereal` | `sounds/music/ethereal.ogg` | 16 Ethereal biomes — Luminescent Grove, Moonpetal Meadow, Duskwood Hollow | Sparse glass harmonics and a slow celesta over a long reverb tail; weightless, cool-toned, no percussion. Should feel lit from within. |
| `music.ancient` | `sounds/music/ancient.ogg` | 16 Ancient biomes — Petrified Forest, Colossal Boneyard, Sunken Temple Reach | Low sustained strings and a distant frame drum, with a mournful solo woodwind theme. Grand and slow, the sound of something enormous that died a long time ago. |
| `music.vibrant` | `sounds/music/vibrant.ogg` | 16 Vibrant biomes — Primal Savanna, Bloomfield, Coral Shallows | Bright, rhythmic and warm: plucked strings, hand percussion, a major-key flute line. Busier than the other Overworld tracks, with forward motion. |
| `music.harsh` | `sounds/music/harsh.ogg` | 16 Harsh biomes — Volcanic Wasteland, Frozen Expanse, Scorched Glassland | Dissonant drones, metallic scrapes and a sparse deep pulse. Uncomfortable and exposed, with wide empty space between events. |
| `music.aquatic` | `sounds/music/aquatic.ogg` | 16 Aquatic biomes — Abyssal Trench, Kelp Cathedral, Tidal Flats | Muffled and submerged: filtered piano, swelling pads, a slow whale-song-like glide. Everything low-passed, as if heard through water. |
| `music.hollow_deep` | `sounds/music/hollow_deep.ogg` | 20 biomes in **The Hollow Deep** | Oppressive and cavernous. Sub-bass swells, dripping resonance, a faint far-off choir buried under stone. Wonder and dread in equal measure. |
| `music.aetherfall` | `sounds/music/aetherfall.ogg` | 20 biomes in **Aetherfall** | Airy and ascending: shimmering strings, high bells, a rising chord progression that never quite resolves. Should feel like falling upwards. |
| `music.void_between` | `sounds/music/void_between.ogg` | 20 biomes in **The Void Between** | Near-silence with structure: granular static, reversed tones, long unresolved drones. Unsettling, cold, and deliberately unlike any Overworld track. |

---

## Ambience — 16 tracks

Continuous looping beds, not music. Each should be seamless at the loop point and
quiet enough to sit under the music track without competing with it.

| Sound id | Path | Serves | Intended track |
| --- | --- | --- | --- |
| `ambient.wind_low` | `sounds/ambient/wind_low.ogg` | 9 biomes — Megalith Moor, Titan Graveyard, Bronze Steppe | Deep slow wind across open ground, no whistle, faint granular grit carried in the gusts. |
| `ambient.wind_high` | `sounds/ambient/wind_high.ogg` | 10 biomes — Frozen Expanse, Howling Peaks, Grave Ice Field | Thin high-altitude wind with a keening whistle and occasional sharp gusts. Colder and more exposed than `wind_low`. |
| `ambient.ash_wind` | `sounds/ambient/ash_wind.ogg` | 1 biome — Ashen Necropolis | Dry wind carrying particulate: a soft continuous hiss under a low gust, like ash moving across stone. |
| `ambient.ember` | `sounds/ambient/ember.ogg` | 5 biomes — Pyroclast Fields, Volcanic Wasteland, Sulphur Vents | Low fire roar with irregular crackle and popping, plus a faint heat-shimmer rumble beneath. |
| `ambient.storm` | `sounds/ambient/storm.ogg` | 1 biome — Stormcell Spire | Distant rolling thunder with heavy rain and a continuous electrical hum; thunder far enough away to never startle. |
| `ambient.drip` | `sounds/ambient/drip.ogg` | 2 biomes — Glowcap Grotto, Weeping Galleries | Cave drips at irregular intervals with a long wet reverb tail and a low cavernous bed. |
| `ambient.tremor` | `sounds/ambient/tremor.ogg` | 2 biomes — Tremor Ward, Hollow Core | Periodic deep sub-bass shudders, like stone shifting far below, over a continuous low rumble. |
| `ambient.hymn` | `sounds/ambient/hymn.ogg` | 2 biomes — Hymn Halls, Crown Apex | A distant wordless choir sustained in a huge stone space. Should sound like it has a source somewhere you cannot reach. |
| `ambient.whisper` | `sounds/ambient/whisper.ogg` | 2 biomes — Whispering Mire, Ghostlight Marsh | Layered breath-like voices just below intelligibility, panned wide, over a soft marsh drone. |
| `ambient.blight` | `sounds/ambient/blight.ogg` | 4 biomes — Blighted Marches, Witherwood, Blackwater Bog | Sickly wet decay: bubbling mud, occasional dry crackle, a low dissonant hum. |
| `ambient.static` | `sounds/ambient/static.ogg` | 5 biomes — Static Wastes, Null Sea, Unraveling Nexus | Broadband electrical static with rhythmic dropouts and faint tonal artifacts, like a signal failing. |
| `ambient.deep_water` | `sounds/ambient/deep_water.ogg` | 7 biomes — Abyssal Trench, Sunken Cathedral, Leviathan Graveyard | Heavy submerged pressure drone, muffled movement, occasional distant metallic creak. |
| `ambient.underwater` | `sounds/ambient/underwater.ogg` | 6 biomes — Jewel Reef, Kelp Cathedral, Flooded Ruins | Close underwater bed: bubble streams, filtered movement, light and warmer than `deep_water`. |
| `ambient.surf` | `sounds/ambient/surf.ogg` | 6 biomes — Monolith Shore, Coral Shallows, Orchid Lagoon | Regular waves breaking on a shore, with wet sand draw-back between sets. |
| `ambient.stream` | `sounds/ambient/stream.ogg` | 4 biomes — River of Lights, Brine Marsh, Mangrove Labyrinth | Continuous shallow flowing water over stones, brighter and faster than surf. |
| `ambient.rapids` | `sounds/ambient/rapids.ogg` | 2 biomes — Whitewater Gorge, Geyser Lagoon | Loud fast whitewater with a strong low-end roar and irregular splashing. |

---

## Boss themes — 5 tracks

One per boss, started on sighting and gated on `BossData.music` plus
`BUSounds.hasAudio()`. These should be the loudest and most structured audio in
the mod, and should read as *combat* music rather than ambience. Each boss has
four phases; a track with distinct sections that can be read as escalation will
land far better than a flat loop.

| Sound id | Path | Boss | Intended track |
| --- | --- | --- | --- |
| `music.boss.heart_of_the_forest` | `sounds/music/boss/heart_of_the_forest.ogg` | **The Heart of the Forest** (Overworld) | Heavy rhythmic drums and somber strings, with a wooden, organic percussion layer — root and timber rather than metal. Ancient and defensive, not evil. |
| `music.boss.warden_of_the_hollow_deep` | `sounds/music/boss/warden_of_the_hollow_deep.ogg` | **Warden of the Hollow Deep** (The Hollow Deep) | Grinding low brass and sub-bass pulses under a tolling bell, with stone-on-stone percussion. Immense, patient, and crushing. |
| `music.boss.the_skyward_crown` | `sounds/music/boss/the_skyward_crown.ogg` | **The Skyward Crown** (Aetherfall) | Soaring brass and rapid high strings over driving timpani; regal and triumphant with an edge of menace. Should feel like an ascent. |
| `music.boss.void_serpent` | `sounds/music/boss/void_serpent.ogg` | **The Void Serpent** (The Void Between) | Slithering chromatic strings and a hissing percussive bed, with sudden silent gaps before a strike. Predatory and quick. |
| `music.boss.the_unraveling` | `sounds/music/boss/the_unraveling.ogg` | **The Unraveling** (The Void Between) | The most abrasive track in the mod: detuned tones, granular static, rhythmic collapse and rebuild. Reality coming apart, with a pulse underneath that never settles. |

---

## Why the placeholders exist

Registering a `SoundEvent` whose id has no `sounds.json` definition is harmless,
but *starting* it makes the client log `Unable to play unknown soundEvent` — for
boss music that is once per sighting, and for biome music every 12–24 seconds per
player, in every biome that authored a track. Before the placeholders existed,
playback was gated off entirely, which was correct but meant the whole audio path
was untested and there was no file for a composer to replace.

Silent real files are the better state: the gating is on, `sounds.json` is
declared, all 140 biomes reference their tracks, boss themes start on sighting,
and the game loads and plays without a single error. What is missing is the
recording, and only the recording.

Composing and encoding 29 real tracks is outside what this pipeline can do —
there is no encoder available in the sandbox, and `gen_audio.py` delegates to
libsndfile through the `soundfile` package purely to mint the silence. That import
is lazy so the validator can keep parsing committed files in CI, where no audio
library is installed.
