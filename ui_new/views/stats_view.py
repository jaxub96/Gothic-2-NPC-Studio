from PySide6.QtWidgets import QVBoxLayout, QWidget

from ui_new.widgets.form import FormSection
from ui_new.widgets.slider import LabeledSlider


_FIELDS = [
    ("Strength",  "str",  0, 100),
    ("Dexterity", "dex",  0, 100),
    ("Mana",      "mana", 0, 1000),
    ("Hit Points", "hp",  0, 1000),
]


def build(model) -> QWidget:
    root = QWidget()
    layout = QVBoxLayout(root)
    layout.setContentsMargins(28, 8, 28, 28)
    layout.setSpacing(0)

    section = FormSection("Attributes")
    for label, attr, lo, hi in _FIELDS:
        s = LabeledSlider(lo, hi, model.get(attr))
        s.valueChanged.connect(lambda v, a=attr: model.set(a, v))
        section.addField(label, s)
    layout.addWidget(section)

    layout.addStretch()
    return root
