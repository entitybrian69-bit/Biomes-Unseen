"""80 hand-designed Hollow Deep mobs (the five original mobs and the boss live in Java).

Row: (id, name, archetype, scale, palette, glow, face, hide, accessory,
      health, damage, speed, effect, theme, (drop item, min, max))
effect: None or (name, ticks, amplifier); names: poison slow blind wither weak hunger
        nausea levitate dark fire (seconds) knock freeze (ticks)
Accessories: biped horns|spikes, brute plates|crystals, quad mane, others none.
"""

MOBS = [
    # ---- heartwood ----
    ("thornback_boar", "Thornback Boar", "quad", 1.0, "root", "amber", "a", "d", "mane", 26, 5, .30, None, "heartwood", ("minecraft:porkchop", 1, 2)),
    ("barkhide_sentry", "Barkhide Sentry", "biped", 1.1, "root", "green", "e", "a", "horns", 44, 6, .26, ("slow", 40, 0), "heartwood", ("minecraft:stick", 1, 3)),
    ("leafmaw", "Leafmaw", "blob", 0.9, "moss", "lime", "c", "d", "none", 14, 3, .30, ("poison", 60, 0), "heartwood", ("minecraft:oak_sapling", 0, 1)),
    ("rootweaver", "Rootweaver", "crawler", 1.1, "root", "green", "d", "b", "none", 24, 4, .30, ("slow", 60, 1), "heartwood", ("minecraft:string", 1, 2)),
    ("canopy_stalker", "Canopy Stalker", "biped", 1.2, "moss", "lime", "b", "e", "spikes", 38, 6, .30, None, "heartwood", ("minecraft:vine", 1, 3)),
    ("sapling_wraith", "Sapling Wraith", "floater", 0.9, "moss", "green", "c", "a", "none", 24, 4, .24, ("weak", 60, 0), "heartwood", ("minecraft:bone_meal", 1, 3)),
    ("heartwood_warden", "Heartwood Warden", "brute", 1.2, "root", "green", "b", "c", "plates", 110, 12, .20, ("knock", 0, 0), "heartwood", ("minecraft:oak_log", 2, 5)),
    # ---- glowcap ----
    ("sporecap_lurker", "Sporecap Lurker", "blob", 1.2, "capblue", "cyan", "a", "a", "none", 18, 3, .28, ("poison", 80, 0), "glowcap", ("minecraft:glow_berries", 1, 3)),
    ("dusk_moth", "Dusk Moth", "floater", 0.7, "violet", "magenta", "d", "d", "none", 16, 3, .28, ("blind", 50, 0), "glowcap", ("minecraft:glowstone_dust", 0, 2)),
    ("mycelid_crawler", "Mycelid Crawler", "crawler", 1.0, "spore", "amber", "c", "e", "none", 22, 4, .31, ("hunger", 100, 0), "glowcap", ("minecraft:red_mushroom", 1, 3)),
    ("puffcap_brute", "Puffcap Brute", "brute", 1.0, "spore", "gold", "a", "d", "plates", 90, 10, .19, ("nausea", 100, 0), "glowcap", ("minecraft:brown_mushroom", 2, 4)),
    ("lantern_stalker", "Lantern Stalker", "biped", 1.0, "capblue", "cyan", "e", "b", "horns", 36, 5, .28, ("blind", 60, 0), "glowcap", ("minecraft:glow_ink_sac", 1, 2)),
    ("sporewhisper", "Sporewhisper", "floater", 1.0, "capblue", "teal", "c", "d", "none", 26, 4, .25, ("nausea", 80, 0), "glowcap", ("minecraft:fermented_spider_eye", 0, 1)),
    ("fungal_hound", "Fungal Hound", "quad", 0.9, "spore", "orange", "b", "a", "mane", 24, 5, .33, ("poison", 60, 0), "glowcap", ("minecraft:spider_eye", 1, 2)),
    # ---- crystal ----
    ("shardling", "Shardling", "blob", 0.8, "amethyst", "violet", "c", "e", "none", 12, 3, .32, None, "crystal", ("minecraft:amethyst_shard", 1, 2)),
    ("prism_crawler", "Prism Crawler", "crawler", 1.1, "amethyst", "cyan", "d", "e", "none", 26, 4, .30, ("weak", 60, 0), "crystal", ("minecraft:amethyst_shard", 1, 3)),
    ("geode_brute", "Geode Brute", "brute", 1.1, "violet", "teal", "b", "c", "crystals", 100, 11, .19, ("knock", 0, 0), "crystal", ("minecraft:amethyst_shard", 2, 5)),
    ("refraction_wraith", "Refraction Wraith", "floater", 1.0, "amethyst", "white", "e", "a", "none", 28, 5, .26, ("blind", 60, 0), "crystal", ("minecraft:quartz", 1, 2)),
    ("quartz_stalker", "Quartz Stalker", "biped", 1.0, "ice", "blue", "b", "e", "spikes", 40, 6, .29, None, "crystal", ("minecraft:quartz", 1, 3)),
    ("crystalback_basilisk", "Crystalback Basilisk", "quad", 1.1, "amethyst", "magenta", "d", "d", "mane", 44, 7, .27, ("slow", 60, 1), "crystal", ("minecraft:amethyst_shard", 1, 3)),
    ("facet_serpent", "Facet Serpent", "serpent", 1.2, "amethyst", "cyan", "e", "d", "none", 30, 5, .30, None, "crystal", ("minecraft:lapis_lazuli", 1, 3)),
    # ---- ashen ----
    ("cinder_wretch", "Cinder Wretch", "biped", 0.9, "ash", "orange", "c", "a", "none", 30, 5, .30, ("fire", 3, 0), "ashen", ("minecraft:coal", 1, 2)),
    ("ashen_hound", "Ashen Hound", "quad", 1.0, "ash", "red", "a", "b", "mane", 28, 5, .34, ("fire", 3, 0), "ashen", ("minecraft:charcoal", 1, 2)),
    ("slagback_brute", "Slagback Brute", "brute", 1.1, "ember", "orange", "b", "e", "plates", 105, 12, .19, ("fire", 5, 0), "ashen", ("minecraft:blaze_powder", 1, 3)),
    ("soot_wraith", "Soot Wraith", "floater", 0.9, "ash", "white", "c", "d", "none", 24, 4, .25, ("blind", 50, 0), "ashen", ("minecraft:gunpowder", 1, 2)),
    ("char_crawler", "Char Crawler", "crawler", 1.0, "ember", "red", "e", "a", "none", 22, 4, .32, ("fire", 2, 0), "ashen", ("minecraft:coal", 1, 3)),
    ("ember_serpent", "Ember Serpent", "serpent", 1.2, "ember", "orange", "d", "d", "none", 32, 6, .31, ("fire", 4, 0), "ashen", ("minecraft:magma_cream", 0, 2)),
    ("pyre_stalker", "Pyre Stalker", "biped", 1.2, "ember", "gold", "e", "c", "horns", 46, 7, .28, ("fire", 5, 0), "ashen", ("minecraft:blaze_rod", 0, 1)),
    # ---- mire ----
    ("bog_lurker", "Bog Lurker", "blob", 1.1, "bog", "lime", "a", "c", "none", 20, 3, .26, ("poison", 80, 0), "mire", ("minecraft:slime_ball", 1, 2)),
    ("mire_hag", "Mire Hag", "biped", 1.0, "bog", "green", "d", "a", "horns", 34, 5, .27, ("weak", 80, 0), "mire", ("minecraft:fermented_spider_eye", 0, 1)),
    ("leech_serpent", "Leech Serpent", "serpent", 1.0, "mud", "lime", "a", "d", "none", 26, 4, .30, ("hunger", 100, 1), "mire", ("minecraft:clay_ball", 1, 3)),
    ("gloomtoad", "Gloomtoad", "quad", 0.8, "bog", "teal", "c", "d", "none", 22, 4, .30, ("slow", 60, 0), "mire", ("minecraft:slime_ball", 1, 3)),
    ("sludge_brute", "Sludge Brute", "brute", 1.0, "mud", "green", "b", "b", "plates", 95, 10, .18, ("slow", 80, 1), "mire", ("minecraft:clay_ball", 2, 5)),
    ("marsh_wisp", "Marsh Wisp", "floater", 0.7, "bog", "lime", "c", "e", "none", 14, 3, .28, ("levitate", 40, 0), "mire", ("minecraft:glowstone_dust", 0, 2)),
    ("reed_crawler", "Reed Crawler", "crawler", 0.9, "mud", "amber", "d", "a", "none", 20, 3, .31, ("poison", 60, 0), "mire", ("minecraft:sugar_cane", 1, 3)),
    # ---- frost ----
    ("rime_stalker", "Rime Stalker", "biped", 1.1, "frost", "blue", "b", "e", "spikes", 40, 6, .28, ("freeze", 160, 0), "frost", ("minecraft:snowball", 2, 5)),
    ("hoarfang_wolf", "Hoarfang Wolf", "quad", 1.0, "ice", "blue", "a", "a", "mane", 30, 6, .35, ("freeze", 120, 0), "frost", ("minecraft:bone", 1, 2)),
    ("glacier_brute", "Glacier Brute", "brute", 1.2, "frost", "white", "e", "c", "plates", 120, 12, .18, ("freeze", 200, 0), "frost", ("minecraft:packed_ice", 1, 3)),
    ("snowshroud_wraith", "Snowshroud Wraith", "floater", 1.0, "ice", "cyan", "c", "a", "none", 26, 5, .26, ("slow", 60, 1), "frost", ("minecraft:ice", 1, 3)),
    ("icicle_crawler", "Icicle Crawler", "crawler", 0.9, "frost", "cyan", "d", "e", "none", 20, 4, .33, ("freeze", 100, 0), "frost", ("minecraft:snowball", 1, 4)),
    ("frostbite_serpent", "Frostbite Serpent", "serpent", 1.1, "ice", "blue", "e", "d", "none", 28, 5, .32, ("freeze", 140, 0), "frost", ("minecraft:ice", 1, 2)),
    ("chill_sprite", "Chill Sprite", "blob", 0.7, "frost", "white", "a", "d", "none", 10, 2, .34, ("slow", 50, 0), "frost", ("minecraft:snowball", 1, 3)),
    # ---- bone ----
    ("ossuary_guard", "Ossuary Guard", "biped", 1.1, "bone", "amber", "e", "b", "horns", 42, 7, .27, None, "bone", ("minecraft:bone", 1, 3)),
    ("rib_crawler", "Rib Crawler", "crawler", 1.0, "bone", "gold", "c", "b", "none", 22, 4, .32, None, "bone", ("minecraft:bone", 1, 2)),
    ("marrow_hound", "Marrow Hound", "quad", 1.0, "bone", "red", "b", "e", "mane", 30, 6, .34, ("hunger", 80, 0), "bone", ("minecraft:bone", 1, 3)),
    ("skull_wraith", "Skull Wraith", "floater", 0.9, "bone", "white", "a", "a", "none", 24, 5, .25, ("wither", 40, 0), "bone", ("minecraft:bone_meal", 2, 4)),
    ("grave_brute", "Grave Brute", "brute", 1.1, "bone", "orange", "d", "d", "plates", 100, 11, .19, ("knock", 0, 0), "bone", ("minecraft:bone_block", 1, 2)),
    ("vertebrae_serpent", "Vertebrae Serpent", "serpent", 1.3, "bone", "gold", "b", "e", "none", 34, 6, .31, None, "bone", ("minecraft:bone", 2, 4)),
    ("dust_imp", "Dust Imp", "blob", 0.8, "salt", "amber", "c", "d", "none", 12, 3, .33, ("blind", 40, 0), "bone", ("minecraft:bone_meal", 1, 2)),
    # ---- sunken ----
    ("drowned_stalker", "Drowned Stalker", "biped", 1.0, "tide", "teal", "d", "a", "none", 36, 5, .27, ("slow", 50, 0), "sunken", ("minecraft:kelp", 1, 3)),
    ("brine_crawler", "Brine Crawler", "crawler", 1.0, "tide", "cyan", "c", "b", "none", 22, 4, .31, ("hunger", 80, 0), "sunken", ("minecraft:prismarine_shard", 1, 2)),
    ("tidebound_brute", "Tidebound Brute", "brute", 1.1, "tide", "blue", "b", "e", "plates", 100, 11, .19, ("knock", 0, 0), "sunken", ("minecraft:prismarine_crystals", 1, 2)),
    ("kelp_serpent", "Kelp Serpent", "serpent", 1.2, "tide", "green", "a", "d", "none", 28, 5, .31, ("poison", 60, 0), "sunken", ("minecraft:dried_kelp", 2, 4)),
    ("abyss_eel", "Abyss Eel", "serpent", 0.9, "tide", "teal", "e", "d", "none", 20, 4, .34, ("weak", 50, 0), "sunken", ("minecraft:ink_sac", 1, 2)),
    ("pearl_sprite", "Pearl Sprite", "blob", 0.8, "tide", "white", "c", "e", "none", 12, 3, .32, None, "sunken", ("minecraft:prismarine_shard", 0, 2)),
    # ---- rust ----
    ("scrap_stalker", "Scrap Stalker", "biped", 1.0, "rust", "orange", "e", "a", "none", 38, 6, .28, None, "rust", ("minecraft:iron_nugget", 1, 4)),
    ("gear_crawler", "Gear Crawler", "crawler", 1.0, "iron", "amber", "d", "b", "none", 24, 4, .31, None, "rust", ("minecraft:iron_nugget", 1, 3)),
    ("ironbound_brute", "Ironbound Brute", "brute", 1.2, "iron", "orange", "b", "e", "plates", 125, 13, .18, ("knock", 0, 0), "rust", ("minecraft:iron_ingot", 1, 2)),
    ("rust_hound", "Rust Hound", "quad", 1.0, "rust", "red", "a", "b", "mane", 30, 6, .34, ("weak", 60, 0), "rust", ("minecraft:iron_nugget", 1, 3)),
    ("clockwork_wraith", "Clockwork Wraith", "floater", 1.0, "iron", "gold", "c", "d", "none", 26, 5, .26, None, "rust", ("minecraft:redstone", 1, 3)),
    ("bolt_serpent", "Bolt Serpent", "serpent", 1.1, "iron", "blue", "e", "a", "none", 30, 5, .32, None, "rust", ("minecraft:copper_ingot", 1, 2)),
    ("rivet_imp", "Rivet Imp", "blob", 0.8, "rust", "gold", "c", "e", "none", 12, 3, .33, None, "rust", ("minecraft:iron_nugget", 1, 3)),
    # ---- void ----
    ("voidling", "Voidling", "blob", 0.9, "void", "violet", "a", "a", "none", 16, 4, .30, ("levitate", 40, 0), "void", ("minecraft:ender_pearl", 0, 1)),
    ("null_stalker", "Null Stalker", "biped", 1.2, "void", "magenta", "b", "c", "spikes", 44, 7, .29, ("dark", 100, 0), "void", ("minecraft:ender_pearl", 0, 1)),
    ("riftcrawler", "Riftcrawler", "crawler", 1.1, "void", "violet", "e", "e", "none", 26, 5, .32, ("blind", 60, 0), "void", ("minecraft:ender_pearl", 0, 1)),
    ("eclipse_wraith", "Eclipse Wraith", "floater", 1.1, "void", "white", "c", "b", "none", 30, 6, .26, ("dark", 120, 0), "void", ("minecraft:echo_shard", 0, 1)),
    ("umbral_brute", "Umbral Brute", "brute", 1.2, "obsidian", "violet", "d", "c", "plates", 120, 13, .19, ("knock", 0, 0), "void", ("minecraft:obsidian", 1, 3)),
    ("starless_serpent", "Starless Serpent", "serpent", 1.2, "void", "magenta", "a", "e", "none", 32, 6, .31, ("wither", 40, 0), "void", ("minecraft:amethyst_shard", 1, 2)),
    # ---- coral ----
    ("coralback_beast", "Coralback Beast", "quad", 1.1, "coral", "gold", "b", "d", "mane", 40, 7, .29, None, "coral", ("minecraft:pink_dye", 1, 3)),
    ("polyp_crawler", "Polyp Crawler", "crawler", 1.0, "coral", "cyan", "d", "a", "none", 22, 4, .31, ("poison", 60, 0), "coral", ("minecraft:sea_pickle", 1, 2)),
    ("anemone_lurker", "Anemone Lurker", "blob", 1.1, "coral", "magenta", "a", "e", "none", 18, 3, .27, ("poison", 80, 1), "coral", ("minecraft:pink_dye", 1, 2)),
    ("reefstalker", "Reefstalker", "biped", 1.0, "coral", "teal", "e", "d", "horns", 36, 6, .28, None, "coral", ("minecraft:tube_coral", 0, 1)),
    ("pearlhide_brute", "Pearlhide Brute", "brute", 1.0, "coral", "white", "c", "c", "plates", 95, 10, .19, ("knock", 0, 0), "coral", ("minecraft:prismarine_shard", 1, 3)),
    ("bloomwraith", "Bloomwraith", "floater", 0.9, "coral", "lime", "b", "d", "none", 22, 4, .26, ("weak", 60, 0), "coral", ("minecraft:magenta_dye", 1, 3)),
    # ---- ember ----
    ("magma_hound", "Magma Hound", "quad", 1.0, "ember", "orange", "a", "e", "mane", 32, 6, .35, ("fire", 5, 0), "ember", ("minecraft:magma_cream", 1, 2)),
    ("lavaback_brute", "Lavaback Brute", "brute", 1.2, "blood", "red", "b", "e", "plates", 130, 14, .19, ("fire", 6, 0), "ember", ("minecraft:blaze_powder", 2, 4)),
    ("flare_wraith", "Flare Wraith", "floater", 1.0, "ember", "gold", "c", "a", "none", 26, 5, .27, ("fire", 4, 0), "ember", ("minecraft:blaze_powder", 1, 2)),
    ("scorch_crawler", "Scorch Crawler", "crawler", 1.1, "blood", "orange", "d", "b", "none", 24, 5, .32, ("fire", 3, 0), "ember", ("minecraft:coal", 1, 3)),
    ("cinder_marauder", "Cinder Marauder", "biped", 1.3, "blood", "orange", "e", "d", "horns", 50, 8, .28, ("fire", 5, 0), "ember", ("minecraft:blaze_rod", 0, 1)),
    ("molten_serpent", "Molten Serpent", "serpent", 1.3, "ember", "red", "b", "d", "none", 36, 7, .32, ("fire", 5, 0), "ember", ("minecraft:magma_cream", 1, 3)),
]
