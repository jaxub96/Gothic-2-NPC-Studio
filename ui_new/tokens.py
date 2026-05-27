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
# Type scale (px) — pixel-perfect sizes for the bundled bitmap-style fonts.
# Integer px (not pt) so Retina / HiDPI scaling stays on integer multiples and
# the pixel fonts render crisp without subpixel blur.
# ---------------------------------------------------------------------------
SIZES = {
    "body":      20,
    "field":     22,
    "label":     20,
    "list_item": 22,
    "checkbox":  20,
    "button":    24,
    "tab":       28,
    "section":   26,
    "menu":      24,
    "menu_item": 20,
    "status":    22,
    "viewport":  24,
    "readout":   28,
    "code":      24,
    "tooltip":   20,
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
# Chrome — fixed widget geometry (px) that doesn't belong to the spacing scale
# ---------------------------------------------------------------------------
CHROME = {
    "tab_min_width":        128,
    "label_col":            180,
    "scroll_w":              16,
    "scroll_min_thumb":      40,
    "indicator":             22,
    "slider_handle_w":       18,
    "slider_handle_h":       24,
    "slider_handle_overhang": 12,
    "slider_groove_h":        8,
    "readout_w":             88,
    "qty_field_w":           96,
    "tree_indent":           18,
    "arrow_combo_w":          6,
    "arrow_combo_h":          8,
    "arrow_spin_w":           5,
    "arrow_spin_h":           6,
    # letter-spacing tracking
    "track_chrome":           1,   # menu bar, status bar
    "track_emph":             2,   # tabs, section titles, buttons
}

# ---------------------------------------------------------------------------
# Window defaults
# ---------------------------------------------------------------------------
WINDOW = {
    "title":   "Gothic II — NPC Studio",
    "size":    (1760, 1080),
    "min":     (1440, 900),
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
    for k, v in CHROME.items():
        flat[f"ch_{k}"] = str(v)
    return flat
