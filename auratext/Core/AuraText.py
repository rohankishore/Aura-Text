from __future__ import annotations
from typing import TYPE_CHECKING
from PyQt6.Qsci import QsciScintilla, QsciAPIs
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QFontMetrics
from PyQt6.QtWidgets import QMenu
from .plugin_interface import ContextMenuPluginInterface
from . import Lexers
from . import Modules as ModuleFile


if TYPE_CHECKING:
    from .window import Window


class CodeEditor(QsciScintilla):
    def __init__(self, window: Window):
        super().__init__(parent=None)

        lexer = Lexers.PythonLexer(window)
        self.setLexer(lexer)
        self.setPaper(QColor(window._themes["editor_theme"]))

        # Autocompletion
        apis = QsciAPIs(self.lexer())
        self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionCaseSensitivity(True)
        self.setWrapMode(QsciScintilla.WrapMode.WrapNone)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionFillupsEnabled(True)

        # Setting up lexers
        lexer.setPaper(QColor(window._themes["editor_theme"]))
        lexer.setColor(QColor("#808080"), lexer.Comment)
        lexer.setColor(QColor("#FFA500"), lexer.Keyword)
        lexer.setColor(QColor("#FFFFFF"), lexer.ClassName)
        lexer.setColor(QColor("#59ff00"), lexer.TripleSingleQuotedString)
        lexer.setColor(QColor("#59ff00"), lexer.TripleDoubleQuotedString)
        lexer.setColor(QColor("#3ba800"), lexer.SingleQuotedString)
        lexer.setColor(QColor("#3ba800"), lexer.DoubleQuotedString)
        lexer.setColor(QColor(window._themes["editor_fg"]), lexer.Default)
        lexer.setFont(QFont(window._themes["font"]))

        self.setTabWidth(4)
        self.setMarginLineNumbers(1, True)
        self.setAutoIndent(True)
        self.setMarginWidth(1, "#0000")
        left_margin_index = 0
        left_margin_width = 7
        self.setMarginsForegroundColor(QColor(window._themes["lines_fg"]))
        self.setMarginsBackgroundColor(QColor(window._themes["lines_theme"]))
        font_metrics = QFontMetrics(self.font())
        left_margin_width_pixels = font_metrics.horizontalAdvance(" ") * left_margin_width
        self.SendScintilla(self.SCI_SETMARGINLEFT, left_margin_index, left_margin_width_pixels)
        self.setFolding(QsciScintilla.FoldStyle.BoxedTreeFoldStyle)
        self.setMarginSensitivity(2, True)
        self.setFoldMarginColors(
            QColor(window._themes["margin_theme"]), QColor(window._themes["margin_theme"])
        )
        self.setBraceMatching(QsciScintilla.BraceMatch.StrictBraceMatch)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#20d3d3d3"))
        self.setWrapMode(QsciScintilla.WrapMode.WrapNone)
        self.setAutoCompletionThreshold(1)
        self.setBackspaceUnindents(True)
        self.setIndentationGuides(True)
        self.setReadOnly(False)

        self.context_menu = QMenu(self)

        self.encrypt_menu = QMenu("Encryption", self.context_menu)
        self.context_menu.addAction("Cut        ").triggered.connect(self.cut)
        self.context_menu.addAction("Copy").triggered.connect(self.copy)
        self.context_menu.addAction("Paste").triggered.connect(self.paste)
        self.context_menu.addAction("Select All").triggered.connect(self.selectAll)
        self.context_menu.addSeparator()
        self.context_menu.addAction("Calculate", self.calculate)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, point):
        self.context_menu.popup(self.mapToGlobal(point))

    def calculate(self):
        ModuleFile.calculate(self)

    def encode(self):
        ModuleFile.encypt(self)

    def decode(self):
        ModuleFile.decode(self)
