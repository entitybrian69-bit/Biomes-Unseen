#!/usr/bin/env python3
"""Verify the forced-load chunks saved a real custom biome and structure start.

Run from smoke/server after the dedicated server has stopped. The RCON smoke first
locates the content, force-loads those chunks so normal world generation runs, and
saves their coordinates in worldgen-smoke.json. This inspects the saved Anvil NBT,
not just registry entries or /locate results.
"""
import gzip
import json
import os
import struct
import sys
import zlib


def read_chunk(world, chunk_x, chunk_z):
    region_x, region_z = chunk_x // 32, chunk_z // 32
    path = os.path.join(world, "region", "r.%d.%d.mca" % (region_x, region_z))
    if not os.path.exists(path):
        return None
    slot = (chunk_x & 31) + (chunk_z & 31) * 32
    with open(path, "rb") as region:
        region.seek(slot * 4)
        location = region.read(4)
        if len(location) != 4:
            return None
        sector = int.from_bytes(location[:3], "big")
        if sector == 0:
            return None
        region.seek(sector * 4096)
        length_bytes = region.read(4)
        if len(length_bytes) != 4:
            return None
        length = struct.unpack(">I", length_bytes)[0]
        compression = region.read(1)
        compressed = region.read(length - 1)
    if not compression or len(compressed) != length - 1:
        return None
    kind = compression[0]
    if kind == 1:
        return gzip.decompress(compressed)
    if kind == 2:
        return zlib.decompress(compressed)
    if kind == 3:
        return compressed
    raise ValueError("unsupported Anvil compression type %d in %s" % (kind, path))


def find_identifier(world, x, z, identifier, radius=0):
    center_x, center_z = x // 16, z // 16
    for dz in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            chunk_x, chunk_z = center_x + dx, center_z + dz
            data = read_chunk(world, chunk_x, chunk_z)
            if data is not None and identifier.encode("utf-8") in data:
                return chunk_x, chunk_z
    return None


def main():
    report_path = "worldgen-smoke.json"
    world = "world"
    if not os.path.exists(report_path):
        raise RuntimeError("missing RCON coordinate report: " + report_path)
    with open(report_path, encoding="utf-8") as stream:
        report = json.load(stream)

    biome = report["biome"]
    biome_chunk = find_identifier(world, biome["x"], biome["z"], biome["id"])
    if biome_chunk is None:
        raise RuntimeError("forced-loaded chunk does not contain biome palette entry %s near %s" %
                           (biome["id"], (biome["x"], biome["z"])))
    print("verified generated biome %s in saved chunk %s" % (biome["id"], biome_chunk), flush=True)

    structure = report["structure"]
    structure_chunk = find_identifier(world, structure["x"], structure["z"], structure["id"], radius=1)
    if structure_chunk is None:
        raise RuntimeError("no generated structure start %s found in saved chunks near %s" %
                           (structure["id"], (structure["x"], structure["z"])))
    print("verified naturally generated structure start %s in saved chunk %s" %
          (structure["id"], structure_chunk), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("Saved-world generation verification failed: %s" % exc, file=sys.stderr)
        sys.exit(1)
