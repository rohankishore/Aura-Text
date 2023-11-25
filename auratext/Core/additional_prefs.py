import json
import os

from PyQt6.QtWidgets import (
    QCheckBox,
    QPushButton,
    QVBoxLayout,
    QDialog,
    QMessageBox,
)

local_app_data = os.path.join(os.getenv("LocalAppData"), "AuraText")


class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()

        with open(f"{local_app_data}/data/config.json", "r") as json_file:
            self._config = json.load(json_file)

        self.splash_status = self._config['splash']
        self.terminaltips_status = self._config["terminal_tips"]

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

        self.ttips_checkbox = QCheckBox("Show Tips in Terminal")
        self.ttips_checkbox.setChecked(
            True) if self.terminaltips_status == "True" else self.ttips_checkbox.setChecked(
            False)

        layout.addWidget(self.splash_checkbox)
        layout.addWidget(self.ttips_checkbox)

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
        self.setWindowTitle("Additional Preferences")

    def save_settings(self):
        if self.splash_checkbox.isChecked():
            self.splash_status = "True"
        else:
            self.splash_status = "False"

        if self.ttips_checkbox.isChecked():
            self.terminaltips_status = "True"
        else:
            self.terminaltips_status = "False"


        config_data = {
            "splash": self.splash_status,
            "terminal_tips": self.terminaltips_status
        }

        with open(f"{local_app_data}/data/config.json", "w") as json_file:
            json.dump(config_data, json_file, indent=4)


        QMessageBox.information(
            self,
            "Settings Applied!",
            "The chosen settings have been applied.",
        )
