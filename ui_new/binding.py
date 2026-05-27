"""Helpers that initialize widgets from model values.

Views write user input back through `model.set(...)`. To round-trip, they
also need to pre-select / pre-fill widgets to match the current NPC when a
view is built. These helpers do that without firing user-input signals,
either by being called before signals are connected or by guarding with
blockSignals on combos.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QTreeWidget, QTreeWidgetItem


def select_combo_by_value(combo: QComboBox, mapping: dict, value) -> None:
    """Set combo to the key whose mapped value equals `value`. No-op if absent."""
    if value is None:
        return
    for key, v in mapping.items():
        if v == value:
            combo.setCurrentText(key)
            return


def select_int_combo(combo: QComboBox, value) -> None:
    """Set combo (whose items are str(int)) to `value` if numeric."""
    if value is None:
        return
    try:
        text = str(int(value))
    except (TypeError, ValueError):
        return
    if combo.findText(text) >= 0:
        combo.setCurrentText(text)


def select_tree_by_userrole(tree: QTreeWidget, value) -> None:
    """Select the first leaf whose UserRole data equals `value`. Expand its parent."""
    if value is None:
        return
    root = tree.invisibleRootItem()
    for i in range(root.childCount()):
        cat = root.child(i)
        for j in range(cat.childCount()):
            leaf = cat.child(j)
            if leaf.data(0, Qt.ItemDataRole.UserRole) == value:
                cat.setExpanded(True)
                tree.setCurrentItem(leaf)
                return


def key_for_value(mapping: dict, value):
    """Reverse lookup; returns first key matching value, or None."""
    for k, v in mapping.items():
        if v == value:
            return k
    return None
