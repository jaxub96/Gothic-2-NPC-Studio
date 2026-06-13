# main.py

import os
import sys

from models.Npc import Npc


def _use_new_ui() -> bool:
    if "--new" in sys.argv:
        sys.argv.remove("--new")
        return True
    return os.environ.get("GOTHIC_NEW_UI", "0") not in ("0", "", "false", "False")


if __name__ == "__main__":
    npc = Npc()
    os.environ["QT_API"] = "pyside6"
    from ui.app_new import launch

    launch(npc)
