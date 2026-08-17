# ui/tabs/general_tab.py

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QIntValidator

from ui.widgets import (create_styled_label, create_styled_entry,
                        create_styled_scale, create_styled_checkbutton,
                        create_styled_combo)
from data.guilds import guildMap
from data.npc_types import typeMap
from constants.colors import TEXT_PRIMARY, FONT_PRIMARY

def build(parent: QWidget, npc, handlers) -> None:
    layout = parent.layout()
    layout.setSpacing(0)

    # --- Name ---
    layout.addWidget(create_styled_label(parent, "Character Name", bold=True))
    layout.addSpacing(5)

    nameEntry = create_styled_entry(parent)
    nameEntry.setText(npc.name)
    nameEntry.textChanged.connect(lambda v: handlers.assignAttribute("name", lambda: v))
    layout.addWidget(nameEntry)
    layout.addSpacing(15)

    # --- ID ---
    layout.addWidget(create_styled_label(parent, "Character ID", bold=True))
    layout.addSpacing(5)

    idEntry = create_styled_entry(parent)
    idEntry.setText(npc.id)
    # Restrict to max 3 digits via a validator
    idEntry.setValidator(QIntValidator(0, 999))
    idEntry.textChanged.connect(lambda v: handlers.assignAttribute("id", lambda: v))
    layout.addWidget(idEntry)
    layout.addSpacing(15)

    # --- level slider
    layout.addWidget(create_styled_label(parent, "Level", bold=True))
    layout.addSpacing(5)
    levelSlider = create_styled_scale(parent, 0, 100)
    levelSlider.setValue(npc.level)
    levelSlider.valueChanged.connect(
        lambda v: handlers.assignAttribute("level", lambda: v, int))


    levelValue = QLabel(str(levelSlider.value()), parent)
    levelValue.setFixedWidth(28)
    levelValue.setStyleSheet(f"""
        background: transparent;
        color: {TEXT_PRIMARY};
        font-family: {FONT_PRIMARY[0]};
        font-size: {FONT_PRIMARY[1]}pt;
        font-weight: bold;
    """)
    levelSlider.valueChanged.connect(lambda v: levelValue.setText(str(v)))
    slider_row = QHBoxLayout()
    slider_row.addWidget(levelSlider)
    slider_row.addWidget(levelValue)
    layout.addLayout(slider_row)
    layout.addSpacing(15)

    # --- Guild ---
    layout.addWidget(create_styled_label(parent, "Guild Affiliation", bold=True))
    layout.addSpacing(5)

    guildCombo = create_styled_combo(parent, list(guildMap.keys()))
    guildCombo.currentTextChanged.connect(
        lambda text: handlers.assignAttribute("guild", lambda: guildMap.get(text)))
    layout.addWidget(guildCombo)
    layout.addSpacing(15)
    # --- npc type --- 
    layout.addWidget(create_styled_label(parent, "NPC Type", bold=True))
    layout.addSpacing(5)

    typeCombo = create_styled_combo(parent, list(typeMap.keys()))
    typeCombo.currentTextChanged.connect(
        lambda text: handlers.assignAttribute("type", lambda: typeMap.get(text)))
    layout.addWidget(typeCombo)
    layout.addSpacing(15)

    # --- Checkboxes ---
    checkRow = QWidget(parent)
    checkRow.setStyleSheet("background: transparent;")
    checkLayout = QHBoxLayout(checkRow)
    checkLayout.setContentsMargins(0, 0, 0, 0)
    checkLayout.setSpacing(20)

    immortalCb = create_styled_checkbutton(checkRow, " Immortal")
    immortalCb.stateChanged.connect(
        lambda state: handlers.assignAttribute("immortal", lambda: int(bool(state)), int))
    checkLayout.addWidget(immortalCb)


    checkLayout.addStretch()
    layout.addWidget(checkRow)

    layout.addStretch()   # push everything to the top
