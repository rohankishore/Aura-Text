from __future__ import annotations

import keyword

from PyQt6.Qsci import QsciAPIs, QsciLexerPython, QsciScintilla


class PythonAutocompleteEngine:
    def __init__(self, editor: QsciScintilla) -> None:
        self.editor = editor
        self._apis: QsciAPIs | None = None
        words = set(keyword.kwlist)
        soft_keywords = getattr(keyword, "softkwlist", [])
        words.update(soft_keywords)
        self._keywords = sorted(words)

    def refresh(self) -> None:
        lexer = self.editor.lexer()
        if not isinstance(lexer, QsciLexerPython):
            self._apis = None
            return

        apis = QsciAPIs(lexer)
        for word in self._keywords:
            apis.add(word)
        apis.prepare()
        self._apis = apis
        self.editor.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAPIs)
        self.editor.setAutoCompletionThreshold(1)
        self.editor.setAutoCompletionCaseSensitivity(True)

    def trigger(self, force: bool = False) -> None:
        lexer = self.editor.lexer()
        if not isinstance(lexer, QsciLexerPython):
            return

        if self._apis is None:
            self.refresh()

        if force:
            self.editor.autoCompleteFromAPIs()
            return

        line, index = self.editor.getCursorPosition()
        if index <= 0:
            return
        char_before_cursor = self.editor.text(line)[index - 1]
        if char_before_cursor.isalnum() or char_before_cursor == "_":
            self.editor.autoCompleteFromAPIs()
