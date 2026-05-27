# ui/tabs/skills_tab.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QButtonGroup, QRadioButton
from PyQt6.QtGui import QFont

from ui.widgets import (create_styled_label, create_styled_scale,
                        create_styled_frame, create_styled_combo)
from constants.colors import BG_DARK, BG_LIGHT, TEXT_PRIMARY, FONT_PRIMARY
from data.fights import fightMap


def _radio_style() -> str:
    return f"""
        QRadioButton {{
            color: {TEXT_PRIMARY};
            font-family: {FONT_PRIMARY[0]};
            font-size: {FONT_PRIMARY[1]}pt;
            background: transparent;
            spacing: 5px;
        }}
        QRadioButton::indicator {{
            width: 14px; height: 14px;
            border: 1px solid {TEXT_PRIMARY};
            border-radius: 7px;
            background: {BG_LIGHT};
        }}
        QRadioButton::indicator:checked {{
            background: {TEXT_PRIMARY};
        }}
    """


def build(parent: QWidget, npc, handlers) -> None:
    layout = parent.layout()
    layout.setSpacing(0)

    # --- Combat style combo ---
    layout.addWidget(create_styled_label(parent, "Combat Style", bold=True))
    layout.addSpacing(5)

    fightCombo = create_styled_combo(parent, list(fightMap.keys()))
    fightCombo.currentTextChanged.connect(
        lambda text: handlers.assignAttribute("fight", lambda: fightMap.get(text)))
    layout.addWidget(fightCombo)
    layout.addSpacing(20)

    # --- Weapon proficiency radio rows ---
    layout.addWidget(create_styled_label(parent, "Weapon Proficiency", bold=True))
    layout.addSpacing(10)

    talent_rows = [
        ("1H Weapon", "none", handlers.setTalent1H),
        ("2H Weapon", "none", handlers.setTalent2H),
        ("Bow",       "none", handlers.setTalentBow),
        ("Crossbow",  "none", handlers.setTalentCBow),
    ]

    for label_text, default, setter in talent_rows:
        row = create_styled_frame(parent)
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(0)

        row_layout.addWidget(create_styled_label(row, label_text))
        row_layout.addSpacing(20)

        group = QButtonGroup(row)   # ensures mutual exclusivity within the row
        for btn_text, value in [("None", "none"), ("Apprentice", "apprentice"), ("Master", "master")]:
            rb = QRadioButton(btn_text, row)
            rb.setStyleSheet(_radio_style())
            rb.setChecked(value == default)
            # Capture value and setter for the signal
            rb.toggled.connect(
                lambda checked, v=value, s=setter: s(v) if checked else None)
            group.addButton(rb)
            row_layout.addWidget(rb)
            row_layout.addSpacing(5)

        row_layout.addStretch()
        layout.addWidget(row)
        layout.addSpacing(5)

    layout.addSpacing(10)

    # --- Magic circle slider ---
    layout.addWidget(create_styled_label(parent, "Magic Circle", bold=True))
    layout.addSpacing(5)

    magicSlider = create_styled_scale(parent, 0, 6)
    magicSlider.setValue(npc.magic)
    magicSlider.valueChanged.connect(
        lambda v: handlers.assignAttribute("magic", lambda: v, int))
    layout.addWidget(magicSlider)

    layout.addStretch()
