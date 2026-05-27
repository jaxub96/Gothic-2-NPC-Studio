# ui/tabs/visual_tab.py
#
# Note: the original tkinter version had a scoping bug — the combo/bind loop
# only wired up the last combo because `combo` and `attr` were overwritten
# each iteration before the bind fired. This version fixes that correctly
# using default-argument capture in lambdas.

from PyQt6.QtWidgets import QWidget
from ui.widgets import create_styled_label, create_styled_combo
from data.heads import headMap
from data.walkings import walkingMap
from data.voices import voiceMap
from constants.mappings import  faces, skinColors, bodyTextures, teethTextures

def build(parent: QWidget, npc, handlers) -> None:
    layout = parent.layout()
    layout.setSpacing(0)

    rows = [
        ("Head Model",    "head",    headMap,    False),
        ("Walking Style", "walking", walkingMap, False),
        ("Voice Type",    "voice",   voiceMap,   True),   # voice needs int cast
        ("Body Texture",  "body_tex", range(1, bodyTextures+1), True),#int 1-? 
        ("Skin Color",    "skin_color", range(1, skinColors+1), True),#skincolor 1-?
        ("Face",  "face", range(1, faces+1), True),#face 1-?
        ("Teeth Texture", "teeth_tex", range(1, teethTextures+1), True)#teethtex 1-?

    ]


    for text, attr, mapping, is_int in rows:
        layout.addWidget(create_styled_label(parent, text, bold=True))
        layout.addSpacing(5)

        if isinstance(mapping, dict):
            values = list(mapping.keys())
            if is_int:
                connect = lambda t, a=attr, m=mapping: handlers.assignAttribute(a, lambda: int(m.get(t)))
            else:
                connect = lambda t, a=attr, m=mapping: handlers.assignAttribute(a, lambda: m.get(t))
        else:
            values = [str(i) for i in mapping]  # convert ints to strings
            connect = lambda t, a=attr: handlers.assignAttribute(a, lambda: int(t))

        combo = create_styled_combo(parent, values)
        combo.currentTextChanged.connect(connect)

        layout.addWidget(combo)
        layout.addSpacing(15)

    layout.addStretch()