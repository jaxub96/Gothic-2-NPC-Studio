from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import pyvista as pv
from pyvistaqt import QtInteractor

from ui_new.tokens import CHROME, COLORS, FONT_FAMILY, SIZES, SPACE


def build(model) -> QWidget:
    root = QWidget()
    layout = QVBoxLayout(root)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    plotter = QtInteractor(root)
    plotter.set_background(COLORS["page"])
    plotter.add_axes()
    plotter.add_mesh(
        pv.Sphere(radius=1.0),
        color=COLORS["gold"],
        smooth_shading=True,
        name="model",
    )
    plotter.reset_camera()
    layout.addWidget(plotter.interactor, stretch=1)

    status = QLabel("No model loaded")
    status.setStyleSheet(
        f"color: {COLORS['gold']};"
        f"padding: {SPACE['md']}px {SPACE['lg']}px;"
        f"font-family: '{FONT_FAMILY['display']}', serif;"
        f"font-size: {SIZES['viewport']}px;"
        f"letter-spacing: {CHROME['track_chrome']}px;"
    )
    layout.addWidget(status)

    btn_load = QPushButton("Load")
    btn_load.setProperty("role", "primary")
    btn_reset = QPushButton("Reset View")
    btn_wire = QPushButton("Wireframe")
    btn_wire.setCheckable(True)

    btn_row = QHBoxLayout()
    btn_row.setContentsMargins(SPACE["lg"], 0, SPACE["lg"], SPACE["md"])
    btn_row.setSpacing(SPACE["sm"])
    btn_row.addWidget(btn_load)
    btn_row.addWidget(btn_reset)
    btn_row.addWidget(btn_wire)
    btn_row.addStretch()
    layout.addLayout(btn_row)

    def load() -> None:
        path, _ = QFileDialog.getOpenFileName(
            root, "Load mesh", str(Path.home()),
            "Meshes (*.obj *.stl *.ply *.gltf *.glb *.vtk *.vtp)",
        )
        if not path:
            return
        try:
            mesh = pv.read(path)
        except Exception as e:
            status.setText(f"Load failed — {e}")
            return
        plotter.remove_actor("model")
        plotter.add_mesh(
            mesh, color=COLORS["gold"], smooth_shading=True,
            style="wireframe" if btn_wire.isChecked() else "surface", name="model",
        )
        plotter.reset_camera()
        status.setText(f"{Path(path).name}  ·  {mesh.n_points} vertices")

    def on_wire_toggled(checked: bool) -> None:
        actor = plotter.renderer.actors.get("model")
        if actor is None:
            return
        prop = actor.GetProperty()
        if checked:
            prop.SetRepresentationToWireframe()
        else:
            prop.SetRepresentationToSurface()
        plotter.render()

    btn_load.clicked.connect(load)
    btn_reset.clicked.connect(plotter.reset_camera)
    btn_wire.toggled.connect(on_wire_toggled)

    root._plotter = plotter
    return root
