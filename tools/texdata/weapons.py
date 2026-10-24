"""Generated weapon and guide icons, recoloured from the shared ore palettes."""

from spec.ores import HOLLOWITE, ORES
from spec.palettes import GLOWS, PALETTES



def canvas():
    return [[None for _ in range(16)] for _ in range(16)]


def put(image, x, y, color):
    if 0 <= x < 16 and 0 <= y < 16:
        image[y][x] = color


def sword(palette):
    outline, dark, mid, light = palette
    image = canvas()
    for step in range(10):
        x, y = 13 - step, 1 + step
        put(image, x + 1, y - 1, outline)
        put(image, x, y, light if step < 5 else mid)
        put(image, x - 1, y + 1, mid)
        put(image, x, y + 1, dark)
        put(image, x - 2, y + 1, outline)
    for step in range(5):
        x, y = 1 + step, 8 + step
        put(image, x, y, outline)
        put(image, x, y + 1, light if step in (1, 2) else mid)
    for step in range(4):
        put(image, 3 - step, 10 + step, dark)
        put(image, 4 - step, 10 + step, outline)
    put(image, 0, 14, outline)
    put(image, 1, 14, light)
    put(image, 0, 15, dark)
    return image


def battleaxe(palette):
    outline, dark, mid, light = palette
    image = canvas()
    for step in range(9):
        x, y = 2 + step, 14 - step
        put(image, x, y, outline)
        put(image, x + 1, y, mid)
        put(image, x, y - 1, dark)
    blade = [(9, 2), (10, 1), (14, 1), (15, 3), (15, 7), (13, 9), (10, 9), (8, 7)]
    for x, y in blade:
        put(image, x, y, outline)
    for y in range(2, 8):
        for x in range(10, 15):
            put(image, x, y, light if x + y < 18 else mid)
    for x, y in ((8, 3), (9, 2), (10, 2), (10, 3), (9, 4), (8, 5), (9, 6), (10, 7)):
        put(image, x, y, outline)
    return image


def sigil(palette, glow):
    outline, dark, mid, light = palette
    accent = GLOWS[glow][0]
    image = canvas()
    for x, y in ((6, 1), (7, 1), (8, 1), (9, 1), (4, 2), (5, 2), (10, 2), (11, 2),
                 (3, 4), (12, 4), (2, 6), (13, 6), (2, 9), (13, 9), (3, 11), (12, 11),
                 (4, 13), (11, 13), (6, 14), (7, 14), (8, 14), (9, 14)):
        put(image, x, y, outline)
    for x, y in ((6, 2), (7, 2), (8, 2), (9, 2), (4, 3), (5, 3), (10, 3), (11, 3),
                 (3, 5), (12, 5), (3, 6), (12, 6), (3, 9), (12, 9), (4, 11), (11, 11),
                 (5, 12), (10, 12), (6, 13), (7, 13), (8, 13), (9, 13)):
        put(image, x, y, mid)
    for x, y in ((7, 5), (8, 5), (6, 6), (9, 6), (5, 7), (10, 7), (6, 8), (9, 8),
                 (7, 9), (8, 9), (7, 7), (8, 7)):
        put(image, x, y, accent)
    put(image, 7, 6, light)
    put(image, 8, 6, light)
    return image


def field_guide():
    image = canvas()
    cover, shadow, page, accent = "#17251C", "#0A120D", "#E8E0C8", "#5FE0D0"
    for y in range(2, 14):
        for x in range(3, 13):
            put(image, x, y, cover)
    for y in range(3, 13):
        for x in range(5, 12):
            put(image, x, y, page)
    for y in range(2, 14):
        put(image, 3, y, shadow)
        put(image, 4, y, accent if y in (3, 12) else cover)
    for y in (5, 7, 9):
        for x in range(6, 11):
            put(image, x, y, "#8C7F62")
    for x, y in ((8, 4), (8, 3), (7, 4), (9, 4), (8, 5)):
        put(image, x, y, accent)
    return image


SPRITES = {"item/field_guide": field_guide(), "item/hollow_sigil": sigil(PALETTES[HOLLOWITE[3]], HOLLOWITE[4]),
           "item/hollowite_sword": sword(PALETTES[HOLLOWITE[3]]),
           "item/hollowite_battleaxe": battleaxe(PALETTES[HOLLOWITE[3]])}
for _row in ORES:
    SPRITES["item/" + _row[0] + "_sword"] = sword(PALETTES[_row[3]])
