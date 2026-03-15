from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout


class FunctionGridWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        root_layout = QVBoxLayout(self)

        header = QLabel("Function Grid")
        root_layout.addWidget(header)

        grid_container = QWidget(self)
        self.grid_layout = QGridLayout(grid_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(12)

        root_layout.addWidget(grid_container)
        root_layout.addStretch(1)
