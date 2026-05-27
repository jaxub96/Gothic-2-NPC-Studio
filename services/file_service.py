# services/file_service.py
# No changes required — pure logic, no tkinter dependency.

import os
from pathlib import Path
from services.output_builder import buildOutput

OUTPUT_FOLDER ='output'
def createOutputFolder() -> None:
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def getFileName(npc) -> str:
    safe_name = npc.name.strip().replace(" ", "_")
    if not safe_name:
        safe_name = "NPC"
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    except NameError:
        base_dir = os.getcwd()
    return os.path.join(base_dir, OUTPUT_FOLDER, f"MOD_{npc.id}_{safe_name}.d")


def generateFile(npc, on_success: callable) -> None:
    createOutputFolder()
    filename = getFileName(npc)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(buildOutput(npc))
    on_success()
