from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QApplication
from PyQt6.QtCore import Qt

class CommandPalette(QDialog):
    def __init__(self, commands, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Command Palette")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(600, 300)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter command...")
        self.command_input.textChanged.connect(self.filter_commands)
        self.layout.addWidget(self.command_input)

        self.command_list = QListWidget()
        self.command_list.itemClicked.connect(self.execute_command)
        self.layout.addWidget(self.command_list)

        self.commands = commands

    def populate_commands(self, filter_text=""):
        self.command_list.clear()
        for command in self.commands:
            if filter_text.lower() in command["name"].lower():
                item = QListWidgetItem(command["name"])
                item.setData(Qt.ItemDataRole.UserRole, command["action"])
                self.command_list.addItem(item)

    def filter_commands(self, text):
        self.populate_commands(text)

    def execute_command(self, item):
        action = item.data(Qt.ItemDataRole.UserRole)
        if action:
            action()
        self.close()

    def showEvent(self, event):
        super().showEvent(event)
        self.center_on_active_window()
        self.command_input.setText("")
        self.populate_commands()

    def center_on_active_window(self):
        if self.parent():
            parent_rect = self.parent().geometry()
            self_rect = self.geometry()
            x = parent_rect.x() + (parent_rect.width() - self_rect.width()) / 2
            y = parent_rect.y() + 50  # A bit of offset from the top
            self.move(int(x), int(y))
        else:
            active_window = QApplication.activeWindow()
            if active_window:
                parent_rect = active_window.geometry()
                self_rect = self.geometry()
                x = parent_rect.x() + (parent_rect.width() - self_rect.width()) / 2
                y = parent_rect.y() + 50  # A bit of offset from the top
                self.move(int(x), int(y))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
