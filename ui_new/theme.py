import sys
from pathlib import Path
from string import Template

from PySide6.QtGui import QColor, QFont, QFontDatabase, QPalette
from PySide6.QtWidgets import QApplication

from ui_new.tokens import COLORS, FONT_FAMILY, SIZES, token_map

ASSETS = Path(__file__).parent / "assets"
QSS_PATH = Path(__file__).parent / "theme.qss"
FONT_DIR = ASSETS / "fonts"


def pixel_font(family_key: str, size_key: str) -> QFont:
    """Build a QFont sized in integer px with hinting/antialiasing tuned for
    the bundled bitmap-style fonts. Use this instead of `QFont(family, pt)`
    anywhere we set a font in Python."""
    f = QFont(FONT_FAMILY[family_key])
    f.setPixelSize(SIZES[size_key])
    f.setStyleStrategy(
        QFont.StyleStrategy.NoAntialias | QFont.StyleStrategy.PreferMatch
    )
    f.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
    return f


def _load_bundled_fonts() -> None:
    """Register every bundled TTF, then warn if any voice family is missing."""
    loaded: list[str] = []
    if FONT_DIR.exists():
        for ttf in sorted(FONT_DIR.glob("*.ttf")):
            font_id = QFontDatabase.addApplicationFont(str(ttf))
            if font_id < 0:
                print(f"[ui_new] failed to register {ttf.name}", file=sys.stderr)
                continue
            loaded.extend(QFontDatabase.applicationFontFamilies(font_id))

    available = set(loaded) | set(QFontDatabase.families())
    for voice, family in FONT_FAMILY.items():
        if family not in available:
            print(
                f"[ui_new] font missing for {voice!r}: {family!r} — "
                f"will fall back to system serif/mono",
                file=sys.stderr,
            )


def _render_qss() -> str:
    template = Template(QSS_PATH.read_text(encoding="utf-8"))
    return template.substitute(token_map())


def apply(app: QApplication) -> None:
    _load_bundled_fonts()
    app.setFont(pixel_font("body", "body"))

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

    app.setStyleSheet(_render_qss())
