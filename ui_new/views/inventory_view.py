from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QCompleter,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QPushButton,
    QSpinBox,
    QSplitter,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from data.armors import armorData
from data.items import all_items
from ui_new.widgets.form import FormSection


def _build_armor_tree() -> QTreeWidget:
    tree = QTreeWidget()
    tree.setHeaderHidden(True)
    tree.setIndentation(14)
    bold = QFont()
    bold.setBold(True)

    for category, items in armorData.items():
        cat_item = QTreeWidgetItem(tree, [category])
        cat_item.setFont(0, bold)
        cat_item.setData(0, Qt.ItemDataRole.UserRole, None)
        for entry in items:
            code, name = entry.split(";", 1)
            child = QTreeWidgetItem(cat_item, [name.strip()])
            child.setData(0, Qt.ItemDataRole.UserRole, code.strip())
    return tree


def build(model) -> QWidget:
    root = QWidget()
    layout = QVBoxLayout(root)
    layout.setContentsMargins(28, 8, 28, 28)
    layout.setSpacing(0)

    splitter = QSplitter(Qt.Orientation.Vertical)
    splitter.setChildrenCollapsible(False)
    splitter.setHandleWidth(1)

    # --- Armor -------------------------------------------------------------
    armor_section = FormSection("Armor")
    tree = _build_armor_tree()

    def on_armor_select() -> None:
        sel = tree.selectedItems()
        if not sel:
            return
        item = sel[0]
        code = item.data(0, Qt.ItemDataRole.UserRole)
        if code is None:
            item.setExpanded(not item.isExpanded())
            return
        model.set("armor", code)
        root_item = tree.invisibleRootItem()
        for i in range(root_item.childCount()):
            cat = root_item.child(i)
            cat.setExpanded(cat is item.parent())

    tree.itemSelectionChanged.connect(on_armor_select)
    armor_section.addWidget(tree)
    splitter.addWidget(armor_section)

    # --- Items -------------------------------------------------------------
    items_section = FormSection("Items")

    completer = QCompleter([f"{k} — {v}" for k, v in all_items.items()])
    completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    completer.setFilterMode(Qt.MatchFlag.MatchContains)

    search = QLineEdit()
    search.setPlaceholderText("Search…")
    search.setCompleter(completer)

    qty = QSpinBox()
    qty.setRange(1, 99)
    qty.setValue(1)
    qty.setFixedWidth(70)

    add_btn = QPushButton("Add")
    add_btn.setProperty("role", "primary")

    search_row = QHBoxLayout()
    search_row.setSpacing(10)
    search_row.addWidget(search, stretch=1)
    search_row.addWidget(qty)
    search_row.addWidget(add_btn)
    items_section.addLayout(search_row)

    inv_list = QListWidget()
    items_section.addWidget(inv_list)

    remove_btn = QPushButton("Remove")
    remove_btn.setProperty("role", "danger")
    actions_row = QHBoxLayout()
    actions_row.addStretch()
    actions_row.addWidget(remove_btn)
    items_section.addLayout(actions_row)

    splitter.addWidget(items_section)
    splitter.setStretchFactor(0, 2)
    splitter.setStretchFactor(1, 3)
    layout.addWidget(splitter)

    def refresh_list() -> None:
        inv_list.clear()
        for entry in model.get("inv_items"):
            inv_list.addItem(f"{entry['item']}    ×{entry['quantity']}")

    def on_add() -> None:
        text = search.text().strip()
        if not text or " — " not in text:
            return
        key = text.split(" — ")[0].strip()
        model.add_inventory(key, qty.value())
        search.clear()
        qty.setValue(1)

    def on_remove() -> None:
        row = inv_list.currentRow()
        if row >= 0:
            model.remove_inventory(row)

    add_btn.clicked.connect(on_add)
    remove_btn.clicked.connect(on_remove)
    search.returnPressed.connect(on_add)
    model.changed.connect(lambda attr: refresh_list() if attr == "inv_items" else None)
    refresh_list()

    return root
