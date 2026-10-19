"""
pixelart/gear_maps.py -- Hand-authored 16x16 pixel matrices for tools & armour.

Golden Rule #3 is enforced by construction here:

    * 1px 'O' outline contours every silhouette and every internal boundary
      where metal meets haft (that boundary line IS the ambient occlusion).
    * Key light comes from the TOP-LEFT: 'H'/'E' live on the upper-left facet
      of every blade, head and pauldron; 'D'/'S' on the lower-right.
    * Stipple dithering is explicit -- single isolated glyphs placed by hand
      between tone bands so the metal reads as brushed, not flat.
    * No two tool *classes* share a silhouette, and the hero families get
      genuinely different shapes: the Void sword is serrated and asymmetric,
      the Hollow pickaxe is an ancient flared-bowl design with a bone haft,
      the Chronos staff is a floating-ring focus rather than a hafted tool.

Glyph vocabulary (see palettes.GEAR_RAMPS):
    W/w/K  haft light / mid / shadow      H/L/M/D/S/O  head metal ramp
    E      cutting edge specular          G            emissive inlay
    .      transparent
"""

from __future__ import annotations

from typing import Dict, List

# ===========================================================================
#  SWORDS -- five distinct blade silhouettes, one per hero material family.
#  All read bottom-left haft -> top-right tip (Minecraft's held-item angle).
# ===========================================================================

SWORD_MAPS: Dict[str, List[str]] = {
    # Classic straight double-bevel blade. Reference silhouette.
    "straight": [
        "............OO..",
        "...........OHEO.",
        "..........OHLEO.",
        ".........OHLMEO.",
        "........OHLMDEO.",
        ".......OHLMDSEO.",
        "......OHLMDSEO..",
        ".....OHLMDSEO...",
        "....OHLMDSEO....",
        "...OOHLMDSEO....",
        "..OWWOOSSEO.....",
        ".OWwWWOSEO......",
        ".OWwKWOO........",
        "..OWwKO.........",
        "...OKKO.........",
        "....OO..........",
    ],
    # Voidsteel: serrated back edge, split tip, emissive crack down the fuller.
    "jagged_void": [
        "...........O....",
        "..........OHO...",
        ".........OHGO.O.",
        "........OHMGOEO.",
        ".......OHMDGEO..",
        "......OHMDGEO.O.",
        ".....OHMDGEO.OE.",
        "....OHMDGEO.OEO.",
        "...OHMDGEO.OEO..",
        "..OHMDGEO.OEO...",
        ".OOHMDGEOOEO....",
        "OWWOSSSSEOO.....",
        "OWwWWSSSEO......",
        ".OWwKWOOO.......",
        "..OWwKO.........",
        "...OKO..........",
    ],
    # Hollow Deep: ancient leaf-shaped blade, wide belly, corroded pitting.
    "ancient_hollow": [
        "..........OO....",
        ".........OHGO...",
        "........OHLGO...",
        ".......OHLLMGO..",
        "......OHLLLMGO..",
        ".....OHLLMMDGO..",
        ".....OHLLMMDGO..",
        "....OHLLMMDGSO..",
        "....OHLLMMDGSO..",
        "...OHLMMMDSSO...",
        "...OHMMMSSO.....",
        "..OOHMMSSO......",
        ".OWWOSSOO.......",
        ".OWwWWOO........",
        "..OWwKO.........",
        "...OKO..........",
    ],
    # Aetherium: slim estoc, needle tip, winged crossguard.
    "celestial_estoc": [
        ".............O..",
        "............OEO.",
        "...........OHLO.",
        "..........OHLMO.",
        ".........OHLMSO.",
        "........OHLMSO..",
        ".......OHLMSO...",
        "......OHLMSO....",
        ".....OHLMSO.....",
        ".OO.OHLMSO......",
        "OHHOOHLMSO......",
        ".OOOWWSSO.......",
        "....OWwWO.......",
        "....OWwKO.......",
        ".....OKO........",
        ".....OO.........",
    ],
    # Pyroclast: heavy cleaver, thick spine, molten inlay pockets.
    "molten_cleaver": [
        "..........OOOO..",
        ".........OHGHSO.",
        "........OHLGHSO.",
        ".......OHLLGHSO.",
        "......OHLLMGHSO.",
        "......OHLLMGHSO.",
        ".....OHLLMGGHSO.",
        ".....OHLLMGHSO..",
        "....OHLLMGGHSO..",
        "....OHLLMGHSO...",
        "...OOLLMMGHSO...",
        "..OOOOLLSSSO....",
        ".OWWOOOSSO......",
        ".OWwWWOO........",
        "..OWwKO.........",
        "...OKKO.........",
    ],
}

# ===========================================================================
#  PICKAXES -- five distinct head geometries.
# ===========================================================================

PICKAXE_MAPS: Dict[str, List[str]] = {
    # Standard symmetric double point.
    "standard": [
        "...OOOOOOOOOO...",
        "..OHLLLLLLLLDO..",
        ".OHLMMMMMMMMDDO.",
        "OHLMDDDDDDDMDDSO",
        "OHMDD.....SDDSSO",
        ".OO.......OOO...",
        "....OWWO........",
        "....OWwO........",
        "....OWwO........",
        "....OWwO........",
        "....OWwO........",
        "....OWwO........",
        "....OWwO........",
        "....OWwO........",
        "....OWKO........",
        ".....OO.........",
    ],
    # Hollow Deep: ancient flared bowl head, chipped edges, bone haft.
    "ancient_flared": [
        "..OOOOOOOOOOOO..",
        ".OHHLLLLLLLLDDO.",
        "OHLLLLMMMMMMDDDO",
        "OHLLMMGMMMMMDDSO",
        "OHLMGMMMMMMMSSSO",
        "OHLMMMGMMMMMSSSO",
        "OHMMMMMMMMMSSSO.",
        ".OSMMMMMMMSSOO..",
        "..OSSSSSSOO.....",
        "....OBBO........",
        "....OBbO........",
        "....OBbO........",
        "....OBbO........",
        "....OBbO........",
        "....OBKO........",
        ".....OO.........",
    ],
    # Void: single asymmetric hook-pick with a floating shard.
    "void_hook": [
        "..........OO....",
        ".........OHLO...",
        "........OHMLO...",
        ".......OHMMLO...",
        "..OO..OHMMMLO...",
        ".OHLO.OHMMMMSO..",
        ".OHMLOOHMMMMSO..",
        ".OHMMSSSMMMMSO..",
        "..OSSSSSSSSSO...",
        "....OWWO........",
        "....OWwO........",
        "....OWwO........",
        "....OWwO........",
        "....OWwO........",
        "....OWKO........",
        ".....OO.........",
    ],
    # Aetherium: twin swept-back wings, hollow light core.
    "winged": [
        "..O..........O..",
        ".OHO........OHO.",
        ".OHLO......OHLO.",
        "..OHLO....OHLO..",
        "...OHLOOOOHLO...",
        "....OHLLHHLO....",
        ".....OLGGLO.....",
        "......OLOO......",
        "......OWWO......",
        "......OWwO......",
        "......OWwO......",
        "......OWwO......",
        "......OWwO......",
        "......OWwO......",
        "......OWKO......",
        ".......OO.......",
    ],
    # Pyroclast: heavy blocky head with molten vents.
    "molten_block": [
        "..OOOOOOOOOOOO..",
        ".OHHHHGGGGHHDDO.",
        ".OHLLLLLLLLLDDO.",
        "OHLLMMGGGMMMLDDO",
        "OHLMGMMMMMMGMDSO",
        "OHLMGMMMMMMGMDSO",
        "OHLLMMGGGMMMLDSO",
        ".OSLLLLLLLLLDSO.",
        "..OSSSSSSSSSSO..",
        ".....OWWO.......",
        ".....OWwO.......",
        ".....OWwO.......",
        ".....OWwO.......",
        ".....OWwO.......",
        ".....OWKO.......",
        "......OO........",
    ],
}

# ===========================================================================
#  AXES -- four head shapes.
# ===========================================================================

AXE_MAPS: Dict[str, List[str]] = {
    "broad": [
        ".....OOOOOO.....",
        "....OHHHHHLO....",
        "...OHLLLLLLLO...",
        "..OHLLMMMMMLLO..",
        ".OHLLMMMMMMMLLO.",
        ".OHMMMMMMMMMMMEO",
        "OHMMMMMMMMMMMMEO",
        "OHMMMMMMMMMMMMEO",
        ".OHMMMMMMMMMMMEO",
        ".OSSMMMMMMMMLLO.",
        "..OSSSSSSMLLO...",
        "....OOOOWWO.....",
        "........OWwO....",
        "........OWwO....",
        "........OWKO....",
        ".........OO.....",
    ],
    "crescent": [
        "......OOOO......",
        "....OOHHHHOO....",
        "...OHHLLLLHHO...",
        "..OHLLMMMMMLHO..",
        ".OHMMMMMMMMMLHO.",
        ".OHMMMMMMMMMMLEO",
        "OHMMMMMMMMMMMMEO",
        "OHMMMMMMMMMMMMEO",
        ".OHMMMMMMMMMMLEO",
        ".OHMMMMMMMMMLHO.",
        "..OHLLMMMMMLHO..",
        "...OSSSSSSOWWO..",
        "...........OWwO.",
        "...........OWwO.",
        "...........OWKO.",
        "............OO..",
    ],
    "void_cleaver": [
        "...OO...........",
        "..OHHOO.........",
        ".OHLGHHOO.......",
        "OHMGGLLHHOO.....",
        "OHMGGMLLLHHO....",
        "OHMGMLLLLLHHO...",
        ".OHMLLLLLLLHHO..",
        "..OHMLLLLLLLHHO.",
        "...OSMLLLLLLHHO.",
        "....OSSLLLLLHOO.",
        ".....OSSSSSOO...",
        ".......OWWO.....",
        ".......OWwO.....",
        ".......OWwO.....",
        ".......OWKO.....",
        "........OO......",
    ],
    "aether_hatchet": [
        "......OOOO......",
        ".....OHHHLO.....",
        "....OHLLLLO.....",
        "...OHLLMMLO.....",
        "..OHLLMMMLLO....",
        ".OHLLMMMMLLO....",
        ".OHHMMMMMMLEO...",
        ".OHHMMMMMMLEO...",
        ".OHHMMMMMMLEO...",
        "..OHHMMMMLEO....",
        "...OOSSSSOO.....",
        "......OWWO......",
        "......OWwO......",
        "......OWwO......",
        "......OWKO......",
        ".......OO.......",
    ],
}

# ===========================================================================
#  SHOVELS / HOES  (one master silhouette each; per-family palette + pommel
#  overlay provides the material identity)
# ===========================================================================

SHOVEL_MAPS: Dict[str, List[str]] = {
    "master": [
        "......OOOO......",
        ".....OHHHLO.....",
        "....OHLLLLLO....",
        "....OHLMMMLLO...",
        "...OHLMMMMMLLO..",
        "...OHMMMMMMMDO..",
        "...OHMMMMMMMDO..",
        "...OHMMMMMMMDO..",
        "....OHMMMMMDO...",
        "....OSSMMMSO....",
        ".....OSSSSO.....",
        "......OWWO......",
        "......OWwO......",
        "......OWwO......",
        "......OWKO......",
        ".......OO.......",
    ],
}

HOE_MAPS: Dict[str, List[str]] = {
    "master": [
        "...OOOOOOOOOO...",
        "..OHHHHHHHHHLDO.",
        ".OHLLLLLLLLLLDDO",
        ".OHMMMMMMMMMMDDO",
        "..OSSSSSSSSSSSO.",
        ".......OWWO.....",
        ".......OWwO.....",
        ".......OWwO.....",
        ".......OWwO.....",
        ".......OWwO.....",
        ".......OWwO.....",
        ".......OWwO.....",
        ".......OWwO.....",
        ".......OWKO.....",
        ".......OWKO.....",
        "........OO......",
    ],
}

# ===========================================================================
#  STAVES / FOCI  (magic "tools": 5 boss-derived artefact weapons)
# ===========================================================================

STAFF_MAPS: Dict[str, List[str]] = {
    "heart_of_forest_staff": [
        ".......OO.......",
        "......OGGO......",
        ".....OGgCGO.....",
        "....OGgCCCgGO...",
        "....OGgCCCgGO...",
        ".....OGgCGO.....",
        "......OGGO......",
        ".....OOWWOO.....",
        "......OWWO......",
        "......OWwO......",
        ".....OWwWO......",
        "......OWwO......",
        "......OWwO......",
        ".....OWwWO......",
        "......OWKO......",
        ".......OO.......",
    ],
    "void_serpent_fang": [
        "..........OO....",
        ".........OHLO...",
        "........OHCLO...",
        ".......OHCCHO...",
        "......OHCCHSO...",
        ".....OHCCHSO....",
        "....OHCCHSO.....",
        "...OHCCHSO......",
        "..OOHCHSO.......",
        ".OWWOOSSO.......",
        ".OWwWWOO........",
        "..OWwKO.........",
        "...OWwO.........",
        "....OWKO........",
        "....OKO.........",
        ".....O..........",
    ],
    "hollow_tremor_maul": [
        "..OOOOOOOOOOOO..",
        ".OHHHHHHHHHHDDO.",
        "OHLLLLLLLLLLDDDO",
        "OHLLGGGGGGLLDDDO",
        "OHLLGGGGGGLLDDDO",
        "OHLLLLLLLLLLDDDO",
        ".OSSSSSSSSSSDSO.",
        "..OOOOOOOOOOOO..",
        "......OBBO......",
        "......OBbO......",
        "......OBbO......",
        "......OBbO......",
        "......OBbO......",
        "......OBbO......",
        "......OBKO......",
        ".......OO.......",
    ],
    "skyward_sceptre": [
        "..O..........O..",
        ".OEO........OEO.",
        "OHEEO......OHEEO",
        "OHLEEO....OHLEEO",
        ".OHLLEOOOOLLHEO.",
        "..OHLLGGGGLLHO..",
        "...OOGGGGGGOO...",
        "......OGGO......",
        "......OWWO......",
        "......OWwO......",
        ".....OWwWO......",
        "......OWwO......",
        "......OWwO......",
        ".....OWwWO......",
        "......OWKO......",
        ".......OO.......",
    ],
    "unraveling_conduit": [
        "...OO......OO...",
        "..OAAO....OAAO..",
        "..OAEA....AEAO..",
        "...OAAOOOOAAO...",
        "....OAAAAAAO....",
        ".....OAEEAO.....",
        "......OAAO......",
        "......OWWO......",
        ".....OWwWO......",
        "......OWwO......",
        "......OWwO......",
        ".....OWwWO......",
        "......OWwO......",
        "......OWwO......",
        "......OWKO......",
        ".......OO.......",
    ],
}

# ===========================================================================
#  ARMOUR  (item icons; worn layers are separate 64x32 sheets in armor_maps)
#  Each piece carries a 1px outline, top-left key light, AO in the folds and
#  stipple dithering on the large plate areas.
# ===========================================================================

HELMET_MAPS: Dict[str, List[str]] = {
    "closed_helm": [
        ".....OOOOOO.....",
        "....OHHHHHLO....",
        "...OHLLLLLLLO...",
        "..OHLLMMMMMLLO..",
        "..OHMMMMMMMMDO..",
        ".OHMMGGGGMMMDO..",
        ".OHMGGGGGGGMMDO.",
        ".OHMGGGGGGGMDDO.",
        ".OHMMGGGGGMMDDO.",
        ".OSSMMMMMMMMDDO.",
        "..OSSSMMMMSSO...",
        "...OOSSSSSSOO...",
        "......OOOO......",
        "................",
        "................",
        "................",
    ],
    "crowned_helm": [
        "..O..O..O..O....",
        ".OGO.OGO.OGO....",
        ".OGO.OGO.OGO....",
        "..OOOOOOOOO.....",
        "...OHHHHHLO.....",
        "..OHLLLLLLLO....",
        ".OHLLMMMMMLLO...",
        ".OHMMMMMMMMDO...",
        ".OHMMGGGGMMMDO..",
        ".OSSMMMMMMMMSO..",
        "..OSSSSSSSSSO...",
        "...OOOOOOOOO....",
        "................",
        "................",
        "................",
        "................",
    ],
}

CHESTPLATE_MAPS: Dict[str, List[str]] = {
    "plate": [
        ".OOO........OOO.",
        "OHHHOOOOOOOOHHLO",
        "OHHHHHHHHHHHHHLO",
        "OHLLLLLLLLLLLLDO",
        "OHLLMMMMMMMMMDDO",
        ".OHMMMMGMMMMMDDO",
        ".OHMMGGGGGGMMDDO",
        ".OHMMGGGGGGMMDDO",
        ".OHMMGGGGGGMMDDO",
        ".OHMMMMGMMMMMDDO",
        ".OHMMMMMMMMMMDDO",
        ".OSSMMMMMMMMSDDO",
        ".OSSSSMMMMSSSSDO",
        "..OOSSSSSSSSOOO.",
        "....OOOOOOOO....",
        "................",
    ],
}

LEGGINGS_MAPS: Dict[str, List[str]] = {
    "greaves": [
        "..OOOOOOOOOOOO..",
        ".OHHHHHHHHHHDDO.",
        ".OHLLLLLLLLLDDO.",
        ".OHLLMMMMMMMLDO.",
        ".OHMMMMMMMMMMDO.",
        ".OSSMMMMMMMMSDO.",
        "..OOMMMMMMMMOO..",
        "..OMMMMMMMMMMO..",
        "..OMMMMOOOMMMO..",
        "..OMMMMOOOMMMO..",
        "..OMMMMOOOMMMO..",
        "..OMMMMOOOMMMO..",
        "..OSMMMOOOMMSO..",
        "..OSSSOOOOSSSO..",
        "...OOOOOOOOOO...",
        "................",
    ],
}

BOOTS_MAPS: Dict[str, List[str]] = {
    "sabaton": [
        "................",
        "...OOO....OOO...",
        "..OHHHO..OHHHO..",
        "..OHLLHO.OHLLHO.",
        "..OHMMMO.OHMMMO.",
        "..OHMMMO.OHMMMO.",
        "..OSSSO..OSSSO..",
        ".OOMMMMOOOMMMMOO",
        "OHHMMMMOOHMMMMDO",
        "OHLLLLLOOHLLLLDO",
        "OHLLLLLOOHLLLLDO",
        "OMMMMMMMOMMMMMDO",
        "OSSSSSSSOSSSSSDO",
        "OOOOOOOOOOOOOOOO",
        "................",
        "................",
    ],
}

# ===========================================================================
#  BOWS / RANGED
# ===========================================================================

BOW_MAPS: Dict[str, List[str]] = {
    "recurve": [
        ".....OOOO.......",
        "...OOHHHHOO.....",
        "..OHHLLLLHHO....",
        ".OHLLMMMMMLHO...",
        ".OHM......MHO...",
        "OHM........MHO..",
        "OHM.........O...",
        "OHM.............",
        "OHM.............",
        "OHM.........O...",
        "OHM........MHO..",
        ".OHM......MHO...",
        ".OHLLMMMMMLHO...",
        "..OHHLLLLHHO....",
        "...OOHHHHOO.....",
        ".....OOOO.......",
    ],
}

CROSSBOW_MAPS: Dict[str, List[str]] = {
    "repeater": [
        "................",
        "..OO........OO..",
        ".OHHO......OHHO.",
        ".OHMHO....OHMHO.",
        "..OHMHOOOOHMHO..",
        "...OHMMMMMMHO...",
        "....OOOOOOOO....",
        ".......OWWO.....",
        ".......OWwO.....",
        "......OWwWO.....",
        ".......OWwO.....",
        ".......OWwO.....",
        ".......OWKO.....",
        "........OO......",
        "................",
        "................",
    ],
}
