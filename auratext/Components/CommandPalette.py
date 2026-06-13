import json
import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem, 
    QApplication, QWidget, QLabel, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor
from auratext.Misc.boilerplates import get_appdata_dirs

class CommandPaletteItemWidget(QWidget):
    def __init__(self, name, shortcut, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(10)
        
        self.name_label = QLabel(name)
        self.name_label.setStyleSheet("color: #e1e1e6; font-size: 13px; font-weight: 500; background: transparent;")
        layout.addWidget(self.name_label)
        
        layout.addStretch()
        
        if shortcut:
            self.shortcut_label = QLabel(shortcut)
            self.shortcut_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(255, 255, 255, 0.08);
                    color: #a5a5b2;
                    border: 1px solid rgba(255, 255, 255, 0.12);
                    border-radius: 4px;
                    padding: 2px 6px;
                    font-size: 11px;
                    font-family: monospace;
                    font-weight: bold;
                }
            """)
            layout.addWidget(self.shortcut_label)

class CommandPalette(QDialog):
    def __init__(self, commands, parent=None):
        super().__init__(parent)
        self.commands = commands
        self.setWindowTitle("Command Palette")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(620, 370)

        # Resolve config and theme background dynamically
        active_window = parent or QApplication.activeWindow()
        config = getattr(active_window, "_config", None)
        theme_bg = "#1e1d23"
        if active_window and hasattr(active_window, "_themes"):
            theme_bg = active_window._themes.get("editor_theme", "#1e1d23")

        if config is None:
            try:
                local_app_data, _ = get_appdata_dirs()
                with open(os.path.join(local_app_data, "data", "config.json"), "r") as config_file:
                    config = json.load(config_file)
            except Exception:
                config = {}

        is_glass = config.get("cmdpaletteglass", "true").lower() == "true"
        bg_color = "rgba(30, 30, 35, 0.93)" if is_glass else theme_bg
        input_bg = "rgba(20, 20, 20, 0.6)" if is_glass else "rgba(0, 0, 0, 0.2)"
        border_color = "rgba(255, 255, 255, 0.15)" if is_glass else "rgba(255, 255, 255, 0.08)"

        # Dialog layout (provides space for drop shadow)
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(10, 10, 10, 10)

        # Floating Container
        self.container = QWidget(self)
        self.container.setObjectName("Container")
        self.container.setStyleSheet(f"""
            QWidget#Container {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 12px;
            }}
            QLineEdit {{
                background-color: {input_bg};
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 10px 12px;
                padding-left: 36px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 1px solid #007acc;
                background-color: rgba(15, 15, 15, 0.8);
            }}
            QListWidget {{
                background-color: transparent;
                border: none;
                outline: none;
            }}
            QListWidget::item {{
                background-color: transparent;
                border-radius: 6px;
                margin: 2px 4px;
            }}
            QListWidget::item:hover {{
                background-color: rgba(255, 255, 255, 0.08);
            }}
            QListWidget::item:selected {{
                background-color: rgba(0, 122, 204, 0.35);
                border: 1px solid rgba(0, 122, 204, 0.5);
            }}
        """)

        # Add Drop Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 5)
        self.container.setGraphicsEffect(shadow)

        dialog_layout.addWidget(self.container)

        # Layout inside the container
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Search Input
        self.search_input = QLineEdit()
        self.command_input = self.search_input
        self.search_input.setPlaceholderText("Type a command...")
        self.search_input.textChanged.connect(self.filter_commands)
        self.search_input.returnPressed.connect(self.execute_selected)
        self.search_input.installEventFilter(self)
        layout.addWidget(self.search_input)

        # Load Search SVG Icon
        local_app_data, _ = get_appdata_dirs()
        icon_path = os.path.join(local_app_data, "icons", "search.svg")
        if os.path.exists(icon_path):
            self.search_input.addAction(QIcon(icon_path), QLineEdit.ActionPosition.LeadingPosition)

        # Command List
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.execute_selected)
        layout.addWidget(self.list_widget)

    def get_shortcut(self, cmd):
        action = cmd.get("action")
        if not action:
            return ""
        
        active_window = QApplication.activeWindow()
        if not active_window or not hasattr(active_window, "_shortcuts"):
            return ""
            
        shortcuts = active_window._shortcuts
        
        action_map = {
            "cs_new_document": "new_file",
            "open_document": "open_file",
            "save_document": "save_file",
            "undo_document": "undo",
            "redo_document": "redo",
            "cut_document": "cut",
            "copy_document": "copy",
            "paste_document": "paste",
            "setupPowershell": "terminal",
            "toggle_split_editor": "split_editor",
            "fullscreen": "fullscreen",
            "run_python_file": "run_python_file",
            "find_in_editor": "find",
            "expandSidebar__Search": "project_search",
            "code_formatting": "format_code",
            "toggle_take_break_mode": "take_break_mode",
            "expandSidebar__Settings": "settings",
        }
        
        func_name = getattr(action, "__name__", "")
        shortcut_key = action_map.get(func_name)
        
        if not shortcut_key:
            name_lower = cmd["name"].lower()
            if "new" in name_lower and "template" not in name_lower:
                shortcut_key = "new_file"
            elif "open" in name_lower and "project" not in name_lower:
                shortcut_key = "open_file"
            elif "save" in name_lower and "as" not in name_lower:
                shortcut_key = "save_file"
            elif "undo" in name_lower:
                shortcut_key = "undo"
            elif "redo" in name_lower:
                shortcut_key = "redo"
            elif "cut" in name_lower:
                shortcut_key = "cut"
            elif "copy" in name_lower:
                shortcut_key = "copy"
            elif "paste" in name_lower:
                shortcut_key = "paste"
            elif "terminal" in name_lower:
                shortcut_key = "terminal"
            elif "split" in name_lower:
                shortcut_key = "split_editor"
            elif "full" in name_lower:
                shortcut_key = "fullscreen"
            elif "run" in name_lower:
                shortcut_key = "run_python_file"
            elif "find" in name_lower:
                shortcut_key = "find"
            elif "search" in name_lower:
                shortcut_key = "project_search"
            elif "format" in name_lower:
                shortcut_key = "format_code"
            elif "zen" in name_lower:
                shortcut_key = "take_break_mode"
            elif "settings" in name_lower:
                shortcut_key = "settings"
                
        if shortcut_key:
            return shortcuts.get(shortcut_key, "")
        return ""

    def populate_list(self, commands):
        self.list_widget.clear()
        for cmd in commands:
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, cmd['action'])
            
            # Create custom widget
            shortcut = self.get_shortcut(cmd)
            widget = CommandPaletteItemWidget(cmd['name'], shortcut, self.list_widget)
            
            item.setSizeHint(widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)
            
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def filter_commands(self, text):
        filtered = [cmd for cmd in self.commands if text.lower() in cmd['name'].lower()]
        self.populate_list(filtered)

    def execute_selected(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            action = current_item.data(Qt.ItemDataRole.UserRole)
            self.close()
            if callable(action):
                action()

    def showEvent(self, event):
        super().showEvent(event)
        self.center_on_active_window()
        self.search_input.setText("")
        self.populate_list(self.commands)
        self.search_input.setFocus()

    def center_on_active_window(self):
        active_window = self.parent() or QApplication.activeWindow()
        if active_window:
            parent_rect = active_window.geometry()
            self_rect = self.geometry()
            x = parent_rect.x() + (parent_rect.width() - self_rect.width()) / 2
            y = parent_rect.y() + 50
            self.move(int(x), int(y))

    def eventFilter(self, obj, event):
        if obj == self.search_input and event.type() == event.Type.KeyPress:
            key = event.key()
            if key == Qt.Key.Key_Down:
                curr_row = self.list_widget.currentRow()
                next_row = (curr_row + 1) % self.list_widget.count() if self.list_widget.count() > 0 else 0
                self.list_widget.setCurrentRow(next_row)
                return True
            elif key == Qt.Key.Key_Up:
                curr_row = self.list_widget.currentRow()
                prev_row = (curr_row - 1) % self.list_widget.count() if self.list_widget.count() > 0 else 0
                self.list_widget.setCurrentRow(prev_row)
                return True
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
