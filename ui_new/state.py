from PySide6.QtCore import QObject, Signal

_MISSING = object()


class NpcModel(QObject):
    """Reactive wrapper around the plain Npc data class.

    Emits `changed(attr_name)` whenever a field is mutated, so views and the
    code preview can update without manual callbacks.
    """

    changed = Signal(str)

    def __init__(self, npc):
        super().__init__()
        self._npc = npc

    @property
    def npc(self):
        return self._npc

    def get(self, attr):
        return getattr(self._npc, attr)

    def set(self, attr: str, value) -> None:
        current = getattr(self._npc, attr, _MISSING)
        if current is not _MISSING and current == value:
            return
        setattr(self._npc, attr, value)
        self.changed.emit(attr)

    def add_inventory(self, item_key: str, quantity: int) -> None:
        for entry in self._npc.inv_items:
            if entry["item"] == item_key:
                entry["quantity"] += quantity
                self.changed.emit("inv_items")
                return
        self._npc.inv_items.append({"item": item_key, "quantity": quantity})
        self.changed.emit("inv_items")

    def remove_inventory(self, index: int) -> None:
        if 0 <= index < len(self._npc.inv_items):
            self._npc.inv_items.pop(index)
            self.changed.emit("inv_items")
