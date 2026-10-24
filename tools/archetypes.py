"""Seven mob archetypes. Each builder returns (bones, hitbox(w, h), animations) at scale 1."""
from modelkit import bone, looped, lunge, make_cube, shift_y, strike, sway, walk, Anim

C = make_cube()
SWING = [(0, [0, 0, 0]), (0.15, [-100, 0, 0]), (0.3, [40, 0, 0]), (0.5, [0, 0, 0])]


def biped(acc):
    bones = [
        bone("root", None, [0, 0, 0]),
        bone("body", "root", [0, 18, 0], [C([-5, 18, -3], [10, 14, 6])]),
        bone("head", "body", [0, 32, 0], [C([-4, 32, -4], [8, 8, 8], front="face")]),
        bone("arm_l", "body", [6, 30, 0], [C([5, 13, -2], [3, 17, 4])]),
        bone("arm_r", "body", [-6, 30, 0], [C([-8, 13, -2], [3, 17, 4])]),
        bone("leg_l", "root", [2.5, 18, 0], [C([0.5, 0, -2], [4, 18, 4])]),
        bone("leg_r", "root", [-2.5, 18, 0], [C([-4.5, 0, -2], [4, 18, 4])]),
    ]
    if acc == "horns":
        bones += [bone("horn_l", "head", [2, 40, 0], [C([1, 40, -1], [2, 7, 2], "dark", "dark", "dark")]),
                  bone("horn_r", "head", [-2, 40, 0], [C([-3, 40, -1], [2, 7, 2], "dark", "dark", "dark")])]
    if acc == "spikes":
        bones.append(bone("spines", "body", [0, 24, 3], [C([-1.5, 20, 3], [3, 12, 3], "dark", "dark", "glow")]))
    anims = {
        "idle": looped(2.0, {"head": ("rotation", sway([4, 0, 0], 2.0)), "body": ("rotation", sway([0, 0, 1.5], 2.0))}),
        "walk": walk(["leg_l", "arm_r"], ["leg_r", "arm_l"], 30, 1.0),
        "attack": strike(0.5, {"arm_l": ("rotation", SWING), "arm_r": ("rotation", SWING),
                               "head": ("rotation", [(0, [0, 0, 0]), (0.15, [-15, 0, 0]), (0.3, [20, 0, 0]), (0.5, [0, 0, 0])])}),
    }
    return bones, (0.7, 2.5), anims


def brute(acc):
    bones = [
        bone("root", None, [0, 0, 0]),
        bone("body", "root", [0, 16, 0], [C([-7, 14, -5], [14, 16, 10])]),
        bone("head", "body", [0, 30, 0], [C([-4, 30, -4], [8, 7, 8], front="face")]),
        bone("arm_l", "body", [9.5, 28, 0], [C([7, 8, -3], [5, 20, 6])]),
        bone("arm_r", "body", [-9.5, 28, 0], [C([-12, 8, -3], [5, 20, 6])]),
        bone("leg_l", "root", [3.5, 14, 0], [C([0.5, 0, -3], [6, 14, 6])]),
        bone("leg_r", "root", [-3.5, 14, 0], [C([-6.5, 0, -3], [6, 14, 6])]),
    ]
    if acc == "crystals":
        bones += [bone("crystal_l", "body", [5, 30, 0], [C([3.5, 30, -1.5], [3, 9, 3], "glow", "glow", "glow")], [0, 0, -18]),
                  bone("crystal_r", "body", [-5, 30, 0], [C([-6.5, 30, -1.5], [3, 9, 3], "glow", "glow", "glow")], [0, 0, 18])]
    if acc == "plates":
        bones += [bone("plate_l", "body", [9, 30, 0], [C([7, 28, -4], [6, 3, 8], "dark", "dark", "dark")]),
                  bone("plate_r", "body", [-9, 30, 0], [C([-13, 28, -4], [6, 3, 8], "dark", "dark", "dark")])]
    slam = [(0, [0, 0, 0]), (0.25, [-120, 0, 0]), (0.5, [30, 0, 0]), (0.8, [0, 0, 0])]
    anims = {
        "idle": looped(2.0, {"arm_l": ("rotation", sway([0, 0, -3], 2.0)), "arm_r": ("rotation", sway([0, 0, 3], 2.0))}),
        "walk": walk(["leg_l", "arm_r"], ["leg_r", "arm_l"], 25, 1.4, {"body": ("rotation", sway([0, 0, 3], 1.4))}),
        "attack": strike(0.8, {"arm_l": ("rotation", slam), "arm_r": ("rotation", slam),
                               "body": ("rotation", [(0, [0, 0, 0]), (0.25, [-10, 0, 0]), (0.5, [12, 0, 0]), (0.8, [0, 0, 0])])}),
    }
    return bones, (1.5, 2.4), anims


def crawler(acc):
    def leg(name, side, z):
        x = 4 * side
        return bone(name, "body", [x, 6, z], [C([3.5 if side > 0 else -5.5, 0, z - 1], [2, 6.5, 2])], [0, 0, -25 * side])
    bones = [
        bone("root", None, [0, 0, 0]),
        bone("body", "root", [0, 6, 0], [C([-4, 4, -3], [8, 6, 11])]),
        bone("head", "body", [0, 7, -3], [C([-3, 4.5, -9], [6, 5, 6], front="face")]),
        bone("abdomen", "body", [0, 7, 8], [C([-3, 4.5, 8], [6, 5, 5], "glow", "dark", "glow")]),
        leg("leg_l1", 1, -1), leg("leg_l2", 1, 3), leg("leg_l3", 1, 7),
        leg("leg_r1", -1, -1), leg("leg_r2", -1, 3), leg("leg_r3", -1, 7),
    ]
    anims = {
        "idle": looped(2.0, {"abdomen": ("rotation", sway([0, 0, 4], 2.0)), "head": ("rotation", sway([3, 0, 0], 2.0))}),
        "walk": walk(["leg_l1", "leg_r2", "leg_l3"], ["leg_r1", "leg_l2", "leg_r3"], 28, 0.7),
        "attack": lunge(0.4, [("head", 25), ("body", 10)]),
    }
    return bones, (1.0, 0.8), anims


def quad(acc):
    bones = [
        bone("root", None, [0, 0, 0]),
        bone("body", "root", [0, 12, 0], [C([-4, 8, -8], [8, 8, 16])]),
        bone("head", "body", [0, 14, -8], [C([-3, 10, -14], [6, 6, 6], front="face")]),
        bone("leg_fl", "root", [2.5, 8, -5], [C([1, 0, -6.5], [3, 8, 3])]),
        bone("leg_fr", "root", [-2.5, 8, -5], [C([-4, 0, -6.5], [3, 8, 3])]),
        bone("leg_bl", "root", [2.5, 8, 5], [C([1, 0, 3.5], [3, 8, 3])]),
        bone("leg_br", "root", [-2.5, 8, 5], [C([-4, 0, 3.5], [3, 8, 3])]),
        bone("tail", "body", [0, 13, 8], [C([-1, 11, 8], [2, 2, 7], "dark", "dark", "dark")]),
    ]
    if acc == "mane":
        bones.append(bone("mane", "body", [0, 16, -6], [C([-2, 16, -7], [4, 4, 10], "dark", "dark", "glow")]))
    anims = {
        "idle": looped(2.0, {"tail": ("rotation", sway([0, 15, 0], 2.0)), "head": ("rotation", sway([4, 0, 0], 2.0))}),
        "walk": walk(["leg_fl", "leg_br"], ["leg_fr", "leg_bl"], 30, 0.8),
        "attack": lunge(0.5, [("head", 30), ("body", 8)]),
    }
    return bones, (0.9, 1.1), anims


def floater(acc):
    bones = [
        bone("root", None, [0, 0, 0]),
        bone("body", "root", [0, 10, 0], [C([-3, 10, -2], [6, 12, 4])]),
        bone("robe", "body", [0, 10, 0], [C([-4, 2, -3], [8, 8, 6], "hide", "hide", "dark")]),
        bone("tail1", "robe", [0, 2, 0], [C([-2.5, -4, -2], [5, 6, 4], "hide", "hide", "dark")]),
        bone("tail2", "tail1", [0, -4, 0], [C([-1.5, -9, -1.5], [3, 5, 3], "dark", "dark", "dark")]),
        bone("head", "body", [0, 22, 0], [C([-3, 22, -3], [6, 6, 6], front="face")]),
        bone("arm_l", "body", [4, 20, 0], [C([3, 10, -1], [2, 11, 2])]),
        bone("arm_r", "body", [-4, 20, 0], [C([-5, 10, -1], [2, 11, 2])]),
    ]
    shift_y(bones, 9)
    anims = {
        "idle": looped(2.0, {"root": ("position", [(0, [0, 0, 0]), (1.0, [0, 2, 0]), (2.0, [0, 0, 0])]),
                             "tail1": ("rotation", sway([0, 0, 8], 2.0)), "tail2": ("rotation", sway([0, 0, -12], 2.0)),
                             "arm_l": ("rotation", sway([-10, 0, 0], 2.0)), "arm_r": ("rotation", sway([-10, 0, 0], 2.0))}),
        "walk": looped(1.0, {"body": ("rotation", [(0, [10, 0, 0]), (0.5, [12, 0, 0]), (1.0, [10, 0, 0])]),
                             "tail1": ("rotation", sway([0, 0, 14], 1.0)), "tail2": ("rotation", sway([0, 0, -20], 1.0)),
                             "arm_l": ("rotation", [(0, [-40, 0, 0]), (0.5, [-55, 0, 0]), (1.0, [-40, 0, 0])]),
                             "arm_r": ("rotation", [(0, [-55, 0, 0]), (0.5, [-40, 0, 0]), (1.0, [-55, 0, 0])])}),
        "attack": strike(0.5, {"arm_l": ("rotation", [(0, [0, 0, 0]), (0.15, [-80, 0, 0]), (0.3, [20, 0, 0]), (0.5, [0, 0, 0])]),
                               "arm_r": ("rotation", [(0, [0, 0, 0]), (0.15, [-80, 0, 0]), (0.3, [20, 0, 0]), (0.5, [0, 0, 0])]),
                               "head": ("rotation", [(0, [0, 0, 0]), (0.15, [-20, 0, 0]), (0.3, [12, 0, 0]), (0.5, [0, 0, 0])])}),
    }
    return bones, (0.7, 2.2), anims


def blob(acc):
    bones = [
        bone("root", None, [0, 0, 0]),
        bone("body", "root", [0, 5, 0], [C([-3, 3, -3], [6, 7, 6], front="face")]),
        bone("cap", "body", [0, 10, 0], [C([-6, 10, -6], [12, 3, 12], "dark", "dark", "glow"),
                                         C([-4, 13, -4], [8, 2, 8], "dark", "dark", "glow")]),
        bone("leg_l", "root", [1.5, 3, 0], [C([0, 0, -1.5], [3, 3, 3])]),
        bone("leg_r", "root", [-1.5, 3, 0], [C([-3, 0, -1.5], [3, 3, 3])]),
    ]
    anims = {
        "idle": looped(1.5, {"cap": ("rotation", sway([0, 0, 6], 1.5)), "body": ("rotation", sway([0, 0, -2], 1.5))}),
        "walk": walk(["leg_l"], ["leg_r"], 35, 0.6, {"body": ("rotation", sway([0, 0, 6], 0.6))}),
        "attack": lunge(0.5, [("cap", 35), ("body", 20)]),
    }
    return bones, (0.7, 0.95), anims


def serpent(acc):
    bones = [
        bone("root", None, [0, 0, 0]),
        bone("head", "root", [0, 3, -3], [C([-3, 0, -9], [6, 6, 6], front="face")]),
        bone("seg1", "root", [0, 3, -3], [C([-3, 0, -3], [6, 6, 8])]),
        bone("seg2", "seg1", [0, 3, 5], [C([-2.5, 0, 5], [5, 5, 8])]),
        bone("seg3", "seg2", [0, 3, 13], [C([-2, 0, 13], [4, 4, 8])]),
        bone("seg4", "seg3", [0, 3, 21], [C([-1.5, 0, 21], [3, 3, 8], "glow", "dark", "glow")]),
    ]
    wave = lambda amp, length: ("rotation", [(0, [0, -amp, 0]), (length / 2, [0, amp, 0]), (length, [0, -amp, 0])])
    anims = {
        "idle": looped(2.0, {"seg1": ("rotation", sway([0, 6, 0], 2.0)), "seg2": ("rotation", sway([0, -8, 0], 2.0)),
                             "seg3": ("rotation", sway([0, 10, 0], 2.0)), "seg4": ("rotation", sway([0, -12, 0], 2.0))}),
        "walk": looped(0.8, {"seg1": wave(14, 0.8), "seg2": wave(-18, 0.8), "seg3": wave(22, 0.8), "seg4": wave(-26, 0.8)}),
        "attack": lunge(0.45, [("head", 30), ("seg1", 12)]),
    }
    return bones, (0.8, 0.6), anims


ARCHETYPES = {"biped": biped, "brute": brute, "crawler": crawler, "quad": quad,
              "floater": floater, "blob": blob, "serpent": serpent}
