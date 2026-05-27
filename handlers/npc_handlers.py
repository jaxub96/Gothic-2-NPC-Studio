# handlers/npc_handlers.py
#
# Changes from tkinter version:
#   - setTalent* methods now accept a plain str value directly instead of a
#     tk.StringVar. The tab builder passes the current combo/radio value.

import random
from constants.mappings import talentLevelMap


class NpcHandlers:
    def __init__(self, npc, refresh: callable):
        self.npc = npc
        self.refresh = refresh

    def assignAttribute(self, attr: str, var: callable, cast: callable = str) -> None:
        setattr(self.npc, attr, cast(var()))
        self.refresh()

    def assignAttributeFromScale(self, attr: str, value) -> None:
        setattr(self.npc, attr, int(float(value)))
        self.refresh()

    def validateID(self, value: str) -> bool:
        if value == "":
            return True
        return value.isdigit() and len(value) <= 3

    # --- Talent setters now receive a plain str, not a tk.StringVar ---

    def setTalent1H(self, value: str) -> None:
        self.npc.t1h = talentLevelMap[value]
        self.refresh()

    def setTalent2H(self, value: str) -> None:
        self.npc.t2h = talentLevelMap[value]
        self.refresh()

    def setTalentBow(self, value: str) -> None:
        self.npc.bow = talentLevelMap[value]
        self.refresh()

    def setTalentCBow(self, value: str) -> None:
        self.npc.cbow = talentLevelMap[value]
        self.refresh()

    def randomizeInventoryQty(self) -> None:
        self.npc.inv_qty = random.randint(1, 20)
        self.refresh()
        # TODO: eventually we want to add actual items, not just random qty, so this method will need to be reworked. For now it just randomizes the qty of a single placeholder item.
    def addInventoryItem(self, item_index: str, quantity: int) -> None:
        print(f"Trying to add: '{item_index}' type={type(item_index)}")
        for entry in self.npc.inv_items:
            print(f"Existing: '{entry['item']}' type={type(entry['item'])}")
            if entry["item"] == item_index:
                entry["quantity"] += quantity
                self.refresh()
                return
        self.npc.inv_items.append({"item": item_index, "quantity": quantity})
        self.refresh()