from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtCore import Qt, QRect

class MiniMapWidget(QWidget):
    def __init__(self, editor, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.setMinimumWidth(80)
        self.setMaximumWidth(120)
        self.setStyleSheet("background: #222;")
        self.editor.textChanged.connect(self.update)
        self.editor.verticalScrollBar().valueChanged.connect(self.update)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        font = QFont(self.editor.font())
        font.setPointSize(4)
        painter.setFont(font)
        lines = self.editor.text().split('\n')
        line_height = 4
        visible_lines = self.height() // line_height
        scroll_value = self.editor.verticalScrollBar().value()
        for i, line in enumerate(lines):
            if i >= visible_lines:
                break
            painter.setPen(QColor('#888'))
            painter.drawText(2, (i+1)*line_height, line[:80])
        # Draw viewport rectangle
        painter.setPen(QColor('#59ff00'))
        painter.drawRect(0, scroll_value, self.width()-1, line_height*visible_lines)

    def mousePressEvent(self, event):
        y = event.position().y()
        line_height = 4
        line_num = int(y // line_height)
        self.editor.verticalScrollBar().setValue(line_num)
