"""
pixelart/__init__.py -- Biomes Unseen art engine.

STUDIO RULE (Golden Rule #1 / #3):
    No procedural texture scripts. No shape primitives. No draw.rect,
    no draw.ellipse, no fill, no flood, no noise-as-art. Every pixel in this
    mod is *authored*: it appears explicitly either as a hex literal in a 2D
    matrix or as a glyph in a hand-placed character map, resolved through a
    curated palette.

What this package provides is therefore strictly *mechanical*:
    - glyph-map  -> pixel-matrix resolution (a lookup table, not a painter)
    - palette remapping between curated colour ramps (art direction, not noise)
    - overlay compositing of hand-placed detail pixels at explicit coordinates
    - PNG serialization via tools/png_codec.py

The artistic decisions -- outlines, top-left key light, stipple dithering,
ambient occlusion in the crevices -- live in the authored data files
(base_maps.py, palettes.py, overlays.py, bosses.py, ...), pixel by pixel.
"""

from .engine import (  # noqa: F401
    TRANSPARENT,
    compose,
    map_to_matrix,
    mirror_x,
    place_overlay,
    remap_palette,
    to_hex_matrix,
)

__all__ = [
    "TRANSPARENT",
    "map_to_matrix",
    "remap_palette",
    "compose",
    "place_overlay",
    "mirror_x",
    "to_hex_matrix",
]
