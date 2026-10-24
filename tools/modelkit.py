"""Helpers for GeckoLib geo/animation JSON and tile-sheet textures (standard library only)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spec.palettes import GLOWS, PALETTES, TILES  # noqa: E402

STD_TILES = {"face": (0, 0), "hide": (8, 0), "dark": (0, 8), "glow": (8, 8)}


def make_cube(tiles=STD_TILES):
    def cube(origin, size, front="hide", side="hide", top="dark", back=None):
        faces = {"north": front, "south": back or side, "east": side, "west": side, "up": top, "down": top}
        uv = {f: {"uv": list(tiles[t]), "uv_size": [8, 8]} for f, t in faces.items()}
        return {"origin": list(origin), "size": list(size), "uv": uv}
    return cube


def bone(name, parent, pivot, cubes=None, rot=None):
    b = {"name": name}
    if parent:
        b["parent"] = parent
    b["pivot"] = list(pivot)
    if rot:
        b["rotation"] = rot
    if cubes:
        b["cubes"] = cubes
    return b


def scale_bones(bones, k):
    for b in bones:
        b["pivot"] = [round(v * k, 3) for v in b["pivot"]]
        for c in b.get("cubes", []):
            c["origin"] = [round(v * k, 3) for v in c["origin"]]
            c["size"] = [round(v * k, 3) for v in c["size"]]


def shift_y(bones, dy):
    for b in bones:
        b["pivot"][1] += dy
        for c in b.get("cubes", []):
            c["origin"][1] += dy


def geo(name, bones, w, h, hitbox):
    hw, hh = hitbox
    return {"format_version": "1.12.0", "minecraft:geometry": [{
        "description": {"identifier": "geometry." + name, "texture_width": w, "texture_height": h,
                        "visible_bounds_width": round(hw * 1.8 + 1, 2),
                        "visible_bounds_height": round(hh * 1.5 + 0.5, 2),
                        "visible_bounds_offset": [0, round(hh / 2, 2), 0]},
        "bones": bones}]}


class Anim:
    def __init__(self, length, loop):
        self.d = {"loop": loop, "animation_length": float(length), "bones": {}}

    def add(self, bone_name, channel, pairs):
        self.d["bones"].setdefault(bone_name, {})[channel] = {str(float(t)): v for t, v in pairs}
        return self


def sway(vec, length):
    return [(0, [0, 0, 0]), (length / 2, vec), (length, [0, 0, 0])]


def looped(length, channels):
    a = Anim(length, True)
    for name, (channel, pairs) in channels.items():
        a.add(name, channel, pairs)
    return a.d


def walk(group_a, group_b, amp, length, extra=None, axis=0):
    a = Anim(length, True)
    hi, lo = [0, 0, 0], [0, 0, 0]
    hi[axis], lo[axis] = amp, -amp
    for b in group_a:
        a.add(b, "rotation", [(0, hi), (length / 2, lo), (length, hi)])
    for b in group_b:
        a.add(b, "rotation", [(0, lo), (length / 2, hi), (length, lo)])
    for name, (channel, pairs) in (extra or {}).items():
        a.add(name, channel, pairs)
    return a.d


def strike(length, channels):
    a = Anim(length, False)
    for name, (channel, pairs) in channels.items():
        a.add(name, channel, pairs)
    return a.d


def lunge(length, bones_amp):
    """Rotate each (bone, amplitude) forward then recoil."""
    t = length
    return strike(length, {b: ("rotation", [(0, [0, 0, 0]), (t * 0.3, [-amp, 0, 0]),
                                            (t * 0.6, [amp * 0.5, 0, 0]), (t, [0, 0, 0])])
                           for b, amp in bones_amp})


def tile_sheet(pal, glow, face, hide):
    """16x16 sheet: face(0,0) hide(1,0) dark(0,1) glow(1,1); returns rows of '#RRGGBB'."""
    o, a, b, c = PALETTES[pal]
    g, w = GLOWS[glow]
    ramp = {"o": o, "a": a, "b": b, "c": c, "g": g, "w": w}
    layout = {(0, 0): "face_" + face, (1, 0): "hide_" + hide, (0, 1): "dark_a", (1, 1): "glow_a"}
    rows = [["#000000"] * 16 for _ in range(16)]
    for (tx, ty), tpl in layout.items():
        for y, line in enumerate(TILES[tpl]):
            for x, ch in enumerate(line):
                rows[ty * 8 + y][tx * 8 + x] = ramp[ch]
    return rows


def emit_sprite(key, rows):
    lines = ['    "%s": [' % key]
    for r in rows:
        lines.append("        [%s]," % ", ".join("None" if c is None else '"%s"' % c for c in r))
    lines.append("    ],")
    return "\n".join(lines)


def hex_int(color):
    return int(color[1:], 16)
