# ui/app.py

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTextEdit, QPushButton, QLabel, QFrame, QSizePolicy, 
)
from PyQt6.QtGui import QFont, QColor, QPalette,QSyntaxHighlighter, QTextCharFormat
from PyQt6.QtCore import Qt
import sys
import re

from models.DaedalusHighlighter import DaedalusHighlighter
from constants.colors import THEME
from constants.colors import BG_DARK, BG_MEDIUM, TEXT_PRIMARY, TEXT_SECONDARY, ACCENT_PRIMARY, WARNING_COLOR, SUCCESS_COLOR
from constants.colors import FONT_PRIMARY
from ui.tabs import general_tab, stats_tab, inventory_tab, skills_tab, visual_tab
from handlers.npc_handlers import NpcHandlers
from services.output_builder import buildOutput
from services.file_service import generateFile


# ---------------------------------------------------------------------------
# Helpers (replacements for ui/widgets.py helpers)
# ---------------------------------------------------------------------------

def _make_button(label: str, icon: str, color: str = THEME["accent_primary"]) -> QPushButton:
    """Create a styled QPushButton."""
    btn = QPushButton(f"{icon}  {label}")
    btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {color};
            color: {THEME["text_primary"]};
            border: none;
            border-radius: 4px;
            padding: 8px 12px;
            font-family: {THEME["font_ui"]};
            font-size: 11px;
            font-weight: bold;
            text-align: left;
        }}
        QPushButton:hover {{
            background-color: {_lighten(color)};
        }}
        QPushButton:pressed {{
            background-color: {_darken(color)};
        }}
    """)
    return btn


def _lighten(hex_color: str, amount: int = 20) -> str:
    """Return a slightly lighter hex color string."""
    c = QColor(hex_color)
    return QColor(
        min(c.red()   + amount, 255),
        min(c.green() + amount, 255),
        min(c.blue()  + amount, 255),
    ).name()


def _darken(hex_color: str, amount: int = 20) -> str:
    """Return a slightly darker hex color string."""
    c = QColor(hex_color)
    return QColor(
        max(c.red()   - amount, 0),
        max(c.green() - amount, 0),
        max(c.blue()  - amount, 0),
    ).name()


def _apply_dark_palette(app: QApplication) -> None:
    """Push a dark QPalette onto the whole application."""
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window,          QColor(BG_DARK))
    palette.setColor(QPalette.ColorRole.WindowText,      QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Base,            QColor(BG_MEDIUM))
    palette.setColor(QPalette.ColorRole.AlternateBase,   QColor(BG_DARK))
    palette.setColor(QPalette.ColorRole.ToolTipBase,     QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.ToolTipText,     QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Text,            QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Button,          QColor(BG_MEDIUM))
    palette.setColor(QPalette.ColorRole.ButtonText,      QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Highlight,       QColor(ACCENT_PRIMARY))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(TEXT_PRIMARY))
    app.setPalette(palette)


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class NpcCreatorWindow(QMainWindow):
    def __init__(self, npc):
        super().__init__()
        self.npc = npc
        self.setWindowTitle("Gothic - NPC Creator Studio")
        self.resize(1000, 800 )

        self.handlers = NpcHandlers(npc, self.refresh)

        # --- Root layout ---
        root_widget = QWidget()
        self.setCentralWidget(root_widget)
        root_layout = QHBoxLayout(root_widget)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(10)

        # --- Notebook (left, weight 2) ---
        self.notebook = QTabWidget()
        self.notebook.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {BG_MEDIUM};
                background: {BG_DARK};
            }}
            QTabBar::tab {{
                background: {BG_MEDIUM};
                color: {TEXT_SECONDARY};
                padding: 8px 14px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }}
            QTabBar::tab:selected {{
                background: {ACCENT_PRIMARY};
                color: {TEXT_PRIMARY};
            }}
        """)

        tab_general   = QWidget(); tab_general.setLayout(QVBoxLayout())
        tab_stats     = QWidget(); tab_stats.setLayout(QVBoxLayout())
        tab_inventory = QWidget(); tab_inventory.setLayout(QVBoxLayout())
        tab_skills    = QWidget(); tab_skills.setLayout(QVBoxLayout())
        tab_visual    = QWidget(); tab_visual.setLayout(QVBoxLayout())
        tab_other     = QWidget(); tab_other.setLayout(QVBoxLayout())

        self.notebook.addTab(tab_general,   f" General")
        self.notebook.addTab(tab_stats,     f" Stats")
        self.notebook.addTab(tab_inventory, f" Inventory")
        self.notebook.addTab(tab_skills,    f" Skills")
        self.notebook.addTab(tab_visual,    f" Visual")
        self.notebook.addTab(tab_other,     f" Other")

        # --- Preview panel (right, weight 1) ---
        preview_frame = QFrame()
        preview_frame.setStyleSheet(f"background: {BG_DARK};")
        preview_layout = QVBoxLayout(preview_frame)
        preview_layout.setContentsMargins(5, 5,5, 5)
        preview_layout.setSpacing(5)

        header = QLabel("PREVIEW")
        header.setFont(QFont(FONT_PRIMARY[0], 12, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {TEXT_PRIMARY};")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(header)

        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setFont(QFont("Consolas", 9))
        self.preview_text.setStyleSheet(f"""
            QTextEdit {{
                background: {BG_MEDIUM};
                color: {TEXT_PRIMARY};
                border: none;
                padding: 10px;
            }}
        """)
        preview_layout.addWidget(self.preview_text, stretch=1)

        btn_refresh = _make_button("Refresh Preview", None)
        btn_refresh.clicked.connect(self.refresh)
        preview_layout.addWidget(btn_refresh)

        btn_random = _make_button("Randomize", None, WARNING_COLOR)
        btn_random.clicked.connect(self.refresh)   # wire to randomize handler later
        preview_layout.addWidget(btn_random)

        btn_save = _make_button("Generate File", None, SUCCESS_COLOR)
        btn_save.clicked.connect(
            lambda: generateFile(npc, lambda: self.generate_label.setText("File generated!"))
        )
        preview_layout.addWidget(btn_save)

        self.generate_label = QLabel("✓ File will be saved to current directory")
        self.generate_label.setFont(QFont(FONT_PRIMARY[0], 8))
        self.generate_label.setStyleSheet(f"color: {TEXT_SECONDARY};")
        self.generate_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(self.generate_label)

        # --- Assemble left/right with stretch ratio 2:1 ---
        root_layout.addWidget(self.notebook,    stretch=1)
        root_layout.addWidget(preview_frame,    stretch=1)

        # --- Build tab contents ---
        general_tab.build(tab_general,     npc, self.handlers)
        stats_tab.build(tab_stats,         npc, self.handlers)
        inventory_tab.build(tab_inventory, npc, self.handlers)
        skills_tab.build(tab_skills,       npc, self.handlers)
        visual_tab.build(tab_visual,       npc, self.handlers)

        # --- Initial render ---
        self.refresh()

    def refresh(self):
        self.preview_text.setPlainText(buildOutput(self.npc))
        DaedalusHighlighter(self.preview_text.document())
        self.generate_label.setText("Unsaved changes")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
from constants.colors import THEME

def launch(npc):
    app = QApplication.instance() or QApplication(sys.argv)
    _apply_dark_palette(app)
    app.setStyleSheet(f"""
    QWidget {{
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 #ffffff,
            stop:0.6 #edf2f8,
            stop:1 #bbcde5
        );
        color: #222222;
    }}
    QTabBar::tab {{
        background: transparent;
        color: #639fab;
        padding: 6px 14px;
        border: none;
    }}
    QTabBar::tab:selected {{
        color: #1c5d99;
        border-bottom: 2px solid #1c5d99;
    }}
    QTabBar::tab:hover {{
        color: #222222;
    }}
""")
    window = NpcCreatorWindow(npc)
    window.show()
    sys.exit(app.exec())