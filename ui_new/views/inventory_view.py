from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
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
from ui_new.binding import select_tree_by_userrole
from ui_new.theme import pixel_font
from ui_new.tokens import CHROME, SPACE
from ui_new.widgets.form import FormSection


_ITEM_KEY_ROLE = Qt.ItemDataRole.UserRole + 1


def _build_armor_tree() -> QTreeWidget:
    tree = QTreeWidget()
    tree.setHeaderHidden(True)
    tree.setIndentation(CHROME["tree_indent"])
    bold = pixel_font("body", "list_item")
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


def _build_item_completer(line_edit: QLineEdit) -> QCompleter:
    """Completer whose visible text is 'key — name' but whose accepted value
    carries the item key in UserRole+1 so we never have to re-parse strings."""
    model = QStandardItemModel(line_edit)
    for key, name in all_items.items():
        item = QStandardItem(f"{key} — {name}")
        item.setData(key, _ITEM_KEY_ROLE)
        model.appendRow(item)

    completer = QCompleter(model, line_edit)
    completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    completer.setFilterMode(Qt.MatchFlag.MatchContains)
    line_edit.setCompleter(completer)
    return completer


def _resolve_item_key(text: str) -> str | None:
    """Map either a raw key or a 'key — name' completion display to a key."""
    text = text.strip()
    if not text:
        return None
    if text in all_items:
        return text
    head = text.split(" ", 1)[0]
    return head if head in all_items else None


def build(model) -> QWidget:
    root = QWidget()
    layout = QVBoxLayout(root)
    layout.setContentsMargins(SPACE["xl"], SPACE["sm"], SPACE["xl"], SPACE["xl"])
    layout.setSpacing(0)

    splitter = QSplitter(Qt.Orientation.Vertical)
    splitter.setChildrenCollapsible(False)

    # --- Armor -------------------------------------------------------------
    armor_section = FormSection("Armor")
    tree = _build_armor_tree()
    select_tree_by_userrole(tree, model.get("armor"))

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

    search = QLineEdit()
    search.setPlaceholderText("Search…")
    _build_item_completer(search)

    qty = QSpinBox()
    qty.setRange(1, 99)
    qty.setValue(1)
    qty.setFixedWidth(CHROME["qty_field_w"])

    add_btn = QPushButton("Add")
    add_btn.setProperty("role", "primary")

    search_row = QHBoxLayout()
    search_row.setSpacing(SPACE["md"])
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
        key = _resolve_item_key(search.text())
        if key is None:
            return
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
