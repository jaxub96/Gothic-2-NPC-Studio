import sys

from PySide6.QtCore import QByteArray, QSettings, Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSplitter,
    QTabWidget,
    QWidget,
)

from services.file_service import generateFile, getFileName
from ui_new import theme
from ui_new.state import NpcModel
from ui_new.views import (
    general_view,
    inventory_view,
    skills_view,
    stats_view,
    viewport_view,
    visual_view,
)
from ui_new.widgets.preview import CodePreviewPane


_ORG = "GothicMods"
_APP = "NPC-Studio-New"


class NewMainWindow(QMainWindow):
    def __init__(self, npc) -> None:
        super().__init__()
        self.model = NpcModel(npc)
        self.setWindowTitle("Gothic II — NPC Studio")
        self.resize(1600, 1000)
        self.setMinimumSize(1280, 820)

        self._settings = QSettings(_ORG, _APP)
        self._build_menu()
        self._build_central()
        self._wire_status()
        self._restore_geometry()

    # ------------------------------------------------------------------ setup

    def _build_central(self) -> None:
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setMovable(False)
        tabs.setUsesScrollButtons(False)
        tabs.addTab(general_view.build(self.model),   "General")
        tabs.addTab(stats_view.build(self.model),     "Stats")
        tabs.addTab(visual_view.build(self.model),    "Visual")
        tabs.addTab(skills_view.build(self.model),    "Skills")
        tabs.addTab(inventory_view.build(self.model), "Inventory")

        viewport = viewport_view.build(self.model)
        preview = CodePreviewPane(self.model)

        right_split = QSplitter(Qt.Orientation.Vertical)
        right_split.addWidget(viewport)
        right_split.addWidget(preview)
        right_split.setStretchFactor(0, 3)
        right_split.setStretchFactor(1, 2)
        right_split.setChildrenCollapsible(False)

        main_split = QSplitter(Qt.Orientation.Horizontal)
        main_split.addWidget(tabs)
        main_split.addWidget(right_split)
        main_split.setStretchFactor(0, 2)
        main_split.setStretchFactor(1, 3)
        main_split.setChildrenCollapsible(False)

        self.setCentralWidget(main_split)
        self._main_split = main_split
        self._right_split = right_split

    def _build_menu(self) -> None:
        mb = self.menuBar()

        file_menu = mb.addMenu("&File")

        save_act = QAction("&Save Daedalus File", self)
        save_act.setShortcut(QKeySequence.StandardKey.Save)
        save_act.triggered.connect(self._save_file)
        file_menu.addAction(save_act)

        file_menu.addSeparator()
        quit_act = QAction("&Quit", self)
        quit_act.setShortcut(QKeySequence.StandardKey.Quit)
        quit_act.triggered.connect(self.close)
        file_menu.addAction(quit_act)

        view_menu = mb.addMenu("&View")
        reset_layout = QAction("&Reset Layout", self)
        reset_layout.triggered.connect(self._reset_layout)
        view_menu.addAction(reset_layout)

    def _wire_status(self) -> None:
        bar = self.statusBar()
        bar.showMessage("Ready")
        self.model.changed.connect(
            lambda _attr: bar.showMessage("Modified", 3000)
        )

    # ----------------------------------------------------------------- actions

    def _save_file(self) -> None:
        path = getFileName(self.model.npc)
        generateFile(
            self.model.npc,
            lambda: self.statusBar().showMessage(f"Saved  ·  {path}", 6000),
        )

    def _reset_layout(self) -> None:
        self._settings.remove("geometry")
        self._settings.remove("main_split")
        self._settings.remove("right_split")
        self.statusBar().showMessage("Layout reset on next launch.", 4000)

    # ----------------------------------------------------------- persistence

    def _restore_geometry(self) -> None:
        geom = self._settings.value("geometry")
        if isinstance(geom, QByteArray):
            self.restoreGeometry(geom)
        main_s = self._settings.value("main_split")
        if isinstance(main_s, QByteArray):
            self._main_split.restoreState(main_s)
        right_s = self._settings.value("right_split")
        if isinstance(right_s, QByteArray):
            self._right_split.restoreState(right_s)

    def closeEvent(self, event) -> None:
        self._settings.setValue("geometry", self.saveGeometry())
        self._settings.setValue("main_split", self._main_split.saveState())
        self._settings.setValue("right_split", self._right_split.saveState())
        super().closeEvent(event)


def launch(npc) -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName(_APP)
    app.setOrganizationName(_ORG)
    theme.apply(app)
    window = NewMainWindow(npc)
    window.show()
    sys.exit(app.exec())
