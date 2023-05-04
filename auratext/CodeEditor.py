from PySide6 import QtGui
from PySide6.QtCore import Qt, QRect, Signal
from PySide6.QtWidgets import QWidget, QPlainTextEdit, QMenu, QTextEdit, QCompleter
from PySide6.QtGui import QPainter, QColor, QTextFormat, QTextCursor
import Modules as ModuleFile

class Completer(QCompleter):
    insertText = Signal(str)

    def __init__(self, myKeywords, parent=None):
        QCompleter.__init__(self, myKeywords, parent)
        self.activated.connect(self.changeCompletion)

    def changeCompletion(self, completion):
        if completion.find("(") != -1:
            completion = completion[:completion.find("(")]
            print(completion)
        print("completion is " + str(completion))
        self.insertText.emit(completion + " ")
        self.popup().hide()


class LineNumberArea(QWidget):
    def __init__(self, editor):
        QWidget.__init__(self, parent=editor)
        self.codeEditor = editor
        self.codeEditor.setStyleSheet("background-color : #1e1f22")

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, keyword, parent=None):
        QPlainTextEdit.__init__(self, parent)
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()
        completer = QCompleter(keyword)
        completer.activated.connect(self.insert_completion)
        completer.setWidget(self)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer = completer
        self.textChanged.connect(self.complete)

    def insert_completion(self, completion):
        tc = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.MoveOperation.Left)
        tc.movePosition(QTextCursor.MoveOperation.EndOfWord)
        tc.insertText(completion[-extra:] + " ")
        self.setTextCursor(tc)

    @property
    def text_under_cursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.SelectionType.WordUnderCursor)
        return tc.selectedText()

    def complete(self):
        prefix = self.text_under_cursor
        self.completer.setCompletionPrefix(prefix)
        popup = self.completer.popup()
        popup.setStyleSheet("background-color : #2b2d30; color: white")
        popup.setFixedWidth(150)
        cr = self.cursorRect()
        popup.setCurrentIndex(self.completer.completionModel().index(0, 0))
        cr.setWidth(
            self.completer.popup().sizeHintForColumn(0)
            + self.completer.popup().verticalScrollBar().sizeHint().width()
        )
        self.completer.complete(cr)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if self.completer.popup().isVisible() and event.key() in [
            #Qt.Key.Key_Enter,
            Qt.Key.Key_Up,
            Qt.Key.Key_Down,
            Qt.Key.Key_Tab,
            Qt.Key.Key_Backtab,
        ]:
            event.ignore()
            return
        super().keyPressEvent(event)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), "#1e1f22")
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(
            block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.white)
                painter.drawText(0, top, self.lineNumberArea.width(),
                                 self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignCenter, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def lineNumberAreaWidth(self):
        space = 50 + 5
        return space

    def encrypt(self):
        ModuleFile.encypt(self)

    def search_google(self):
        ModuleFile.search_google(self)

    def decrypt(self):
        ModuleFile.decode(self)

    def calculate(self):
        ModuleFile.calculate(self)

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)

        encrypt_menu = QMenu(contextMenu)
        encrypt_menu.setTitle("Encryption")
        encrypt_menu.addAction("Encrypt Selection", self.encrypt)
        encrypt_menu.addAction("Decrypt Selection", self.decrypt)

        contextMenu.addAction("Undo", self.undo).setShortcut("Ctrl+Z")
        contextMenu.addAction("Redo", self.redo).setShortcut("Ctrl+Shift+Z")
        contextMenu.addSeparator()
        contextMenu.addAction("Select All",
                              self.selectAll).setShortcut("Ctrl+A")
        contextMenu.addAction("Cut", self.cut).setShortcut("Ctrl+X")
        contextMenu.addAction(
            "Copy                                  ",
            self.copy).setShortcut("Ctrl+C")
        contextMenu.addAction("Paste", self.paste).setShortcut("Ctrl+V")
        contextMenu.addSeparator()
        contextMenu.addAction("Search In Google", self.search_google)
        contextMenu.addAction("Calculate", self.calculate)
        contextMenu.addMenu(encrypt_menu)
        action = contextMenu.exec(self.mapToGlobal(event.pos()))

    def resizeEvent(self, event):
        QPlainTextEdit.resizeEvent(self, event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(
                cr.left(),
                cr.top(),
                self.lineNumberAreaWidth(),
                cr.height()))

    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            formatt = QtGui.QTextCharFormat()
            selection = QTextEdit.ExtraSelection()
            selection.format = formatt
            lineColor = QColor("#2b2d30").lighter(190)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(
                0, rect.y(),
                self.lineNumberArea.width(),
                rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)
