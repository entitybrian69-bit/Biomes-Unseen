"""
content -- the single source of truth for Biomes Unseen.

Everything in the mod is described here as data:

    biomes.py      80 Overworld biomes + 20 per dimension (140 total)
    mobs.py        55 mobs + 5 bosses
    ores.py        20 Overworld ores + 24 dimension ores (44 total)
    gear.py        tool & armour sets derived from the ores
    structures.py  30+ structures incl. 5 boss arenas

From these tables the studio build emits, deterministically:

    * the Java registry classes            (tools/codegen_java.py)
    * the DataGen-equivalent JSON          (tools/generate_data.py)
    * every texture                        (tools/generate_textures.py)

so Java, JSON and PNG can never drift apart. tools/validate.py proves it.
"""
