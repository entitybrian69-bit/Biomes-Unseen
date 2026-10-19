"""
pixelart/items_maps.py -- Hand-authored 16x16 pixel matrices for items.

These are the *compositions* every material variant shares. Each composition
carries its own outline, key light (top-left), form shadow, ambient occlusion
and hand-placed stipple. A mineral identity is then expressed by substituting
the curated ramp from palettes.MINERAL_RAMPS -- the artwork itself is never
regenerated, so an ingot still looks like an ingot and a shard still looks
like a shard at any material.

Glyph vocabulary (see palettes.MINERAL_RAMPS):
    C  emissive / specular core      H  highlight
    L  key light                     M  mid body tone
    D  form shadow                   S  ambient occlusion
    O  1px outline                   B  bone / organic light
    b  bone / organic shadow         A  secondary accent
    .  transparent
"""

from __future__ import annotations

from typing import Dict, List

# ---------------------------------------------------------------------------
#  REFINED METALS
# ---------------------------------------------------------------------------

INGOT_MAPS: Dict[str, List[str]] = {
    # Classic trapezoid ingot, bevelled top face catching the key light.
    "standard": [
        "................",
        "................",
        "....OOOOOOOO....",
        "...OHHHHHHHLO...",
        "..OHLLLLLLLLLO..",
        ".OHLLLLLLLLLLLO.",
        ".OHMMMMMMMMMMDO.",
        ".OHMMMMMMMMMMDO.",
        ".OMMMMMMMMMMDDO.",
        ".OMMMMMMMMMMDDO.",
        ".OSSSSSSSSSSDSO.",
        "..OOOOOOOOOOO...",
        "................",
        "................",
        "................",
        "................",
    ],
    # Stamped bar with a maker's mark -- used for the "refined" tier.
    "stamped": [
        "................",
        "...OOOOOOOOOO...",
        "..OHHHHHHHHHLO..",
        ".OHLLLLLLLLLLLO.",
        ".OHLLLOOOOLLLLO.",
        ".OHLMOSSSOMMLLO.",
        ".OHLMOSCSOMMLLO.",
        ".OHLMOSCSOMMLLO.",
        ".OHLMOSSSOMMLLO.",
        ".OHLLLOOOOLLLDO.",
        ".OMMMMMMMMMMMDO.",
        ".OSSSSSSSSSSDSO.",
        "..OOOOOOOOOOOO..",
        "................",
        "................",
        "................",
    ],
}

NUGGET_MAPS: Dict[str, List[str]] = {
    "standard": [
        "................",
        "................",
        "................",
        "................",
        "......OOOO......",
        ".....OHHHLO.....",
        "....OHLLLLO.....",
        "....OHMLLMLLO...",
        ".....OMMMMDO....",
        ".....OSSSSO.....",
        "......OOOO......",
        "................",
        "................",
        "................",
        "................",
        "................",
    ],
}

PLATE_MAPS: Dict[str, List[str]] = {
    "sheet": [
        "................",
        "..OOOOOOOOOOOO..",
        ".OHHHHHHHHHHHLO.",
        ".OHLLLLLLLLLLLO.",
        ".OHMMMMMMMMMMDO.",
        ".OHMMMMMMMMMMDO.",
        ".OMMMMMMMMMMMDO.",
        ".OMMMMMMMMMMMDO.",
        ".OMMMMMMMMMMMDO.",
        ".OSSSSSSSSSSSSO.",
        "..OOOOOOOOOOOO..",
        "................",
        "................",
        "................",
        "................",
        "................",
    ],
}

ROD_MAPS: Dict[str, List[str]] = {
    "staff_rod": [
        "................",
        "..........OOO...",
        ".........OHHO...",
        ".........OHLO...",
        "..........OLMO..",
        ".........OHHO...",
        ".........OHLO...",
        "..........OLMO..",
        ".........OHHO...",
        ".........OHLO...",
        "..........OLMO..",
        ".........OHHO...",
        ".........OHSO...",
        "..........OSO...",
        "...........O....",
        "................",
    ],
}

# ---------------------------------------------------------------------------
#  CRYSTALS / GEMS / SHARDS
# ---------------------------------------------------------------------------

GEM_MAPS: Dict[str, List[str]] = {
    # Brilliant cut: table facet top-left, pavilion converging bottom-right.
    "brilliant": [
        "................",
        "......OOOO......",
        ".....OHHHHO.....",
        "....OHLLLLHO....",
        "...OHLLLLLLHO...",
        "..OHLLCCCCLLHO..",
        ".OHLLCCCCCCCLHO.",
        ".OHLCCCCCCCCCLHO",
        "..OHMCCCCCCCMHO.",
        "...OMMCCCCMMO...",
        "....OMMMMMMO....",
        ".....OSSSSO.....",
        "......OOOO......",
        "................",
        "................",
        "................",
    ],
    # Raw crystal shard: asymmetric, splintered, emissive core.
    "shard": [
        "...........O....",
        "..........OHO...",
        "..OHHHHHO.......",
        "........OHLLMO..",
        ".......OHLLCMO..",
        "......OHLLCCMO..",
        ".....OHLLCCCMO..",
        "....OHLLCCCCMO..",
        "...OHLLCCCCMDO..",
        "..OHLLCCCCMMDO..",
        ".OHLLCCCCMMMDO..",
        ".OMMCCCCMMMMDO..",
        ".OSSSMMMMSDDSO..",
        "..OOOOOOOOOOO...",
        "................",
        "................",
    ],
    # Hexagonal prism cluster.
    "prism": [
        "................",
        "...OOO.....OOO..",
        "..OHHHO...OHHLO.",
        "..OHLHO...OHLLO.",
        "..OHCMO...OHLCMO",
        "..OHCCMO.OHCCCMO",
        "..OHCCMO.OHCCCMO",
        "..OHCCMOOOHCCCMO",
        "..OHCCMOOOHCCCMO",
        "..OMCCMMMMMCCCMO",
        "..OMMMMMMMMMCMMO",
        "..OSSSSSSSSSSSSO",
        "...OOOOOOOOOOOO.",
        "................",
        "................",
        "................",
    ],
}

DUST_MAPS: Dict[str, List[str]] = {
    "pile": [
        "................",
        "................",
        "................",
        "......O..O......",
        ".....OMOOMO.....",
        "....OMMHMMMO....",
        "..O.OMHHHHMMO.O.",
        ".OMOOMHHHHHMMOO.",
        ".OMMHHHHHHHHMMO.",
        "OMMHHHHHHHHHHMMO",
        "OMMMHHHHHHHHMMMO",
        "OSSSMMMMMMMMSSSO",
        ".OOOOOOOOOOOOOO.",
        "................",
        "................",
        "................",
    ],
}

ESSENCE_MAPS: Dict[str, List[str]] = {
    # Floating mote of energy: emissive core, glow falloff, orbiting sparks.
    "mote": [
        "................",
        "......O....O....",
        ".....OgO..OgO...",
        "......O....O....",
        "...O............",
        "..OgO...gggg....",
        "...O..ggHHHHgg..",
        ".....gHHLLLLHHg.",
        "....gHLLCCCCLLHg",
        "....gHLLCCCCLLHg",
        ".....gHHLLLLHHg.",
        "...O..ggHHHHgg..",
        "..OgO...gggg....",
        "...O............",
        "......O....O....",
        ".....OgO..OgO...",
    ],

}

CORE_MAPS: Dict[str, List[str]] = {
    # Boss soul-core: a caged sphere of energy.
    "soul_core": [
        "................",
        ".....OOOOOO.....",
        "...OOSSSSSSOO...",
        "..OSSSSSSSSSSO..",
        ".OSSSggggggSSSO.",
        ".OSSgCCCCCCgSSO.",
        "OSggCCCCCCCCggSO",
        "OSgCCCCCCCCCCgSO",
        "OSgCCCCCCCCCCgSO",
        "OSggCCCCCCCCggSO",
        ".OSSgCCCCCCgSSO.",
        ".OSSSggggggSSSO.",
        "..OSSSSSSSSSSO..",
        "...OOSSSSSSOO...",
        ".....OOOOOO.....",
        "................",
    ],
}

PEARL_MAPS: Dict[str, List[str]] = {
    "sphere": [
        "................",
        "................",
        ".....OOOOOO.....",
        "....OHHHHHHO....",
        "...OHLLLLLLHO...",
        "..OHLLCCCCLLHO..",
        "..OHLLCCCCLLHO..",
        ".OHLLCCCCCCCLHO.",
        ".OHMCCCCCCCCMDO.",
        ".OHMCCCCCCCCMDO.",
        "..OMMCCCCCCMMDO.",
        "..OSSMMMMMMSSDO.",
        "...OSSSSSSSSO...",
        ".....OOOOOO.....",
        "................",
        "................",
    ],
}

# ---------------------------------------------------------------------------
#  ORGANIC DROPS
# ---------------------------------------------------------------------------

ORGANIC_ITEM_MAPS: Dict[str, List[str]] = {
    "fang": [
        "................",
        "..........OO....",
        ".........OHHO...",
        "........OHHBO...",
        ".......OHHBBO...",
        ".......OHBBbO...",
        "......OHBBbbO...",
        "......OBBBbbO...",
        ".....OBBBbbO....",
        ".....OBBbbbO....",
        "....OBBBbbO.....",
        "....OBbbbbbO....",
        "...ObbbbbbO.....",
        "...ObbbbbO......",
        "....OOOOO.......",
        "................",
    ],
    "claw": [
        "................",
        ".......OOO......",
        "......OBBBO.....",
        "......OBBBBO....",
        ".....OBBBbbO....",
        ".....OBBBbbO....",
        "....OBBBbbO.....",
        "....OBBBbbO.....",
        "...OBBBbbO......",
        "...OBBBbbO......",
        "..OBBBbbO.......",
        "..OBbbbO........",
        ".ObbbbO.........",
        ".ObbbO..........",
        "..OOO...........",
        "................",
    ],
    "scale": [
        "................",
        "......OOOO......",
        ".....OHHHHO.....",
        "....OHLLLLHO....",
        "...OHLLLLLLHO...",
        "..OHLLMMMMMLHO..",
        "..OHMLMMMMMMLHO.",
        ".OHMLMMMMMMMMLHO",
        ".OHMLMMMMMMMMLHO",
        ".OHMLMMMMMMMMDHO",
        "..OMMMMMMMMMMDO.",
        "..OSSSMMMMMSSDO.",
        "...OSSSSSSSSSO..",
        "....OOOOOOOOO...",
        "................",
        "................",
    ],
    "feather": [
        "..............O.",
        ".............OBO",
        "............OBBO",
        "...........OBBBO",
        "..........OBBBbO",
        ".........OBBBbbO",
        "........OBBBbbO.",
        ".......OBBBbbO..",
        "......OBBBbbO...",
        ".....OBBBbbO....",
        "....OBBBbbO.....",
        "...OBBBbbO......",
        "..OBBBbbO.......",
        ".OBbbbbbO.......",
        ".ObbbbbbO.......",
        "..OOOOOO........",
    ],
    "spore_pod_item": [
        "................",
        "......OOOO......",
        ".....OAggAO.....",
        "....OAgAAgAO....",
        "....OAgAAAAO....",
        "...OAgAAAAAAO...",
        "...OAAAAAAAAO...",
        "..OAAASSSSAAAO..",
        "..OAASSSSSSAAO..",
        "..OASSSSSSSSAO..",
        "...OSSSSSSSSO...",
        "....OSSSSSSO....",
        ".....OOSSOO.....",
        ".......OO.......",
        "................",
        "................",
    ],
    "mushroom_cap": [
        "................",
        "......OOOO......",
        "....OOHHHHOO....",
        "...OHHLLLLHHO...",
        "..OHLLMMMMMLHO..",
        ".OHLLMMMMMMMMDO.",
        ".OHMMMMMMMMMMDDO",
        "OHMMMMMMMMMMMMDO",
        "OSSSSSSSSSSSSSSO",
        ".OOOOOOOOOOOOOO.",
        ".....OBBBBO.....",
        ".....OBBBBO.....",
        ".....OBBBBO.....",
        ".....OSSSSO.....",
        "......OOOO......",
        "................",
    ],
    "heart_fruit": [
        "................",
        ".......OO.......",
        "......OOGO......",
        ".....OO.OO......",
        "....OHHOHHO.....",
        "...OHLLHLLHO....",
        "..OHLLLLLLLHO...",
        "..OHLLLLLLLHO...",
        "..OHLLLLLLLHDO..",
        "...OHLLLLLHDDO..",
        "....OHLLLHDDO...",
        ".....OHLLHDO....",
        "......OHHDO.....",
        ".......ODO......",
        "........O.......",
        "................",
    ],
}

# ---------------------------------------------------------------------------
#  LORE / UTILITY ITEMS
# ---------------------------------------------------------------------------

UTILITY_ITEM_MAPS: Dict[str, List[str]] = {
    "lore_book": [
        "................",
        ".OOOOOOOOOOOOO..",
        ".OBBBBBBBBBBBBO.",
        ".OBAAAAAAAAAAAO.",
        ".OBAAAAAAAAAAAO.",
        ".OBAOOOOOOOOAAO.",
        ".OBAAAAAAAAAAAO.",
        ".OBAAGGGGGGAAAO.",
        ".OBAAAAAAAAAAAO.",
        ".OBAOOOOOOOOAAO.",
        ".OBAAAAAAAAAAAO.",
        ".OBAAGGGGGGAAAO.",
        ".OBAAAAAAAAAAAO.",
        ".OBBBBBBBBBBBBO.",
        ".OOOOOOOOOOOOO..",
        "................",
    ],
    "portal_igniter": [
        "................",
        "...........OO...",
        "..........OGGO..",
        ".........OGCGO..",
        "..........OGGO..",
        "...........OO...",
        "..........OWWO..",
        ".........OWWwO..",
        ".........OWwO...",
        "........OWwO....",
        "........OWwO....",
        ".......OWwO.....",
        ".......OWwO.....",
        "......OWwO......",
        "......OWKO......",
        ".......OO.......",
    ],
    "compass_reality": [
        "................",
        ".....OOOOOO.....",
        "...OOHHHHHHOO...",
        "..OHLLLLLLLLO...",
        ".OHLLLOOOOLLLHO.",
        ".OOLOOEEEOOLLOO.",
        "OHLOOEEEEEOOLOO.",
        "OHLOEEEGEEEEOLOO",
        "OHLOOEEEEEOOLOOO",
        ".OHLOOEEEOOLLOO.",
        ".OHLLLOOOOLLLHO.",
        "..OHLLLLLLLLO...",
        "...OSSSSSSSSO...",
        ".....OOOOOO.....",
        "................",
        "................",
    ],
    "music_disc_unseen": [
        "................",
        "....OOOOOOOO....",
        "..OOSSSSSSSSOO..",
        ".OSSMMMMMMMMSSO.",
        "OSMMSSSSSSSSMMSO",
        "OSMSMMMMMMMMSMSO",
        "OSMSMMOOOOMMSMSO",
        "OSMSMOHHHHOMSMSO",
        "OSMSMOHHHHOMSMSO",
        "OSMSMMOOOOMMSMSO",
        "OSMSMMMMMMMMSMSO",
        "OSMMSSSSSSSSMMSO",
        ".OSSMMMMMMMMSSO.",
        "..OOSSSSSSSSOO..",
        "....OOOOOOOO....",
        "................",
    ],
}
