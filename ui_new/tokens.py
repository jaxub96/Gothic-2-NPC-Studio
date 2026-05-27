"""Design tokens — single source of truth for every UI value.

Anything visual (color, font, size, spacing, border thickness) lives here.
The QSS file is a template that references these tokens via $name; theme.py
substitutes them at startup. Widgets that style themselves in Python pull
values straight from the TOKENS / FONTS / SIZES / SPACE / BORDER dicts.

To add a new theme later: create a sibling module (e.g. tokens_modern.py),
expose the same shape, and have theme.apply() pick which to load.
"""

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
COLORS = {
    # neutral walnut ladder (deepest → lightest)
    "ink":          "#0a0604",
    "page_deep":    "#0e0805",
    "page":         "#1a120a",
    "panel":        "#2a1c10",
    "panel_hi":     "#3a2a1a",
    "edge":         "#3a2818",
    "bevel":        "#5e4628",
    "bevel_hi":     "#8a6a3a",

    # text scale
    "muted":        "#6a5638",
    "secondary":    "#8a7350",
    "body":         "#c9b48a",
    "body_hi":      "#fde9b5",

    # primary accent (rust) — used for actions, selection, active tab
    "rust":         "#c44a20",
    "rust_hi":      "#e87648",
    "rust_lo":      "#6e2410",
    "rust_pressed": "#7a3018",

    # secondary accent (gold) — used for section titles, slider handle,
    # numeric readouts, status text
    "gold":         "#d4a528",
    "gold_hi":      "#f3d050",
    "gold_lo":      "#6e4810",

    # destructive (blood) — only on danger buttons
    "blood":        "#8b2520",
    "blood_hi":     "#c44030",
    "blood_lo":     "#4a1410",

    # parchment scroll for code preview
    "parchment":    "#ece0c0",
    "ink_dark":     "#2e1f0e",
}

# ---------------------------------------------------------------------------
# Fonts — three voices, used at multiple sizes for hierarchy
# ---------------------------------------------------------------------------
FONTS = {
    "display": '"Jersey 10", "Iowan Old Style", "Palatino", serif',
    "body":    '"Pixelify Sans", "Iowan Old Style", "Palatino", serif',
    "mono":    '"VT323", "Menlo", "Consolas", monospace',
}

# Font family names as plain strings (for QFont(...) constructor calls).
FONT_FAMILY = {
    "display": "Jersey 10",
    "body":    "Pixelify Sans",
    "mono":    "VT323",
}

# ---------------------------------------------------------------------------
# Type scale (pt) — strict ladder, no off-scale sizes anywhere in the UI
# ---------------------------------------------------------------------------
SIZES = {
    "body":      13,
    "field":     14,
    "label":     13,
    "list_item": 14,
    "checkbox":  13,
    "button":    16,
    "tab":       18,
    "section":   17,
    "menu":      16,
    "menu_item": 13,
    "status":    15,
    "viewport":  16,
    "readout":   18,
    "code":      16,
    "tooltip":   13,
}

# ---------------------------------------------------------------------------
# Spacing scale (px) — multiples of 4
# ---------------------------------------------------------------------------
SPACE = {
    "xxs":  2,
    "xs":   4,
    "sm":   8,
    "md":   12,
    "lg":   16,
    "xl":   24,
    "xxl":  32,
    "huge": 48,
}

# ---------------------------------------------------------------------------
# Borders
# ---------------------------------------------------------------------------
BORDER = {
    "width": 2,
}

# ---------------------------------------------------------------------------
# Window defaults
# ---------------------------------------------------------------------------
WINDOW = {
    "title":   "Gothic II — NPC Studio",
    "size":    (1600, 1000),
    "min":     (1280, 820),
    "org":     "GothicMods",
    "app":     "NPC-Studio-New",
}


def token_map() -> dict[str, str]:
    """Flatten every token into a single namespace for QSS substitution.

    Keys are prefixed by category so they can't collide:
      col_*  colors
      font_* font stacks
      sz_*   point sizes (rendered as integer text)
      sp_*   spacing px (integer text)
      bd_*   border width
    """
    flat: dict[str, str] = {}
    for k, v in COLORS.items():
        flat[f"col_{k}"] = v
    for k, v in FONTS.items():
        flat[f"font_{k}"] = v
    for k, v in SIZES.items():
        flat[f"sz_{k}"] = str(v)
    for k, v in SPACE.items():
        flat[f"sp_{k}"] = str(v)
    for k, v in BORDER.items():
        flat[f"bd_{k}"] = str(v)
    return flat
