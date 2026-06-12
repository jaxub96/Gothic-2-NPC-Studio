from PySide6.QtWidgets import QVBoxLayout, QWidget

from ui_new.widgets.head_viewer import HeadViewer


def build(model) -> QWidget:
    root = QWidget()
    layout = QVBoxLayout(root)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    viewer = HeadViewer(model, root)
    layout.addWidget(viewer, stretch=1)

    root._viewer = viewer
    return root
