#!/usr/bin/env python3
"""
nbt_codec.py -- a dependency-free NBT writer for Minecraft structure templates.

Structure templates are the binary .nbt files a jigsaw pool places. They cannot
be JSON, so without a writer every one of the mod's 115 structures would
reference a template that does not exist and the pool would place nothing --
the structure would simply never appear in a world, with no error at build time.

NBT is big-endian, self-describing and gzip-compressed on disk. The format is
small enough to encode directly, which keeps the repository free of a binary
build dependency and lets templates be regenerated from source like every other
asset here.

Values are passed as explicit tagged tuples rather than bare Python objects,
because NBT distinguishes types Python does not: a block palette index is an Int
but a coordinate inside a List must also be declared Int, and guessing from the
Python type would silently emit a Short where the game reads an Int.

    ("byte", 1)  ("short", 2)  ("int", 3)  ("long", 4)
    ("float", 1.0)  ("double", 2.0)  ("string", "x")
    ("int_array", [1, 2])
    ("list", "int", [("int", 1), ("int", 2)])
    ("compound", {"Name": ("string", "minecraft:stone")})
"""

from __future__ import annotations

import gzip
import struct
from typing import Dict, List, Sequence, Tuple

TAG_END = 0
TAG_BYTE = 1
TAG_SHORT = 2
TAG_INT = 3
TAG_LONG = 4
TAG_FLOAT = 5
TAG_DOUBLE = 6
TAG_BYTE_ARRAY = 7
TAG_STRING = 8
TAG_LIST = 9
TAG_COMPOUND = 10
TAG_INT_ARRAY = 11
TAG_LONG_ARRAY = 12

TYPE_IDS: Dict[str, int] = {
    "end": TAG_END,
    "byte": TAG_BYTE,
    "short": TAG_SHORT,
    "int": TAG_INT,
    "long": TAG_LONG,
    "float": TAG_FLOAT,
    "double": TAG_DOUBLE,
    "byte_array": TAG_BYTE_ARRAY,
    "string": TAG_STRING,
    "list": TAG_LIST,
    "compound": TAG_COMPOUND,
    "int_array": TAG_INT_ARRAY,
    "long_array": TAG_LONG_ARRAY,
}

# 1.20.1. A template written with the wrong DataVersion is upgraded (or rejected)
# by the game on load, so this must track the target Minecraft version.
DATA_VERSION_1_20_1 = 3465


def _named(name: str) -> bytes:
    """A length-prefixed UTF-8 tag name."""
    raw = name.encode("utf-8")
    return struct.pack(">H", len(raw)) + raw


def encode_payload(value: Tuple) -> bytes:
    """Encode one tagged value's payload, without its type byte or name."""
    kind = value[0]
    if kind == "byte":
        return struct.pack(">b", int(value[1]))
    if kind == "short":
        return struct.pack(">h", int(value[1]))
    if kind == "int":
        return struct.pack(">i", int(value[1]))
    if kind == "long":
        return struct.pack(">q", int(value[1]))
    if kind == "float":
        return struct.pack(">f", float(value[1]))
    if kind == "double":
        return struct.pack(">d", float(value[1]))
    if kind == "string":
        return _named(str(value[1]))
    if kind == "byte_array":
        items = bytes(value[1])
        return struct.pack(">i", len(items)) + items
    if kind == "int_array":
        items = list(value[1])
        return struct.pack(">i", len(items)) + b"".join(
            struct.pack(">i", int(i)) for i in items)
    if kind == "long_array":
        items = list(value[1])
        return struct.pack(">i", len(items)) + b"".join(
            struct.pack(">q", int(i)) for i in items)
    if kind == "list":
        element_type = value[1]
        entries: Sequence = value[2]
        element_id = TYPE_IDS[element_type]
        body = b"".join(encode_payload(e) for e in entries)
        return struct.pack(">bi", element_id, len(entries)) + body
    if kind == "compound":
        out = bytearray()
        for name, child in value[1].items():
            out.append(TYPE_IDS[child[0]])
            out += _named(name)
            out += encode_payload(child)
        out.append(TAG_END)
        return bytes(out)
    raise ValueError(f"unknown NBT tag kind: {kind!r}")


def encode_root(name: str, compound: Tuple) -> bytes:
    """Encode a complete, uncompressed NBT document."""
    if compound[0] != "compound":
        raise ValueError("NBT root must be a compound tag")
    return bytes([TAG_COMPOUND]) + _named(name) + encode_payload(compound)


def write_gzip(path: str, name: str, compound: Tuple) -> None:
    """Write a gzip-compressed NBT document, as structure templates require."""
    data = encode_root(name, compound)
    # mtime=0 so regenerating an unchanged template produces identical bytes and
    # does not show up as a diff.
    with gzip.GzipFile(path, "wb", mtime=0) as handle:
        handle.write(data)


# --------------------------------------------------------------------------- #
#  Structure-template helpers
# --------------------------------------------------------------------------- #

def int_list(values: Sequence[int]) -> Tuple:
    """A List<Int>, used for block positions and template size."""
    return ("list", "int", [("int", int(v)) for v in values])


def block_state(name: str, properties: Dict[str, str] | None = None) -> Tuple:
    """One palette entry."""
    entry: Dict[str, Tuple] = {"Name": ("string", name)}
    if properties:
        entry["Properties"] = ("compound",
                               {k: ("string", v) for k, v in properties.items()})
    return ("compound", entry)


def structure_template(size: Sequence[int],
                       palette: Sequence[Tuple],
                       blocks: Sequence[Tuple[str, Tuple]],
                       data_version: int = DATA_VERSION_1_20_1) -> Tuple:
    """
    Assemble a structure template document.

    @param size    the template's (x, y, z) extent in blocks
    @param palette the block states, in index order
    @param blocks  (position, palette index) pairs, or (position, index, nbt)
    """
    entries: List[Tuple] = []
    for block in blocks:
        position, index = block[0], block[1]
        entry: Dict[str, Tuple] = {
            "pos": int_list(position),
            "state": ("int", int(index)),
        }
        if len(block) > 2 and block[2] is not None:
            # Chests and other block entities carry their contents inline; a
            # chest without this tag places empty and loses its authored loot.
            entry["nbt"] = block[2]
        entries.append(("compound", entry))

    return ("compound", {
        "size": int_list(size),
        "entities": ("list", "compound", []),
        "blocks": ("list", "compound", entries),
        "palette": ("list", "compound", list(palette)),
        "DataVersion": ("int", data_version),
    })


def chest_nbt(loot_table: str, seed: int) -> Tuple:
    """
    Block-entity NBT for a chest that rolls an authored loot table.

    Setting LootTable rather than Items is what makes the chest fill on first
    open, so the structure's authored loot -- including the lore book the Golden
    Rules require every structure to guarantee -- actually appears.
    """
    return ("compound", {
        "id": ("string", "minecraft:chest"),
        "LootTable": ("string", loot_table),
        "LootTableSeed": ("long", int(seed)),
    })

# --------------------------------------------------------------------------- #
#  Reading
# --------------------------------------------------------------------------- #

class _Reader:
    """Cursor over a big-endian NBT byte string."""

    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def u8(self) -> int:
        value = self.data[self.pos]
        self.pos += 1
        return value

    def i8(self) -> int:
        value = struct.unpack_from(">b", self.data, self.pos)[0]
        self.pos += 1
        return value

    def u16(self) -> int:
        value = struct.unpack_from(">H", self.data, self.pos)[0]
        self.pos += 2
        return value

    def i16(self) -> int:
        value = struct.unpack_from(">h", self.data, self.pos)[0]
        self.pos += 2
        return value

    def i32(self) -> int:
        value = struct.unpack_from(">i", self.data, self.pos)[0]
        self.pos += 4
        return value

    def i64(self) -> int:
        value = struct.unpack_from(">q", self.data, self.pos)[0]
        self.pos += 8
        return value

    def f32(self) -> float:
        value = struct.unpack_from(">f", self.data, self.pos)[0]
        self.pos += 4
        return value

    def f64(self) -> float:
        value = struct.unpack_from(">d", self.data, self.pos)[0]
        self.pos += 8
        return value

    def name(self) -> str:
        length = self.u16()
        value = self.data[self.pos:self.pos + length].decode("utf-8")
        self.pos += length
        return value

    def payload(self, tag: int):
        if tag == TAG_BYTE:
            return self.i8()
        if tag == TAG_SHORT:
            return self.i16()
        if tag == TAG_INT:
            return self.i32()
        if tag == TAG_LONG:
            return self.i64()
        if tag == TAG_FLOAT:
            return self.f32()
        if tag == TAG_DOUBLE:
            return self.f64()
        if tag == TAG_BYTE_ARRAY:
            length = self.i32()
            value = self.data[self.pos:self.pos + length]
            self.pos += length
            return value
        if tag == TAG_STRING:
            return self.name()
        if tag == TAG_LIST:
            element_tag = self.u8()
            length = self.i32()
            return [self.payload(element_tag) for _ in range(length)]
        if tag == TAG_COMPOUND:
            out: Dict[str, object] = {}
            while True:
                child = self.u8()
                if child == TAG_END:
                    return out
                key = self.name()
                out[key] = self.payload(child)
        if tag == TAG_INT_ARRAY:
            length = self.i32()
            return [self.i32() for _ in range(length)]
        if tag == TAG_LONG_ARRAY:
            length = self.i32()
            return [self.i64() for _ in range(length)]
        raise ValueError(f"unknown NBT tag id {tag} at offset {self.pos}")


def read_gzip(path: str) -> Tuple[str, Dict[str, object]]:
    """
    Decode a gzip-compressed NBT document.

    @return the root tag's name and its compound contents
    @raises ValueError if the root is not a compound tag
    """
    with gzip.open(path, "rb") as handle:
        data = handle.read()
    reader = _Reader(data)
    tag = reader.u8()
    if tag != TAG_COMPOUND:
        raise ValueError(f"root tag is {tag}, expected TAG_Compound")
    return reader.name(), reader.payload(TAG_COMPOUND)

