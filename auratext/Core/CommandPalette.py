from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction

class CommandPalette(QDialog):
    def __init__(self, commands, parent=None):
        super().__init__(parent)
        self.commands = commands  # List of dicts: {'name': str, 'action': callable}
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.setFixedSize(600, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #252526;
                border: 1px solid #454545;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: #cccccc;
                border: 1px solid #3c3c3c;
                padding: 8px;
                font-size: 14px;
            }
            QListWidget {
                background-color: #252526;
                border: none;
                color: #cccccc;
            }
            QListWidget::item {
                padding: 8px;
            }
            QListWidget::item:selected {
                background-color: #094771;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type a command...")
        self.search_input.textChanged.connect(self.filter_commands)
        self.search_input.returnPressed.connect(self.execute_selected)
        layout.addWidget(self.search_input)

        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.execute_selected)
        layout.addWidget(self.list_widget)

        self.populate_list(self.commands)

    def populate_list(self, commands):
        self.list_widget.clear()
        for cmd in commands:
            item = QListWidgetItem(cmd['name'])
            item.setData(Qt.ItemDataRole.UserRole, cmd['action'])
            self.list_widget.addItem(item)
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def filter_commands(self, text):
        filtered = [cmd for cmd in self.commands if text.lower() in cmd['name'].lower()]
        self.populate_list(filtered)

    def execute_selected(self):
        if self.list_widget.currentItem():
            action = self.list_widget.currentItem().data(Qt.ItemDataRole.UserRole)
            self.close()
            if callable(action):
                action()
