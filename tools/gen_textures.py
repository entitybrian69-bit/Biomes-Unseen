#!/usr/bin/env python3
"""Biomes Unseen texture generator (pure standard library: zlib + struct).

Reads every tools/texdata/*.py module. Each module defines:
    SPRITES = {"block/name": [[cell, ...], ...], ...}
where a cell is "#RRGGBB" or None (transparent). Keys are paths relative to
assets/biomesunseen/textures/ without extension. Output is written as PNG.

Usage:
    python tools/gen_textures.py            write all PNGs
    python tools/gen_textures.py --check    validate matrices only
Runs on desktop Python, Termux, or Pydroid (no Pillow needed).
"""
import importlib.util
import os
import re
import struct
import sys
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXDATA = os.path.join(ROOT, "tools", "texdata")
OUT = os.path.join(ROOT, "src", "main", "resources", "assets", "biomesunseen", "textures")
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def load_sprites():
    sprites = {}
    for fname in sorted(os.listdir(TEXDATA)):
        if not fname.endswith(".py") or fname.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location("texdata_" + fname[:-3], os.path.join(TEXDATA, fname))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for key, rows in mod.SPRITES.items():
            if key in sprites:
                raise SystemExit("duplicate sprite key: " + key)
            sprites[key] = rows
    return sprites


def validate(key, rows):
    if not rows or not rows[0]:
        raise SystemExit("%s: empty matrix" % key)
    width = len(rows[0])
    for y, row in enumerate(rows):
        if len(row) != width:
            raise SystemExit("%s: row %d has %d cells, expected %d" % (key, y, len(row), width))
        for x, cell in enumerate(row):
            if cell is not None and not HEX.match(cell):
                raise SystemExit("%s: bad cell at (%d,%d): %r" % (key, x, y, cell))


def to_rgba(cell):
    if cell is None:
        return (0, 0, 0, 0)
    return (int(cell[1:3], 16), int(cell[3:5], 16), int(cell[5:7], 16), 255)


def chunk(tag, data):
    body = tag + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def write_png(path, rows):
    height, width = len(rows), len(rows[0])
    raw = b"".join(b"\x00" + bytes(v for cell in row for v in to_rgba(cell)) for row in rows)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(png)


def main():
    check_only = "--check" in sys.argv[1:]
    sprites = load_sprites()
    for key, rows in sprites.items():
        validate(key, rows)
        if not check_only:
            write_png(os.path.join(OUT, key + ".png"), rows)
    print("%s %d sprite(s)" % ("validated" if check_only else "wrote", len(sprites)))


if __name__ == "__main__":
    main()
