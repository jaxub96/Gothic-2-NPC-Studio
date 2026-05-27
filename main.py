# main.py

from models.Npc import Npc
from ui.app import launch

if __name__ == "__main__":
    npc = Npc()
    launch(npc)