"""Hollowite ore block + ingot sprites. Cells: "#RRGGBB" or None (transparent).
Hand-authored 16x16 matrices: 1px outline, top-left light, 3-tone ramp. Paths are
relative to assets/biomesunseen/textures/ (no extension)."""

SPRITES = {
    "block/hollowite_ore": [
        ["#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47"],
        ["#3B3F47", "#8C919B", "#8C919B", "#8C919B", "#6F747E", "#8C919B", "#8C919B", "#8C919B", "#8C919B", "#6F747E", "#8C919B", "#8C919B", "#8C919B", "#6F747E", "#6F747E", "#3B3F47"],
        ["#3B3F47", "#8C919B", "#6F747E", "#6F747E", "#6F747E", "#0F3E47", "#0F3E47", "#0F3E47", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#575C66", "#575C66", "#3B3F47"],
        ["#3B3F47", "#8C919B", "#6F747E", "#6F747E", "#0F3E47", "#1B6F78", "#2FC4C0", "#1B6F78", "#0F3E47", "#6F747E", "#6F747E", "#6F747E", "#575C66", "#6F747E", "#575C66", "#3B3F47"],
        ["#3B3F47", "#6F747E", "#6F747E", "#6F747E", "#0F3E47", "#2FC4C0", "#A5FFF2", "#2FC4C0", "#1B6F78", "#0F3E47", "#6F747E", "#6F747E", "#6F747E", "#575C66", "#575C66", "#3B3F47"],
        ["#3B3F47", "#6F747E", "#6F747E", "#6F747E", "#0F3E47", "#1B6F78", "#2FC4C0", "#1B6F78", "#0F3E47", "#6F747E", "#6F747E", "#575C66", "#6F747E", "#575C66", "#6F747E", "#3B3F47"],
        ["#3B3F47", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#0F3E47", "#0F3E47", "#0F3E47", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#575C66", "#575C66", "#575C66", "#3B3F47"],
        ["#3B3F47", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#575C66", "#6F747E", "#6F747E", "#575C66", "#575C66", "#3B3F47"],
        ["#3B3F47", "#6F747E", "#0F3E47", "#0F3E47", "#0F3E47", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#575C66", "#575C66", "#575C66", "#3B3F47"],
        ["#3B3F47", "#6F747E", "#0F3E47", "#1B6F78", "#2FC4C0", "#0F3E47", "#6F747E", "#6F747E", "#6F747E", "#0F3E47", "#0F3E47", "#0F3E47", "#6F747E", "#575C66", "#575C66", "#3B3F47"],
        ["#3B3F47", "#6F747E", "#0F3E47", "#2FC4C0", "#A5FFF2", "#0F3E47", "#6F747E", "#6F747E", "#0F3E47", "#1B6F78", "#2FC4C0", "#1B6F78", "#0F3E47", "#575C66", "#575C66", "#3B3F47"],
        ["#3B3F47", "#6F747E", "#0F3E47", "#1B6F78", "#2FC4C0", "#0F3E47", "#6F747E", "#6F747E", "#0F3E47", "#2FC4C0", "#A5FFF2", "#2FC4C0", "#0F3E47", "#575C66", "#575C66", "#3B3F47"],
        ["#3B3F47", "#6F747E", "#6F747E", "#0F3E47", "#0F3E47", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#0F3E47", "#1B6F78", "#2FC4C0", "#1B6F78", "#0F3E47", "#575C66", "#3B3F47"],
        ["#3B3F47", "#575C66", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#0F3E47", "#0F3E47", "#0F3E47", "#6F747E", "#575C66", "#3B3F47"],
        ["#3B3F47", "#575C66", "#575C66", "#6F747E", "#6F747E", "#6F747E", "#575C66", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#6F747E", "#575C66", "#575C66", "#575C66", "#3B3F47"],
        ["#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47", "#3B3F47"],
    ],
    "item/hollowite_ingot": [
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, "#0F3E47", "#0F3E47", "#0F3E47", "#0F3E47", "#0F3E47", "#0F3E47", "#0F3E47", "#0F3E47", None, None],
        [None, None, None, None, None, "#0F3E47", "#E6FFFB", "#8FF5E6", "#8FF5E6", "#8FF5E6", "#8FF5E6", "#8FF5E6", "#2FC4C0", "#0F3E47", None, None],
        [None, None, None, None, "#0F3E47", "#E6FFFB", "#8FF5E6", "#8FF5E6", "#8FF5E6", "#8FF5E6", "#8FF5E6", "#8FF5E6", "#8FF5E6", "#2FC4C0", "#0F3E47", None],
        [None, None, None, "#0F3E47", "#E6FFFB", "#8FF5E6", "#8FF5E6", "#8FF5E6", "#8FF5E6", "#8FF5E6", "#8FF5E6", "#8FF5E6", "#8FF5E6", "#8FF5E6", "#2FC4C0", "#0F3E47"],
        [None, None, None, "#0F3E47", "#8FF5E6", "#8FF5E6", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#1E8A91", "#0F3E47"],
        [None, None, None, "#0F3E47", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#1E8A91", "#0F3E47"],
        [None, None, None, "#0F3E47", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#2FC4C0", "#1E8A91", "#0F3E47"],
        [None, None, None, "#0F3E47", "#1E8A91", "#1E8A91", "#1E8A91", "#1E8A91", "#1E8A91", "#1E8A91", "#1E8A91", "#1E8A91", "#1E8A91", "#1E8A91", "#1E8A91", "#0F3E47"],
        [None, None, None, "#0F3E47", "#0F3E47", "#0F3E47", "#0F3E47", "#0F3E47", "#0F3E47", "#0F3E47", "#0F3E47", "#0F3E47", "#0F3E47", "#0F3E47", "#0F3E47", "#0F3E47"],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    ],
}
