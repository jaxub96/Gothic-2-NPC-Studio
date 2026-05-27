from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QCheckBox, QComboBox, QLineEdit, QVBoxLayout, QWidget

from data.guilds import guildMap
from data.types import typeMap
from ui_new.widgets.form import FormSection
from ui_new.widgets.slider import LabeledSlider


def build(model) -> QWidget:
    root = QWidget()
    layout = QVBoxLayout(root)
    layout.setContentsMargins(28, 8, 28, 28)
    layout.setSpacing(0)

    identity = FormSection("Identity")
    name_edit = QLineEdit(model.get("name"))
    name_edit.setPlaceholderText("Diego, Xardas, Lee…")
    name_edit.textChanged.connect(lambda v: model.set("name", v))
    identity.addField("Name", name_edit)

    id_edit = QLineEdit(str(model.get("id")))
    id_edit.setPlaceholderText("001 – 999")
    id_edit.setValidator(QIntValidator(0, 999))
    id_edit.setMaxLength(3)
    id_edit.textChanged.connect(lambda v: model.set("id", v))
    identity.addField("ID", id_edit)

    immortal = QCheckBox("Cannot be killed")
    immortal.setChecked(bool(model.get("immortal")))
    immortal.stateChanged.connect(lambda s: model.set("immortal", int(bool(s))))
    identity.addField("Immortal", immortal)
    layout.addWidget(identity)

    role = FormSection("Role")
    level = LabeledSlider(0, 100, model.get("level"))
    level.valueChanged.connect(lambda v: model.set("level", v))
    role.addField("Level", level)

    guild = QComboBox()
    guild.addItems(list(guildMap.keys()))
    guild.currentTextChanged.connect(lambda t: model.set("guild", guildMap.get(t)))
    role.addField("Guild", guild)

    npc_type = QComboBox()
    npc_type.addItems(list(typeMap.keys()))
    npc_type.currentTextChanged.connect(lambda t: model.set("type", typeMap.get(t)))
    role.addField("Type", npc_type)
    layout.addWidget(role)

    layout.addStretch()
    return root
