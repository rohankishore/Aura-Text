from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QLabel, QGridLayout


class FunctionGridDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Function Grid")
        self.resize(720, 460)

        root_layout = QVBoxLayout(self)

        header = QLabel("Function Grid")
        root_layout.addWidget(header)

        grid_container = QWidget(self)
        self.grid_layout = QGridLayout(grid_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(12)

        root_layout.addWidget(grid_container)
        root_layout.addStretch(1)
