# ui/tabs/stats_tab.py

from PyQt6.QtWidgets import QWidget
from ui.widgets import create_styled_label, create_styled_scale


def build(parent: QWidget, npc, handlers) -> None:
    layout = parent.layout()
    layout.setSpacing(0)

    create_styled_label(parent, "Combat Attributes", font_size=11, bold=True)
    layout.addWidget(create_styled_label(parent, "Combat Attributes", font_size=11, bold=True))
    layout.addSpacing(15)

    for text, attr, max_val, current in [
        ("Strength",  "str",  100,  npc.str),
        ("Dexterity", "dex",  100,  npc.dex),
        ("Mana",      "mana", 1000, npc.mana),
        ("HP",        "hp",   1000, npc.hp),
    ]:
        layout.addWidget(create_styled_label(parent, text))
        layout.addSpacing(5)

        slider = create_styled_scale(parent, 0, max_val)
        slider.setValue(current)
        # Capture attr by default argument to avoid closure-over-loop issue
        slider.valueChanged.connect(
            lambda v, a=attr: handlers.assignAttribute(a, lambda: v, int))
        layout.addWidget(slider)
        layout.addSpacing(15)

    layout.addSpacing(10)
    layout.addWidget(create_styled_label(parent, "Vital Statistics", font_size=11, bold=True))
    layout.addSpacing(15)

    layout.addStretch()
