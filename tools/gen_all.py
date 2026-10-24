#!/usr/bin/env python3
"""Runs every content generator in dependency order, then validates the resources.

Install the pinned audio dependencies first: python -m pip install -r tools/requirements-audio.txt
Order: biomes -> models -> ores -> structures -> textures -> synthesized audio -> data assets -> validate.
Usage: python tools/gen_all.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["gen_biomes.py", "gen_models.py", "gen_ores.py", "gen_structure_set.py",
         "gen_structures.py", "gen_textures.py", "gen_audio.py",
         "gen_datagen_assets.py", "validate.py"]


def main():
    for step in STEPS:
        print("==> " + step)
        result = subprocess.run([sys.executable, os.path.join(HERE, step)])
        if result.returncode != 0:
            sys.exit(result.returncode)


if __name__ == "__main__":
    main()
