import json
import os
import sys

from PyQt6.QtWidgets import (
    QLabel,
    QCheckBox,
    QPushButton,
    QVBoxLayout,
    QDialog,
    QWidget,
    QMessageBox,
    QComboBox,
    QApplication,
)

local_app_data = os.path.join(os.getenv("LocalAppData"), "AuraText")


class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()

        with open(f"{local_app_data}/data/config.json", "r") as json_file:
            self._config = json.load(json_file)

        self.splash_status = self._config['splash']

        self._config = {
            "splash": "",
        }

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addSpacing(100)

        self.splash_checkbox = QCheckBox("Show Adaptive Splash Screens")
        self.splash_checkbox.setChecked(True) if self.splash_status == "True" else self.splash_checkbox.setChecked(
            False)

        layout.addWidget(self.splash_checkbox)

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
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.setWindowTitle("Settings Window")

    def save_settings(self):
        if self.splash_checkbox.isChecked():
            self.splash_status = "True"
        else:
            self.splash_status = "False"

            # Update the splash status in the existing configuration
        self._config["splash"] = self.splash_status

        # Save the updated configuration back to the JSON file
        with open(f"{local_app_data}/data/config.json", "w") as json_file:
            json.dump(self._config, json_file, indent=4)

        print(self.splash_status)

        # self._themes["editor_theme"] = self.editor_theme_input.isChecked()
        # self._themes["margin_theme"] = self.margin_theme_input.isChecked()
        # self._themes["lines_theme"] = self.lines_theme_input.isChecked()
        # self._themes["lines_fg"] = self.lines_fg_input.isChecked()
        # self._themes["font"] = self.font_theme_combobox.currentText()
        # self._themes["theme_type"] = self.theme_combobox.currentText()

        QMessageBox.information(
            self,
            "Settings Applied!",
            "The chosen settings have been applied.",
        )
