from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame


class FunctionGridDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setModal(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.resize(720, 460)
        self.setStyleSheet(
            "QDialog { background-color: #1f1f1f; border: 1px solid #3a3a3a; border-radius: 12px; }"
            "QLabel { color: #f0f0f0; font-size: 15px; }"
            "QFrame { background-color: #2b2b2b; border: 1px solid #4a4a4a; border-radius: 8px; }"
        )

        self.rows = 3
        self.cols = 4
        self.slots = []
        self.selected_index = 0

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(18, 18, 18, 18)
        root_layout.setSpacing(12)

        header = QLabel("Function Grid")
        root_layout.addWidget(header)

        grid_container = QWidget(self)
        self.grid_layout = QGridLayout(grid_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(12)

        for row in range(self.rows):
            for col in range(self.cols):
                slot = QFrame(grid_container)
                slot.setMinimumSize(120, 90)
                slot.installEventFilter(self)
                self.grid_layout.addWidget(slot, row, col)
                self.slots.append(slot)

        self.update_selection()

        root_layout.addWidget(grid_container)
        root_layout.addStretch(1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
            return

        if event.key() == Qt.Key.Key_Left:
            if self.selected_index % self.cols != 0:
                self.selected_index -= 1
                self.update_selection()
            return

        if event.key() == Qt.Key.Key_Right:
            if self.selected_index % self.cols != self.cols - 1:
                self.selected_index += 1
                self.update_selection()
            return

        if event.key() == Qt.Key.Key_Up:
            if self.selected_index - self.cols >= 0:
                self.selected_index -= self.cols
                self.update_selection()
            return

        if event.key() == Qt.Key.Key_Down:
            if self.selected_index + self.cols < len(self.slots):
                self.selected_index += self.cols
                self.update_selection()
            return

        super().keyPressEvent(event)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.MouseButtonPress and watched in self.slots:
            self.selected_index = self.slots.index(watched)
            self.update_selection()
            return True
        return super().eventFilter(watched, event)

    def update_selection(self):
        for index, slot in enumerate(self.slots):
            if index == self.selected_index:
                slot.setStyleSheet("background-color: #2b2b2b; border: 2px solid #00a2ff; border-radius: 8px;")
            else:
                slot.setStyleSheet("background-color: #2b2b2b; border: 1px solid #4a4a4a; border-radius: 8px;")
