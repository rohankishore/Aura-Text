from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtCore import Qt, QRect

class MiniMapWidget(QWidget):
    def __init__(self, editor=None, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.setMinimumWidth(80)
        self.setMaximumWidth(120)
        self.setStyleSheet("background: #222;")
        if self.editor:
            self.editor.textChanged.connect(self.update)
            self.editor.verticalScrollBar().valueChanged.connect(self.update)

    def set_editor(self, editor):
        if self.editor:
            try:
                self.editor.textChanged.disconnect(self.update)
                self.editor.verticalScrollBar().valueChanged.disconnect(self.update)
            except Exception:
                pass
        self.editor = editor
        if self.editor:
            self.editor.textChanged.connect(self.update)
            self.editor.verticalScrollBar().valueChanged.connect(self.update)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if not self.editor:
            painter.end()
            return
        font = QFont(self.editor.font())
        font.setPointSize(3)
        painter.setFont(font)
        lines = self.editor.text().split('\n')
        line_height = 3
        margin = 2
        max_lines = self.height() // line_height
        for i, line in enumerate(lines[:max_lines]):
            painter.setPen(QColor('#888'))
            # Draw a tiny rectangle for each line, simulating code blocks
            painter.drawRect(margin, i*line_height, self.width()-2*margin, line_height-1)
        # Draw viewport rectangle
        if hasattr(self.editor, 'firstVisibleLine'):
            first_visible = self.editor.firstVisibleLine()
            visible_lines = self.editor.linesOnScreen() if hasattr(self.editor, 'linesOnScreen') else 20
            painter.setPen(QColor('#59ff00'))
            painter.drawRect(0, first_visible*line_height, self.width()-1, visible_lines*line_height)

    def mousePressEvent(self, event):
        if not self.editor:
            return
        y = event.position().y()
        line_height = 3
        line_num = int(y // line_height)
        if hasattr(self.editor, 'setFirstVisibleLine'):
            self.editor.setFirstVisibleLine(line_num)
