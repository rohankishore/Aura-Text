from __future__ import annotations
from typing import TYPE_CHECKING
from PyQt6.Qsci import QsciScintilla, QsciAPIs
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QColor, QFont, QFontMetrics, QShortcut, QKeySequence, QAction
from PyQt6.QtWidgets import QMenu, QLineEdit, QCheckBox, QPushButton, QLabel, QMessageBox, QDialog
from . import Lexers
from . import Modules as ModuleFile

if TYPE_CHECKING:
    from .window import Window


class Search(QDialog):
    def __init__(self, editor: CodeEditor) -> None:
        super().__init__()
        self.setObjectName("Search")
        self.editor = editor

        self.textBox = QLineEdit(self)
        self.textBox.setObjectName("Textbox")
        self.textBox.setGeometry(QRect(10, 30, 251, 21))
        self.textBox.setPlaceholderText("Enter text to find")

        self.cs = QCheckBox(self)
        self.cs.setObjectName("Case")
        self.cs.setGeometry(QRect(10, 70, 41, 17))
        self.cs.setText("Case sensitive")

        self.next = QPushButton(self)
        self.next.setObjectName("Next")
        self.next.setGeometry(QRect(190, 70, 71, 23))
        self.next.setText("Next")
        self.next.clicked.connect(self.find_next)

        self.previous = QPushButton(self)
        self.previous.setObjectName("Previous")
        self.previous.setText("Previous")
        self.previous.setGeometry(QRect(110, 70, 75, 23))
        self.previous.clicked.connect(self.find_previous)

        self.label = QLabel(self)
        self.label.setObjectName("Label")
        self.label.setGeometry(QRect(10, 10, 91, 16))
        self.label.setText("Enter Text to Find")

        self.setWindowTitle("Find")

    def find_next(self):
        search_text = self.textBox.text()
        case_sensitive = self.cs.isChecked()
        if search_text:
            self.editor.search(search_text, case_sensitive, forward=True)
        else:
            QMessageBox.warning(self, "Warning", "Please enter text to find.")

    def find_previous(self):
        search_text = self.textBox.text()
        case_sensitive = self.cs.isChecked()
        if search_text:
            self.editor.search(search_text, case_sensitive, forward=False)
        else:
            QMessageBox.warning(self, "Warning", "Please enter text to find.")


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
        find_action = QAction("Find", self)
        find_action.triggered.connect(self.show_search_dialog)
        find_action.setShortcut(QKeySequence.StandardKey.Find)  # Setting shortcut to Ctrl+F
        self.context_menu.addAction(find_action)
        self.context_menu.addSeparator()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, point):
        self.context_menu.popup(self.mapToGlobal(point))

    def show_search_dialog(self):
        search_dialog = Search(self)
        search_dialog.exec()

    def calculate(self):
        ModuleFile.calculate(self)

    def encode(self):
        ModuleFile.encypt(self)

    def decode(self):
        ModuleFile.decode(self)

    # noinspection ReturnValueFromInit
    def search(self, string: str, cs: bool = False, forward: bool = True) -> None:
        """Seaches for string in the editor

        Parameters
        ----------
        string : `str`
            The string to search for
        cs : `bool`
            Case sensitive, by default False
        forward : `bool`
            Check ahead for behind the cursor, by default True
        """
        if not string:
            return
        if self.hasSelectedText():
            pos = self.getSelection()[2:] if forward else self.getSelection()[:2]
        else:
            pos = self.getCursorPosition()
        start = self.positionFromLineIndex(*pos) if forward else 0
        end = len(self.text()) if forward else self.positionFromLineIndex(*pos)
        pos = self._search(string, cs, forward, start, end)
        if pos >= 0:
            return self._highlight(len(string), pos)
        pos = self._search(string, cs, forward, 0, len(self.text()))
        if pos >= 0:
            return self._highlight(len(string), pos)
        if self.hasSelectedText():
            pos = self.getSelection()[2:] if forward else self.getSelection()[:2]
            return self.setCursorPosition(*pos)

    def _highlight(self, length: int, pos: int) -> None:
        """Highlights the searched text if found

        Parameters
        ----------
        length: `int`
            The string being
        pos: `int`
            The starting position of the highlight
        """
        self.SendScintilla(self.SCI_SETSEL, pos, pos + length)

    # noinspection
    def _search(
            self,
            string: str,
            cs: bool = False,
            forward: bool = True,
            start: int = -1,
            end: int = -1,
    ) -> None:
        """Sets search for the string"""
        search = self.SendScintilla
        search(self.SCI_SETTARGETSTART, start if forward else end)
        search(self.SCI_SETTARGETEND, end if forward else start)
        search(self.SCI_SETSEARCHFLAGS, self.SCFIND_MATCHCASE if cs else 0)
        return search(self.SCI_SEARCHINTARGET, len(string), bytes(string, "utf-8"))
