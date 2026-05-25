from __future__ import annotations

import json
import platform
if platform.system() == "Windows":
    import winreg
from typing import TYPE_CHECKING

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QComboBox, QGroupBox, QScrollArea, QDialog, )

if TYPE_CHECKING:
    from .window import Window


class ConfigPage(QWidget):
    def __init__(self, window: Window):
        super().__init__()
        self._window = window

        self.json_data = {"editor_theme": "", "margin_theme": "", "lines_theme": ""}

        self.init_ui()

    def init_ui(self):
        # Main layout for ConfigPage
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Create a widget to hold all the content
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)

        self.theme_grouping = QGroupBox("Theming")
        self.theme_layout = QVBoxLayout()
        self.theme_grouping.setLayout(self.theme_layout)

        self.editor_grouping = QGroupBox("Editor")
        self.editor_layout = QVBoxLayout()
        self.editor_grouping.setLayout(self.editor_layout)

        # Theming Type
        theming_label = QLabel("Theming Type :")
        self.theming_combobox = QComboBox()
        self.theming_combobox.currentTextChanged.connect(self.theming_shift)
        if self._window._themes["theming"] == "flat":
            self.theming_combobox.setCurrentText("Flat (Default)")
        else:
            self.theming_combobox.setCurrentText("Material")

        theme_opt = ["Material", "Flat (Default)"]
        self.theming_combobox.addItems(theme_opt)
        self.theme_layout.addWidget(theming_label)
        self.theme_layout.addWidget(self.theming_combobox)

        # Titlebar Type
        self.titlebar_label = QLabel("Titlebar Type")
        self.titlebar = QComboBox()
        self.titlebar.setCurrentText("Flat (Default)")
        titlebar_opt = ['Mica',
                        'Acrylic',
                        'Aero',
                        'Transparent ',
                        'Win7',
                        'Optimised',
                        'Inverse',
                        'Native',
                        'Popup',
                        'Dark',
                        'Normal']
        self.titlebar.addItems(titlebar_opt)
        self.theme_layout.addWidget(self.titlebar_label)
        self.theme_layout.addWidget(self.titlebar)

        # Theme
        theme_label = QLabel("Theme Color:")
        self.theme_input = QLineEdit()
        self.theme_input.setText(self._window._themes["theme"])
        self.theme_layout.addWidget(theme_label)
        self.theme_layout.addWidget(self.theme_input)

        theme_label1 = QLabel("Theme :")
        self.theme_combobox = QComboBox()
        self.theme_combobox.setCurrentText(self._window._themes["font"])
        theme_opt = ["dark", "light"]
        self.theme_combobox.addItems(theme_opt)
        current_font_theme = self._window._themes.get("font", "")
        self.theme_combobox.setCurrentText(self._window._themes["theme_type"])
        self.theme_layout.addWidget(theme_label1)
        self.theme_layout.addWidget(self.theme_combobox)

        # Editor Theme
        editor_theme_label = QLabel("Editor Background:")
        self.editor_theme_input = QLineEdit()
        self.editor_theme_input.setText(self._window._themes["editor_theme"])
        self.editor_layout.addWidget(editor_theme_label)
        self.editor_layout.addWidget(self.editor_theme_input)

        # Sidebar Theme
        sidebar_theme_label = QLabel("Sidebar Background:")
        self.sidebar_theme_input = QLineEdit()
        self.sidebar_theme_input.setText(self._window._themes["sidebar_bg"])
        self.theme_layout.addWidget(sidebar_theme_label)
        self.theme_layout.addWidget(self.sidebar_theme_input)

        # MenuBar Theme
        menubar_theme_label = QLabel("MenuBar Background:")
        self.menubar_theme_input = QLineEdit()
        self.menubar_theme_input.setText(self._window._themes["menubar_bg"])
        self.theme_layout.addWidget(menubar_theme_label)
        self.theme_layout.addWidget(self.menubar_theme_input)

        # Margin Theme
        margin_theme_label = QLabel("Margin Background:")
        self.margin_theme_input = QLineEdit()
        self.margin_theme_input.setText(self._window._themes["margin_theme"])
        self.theme_layout.addWidget(margin_theme_label)
        self.theme_layout.addWidget(self.margin_theme_input)

        # Lines Background
        lines_theme_label = QLabel("Line Number Background:")
        self.lines_theme_input = QLineEdit()
        self.lines_theme_input.setText(self._window._themes["lines_theme"])
        self.editor_layout.addWidget(lines_theme_label)
        self.editor_layout.addWidget(self.lines_theme_input)

        # Lines Foreground
        lines_fg_label = QLabel("Line Number Foreground:")
        self.lines_fg_input = QLineEdit()
        self.lines_fg_input.setText(self._window._themes["lines_fg"])
        self.editor_layout.addWidget(lines_fg_label)
        self.editor_layout.addWidget(self.lines_fg_input)

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
        self.editor_layout.addWidget(font_theme_label)
        self.editor_layout.addWidget(self.font_theme_combobox)

        # Save Button
        save_button = QPushButton("Apply")
        # Use theme-aware colors
        theme_type = self._window._themes.get("theme_type", "dark")
        if theme_type == "light":
            button_bg = "#e0e0e0"
            button_color = "#000000"
        else:
            button_bg = "#121212"
            button_color = "#ffffff"
        save_button.setStyleSheet(
            f"QPushButton {{"
            f"   border-radius: 10px;"
            f"   padding: 5px;"
            f"background-color: {button_bg};"
            f"color: {button_color};"
            f"}}"
        )
        save_button.clicked.connect(self.save_json)

        # Add theme_grouping to the scroll layout
        self.scroll_layout.addWidget(self.theme_grouping)
        self.scroll_layout.addWidget(self.editor_grouping)
        self.scroll_layout.addWidget(save_button)

        # Set the scroll widget and add scroll area to main layout
        self.scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(self.scroll_area)

    def save_json(self):
        self._window._themes["theme"] = self.theme_input.text()
        self._window._themes["editor_theme"] = self.editor_theme_input.text()
        self._window._themes["titlebar"] = (self.titlebar.currentText().lower())
        self._window._themes["margin_theme"] = self.margin_theme_input.text()
        self._window._themes["sidebar_bg"] = self.sidebar_theme_input.text()
        self._window._themes["menubar_bg"] = self.menubar_theme_input.text()
        self._window._themes["lines_theme"] = self.lines_theme_input.text()
        self._window._themes["lines_fg"] = self.lines_fg_input.text()
        self._window._themes["font"] = self.font_theme_combobox.currentText()
        self._window._themes["theme_type"] = self.theme_combobox.currentText()
        self._window._themes["material_type"] = self.materialconfig_combobox.currentText()

        if self.theming_combobox.currentText() == "Flat (Default)":
            self._window._themes["theming"] = "flat"
        else:
            self._window._themes["theming"] = "material"

        with open(f"{self._window.local_app_data}/data/theme.json", "w") as json_file:
            json.dump(self._window._themes, json_file)

        QMessageBox.information(
            self,
            "Settings Applied!",
            "The chosen settings have been applied. Restart Aura Text to see the changes.",
        )

    def material_theme_settings(self):
        self.materialconfig_label = QLabel("Material Theme Type")
        self.materialconfig_combobox = QComboBox()
        self.materialconfig_combobox.setCurrentText(self._window._themes["material_type"])
        theme_opt = ['dark_amber',
                     'dark_blue',
                     'dark_cyan',
                     'dark_lightgreen',
                     'dark_pink',
                     'dark_purple',
                     'dark_red',
                     'dark_teal',
                     'dark_yellow',
                     'light_amber',
                     'light_blue',
                     'light_cyan',
                     'light_cyan_500',
                     'light_lightgreen',
                     'light_pink',
                     'light_purple',
                     'light_red',
                     'light_teal',
                     'light_yellow']
        self.materialconfig_combobox.addItems(theme_opt)
        self.theme_layout.addWidget(self.materialconfig_label)
        self.theme_layout.addWidget(self.materialconfig_combobox)

    def theming_shift(self):
        if self.theming_combobox.currentText() == "Material":
            self.material_theme_settings()
        else:
            self.materialconfig_label.hide()
            self.materialconfig_combobox.hide()

    # @staticmethod
    if platform.system() == "Windows":
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
    else:
        def get_installed_fonts(self):
            font_names = []
            return font_names
