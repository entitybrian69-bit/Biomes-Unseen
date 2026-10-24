"""Pixel-art texture for the pass-through Hollow Portal block."""
import math


COLORS = [
    "#091522",  # deep edge
    "#132B46",
    "#185C69",
    "#218D91",
    "#37D2C4",
    "#A5FFF2",
    "#60408F",
    "#291B4F",
]


def portal_sprite():
    image = [[None for _ in range(16)] for _ in range(16)]
    for y in range(16):
        for x in range(16):
            dx = (x - 7.5) / 5.1
            dy = (y - 7.5) / 7.3
            radius = math.sqrt(dx * dx + dy * dy)
            if radius > 1.0:
                continue
            if radius > 0.82:
                image[y][x] = COLORS[0 if radius > 0.92 else 1]
                continue
            swirl = math.sin(math.atan2(dy, dx) * 2.0 + radius * 8.0 + y * 0.35)
            wave = math.sin(x * 0.9 - y * 0.55 + swirl)
            if radius < 0.18 or wave > 0.72:
                color = COLORS[5]
            elif wave > 0.32:
                color = COLORS[4]
            elif wave > -0.05:
                color = COLORS[3]
            elif wave > -0.42:
                color = COLORS[2]
            elif wave > -0.72:
                color = COLORS[6]
            else:
                color = COLORS[7]
            image[y][x] = color
    return image


SPRITES = {"block/hollow_portal": portal_sprite()}
