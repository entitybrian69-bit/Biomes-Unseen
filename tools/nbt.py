# -*- coding: utf-8 -*-
"""Minimal NBT writer used to stamp real structure template .nbt files for
jigsaw pools.  Produces gzipped big-endian NBT (the structure template
format Minecraft loads from data/<ns>/structures/<path>.nbt)."""

import gzip
import struct


class NbtWriter:
    def __init__(self):
        self.buf = bytearray()

    # --- primitives ------------------------------------------------- #
    def _byte(self, v):
        self.buf.append(v & 0xFF)

    def _int(self, v):
        self.buf.extend(struct.pack(">i", v))

    def _short(self, v):
        self.buf.extend(struct.pack(">h", v))

    def _str(self, s):
        data = s.encode("utf-8")
        self.buf.extend(struct.pack(">H", len(data)))
        self.buf.extend(data)

    # --- tags ------------------------------------------------------- #
    def tag_compound(self, name, entries):
        """entries: list of (type_id, name, writer_callable) in order."""
        self._byte(0x0A)
        self._str(name)
        for type_id, tag_name, write in entries:
            self._byte(type_id)
            self._str(tag_name)
            write(self)
        self._byte(0x00)  # TAG_End

    def tag_list_int(self, name, values):
        self._byte(0x09)
        self._str(name)
        self._byte(0x03)  # element type: int
        self._str("")
        self._int(len(values))
        for v in values:
            self._int(v)

    def tag_list_compound(self, name, writers):
        self._byte(0x09)
        self._str(name)
        self._byte(0x0A)  # element type: compound
        self._str("")
        self._int(len(writers))
        for write_entries in writers:
            for type_id, tag_name, write in write_entries:
                self._byte(type_id)
                self._str(tag_name)
                write(self)
            self._byte(0x00)

    def tag_string(self, name, value):
        self._byte(0x08)
        self._str(name)
        self._str(value)

    def tag_int(self, name, value):
        self._byte(0x03)
        self._str(name)
        self._int(value)

    def tag_int_value(self, value):
        self._int(value)

    def tag_string_value(self, value):
        self._str(value)


def write_structure_nbt(path, size, palette, blocks, data_version=2586):
    """Write a structure template NBT.

    size: (sx, sy, sz)
    palette: list of block names, e.g. ["minecraft:stone", ...]
    blocks: list of (x, y, z, state_index)
    """
    w = NbtWriter()
    # Root is an unnamed compound
    w._byte(0x0A)
    w._str("")

    # size: list of ints
    w._byte(0x09)
    w._str("size")
    w._byte(0x03)
    w._str("")
    w._int(3)
    for v in size:
        w._int(v)

    # entities: empty list of compounds
    w._byte(0x09)
    w._str("entities")
    w._byte(0x0A)
    w._str("")
    w._int(0)

    # blocks: list of compounds
    w._byte(0x09)
    w._str("blocks")
    w._byte(0x0A)
    w._str("")
    w._int(len(blocks))
    for (x, y, z, state) in blocks:
        # pos: list of 3 ints
        w._byte(0x09)
        w._str("pos")
        w._byte(0x03)
        w._str("")
        w._int(3)
        w._int(x)
        w._int(y)
        w._int(z)
        # state: int
        w._byte(0x03)
        w._str("state")
        w._int(state)

    # palette: list of compounds with "Name" strings
    w._byte(0x09)
    w._str("palette")
    w._byte(0x0A)
    w._str("")
    w._int(len(palette))
    for name in palette:
        w._byte(0x08)
        w._str("Name")
        w._str(name)

    # DataVersion
    w._byte(0x03)
    w._str("DataVersion")
    w._int(data_version)

    w._byte(0x00)  # end root compound

    # mtime=0 keeps the gzip header stable so regenerated trees are
    # byte-identical between runs (gzip.open stamps wall-clock time).
    with open(path, "wb") as fh:
        with gzip.GzipFile(fileobj=fh, mode="wb", mtime=0) as gz:
            gz.write(bytes(w.buf))


def build_room(size_x=5, size_y=4, size_z=5, floor_state=0, wall_state=1,
               accent_state=2, ceiling_state=3):
    """Build a hollow room with pillars. Returns (size, palette_len, blocks)."""
    blocks = []
    for x in range(size_x):
        for z in range(size_z):
            blocks.append((x, 0, z, floor_state))
            blocks.append((x, size_y - 1, z, ceiling_state))
    for y in range(1, size_y - 1):
        for x in range(size_x):
            blocks.append((x, y, 0, wall_state))
            blocks.append((x, y, size_z - 1, wall_state))
        for z in range(size_z):
            blocks.append((0, y, z, wall_state))
            blocks.append((size_x - 1, y, z, wall_state))
    # corner pillars in accent material
    for (x, z) in ((0, 0), (0, size_z - 1), (size_x - 1, 0), (size_x - 1, size_z - 1)):
        for y in range(1, size_y - 1):
            blocks.append((x, y, z, accent_state))
    return ((size_x, size_y, size_z), 4, blocks)
