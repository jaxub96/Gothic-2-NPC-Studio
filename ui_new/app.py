import sys

from PySide6.QtCore import QByteArray, QSettings, Qt, QTimer
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QSplitter,
    QTabWidget,
)

from services.file_service import generateFile, getFileName
from ui_new import theme
from ui_new.state import NpcModel
from ui_new.tokens import WINDOW
from ui_new.views import (
    general_view,
    inventory_view,
    skills_view,
    stats_view,
    viewport_view,
    visual_view,
)
from ui_new.widgets.preview import CodePreviewPane


_ORG = WINDOW["org"]
_APP = WINDOW["app"]

_STATUS_DEBOUNCE_MS = 400

_IMPORTABLE_ATTRS = (
    "name",
    "id",
    "guild",
    "level",
    "type",
    "str",
    "dex",
    "mana",
    "hp",
    "voice",
    "fatness",
    "immortal",
    "friend",
    "head",
    "walking",
    "armor",
    "body_tex",
    "face",
    "teeth_tex",
    "skin_color",
    "fight",
    "t1h",
    "t2h",
    "bow",
    "cbow",
    "magic",
    "inv_qty",
)


class NewMainWindow(QMainWindow):
    def __init__(self, npc) -> None:
        super().__init__()
        self.model = NpcModel(npc)
        self.setWindowTitle(WINDOW["title"])
        self.resize(*WINDOW["size"])
        self.setMinimumSize(*WINDOW["min"])

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

        open_act = QAction("&Open Daedalus File…", self)
        open_act.setShortcut(QKeySequence.StandardKey.Open)
        open_act.triggered.connect(self._open_file)
        file_menu.addAction(open_act)

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

        self._status_timer = QTimer(self)
        self._status_timer.setSingleShot(True)
        self._status_timer.setInterval(_STATUS_DEBOUNCE_MS)
        self._status_timer.timeout.connect(
            lambda: bar.showMessage("Modified", _STATUS_DEBOUNCE_MS * 4)
        )
        self.model.changed.connect(lambda _attr: self._status_timer.start())

    # ----------------------------------------------------------------- actions

    def _open_file(self) -> None:
        bar = self.statusBar()
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Daedalus File", "", "Daedalus (*.d)"
        )
        if not path:
            return
        try:
            from services.input_parser import parseInputFile
            parsed = parseInputFile(path)
        except Exception as e:
            bar.showMessage(f"Open failed — {e}", 6000)
            return

        try:
            for attr in _IMPORTABLE_ATTRS:
                self.model.set(attr, getattr(parsed, attr))
            while self.model.npc.inv_items:
                self.model.remove_inventory(0)
            for entry in parsed.inv_items:
                self.model.add_inventory(entry["item"], entry["quantity"])
        except Exception as e:
            bar.showMessage(f"Open failed — {e}", 6000)
            return

        bar.showMessage(f"Loaded  ·  {path}", 6000)

    def _save_file(self) -> None:
        bar = self.statusBar()
        try:
            path = getFileName(self.model.npc)
        except Exception as e:
            bar.showMessage(f"Save failed — {e}", 6000)
            return
        if not path:
            bar.showMessage("Save failed — no output path", 6000)
            return
        try:
            generateFile(
                self.model.npc,
                lambda: bar.showMessage(f"Saved  ·  {path}", 6000),
            )
        except Exception as e:
            bar.showMessage(f"Save failed — {e}", 6000)

    def _reset_layout(self) -> None:
        self._settings.remove("geometry")
        self._settings.remove("main_split")
        self._settings.remove("right_split")
        self.resize(*WINDOW["size"])
        self._main_split.setSizes([400, 600])
        self._right_split.setSizes([600, 400])
        self.statusBar().showMessage("Layout reset.", 3000)

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
