from pathlib import Path
from string import Template

from PySide6.QtGui import QColor, QFont, QFontDatabase, QPalette
from PySide6.QtWidgets import QApplication

from ui_new.tokens import COLORS, FONT_FAMILY, SIZES, token_map

ASSETS = Path(__file__).parent / "assets"
QSS_PATH = Path(__file__).parent / "theme.qss"
FONT_DIR = ASSETS / "fonts"


def _load_bundled_fonts() -> None:
    """Register every bundled TTF so QSS can address it by family name."""
    if not FONT_DIR.exists():
        return
    for ttf in sorted(FONT_DIR.glob("*.ttf")):
        QFontDatabase.addApplicationFont(str(ttf))


def _render_qss() -> str:
    template = Template(QSS_PATH.read_text(encoding="utf-8"))
    return template.substitute(token_map())


def apply(app: QApplication) -> None:
    _load_bundled_fonts()

    base = QFont(FONT_FAMILY["body"], SIZES["body"])
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

    app.setStyleSheet(_render_qss())
