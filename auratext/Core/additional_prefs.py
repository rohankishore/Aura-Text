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

        self.splash_checkbox = QCheckBox("Show Adaptive Splash Screens")
        self.expopen_checkbox = QCheckBox("Show Tips in Terminal")
        self.open_last_file_checkbox = QCheckBox("Open the last opened file at startup")
        self.ttips_checkbox = QCheckBox("Show Explorer on Startup")
        with open(f"{local_app_data}/data/config.json", "r") as json_file:
            self._config = json.load(json_file)

        self.splash_status = self._config['splash']
        self.terminaltips_status = self._config["terminal_tips"]
        self.exp_open_status = self._config["explorer_default_open"]
        self.file_open_status = self._config["open_last_file"]
        print(self.exp_open_status)

        self._config = {
            "splash": "",
        }

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addSpacing(100)

        self.splash_checkbox.setChecked(True) if self.splash_status == "True" else self.splash_checkbox.setChecked(
            False)

        self.ttips_checkbox.setChecked(
            True) if self.terminaltips_status == "True" else self.ttips_checkbox.setChecked(
            False)

        self.ttips_checkbox.setChecked(
            True) if self.terminaltips_status == "True" else self.ttips_checkbox.setChecked(
            False)

        self.expopen_checkbox.setChecked(
            True) if self.exp_open_status == "True" else self.expopen_checkbox.setChecked(
            False)

        layout.addWidget(self.splash_checkbox)
        layout.addWidget(self.ttips_checkbox)
        layout.addWidget(self.expopen_checkbox)
        layout.addWidget(self.open_last_file_checkbox)

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

        if self.expopen_checkbox.isChecked():
            self.exp_open_status = "True"
        elif not self.expopen_checkbox.isChecked():
            self.exp_open_status = "False"

        if self.open_last_file_checkbox.isChecked():
            self.file_open_status = "True"
        else:
            self.file_open_status = "False"

        print(self.exp_open_status)

        config_data = {
            "splash": self.splash_status,
            "terminal_tips": self.terminaltips_status,
            "explorer_default_open": self.exp_open_status,
            "open_last_file": self.file_open_status
        }

        with open(f"{local_app_data}/data/config.json", "w") as json_file:
            json.dump(config_data, json_file, indent=4)

        QMessageBox.information(
            self,
            "Settings Applied!",
            "The chosen settings have been applied.",
        )
