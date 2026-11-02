"""Embedded head preview — PyVista port of the TextureModel three.js viewer.

Feature parity with `TextureModel/static/viewer.js`:
  - head mesh follows the NPC `head` attribute (reactive, via model.changed)
  - bundled TGA skin texture applied to the head
  - wireframe / grid / texture toggles, reset view
  - vertex + triangle readout

Assets live in `ui_new/assets/models/*.glb` and `ui_new/assets/textures/*.tga`.
Heads without a bundled GLB show an empty state instead of a mesh.
"""

import warnings
from pathlib import Path

import numpy as np
import pyvista as pv
from PIL import Image
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from pyvistaqt import QtInteractor

from ui_new.tokens import CHROME, COLORS, FONT_FAMILY, SIZES, SPACE

_ASSETS = Path(__file__).resolve().parents[1] / "assets"
_MODELS_DIR = Path(
    r"C:\Users\jkjw\Documents\Python Projects\Gothic-2-NPC-Studio\ui_new\assets\models"
)
_TEXTURES_DIR = Path(
    r"C:\Users\jkjw\OneDrive - Demant\Documents\BLENDER PROJECTS\g2mdk-asc_armor\_work\data\Anims\asc_bodies\armor\head_text"
)

# three.js parity: GridHelper(20, 40) → fixed divisions, span scaled to mesh;
# fitCamera() → dist = radius * 4, eye lifted 0.2 * dist above center.
# The converted Gothic GLBs keep ZenGin axes (+Z up, face +X); meshes are
# rotated -90° about X on load so the viewer works in conventional Y-up.
_GRID_DIVISIONS = 40
_GRID_SPAN = 4.0
_FIT_DIST = 4.0
_FIT_LIFT = 0.2
_UP = (0.0, 1.0, 0.0)
_ZUP_TO_YUP_DEG = -90.0

_MODEL_ACTOR = "model"
_GRID_ACTOR = "grid"


def _read_head(path: Path) -> pv.PolyData:
    mesh = pv.get_reader(str(path)).read()
    if isinstance(mesh, pv.MultiBlock):
        mesh = mesh.combine()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        surf = mesh.extract_surface()
    if "TEXCOORD_0" in surf.point_data:
        surf.active_texture_coordinates = surf.point_data["TEXCOORD_0"]
    surf.rotate_x(_ZUP_TO_YUP_DEG, inplace=True)
    surf.rotate_x(90.0, inplace=True)
    surf.rotate_y(90.0, inplace=True)
    return surf


def _load_texture(path: Path) -> pv.Texture:
    img = Image.open(path).convert("RGB")
    # glTF UV origin is top-left; VTK samples bottom-left — flip once on load.
    img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return pv.Texture(np.array(img))


def _grid_polydata(
    center_x: float, center_z: float, y: float, size: float
) -> pv.PolyData:
    """Line grid in the XZ ground plane (Y-up) — equivalent of three.js GridHelper."""
    half = size / 2.0
    ticks = np.linspace(-half, half, _GRID_DIVISIONS + 1)
    points = []
    for t in ticks:
        points.append((center_x + t, y, center_z - half))
        points.append((center_x + t, y, center_z + half))
        points.append((center_x - half, y, center_z + t))
        points.append((center_x + half, y, center_z + t))
    pts = np.array(points)
    lines = np.hstack([[2, i, i + 1] for i in range(0, len(pts), 2)])
    return pv.PolyData(pts, lines=lines)


class HeadViewer(QWidget):
    """3D head preview bound to an NpcModel."""

    def __init__(self, model, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._model = model
        self._mesh: pv.PolyData | None = None
        self._texture = self._find_texture(model.get("face"))
        self.setMinimumHeight(CHROME["head_viewer_min_h"])

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._plotter = QtInteractor(self)
        self._plotter.set_background(COLORS["page"])
        layout.addWidget(self._plotter.interactor, stretch=1)

        self._status = QLabel("")
        self._status.setStyleSheet(
            f"color: {COLORS['gold']};"
            f"padding: {SPACE['sm']}px {SPACE['lg']}px;"
            f"font-family: '{FONT_FAMILY['display']}', serif;"
            f"font-size: {SIZES['viewport']}px;"
            f"letter-spacing: {CHROME['track_chrome']}px;"
        )
        layout.addWidget(self._status)

        self._btn_reset = QPushButton("Reset View")
        self._btn_wire = QPushButton("Wireframe")
        self._btn_wire.setCheckable(True)
        self._btn_grid = QPushButton("Grid")
        self._btn_grid.setCheckable(True)
        self._btn_grid.setChecked(True)
        self._btn_tex = QPushButton("Texture")
        self._btn_tex.setCheckable(True)
        self._btn_tex.setChecked(self._texture is not None)
        self._btn_tex.setEnabled(self._texture is not None)

        row = QHBoxLayout()
        row.setContentsMargins(SPACE["lg"], 0, SPACE["lg"], SPACE["md"])
        row.setSpacing(SPACE["sm"])
        row.addWidget(self._btn_reset)
        row.addWidget(self._btn_wire)
        row.addWidget(self._btn_grid)
        row.addWidget(self._btn_tex)
        row.addStretch()
        layout.addLayout(row)

        self._btn_reset.clicked.connect(self._fit_camera)
        self._btn_wire.toggled.connect(self._on_wireframe)
        self._btn_grid.toggled.connect(self._on_grid)
        self._btn_tex.toggled.connect(lambda _on: self._add_model_actor())

        model.changed.connect(self._on_model_changed)
        self._load_head(model.get("head") or _DEFAULT_HEAD)

    # ------------------------------------------------------------- reactive
    def _on_model_changed(self, attr: str) -> None:
        if attr == "head":
            self._load_head(self._model.get("head"))
        elif attr == "face":
            self._on_face_changed(self._model.get("face"))

    def _on_face_changed(self, face_code) -> None:
        self._texture = self._find_texture(face_code)
        self._btn_tex.setEnabled(self._texture is not None)
        if self._texture is None:
            self._btn_tex.setChecked(False)
        elif not self._btn_tex.isChecked():
            self._btn_tex.setChecked(True)
        self._add_model_actor()

    # -------------------------------------------------------------- loading

    @staticmethod
    def _find_texture(face_code=None) -> pv.Texture | None:
        """Resolve the head texture for the given Face index (1-based).

        Matches Hum_Head_V{face_code}_C*.tga; falls back to any Hum_Head_*
        texture, then to the first TGA found, if no exact face match exists.
        """
        candidates = (
            sorted(_TEXTURES_DIR.glob("*.tga")) if _TEXTURES_DIR.is_dir() else []
        )
        if not candidates:
            return None

        pick = None
        if face_code is not None:
            prefix = f"hum_head_v{face_code}_"
            matches = [c for c in candidates if c.name.lower().startswith(prefix)]
            if matches:
                pick = matches[0]

        if pick is None:
            heads = [c for c in candidates if c.name.lower().startswith("hum_head")]
            pick = heads[0] if heads else candidates[0]

        try:
            return _load_texture(pick)
        except Exception:
            return None

    def _load_head(self, head_code) -> None:
        self._plotter.remove_actor(_MODEL_ACTOR)
        self._plotter.remove_actor(_GRID_ACTOR)
        self._mesh = None

        if not head_code:
            self._status.setText("No head selected")
            self._plotter.render()
            return

        path = _MODELS_DIR / f"{head_code}.glb"
        if not path.exists():
            self._status.setText(f"No mesh for {head_code}")
            self._plotter.render()
            return

        try:
            self._mesh = _read_head(path)
        except Exception as e:
            self._status.setText(f"Load failed — {e}")
            self._plotter.render()
            return

        self._add_model_actor()
        self._rebuild_grid()
        self._fit_camera()
        tris = self._mesh.n_cells
        verts = self._mesh.n_points
        self._status.setText(f"{head_code}  ·  {verts} verts  ·  {tris} tris")

    # --------------------------------------------------------------- actors

    def _add_model_actor(self) -> None:
        if self._mesh is None:
            return
        kwargs = {"name": _MODEL_ACTOR, "smooth_shading": True}
        textured = (
            self._btn_tex.isChecked()
            and self._texture is not None
            and self._mesh.active_texture_coordinates is not None
        )
        if textured:
            kwargs["texture"] = self._texture
        else:
            kwargs["color"] = COLORS["gold"]
        self._plotter.add_mesh(self._mesh, **kwargs)
        if self._btn_wire.isChecked():
            self._on_wireframe(True)
        self._plotter.render()

    def _rebuild_grid(self) -> None:
        if self._mesh is None:
            return
        radius = max(self._mesh.length / 2.0, 1e-3)
        cx, _cy, cz = self._mesh.center
        y_min = self._mesh.bounds[2]
        grid = _grid_polydata(cx, cz, y_min, radius * _GRID_SPAN)
        self._plotter.add_mesh(
            grid,
            color=COLORS["edge"],
            name=_GRID_ACTOR,
            lighting=False,
            pickable=False,
        )
        actor = self._plotter.renderer.actors.get(_GRID_ACTOR)
        if actor is not None:
            actor.SetVisibility(self._btn_grid.isChecked())

    # -------------------------------------------------------------- toggles

    def _on_wireframe(self, checked: bool) -> None:
        actor = self._plotter.renderer.actors.get(_MODEL_ACTOR)
        if actor is None:
            return
        prop = actor.GetProperty()
        if checked:
            prop.SetRepresentationToWireframe()
        else:
            prop.SetRepresentationToSurface()
        self._plotter.render()

    def _on_grid(self, checked: bool) -> None:
        actor = self._plotter.renderer.actors.get(_GRID_ACTOR)
        if actor is None:
            return
        actor.SetVisibility(checked)
        self._plotter.render()

    # --------------------------------------------------------------- camera

    def _fit_camera(self) -> None:
        if self._mesh is None:
            self._plotter.reset_camera()
            return
        center = np.array(self._mesh.center)
        radius = max(self._mesh.length / 2.0, 1e-3)
        dist = radius * _FIT_DIST
        # in front of the face (+X), lifted along Y
        eye = center + np.array([dist, dist * _FIT_LIFT, 0.0])
        self._plotter.camera_position = [tuple(eye), tuple(center), _UP]
        self._plotter.render()
