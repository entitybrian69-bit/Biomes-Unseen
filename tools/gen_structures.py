#!/usr/bin/env python3
"""Writes the Heart of the Forest boss arena template (gzip NBT, pure standard library).

Output: src/main/resources/data/biomesunseen/structures/heart_arena/arena.nbt
The template is a 21x15x21 mossy-brick arena: solid base (y0-5), floor (y6),
cleared cavity (y7-13), a gapped wall ring, pillars with shroomlight caps, and
the boss entity placed at the centre (spawned once when the structure generates).

Usage: python tools/gen_structures.py
"""
import gzip
import math
import os
import struct

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "src", "main", "resources", "data", "biomesunseen",
                   "structures", "heart_arena", "arena.nbt")

SIZE_X, SIZE_Y, SIZE_Z = 21, 15, 21
CX = CZ = 10
DATA_VERSION = 3465  # Minecraft 1.20.1

# NBT tag ids
T_BYTE, T_INT, T_DOUBLE, T_STRING, T_LIST, T_COMPOUND = 1, 3, 6, 8, 9, 10


def w_str(s):
    raw = s.encode("utf-8")
    return struct.pack(">H", len(raw)) + raw


def p_list(tag_id, payloads):
    return bytes([tag_id]) + struct.pack(">i", len(payloads)) + b"".join(payloads)


def p_compound(fields):
    """fields: list of (tag_id, name, payload)."""
    return b"".join(bytes([t]) + w_str(n) + p for t, n, p in fields) + b"\x00"


def p_int_list(values):
    return p_list(T_INT, [struct.pack(">i", v) for v in values])


def p_double_list(values):
    return p_list(T_DOUBLE, [struct.pack(">d", v) for v in values])


def block_at(x, y, z):
    """Return the palette block name for a cell, or None to leave it out."""
    dx, dz = x - CX, z - CZ
    r = math.hypot(dx, dz)
    h = (x * 7 + y * 13 + z * 17) % 11
    if y <= 5:
        if r <= 10.3:
            return "minecraft:stone_bricks" if h > 2 else "minecraft:cracked_stone_bricks"
        return None
    if y == 6:
        if r > 10.3:
            return None
        if r <= 2.2:
            return "minecraft:chiseled_stone_bricks"
        if r > 8.5:
            return "minecraft:mossy_stone_bricks"
        return "minecraft:moss_block" if h > 3 else "minecraft:mossy_stone_bricks"
    if y <= 13:
        if r > 10.3:
            return None
        on_wall = r > 9.2 and y <= 10
        gate = abs(dx) <= 1 or abs(dz) <= 1
        if on_wall and not gate:
            return "minecraft:mossy_stone_bricks"
        pillar = any(abs(dx - px) < 0.6 and abs(dz - pz) < 0.6 for px, pz in PILLARS)
        if pillar and y <= 11:
            return "minecraft:mossy_stone_brick_wall"
        if pillar and y == 12:
            return "minecraft:shroomlight"
        if r < 9.2:
            return "minecraft:air"
    return None


PILLARS = [(round(6.5 * math.cos(a * math.pi / 4)), round(6.5 * math.sin(a * math.pi / 4))) for a in range(8)]


def build():
    palette, index, blocks = [], {}, []
    for y in range(SIZE_Y):
        for z in range(SIZE_Z):
            for x in range(SIZE_X):
                name = block_at(x, y, z)
                if name is None:
                    continue
                if name not in index:
                    index[name] = len(palette)
                    palette.append(name)
                blocks.append((x, y, z, index[name]))
    palette_payloads = [p_compound([(T_STRING, "Name", w_str(n))]) for n in palette]
    block_payloads = [p_compound([(T_LIST, "pos", p_int_list([x, y, z])), (T_INT, "state", struct.pack(">i", s))])
                      for x, y, z, s in blocks]
    boss_nbt = p_compound([(T_STRING, "id", w_str("biomesunseen:heart_of_the_forest")),
                           (T_BYTE, "PersistenceRequired", b"\x01")])
    entity = p_compound([(T_LIST, "pos", p_double_list([CX + 0.5, 7.0, CZ + 0.5])),
                         (T_LIST, "blockPos", p_int_list([CX, 7, CZ])),
                         (T_COMPOUND, "nbt", boss_nbt)])
    root = p_compound([
        (T_INT, "DataVersion", struct.pack(">i", DATA_VERSION)),
        (T_LIST, "size", p_int_list([SIZE_X, SIZE_Y, SIZE_Z])),
        (T_LIST, "palette", p_list(T_COMPOUND, palette_payloads)),
        (T_LIST, "blocks", p_list(T_COMPOUND, block_payloads)),
        (T_LIST, "entities", p_list(T_COMPOUND, [entity])),
    ])
    return bytes([T_COMPOUND]) + w_str("") + root, len(blocks), len(palette)


def main():
    data, n_blocks, n_palette = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with gzip.open(OUT, "wb") as fh:
        fh.write(data)
    print("wrote %s (%d blocks, %d palette entries)" % (OUT, n_blocks, n_palette))


if __name__ == "__main__":
    main()
