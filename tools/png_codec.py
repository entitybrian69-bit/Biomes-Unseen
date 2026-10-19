"""
png_codec.py -- Minimal, dependency-free RGBA PNG encoder.

The studio art pipeline forbids shape-drawing primitives. This module therefore
contains NO drawing logic whatsoever: it is purely a container serializer. It
takes an already-authored 2D matrix of pixels (produced by hand in the
`pixelart/` authoring modules) and packs it into a real, spec-correct PNG
bitstream: signature, IHDR, IDAT (zlib, per-scanline filter 0), IEND, with
CRC-32 on every chunk.

Nothing here decides what a pixel looks like. Every pixel is authored by hand.
"""

from __future__ import annotations

import struct
import zlib
from typing import Iterable, List, Sequence, Tuple

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

Pixel = Tuple[int, int, int, int]


def _chunk(tag: bytes, payload: bytes) -> bytes:
    """Assemble one PNG chunk: length, tag, payload, CRC32(tag+payload)."""
    return (
        struct.pack(">I", len(payload))
        + tag
        + payload
        + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF)
    )


def encode_png(matrix: Sequence[Sequence[Pixel | None]], *, bit_depth: int = 8) -> bytes:
    """
    Serialize a hand-authored pixel matrix to PNG bytes.

    `matrix[row][col]` is either an (r, g, b, a) tuple or None for a fully
    transparent pixel. Row 0 is the TOP row of the image (Minecraft / PNG
    convention: UV origin top-left, light source authored top-left to match).
    """
    if not matrix:
        raise ValueError("encode_png: empty matrix")

    height = len(matrix)
    width = len(matrix[0])
    for y, row in enumerate(matrix):
        if len(row) != width:
            raise ValueError(
                f"encode_png: ragged matrix at row {y}: expected {width} px, got {len(row)}"
            )
    if bit_depth != 8:
        raise ValueError("encode_png: only 8-bit RGBA is supported (Minecraft texture standard)")

    raw = bytearray()
    for row in matrix:
        raw.append(0)  # scanline filter type 0 (None) -- lossless, no prediction
        for px in row:
            if px is None:
                raw += b"\x00\x00\x00\x00"
            else:
                r, g, b, a = px
                raw += bytes((r & 0xFF, g & 0xFF, b & 0xFF, a & 0xFF))

    ihdr = struct.pack(">IIBBBBB", width, height, bit_depth, 6, 0, 0, 0)  # 6 = truecolor+alpha
    compressed = zlib.compress(bytes(raw), 9)

    return PNG_SIGNATURE + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", compressed) + _chunk(b"IEND", b"")


def decode_png(data: bytes) -> Tuple[int, int, List[List[Pixel]]]:
    """
    Decode an RGBA PNG back into a pixel matrix.

    Used by tools/validate.py to prove that every committed texture is a real,
    decodable PNG of the expected dimensions -- not a renamed blob.
    Only supports the flavour this pipeline writes (8-bit RGBA, filter 0) plus
    the standard filter types, so it can also audit hand-supplied art.
    """
    if data[:8] != PNG_SIGNATURE:
        raise ValueError("decode_png: not a PNG (bad signature)")

    pos = 8
    width = height = bit_depth = color_type = None
    idat = bytearray()

    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError("decode_png: truncated chunk header")
        (length,) = struct.unpack(">I", data[pos : pos + 4])
        tag = data[pos + 4 : pos + 8]
        payload = data[pos + 8 : pos + 8 + length]
        if len(payload) != length:
            raise ValueError(f"decode_png: truncated {tag!r} chunk")

        declared_crc = struct.unpack(">I", data[pos + 8 + length : pos + 12 + length])[0]
        if zlib.crc32(tag + payload) & 0xFFFFFFFF != declared_crc:
            raise ValueError(f"decode_png: CRC mismatch in {tag!r}")

        if tag == b"IHDR":
            width, height, bit_depth, color_type, comp, filt, interlace = struct.unpack(
                ">IIBBBBB", payload
            )
            if comp != 0 or filt != 0:
                raise ValueError("decode_png: unsupported compression/filter method")
            if interlace != 0:
                raise ValueError("decode_png: interlaced PNGs are not supported")
        elif tag == b"IDAT":
            idat += payload
        elif tag == b"IEND":
            break
        pos += 12 + length

    if width is None:
        raise ValueError("decode_png: missing IHDR")
    if bit_depth != 8:
        raise ValueError(f"decode_png: unsupported bit depth {bit_depth}")
    if color_type not in (2, 6):
        raise ValueError(f"decode_png: unsupported color type {color_type}")

    channels = 4 if color_type == 6 else 3
    stride = width * channels
    raw = zlib.decompress(bytes(idat))

    if len(raw) != height * (stride + 1):
        raise ValueError("decode_png: IDAT length does not match IHDR dimensions")

    # Reconstruct scanlines (handles the five standard PNG filters).
    prev = bytearray(stride)
    out_rows: List[List[Pixel]] = []
    for y in range(height):
        ftype = raw[y * (stride + 1)]
        line = bytearray(raw[y * (stride + 1) + 1 : y * (stride + 1) + 1 + stride])
        if ftype == 0:
            pass
        elif ftype == 1:
            for i in range(channels, stride):
                line[i] = (line[i] + line[i - channels]) & 0xFF
        elif ftype == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif ftype == 3:
            for i in range(stride):
                left = line[i - channels] if i >= channels else 0
                line[i] = (line[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif ftype == 4:
            for i in range(stride):
                a = line[i - channels] if i >= channels else 0
                b = prev[i]
                c = prev[i - channels] if i >= channels else 0
                line[i] = (line[i] + _paeth(a, b, c)) & 0xFF
        else:
            raise ValueError(f"decode_png: unknown filter type {ftype}")

        pixels: List[Pixel] = []
        for x in range(width):
            base = x * channels
            r, g, b = line[base], line[base + 1], line[base + 2]
            a = line[base + 3] if channels == 4 else 255
            pixels.append((r, g, b, a))
        out_rows.append(pixels)
        prev = line

    return width, height, out_rows


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def png_dimensions(data: bytes) -> Tuple[int, int]:
    """Cheap header-only dimension probe used by the validator."""
    if data[:8] != PNG_SIGNATURE or data[12:16] != b"IHDR":
        raise ValueError("png_dimensions: not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def write_png(path, matrix: Sequence[Sequence[Pixel | None]]) -> bytes:
    """Encode and write to disk, creating parent directories as needed."""
    import os

    data = encode_png(matrix)
    os.makedirs(os.path.dirname(str(path)), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)
    return data


def matrix_from_hex(rows: Iterable[Iterable[str]]) -> List[List[Pixel]]:
    """
    Convert a hand-authored 2D array of '#RRGGBB' / '#RRGGBBAA' strings (or
    None / '' for transparent) into the pixel-matrix form encode_png wants.
    This exists so the art source can be written in the literal hex-matrix
    form the studio standard mandates.
    """
    out: List[List[Pixel]] = []
    for row in rows:
        out_row: List[Pixel] = []
        for cell in row:
            if cell is None or cell == "":
                out_row.append(None)
                continue
            h = cell.lstrip("#")
            if len(h) == 6:
                out_row.append((int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255))
            elif len(h) == 8:
                out_row.append(
                    (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16))
                )
            else:
                raise ValueError(f"matrix_from_hex: bad color literal {cell!r}")
        out.append(out_row)
    return out
