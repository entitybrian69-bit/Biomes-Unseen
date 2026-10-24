# Biomes Unseen — Audio

All sounds are placeholders: valid, silent Ogg Vorbis files (0.25 s, mono, 22.05 kHz)
written by `tools/gen_audio.py`. The generator reads
`src/main/resources/assets/biomesunseen/sounds.json` and writes one file per entry,
so adding a sound means adding it to `sounds.json` and `ModSounds.java`, then re-running the script.

## Sound events (41)

| Event id | File (under `assets/biomesunseen/sounds/`) |
|---|---|
| `hollow_stalker.ambient` / `.hurt` / `.death` | `mob/hollow_stalker/{ambient,hurt,death}.ogg` |
| `sporeling.ambient` / `.hurt` / `.death` | `mob/sporeling/{ambient,hurt,death}.ogg` |
| `gloom_crawler.ambient` / `.hurt` / `.death` | `mob/gloom_crawler/{ambient,hurt,death}.ogg` |
| `crystal_golem.ambient` / `.hurt` / `.death` | `mob/crystal_golem/{ambient,hurt,death}.ogg` |
| `mire_wraith.ambient` / `.hurt` / `.death` | `mob/mire_wraith/{ambient,hurt,death}.ogg` |
| `heart_of_the_forest.ambient` / `.hurt` / `.death` | `mob/heart_of_the_forest/{ambient,hurt,death}.ogg` |
| `heart_of_the_forest.shoot` | `mob/heart_of_the_forest/shoot.ogg` |
| `heart_of_the_forest.phase_shift` | `mob/heart_of_the_forest/phase_shift.ogg` |

### Shared sets for the 80 generated mobs

Generated mobs share one set per archetype, selected in `SpecMobEntity`:

| Event id | File |
|---|---|
| `generic_<archetype>.ambient` / `.hurt` / `.death` | `mob/generic/<archetype>/{ambient,hurt,death}.ogg` |

Archetypes: `biped`, `brute`, `crawler`, `quad`, `floater`, `blob`, `serpent` (21 events).

## Replacing placeholders

1. Export your audio as Ogg Vorbis (mono for positional sounds).
2. Overwrite the file at the same path. Do not rename it unless you also edit `sounds.json`.
3. Run `python tools/validate.py`. It checks the `OggS` and `vorbis` headers of every `.ogg`.

Re-running `gen_audio.py` overwrites every file with silence, so run it only once, before adding real audio.
