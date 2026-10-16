#!/usr/bin/env python3
"""Derive the mod logo/icon from the master artwork.

Writes the square, resized icons the loaders point at:
  common/src/main/resources/assets/biomesunseen/icon.png       (128x128, mod list)
  common/src/main/resources/assets/biomesunseen/icon_256.png   (256x256, store art)

Run after replacing assets/biomesunseen/icon_raw.png.  Needs Pillow.
"""
import os
import sys

from PIL import Image

MOD_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(MOD_ROOT, "common", "src", "main", "resources",
                      "assets", "biomesunseen")


def main():
    # The master artwork intentionally lives outside the jar resources.
    raw = os.path.join(MOD_ROOT, "docs", "assets", "icon_raw.png")
    if not os.path.exists(raw):
        print("missing master artwork: %s" % raw, file=sys.stderr)
        return 1
    image = Image.open(raw).convert("RGBA")
    side = min(image.size)
    left = (image.width - side) // 2
    top = (image.height - side) // 2
    square = image.crop((left, top, left + side, top + side))
    for size, name in ((128, "icon.png"), (256, "icon_256.png")):
        out = square.resize((size, size), Image.LANCZOS)
        path = os.path.join(ASSETS, name)
        out.save(path, "PNG", optimize=True)
        print("wrote %s (%dx%d)" % (path, size, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
