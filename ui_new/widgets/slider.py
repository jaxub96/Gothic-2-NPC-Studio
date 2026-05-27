from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSlider, QWidget


class LabeledSlider(QWidget):
    """Horizontal slider with a chunky pixel numeric readout."""

    valueChanged = Signal(int)

    def __init__(
        self,
        minimum: int,
        maximum: int,
        value: int = 0,
        suffix: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._suffix = suffix

        self._slider = QSlider(Qt.Orientation.Horizontal, self)
        self._slider.setRange(minimum, maximum)
        self._slider.setValue(value)

        readout_font = QFont("VT323", 18)

        self._readout = QLabel(self._format(value), self)
        self._readout.setFont(readout_font)
        self._readout.setFixedWidth(52)
        self._readout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self._readout.setStyleSheet("color: #d4a528;")

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(16)
        lay.addWidget(self._slider, stretch=1)
        lay.addWidget(self._readout)

        self._slider.valueChanged.connect(self._on_changed)

    def _format(self, v: int) -> str:
        return f"{v}{self._suffix}"

    def _on_changed(self, v: int) -> None:
        self._readout.setText(self._format(v))
        self.valueChanged.emit(v)

    def setValue(self, v: int) -> None:
        self._slider.setValue(v)

    def value(self) -> int:
        return self._slider.value()
