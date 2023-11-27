import os
import shutil
import sys
import requests
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QMessageBox,
    QLineEdit,
    QGroupBox,
    QHBoxLayout,
    QFormLayout,
    QScrollArea,
)


class ThemeDownloader(QWidget):
    def __init__(self, window):
        super().__init__()
        self._window = window
        self.search_input = QLineEdit(self)
        self.list_widget = QListWidget()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        search_group_box = QGroupBox("Search Extensions")
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        self.search_input.textChanged.connect(self.filter_list)
        search_group_box.setLayout(search_layout)
        layout.addWidget(search_group_box)

        # Extensions List
        extensions_group_box = QGroupBox("Available Extensions")
        extensions_layout = QFormLayout()
        extensions_group_box.setLayout(extensions_layout)

        extensions_scroll_area = QScrollArea()
        extensions_scroll_area.setWidgetResizable(True)
        extensions_scroll_area.setWidget(extensions_group_box)
        layout.addWidget(extensions_scroll_area)

        # Add the file list to the QListWidget
        self.get_theme_list()
        extensions_layout.addWidget(self.list_widget)

        self.setLayout(layout)
        self.setWindowTitle("Extensions Downloader")

    def filter_list(self, text):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item_text = item.text()
            if text.lower() in item_text.lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    username = "rohankishore"
    repo = "AuraText-Themes"

    def get_theme_list(self):
        api_url = f"https://api.github.com/repos/{self.username}/{self.repo}/contents/Themes"
        response = requests.get(api_url)
        if response.status_code == 200:
            content = response.json()
            files_info = [file["name"].split(".")[0] for file in content if file["type"] == "file"]
            self.list_widget.clear()
            for file_info in files_info:
                install_button = QPushButton("Install", self)
                install_button.setToolTip(f"Download '{file_info}'")
                install_button.clicked.connect(lambda _, name=file_info: self.download_theme(name))
                self.list_widget.addItem(file_info)
                self.list_widget.setItemWidget(
                    self.list_widget.item(self.list_widget.count() - 1), install_button
                )

    def download_theme(self, file_name):
        selected_file = file_name + ".json"
        download_url = f"https://raw.githubusercontent.com/{self.username}/{self.repo}/main/Themes/{selected_file}"
        response = requests.get(download_url)

        if response.status_code == 200:
            local_file_path = os.path.join(self._window.local_app_data, "plugins", selected_file)
            with open(local_file_path, "wb") as file:
                file.write(response.content)

            # Assuming you want to copy the downloaded file to "theme.json"
            theme_json_path = os.path.join(self._window.local_app_data, "data", "theme.json")
            shutil.copy(local_file_path, theme_json_path)

            QMessageBox.information(
                self,
                "Theme Downloaded",
                f"Theme '{selected_file}' has been applied successfully.",
            )

            # Update the Install button to "Installed" and disable it
            for i in range(self.list_widget.count()):
                item = self.list_widget.item(i)
                if item.text() == file_name:
                    button = self.list_widget.itemWidget(item)
                    button.setText("Installed")
                    button.setDisabled(True)
                    break
        else:
            QMessageBox.critical(
                self,
                "Download Failed",
                f"Failed to download theme '{selected_file}'.\nStatus Code: {response.status_code}\nContent: {response.content}",
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThemeDownloader()
    window.show()
    sys.exit(app.exec())
