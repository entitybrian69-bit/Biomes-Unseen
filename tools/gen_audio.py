#!/usr/bin/env python3
"""Generate original, deterministic Ogg/Vorbis creature and portal sound effects.

The short synthesized clips are distinct by creature archetype and event (ambient,
hurt, death, attack, or gate travel). Install tools/requirements-audio.txt first.
Usage: python tools/gen_audio.py
"""
import hashlib
import json
import os

import numpy as np
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "src", "main", "resources", "assets", "biomesunseen")
NAMESPACE = "biomesunseen"
RATE = 22050

# (fundamental pitch, noise amount, brightness, modulation rate)
PROFILES = {
    "biped": (112.0, 0.15, 0.34, 1.1),
    "brute": (68.0, 0.19, 0.20, 0.7),
    "crawler": (154.0, 0.35, 0.42, 1.8),
    "quad": (96.0, 0.20, 0.30, 1.3),
    "floater": (224.0, 0.31, 0.48, 0.8),
    "blob": (138.0, 0.28, 0.16, 2.4),
    "serpent": (184.0, 0.39, 0.55, 1.0),
}
CUSTOM_PROFILES = {
    "hollow_stalker": "serpent",
    "sporeling": "blob",
    "gloom_crawler": "crawler",
    "crystal_golem": "brute",
    "mire_wraith": "floater",
    "heart_of_the_forest": "brute",
}
DURATIONS = {
    "ambient": 0.90,
    "hurt": 0.34,
    "death": 0.82,
    "shoot": 0.29,
    "phase_shift": 0.72,
    "travel": 0.66,
}


def sound_files():
    with open(os.path.join(ASSETS, "sounds.json"), "r", encoding="utf-8") as fh:
        spec = json.load(fh)
    results = {}
    for event, entry in spec.items():
        for sound in entry["sounds"]:
            name = sound["name"] if isinstance(sound, dict) else sound
            namespace, _, path = name.partition(":")
            if namespace == NAMESPACE:
                results[path] = (event, os.path.join(ASSETS, "sounds", *path.split("/")) + ".ogg")
    return sorted(results.items())


def profile_for(path):
    parts = path.split("/")
    if len(parts) >= 4 and parts[0:2] == ["mob", "generic"]:
        return parts[2] if parts[2] in PROFILES else "biped"
    if len(parts) >= 3 and parts[0] == "mob":
        return CUSTOM_PROFILES.get(parts[1], "biped")
    if parts[0] == "hollow_gate":
        return "floater"
    return "biped"


def seed_for(event, path):
    digest = hashlib.blake2b((event + ":" + path).encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "little")


def synthesize(event, path):
    duration = DURATIONS.get(event.rsplit(".", 1)[-1], 0.55)
    base, noise_level, brightness, pulse_rate = PROFILES[profile_for(path)]
    rng = np.random.default_rng(seed_for(event, path))
    count = int(RATE * duration)
    t = np.arange(count, dtype=np.float64) / RATE
    progress = t / duration
    phase_jitter = rng.uniform(0.0, 2.0 * np.pi)

    if event.endswith(".ambient"):
        frequency = base * (0.86 + 0.08 * np.sin(2.0 * np.pi * 0.7 * t + phase_jitter)
                            + 0.035 * np.sin(2.0 * np.pi * pulse_rate * t))
        envelope = np.sin(np.pi * progress) ** 0.45
        envelope *= 0.42 + 0.46 * (0.5 + 0.5 * np.sin(2.0 * np.pi * pulse_rate * t + phase_jitter))
        noise_scale = 0.52
    elif event.endswith(".hurt"):
        frequency = base * (2.0 - 0.95 * progress) * (1.0 + 0.025 * np.sin(2.0 * np.pi * 9.0 * t))
        envelope = np.exp(-4.2 * progress) * (0.58 + 0.42 * np.sin(np.pi * np.minimum(1.0, progress * 2.2)))
        noise_scale = 1.0
    elif event.endswith(".death"):
        frequency = base * (1.75 - 1.18 * progress) * (1.0 + 0.045 * np.sin(2.0 * np.pi * 3.0 * t))
        envelope = (1.0 - progress) ** 0.58 * (0.72 + 0.28 * np.sin(2.0 * np.pi * pulse_rate * t + phase_jitter))
        noise_scale = 0.86
    elif event.endswith(".shoot"):
        frequency = base * (2.8 - 1.65 * progress) * (1.0 + 0.06 * np.sin(2.0 * np.pi * 13.0 * t))
        envelope = np.exp(-4.8 * progress) * (0.65 + 0.35 * np.sin(np.pi * progress))
        noise_scale = 0.75
    elif event.endswith(".phase_shift"):
        sweep = np.sin(np.pi * progress)
        frequency = base * (0.85 + 1.55 * sweep) * (1.0 + 0.025 * np.sin(2.0 * np.pi * 5.0 * t))
        envelope = np.sin(np.pi * progress) ** 0.65 * (0.7 + 0.3 * np.sin(2.0 * np.pi * 2.2 * t + phase_jitter))
        noise_scale = 0.72
    else:  # Hollow gate travel: rising, then falling resonant sweep.
        frequency = 115.0 + 390.0 * np.sin(np.pi * progress) ** 1.2
        envelope = np.sin(np.pi * progress) ** 0.72
        noise_scale = 0.45

    phase = np.cumsum(frequency, dtype=np.float64) * (2.0 * np.pi / RATE)
    # Soft, inharmonic partials give each archetype a recognizable spectral color.
    tone = (np.sin(phase)
            + (0.30 + brightness * 0.10) * np.sin(phase * 2.01 + 0.37)
            + (0.12 + brightness * 0.18) * np.sin(phase * 3.03 + 1.12)
            + (0.035 + brightness * 0.10) * np.sin(phase * 4.97 + 0.71))
    raw_noise = rng.standard_normal(count)
    smooth_noise = np.convolve(raw_noise, np.ones(13, dtype=np.float64) / 13.0, mode="same")
    texture = (0.72 * raw_noise + 1.4 * smooth_noise) * noise_level * noise_scale
    signal = envelope * (0.66 * tone + 0.32 * texture)

    # Short transient makes damage and attacks read as effects instead of sustained notes.
    if event.endswith((".hurt", ".shoot")):
        transient = np.exp(-np.maximum(0.0, t - 0.012) * 70.0) * (t < 0.12)
        signal += transient * rng.standard_normal(count) * (0.10 if event.endswith(".hurt") else 0.075)
    peak = float(np.max(np.abs(signal)))
    if peak > 0.0:
        signal = signal * (0.72 / peak)
    return np.asarray(np.clip(signal, -0.92, 0.92), dtype=np.float32)


def main():
    files = sound_files()
    if not files:
        raise SystemExit("sounds.json contains no biomesunseen sound files")
    for path, (event, filename) in files:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        sf.write(filename, synthesize(event, path), RATE, format="OGG", subtype="VORBIS")
    print("generated %d original Ogg/Vorbis sound effect(s) at %d Hz" % (len(files), RATE))


if __name__ == "__main__":
    main()
