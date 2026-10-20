#!/usr/bin/env python3
"""
gen_audio.py -- mint the silent Ogg Vorbis placeholder behind every sound id.

The mod registers 29 SoundEvents: eight biome/dimension music tracks, sixteen
ambience tracks and five boss themes. None of them shipped audio, so the
generators emitted no sounds.json, no biome named a track, and BUSounds.hasAudio
gated every playback site off. That is correct behaviour for audio that does not
exist -- declaring an entry whose file is missing turns a silent SoundEvent into
a resource-load error naming a missing file, for every player, on every load --
but it also meant the whole audio path was untested and unexercised, and that a
composer replacing a track later had no file to replace.

This mints a valid, silent, one-second Ogg Vorbis file at each of the 29 paths
the pipeline expects. With those in place the existing gating switches
everything on with no code edit anywhere:

    generate_worldgen.py   each biome's JSON gains its music / ambient_sound
    generate_resources.py  sounds.json declares all 29 with the right category
                           and stream flag
    generate_java.py       SOUNDS_WITH_AUDIO fills in, so hasAudio() returns true
                           and boss themes and biome music actually start

The game then loads cleanly and plays silence, which is the honest state: the
wiring is live and verified end to end, and the only thing missing is the
recording. See docs/AUDIO.md for the replacement checklist, which lists every id,
its exact path, the biomes or boss it serves, and the intended vibe.

Two constraints shaped this script.

Minecraft 1.20.1 decodes audio with a Vorbis decoder reading an Ogg container,
so a .wav placeholder is not a substitute -- it would sit in the pack unused, or
worse, be declared and fail to decode. Ogg Vorbis needs a real encoder: the
container framing is simple, but the setup header carries the codebooks, and
there is no way to author those by hand the way png_codec.py authors a PNG. So
encoding is delegated to libsndfile through the soundfile package, and that
import is lazy -- this module is imported by validate.py, which must keep running
in CI where no audio library is installed.

Verification is not delegated. Every file, whether just minted or already
committed, is parsed here by a pure-Python Ogg page walker that checks the
capture pattern, the version, the three Vorbis header packets, the identification
header fields and framing bit, and the final granule position. A library that
wrote a truncated or non-Vorbis file would be caught rather than trusted.

Because encoder output is not guaranteed byte-identical across libsndfile
versions, existing valid files are left untouched: re-running is idempotent and
cannot churn committed bytes into a spurious CI drift failure. This script is
deliberately NOT part of the regenerate-and-compare chain in CI for the same
reason -- the .ogg files are committed artefacts, and the deterministic
generators that read them are what CI reproduces. Use --force to re-mint.
"""

import argparse
import os
import struct
import sys
from typing import Dict, List, Optional, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

MODID = "biomesunseen"
ASSETS_ROOT = os.path.join(ROOT, "src", "main", "resources", "assets", MODID)

# Authored placeholder length. One second is enough to prove the whole decode
# path works and keeps 29 files to a few kilobytes each; a real track replaces it
# wholesale. Music is declared with "stream": true, so a longer file streams
# rather than loading into memory up front.
DURATION_SECONDS = 1.0
SAMPLE_RATE = 44100
CHANNELS = 1

OGG_CAPTURE = b"OggS"
PAGE_HEADER_SIZE = 27


# --------------------------------------------------------------------------- #
#  Which sounds exist, and where their audio goes
# --------------------------------------------------------------------------- #

def sound_ids() -> List[str]:
    """
    Every sound id the mod registers, derived exactly as generate_java.py does.

    Taken from the content tables rather than hand-listed, so a biome or boss
    authored with a new track gets a placeholder on the next run and this script
    cannot drift out of agreement with BUContent.SOUNDS.
    """
    from content import biomes as BIOMES
    from content import bosses as BOSSES

    music = {b.music.split(":")[-1] for b in BIOMES.ALL_BIOMES if b.music}
    ambient = {b.ambient_sound.split(":")[-1]
               for b in BIOMES.ALL_BIOMES if b.ambient_sound}
    boss_music = {b.music.split(":")[-1] for b in BOSSES.ALL_BOSSES if b.music}
    return sorted(music | ambient | boss_music)


def ogg_path(sound_id: str) -> str:
    """
    The .ogg a sound id resolves to, by the pipeline's one shared convention.

    "music.ethereal" -> sounds/music/ethereal.ogg, and a dotted boss id nests one
    level deeper: "music.boss.the_unraveling" -> sounds/music/boss/the_unraveling
    .ogg. generate_java.py, generate_resources.py, generate_worldgen.py and
    validate.py all build this same path, so a track dropped in here is found by
    every one of them.
    """
    bare = sound_id.split(":")[-1]
    return os.path.join(ASSETS_ROOT, "sounds", bare.replace(".", os.sep) + ".ogg")


# --------------------------------------------------------------------------- #
#  Pure-Python Ogg Vorbis verification
# --------------------------------------------------------------------------- #

def parse_ogg(data: bytes) -> Tuple[List[dict], List[str]]:
    """
    Walk the Ogg page structure. Returns (pages, problems).

    Each page is 27 bytes of header, a segment table, then a body whose length is
    the sum of that table. Walking it this way is what distinguishes a real
    container from a file that merely starts with OggS: a truncated or corrupted
    stream desynchronises and either runs off the end or lands on bytes that are
    not a capture pattern.
    """
    problems: List[str] = []
    pages: List[dict] = []
    if len(data) < PAGE_HEADER_SIZE:
        return pages, [f"file is {len(data)} bytes, shorter than one page header"]
    if data[:4] != OGG_CAPTURE:
        return pages, [f"bad capture pattern {data[:4]!r}, expected {OGG_CAPTURE!r}"]

    offset = 0
    while offset < len(data):
        if data[offset:offset + 4] != OGG_CAPTURE:
            problems.append(f"lost page sync at byte {offset}: {data[offset:offset + 4]!r}")
            break
        if offset + PAGE_HEADER_SIZE > len(data):
            problems.append(f"page at byte {offset} has a truncated header")
            break
        version = data[offset + 4]
        if version != 0:
            problems.append(f"page at byte {offset} has stream version {version}, expected 0")
        header_type = data[offset + 5]
        granule = struct.unpack("<q", data[offset + 6:offset + 14])[0]
        serial = struct.unpack("<I", data[offset + 14:offset + 18])[0]
        sequence = struct.unpack("<I", data[offset + 18:offset + 22])[0]
        segment_count = data[offset + 26]
        table_end = offset + PAGE_HEADER_SIZE + segment_count
        if table_end > len(data):
            problems.append(f"page {sequence} has a truncated segment table")
            break
        segment_table = data[offset + PAGE_HEADER_SIZE:table_end]
        body_size = sum(segment_table)
        body_end = table_end + body_size
        if body_end > len(data):
            problems.append(f"page {sequence} declares {body_size} body bytes but the "
                            f"file ends {body_end - len(data)} bytes short")
            break
        pages.append({
            "header_type": header_type,
            "granule": granule,
            "serial": serial,
            "sequence": sequence,
            "segments": segment_count,
            "body": data[table_end:body_end],
        })
        offset = body_end

    if not problems and not pages:
        problems.append("no pages parsed")
    return pages, problems


def verify_ogg_vorbis(path: str) -> Tuple[bool, List[str], Dict[str, object]]:
    """
    Check a file is a complete, decodable-shaped Ogg Vorbis stream.

    Structural only -- this cannot listen. It confirms the container framing, the
    presence of all three Vorbis header packets (identification, comment, and the
    setup packet carrying the codebooks, without which nothing can decode), the
    identification header's own fields including the framing bit the spec requires
    to be 1, and a final granule position that implies a non-zero duration.

    Returns (ok, problems, info).
    """
    problems: List[str] = []
    info: Dict[str, object] = {}
    if not os.path.isfile(path):
        return False, ["file does not exist"], info
    with open(path, "rb") as handle:
        data = handle.read()
    info["bytes"] = len(data)
    if not data:
        return False, ["file is empty"], info

    pages, page_problems = parse_ogg(data)
    problems.extend(page_problems)
    if not pages:
        return False, problems, info
    info["pages"] = len(pages)

    serials = {p["serial"] for p in pages}
    if len(serials) > 1:
        problems.append(f"{len(serials)} distinct stream serials in one file")

    stream = b"".join(p["body"] for p in pages)

    # The three header packets. Search the concatenated stream rather than
    # assuming one packet per page: a comment and a setup header legitimately
    # share a page, which is what libsndfile writes.
    for byte, name in ((b"\x01vorbis", "identification"),
                       (b"\x03vorbis", "comment"),
                       (b"\x05vorbis", "setup")):
        if byte not in stream:
            problems.append(f"no Vorbis {name} header packet")

    ident = stream.find(b"\x01vorbis")
    if ident >= 0:
        if len(stream) < ident + 30:
            problems.append("identification header is truncated")
        else:
            version = struct.unpack("<I", stream[ident + 7:ident + 11])[0]
            channels = stream[ident + 11]
            rate = struct.unpack("<I", stream[ident + 12:ident + 16])[0]
            bitrate_nominal = struct.unpack("<i", stream[ident + 20:ident + 24])[0]
            framing = stream[ident + 29] & 1
            info.update(channels=channels, sample_rate=rate,
                        bitrate_nominal=bitrate_nominal)
            if version != 0:
                problems.append(f"Vorbis version {version}, expected 0")
            if channels < 1:
                problems.append(f"channel count is {channels}")
            if rate <= 0:
                problems.append(f"sample rate is {rate}")
            if framing != 1:
                problems.append("identification header framing bit is 0; the spec "
                                "requires 1 and decoders reject the stream without it")

    # Audio packets follow the headers. A stream that is all headers has no
    # samples and nothing to play.
    final_granule = max((p["granule"] for p in pages), default=0)
    rate_value = int(info.get("sample_rate") or SAMPLE_RATE)
    if final_granule <= 0:
        problems.append("final granule position is not positive, so the stream "
                        "carries no samples")
    else:
        info["duration"] = round(final_granule / float(rate_value), 4)

    if not (pages[0]["header_type"] & 0x02):
        problems.append("first page is not marked beginning-of-stream")
    if not (pages[-1]["header_type"] & 0x04):
        problems.append("last page is not marked end-of-stream, so the file is "
                        "truncated")

    return not problems, problems, info


def is_silent(path: str) -> Optional[bool]:
    """
    Whether a placeholder decodes to true silence, if a decoder is available.

    Returns None when soundfile is not installed, which is the case in CI: the
    structural check above still runs there, and silence is a property of what
    this script writes rather than something a committed file could silently lose.
    """
    try:
        import soundfile
    except ImportError:
        return None
    try:
        samples, _ = soundfile.read(path, dtype="float64", always_2d=False)
    except Exception:
        return None
    peak = 0.0
    for value in (samples.flatten() if hasattr(samples, "flatten") else samples):
        magnitude = abs(float(value))
        if magnitude > peak:
            peak = magnitude
    return peak == 0.0


# --------------------------------------------------------------------------- #
#  Minting
# --------------------------------------------------------------------------- #

def mint(path: str) -> Tuple[bool, str]:
    """
    Write DURATION_SECONDS of digital silence as Ogg Vorbis at `path`.

    All-zero samples at 44100 Hz mono. Silence encodes to a few kilobytes because
    Vorbis spends almost nothing on a frame with no signal; nearly all of the file
    is the setup packet's codebooks, which is also why the placeholder cannot be
    hand-written.
    """
    try:
        import soundfile
    except ImportError:
        return False, ("the soundfile package is not installed, so no Vorbis "
                       "encoder is available")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    # A flat sequence is mono by definition; soundfile takes the channel count
    # from the shape of the data and has no `channels` argument of its own.
    frames = [0.0] * int(SAMPLE_RATE * DURATION_SECONDS)
    assert CHANNELS == 1, "interleave the frames as tuples for more than one channel"
    try:
        soundfile.write(path, frames, SAMPLE_RATE, format="OGG", subtype="VORBIS")
    except Exception as exc:
        return False, f"encoder failed: {exc}"
    return True, "written"


# --------------------------------------------------------------------------- #

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Mint silent Ogg Vorbis placeholders for every authored sound id.")
    parser.add_argument("--force", action="store_true",
                        help="re-mint even where a valid file already exists")
    parser.add_argument("--verify-only", action="store_true",
                        help="check the committed files and change nothing")
    args = parser.parse_args(argv)

    ids = sound_ids()
    if not ids:
        print("[audio] no sound ids resolved from the content tables", file=sys.stderr)
        return 1

    written = skipped = invalid = 0
    total_bytes = 0
    failures: List[str] = []

    for sound_id in ids:
        path = ogg_path(sound_id)
        relative = os.path.relpath(path, ROOT)

        if os.path.isfile(path) and not (args.force and not args.verify_only):
            ok, problems, info = verify_ogg_vorbis(path)
            if ok:
                skipped += 1
                total_bytes += int(info.get("bytes") or 0)
                print(f"  ok       {relative} "
                      f"({info.get('bytes')} B, {info.get('duration')}s, "
                      f"{info.get('sample_rate')} Hz, {info.get('channels')} ch)")
                continue
            if args.verify_only:
                invalid += 1
                failures.append(f"{relative}: " + "; ".join(problems))
                print(f"  INVALID  {relative}: {'; '.join(problems)}")
                continue
            # A committed file that no longer parses is worth replacing rather
            # than reporting, which is what the mint below does.
            failures.append(f"{relative} was invalid and will be re-minted: "
                            + "; ".join(problems))

        if args.verify_only:
            invalid += 1
            failures.append(f"{relative}: missing")
            print(f"  MISSING  {relative}")
            continue

        ok, message = mint(path)
        if not ok:
            invalid += 1
            failures.append(f"{relative}: {message}")
            print(f"  FAILED   {relative}: {message}")
            continue

        ok, problems, info = verify_ogg_vorbis(path)
        if not ok:
            invalid += 1
            failures.append(f"{relative}: encoder wrote a file that fails "
                            f"verification: " + "; ".join(problems))
            print(f"  INVALID  {relative}: {'; '.join(problems)}")
            continue
        written += 1
        total_bytes += int(info.get("bytes") or 0)
        print(f"  minted   {relative} "
              f"({info.get('bytes')} B, {info.get('duration')}s, "
              f"{info.get('sample_rate')} Hz, {info.get('channels')} ch)")

    print(f"\n[audio] {len(ids)} sound id(s): {written} minted, {skipped} already "
          f"valid, {invalid} unusable, {total_bytes} bytes total")

    if failures:
        print("\nProblems:", file=sys.stderr)
        for line in failures:
            print(f"  ! {line}", file=sys.stderr)
        if any("not installed" in f for f in failures):
            print("\n  Install an encoder to mint the placeholders:\n"
                  "      python3 -m pip install --target <dir> soundfile\n"
                  "  then re-run with that directory on PYTHONPATH. Committed\n"
                  "  files need no encoder: they are verified structurally.",
                  file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
