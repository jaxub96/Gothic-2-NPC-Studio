
# ══════════════════════════════════════════════════════════════════════════════
#  THEME  —  change everything visual here, nowhere else
# ══════════════════════════════════════════════════════════════════════════════

THEME = {
    # ── Colors ────────────────────────────────────────────────────────────────
    # Backgrounds (light → dark)
    "bg_main":          "#f5edd6",   # window / editor background
    "bg_panel":         "#ede0c0",   # sidebar, group boxes
    "bg_bar":           "#e0ceaa",   # top bar, item hover
    "bg_border":        "#c9b68a",   # borders, separators, scrollbar handle
    "bg_input":         "#d8ccb8",   # text field / spinbox background
    "bg_input_border":  "#c8bca0",   # text field border
    "bg_code":          "#faf4e4",   # code preview background
    "bg_choice":        "#eee8d0",   # choice row background
    "bg_choice_input":  "#f0ead8",   # choice label input

    # Text
    "text_primary":     "#2e1f0e",   # main body text
    "text_secondary":   "#5a3e28",   # labels, secondary
    "text_muted":       "#9a7d5a",   # placeholders, inactive

    # Accents
    "accent_primary":   "#8b3a1a",   # rust red  — active, selected, export btn
    "accent_hover":     "#c05a30",   # lighter rust for hover
    "accent_secondary": "#4a5e35",   # moss green — choices, log
    "accent_gold":      "#a07820",   # gold       — group box titles

    # Syntax highlighting (code preview only)
    "syn_keyword":      "#7a2010",   # instance / func / void …
    "syn_type":         "#5a3e80",   # C_INFO / TRUE / LOG_* …
    "syn_function":     "#1a5a30",   # AI_Output / B_GiveXP …
    "syn_string":       "#7a5010",   # "quoted strings"
    "syn_comment":      "#9a8060",   # // comments
    "syn_number":       "#1a407a",   # numeric literals

    # ── Typography ────────────────────────────────────────────────────────────
    "font_ui":          "Georgia, serif",          # all UI chrome
    "font_code":        "Cascadia Code, Consolas, monospace",  # code preview
    "font_size_ui":     "12px",
    "font_size_small":  "11px",
    "font_size_tiny":   "9px",
    "font_size_title":  "16px",
    "font_size_placeholder": "17px",
    "font_size_code":   10,          # pt, used for QFont object

    # ── Geometry ──────────────────────────────────────────────────────────────
    "radius_sm":        "3px",
    "radius_md":        "4px",
    "radius_lg":        "6px",
    "border_width":     "1px",
    "topbar_height":    56,
    "sidebar_width":    204,
    "splitter_sizes":   [204, 530, 480],
    "window_size":      (1280, 840),

    # ── Spacing ───────────────────────────────────────────────────────────────
    "label_col_width":  "44px",      # left-column label width in editor rows
}

# ── Derived stylesheet fragments (built once from THEME, used everywhere) ─────
# These are the only place that translates THEME values into Qt stylesheet text.

def _ss_field():
    t = THEME
    return (
        f"QLineEdit {{ background:{t['bg_input']}; color:{t['text_primary']}; "
        f"  border:{t['border_width']} solid {t['bg_input_border']}; "
        f"  border-radius:{t['radius_sm']}; padding:4px 8px; "
        f"  selection-background-color:{t['accent_hover']}; "
        f"  font-family:{t['font_ui']}; }}"
        f"QLineEdit:focus {{ border:{t['border_width']} solid {t['accent_primary']}; }}"
        f"QLineEdit::placeholder {{ color:{t['text_muted']}; }}"
    )

def _ss_spin():
    t = THEME
    return (
        f"QSpinBox {{ background:{t['bg_input']}; color:{t['text_primary']}; "
        f"  border:{t['border_width']} solid {t['bg_input_border']}; "
        f"  border-radius:{t['radius_sm']}; padding:2px 4px; }}"
        f"QSpinBox:focus {{ border:{t['border_width']} solid {t['accent_primary']}; }}"
    )

def _ss_combo():
    t = THEME
    return (
        f"QComboBox {{ background:{t['bg_input']}; color:{t['text_primary']}; "
        f"  border:{t['border_width']} solid {t['bg_input_border']}; "
        f"  border-radius:{t['radius_sm']}; padding:2px 6px; }}"
        f"QComboBox::drop-down {{ border:none; }}"
        f"QComboBox QAbstractItemView {{ background:{t['bg_panel']}; color:{t['text_primary']}; "
        f"  selection-background-color:{t['accent_primary']}; "
        f"  selection-color:{t['bg_main']}; }}"
    )

def _ss_check():
    t = THEME
    return (
        f"QCheckBox {{ color:{t['text_secondary']}; spacing:6px; }}"
        f"QCheckBox::indicator {{ width:13px; height:13px; "
        f"  border:{t['border_width']} solid {t['bg_border']}; "
        f"  border-radius:2px; background:{t['bg_input']}; }}"
        f"QCheckBox::indicator:checked {{ background:{t['accent_primary']}; "
        f"  border-color:{t['accent_primary']}; }}"
    )

def _ss_group(title_color=None):
    t = THEME
    c = title_color or t["accent_gold"]
    return (
        f"QGroupBox {{ color:{c}; font-weight:700; font-size:{t['font_size_small']}; "
        f"  letter-spacing:0.5px; border:{t['border_width']} solid {t['bg_border']}; "
        f"  border-radius:{t['radius_lg']}; margin-top:10px; padding-top:6px; "
        f"  background:{t['bg_panel']}; font-family:{t['font_ui']}; }}"
        f"QGroupBox::title {{ subcontrol-origin:margin; left:10px; "
        f"  background:{t['bg_panel']}; padding:0 4px; }}"
    )

def _ss_add_btn(color=None):
    t = THEME
    c = color or t["accent_primary"]
    return (
        f"QPushButton {{ background:{t['bg_bar']}; color:{c}; "
        f"  border:{t['border_width']} solid {t['bg_border']}; "
        f"  border-radius:{t['radius_sm']}; padding:4px 12px; "
        f"  font-size:{t['font_size_small']}; font-weight:600; }}"
        f"QPushButton:hover {{ background:{t['bg_input_border']}; color:{t['text_primary']}; }}"
    )

def _ss_rm_btn():
    t = THEME
    return (
        f"QPushButton {{ background:transparent; color:{t['text_muted']}; border:none; }}"
        f"QPushButton:hover {{ color:{t['accent_primary']}; }}"
    )

def _ss_global():
    t = THEME
    return f"""
        QMainWindow, QWidget {{
            background: {t['bg_main']};
            color: {t['text_primary']};
            font-family: {t['font_ui']};
            font-size: {t['font_size_ui']};
        }}
        QLabel {{ color: {t['text_secondary']}; }}
        QScrollBar:vertical {{
            background: {t['bg_panel']}; width: 8px; border-radius: 4px;
        }}
        QScrollBar::handle:vertical {{
            background: {t['bg_border']}; border-radius: 4px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        QSplitter::handle {{ background: {t['bg_border']}; }}
        QTabWidget::pane {{
            border: {t['border_width']} solid {t['bg_border']};
            background: {t['bg_main']};
            border-radius: {t['radius_md']};
        }}
        QTabBar::tab {{
            background: {t['bg_bar']};
            color: {t['text_secondary']};
            padding: 6px 16px;
            border-top-left-radius: {t['radius_md']};
            border-top-right-radius: {t['radius_md']};
            border: {t['border_width']} solid {t['bg_border']};
            margin-right: 2px;
            font-family: {t['font_ui']};
        }}
        QTabBar::tab:selected {{
            background: {t['bg_main']};
            color: {t['accent_primary']};
            font-weight: 700;
            border-bottom: 2px solid {t['accent_primary']};
        }}
        QMessageBox {{ background: {t['bg_main']}; }}
    """

# Build all sheets once at import time
SS = {
    "field":    _ss_field(),
    "spin":     _ss_spin(),
    "combo":    _ss_combo(),
    "check":    _ss_check(),
    "group":    _ss_group(),
    "group_rust": _ss_group(THEME["accent_primary"]),
    "group_moss": _ss_group(THEME["accent_secondary"]),
    "group_mid":  _ss_group(THEME["text_secondary"]),
    "add_btn":    _ss_add_btn(),
    "add_btn_rust": _ss_add_btn(THEME["accent_primary"]),
    "add_btn_moss": _ss_add_btn(THEME["accent_secondary"]),
    "rm_btn":   _ss_rm_btn(),
    "global":   _ss_global(),
}

# ══════════════════════════════════════════════════════════════════════════════
#  END OF THEME
# ══════════════════════════════════════════════════════════════════════════════
# ---------------------------------------------------------------------------
# Gothic theme compatibility aliases
# Maps old project color names to  THEME values
# ---------------------------------------------------------------------------

from constants.colors import THEME

# Backgrounds
BG_DARK   = THEME["bg_main"]
BG_MEDIUM = THEME["bg_panel"]
BG_LIGHT  = THEME["bg_input"]

# Accents
ACCENT_PRIMARY   = THEME["accent_primary"]
ACCENT_SECONDARY = THEME["accent_secondary"]

# Text
TEXT_PRIMARY   = THEME["text_primary"]
TEXT_SECONDARY = THEME["text_secondary"]
TEXT_DARK      = THEME["text_muted"]

# Fonts
FONT_PRIMARY = (
    THEME["font_ui"].split(",")[0].strip(),
    THEME["font_size_code"],
)

# Optional compatibility aliases for extra usage across project
WARNING_COLOR = THEME["accent_gold"]
SUCCESS_COLOR = THEME["accent_secondary"]

# Optional common borders / surfaces
BORDER_COLOR = THEME["bg_border"]
INPUT_BORDER = THEME["bg_input_border"]

# Optional code/editor colors
CODE_BG = THEME["bg_code"]

# Optional hover accents
ACCENT_HOVER = THEME["accent_hover"]