from PyQt6.QtCore import Qt, QEvent, QSize
from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QLabel, QGridLayout, QToolButton, QStyle


class FunctionGridDialog(QDialog):
    def __init__(self, parent=None, actions=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setModal(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.resize(720, 460)
        self.setStyleSheet(
            "QDialog { background-color: #1f1f1f; border: 1px solid #3a3a3a; border-radius: 12px; }"
            "QLabel { color: #f0f0f0; font-size: 15px; }"
            "QToolButton { background-color: #2b2b2b; border: 1px solid #4a4a4a; border-radius: 8px; }"
            "QToolButton:hover { border: 1px solid #6a6a6a; }"
        )

        self.actions = actions or {}
        self.rows = 3
        self.cols = 4
        self.buttons = []
        self.selected_index = 0

        self.grid_items = [
            ("open_project", "Open", "Open Project", QStyle.StandardPixmap.SP_DialogOpenButton),
            ("settings", "Settings", "Settings", QStyle.StandardPixmap.SP_FileDialogDetailedView),
            ("todo", "To-Do", "To-Do", QStyle.StandardPixmap.SP_DialogApplyButton),
            ("additional_prefs", "Prefs", "Additional Preferences", QStyle.StandardPixmap.SP_FileDialogInfoView),
            ("keyboard_bindings", "Keys", "Keyboard Bindings", QStyle.StandardPixmap.SP_ComputerIcon),
            ("extensions", "Extensions", "Extensions", QStyle.StandardPixmap.SP_DirIcon),
            ("themes", "Themes", "Themes", QStyle.StandardPixmap.SP_FileDialogListView),
            ("performance_monitor", "Perf", "Performance Monitor", QStyle.StandardPixmap.SP_BrowserReload),
            ("notes", "Notes", "Notes", QStyle.StandardPixmap.SP_FileIcon),
            ("manage_projects", "Projects", "Manage Projects", QStyle.StandardPixmap.SP_DirOpenIcon),
            ("open_project_tree", "Tree", "Open Project as Tree View", QStyle.StandardPixmap.SP_DirHomeIcon),
            ("command_palette", "Palette", "Command Palette", QStyle.StandardPixmap.SP_DesktopIcon),
        ]

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(18, 18, 18, 18)
        root_layout.setSpacing(12)

        header = QLabel("Function Grid")
        root_layout.addWidget(header)

        grid_container = QWidget(self)
        self.grid_layout = QGridLayout(grid_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(12)

        for index, (action_key, caption_text, tooltip_text, icon_name) in enumerate(self.grid_items):
            row = index // self.cols
            col = index % self.cols
            button = QToolButton(grid_container)
            button.setIcon(self.style().standardIcon(icon_name))
            button.setIconSize(QSize(30, 30))
            button.setText(caption_text)
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            button.setToolTip(tooltip_text)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(132, 132)
            button.installEventFilter(self)
            button.clicked.connect(lambda checked=False, key=action_key: self.trigger_action(key))
            self.grid_layout.addWidget(button, row, col)
            self.buttons.append(button)

        for row in range(self.rows):
            self.grid_layout.setRowStretch(row, 0)
        for col in range(self.cols):
            self.grid_layout.setColumnStretch(col, 0)

        self.update_selection()

        root_layout.addWidget(grid_container)
        root_layout.addStretch(1)
        self.setFocus()

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
            if self.selected_index + self.cols < len(self.buttons):
                self.selected_index += self.cols
                self.update_selection()
            return

        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            action_key = self.grid_items[self.selected_index][0]
            self.trigger_action(action_key)
            return

        super().keyPressEvent(event)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.MouseButtonPress and watched in self.buttons:
            self.selected_index = self.buttons.index(watched)
            self.update_selection()
            return False
        return super().eventFilter(watched, event)

    def update_selection(self):
        for index, button in enumerate(self.buttons):
            if index == self.selected_index:
                button.setStyleSheet("background-color: #2b2b2b; border: 2px solid #00a2ff; border-radius: 8px;")
            else:
                button.setStyleSheet("background-color: #2b2b2b; border: 1px solid #4a4a4a; border-radius: 8px;")

    def trigger_action(self, action_key):
        action = self.actions.get(action_key)
        if callable(action):
            self.accept()
            action()
