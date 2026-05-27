from pathlib import Path

from PySide6.QtGui import QColor, QFont, QFontDatabase, QPalette
from PySide6.QtWidgets import QApplication

ASSETS = Path(__file__).parent / "assets"
QSS_PATH = Path(__file__).parent / "theme.qss"
FONT_DIR = ASSETS / "fonts"

# ---------------------------------------------------------------------------
# Palette — pixel-RPG walnut + rust + gold. Few shades, each used >=2 places.
# ---------------------------------------------------------------------------
COLORS = {
    "ink":           "#0a0604",  # bevel shadow, deepest
    "page_deep":     "#0e0805",  # input/list background
    "page":          "#1a120a",  # window
    "panel":         "#2a1c10",  # raised panel
    "panel_hi":      "#3a2a1a",  # hover row
    "edge":          "#3a2818",  # subtle edge / focus rule
    "bevel":         "#5e4628",  # bevel highlight
    "bevel_hi":      "#8a6a3a",  # bright bevel highlight
    "muted":         "#6a5638",
    "secondary":     "#8a7350",
    "body":          "#c9b48a",
    "body_hi":       "#fde9b5",  # parchment cream — text on rust
    "rust":          "#c44a20",  # primary accent
    "rust_hi":       "#e87648",  # rust top-bevel
    "rust_lo":       "#6e2410",  # rust bottom-bevel
    "rust_pressed":  "#7a3018",
    "gold":          "#d4a528",  # secondary accent
    "gold_hi":       "#f3d050",  # gold top-bevel
    "gold_lo":       "#6e4810",  # gold bottom-bevel
    "blood":         "#8b2520",
    "blood_hi":      "#c44030",
    "parchment":     "#ece0c0",
    "ink_dark":      "#2e1f0e",
}


def _load_bundled_fonts() -> None:
    """Register the bundled pixel TTFs so QSS can address them by family name."""
    if not FONT_DIR.exists():
        return
    for ttf in sorted(FONT_DIR.glob("*.ttf")):
        QFontDatabase.addApplicationFont(str(ttf))


def apply(app: QApplication) -> None:
    _load_bundled_fonts()

    base = QFont("Pixelify Sans", 13)
    base.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    app.setFont(base)

    p = QPalette()
    p.setColor(QPalette.ColorRole.Window,          QColor(COLORS["page"]))
    p.setColor(QPalette.ColorRole.WindowText,      QColor(COLORS["body"]))
    p.setColor(QPalette.ColorRole.Base,            QColor(COLORS["page_deep"]))
    p.setColor(QPalette.ColorRole.AlternateBase,   QColor(COLORS["panel"]))
    p.setColor(QPalette.ColorRole.Text,            QColor(COLORS["body"]))
    p.setColor(QPalette.ColorRole.PlaceholderText, QColor(COLORS["muted"]))
    p.setColor(QPalette.ColorRole.Button,          QColor(COLORS["panel"]))
    p.setColor(QPalette.ColorRole.ButtonText,      QColor(COLORS["body"]))
    p.setColor(QPalette.ColorRole.Highlight,       QColor(COLORS["rust"]))
    p.setColor(QPalette.ColorRole.HighlightedText, QColor(COLORS["body_hi"]))
    p.setColor(QPalette.ColorRole.ToolTipBase,     QColor(COLORS["panel"]))
    p.setColor(QPalette.ColorRole.ToolTipText,     QColor(COLORS["body_hi"]))
    p.setColor(QPalette.ColorRole.Link,            QColor(COLORS["gold"]))
    app.setPalette(p)
    app.setStyleSheet(QSS_PATH.read_text(encoding="utf-8"))
