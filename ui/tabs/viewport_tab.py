from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog, QLabel,
)
from pyvistaqt import QtInteractor
import pyvista as pv

from constants.colors import TEXT_PRIMARY, BG_DARK


def build(parent: QWidget, npc, handlers) -> None:
    layout: QVBoxLayout = parent.layout()
    layout.setSpacing(6)

    plotter = QtInteractor(parent)
    plotter.set_background(BG_DARK)
    plotter.add_axes()

    default_mesh = pv.Sphere(radius=1.0)
    plotter.add_mesh(default_mesh, color="#bbcde5", smooth_shading=True, name="model")
    plotter.reset_camera()

    layout.addWidget(plotter.interactor, stretch=1)

    status = QLabel("Default sphere. Load an OBJ/STL/PLY/glTF to preview NPC mesh.")
    status.setStyleSheet(f"color: {TEXT_PRIMARY}; padding: 4px;")
    layout.addWidget(status)

    btn_row = QWidget()
    btn_layout = QHBoxLayout(btn_row)
    btn_layout.setContentsMargins(0, 0, 0, 0)

    btn_load = QPushButton("Load Mesh…")
    btn_reset = QPushButton("Reset Camera")
    btn_wire = QPushButton("Toggle Wireframe")
    btn_layout.addWidget(btn_load)
    btn_layout.addWidget(btn_reset)
    btn_layout.addWidget(btn_wire)
    layout.addWidget(btn_row)

    state = {"wireframe": False}

    def load_mesh():
        path, _ = QFileDialog.getOpenFileName(
            parent, "Load mesh",
            str(Path.home()),
            "Meshes (*.obj *.stl *.ply *.gltf *.glb *.vtk *.vtp);;All files (*)",
        )
        if not path:
            return
        try:
            mesh = pv.read(path)
        except Exception as e:
            status.setText(f"Load failed: {e}")
            return
        plotter.remove_actor("model")
        plotter.add_mesh(
            mesh,
            color="#bbcde5",
            smooth_shading=True,
            style="wireframe" if state["wireframe"] else "surface",
            name="model",
        )
        plotter.reset_camera()
        status.setText(f"Loaded: {Path(path).name}  ({mesh.n_points} pts / {mesh.n_cells} cells)")

    def toggle_wireframe():
        state["wireframe"] = not state["wireframe"]
        actor = plotter.renderer.actors.get("model")
        if actor is None:
            return
        prop = actor.GetProperty()
        prop.SetRepresentationToWireframe() if state["wireframe"] else prop.SetRepresentationToSurface()
        plotter.render()

    btn_load.clicked.connect(load_mesh)
    btn_reset.clicked.connect(plotter.reset_camera)
    btn_wire.clicked.connect(toggle_wireframe)

    parent._plotter = plotter
