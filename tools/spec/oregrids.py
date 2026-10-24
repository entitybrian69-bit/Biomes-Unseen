"""16x16 char grids for generated ore blocks (3 vein layouts) and ore item sprites (6 styles).

Block chars: O/h/m/d = host stone ramp; k/x/c/l = ore ramp (outline, dark, mid, light).
Item chars: '.' transparent; O outline; w highlight; l/c/d light/mid/dark.
"""

BLOCKS = {
    "A": ["OOOOOOOOOOOOOOOO", "OhhhmhhhhmhhhmmO", "OhmmmkkkmmmmmddO", "OhmmkxcxkmmmdmdO",
          "OmmmkclcxkmmmddO", "OmmmkxcxkmmdmdmO", "OmmmmkkkmmmmdddO", "OmmmmmmmmmdmmddO",
          "OmkkkmmmmmmmdddO", "OmkxckmmmkkkmddO", "OmkclkmmkxcxkddO", "OmkxckmmkclckddO",
          "OmmkkmmmmkxcxkdO", "OdmmmmmmmmkkkmdO", "OddmmmdmmmmmdddO", "OOOOOOOOOOOOOOOO"],
    "B": ["OOOOOOOOOOOOOOOO", "OhhhmhhhhmhhhmmO", "OhmkcmmmmmmmmddO", "OmmxlkmmmmkclmdO",
          "OmmmkkmmmmxlkmdO", "OmmmmmmmmmmkkmdO", "OhmmmmkcmmmmmmdO", "OmmmmxlkmmmmddmO",
          "OmmmmmkkmmkcmmdO", "OmkcmmmmmmxlkmdO", "OmxlkmmmmmmkkmdO", "OmmkkmmkcmmmmmdO",
          "OdmmmmmxlkmmmmdO", "OddmmmdmmkkmmddO", "OddmmmdmmmmmdddO", "OOOOOOOOOOOOOOOO"],
    "C": ["OOOOOOOOOOOOOOOO", "OhhhmhhhhmhhhmmO", "OhmmmmmkkmmmmddO", "OhmmmmkxckmmmmdO",
          "OmmmmkxclckmmmdO", "OmmmmkcllxkmmddO", "OmmmmmkxcxkmmdmO", "OhmmmmmkcxkmmddO",
          "OmmmmmkxclkmmdmO", "OmmmmkxcclkmmddO", "OmmmmkclxkmmmdmO", "OmmmmmkxkmmmddmO",
          "OdmmmmmkkmmmdmdO", "OdmmmmmmmmmdmddO", "OddmmmdmmmmmdddO", "OOOOOOOOOOOOOOOO"],
}

ITEMS = {
    "ingot": ["................", "................", "................", "................",
              "......OOOOOOOO..", ".....OwlllllcO..", "....OwlllllllcO.", "...OwlllllllllcO",
              "...OllcccccccddO"[:16], "...OccccccccccdO", "...OccccccccccdO", "...OdddddddddddO",
              "...OOOOOOOOOOOOO", "................", "................", "................"],
    "gem": ["................", "................", "................", ".....OOOOOO.....",
            "....OwllllcO....", "...OwllccccdO...", "..OwlccccccddO..", ".OOOOOOOOOOOOOO.",
            ".OlllcccccddddO.", "..OlllccccddO...", "...OllcccddO....", "....OlccdO......",
            ".....OcdO.......", "......OO........", "................", "................"],
    "shard": ["................", "..........OO....", ".........OwlO...", "........OwllcO..",
              ".......OwllcdO..", "......OwllcddO..", ".....OwllcddO...", "....OwllcddO....",
              "...OllcddO......", "..OllcddO.......", ".OlcddO.........", ".OcdOO..........",
              "..OO............", "................", "................", "................"],
    "crystal": ["................", "......OOOO......", ".....OwllcO.....", ".....OwlccdO....",
                ".....OwlccdO....", ".....OwlccdO....", ".....OllccdO....", ".....OllccddO...",
                "....OllcccddO...", "....OllcccddO...", "...OllcccddddO..", "...OOOOOOOOOOO..",
                "................", "................", "................", "................"],
    "nugget": ["................", "................", "................", "................",
               "................", "................", "....OOOO........", "...OwllcO.......",
               "..OwllccdO..OO..", "..OllccdddO.OcO.", "...OddddO..OOO..", "....OOOO........",
               "................", "................", "................", "................"],
    "orb": ["................", "................", ".....OOOOOO.....", "...OOwlllllcOO..",
            "..OwllllllcccO..", "..OwlllllcccddO.", "..OllllcccccddO.", "..OlllcccccdddO.",
            "..OllccccddddO..", "..OlcccdddddO...", "...OccddddddO...", "....OOddddOO....",
            "......OOOO......", "................", "................", "................"],
}

for _k, _g in list(BLOCKS.items()) + list(ITEMS.items()):
    assert len(_g) == 16 and all(len(r) == 16 for r in _g), (_k, [len(r) for r in _g])
