from __future__ import annotations

import json
import winreg
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QComboBox, )

if TYPE_CHECKING:
    from .window import Window


class ConfigPage(QWidget):
    def __init__(self, window: Window):
        super().__init__()
        self._window = window

        self.json_data = {"editor_theme": "", "margin_theme": "", "lines_theme": ""}

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        #layout.addStretch()
        #layout.addSpacing(100)

        # Theme
        theme_label = QLabel("Theme Color:")
        self.theme_input = QLineEdit()
        self.theme_input.setText(self._window._themes["theme"])
        layout.addWidget(theme_label)
        layout.addWidget(self.theme_input)

        theme_label1 = QLabel("Theme :")
        self.theme_combobox = QComboBox()
        self.theme_combobox.setCurrentText(self._window._themes["font"])
        theme_opt = ["dark", "light"]
        self.theme_combobox.addItems(theme_opt)
        current_font_theme = self._window._themes.get("font", "")
        self.theme_combobox.setCurrentText(self._window._themes["theme_type"])
        layout.addWidget(theme_label1)
        layout.addWidget(self.theme_combobox)

        # Editor Theme
        editor_theme_label = QLabel("Editor Background:")
        self.editor_theme_input = QLineEdit()
        self.editor_theme_input.setText(self._window._themes["editor_theme"])
        layout.addWidget(editor_theme_label)
        layout.addWidget(self.editor_theme_input)

        # Sidebar Theme
        sidebar_theme_label = QLabel("Sidebar Background:")
        self.sidebar_theme_input = QLineEdit()
        self.sidebar_theme_input.setText(self._window._themes["sidebar_bg"])
        layout.addWidget(sidebar_theme_label)
        layout.addWidget(self.sidebar_theme_input)

        # MenuBar Theme
        menubar_theme_label = QLabel("MenuBar Background:")
        self.menubar_theme_input = QLineEdit()
        self.menubar_theme_input.setText(self._window._themes["menubar_bg"])
        layout.addWidget(menubar_theme_label)
        layout.addWidget(self.menubar_theme_input)

        # Margin Theme
        margin_theme_label = QLabel("Margin Background:")
        self.margin_theme_input = QLineEdit()
        self.margin_theme_input.setText(self._window._themes["margin_theme"])
        layout.addWidget(margin_theme_label)
        layout.addWidget(self.margin_theme_input)

        # Lines Background
        lines_theme_label = QLabel("Line Number Background:")
        self.lines_theme_input = QLineEdit()
        self.lines_theme_input.setText(self._window._themes["lines_theme"])
        layout.addWidget(lines_theme_label)
        layout.addWidget(self.lines_theme_input)

        # Lines Foreground
        lines_fg_label = QLabel("Line Number Foreground:")
        self.lines_fg_input = QLineEdit()
        self.lines_fg_input.setText(self._window._themes["lines_fg"])
        layout.addWidget(lines_fg_label)
        layout.addWidget(self.lines_fg_input)

        # Get the list of installed fonts
        font_names = self.get_installed_fonts()

        # Font Theme
        font_theme_label = QLabel("Font Theme:")
        self.font_theme_combobox = QComboBox()
        self.font_theme_combobox.setCurrentText(self._window._themes["font"])
        self.font_theme_combobox.addItems(font_names)
        current_font_theme = self._window._themes.get("font", "")
        if current_font_theme in font_names:
            self.font_theme_combobox.setCurrentText(current_font_theme)
        layout.addWidget(font_theme_label)
        layout.addWidget(self.font_theme_combobox)

        # Save Button
        save_button = QPushButton("Apply")
        save_button.setStyleSheet(
            "QPushButton {"
            "   border-radius: 10px;"
            "   padding: 5px;"
            "background-color: #121212;"
            "color: white;"
            "}"
        )
        save_button.clicked.connect(self.save_json)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.setWindowTitle("Settings")

    def save_json(self):
        self._window._themes["theme"] = self.theme_input.text()
        self._window._themes["editor_theme"] = self.editor_theme_input.text()
        self._window._themes["margin_theme"] = self.margin_theme_input.text()
        self._window._themes["sidebar_bg"] = self.sidebar_theme_input.text()
        self._window._themes["menubar_bg"] = self.menubar_theme_input.text()
        self._window._themes["lines_theme"] = self.lines_theme_input.text()
        self._window._themes["lines_fg"] = self.lines_fg_input.text()
        self._window._themes["font"] = self.font_theme_combobox.currentText()
        self._window._themes["theme_type"] = self.theme_combobox.currentText()

        with open(f"{self._window.local_app_data}/data/theme.json", "w") as json_file:
            json.dump(self._window._themes, json_file)

        QMessageBox.information(
            self,
            "Settings Applied!",
            "The chosen settings have been applied. Restart Aura Text to see the changes.",
        )

    def get_installed_fonts(self):
        font_key_path = r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"
        font_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, font_key_path)

        font_names = []
        try:
            index = 0
            while True:
                font_name, _, _ = winreg.EnumValue(font_key, index)
                font_name = font_name.replace("(TrueType)", "")
                font_names.append(font_name)
                index += 1
        except WindowsError:
            pass

        winreg.CloseKey(font_key)

        return font_names


