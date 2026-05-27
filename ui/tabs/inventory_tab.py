# ui/tabs/inventory_tab.py
"""Inventory tab UI builder for the NPC creator."""
# region import
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QLineEdit,
    QCompleter,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
)
from constants.colors import (
    ACCENT_PRIMARY,
    BG_LIGHT,
    BG_MEDIUM,
    FONT_PRIMARY,
    TEXT_PRIMARY,
    WARNING_COLOR,
    SUCCESS_COLOR,
)
from data.armors import armorData
from data.items import all_items
from ui.widgets import create_styled_button, create_styled_spinbox, create_styled_label
# endregion


def build(parent: QWidget, npc, handlers) -> None:
    """Build the inventory tab UI inside the provided parent widget."""
    # MAIN LAYOUT
    layout = parent.layout()
    layout.setSpacing(5)
    layout.setContentsMargins(0, 0, 0, 0)
    # region DEFINE EVENTS
    def on_add_clicked() -> None:
        '''Add the selected item and quantity to the NPC's inventory.'''
        text = item_search.text()
        if not text:
            return

        item_key = str(text.split(" - ")[0])
        item_name = str(text.split(" - ")[1]).strip("()")
        handlers.addInventoryItem(item_key, item_qty.value())
        inventory_list.addItem(f"{item_name} \u00d7 {item_qty.value()}")
        item_search.clear()
        refresh_inventory_list()  # add this to update the list after adding an item

    def refresh_inventory_list() -> None:
        '''Refresh the inventory list widget to reflect the current state of npc.inv_items.'''
        inventory_list.clear()
        for index, entry in enumerate(npc.inv_items, start=1):
            inventory_list.addItem(f" - {entry['item']} ({entry['quantity']})")

    def on_remove_clicked() -> None:
        '''Remove the selected item from the NPC's inventory.'''
        selected_row = inventory_list.currentRow()
        if selected_row >= 0:
            npc.inv_items.pop(selected_row)
            handlers.refresh()
            refresh_inventory_list()

    def on_armor_selected() -> None:
        '''Handle selection of an armor item from the tree. 
        If a category is clicked, toggle expand/collapse. 
        If an item is clicked, assign it to npc.armor.'''
        selected_items = tree.selectedItems()
        if not selected_items:
            return

        selected_item = selected_items[0]
        code = selected_item.data(0, Qt.ItemDataRole.UserRole)
        if code is None:
            # Clicked a category — toggle expand/collapse, don't assign
            selected_item.setExpanded(not selected_item.isExpanded())
            return

        npc.armor = code
        handlers.refresh()

        parent_item = selected_item.parent()
        root = tree.invisibleRootItem()
        for i in range(root.childCount()):
            category_item = root.child(i)
            category_item.setExpanded(category_item is parent_item)
    # endregion
    
    item_choices = [f"{key} - ({value})" for key, value in all_items.items()]
    completer = QCompleter(item_choices)
    completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    completer.setFilterMode(Qt.MatchFlag.MatchContains)  # matches anywhere in string, not just start

    item_qty = create_styled_spinbox(parent, min_val=1, max_val=99, default=1)
    item_search = QLineEdit(parent)
    item_search.setPlaceholderText("Search item...")
    item_search.setCompleter(completer)
    item_search.setStyleSheet(
        f"""
        QLineEdit {{
            background: {BG_LIGHT};
            color: {TEXT_PRIMARY};
            border: none;
            border-radius: 3px;
            padding: 6px 8px;
            font-family: {FONT_PRIMARY[0]};
            font-size: {FONT_PRIMARY[1]}pt;
        }}
        """
    )

    
    # region ARMOR TREE
    tree = QTreeWidget(parent)
    tree.setHeaderHidden(True)
    tree.setColumnCount(2)
    tree.setStyleSheet(f"""
        QTreeWidget {{
            background: {BG_LIGHT};
            color: {TEXT_PRIMARY};
            border: none;
            font-family: {FONT_PRIMARY[0]};
            font-size: {FONT_PRIMARY[1]}pt;
        }}
        QTreeWidget::item:selected {{
            background: {ACCENT_PRIMARY};
            color: {TEXT_PRIMARY};
        }}
        QTreeWidget::item:hover {{
            background: {BG_MEDIUM};
        }}
        QScrollBar:vertical {{
            background: {BG_MEDIUM};
            width: 8px;
            border: none;
        }}
        QScrollBar::handle:vertical {{
            background: {ACCENT_PRIMARY};
            border-radius: 4px;
        }}
    """)
    # endregion
    bold_font = QFont(FONT_PRIMARY[0], FONT_PRIMARY[1], QFont.Weight.Bold)

    for category, items in armorData.items():
        category_item = QTreeWidgetItem(tree, [category])
        category_item.setFont(0, bold_font)
        category_item.setData(0, Qt.ItemDataRole.UserRole, None)   # not selectable as armor
        for entry in items:
            code, name = entry.split(";", 1)
            child_item = QTreeWidgetItem(category_item, [name.strip()])
            child_item.setData(0, Qt.ItemDataRole.UserRole, code.strip())

    # region CONNECT EVENTS
    tree.itemSelectionChanged.connect(on_armor_selected)
    add_button = create_styled_button(
        parent,
        "Add Item",
        None,
        bg_color=SUCCESS_COLOR,
    )
    add_button.clicked.connect(on_add_clicked)
    # endregion

    # Horizontal layout for search and add button
    search_row = QHBoxLayout()
    search_row.addWidget(item_search)
    search_row.addWidget(item_qty)
    search_row.addWidget(add_button)

    # # --- Randomize button ---
    # randomize_button = create_styled_button(
    #     parent,
    #     "Randomize Inventory",
    #     handlers.randomizeInventoryQty,
    #     bg_color=SUCCESS_COLOR,
    # )

    inventory_list = QListWidget(parent)
    inventory_list.setStyleSheet(f"""
        QListWidget {{
            background: {BG_LIGHT};
            color: {TEXT_PRIMARY};
            border: none;
            border-radius: 3px;
            font-family: {FONT_PRIMARY[0]};
            font-size: {FONT_PRIMARY[1]}pt;
        }}
        QListWidget::item:selected {{
            background: {ACCENT_PRIMARY};
            color: {TEXT_PRIMARY};
        }}
        QListWidget::item:hover {{
            background: {BG_MEDIUM};
        }}
    """)

    remove_button = create_styled_button(parent, "Remove Selected", None, bg_color=WARNING_COLOR)
    remove_button.clicked.connect(on_remove_clicked)

    # Print
    layout.addWidget(create_styled_label(parent, "Armor", font_size=11, bold=True))
    layout.addWidget(tree, stretch=1)
    layout.addWidget(create_styled_label(parent, "Items", font_size=11, bold=True))
    #layout.addWidget(randomize_button)
    layout.addLayout(search_row)
    layout.addWidget(remove_button)
    layout.addWidget(inventory_list, stretch=1)

