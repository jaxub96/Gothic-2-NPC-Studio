from PySide6.QtWidgets import QComboBox, QVBoxLayout, QWidget

from constants.mappings import bodyTextures, faces, skinColors, teethTextures
from data.heads import headMap
from data.voices import voiceMap
from data.walkings import walkingMap
from ui_new.widgets.form import FormSection


def _int_combo(values) -> QComboBox:
    c = QComboBox()
    c.addItems([str(v) for v in values])
    return c


def _map_combo(mapping: dict) -> QComboBox:
    c = QComboBox()
    c.addItems(list(mapping.keys()))
    return c


def build(model) -> QWidget:
    root = QWidget()
    layout = QVBoxLayout(root)
    layout.setContentsMargins(28, 8, 28, 28)
    layout.setSpacing(0)

    body = FormSection("Body")
    head = _map_combo(headMap)
    head.currentTextChanged.connect(lambda t: model.set("head", headMap.get(t)))
    body.addField("Head", head)

    walking = _map_combo(walkingMap)
    walking.currentTextChanged.connect(lambda t: model.set("walking", walkingMap.get(t)))
    body.addField("Gait", walking)

    voice = _map_combo(voiceMap)
    voice.currentTextChanged.connect(
        lambda t: model.set("voice", int(voiceMap.get(t)) if voiceMap.get(t) is not None else 0)
    )
    body.addField("Voice", voice)
    layout.addWidget(body)

    skin = FormSection("Skin & Face")
    body_tex = _int_combo(range(1, bodyTextures + 1))
    body_tex.currentTextChanged.connect(lambda t: model.set("body_tex", int(t)))
    skin.addField("Body Texture", body_tex)

    skin_color = _int_combo(range(1, skinColors + 1))
    skin_color.currentTextChanged.connect(lambda t: model.set("skin_color", int(t)))
    skin.addField("Skin Tone", skin_color)

    face = _int_combo(range(1, faces + 1))
    face.currentTextChanged.connect(lambda t: model.set("face", int(t)))
    skin.addField("Face", face)

    teeth = _int_combo(range(1, teethTextures + 1))
    teeth.currentTextChanged.connect(lambda t: model.set("teeth_tex", int(t)))
    skin.addField("Teeth", teeth)
    layout.addWidget(skin)

    layout.addStretch()
    return root
