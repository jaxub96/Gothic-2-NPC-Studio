import re

from PySide6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat

from constants.colors import THEME


class DaedalusHighlighter(QSyntaxHighlighter):
    """PySide6 port of the legacy DaedalusHighlighter (models/).

    Colors come from constants.colors.THEME so both UIs stay visually in sync.
    """

    def __init__(self, document) -> None:
        super().__init__(document)
        t = THEME
        self.rules: list[tuple[re.Pattern, QTextCharFormat]] = []

        def fmt(color: str, bold: bool = False, italic: bool = False) -> QTextCharFormat:
            f = QTextCharFormat()
            f.setForeground(QColor(color))
            if bold:
                f.setFontWeight(QFont.Weight.Bold)
            if italic:
                f.setFontItalic(True)
            return f

        kw = fmt(t["syn_keyword"], bold=True)
        for w in (
            "instance", "func", "void", "int", "var", "return", "if", "else",
            "INSTANCE", "FUNC", "VOID", "INT", "VAR",
        ):
            self.rules.append((re.compile(r"\b" + w + r"\b"), kw))

        tp = fmt(t["syn_type"], bold=True)
        for w in (
            "C_INFO", "TRUE", "FALSE", "LOG_MISSION", "LOG_NOTE",
            "LOG_RUNNING", "LOG_SUCCESS", "DIALOG_ENDE",
        ):
            self.rules.append((re.compile(r"\b" + w + r"\b"), tp))

        fn = fmt(t["syn_function"])
        for w in (
            "AI_Output", "AI_StopProcessInfos", "B_GiveXP", "B_GiveInvItems",
            "CreateInvItems", "Log_CreateTopic", "Log_SetTopicStatus", "B_LogEntry",
            "Info_ClearChoices", "Info_AddChoice", "Npc_KnowsInfo",
            "Npc_GetTrueGuild", "Npc_IsInState", "Npc_SetTalentSkill",
            "Mdl_SetVisual", "Mdl_ApplyOverlayMds", "Mdl_SetVisualBody",
            "B_Scale", "Mdl_SetModelFatness", "TA_Position",
        ):
            self.rules.append((re.compile(r"\b" + w + r"\b"), fn))

        self.rules.append((re.compile(r'"[^"]*"'), fmt(t["syn_string"])))
        self.rules.append((re.compile(r"//[^\n]*"), fmt(t["syn_comment"], italic=True)))
        self.rules.append((re.compile(r"\b\d+\b"), fmt(t["syn_number"])))

    def highlightBlock(self, text: str) -> None:
        for pattern, char_format in self.rules:
            for m in pattern.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), char_format)
