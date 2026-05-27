from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QHBoxLayout,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from constants.mappings import talentLevelMap
from data.fights import fightMap
from ui_new.widgets.form import FormSection
from ui_new.widgets.slider import LabeledSlider


_TALENT_ATTRS = [
    ("1-Handed", "t1h"),
    ("2-Handed", "t2h"),
    ("Bow",      "bow"),
    ("Crossbow", "cbow"),
]
_TALENT_LEVELS = [("None", "none"), ("Apprentice", "apprentice"), ("Master", "master")]


def _talent_row(model, attr: str) -> QWidget:
    row = QWidget()
    lay = QHBoxLayout(row)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(22)

    group = QButtonGroup(row)
    group.setExclusive(True)

    for text, key in _TALENT_LEVELS:
        rb = QRadioButton(text, row)
        rb.setChecked(key == "none")
        rb.toggled.connect(
            lambda checked, k=key, a=attr: checked and model.set(a, talentLevelMap[k])
        )
        group.addButton(rb)
        lay.addWidget(rb)
    lay.addStretch()
    return row


def build(model) -> QWidget:
    root = QWidget()
    layout = QVBoxLayout(root)
    layout.setContentsMargins(28, 8, 28, 28)
    layout.setSpacing(0)

    combat = FormSection("Combat")
    fight = QComboBox()
    fight.addItems(list(fightMap.keys()))
    fight.currentTextChanged.connect(lambda t: model.set("fight", fightMap.get(t)))
    combat.addField("Tactic", fight)

    magic = LabeledSlider(0, 6, model.get("magic"))
    magic.valueChanged.connect(lambda v: model.set("magic", v))
    combat.addField("Magic Circle", magic)
    layout.addWidget(combat)

    weapons = FormSection("Weapon Proficiency")
    for label, attr in _TALENT_ATTRS:
        weapons.addField(label, _talent_row(model, attr))
    layout.addWidget(weapons)

    layout.addStretch()
    return root
