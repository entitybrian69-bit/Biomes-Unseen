# -*- coding: utf-8 -*-
"""Emits shared assets: lang, blockstates/models, sounds.json, textures (PNG),
GeckoLib geometry and FULL animation clips for every mob, boss and animated
block.  Everything in the mod is animated."""

import json
import os

from content import (BIOME_ROWS, ORE_ROWS, DECOR_ROWS, PLANT_ROWS, MOB_ROWS,
                     BOSS_ROWS, STRUCTURE_ROWS, SOUND_EVENTS, PARTICLE_TYPES,
                     CONFIG_ROWS)
import pnggen


def _w(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text if text.endswith("\n") else text + "\n")


def emit_logo(root):
    """Copy the mod icon into the asset root.

    The icon is part of the loader metadata (fabric.mod.json "icon",
    mods.toml logoFile), so it has to be re-emitted with everything else -
    generate.py purges and rewrites the whole content tree.
    """
    import shutil
    assets = os.path.join(root, "common", "src", "main", "resources",
                          "assets", "biomesunseen")
    source = os.path.join(root, "docs", "assets")
    os.makedirs(assets, exist_ok=True)
    copied = []
    for name in ("icon.png", "icon_256.png"):
        src = os.path.join(source, name)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(assets, name))
            copied.append(name)
    return copied


def _wj(root, rel, obj):
    _w(root, rel, json.dumps(obj, indent=2))


# ---------------------------------------------------------------------------
# Geometry templates
# ---------------------------------------------------------------------------

def _quadruped_geo(mob_id, w, h, glow):
    """Standard quadruped-ish geometry scaled to the mob size."""
    bw = int(round(w * 8))
    bh = int(round(h * 8))
    head = max(4, bw - 1)
    return {
        "format_version": "1.12.0",
        "minecraft:geometry": [{
            "description": {
                "identifier": "geometry." + mob_id,
                "texture_width": 32,
                "texture_height": 32,
                "visible_bounds_width": 3,
                "visible_bounds_height": 3,
                "visible_bounds_offset": [0, 1, 0]
            },
            "bones": [
                {"name": "root", "pivot": [0, 0, 0]},
                {"name": "body", "parent": "root", "pivot": [0, bh, 0],
                 "cubes": [{"origin": [-bw, 2, -bw], "size": [bw * 2, bh, bw * 2 - 1],
                            "uv": [16, 16]}]},
                {"name": "head", "parent": "body", "pivot": [0, bh + 4, -bw - 1],
                 "cubes": [{"origin": [-head // 2, bh, -bw - head], "size": [head, head, head],
                            "uv": [0, 0]}]},
                {"name": "leg0", "parent": "root", "pivot": [-bw + 1, 8, bw - 2],
                 "cubes": [{"origin": [-bw, 0, bw - 3], "size": [3, 8, 3], "uv": [0, 16]}]},
                {"name": "leg1", "parent": "root", "pivot": [bw - 1, 8, bw - 2],
                 "cubes": [{"origin": [bw - 3, 0, bw - 3], "size": [3, 8, 3], "uv": [0, 16]}]},
                {"name": "leg2", "parent": "root", "pivot": [-bw + 1, 8, -bw + 1],
                 "cubes": [{"origin": [-bw, 0, -bw], "size": [3, 8, 3], "uv": [0, 16]}]},
                {"name": "leg3", "parent": "root", "pivot": [bw - 1, 8, -bw + 1],
                 "cubes": [{"origin": [bw - 3, 0, -bw], "size": [3, 8, 3], "uv": [0, 16]}]},
            ]
        }]
    }


def _bird_geo(mob_id, w, h):
    bw = max(3, int(round(w * 6)))
    return {
        "format_version": "1.12.0",
        "minecraft:geometry": [{
            "description": {
                "identifier": "geometry." + mob_id,
                "texture_width": 32,
                "texture_height": 32,
                "visible_bounds_width": 3,
                "visible_bounds_height": 3,
                "visible_bounds_offset": [0, 1, 0]
            },
            "bones": [
                {"name": "root", "pivot": [0, 0, 0]},
                {"name": "body", "parent": "root", "pivot": [0, 12, 0],
                 "cubes": [{"origin": [-bw, 12 - bw, -bw], "size": [bw * 2, bw * 2, bw * 3],
                            "uv": [0, 0]}]},
                {"name": "head", "parent": "body", "pivot": [0, 14, -bw - 1],
                 "cubes": [{"origin": [-3, 11, -bw - 5], "size": [6, 6, 6], "uv": [0, 10]}]},
                {"name": "wing0", "parent": "body", "pivot": [-bw - 1, 13, 0],
                 "cubes": [{"origin": [-bw - 11, 11, -4], "size": [11, 2, 10], "uv": [16, 0]}]},
                {"name": "wing1", "parent": "body", "pivot": [bw + 1, 13, 0],
                 "cubes": [{"origin": [bw, 11, -4], "size": [11, 2, 10], "uv": [16, 0]}]},
                {"name": "tail", "parent": "body", "pivot": [0, 12, bw * 2],
                 "cubes": [{"origin": [-2, 10, bw * 2], "size": [4, 2, 8], "uv": [0, 22]}]},
            ]
        }]
    }


def _serpent_geo():
    bones = [{"name": "root", "pivot": [0, 0, 0]}]
    for i in range(8):
        bones.append({
            "name": "segment%d" % i,
            "parent": "root" if i == 0 else "segment%d" % (i - 1),
            "pivot": [0, 12, -8 * i],
            "cubes": [{"origin": [-5, 7, -8 * i - 8], "size": [10, 10, 10], "uv": [0, 0]}],
        })
    bones.append({"name": "head", "parent": "segment0", "pivot": [0, 13, -12],
                  "cubes": [{"origin": [-6, 6, -24], "size": [12, 12, 14], "uv": [0, 12]}]})
    bones.append({"name": "jaw", "parent": "head", "pivot": [0, 8, -24],
                  "cubes": [{"origin": [-4, 3, -30], "size": [8, 4, 8], "uv": [16, 0]}]})
    return {
        "format_version": "1.12.0",
        "minecraft:geometry": [{
            "description": {
                "identifier": "geometry.void_serpent",
                "texture_width": 64,
                "texture_height": 32,
                "visible_bounds_width": 8,
                "visible_bounds_height": 6,
                "visible_bounds_offset": [0, 2, 0]
            },
            "bones": bones
        }]
    }


def _heart_geo():
    return {
        "format_version": "1.12.0",
        "minecraft:geometry": [{
            "description": {
                "identifier": "geometry.heart_of_the_forest",
                "texture_width": 64,
                "texture_height": 64,
                "visible_bounds_width": 8,
                "visible_bounds_height": 10,
                "visible_bounds_offset": [0, 3, 0]
            },
            "bones": [
                {"name": "root", "pivot": [0, 0, 0]},
                {"name": "trunk", "parent": "root", "pivot": [0, 20, 0],
                 "cubes": [{"origin": [-10, 0, -10], "size": [20, 34, 20], "uv": [0, 0]}]},
                {"name": "heart", "parent": "trunk", "pivot": [0, 26, -11],
                 "cubes": [{"origin": [-5, 21, -16], "size": [10, 10, 8], "uv": [0, 55]}]},
                {"name": "branch0", "parent": "trunk", "pivot": [-12, 30, 0],
                 "cubes": [{"origin": [-34, 28, -3], "size": [24, 6, 6], "uv": [20, 40]}]},
                {"name": "branch1", "parent": "trunk", "pivot": [12, 30, 0],
                 "cubes": [{"origin": [10, 28, -3], "size": [24, 6, 6], "uv": [20, 40]}]},
                {"name": "roots0", "parent": "root", "pivot": [-12, 2, -8],
                 "cubes": [{"origin": [-26, 0, -12], "size": [18, 6, 8], "uv": [30, 55]}]},
                {"name": "roots1", "parent": "root", "pivot": [12, 2, -8],
                 "cubes": [{"origin": [8, 0, -12], "size": [18, 6, 8], "uv": [30, 55]}]},
            ]
        }]
    }


def _block_geo(block_id):
    return {
        "format_version": "1.12.0",
        "minecraft:geometry": [{
            "description": {
                "identifier": "geometry." + block_id,
                "texture_width": 16,
                "texture_height": 16,
                "visible_bounds_width": 2,
                "visible_bounds_height": 2,
                "visible_bounds_offset": [0, 0.5, 0]
            },
            "bones": [
                {"name": "root", "pivot": [0, 0, 0]},
                {"name": "cube", "parent": "root", "pivot": [0, 8, 0],
                 "cubes": [{"origin": [-8, 0, -8], "size": [16, 16, 16], "uv": [0, 0]}]},
                {"name": "crystals", "parent": "cube", "pivot": [0, 16, 0],
                 "cubes": [
                     {"origin": [-6, 14, -6], "size": [3, 7, 3], "uv": [0, 0]},
                     {"origin": [3, 14, 3], "size": [3, 5, 3], "uv": [0, 8]},
                 ]},
            ]
        }]
    }


# ---------------------------------------------------------------------------
# Animation clips
# ---------------------------------------------------------------------------

def _clip(length, looping, bone_keys):
    clip = {"animation_length": length, "loop": looping, "bones": bone_keys}
    return clip


def _mob_anims(mob_id, anims, is_bird, is_serpent):
    """Build the complete animation dictionary for one mob/boss."""
    out = {}
    prefix = "animation." + mob_id + "."

    def legs_swing(speed, amp):
        return {
            "leg0": {"rotation": {"0.0": [0, 0, 0], "%s" % (speed / 2): [amp, 0, 0], str(speed): [0, 0, 0]}},
            "leg1": {"rotation": {"0.0": [0, 0, 0], "%s" % (speed / 2): [-amp, 0, 0], str(speed): [0, 0, 0]}},
            "leg2": {"rotation": {"0.0": [0, 0, 0], "%s" % (speed / 2): [-amp, 0, 0], str(speed): [0, 0, 0]}},
            "leg3": {"rotation": {"0.0": [0, 0, 0], "%s" % (speed / 2): [amp, 0, 0], str(speed): [0, 0, 0]}},
        }

    def wings(speed, amp):
        return {
            "wing0": {"rotation": {"0.0": [0, 0, 0], "%s" % (speed / 2): [0, 0, -amp], str(speed): [0, 0, 0]}},
            "wing1": {"rotation": {"0.0": [0, 0, 0], "%s" % (speed / 2): [0, 0, amp], str(speed): [0, 0, 0]}},
        }

    def breathe(period):
        return {
            "body": {"scale": {"0.0": [1, 1, 1], "%s" % (period / 2): [1.02, 1.04, 1.02],
                               str(period): [1, 1, 1]}},
            "head": {"rotation": {"0.0": [0, 0, 0], "%s" % (period / 2): [1.5, 0, 0], str(period): [0, 0, 0]}},
        }

    for anim in anims:
        name = prefix + anim
        if anim == "idle":
            if is_serpent:
                out[name] = _clip(3.0, True, {
                    "segment0": {"rotation": {"0.0": [0, 0, 0], "1.5": [0, 8, 5], "3.0": [0, 0, 0]}},
                    "segment1": {"rotation": {"0.0": [0, 0, 0], "1.2": [0, -8, -5], "3.0": [0, 0, 0]}},
                    "segment2": {"rotation": {"0.0": [0, 0, 0], "1.8": [0, 8, 5], "3.0": [0, 0, 0]}},
                    "head": {"rotation": {"0.0": [0, 0, 0], "1.5": [4, 0, 0], "3.0": [0, 0, 0]}},
                    "jaw": {"rotation": {"0.0": [0, 0, 0], "2.2": [8, 0, 0], "3.0": [0, 0, 0]}},
                })
            elif "branch0" in str(anims):
                out[name] = _clip(4.0, True, breathe(4.0))
            elif is_bird:
                out[name] = _clip(2.5, True, {
                    "body": {"rotation": {"0.0": [0, 0, 0], "1.25": [2, 0, 0], "2.5": [0, 0, 0]}},
                    "head": {"rotation": {"0.0": [0, 0, 0], "0.8": [0, 12, 0], "1.6": [0, -8, 0], "2.5": [0, 0, 0]}},
                    **wings(2.5, 6),
                })
            else:
                out[name] = _clip(3.0, True, breathe(3.0))
        elif anim == "walk":
            if is_serpent:
                out[name] = _clip(1.2, True, {
                    "segment0": {"rotation": {"0.0": [0, 0, 0], "0.6": [0, 18, 0], "1.2": [0, 0, 0]}},
                    "segment1": {"rotation": {"0.0": [0, 0, 0], "0.5": [0, -18, 0], "1.2": [0, 0, 0]}},
                    "segment2": {"rotation": {"0.0": [0, 0, 0], "0.7": [0, 18, 0], "1.2": [0, 0, 0]}},
                    "head": {"rotation": {"0.0": [0, 0, 0], "0.6": [0, -10, 0], "1.2": [0, 0, 0]}},
                })
            elif is_bird:
                out[name] = _clip(1.0, True, wings(1.0, 12))
            else:
                out[name] = _clip(1.0, True, legs_swing(1.0, 22))
        elif anim == "run":
            if is_bird:
                out[name] = _clip(0.55, True, wings(0.55, 32))
            else:
                out[name] = _clip(0.6, True, legs_swing(0.6, 32))
        elif anim in ("fly", "soar", "glide", "swim", "swim_air", "dance"):
            out[name] = _clip(1.6, True, {
                "body": {"rotation": {"0.0": [0, 0, 0], "0.8": [3, 0, 4], "1.6": [0, 0, 0]}},
                **wings(1.6, 18 if anim != "glide" else 3),
            })
        elif anim in ("attack", "pounce", "headbutt", "charge", "slam", "tail_sweep"):
            out[name] = _clip(0.8, False, {
                "body": {"rotation": {"0.0": [0, 0, 0], "0.25": [-14, 0, 0], "0.55": [18, 0, 0], "0.8": [0, 0, 0]}},
                "head": {"rotation": {"0.0": [0, 0, 0], "0.3": [16, 0, 0], "0.8": [0, 0, 0]}},
            })
        elif anim in ("graze", "eat", "pollinate"):
            out[name] = _clip(2.2, False, {
                "head": {"rotation": {"0.0": [0, 0, 0], "0.7": [38, 0, 0], "1.6": [34, 0, 0], "2.2": [0, 0, 0]}},
                "body": {"rotation": {"0.0": [0, 0, 0], "1.1": [4, 0, 0], "2.2": [0, 0, 0]}},
            })
        elif anim in ("sit", "shell", "fortify", "burrow", "lurk"):
            out[name] = _clip(1.2, False, {
                "body": {"position": {"0.0": [0, 0, 0], "0.6": [0, -3, 0], "1.2": [0, -3, 0]},
                         "rotation": {"0.0": [0, 0, 0], "0.6": [10, 0, 0], "1.2": [10, 0, 0]}},
                "head": {"rotation": {"0.0": [0, 0, 0], "0.6": [-6, 0, 0], "1.2": [-6, 0, 0]}},
            })
        elif anim in ("flee", "skitter", "hop"):
            out[name] = _clip(0.7, False, {
                "body": {"position": {"0.0": [0, 0, 0], "0.25": [0, 4, 0], "0.55": [0, 0, 0], "0.7": [0, 0, 0]}},
                **legs_swing(0.7, 26),
            })
        elif anim in ("hurt",):
            out[name] = _clip(0.4, False, {
                "body": {"rotation": {"0.0": [0, 0, 0], "0.12": [0, 0, 12], "0.28": [0, 0, -8], "0.4": [0, 0, 0]}},
            })
        elif anim in ("death",):
            out[name] = _clip(1.2, False, {
                "root": {"rotation": {"0.0": [0, 0, 0], "0.9": [0, 0, -88], "1.2": [0, 0, -90]},
                         "position": {"0.0": [0, 0, 0], "1.2": [0, -2, 0]}},
            })
        elif anim in ("howl", "roar", "beam", "cast", "rift_barrage", "devour", "gravity_well",
                      "void_beam", "spore_cloud", "verdant_beam", "quake_stomp", "summon",
                      "awaken", "wrath", "final_bloom", "phase_shift", "unmaking", "frenzy"):
            out[name] = _clip(1.4, False, {
                "body": {"rotation": {"0.0": [0, 0, 0], "0.45": [-22, 0, 0], "1.0": [-16, 0, 0], "1.4": [0, 0, 0]}},
                "head": {"rotation": {"0.0": [0, 0, 0], "0.4": [-28, 0, 0], "1.4": [0, 0, 0]}},
            })
        elif anim in ("bloom", "spore_burst", "ember_burst", "heal", "pulse", "trade", "tame",
                      "beg", "fetch", "build", "mire_step", "resonate", "dance_joy"):
            out[name] = _clip(1.5, False, {
                "body": {"scale": {"0.0": [1, 1, 1], "0.5": [1.08, 1.12, 1.08], "1.5": [1, 1, 1]},
                         "rotation": {"0.0": [0, 0, 0], "0.5": [0, 8, 0], "1.5": [0, 0, 0]}},
            })
        elif anim in ("follow_herd", "guard_herd", "pack_tactics", "ambush", "intimidate",
                      "stalk", "terrain_use", "barter", "wander_trade", "reflect_damage",
                      "fire_immune", "water_walk", "water_affinity", "water_herd", "tide_pull",
                      "heal_allies", "shock_on_hit", "plant_self", "spread_spores", "attracted_to_light",
                      "attracted_to_flowers", "follow_weather", "gentle_giant", "levitate",
                      "flee_when_alone", "swarm_day", "swarm", "night_hunt", "build_mounds",
                      "light_aura", "call_pack", "ambient_fly"):
            # Behaviour flags are AI-level; give them a gentle presence clip so
            # every listed animation name resolves in the animation file.
            out[name] = _clip(2.0, True, breathe(2.0))
        else:
            out[name] = _clip(1.8, True, breathe(1.8))
    return out


def _boss_anims(boss_id, phases, attacks):
    anims = list(phases) + list(attacks) + ["idle", "walk", "run", "hurt", "death"]
    out = _mob_anims(boss_id, anims, False, boss_id == "void_serpent")
    if boss_id == "heart_of_the_forest":
        out["animation.heart_of_the_forest.wrath_idle"] = _clip(2.2, True, {
            "trunk": {"rotation": {"0.0": [0, 0, 0], "1.1": [0, 2, 2], "2.2": [0, 0, 0]}},
            "branch0": {"rotation": {"0.0": [0, 0, 0], "0.7": [0, 0, -12], "1.5": [0, 0, 8], "2.2": [0, 0, 0]}},
            "branch1": {"rotation": {"0.0": [0, 0, 0], "0.7": [0, 0, 12], "1.5": [0, 0, -8], "2.2": [0, 0, 0]}},
            "heart": {"scale": {"0.0": [1, 1, 1], "1.1": [1.15, 1.15, 1.15], "2.2": [1, 1, 1]}},
        })
        out["animation.heart_of_the_forest.idle"] = _clip(4.0, True, {
            "trunk": {"rotation": {"0.0": [0, 0, 0], "2.0": [0, 1.5, 1.5], "4.0": [0, 0, 0]}},
            "heart": {"scale": {"0.0": [1, 1, 1], "1.0": [1.12, 1.12, 1.12], "2.0": [1, 1, 1],
                                "3.0": [1.12, 1.12, 1.12], "4.0": [1, 1, 1]}},
            "branch0": {"rotation": {"0.0": [0, 0, 0], "2.0": [0, 0, -5], "4.0": [0, 0, 0]}},
            "branch1": {"rotation": {"0.0": [0, 0, 0], "2.0": [0, 0, 5], "4.0": [0, 0, 0]}},
        })
        out["animation.heart_of_the_forest.walk"] = _clip(2.4, True, {
            "roots0": {"rotation": {"0.0": [0, 0, 0], "0.6": [-14, 0, 0], "1.2": [0, 0, 0],
                                    "1.8": [-14, 0, 0], "2.4": [0, 0, 0]}},
            "roots1": {"rotation": {"0.0": [0, 0, 0], "0.6": [-14, 0, 0], "1.2": [0, 0, 0],
                                    "1.8": [-14, 0, 0], "2.4": [0, 0, 0]}},
            "trunk": {"position": {"0.0": [0, 0, 0], "0.6": [0, 2, 0], "1.2": [0, 0, 0],
                                   "1.8": [0, 2, 0], "2.4": [0, 0, 0]}},
        })
    if boss_id == "void_serpent":
        out["animation.void_serpent.swim"] = _clip(1.2, True, {
            "segment0": {"rotation": {"0.0": [0, 0, 0], "0.6": [0, 22, 0], "1.2": [0, 0, 0]}},
            "segment1": {"rotation": {"0.0": [0, 0, 0], "0.5": [0, -22, 0], "1.2": [0, 0, 0]}},
            "segment2": {"rotation": {"0.0": [0, 0, 0], "0.7": [0, 22, 0], "1.2": [0, 0, 0]}},
            "segment3": {"rotation": {"0.0": [0, 0, 0], "0.5": [0, -22, 0], "1.2": [0, 0, 0]}},
            "head": {"rotation": {"0.0": [0, 0, 0], "0.6": [0, -12, 0], "1.2": [0, 0, 0]}},
        })
        out["animation.void_serpent.frenzy_swim"] = _clip(0.7, True, {
            "segment0": {"rotation": {"0.0": [0, 0, 0], "0.35": [0, 34, 0], "0.7": [0, 0, 0]}},
            "segment1": {"rotation": {"0.0": [0, 0, 0], "0.3": [0, -34, 0], "0.7": [0, 0, 0]}},
            "segment2": {"rotation": {"0.0": [0, 0, 0], "0.4": [0, 34, 0], "0.7": [0, 0, 0]}},
            "jaw": {"rotation": {"0.0": [0, 0, 0], "0.35": [22, 0, 0], "0.7": [6, 0, 0]}},
        })
        out["animation.void_serpent.phase_shift"] = _clip(1.0, False, {
            "root": {"scale": {"0.0": [1, 1, 1], "0.35": [0.6, 0.6, 0.6], "0.55": [0.2, 0.2, 0.2],
                               "0.75": [0.7, 0.7, 0.7], "1.0": [1, 1, 1]}},
            "head": {"rotation": {"0.0": [0, 0, 0], "0.5": [0, 360, 0], "1.0": [0, 720, 0]}},
        })
        out["animation.void_serpent.idle"] = _clip(3.0, True, {
            "segment0": {"rotation": {"0.0": [0, 0, 0], "1.5": [0, 12, 6], "3.0": [0, 0, 0]}},
            "segment1": {"rotation": {"0.0": [0, 0, 0], "1.3": [0, -12, -6], "3.0": [0, 0, 0]}},
            "segment2": {"rotation": {"0.0": [0, 0, 0], "1.7": [0, 12, 6], "3.0": [0, 0, 0]}},
            "head": {"rotation": {"0.0": [0, 0, 0], "1.5": [5, 0, 0], "3.0": [0, 0, 0]}},
            "jaw": {"rotation": {"0.0": [0, 0, 0], "2.3": [10, 0, 0], "3.0": [0, 0, 0]}},
        })
    return out


def emit(root):
    emit_logo(root)
    A = "common/src/main/resources/assets/biomesunseen"
    D = "common/src/main/resources/data/biomesunseen"

    # ---------------- lang ----------------
    lang = {"itemGroup.biomesunseen": "Biomes Unseen"}
    for (bid, display, *_r) in BIOME_ROWS:
        lang["biome.biomesunseen." + bid] = display
    for (oid, display, *_r) in ORE_ROWS:
        lang["block.biomesunseen." + oid + "_ore"] = display + " Ore"
        lang["item.biomesunseen." + oid] = display
        for suffix, label in (("_pickaxe", " Pickaxe"), ("_sword", " Sword"),
                              ("_helmet", " Helmet"), ("_chestplate", " Chestplate"),
                              ("_leggings", " Leggings"), ("_boots", " Boots"),
                              ("_tonic", " Tonic")):
            lang["item.biomesunseen." + oid + suffix] = display + label
    for (did, display, *_r) in DECOR_ROWS:
        lang["block.biomesunseen." + did] = display
    for (pid, display, *_r) in PLANT_ROWS:
        lang["block.biomesunseen." + pid] = display
    for (mid, display, *_r) in MOB_ROWS:
        lang["entity.biomesunseen." + mid] = display
        lang["item.biomesunseen." + mid + "_spawn_egg"] = display + " Spawn Egg"
        lang["item.biomesunseen." + mid + "_trophy"] = display + " Trophy"
    for (bid, display, *_r) in BOSS_ROWS:
        lang["entity.biomesunseen." + bid] = display
        lang["item.biomesunseen." + bid + "_spawn_egg"] = display + " Spawn Egg"
    lang["item.biomesunseen.unseen_sigil"] = "Unseen Sigil"
    for tier in range(1, 5):
        lang["item.biomesunseen.machine_core_t%d" % tier] = "Machine Core T%d" % tier
    for row in STRUCTURE_ROWS:
        lang["structure.biomesunseen." + row[0]] = row[1]
        lang["book.biomesunseen." + row[13]] = "Journal of the " + row[13].replace("_", " ").title()
    for key, _typ, _d, comment in CONFIG_ROWS:
        lang["biomesunseen.config." + key] = key
    for se in SOUND_EVENTS:
        lang["subtitles." + se.split(".", 1)[-1] if se.startswith("subtitles.") else
             "subtitles." + se] = se
    _wj(root, A + "/lang/en_us.json", lang)

    # ---------------- sounds.json ----------------
    sounds = {}
    for se in SOUND_EVENTS:
        sound_entry = {"subtitle": "subtitles.biomesunseen." + se.split(".")[-1]}
        if se.startswith("music."):
            sound_entry["sounds"] = [{"sound": "biomesunseen:" + se.replace(".", "/"),
                                      "stream": True}]
        else:
            sound_entry["sounds"] = ["biomesunseen:" + se.replace(".", "/")]
        sounds[se] = sound_entry
    _wj(root, A + "/sounds.json", sounds)

    # ---------------- blockstates + models ----------------
    states = A + "/blockstates"
    bmodels = A + "/models/block"
    imodels = A + "/models/item"
    all_ids = ([(o[0] + "_ore", "block", "cube_all") for o in ORE_ROWS]
               + [(d[0], "block", "cube_all") for d in DECOR_ROWS]
               + [(p[0], "block", "cross") for p in PLANT_ROWS])
    for bid, _kind, parent in all_ids:
        _wj(root, states + "/%s.json" % bid,
            {"variants": {"": {"model": "biomesunseen:block/" + bid}}})
        if parent == "cube_all":
            _wj(root, bmodels + "/%s.json" % bid,
                {"parent": "minecraft:block/cube_all",
                 "textures": {"all": "biomesunseen:block/" + bid}})
        else:
            _wj(root, bmodels + "/%s.json" % bid,
                {"parent": "minecraft:block/cross",
                 "textures": {"cross": "biomesunseen:block/" + bid}})

    def flat_item(item_id, texture):
        _wj(root, imodels + "/%s.json" % item_id,
            {"parent": "minecraft:item/generated",
             "textures": {"layer0": texture}})

    for (oid, display, *_r) in ORE_ROWS:
        for suffix in ("", "_pickaxe", "_sword", "_helmet", "_chestplate",
                       "_leggings", "_boots", "_tonic"):
            flat_item(oid + suffix, "biomesunseen:item/" + oid + suffix)
    for (mid, *_r) in MOB_ROWS:
        flat_item(mid + "_spawn_egg", "minecraft:item/template_spawn_egg")
        flat_item(mid + "_trophy", "biomesunseen:item/" + mid + "_trophy")
    for (bid, *_r) in BOSS_ROWS:
        flat_item(bid + "_spawn_egg", "minecraft:item/template_spawn_egg")
    for tier in range(1, 5):
        flat_item("machine_core_t%d" % tier, "biomesunseen:item/machine_core_t%d" % tier)
    flat_item("unseen_sigil", "biomesunseen:item/unseen_sigil")
    themes = sorted({row[13] for row in STRUCTURE_ROWS})
    for theme in themes:
        flat_item("lore_journal_" + theme, "biomesunseen:item/lore_journal_" + theme)

    # ---------------- textures ----------------
    tblock = A + "/textures/block"
    titem = A + "/textures/item"
    tentity = A + "/textures/entity"
    tpart = A + "/textures/particle"
    for idx, (oid, display, color, pcolor, *_r) in enumerate(ORE_ROWS):
        pnggen.write_png(os.path.join(root, tblock, oid + "_ore.png"),
                         pnggen.ore_texture(color, pcolor, 1000 + idx), 16, 16)
        pnggen.write_png(os.path.join(root, titem, oid + ".png"),
                         pnggen.item_texture(color, 2000 + idx, "blob"), 16, 16)
        pnggen.write_png(os.path.join(root, titem, oid + "_pickaxe.png"),
                         pnggen.item_texture(color, 2100 + idx, "ingot"), 16, 16)
        pnggen.write_png(os.path.join(root, titem, oid + "_sword.png"),
                         pnggen.item_texture(color, 2200 + idx, "blob"), 16, 16)
        for suffix in ("_helmet", "_chestplate", "_leggings", "_boots"):
            pnggen.write_png(os.path.join(root, titem, oid + suffix + ".png"),
                             pnggen.item_texture(color, 2300 + idx, "ingot"), 16, 16)
        pnggen.write_png(os.path.join(root, titem, oid + "_tonic.png"),
                         pnggen.item_texture(pcolor, 2400 + idx, "blob"), 16, 16)
    for idx, (did, display, color, sound, material) in enumerate(DECOR_ROWS):
        style = "glass" if sound == "glass" else ("brick" if "brick" in did or "block" in did
                                                  else ("plank" if material == "wood" else "noise"))
        pnggen.write_png(os.path.join(root, tblock, did + ".png"),
                         pnggen.block_texture(color, 3000 + idx, style), 16, 16)
    for idx, (pid, display, color, *_r) in enumerate(PLANT_ROWS):
        pnggen.write_png(os.path.join(root, tblock, pid + ".png"),
                         pnggen.block_texture(color, 3500 + idx, "cross"), 16, 16)
    for idx, (mid, display, cat, hp, spd, atk, defn, w, h, behaviors, tame, trade,
              pack, herd, flees, terrain, bg, weight, night, anims, color, glow) in enumerate(MOB_ROWS):
        accent = (color // 2) & 0xFFFFFF
        pnggen.write_png(os.path.join(root, tentity, mid + ".png"),
                         pnggen.entity_texture(color, 4000 + idx, accent), 32, 32)
        pnggen.write_png(os.path.join(root, titem, mid + "_trophy.png"),
                         pnggen.item_texture(color, 4500 + idx, "blob"), 16, 16)
    for idx, (bid, display, hp, spd, atk, w, h, arena, music, phases, attacks, loot,
              grp, color, glow) in enumerate(BOSS_ROWS):
        pnggen.write_png(os.path.join(root, tentity, bid + ".png"),
                         pnggen.entity_texture(color, 5000 + idx, (color // 3) & 0xFFFFFF), 32, 32)
    for idx, p in enumerate(PARTICLE_TYPES):
        color = [0x80FFF0, 0xFFB060, 0x9A40D0, 0xC8A832, 0xC0F0FF, 0xFFFFA0,
                 0xFF9AC8, 0x88FF88][idx]
        pnggen.write_png(os.path.join(root, tpart, p + ".png"),
                         pnggen.particle_texture(color), 8, 8)
    pnggen.write_png(os.path.join(root, titem, "unseen_sigil.png"),
                     pnggen.gui_icon_texture(0x9AF0E0, 6001), 16, 16)
    for idx in range(1, 5):
        pnggen.write_png(os.path.join(root, titem, "machine_core_t%d.png" % idx),
                         pnggen.item_texture(0xC0C8D0 + idx * 0x080808, 6100 + idx, "ingot"), 16, 16)
    for idx, theme in enumerate(themes):
        pnggen.write_png(os.path.join(root, titem, "lore_journal_%s.png" % theme),
                         pnggen.item_texture(0xD8C8A0, 6200 + idx, "ingot"), 16, 16)

    # ---------------- geo + animations ----------------
    geo = A + "/geo"
    anims_dir = A + "/animations"
    for (mid, display, cat, hp, spd, atk, defn, w, h, behaviors, tame, trade,
         pack, herd, flees, terrain, bg, weight, night, anims, color, glow) in MOB_ROWS:
        is_bird = "fly" in anims or "flutter" in anims or "glide" in anims
        if is_bird:
            g = _bird_geo(mid, w, h)
        else:
            g = _quadruped_geo(mid, w, h, glow)
        _wj(root, geo + "/%s.geo.json" % mid, g)
        _wj(root, anims_dir + "/%s.animation.json" % mid,
            {"format_version": "1.8.0",
             "animations": _mob_anims(mid, anims, is_bird, False)})
    # Bosses
    _wj(root, geo + "/heart_of_the_forest.geo.json", _heart_geo())
    _wj(root, geo + "/void_serpent.geo.json", _serpent_geo())
    for (bid, display, hp, spd, atk, w, h, arena, music, phases, attacks, loot,
         grp, color, glow) in BOSS_ROWS:
        _wj(root, anims_dir + "/%s.animation.json" % bid,
            {"format_version": "1.8.0",
             "animations": _boss_anims(bid, phases, attacks)})
    # Animated blocks: crystal_shard_block, glowcap_block, nullglass
    for block_id in ("crystal_shard_block", "glowcap_block", "nullglass"):
        _wj(root, geo + "/%s.geo.json" % block_id, _block_geo(block_id))
        _wj(root, anims_dir + "/%s.animation.json" % block_id,
            {"format_version": "1.8.0",
             "animations": {
                 "animation.%s.pulse" % block_id: {
                     "animation_length": 2.0,
                     "loop": True,
                     "bones": {
                         "cube": {"scale": {"0.0": [1, 1, 1], "1.0": [1.04, 1.06, 1.04],
                                            "2.0": [1, 1, 1]}},
                         "crystals": {
                             "rotation": {"0.0": [0, 0, 0], "1.0": [0, 12, 0], "2.0": [0, 0, 0]},
                             "scale": {"0.0": [1, 1, 1], "1.0": [1.12, 1.12, 1.12],
                                       "2.0": [1, 1, 1]}},
                     },
                 },
                 "animation.%s.glow" % block_id: {
                     "animation_length": 3.0,
                     "loop": True,
                     "bones": {
                         "cube": {"scale": {"0.0": [1, 1, 1], "1.5": [1.08, 1.08, 1.08],
                                            "3.0": [1, 1, 1]}},
                     },
                 },
             }})
    # Placeholder ogg references: sounds.json points at
    # assets/biomesunseen/sounds/*.ogg; ship a sounds/README so the folder
    # exists and audio can be dropped in without touching code.
    _w(root, A + "/sounds/README.md",
       "# Sound files\n\nPlace .ogg files here using the paths referenced by sounds.json "
       "(e.g. `music/boss_heart.ogg`, `ambient/crystal_loop.ogg`). "
       "Missing files fall back to silence without errors.\n")
