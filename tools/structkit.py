"""Parametric structure builders. Floor level is y=0; negative y is foundation/shaft."""
import math

from nbtkit import chest_nbt, template

AIR = "minecraft:air"
LOOT = {"tower": "minecraft:chests/simple_dungeon", "ruin": "minecraft:chests/abandoned_mineshaft",
        "shrine": "minecraft:chests/desert_pyramid", "hut": "minecraft:chests/village/village_toolsmith",
        "circle": "minecraft:chests/jungle_temple", "camp": "minecraft:chests/igloo_chest",
        "crypt": "minecraft:chests/stronghold_corridor"}
GUARDED = {"tower", "ruin", "shrine", "circle", "crypt"}


def h(x, y, z):
    return (x * 7349 + y * 913 + z * 3571 + x * z * 31) % 97


class Build:
    def __init__(self):
        self.blocks, self.chests = {}, set()

    def put(self, x, y, z, name):
        self.blocks[(x, y, z)] = name

    def fill(self, x1, y1, z1, x2, y2, z2, name):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    self.blocks[(x, y, z)] = name

    def chest(self, x, y, z):
        self.blocks[(x, y, z)] = "minecraft:chest"
        self.chests.add((x, y, z))


def tower(P, w, ht):
    wall, floor, acc, light, roof = P
    b = Build()
    b.fill(0, 0, 0, w - 1, 0, w - 1, floor)
    mid = w // 2
    for y in range(1, ht + 1):
        for x in range(w):
            for z in range(w):
                if x in (0, w - 1) or z in (0, w - 1):
                    corner = x in (0, w - 1) and z in (0, w - 1)
                    if y % 4 == 2 and (x == mid or z == mid) and not corner:
                        continue
                    b.put(x, y, z, acc if corner and y % 4 == 0 else wall)
        if y % 5 == 0 or y == ht:
            for x in range(1, w - 1):
                for z in range(1, w - 1):
                    if (x, z) != (mid, 1):
                        b.put(x, y, z, floor)
        b.put(mid, y, 1, "minecraft:ladder[facing=south]")
    for y in (1, 2):
        b.put(mid, y, 0, AIR)
    for x in range(w):
        for z in range(w):
            if (x in (0, w - 1) or z in (0, w - 1)) and (x + z) % 2 == 0:
                b.put(x, ht + 1, z, wall)
    b.put(1, 1, 1, light)
    b.put(w - 2, 1, w - 2, light)
    b.chest(mid, 1, mid)
    return b


def ruin(P, w, d):
    wall, floor, acc, light, roof = P
    b = Build()
    for x in range(w):
        for z in range(d):
            if h(x, 0, z) % 5:
                b.put(x, 0, z, floor)
            if x in (0, w - 1) or z in (0, d - 1):
                top = 0 if h(x, 2, z) % 6 == 0 else 1 + h(x, 1, z) % 4
                for y in range(1, top + 1):
                    b.put(x, y, z, wall)
            elif h(x, 3, z) % 17 == 0:
                b.put(x, 1, z, roof)
    for cx, cz in ((0, 0), (w - 1, 0), (0, d - 1), (w - 1, d - 1)):
        for y in range(1, 6):
            b.put(cx, y, cz, acc)
        b.put(cx, 6, cz, light)
    b.fill(w // 2, 0, d // 2, w // 2, 0, d // 2, floor)
    b.chest(w // 2, 1, d // 2)
    return b


def shrine(P, a, tiers):
    wall, floor, acc, light, roof = P
    b = Build()
    for t in range(tiers):
        half = a - t
        b.fill(-half, t, -half, half, t, half, floor)
        for x in range(-half, half + 1):
            for z in range(-half, half + 1):
                if (abs(x) == half or abs(z) == half) and (x + z) % 2 == 0:
                    b.put(x, t, z, acc)
    top = tiers - 1
    half = a - top
    b.put(0, tiers, 0, acc)
    b.put(0, tiers + 1, 0, light)
    for sx in (-1, 1):
        for sz in (-1, 1):
            for y in range(tiers, tiers + 4):
                b.put(sx * half, y, sz * half, wall)
            b.put(sx * half, tiers + 4, sz * half, light)
    b.chest(0, tiers, half - 1)
    return b


def hut(P, w, d):
    wall, floor, acc, light, roof = P
    b = Build()
    b.fill(0, 0, 0, w - 1, 0, d - 1, floor)
    for x in range(w):
        for z in range(d):
            if x in (0, w - 1) or z in (0, d - 1):
                corner = x in (0, w - 1) and z in (0, d - 1)
                for y in range(1, 4):
                    b.put(x, y, z, acc if corner else wall)
    for y in (1, 2):
        b.put(w // 2, y, d - 1, AIR)
    b.put(0, 2, d // 2, AIR)
    b.put(w - 1, 2, d // 2, AIR)
    i = 0
    while i - 1 <= w - i and i - 1 <= d - i:
        b.fill(i - 1, 4 + i, i - 1, w - i, 4 + i, d - i, roof)
        i += 1
    b.put(1, 1, 1, light)
    b.chest(w - 2, 1, 1)
    return b


def obelisk(P, ht, _unused):
    wall, floor, acc, light, roof = P
    b = Build()
    b.fill(-1, 0, -1, 1, 0, 1, floor)
    b.fill(-1, 1, -1, 1, 1, 1, acc)
    for y in range(2, ht + 1):
        if y <= ht // 3:
            b.fill(-1, y, -1, 1, y, 1, wall)
        else:
            b.put(0, y, 0, acc if y % 4 == 0 else wall)
    b.put(0, ht + 1, 0, light)
    return b


def circle(P, r, _unused):
    wall, floor, acc, light, roof = P
    b = Build()
    n = max(8, int(math.pi * r))
    for i in range(n):
        ang = 2 * math.pi * i / n
        x, z = round(r * math.cos(ang)), round(r * math.sin(ang))
        b.put(x, 0, z, floor)
        top = 2 + h(x, i, z) % 4
        for y in range(1, top + 1):
            b.put(x, y, z, wall)
        b.put(x, top + 1, z, acc if i % 2 else light)
    for i in range(n * 2):
        ang = 2 * math.pi * i / (n * 2)
        for rr in (r - 1, r + 1):
            b.blocks.setdefault((round(rr * math.cos(ang)), 0, round(rr * math.sin(ang))), floor)
    b.fill(-1, 0, -1, 1, 0, 1, floor)
    b.put(0, 1, 0, acc)
    b.put(0, 2, 0, light)
    b.chest(1, 1, 0)
    return b


def well(P, r, _unused):
    wall, floor, acc, light, roof = P
    b = Build()
    big = r + 1
    for x in range(-big, big + 1):
        for z in range(-big, big + 1):
            dist = math.hypot(x, z)
            if dist <= r + 0.3:
                for y in (0, -1, -2):
                    b.put(x, y, z, "minecraft:water")
            elif dist <= big + 0.3:
                b.put(x, 0, z, floor)
                b.put(x, 1, z, wall)
    for sx in (-1, 1):
        for sz in (-1, 1):
            for y in range(1, 4):
                b.put(sx * r, y, sz * r, acc)
    b.fill(-r, 4, -r, r, 4, r, roof)
    b.put(0, 3, 0, light)
    return b


def bridge(P, length, _unused):
    wall, floor, acc, light, roof = P
    b = Build()
    b.fill(0, 0, 0, length - 1, 0, 2, floor)
    for x in range(length):
        for z in (0, 2):
            b.put(x, 1, z, wall)
            if x % 6 == 0:
                b.put(x, 2, z, acc)
                b.put(x, 3, z, light)
    for z in (0, 1, 2):
        for y in (1, 2):
            b.put(0, y, z, acc if z != 1 else AIR)
    return b


def camp(P, a, _unused):
    wall, floor, acc, light, roof = P
    b = Build()
    for x in range(-a, a + 1):
        for z in range(-a, a + 1):
            if math.hypot(x, z) <= a + 0.5:
                b.put(x, 0, z, floor)
    b.put(0, 1, 0, "minecraft:campfire")
    for x0 in (-a - 5, a + 1):
        b.fill(x0, 0, -2, x0 + 4, 0, 1, floor)
        for z in range(-2, 2):
            for dx, y in ((0, 1), (4, 1), (1, 2), (3, 2), (2, 3)):
                b.put(x0 + dx, y, z, roof)
        b.put(x0 + 2, 1, -1, acc)
    b.chest(0, 1, 2)
    b.put(1, 1, 0, light)
    return b


def crypt(P, w, d):
    wall, floor, acc, light, roof = P
    b = Build()
    b.fill(0, 0, 0, w - 1, 0, d - 1, floor)
    for x in range(w):
        for z in range(d):
            if x in (0, w - 1) or z in (0, d - 1):
                for y in range(1, 4):
                    b.put(x, y, z, wall)
    b.fill(-1, 4, -1, w, 4, d, roof)
    b.fill(1, 5, 1, w - 2, 5, d - 2, roof)
    for x in (w // 2 - 1, w // 2):
        for y in (1, 2):
            b.put(x, y, 0, AIR)
    for x in range(2, w - 2, 2):
        b.put(x, 1, d // 2, acc)
        b.put(x, 2, d // 2, floor)
    for cx, cz in ((1, 1), (w - 2, 1), (1, d - 2), (w - 2, d - 2)):
        b.put(cx, 1, cz, light)
    b.chest(w // 2, 1, d - 2)
    return b


BUILDERS = {"tower": tower, "ruin": ruin, "shrine": shrine, "hut": hut, "obelisk": obelisk,
            "circle": circle, "well": well, "bridge": bridge, "camp": camp, "crypt": crypt}


def assemble(arch, pal, a, b_, base, guard):
    """Build, add foundation, shift to the origin, carve air; return (size, nbt bytes, block count)."""
    build = BUILDERS[arch](pal, a, b_)
    blocks = build.blocks
    footprint = {(x, z) for (x, y, z) in blocks if y == 0}
    for x, z in footprint:
        for y in range(-1, -base - 1, -1):
            blocks.setdefault((x, y, z), pal[0])
    xs, ys, zs = zip(*blocks)
    ox, oy, oz = min(xs), min(ys), min(zs)
    size = (max(xs) - ox + 1, max(ys) - oy + 1, max(zs) - oz + 1)
    floor_y = -oy
    for x in range(size[0]):
        for y in range(floor_y + 1, size[1]):
            for z in range(size[2]):
                blocks.setdefault((x + ox, y + oy, z + oz), AIR)
    loot = LOOT.get(arch)
    out = []
    for (x, y, z), name in blocks.items():
        nbt = chest_nbt(loot) if (x, y, z) in build.chests and loot else None
        out.append((x - ox, y - oy, z - oz, name, nbt))
    entities = []
    if guard and arch in GUARDED:
        cx, cz = size[0] // 2, size[2] // 2
        occupied = {(bx, bz) for (bx, by, bz, *_r) in out if by == floor_y + 1 and _r[0] != AIR}
        spot = min((c for c in {(x - ox, z - oz) for x, z in footprint} if c not in occupied),
                   key=lambda c: (c[0] - cx) ** 2 + (c[1] - cz) ** 2, default=None)
        if spot:
            entities.append((spot[0], floor_y + 1, spot[1], guard))
    return size, template(size, out, entities), len(out)
