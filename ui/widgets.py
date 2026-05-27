# ui/widgets.py
#
# Full replacement for the tkinter widget helpers.
# Every function returns a QWidget subclass; the caller adds it to a layout.

from PyQt6.QtWidgets import (
    QLabel, QLineEdit, QPushButton, QSlider, QCheckBox,
    QFrame, QWidget, QComboBox, QSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QStyleFactory

from constants.colors import (
    BG_DARK, BG_MEDIUM, BG_LIGHT,
    ACCENT_PRIMARY, ACCENT_SECONDARY,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_DARK,
    FONT_PRIMARY,
)






# ---------------------------------------------------------------------------
# Internal colour helper
# ---------------------------------------------------------------------------

def _hover_color(hex_color: str, amount: int = 20) -> str:
    c = QColor(hex_color)
    return QColor(
        min(c.red()   + amount, 255),
        min(c.green() + amount, 255),
        min(c.blue()  + amount, 255),
    ).name()


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def create_styled_label(parent: QWidget, text: str,
                        font_size: int = 10, bold: bool = False) -> QLabel:
    label = QLabel(text, parent)
    weight = QFont.Weight.Bold if bold else QFont.Weight.Normal
    label.setFont(QFont(FONT_PRIMARY[0], font_size, weight))
    label.setStyleSheet(f"color: {TEXT_SECONDARY}; background: transparent;")
    return label


def create_styled_entry(parent: QWidget, **kwargs) -> QLineEdit:
    entry = QLineEdit(parent)
    entry.setStyleSheet(f"""
        QLineEdit {{
            background: {BG_LIGHT};
            color: {TEXT_PRIMARY};
            border: none;
            border-radius: 3px;
            padding: 6px 8px;
            font-family: {FONT_PRIMARY[0]};
            font-size: {FONT_PRIMARY[1]}pt;
            selection-background-color: {ACCENT_PRIMARY};
        }}
    """)
    return entry


def create_styled_button(parent: QWidget, text: str, command, bg_color: str = ACCENT_PRIMARY) -> QPushButton:
    label = f"{text}" 
    btn = QPushButton(label, parent)
    hover = _hover_color(bg_color)
    btn.setStyleSheet(f"""
        QPushButton {{
            background: {bg_color};
            color: {TEXT_PRIMARY};
            border: none;
            border-radius: 4px;
            padding: 8px 15px;
            font-family: {FONT_PRIMARY[0]};
            font-size: {FONT_PRIMARY[1]}pt;
            text-align: left;
        }}
        QPushButton:hover  {{ background: {hover}; }}
        QPushButton:pressed {{ background: {bg_color}; }}
    """)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    if command:
        btn.clicked.connect(command)
    return btn


def create_styled_scale(parent: QWidget, from_: int, to: int,
                         command=None, orient: str = "horizontal") -> QSlider:
    orientation = (Qt.Orientation.Horizontal
                   if orient == "horizontal"
                   else Qt.Orientation.Vertical)
    slider = QSlider(orientation, parent)
    slider.setStyle(QStyleFactory.create("Fusion"))

    slider.setMinimum(from_)
    slider.setMaximum(to)
    slider.setStyleSheet(f"""
        QSlider::groove:horizontal {{
            border: none;
            background: rgba(0,0,0,0.3);
            height: 1px;
            margin: 0px;
        }}
        QSlider::handle:horizontal {{
            background: {ACCENT_PRIMARY};
            border: none;
            width: 8px;
            height: 8px;
            margin: -4px 0px;
            border-radius: 4px;
        }}
        QSlider::sub-page:horizontal {{
            background: {ACCENT_PRIMARY};
            border: none;
            height: 1px;
            margin: 0px;
        }}
        QSlider::add-page:horizontal {{
            background: rgba(0,0,0,0.3);
            border: none;
            height: 1px;
            margin: 0px;
        }}
    """)

    if command:
        slider.valueChanged.connect(command)
    return slider


def create_styled_checkbutton(parent: QWidget, text: str,
                               command=None) -> QCheckBox:
    """Returns a QCheckBox. Use .isChecked() instead of a tk.IntVar."""
    cb = QCheckBox(text, parent)
    cb.setStyleSheet(f"""
        QCheckBox {{
            color: {TEXT_PRIMARY};
            font-family: {FONT_PRIMARY[0]};
            font-size: {FONT_PRIMARY[1]}pt;
            spacing: 6px;
            background: transparent;
        }}
        QCheckBox::indicator {{
            width: 16px; height: 16px;
            border: 1px solid {ACCENT_PRIMARY};
            border-radius: 3px;
            background: {BG_LIGHT};
        }}
        QCheckBox::indicator:checked {{
            background: {ACCENT_PRIMARY};
        }}
    """)
    cb.setCursor(Qt.CursorShape.PointingHandCursor)
    if command:
        cb.stateChanged.connect(lambda _: command())
    return cb


def create_styled_frame(parent: QWidget = None, **kwargs) -> QFrame:
    frame = QFrame(parent)
    frame.setStyleSheet(f"background: {BG_DARK}; border: none;")
    return frame
def create_styled_spinbox(parent: QWidget, min_val: int = 1, max_val: int = 100, default: int = 1) -> QSpinBox:
    spinbox = QSpinBox(parent)
    spinbox.setMinimum(min_val)
    spinbox.setMaximum(max_val)
    spinbox.setValue(default)
    spinbox.setFixedWidth(60)
    spinbox.setStyleSheet(f"""
        QSpinBox {{
            background: {BG_DARK};
            color: {TEXT_PRIMARY};
            border: none;
            border-radius: 3px;
            padding: 5px 8px;
            font-family: {FONT_PRIMARY[0]};
            font-size: {FONT_PRIMARY[1]}pt;
        }}
        QSpinBox::up-button, QSpinBox::down-button {{
            border: {TEXT_PRIMARY} 1px solid;
            background: {BG_LIGHT};
            width: 16px;
        }}
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
            background: {ACCENT_PRIMARY};
        }}
    """)
    return spinbox

def create_styled_combo(parent: QWidget, values: list) -> QComboBox:
    combo = QComboBox(parent)
    combo.addItems(values)
    combo.setStyleSheet(f"""
        QComboBox {{
            background: {BG_LIGHT};
            color: {TEXT_PRIMARY};
            border: none;
            border-radius: 3px;
            padding: 5px 8px;
            font-family: {FONT_PRIMARY[0]};
            font-size: {FONT_PRIMARY[1]}pt;
        }}
        QComboBox::drop-down {{ border: none; }}
        QComboBox QAbstractItemView {{
            background: {BG_LIGHT};
            color: {TEXT_PRIMARY};
            selection-background-color: {ACCENT_PRIMARY};
            selection-color: {TEXT_PRIMARY};
            border: none;
        }}
    """)
    return combo
