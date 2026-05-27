import sys

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout

from ui.app import NpcCreatorWindow, _apply_dark_palette
from ui.tabs import viewport_tab


def launch(npc):
    app = QApplication.instance() or QApplication(sys.argv)
    _apply_dark_palette(app)
    window = NpcCreatorWindow(npc)
    window.setWindowTitle("Gothic - NPC Creator Studio  [NEW UI / 3D]")

    viewport = QWidget()
    viewport.setLayout(QVBoxLayout())
    window.notebook.addTab(viewport, " 3D Viewport")
    viewport_tab.build(viewport, npc, window.handlers)
    window.notebook.setCurrentWidget(viewport)

    window.show()
    sys.exit(app.exec())
