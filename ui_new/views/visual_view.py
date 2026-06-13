from PySide6.QtWidgets import QComboBox, QVBoxLayout, QWidget

from constants.mappings import bodyTextures, faces, skinColors, teethTextures
from data.heads import headMap
from data.voices import voiceMap
from data.walkings import walkingMap
from ui_new.binding import select_combo_by_value, select_int_combo
from ui_new.tokens import SPACE
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
    layout.setContentsMargins(SPACE["xl"], SPACE["sm"], SPACE["xl"], SPACE["xl"])
    layout.setSpacing(0)

    body = FormSection("Body")

    head = _map_combo(headMap)
    select_combo_by_value(head, headMap, model.get("head"))
    head.currentTextChanged.connect(lambda t: model.set("head", headMap.get(t)))
    body.addField("Head", head)
    head.currentTextChanged.emit(head.currentText())

    walking = _map_combo(walkingMap)
    select_combo_by_value(walking, walkingMap, model.get("walking"))
    walking.currentTextChanged.connect(lambda t: model.set("walking", walkingMap.get(t)))
    body.addField("Gait", walking)

    voice = _map_combo(voiceMap)
    select_combo_by_value(voice, voiceMap, model.get("voice"))
    voice.currentTextChanged.connect(lambda t: model.set("voice", voiceMap.get(t, 0)))
    body.addField("Voice", voice)
    layout.addWidget(body)

    skin = FormSection("Skin & Face")

    body_tex = _int_combo(range(1, bodyTextures + 1))
    select_int_combo(body_tex, model.get("body_tex"))
    body_tex.currentTextChanged.connect(lambda t: model.set("body_tex", int(t)))
    skin.addField("Body Texture", body_tex)

    skin_color = _int_combo(range(1, skinColors + 1))
    select_int_combo(skin_color, model.get("skin_color"))
    skin_color.currentTextChanged.connect(lambda t: model.set("skin_color", int(t)))
    skin.addField("Skin Tone", skin_color)

    face = _int_combo(range(1, faces + 1))
    select_int_combo(face, model.get("face"))
    face.currentTextChanged.connect(lambda t: model.set("face", int(t)))
    skin.addField("Face", face)

    teeth = _int_combo(range(1, teethTextures + 1))
    select_int_combo(teeth, model.get("teeth_tex"))
    teeth.currentTextChanged.connect(lambda t: model.set("teeth_tex", int(t)))
    skin.addField("Teeth", teeth)
    layout.addWidget(skin)

    layout.addStretch()
    return root
