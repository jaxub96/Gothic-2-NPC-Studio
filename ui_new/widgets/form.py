from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFormLayout, QGroupBox, QLabel, QLayout, QWidget

from ui_new.tokens import SPACE


class FormSection(QGroupBox):
    """Titled section with a clean QFormLayout interior."""

    LABEL_MIN_WIDTH = 140

    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(title, parent)
        self._form = QFormLayout(self)
        self._form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self._form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        self._form.setHorizontalSpacing(SPACE["xl"])
        self._form.setVerticalSpacing(SPACE["lg"] + 4)
        self._form.setContentsMargins(0, SPACE["xs"], 0, SPACE["xs"])
        self._form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

    def addField(self, label: str, widget: QWidget) -> None:
        lbl = QLabel(label)
        lbl.setMinimumWidth(self.LABEL_MIN_WIDTH)
        self._form.addRow(lbl, widget)

    def addWidget(self, widget: QWidget) -> None:
        self._form.addRow(widget)

    def addLayout(self, layout: QLayout) -> None:
        self._form.addRow(layout)
