from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget

from ui_new.theme import pixel_font
from ui_new.tokens import COLORS, SPACE
from ui_new.widgets.form import FormSection
from ui_new.widgets.slider import LabeledSlider


_FIELDS = [
    ("Strength",   "str",  0, 100),
    ("Dexterity",  "dex",  0, 100),
    ("Mana",       "mana", 0, 1000),
    ("Hit Points", "hp",   0, 1000),
]


def _attr_cell(model, label: str, attr: str, lo: int, hi: int) -> QWidget:
    cell = QWidget()
    grid = QGridLayout(cell)
    grid.setContentsMargins(0, 0, 0, 0)
    grid.setHorizontalSpacing(SPACE["lg"])
    grid.setVerticalSpacing(SPACE["xs"])

    name = QLabel(label)
    name.setFont(pixel_font("body", "label"))

    value = QLabel(str(model.get(attr)))
    value.setFont(pixel_font("mono", "readout"))
    value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    value.setStyleSheet(f"color: {COLORS['gold']};")

    slider = LabeledSlider(lo, hi, model.get(attr), show_readout=False)

    def on_change(v: int) -> None:
        value.setText(str(v))
        model.set(attr, v)

    slider.valueChanged.connect(on_change)

    grid.addWidget(name,   0, 0)
    grid.addWidget(value,  0, 1, Qt.AlignmentFlag.AlignRight)
    grid.addWidget(slider, 1, 0, 1, 2)
    return cell


def build(model) -> QWidget:
    root = QWidget()
    layout = QVBoxLayout(root)
    layout.setContentsMargins(SPACE["xl"], SPACE["sm"], SPACE["xl"], SPACE["xl"])
    layout.setSpacing(0)

    section = FormSection("Attributes")
    grid = QGridLayout()
    grid.setHorizontalSpacing(SPACE["xxl"])
    grid.setVerticalSpacing(SPACE["xl"])
    for idx, (label, attr, lo, hi) in enumerate(_FIELDS):
        row, col = divmod(idx, 2)
        grid.addWidget(_attr_cell(model, label, attr, lo, hi), row, col)
    section.addLayout(grid)
    layout.addWidget(section)

    layout.addStretch()
    return root
