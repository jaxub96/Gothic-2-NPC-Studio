from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPlainTextEdit

from services.output_builder import buildOutput
from ui_new.widgets.highlighter import DaedalusHighlighter


class CodePreviewPane(QPlainTextEdit):
    """Live, syntax-highlighted Daedalus preview using VT323 pixel mono."""

    REFRESH_MS = 120

    def __init__(self, model, parent=None) -> None:
        super().__init__(parent)
        self.setReadOnly(True)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        mono = QFont("VT323", 16)
        self.setFont(mono)

        self._model = model
        self._highlighter = DaedalusHighlighter(self.document())

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(self.REFRESH_MS)
        self._timer.timeout.connect(self._render)

        model.changed.connect(lambda _attr: self._timer.start())
        self._render()

    def _render(self) -> None:
        self.setPlainText(buildOutput(self._model.npc))
