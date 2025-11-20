import os
import sys
import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QMessageBox, 
    QLineEdit, QHBoxLayout, QScrollArea, 
    QLabel, QFrame
)
from PyQt6.QtCore import Qt

class ExtensionCard(QFrame):
    def __init__(self, name, description, parent=None):
        super().__init__(parent)
        self.name = name
        self.setFixedHeight(80)
        self.setStyleSheet("""
            QFrame {
                background-color: #252526;
                border-radius: 5px;
                border: 1px solid #3e3e3e;
            }
            QFrame:hover {
                border-color: #007acc;
            }
        """)
        
        layout = QHBoxLayout(self)
        
        # Info
        info_layout = QVBoxLayout()
        name_label = QLabel(name)
        name_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #cccccc; border: none; background: transparent;")
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #888888; border: none; background: transparent;")
        desc_label.setWordWrap(True)
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(desc_label)
        layout.addLayout(info_layout)
        
        # Install Button
        self.install_btn = QPushButton("Install")
        self.install_btn.setFixedSize(80, 30)
        self.install_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.install_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                border-radius: 2px;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
            QPushButton:disabled {
                background-color: #3e3e3e;
                color: #888888;
            }
        """)
        layout.addWidget(self.install_btn)

class FileDownloader(QWidget):
    def __init__(self, window):
        super().__init__()
        self._window = window
        self.username = "rohankishore"
        self.repo = "AuraText-Plugins"
        self.cards = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Search Header
        header = QWidget()
        header.setStyleSheet("background-color: #252526; padding: 10px;")
        header_layout = QVBoxLayout(header)
        
        title = QLabel("EXTENSIONS")
        title.setStyleSheet("font-weight: bold; color: #bbbbbb;")
        header_layout.addWidget(title)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Extensions...")
        self.search_input.textChanged.connect(self.filter_list)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #3c3c3c;
                color: #cccccc;
                border: 1px solid #3c3c3c;
                padding: 5px;
            }
            QLineEdit:focus {
                border-color: #007acc;
            }
        """)
        header_layout.addWidget(self.search_input)
        layout.addWidget(header)
        
        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background-color: #1e1e1e;")
        
        self.container = QWidget()
        self.container.setStyleSheet("background-color: #1e1e1e;")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.container_layout.setSpacing(10)
        self.container_layout.setContentsMargins(10, 10, 10, 10)
        
        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)

        # Load extensions
        self.get_file_list()

    def filter_list(self, text):
        for card in self.cards:
            if text.lower() in card.name.lower():
                card.show()
            else:
                card.hide()

    def get_file_list(self):
        api_url = f"https://api.github.com/repos/{self.username}/{self.repo}/contents/Plugins"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                content = response.json()
                files_info = [file["name"].split(".")[0] for file in content if file["type"] == "file"]
                
                # Clear existing
                for i in reversed(range(self.container_layout.count())): 
                    self.container_layout.itemAt(i).widget().setParent(None)
                self.cards = []

                for file_info in files_info:
                    # Description is hardcoded for now as API doesn't provide it easily without extra calls
                    card = ExtensionCard(file_info, f"Extension for {file_info}")
                    card.install_btn.clicked.connect(lambda _, name=file_info, btn=card.install_btn: self.download_file(name, btn))
                    self.container_layout.addWidget(card)
                    self.cards.append(card)

                self.update_install_buttons()
        except Exception as e:
            print(f"Error fetching extensions: {e}")

    def update_install_buttons(self):
        for card in self.cards:
            selected_file = card.name + ".py"
            local_file_path = os.path.join(self._window.local_app_data, "plugins", selected_file)
            if os.path.exists(local_file_path):
                card.install_btn.setText("Installed")
                card.install_btn.setDisabled(True)

    def download_file(self, file_name, button):
        selected_file = file_name + ".py"
        download_url = f"https://raw.githubusercontent.com/{self.username}/{self.repo}/master/Plugins/{selected_file}"
        try:
            response = requests.get(download_url)
            if response.status_code == 200:
                local_file_path = os.path.join(self._window.local_app_data, "plugins", selected_file)
                with open(local_file_path, "wb") as f:
                    f.write(response.content)
                
                button.setText("Installed")
                button.setDisabled(True)
                QMessageBox.information(self, "Success", f"{file_name} installed successfully!")
                self._window.load_plugins()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download: {e}")
