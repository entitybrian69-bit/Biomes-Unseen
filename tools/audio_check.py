"""Ogg/Vorbis header, decode, level, and sounds.json consistency checks."""
import glob
import json
import os


def check_audio_files(assets, namespace, relative_path):
    errors, warnings = [], []
    sounds_path = os.path.join(assets, "sounds.json")
    files = glob.glob(os.path.join(assets, "sounds", "**", "*.ogg"), recursive=True)
    try:
        import soundfile as sf
    except ImportError:
        sf = None
    for path in files:
        with open(path, "rb") as stream:
            header = stream.read(64)
        if header[:4] != b"OggS" or b"\x01vorbis" not in header:
            errors.append("%s: missing OggS/vorbis header" % relative_path(path))
        if sf is None:
            continue
        try:
            audio, rate = sf.read(path, dtype="float32")
            rms = float((audio.astype("float64") ** 2).mean() ** 0.5) if audio.size else 0.0
            peak = float(abs(audio).max()) if audio.size else 0.0
            channels = 1 if audio.ndim == 1 else audio.shape[1] if audio.ndim == 2 else 0
            if rate != 22050 or channels != 1:
                errors.append("%s: expected mono 22050 Hz audio, found %d Hz / %d channel(s)" %
                              (relative_path(path), rate, channels))
            if rms < 0.01 or peak < 0.04:
                errors.append("%s: decoded audio is silent or too quiet (RMS %.5f, peak %.5f)" %
                              (relative_path(path), rms, peak))
            if peak > 0.99:
                errors.append("%s: decoded audio clips (peak %.5f)" % (relative_path(path), peak))
        except Exception as exc:
            errors.append("%s: cannot decode audio (%s)" % (relative_path(path), exc))
    if sf is None:
        warnings.append("soundfile unavailable; Ogg headers checked but decoded audio not verified")
    if not os.path.exists(sounds_path):
        errors.append("sounds.json missing")
        return errors, warnings
    with open(sounds_path, encoding="utf-8") as stream:
        sounds = json.load(stream)
    for event, entry in sounds.items():
        for sound in entry["sounds"]:
            name = sound["name"] if isinstance(sound, dict) else sound
            sound_namespace, _, sound_path = name.partition(":")
            target = os.path.join(assets, "sounds", *sound_path.split("/")) + ".ogg"
            if sound_namespace == namespace and not os.path.exists(target):
                warnings.append("sound '%s' has no file yet (run tools/gen_audio.py)" % event)
    return errors, warnings
