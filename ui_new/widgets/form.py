from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFormLayout, QGroupBox, QLabel, QLayout, QWidget


class FormSection(QGroupBox):
    """Titled section with a clean QFormLayout interior."""

    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(title, parent)
        self._form = QFormLayout(self)
        self._form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self._form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        self._form.setHorizontalSpacing(24)
        self._form.setVerticalSpacing(20)
        self._form.setContentsMargins(0, 4, 0, 4)
        self._form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

    def addField(self, label: str, widget: QWidget) -> None:
        lbl = QLabel(label)
        lbl.setMinimumWidth(140)
        self._form.addRow(lbl, widget)

    def addWidget(self, widget: QWidget) -> None:
        self._form.addRow(widget)

    def addLayout(self, layout: QLayout) -> None:
        self._form.addRow(layout)
