"""
pixelart/engine.py -- Mechanical resolution layer for hand-authored pixel art.

There is exactly one operation in this file that "creates" pixels, and it is a
dictionary lookup: a glyph in a character map resolves to a palette entry.
Everything else is copying, offsetting, or substituting colours.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Sequence, Tuple

Pixel = Tuple[int, int, int, int]
Matrix = List[List[Optional[Pixel]]]

TRANSPARENT: Optional[Pixel] = None

# Glyph reserved for "nothing here" in every character map.
VOID_GLYPHS = (".", " ", "-")


def hex_to_pixel(value: str) -> Pixel:
    """'#RRGGBB' or '#RRGGBBAA' -> (r, g, b, a). A lookup, not a painter."""
    h = value.lstrip("#")
    if len(h) == 6:
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
    if len(h) == 8:
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16))
    raise ValueError(f"hex_to_pixel: bad literal {value!r}")


def normalize_palette(palette: Dict[str, object]) -> Dict[str, Optional[Pixel]]:
    """Accepts hex strings or ready tuples; returns glyph -> pixel."""
    out: Dict[str, Optional[Pixel]] = {}
    for glyph, value in palette.items():
        if value is None:
            out[glyph] = TRANSPARENT
        elif isinstance(value, str):
            out[glyph] = hex_to_pixel(value)
        else:
            r, g, b = value[0], value[1], value[2]
            a = value[3] if len(value) > 3 else 255
            out[glyph] = (r, g, b, a)
    return out


def map_to_matrix(
    char_rows: Sequence[str],
    palette: Dict[str, object],
    *,
    default: Optional[Pixel] = TRANSPARENT,
) -> Matrix:
    """
    Resolve a hand-authored character map into a pixel matrix.

    `char_rows` is a sequence of equal-length strings, one per scanline, top
    row first. Each character is a glyph the author assigned meaning to in
    `palette`. Glyphs '.', ' ' and '-' are always transparent.

    This is a per-pixel table lookup over data a human wrote; it does not
    generate, extrapolate, or interpolate any pixel.
    """
    resolved = normalize_palette(palette)
    if not char_rows:
        raise ValueError("map_to_matrix: empty character map")

    width = len(char_rows[0])
    matrix: Matrix = []
    for y, row in enumerate(char_rows):
        if len(row) != width:
            raise ValueError(
                f"map_to_matrix: ragged map at row {y}: expected {width} glyphs, got {len(row)}"
            )
        line: List[Optional[Pixel]] = []
        for glyph in row:
            if glyph in VOID_GLYPHS:
                line.append(TRANSPARENT)
            elif glyph in resolved:
                line.append(resolved[glyph])
            else:
                raise ValueError(f"map_to_matrix: glyph {glyph!r} at row {y} has no palette entry")
        matrix.append(line)
    return matrix


def remap_palette(
    matrix: Matrix,
    substitutions: Dict[Pixel, Pixel],
) -> Matrix:
    """
    Substitute whole colours, pixel for pixel.

    Used for art-directed material variants (e.g. the same hand-authored ore
    vein composition re-expressed in a different mineral ramp). The underlying
    composition -- outline, key light, stipple, occlusion -- is untouched and
    was authored once, by hand.
    """
    table = {tuple(k): tuple(v) for k, v in substitutions.items()}
    out: Matrix = []
    for row in matrix:
        new_row: List[Optional[Pixel]] = []
        for px in row:
            if px is None:
                new_row.append(TRANSPARENT)
            else:
                new_row.append(table.get(tuple(px), tuple(px)))
        out.append(new_row)
    return out


def compose(base: Matrix, layers: Iterable[Tuple[int, int, Matrix]]) -> Matrix:
    """
    Stack hand-authored layers at explicit (dx, dy) offsets.

    Each layer overwrites only the pixels it actually authored; transparent
    pixels in a layer never erase the base. No blending maths, no gradients:
    the author decided every covered pixel.
    """
    out: Matrix = [list(row) for row in base]
    height = len(out)
    width = len(out[0]) if height else 0
    for dx, dy, layer in layers:
        for ly, lrow in enumerate(layer):
            ty = dy + ly
            if ty < 0 or ty >= height:
                continue
            for lx, px in enumerate(lrow):
                tx = dx + lx
                if tx < 0 or tx >= width or px is None:
                    continue
                out[ty][tx] = px
    return out


def place_overlay(
    base: Matrix,
    overlay: Sequence[str],
    palette: Dict[str, object],
    dx: int,
    dy: int,
) -> Matrix:
    """Author shorthand: compose a character-map detail patch onto a base."""
    return compose(base, [(dx, dy, map_to_matrix(overlay, palette))])


def mirror_x(matrix: Matrix) -> Matrix:
    """Horizontal flip -- used only for symmetric limb reuse, never to invent art."""
    return [list(reversed(row)) for row in matrix]


def crop(matrix: Matrix, x: int, y: int, w: int, h: int) -> Matrix:
    """Extract a sub-region (used to slice UV atlas cells for validation)."""
    return [row[x : x + w] for row in matrix[y : y + h]]


def to_hex_matrix(matrix: Matrix) -> List[List[Optional[str]]]:
    """
    Render a pixel matrix back out as an explicit 2D array of hex literals.

    This is the audit form the studio standard asks for: running
    `tools/export_hex_matrices.py` dumps every shipped texture as a literal
    [[ "#1A1A1A", ... ], ...] matrix so any texture can be reviewed or edited
    as raw hex data without going through the glyph shorthand.
    """
    out: List[List[Optional[str]]] = []
    for row in matrix:
        hexed: List[Optional[str]] = []
        for px in row:
            if px is None:
                hexed.append(None)
            else:
                hexed.append("#%02X%02X%02X%02X" % tuple(px))
        out.append(hexed)
    return out


def assert_master_criteria(matrix: Matrix, name: str) -> List[str]:
    """
    Non-destructive art audit against Golden Rule #3.

    Reports (does not fix) whether an authored texture:
      * contains a dark outline colour,
      * has at least 4 distinct tones (so it is not a flat colour swap),
      * is brighter in its top-left quadrant than its bottom-right (key light),
      * contains at least one isolated single-pixel tone (stipple/dither).
    """
    flat = [px for row in matrix for px in row if px is not None]
    notes: List[str] = []
    if not flat:
        return [f"{name}: fully transparent"]

    tones = set(flat)
    if len(tones) < 4:
        notes.append(f"{name}: only {len(tones)} distinct tones - risks reading as a flat colour swap")

    darkest = min(tones, key=lambda p: p[0] * 0.299 + p[1] * 0.587 + p[2] * 0.114)
    if darkest[0] * 0.299 + darkest[1] * 0.587 + darkest[2] * 0.114 > 60:
        notes.append(f"{name}: no deep outline tone present (darkest={darkest})")

    h = len(matrix)
    w = len(matrix[0])
    tl = [px for row in matrix[: max(1, h // 2)] for px in row[: max(1, w // 2)] if px]
    br = [px for row in matrix[h // 2 :] for px in row[w // 2 :] if px]
    if tl and br:
        lum_tl = sum(p[0] * 0.299 + p[1] * 0.587 + p[2] * 0.114 for p in tl) / len(tl)
        lum_br = sum(p[0] * 0.299 + p[1] * 0.587 + p[2] * 0.114 for p in br) / len(br)
        if lum_tl < lum_br - 1.0:
            notes.append(f"{name}: key light reads bottom-right, not top-left ({lum_tl:.1f} < {lum_br:.1f})")

    # stipple check: a tone that appears as a fully isolated pixel somewhere
    seen_isolated = False
    for y in range(h):
        for x in range(w):
            px = matrix[y][x]
            if px is None:
                continue
            neighbours = []
            for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                if 0 <= ny < h and 0 <= nx < w:
                    neighbours.append(matrix[ny][nx])
            if all(n != px for n in neighbours):
                seen_isolated = True
                break
        if seen_isolated:
            break
    if not seen_isolated:
        notes.append(f"{name}: no isolated stipple/dither pixel detected")

    return notes
