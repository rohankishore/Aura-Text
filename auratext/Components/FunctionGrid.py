from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame


class FunctionGridDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setModal(True)
        self.resize(720, 460)
        self.setStyleSheet(
            "QDialog { background-color: #1f1f1f; border: 1px solid #3a3a3a; border-radius: 12px; }"
            "QLabel { color: #f0f0f0; font-size: 15px; }"
            "QFrame { background-color: #2b2b2b; border: 1px solid #4a4a4a; border-radius: 8px; }"
        )

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(18, 18, 18, 18)
        root_layout.setSpacing(12)

        header = QLabel("Function Grid")
        root_layout.addWidget(header)

        grid_container = QWidget(self)
        self.grid_layout = QGridLayout(grid_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(12)

        for row in range(3):
            for col in range(4):
                slot = QFrame(grid_container)
                slot.setMinimumSize(120, 90)
                self.grid_layout.addWidget(slot, row, col)

        root_layout.addWidget(grid_container)
        root_layout.addStretch(1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
            return
        super().keyPressEvent(event)
