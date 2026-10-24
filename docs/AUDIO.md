# Biomes Unseen — Audio

The mod now ships with **42 original, procedurally synthesized Ogg/Vorbis effects** at 22.05 kHz mono. The deterministic generator creates different short ambient, hurt, death, boss-attack, and portal-travel effects; creature archetypes have distinct pitch and noise profiles. These are custom synth effects, not recorded voices or licensed stock clips.

`tools/gen_audio.py` reads `src/main/resources/assets/biomesunseen/sounds.json` and writes one `.ogg` per referenced sound. To regenerate them, first install the pinned dependencies with `python -m pip install -r tools/requirements-audio.txt`, then run `python tools/gen_audio.py` (or `python tools/gen_all.py`). Re-running the generator overwrites the audio files.

## Sound events

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
| `hollow_gate.travel` | `hollow_gate/travel.ogg` |

### Shared sets for the 80 generated mobs

Generated mobs share one sound set per archetype, selected in `SpecMobEntity`:

| Event id | File |
|---|---|
| `generic_<archetype>.ambient` / `.hurt` / `.death` | `mob/generic/<archetype>/{ambient,hurt,death}.ogg` |

Archetypes: `biped`, `brute`, `crawler`, `quad`, `floater`, `blob`, `serpent` (21 events).

## Replacing or checking effects

1. Replace a generated `.ogg` with your own Ogg/Vorbis file at the same path. Do not rename it unless you also edit `sounds.json`.
2. Run `python tools/validate.py` with the audio requirements installed. The validator checks Ogg/Vorbis headers, decodes each file, verifies mono/22.05 kHz format, and rejects silent or clipped output.
3. Avoid running `gen_audio.py` afterward unless you intend to restore the synthesized versions.
