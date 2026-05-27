from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSlider, QWidget

from ui_new.theme import pixel_font
from ui_new.tokens import CHROME, COLORS, SPACE


class LabeledSlider(QWidget):
    """Horizontal slider with a chunky pixel numeric readout."""

    valueChanged = Signal(int)

    def __init__(
        self,
        minimum: int,
        maximum: int,
        value: int = 0,
        suffix: str = "",
        show_readout: bool = True,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._suffix = suffix

        self._slider = QSlider(Qt.Orientation.Horizontal, self)
        self._slider.setRange(minimum, maximum)
        self._slider.setValue(value)

        self._readout = QLabel(self._format(value), self)
        self._readout.setFont(pixel_font("mono", "readout"))
        self._readout.setFixedWidth(CHROME["readout_w"])
        self._readout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self._readout.setStyleSheet(f"color: {COLORS['gold']};")
        self._readout.setVisible(show_readout)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(SPACE["lg"])
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
