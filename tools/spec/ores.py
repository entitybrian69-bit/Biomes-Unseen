"""44 ores: hollowite (hand-registered in Java) plus 43 generated ones.

Row: (id, name, style, palette, glow, host, layout, tier, vein, count, y_min, y_max, dim)
Block id = <id>_ore. Item id = <id>_<style>. dim: "ow" Overworld, "hd" Hollow Deep.
tier 0/1/2 -> stone/iron/diamond tool. Deep-host ("dark") ores glow faintly.
"""

HOLLOWITE = ("hollowite", "Hollowite", "ingot", "tide", "cyan", "deepslate", "A", 1, 7, 14, 8, 200, "hd")

ORES = [
    # ---- Overworld (21) ----
    ("azurite", "Azurite", "gem", "capblue", "blue", "stone", "A", 1, 6, 6, -16, 64, "ow"),
    ("malachite", "Malachite", "gem", "moss", "green", "stone", "B", 1, 6, 5, 0, 72, "ow"),
    ("peridot", "Peridot", "gem", "moss", "lime", "stone", "C", 1, 5, 4, -8, 48, "ow"),
    ("sunstone", "Sunstone", "gem", "gold", "gold", "stone", "A", 1, 5, 4, 16, 110, "ow"),
    ("moonstone", "Moonstone", "gem", "ice", "white", "stone", "B", 1, 5, 4, 24, 128, "ow"),
    ("cobaltite", "Cobaltite", "ingot", "capblue", "blue", "deepslate", "C", 2, 6, 5, -60, 0, "ow"),
    ("tinite", "Tinite", "ingot", "salt", "cyan", "stone", "A", 0, 9, 10, -8, 72, "ow"),
    ("nickelite", "Nickelite", "ingot", "iron", "white", "stone", "B", 1, 8, 7, -24, 56, "ow"),
    ("silverite", "Silverite", "ingot", "ice", "white", "deepslate", "A", 1, 7, 6, -48, 16, "ow"),
    ("platinite", "Platinite", "ingot", "ice", "cyan", "deepslate", "C", 2, 5, 3, -60, -8, "ow"),
    ("rosequartz", "Rose Quartz", "shard", "coral", "white", "stone", "B", 0, 7, 8, 0, 96, "ow"),
    ("citrine", "Citrine", "gem", "gold", "amber", "stone", "C", 1, 5, 4, -16, 40, "ow"),
    ("jadeite", "Jadeite", "gem", "moss", "teal", "stone", "A", 1, 5, 4, 0, 64, "ow"),
    ("onyxite", "Onyxite", "gem", "obsidian", "violet", "deepslate", "B", 2, 4, 3, -60, -16, "ow"),
    ("tourmaline", "Tourmaline", "gem", "coral", "magenta", "stone", "C", 1, 5, 4, -8, 56, "ow"),
    ("spinel", "Spinel", "gem", "blood", "red", "deepslate", "A", 2, 4, 3, -56, -4, "ow"),
    ("opaline", "Opaline", "shard", "salt", "cyan", "stone", "B", 0, 6, 7, 8, 100, "ow"),
    ("selenite", "Selenite", "shard", "ice", "white", "stone", "C", 0, 6, 6, 16, 120, "ow"),
    ("aetherite", "Aetherite", "crystal", "frost", "cyan", "deepslate", "A", 2, 4, 2, -60, 0, "ow"),
    ("runestone", "Runestone", "orb", "violet", "violet", "deepslate", "B", 2, 4, 2, -60, -20, "ow"),
    ("dawnstone", "Dawnstone", "gem", "spore", "orange", "stone", "C", 1, 5, 4, 32, 140, "ow"),
    # ---- Hollow Deep (22) ----
    ("emberite", "Emberite", "ingot", "ember", "orange", "dark", "A", 1, 7, 10, 8, 120, "hd"),
    ("frostite", "Frostite", "shard", "frost", "blue", "dark", "B", 1, 7, 9, 8, 200, "hd"),
    ("voidite", "Voidite", "crystal", "void", "violet", "dark", "C", 2, 5, 5, 8, 240, "hd"),
    ("sporestone", "Sporestone", "gem", "spore", "amber", "dark", "A", 0, 6, 8, 8, 160, "hd"),
    ("amberite", "Amberite", "gem", "gold", "amber", "deepslate", "B", 1, 6, 7, 16, 180, "hd"),
    ("marrowite", "Marrowite", "shard", "bone", "white", "deepslate", "C", 0, 7, 8, 8, 200, "hd"),
    ("tidestone", "Tidestone", "gem", "tide", "teal", "dark", "A", 1, 6, 6, 8, 140, "hd"),
    ("rustite", "Rustite", "ingot", "rust", "orange", "deepslate", "B", 1, 8, 9, 8, 180, "hd"),
    ("scrapite", "Scrapite", "nugget", "iron", "amber", "tuff", "C", 0, 9, 10, 8, 200, "hd"),
    ("coralite", "Coralite", "gem", "coral", "magenta", "tuff", "A", 1, 6, 6, 16, 160, "hd"),
    ("ashenite", "Ashenite", "ingot", "ash", "orange", "dark", "B", 1, 8, 9, 8, 140, "hd"),
    ("mireglass", "Mireglass", "shard", "bog", "lime", "dark", "C", 0, 7, 8, 8, 120, "hd"),
    ("prismite", "Prismite", "crystal", "amethyst", "cyan", "deepslate", "A", 2, 5, 4, 24, 220, "hd"),
    ("umbrite", "Umbrite", "ingot", "obsidian", "violet", "dark", "B", 2, 5, 4, 8, 100, "hd"),
    ("solarite", "Solarite", "gem", "gold", "gold", "dark", "C", 2, 4, 3, 100, 240, "hd"),
    ("lunarite", "Lunarite", "gem", "ice", "cyan", "dark", "A", 2, 4, 3, 100, 240, "hd"),
    ("gloomstone", "Gloomstone", "orb", "obsidian", "teal", "dark", "B", 1, 5, 5, 8, 200, "hd"),
    ("wyrmite", "Wyrmite", "ingot", "ember", "red", "dark", "C", 2, 4, 3, 8, 90, "hd"),
    ("thornite", "Thornite", "ingot", "root", "green", "tuff", "A", 1, 7, 8, 16, 200, "hd"),
    ("lumenite", "Lumenite", "crystal", "capblue", "cyan", "dark", "B", 1, 6, 6, 16, 220, "hd"),
    ("stormite", "Stormite", "gem", "violet", "blue", "dark", "C", 2, 4, 3, 120, 250, "hd"),
    ("echoite", "Echoite", "shard", "void", "white", "dark", "A", 2, 5, 4, 8, 240, "hd"),
]
