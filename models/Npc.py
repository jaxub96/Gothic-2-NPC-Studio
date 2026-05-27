# models/Npc.py
# No changes required — already pure Python with no tkinter dependency.

class Npc:
    """Main NPC class containing all variables for a Gothic 1 NPC"""

    def __init__(self):

        # ---------- General ----------
        self.name = ""
        self.id = "001"
        self.guild = None
        self.level = 0
        self.type = "npctype_main"

        # ---------- Attributes ----------
        self.str = 5
        self.dex = 5
        self.mana = 5
        self.hp = 10

        # ---------- Visual ----------
        self.voice = 0
        self.fatness = 0
        
        self.immortal = 0
        self.friend = 0
        self.head = None
        self.walking = None
        self.armor = "NO_ARMOR"

        self.body_tex = 1
        self.face = "FACE_N_Player"
        self.teeth_tex = 1
        self.skin_color = 0
        # ---------- Fight ----------
        self.fight = None

        # ---------- Talents ----------
        self.t1h = 0
        self.t2h = 0
        self.bow = 0
        self.cbow = 0
        self.magic = 0

        # ---------- Inventory ----------
        self.inv_qty = 1
        self.inv_items = []
