# -*- coding: utf-8 -*-
"""Procedural PNG texture writer (no PIL dependency).

Writes real, valid PNG files (8-bit RGBA) for block, item and entity textures.
Textures are deterministic 16x16 (or WxH) noise/pattern images so every content
entry ships with its own unique texture file.
"""

import os
import struct
import zlib


def _chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(
        ">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


def write_png(path, pixels, width, height):
    """pixels: list of rows, each row a list of (r, g, b, a) tuples."""
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # filter type 0
        for x in range(width):
            r, g, b, a = pixels[y][x]
            raw.extend((r & 0xFF, g & 0xFF, b & 0xFF, a & 0xFF))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n"
           + _chunk(b"IHDR", ihdr)
           + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + _chunk(b"IEND", b""))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(png)


def _hash_noise(x, y, seed):
    n = (x * 374761393 + y * 668265263 + seed * 1274126177) & 0xFFFFFFFF
    n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFF)


def _lerp(a, b, t):
    return a + (b - a) * t


def _shade(color, factor):
    r = (color >> 16) & 0xFF
    g = (color >> 8) & 0xFF
    b = color & 0xFF
    return (max(0, min(255, int(r * factor))),
            max(0, min(255, int(g * factor))),
            max(0, min(255, int(b * factor))),
            255)


def ore_texture(base_color, spark_color, seed, stone_base=0x7A7A7A):
    """Stone background with mineral inclusions of base/spark colors."""
    rows = []
    for y in range(16):
        row = []
        for x in range(16):
            n = _hash_noise(x, y, seed)
            f = 0.82 + (n / 255.0) * 0.36
            px = _shade(stone_base, f)
            m = _hash_noise(x * 3 + 1, y * 3 + 7, seed + 91)
            if m > 170:
                px = _shade(base_color, 0.75 + (n / 255.0) * 0.5)
            elif m > 150:
                px = _shade(spark_color, 0.9 + (n / 255.0) * 0.3)
            row.append(px)
        rows.append(row)
    return rows


def block_texture(color, seed, style="noise"):
    rows = []
    for y in range(16):
        row = []
        for x in range(16):
            n = _hash_noise(x, y, seed)
            f = 0.78 + (n / 255.0) * 0.44
            if style == "brick":
                mortar = (y % 8 == 0) or ((x + (4 if (y // 8) % 2 else 0)) % 8 == 0)
                if mortar:
                    f *= 0.62
            elif style == "plank":
                if y % 4 == 3:
                    f *= 0.68
                f *= 0.92 + ((x * 7 + seed) % 5) * 0.03
            elif style == "glass":
                edge = x in (0, 15) or y in (0, 15) or (x + y) % 14 == 0
                if edge:
                    f = min(1.35, f * 1.4)
            elif style == "cross":
                pass
            row.append(_shade(color, f))
        rows.append(row)
    return rows


def item_texture(color, seed, shape="blob"):
    rows = []
    for y in range(16):
        row = []
        for x in range(16):
            dx, dy = x - 7.5, y - 7.5
            d = (dx * dx + dy * dy) ** 0.5
            inside = d < 6.2 if shape == "blob" else (
                2 <= x <= 13 and 2 <= y <= 13 if shape == "ingot" else
                ((dx / 4.8) ** 2 + (dy / 6.8) ** 2) < 1.0 if shape == "egg" else
                (abs(dx) + abs(dy) < 7.0))
            if inside:
                n = _hash_noise(x, y, seed)
                f = 0.8 + (n / 255.0) * 0.5
                row.append(_shade(color, f))
            else:
                row.append((0, 0, 0, 0))
        rows.append(row)
    return rows


def entity_texture(color, seed, accent):
    """32x32 mob skin: base body noise with accent banding."""
    rows = []
    for y in range(32):
        row = []
        for x in range(32):
            n = _hash_noise(x, y, seed)
            f = 0.8 + (n / 255.0) * 0.4
            if (y // 4 + x // 8) % 2 == 0 and n > 96:
                row.append(_shade(accent, f))
            else:
                row.append(_shade(color, f))
        rows.append(row)
    return rows


def particle_texture(color):
    rows = []
    for y in range(8):
        row = []
        for x in range(8):
            dx, dy = x - 3.5, y - 3.5
            if dx * dx + dy * dy <= 10.0:
                row.append(_shade(color, 1.0))
            else:
                row.append((0, 0, 0, 0))
        rows.append(row)
    return rows


def gui_icon_texture(color, seed):
    rows = []
    for y in range(16):
        row = []
        for x in range(16):
            n = _hash_noise(x, y, seed)
            edge = x in (0, 15) or y in (0, 15)
            f = 0.6 if edge else 0.85 + (n / 255.0) * 0.4
            row.append(_shade(color, f))
        rows.append(row)
    return rows
