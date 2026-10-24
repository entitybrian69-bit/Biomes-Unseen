"""Shared palettes and 8x8 tile templates for generated mobs and ores.

PALETTES: name -> (outline, dark, mid, light).  GLOWS: name -> (glow, highlight).
TILES: 8x8 char grids; o/a/b/c = palette ramp, g/w = glow accent.
HOSTS: ore host-stone ramps (outline, light, mid, dark).
"""

PALETTES = {
    "moss": ("#0F1A10", "#1E3320", "#356B3C", "#5C9C58"),
    "root": ("#1A110A", "#3B2616", "#5E3E24", "#85603B"),
    "spore": ("#3A1F14", "#8A4B2A", "#B8703B", "#E0A064"),
    "capblue": ("#101A33", "#1F3A66", "#2F5FA8", "#5F95DC"),
    "violet": ("#17142A", "#3A3560", "#5A4A8A", "#8A7AC0"),
    "amethyst": ("#1E0F2E", "#4A2670", "#7A44B0", "#B07AE0"),
    "ash": ("#141210", "#2B2522", "#4A413C", "#7A6E66"),
    "ember": ("#2A0E06", "#6A2410", "#B04418", "#E8782A"),
    "obsidian": ("#07060C", "#14121F", "#241F3A", "#3E3660"),
    "bog": ("#0C140C", "#1E2E1E", "#34503A", "#5C8A58"),
    "mud": ("#1E1608", "#3F2F14", "#6A5226", "#96783A"),
    "frost": ("#0E1E2E", "#24506E", "#4A8CB5", "#9AD0E8"),
    "ice": ("#2A3A48", "#7A96AA", "#B8D2E2", "#EAF6FF"),
    "bone": ("#2A2418", "#6E6450", "#B4A98C", "#E8E0C8"),
    "salt": ("#3A3326", "#8C7F62", "#C8B98E", "#F0E6C0"),
    "tide": ("#07182A", "#0F3D63", "#1A6A9E", "#4AA6D4"),
    "rust": ("#1E0E08", "#4A2214", "#8A4A22", "#C07A3A"),
    "iron": ("#121418", "#2C323A", "#505A66", "#8896A4"),
    "void": ("#05030A", "#120A22", "#2A1650", "#5A32A0"),
    "coral": ("#2A0E1E", "#7A2A52", "#C04A7E", "#F28AB0"),
    "gold": ("#2A1E06", "#7A5A10", "#C89A20", "#F5D050"),
    "blood": ("#1E0508", "#5A0F1A", "#9A1E2E", "#D44A5A"),
}

GLOWS = {
    "cyan": ("#5FE0D0", "#E6FFFB"), "lime": ("#9AFF5A", "#F0FFD6"), "amber": ("#FFC24A", "#FFF3CE"),
    "magenta": ("#FF5AD0", "#FFD6F4"), "white": ("#E8F4FF", "#FFFFFF"), "red": ("#FF4A3A", "#FFD0C8"),
    "orange": ("#FF8A2A", "#FFE0BA"), "violet": ("#B066FF", "#EBD0FF"), "teal": ("#2AE0A0", "#CCFFEB"),
    "gold": ("#FFE15A", "#FFF8CC"), "blue": ("#5A9AFF", "#D6E6FF"), "green": ("#7CFFB2", "#D6FFE9"),
}

HOSTS = {
    "stone": ("#3B3B3B", "#8A8A8A", "#747474", "#5C5C5C"),
    "deepslate": ("#1C1C22", "#4E4E58", "#3C3C46", "#2C2C34"),
    "tuff": ("#3C4236", "#7A8070", "#666C5C", "#50564A"),
    "dark": ("#120F14", "#3A3340", "#2A242F", "#1E1922"),
}

TILES = {
    "face_a": ["oooooooo", "occcbbbo", "ocbbbbbo", "obgbbgbo", "obgbbgbo", "obbbbbbo", "obbaabbo", "oooooooo"],
    "face_b": ["oooooooo", "ocbbbbbo", "oabbbbao", "obgbbgbo", "obbbbbbo", "oabaabao", "obbbbbbo", "oooooooo"],
    "face_c": ["oooooooo", "occcbbbo", "ocbbbbbo", "obbggbbo", "obbggbbo", "obbbbbbo", "obaaaabo", "oooooooo"],
    "face_d": ["oooooooo", "occcbbbo", "ocgbbgbo", "obbbbbbo", "obgbbgbo", "obbbbbbo", "obaaaabo", "oooooooo"],
    "face_e": ["oooooooo", "occcbbbo", "oaaaaaao", "oggggggo", "oaaaaaao", "obbbbbbo", "obabbabo", "oooooooo"],
    "hide_a": ["oooooooo", "occbbbbo", "ocbbabbo", "obbbbbbo", "obabbbao", "obbbbabo", "obbabbbo", "oooooooo"],
    "hide_b": ["oooooooo", "occbbbbo", "ocbbbbbo", "oaaaaaao", "obbbbbbo", "obbbbbbo", "oaaaaaao", "oooooooo"],
    "hide_c": ["oooooooo", "occbbbbo", "ocbbgbbo", "obbgbbbo", "obbbgbbo", "obbbbgbo", "obbbbbbo", "oooooooo"],
    "hide_d": ["oooooooo", "ocbcbcbo", "oabababo", "obcbcbco", "oabababo", "ocbcbcbo", "oabababo", "oooooooo"],
    "hide_e": ["oooooooo", "occbbbbo", "ocbbbbbo", "obbaabbo", "obaccabo", "obbaabbo", "obbbbbbo", "oooooooo"],
    "dark_a": ["oooooooo", "oaaaaaao", "oaabaaao", "oaaaaaao", "oabaaabo", "oaaaaaao", "oaaabaao", "oooooooo"],
    "glow_a": ["oooooooo", "oaggggao", "ogwwwwgo", "ogwwwwgo", "ogwwwwgo", "ogwwwwgo", "oaggggao", "oooooooo"],
}
for _name, _grid in TILES.items():
    assert len(_grid) == 8 and all(len(r) == 8 for r in _grid), _name
