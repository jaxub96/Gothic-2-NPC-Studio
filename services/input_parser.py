# services/input_parser.py
"""
Daedalus `.d` NPC importer — reverses the format emitted by
``services.output_builder.buildOutput``.

Public API:
    parseInputString(src: str) -> Npc
    parseInputFile(path: str)  -> Npc

stdlib only.
"""

from __future__ import annotations

import re
from pathlib import Path

from models.Npc import Npc


# ---------------------------------------------------------------------------
# Regex helpers
# ---------------------------------------------------------------------------

# Common building blocks
_WS = r"[ \t]*"

# instance MOD_<id>_<name> (Npc_Default)
_RE_INSTANCE = re.compile(
    r"instance\s+MOD_([^_\s]+)_([A-Za-z0-9_]+)\s*\(\s*Npc_Default\s*\)",
    re.IGNORECASE,
)

# Simple `key = value;` (value may be quoted or a bare token / number / -1)
def _kv(key: str) -> re.Pattern:
    return re.compile(
        rf"(?<!//)\b{re.escape(key)}\b{_WS}={_WS}([^;]+?){_WS};",
    )

_RE_NAME       = re.compile(r'(?<!//)\bname\b\s*=\s*"([^"]*)"\s*;')
_RE_NPCTYPE    = _kv("npctype")
_RE_GUILD      = _kv("guild")
_RE_LEVEL      = _kv("level")
_RE_VOICE      = _kv("voice")
_RE_ID         = _kv("id")
_RE_FLAGS      = _kv("flags")
_RE_FIGHT      = _kv("fight_tactic")

# Commented attribute lines
_RE_ATR_STR  = re.compile(r"//\s*attribute\[ATR_STRENGTH\]\s*=\s*(\d+)")
_RE_ATR_DEX  = re.compile(r"//\s*attribute\[ATR_DEXTERITY\]\s*=\s*(\d+)")
_RE_ATR_MANA = re.compile(r"//\s*attribute\[ATR_MANA_MAX\]\s*=\s*(\d+)")
_RE_ATR_HP   = re.compile(r"//\s*attribute\[ATR_HITPOINTS_MAX\]\s*=\s*(\d+)")

# Commented talent lines
_RE_T1H   = re.compile(r"//\s*Npc_SetTalentSkill\s*\(\s*self\s*,\s*NPC_TALENT_1H\s*,\s*(\d+)\s*\)")
_RE_T2H   = re.compile(r"//\s*Npc_SetTalentSkill\s*\(\s*self\s*,\s*NPC_TALENT_2H\s*,\s*(\d+)\s*\)")
_RE_BOW   = re.compile(r"//\s*Npc_SetTalentSkill\s*\(\s*self\s*,\s*NPC_TALENT_BOW\s*,\s*(\d+)\s*\)")
_RE_CBOW  = re.compile(r"//\s*Npc_SetTalentSkill\s*\(\s*self\s*,\s*NPC_TALENT_CROSSBOW\s*,\s*(\d+)\s*\)")
_RE_MAGIC = re.compile(r"//\s*Npc_SetTalentSkill\s*\(\s*self\s*,\s*NPC_TALENT_MAGE\s*,\s*(\d+)\s*\)")

# Visuals
_RE_OVERLAY = re.compile(
    r'(?<!//)\bMdl_ApplyOverlayMds\b\s*\(\s*self\s*,\s*"([^"]+)"\s*\)\s*;'
)
_RE_NPCVISUAL = re.compile(
    r'(?<!//)\bMdl_SetNpcVisual\b\s*\(\s*self\s*,\s*'
    r'"([^"]+)"\s*,\s*'           # body model
    r'(-?\d+)\s*,\s*'             # body_tex
    r'(-?\d+)\s*,\s*'             # skin_color
    r'"([^"]*)"\s*,\s*'           # head
    r'([A-Za-z_][A-Za-z0-9_]*)\s*,\s*'  # face
    r'(-?\d+)\s*,\s*'             # teeth_tex
    r'([^)]+?)\s*\)\s*;'          # armor (token or -1)
)
_RE_FATNESS = re.compile(
    r'(?<!//)\bMdl_SetModelFatness\b\s*\(\s*self\s*,\s*([-\d.]+)\s*\)\s*;'
)

# Inventory
_RE_INV = re.compile(
    r'(?<!//)\bCreateInvItems\b\s*\(\s*self\s*,\s*'
    r'([A-Za-z_][A-Za-z0-9_]*)\s*,\s*(\d+)\s*\)\s*;'
)


# ---------------------------------------------------------------------------
# Casting helpers
# ---------------------------------------------------------------------------

def _to_int(s: str) -> int:
    return int(s.strip())


def _to_number(s: str):
    s = s.strip()
    if "." in s:
        return float(s)
    return int(s)


def _strip_token(s: str) -> str:
    return s.strip().strip('"').strip()


# ---------------------------------------------------------------------------
# Main parser
# ---------------------------------------------------------------------------

def parseInputString(src: str) -> Npc:
    """Parse Daedalus source text, return populated Npc."""
    npc = Npc()
    npc.inv_items = []  # explicit reset

    # --- instance header (used as fallback for name + always for id) -----
    header_name_fallback = None
    m = _RE_INSTANCE.search(src)
    if m:
        npc.id = m.group(1)              # preserve leading zeros, keep as str
        header_name_fallback = m.group(2)

    # --- name = "..."; (preferred over header token) ---------------------
    m = _RE_NAME.search(src)
    if m:
        npc.name = m.group(1)
    elif header_name_fallback is not None:
        npc.name = header_name_fallback

    # --- id (explicit `id = N;` line — overrides header if present) ------
    m = _RE_ID.search(src)
    if m:
        npc.id = _strip_token(m.group(1))

    # --- npctype ---------------------------------------------------------
    m = _RE_NPCTYPE.search(src)
    if m:
        tok = _strip_token(m.group(1))
        if tok == "NPCTYPE_FRIEND":
            npc.friend = 1
            # leave npc.type at default
        else:
            npc.type = tok
            npc.friend = 0

    # --- guild -----------------------------------------------------------
    m = _RE_GUILD.search(src)
    if m:
        tok = _strip_token(m.group(1))
        if tok == "GIL_NONE":
            npc.guild = None
        else:
            npc.guild = tok

    # --- level -----------------------------------------------------------
    m = _RE_LEVEL.search(src)
    if m:
        npc.level = _to_int(m.group(1))

    # --- voice -----------------------------------------------------------
    m = _RE_VOICE.search(src)
    if m:
        npc.voice = _to_int(m.group(1))

    # --- flags -----------------------------------------------------------
    m = _RE_FLAGS.search(src)
    if m:
        tok = _strip_token(m.group(1))
        npc.immortal = 1 if tok == "NPC_FLAG_IMMORTAL" else 0

    # --- attributes (commented) ------------------------------------------
    for rx, attr in (
        (_RE_ATR_STR,  "str"),
        (_RE_ATR_DEX,  "dex"),
        (_RE_ATR_MANA, "mana"),
        (_RE_ATR_HP,   "hp"),
    ):
        m = rx.search(src)
        if m:
            setattr(npc, attr, _to_int(m.group(1)))

    # --- talents (commented) ---------------------------------------------
    for rx, attr in (
        (_RE_T1H,   "t1h"),
        (_RE_T2H,   "t2h"),
        (_RE_BOW,   "bow"),
        (_RE_CBOW,  "cbow"),
        (_RE_MAGIC, "magic"),
    ):
        m = rx.search(src)
        if m:
            setattr(npc, attr, _to_int(m.group(1)))

    # --- overlay / walking ----------------------------------------------
    m = _RE_OVERLAY.search(src)
    if m:
        mds = m.group(1)
        npc.walking = None if mds == "HUMANS_MILITIA.MDS" else mds

    # --- npc visual block -----------------------------------------------
    m = _RE_NPCVISUAL.search(src)
    if m:
        # group 1: body model (ignored — always "hum_body_Naked0")
        npc.body_tex   = _to_int(m.group(2))
        npc.skin_color = _to_int(m.group(3))
        head_tok       = m.group(4)
        npc.head       = None if head_tok == "HUM_HEAD_PONY" else head_tok
        npc.face       = m.group(5)
        npc.teeth_tex  = _to_int(m.group(6))
        armor_raw      = m.group(7).strip()
        if armor_raw == "-1":
            npc.armor = "NO_ARMOR"
        else:
            npc.armor = _strip_token(armor_raw)

    # --- fatness ---------------------------------------------------------
    m = _RE_FATNESS.search(src)
    if m:
        npc.fatness = _to_number(m.group(1))

    # --- fight_tactic ----------------------------------------------------
    m = _RE_FIGHT.search(src)
    if m:
        tok = _strip_token(m.group(1))
        npc.fight = None if tok == "FAI_Human_Strong" else tok

    # --- inventory -------------------------------------------------------
    for inv_match in _RE_INV.finditer(src):
        npc.inv_items.append({
            "item": inv_match.group(1),
            "quantity": _to_int(inv_match.group(2)),
        })

    return npc


def parseInputFile(path: str) -> Npc:
    """Read file at path, return populated Npc."""
    return parseInputString(Path(path).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Round-trip self-test
# ---------------------------------------------------------------------------

def _selftest() -> int:
    from services.output_builder import buildOutput

    src_npc = Npc()
    src_npc.name        = "Test Guy"
    src_npc.id          = "042"
    src_npc.guild       = "GIL_MIL"
    src_npc.level       = 12
    src_npc.type        = "npctype_main"
    src_npc.voice       = 3
    src_npc.immortal    = 1
    src_npc.friend      = 0
    src_npc.str         = 20
    src_npc.dex         = 15
    src_npc.mana        = 7
    src_npc.hp          = 110
    src_npc.fatness     = 1.25
    src_npc.head        = "HUM_HEAD_BALD"
    src_npc.walking     = "HUMANS_TIRED.MDS"
    src_npc.armor       = "ITAR_MIL_M"
    src_npc.body_tex    = 9
    src_npc.face        = "FACE_N_Bartholo"
    src_npc.teeth_tex   = 2
    src_npc.skin_color  = 1
    src_npc.fight       = "FAI_Human_Master"
    src_npc.t1h         = 60
    src_npc.t2h         = 30
    src_npc.bow         = 10
    src_npc.cbow        = 5
    src_npc.magic       = 0
    src_npc.inv_items   = [
        {"item": "ItMw_1H_Sword_Long_04", "quantity": 1},
        {"item": "ItFo_Apple",            "quantity": 5},
    ]

    out = buildOutput(src_npc)
    parsed = parseInputString(out)

    # All attributes we set in step 1 should round-trip exactly.
    fields = [
        "name", "id", "guild", "level", "type", "voice", "immortal", "friend",
        "str", "dex", "mana", "hp", "fatness", "head", "walking", "armor",
        "body_tex", "face", "teeth_tex", "skin_color", "fight",
        "t1h", "t2h", "bow", "cbow", "magic", "inv_items",
    ]

    diffs = []
    for f in fields:
        a = getattr(src_npc, f)
        b = getattr(parsed, f)
        if a != b:
            diffs.append(f"  {f}: src={a!r}  parsed={b!r}")

    if diffs:
        print("FAIL — round-trip mismatch:")
        print("\n".join(diffs))
        return 1

    # --- defaults case: a fresh Npc must also round-trip ----------------
    default_npc = Npc()
    default_npc.name = "NPC"  # output_builder coerces empty → "NPC"
    out2 = buildOutput(Npc())
    parsed2 = parseInputString(out2)
    default_fields = [
        "id", "guild", "level", "type", "voice", "immortal", "friend",
        "str", "dex", "mana", "hp", "fatness", "head", "walking", "armor",
        "body_tex", "face", "teeth_tex", "skin_color", "fight",
        "t1h", "t2h", "bow", "cbow", "magic", "inv_items",
    ]
    default_diffs = []
    for f in default_fields:
        a = getattr(default_npc, f)
        b = getattr(parsed2, f)
        if a != b:
            default_diffs.append(f"  {f}: default={a!r}  parsed={b!r}")
    # name: explicit `name = "";` line wins over the header's MOD_<id>_NPC
    # token, so parsed name is the real default ("").
    if parsed2.name != "":
        default_diffs.append(f"  name: expected '', got {parsed2.name!r}")

    if default_diffs:
        print("FAIL — defaults round-trip mismatch:")
        print("\n".join(default_diffs))
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(_selftest())
