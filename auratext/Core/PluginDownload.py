import os
import sys
import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QMessageBox, 
    QLineEdit, QHBoxLayout, QScrollArea, 
    QLabel, QFrame
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QBrush
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class ExtensionCard(QFrame):
    def __init__(self, name, description, plugin_type, parent_downloader=None):
        super().__init__(parent_downloader)
        self.name = name
        self.plugin_type = plugin_type  # "file" or "dir"
        self.parent_downloader = parent_downloader
        
        self.setFixedHeight(85)
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
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Icon Label
        self.icon_label = QLabel(self)
        self.icon_label.setFixedSize(48, 48)
        self.icon_label.setStyleSheet("background: transparent; border: none;")
        self.icon_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.set_default_icon()
        layout.addWidget(self.icon_label)
        
        # Info Layout
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        info_layout.setContentsMargins(0, 0, 0, 0)
        
        self.name_label = QLabel(name)
        self.name_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #cccccc; border: none; background: transparent;")
        self.name_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.desc_label = QLabel(description)
        self.desc_label.setStyleSheet("color: #888888; border: none; background: transparent; font-size: 11px;")
        self.desc_label.setWordWrap(True)
        self.desc_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.desc_label)
        layout.addLayout(info_layout)
        
        # Install Button
        self.install_btn = QPushButton("Install")
        self.install_btn.setFixedSize(70, 26)
        self.install_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.install_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                border-radius: 2px;
                font-size: 11px;
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
        
        # Load Icon
        self.load_icon()
        self.load_metadata()

    def set_default_icon(self):
        pixmap = QPixmap(48, 48)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        color = QColor("#007acc")
        painter.setPen(QPen(color, 1.5))
        painter.setBrush(QBrush(QColor(0, 122, 204, 30)))
        painter.drawRoundedRect(3, 3, 42, 42, 8, 8)
        
        painter.setBrush(QBrush(color))
        painter.drawRoundedRect(16, 16, 16, 16, 3, 3)
        
        painter.end()
        self.icon_label.setPixmap(pixmap)

    def load_icon(self):
        # 1. Try local icon if installed
        local_plugins_dir = os.path.join(self.parent_downloader._window.local_app_data, "plugins")
        if self.plugin_type == "dir":
            local_dir = os.path.join(local_plugins_dir, self.name)
            if os.path.isdir(local_dir):
                for ext in [".png", ".jpg", ".jpeg", ".svg"]:
                    icon_path = os.path.join(local_dir, f"icon{ext}")
                    if os.path.exists(icon_path):
                        pixmap = QPixmap(icon_path)
                        if not pixmap.isNull():
                            self.icon_label.setPixmap(pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                            return
            # If not local or no local icon, fetch from network
            icon_url = f"https://raw.githubusercontent.com/{self.parent_downloader.username}/{self.parent_downloader.repo}/main/Plugins/{self.name}/icon.png"
            self.parent_downloader.load_image_async(icon_url, self.on_icon_loaded)

    def on_icon_loaded(self, pixmap):
        if not pixmap.isNull():
            self.icon_label.setPixmap(pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def load_metadata(self):
        # 1. Try local metadata first if installed
        local_plugins_dir = os.path.join(self.parent_downloader._window.local_app_data, "plugins")
        local_file_path = os.path.join(local_plugins_dir, f"{self.name}.py")
        local_dir_path = os.path.join(local_plugins_dir, self.name)
        installed = os.path.exists(local_file_path) or os.path.isdir(local_dir_path)
        
        if installed:
            self.load_local_metadata()
            return
            
        # 2. Otherwise, fetch remote metadata from GitHub raw CDN (non-rate-limited)
        if self.plugin_type == "dir":
            data_json_url = f"https://raw.githubusercontent.com/{self.parent_downloader.username}/{self.parent_downloader.repo}/main/Plugins/{self.name}/data.json"
            self.parent_downloader.load_text_async(data_json_url, self.on_remote_data_json_loaded)
            
            # Optionally also try to load first line of README.md as backup description
            readme_url = f"https://raw.githubusercontent.com/{self.parent_downloader.username}/{self.parent_downloader.repo}/main/Plugins/{self.name}/README.md"
            self.parent_downloader.load_text_async(readme_url, self.on_remote_readme_loaded)
        else:
            py_url = f"https://raw.githubusercontent.com/{self.parent_downloader.username}/{self.parent_downloader.repo}/main/Plugins/{self.name}.py"
            self.parent_downloader.load_text_async(py_url, self.on_remote_py_loaded)

    def load_local_metadata(self):
        local_plugins_dir = os.path.join(self.parent_downloader._window.local_app_data, "plugins")
        local_dir = os.path.join(local_plugins_dir, self.name)
        legacy_file = os.path.join(local_plugins_dir, f"{self.name}.py")
        
        has_metadata = False
        
        if os.path.isdir(local_dir):
            # 1. Check data.json
            data_json_path = os.path.join(local_dir, "data.json")
            if os.path.exists(data_json_path):
                try:
                    import json
                    with open(data_json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if isinstance(data, dict):
                        if "name" in data:
                            self.name_label.setText(data["name"])
                            has_metadata = True
                        if "descr" in data:
                            self.desc_label.setText(data["descr"])
                except Exception as e:
                    print(f"Error parsing card data.json: {e}")
            
            # 2. Check README.md
            readme_md_path = os.path.join(local_dir, "README.md")
            if os.path.exists(readme_md_path):
                try:
                    with open(readme_md_path, "r", encoding="utf-8") as f:
                        readme = f.read().strip()
                    lines = [l.strip() for l in readme.split("\n") if l.strip() and not l.strip().startswith("#")]
                    if lines:
                        self.desc_label.setText(lines[0])
                except Exception as e:
                    print(f"Error reading card README.md: {e}")
        
        if not has_metadata:
            # Fallback to py AST parsing
            py_file_path = None
            if os.path.isdir(local_dir):
                py_files = [f for f in os.listdir(local_dir) if f.endswith(".py") and f != "__init__.py"]
                if py_files:
                    best_match = None
                    for py in py_files:
                        if py.lower() == f"{self.name.lower()}.py":
                            best_match = py
                            break
                    if not best_match:
                        best_match = py_files[0]
                    py_file_path = os.path.join(local_dir, best_match)
            elif os.path.exists(legacy_file):
                py_file_path = legacy_file
                
            if py_file_path and os.path.exists(py_file_path):
                try:
                    import ast
                    with open(py_file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    tree = ast.parse(content)
                    meta = {}
                    for node in tree.body:
                        if isinstance(node, ast.Assign):
                            for target in node.targets:
                                if isinstance(target, ast.Name) and target.id in ("__name__", "__author__", "__readme__"):
                                    value = node.value
                                    if isinstance(value, ast.Constant):
                                        meta[target.id] = value.value
                                    elif isinstance(value, ast.Str):
                                        meta[target.id] = value.s
                                        
                    if "__name__" in meta:
                        self.name_label.setText(meta["__name__"])
                    if "__readme__" in meta:
                        readme = meta["__readme__"].strip()
                        lines = [l.strip() for l in readme.split("\n") if l.strip() and not l.strip().startswith("#")]
                        if lines:
                            self.desc_label.setText(lines[0])
                except Exception as e:
                    print(f"Error loading local metadata fallback for card {self.name}: {e}")

    def on_remote_data_json_loaded(self, text):
        import json
        try:
            data = json.loads(text)
            if isinstance(data, dict):
                if "name" in data:
                    self.name_label.setText(data["name"])
                if "descr" in data:
                    self.desc_label.setText(data["descr"])
        except Exception as e:
            print(f"Error parsing remote data.json for card {self.name}: {e}")

    def on_remote_readme_loaded(self, text):
        try:
            lines = [l.strip() for l in text.split("\n") if l.strip() and not l.strip().startswith("#")]
            if lines and self.desc_label.text() == f"Extension for {self.name}":
                self.desc_label.setText(lines[0])
        except Exception as e:
            print(f"Error parsing remote readme for card {self.name}: {e}")

    def on_remote_py_loaded(self, text):
        try:
            import ast
            tree = ast.parse(text)
            meta = {}
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id in ("__name__", "__readme__"):
                            value = node.value
                            if isinstance(value, ast.Constant):
                                meta[target.id] = value.value
                            elif isinstance(value, ast.Str):
                                meta[target.id] = value.s
                                
            if "__name__" in meta:
                self.name_label.setText(meta["__name__"])
            if "__readme__" in meta:
                readme = meta["__readme__"].strip()
                lines = [l.strip() for l in readme.split("\n") if l.strip() and not l.strip().startswith("#")]
                if lines:
                    self.desc_label.setText(lines[0])
        except Exception as e:
            print(f"Error parsing remote py fallback for card {self.name}: {e}")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Only trigger details if not clicking the install button directly
            if not self.install_btn.geometry().contains(event.pos()):
                self.parent_downloader._window.open_plugin_details(self.name, self.plugin_type)
        super().mousePressEvent(event)


class FileDownloader(QWidget):
    def __init__(self, window):
        super().__init__()
        self._window = window
        self.username = "rohankishore"
        self.repo = "AuraText-Plugins"
        self.cards = []
        self._active_managers = []
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

    def load_image_async(self, url, callback):
        manager = QNetworkAccessManager(self)
        self._active_managers.append(manager)
        
        def handle_finished(reply):
            if reply.error() == QNetworkReply.NetworkError.NoError:
                data = reply.readAll()
                pixmap = QPixmap()
                if pixmap.loadFromData(data):
                    callback(pixmap)
            reply.deleteLater()
            if manager in self._active_managers:
                self._active_managers.remove(manager)
                
        manager.finished.connect(handle_finished)
        manager.get(QNetworkRequest(QUrl(url)))

    def load_text_async(self, url, callback):
        manager = QNetworkAccessManager(self)
        self._active_managers.append(manager)
        
        def handle_finished(reply):
            if reply.error() == QNetworkReply.NetworkError.NoError:
                data = reply.readAll().data().decode("utf-8")
                callback(data)
            reply.deleteLater()
            if manager in self._active_managers:
                self._active_managers.remove(manager)
                
        manager.finished.connect(handle_finished)
        manager.get(QNetworkRequest(QUrl(url)))

    def get_file_list(self):
        api_url = f"https://api.github.com/repos/{self.username}/{self.repo}/contents/Plugins"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                content = response.json()
                
                # Parse directory structure changes
                plugins_data = []
                for file_info in content:
                    if file_info["type"] == "dir":
                        plugins_data.append({"name": file_info["name"], "type": "dir"})
                    elif file_info["type"] == "file" and file_info["name"].endswith(".py"):
                        plugins_data.append({"name": file_info["name"].split(".")[0], "type": "file"})
                
                # Clear existing
                for i in reversed(range(self.container_layout.count())): 
                    widget = self.container_layout.itemAt(i).widget()
                    if widget:
                        widget.setParent(None)
                self.cards = []

                for p_data in plugins_data:
                    name = p_data["name"]
                    p_type = p_data["type"]
                    card = ExtensionCard(name, f"Extension for {name}", p_type, self)
                    card.install_btn.clicked.connect(
                        lambda _, n=name, t=p_type, btn=card.install_btn: self.download_plugin(n, t, btn)
                    )
                    self.container_layout.addWidget(card)
                    self.cards.append(card)

                self.update_install_buttons()
        except Exception as e:
            print(f"Error fetching extensions: {e}")

    def update_install_buttons(self):
        for card in self.cards:
            local_file_path = os.path.join(self._window.local_app_data, "plugins", f"{card.name}.py")
            local_dir_path = os.path.join(self._window.local_app_data, "plugins", card.name)
            installed = os.path.exists(local_file_path) or os.path.isdir(local_dir_path)
                
            if installed:
                card.install_btn.setText("Installed")
                card.install_btn.setDisabled(True)
            else:
                card.install_btn.setText("Install")
                card.install_btn.setDisabled(False)

    def download_plugin(self, file_name, plugin_type, button):
        if plugin_type == "file":
            selected_file = file_name + ".py"
            download_url = f"https://raw.githubusercontent.com/{self.username}/{self.repo}/main/Plugins/{selected_file}"
            try:
                response = requests.get(download_url)
                if response.status_code != 200:
                    # Fallback to master
                    download_url = f"https://raw.githubusercontent.com/{self.username}/{self.repo}/master/Plugins/{selected_file}"
                    response = requests.get(download_url)
                
                if response.status_code == 200:
                    local_file_path = os.path.join(self._window.local_app_data, "plugins", selected_file)
                    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                    with open(local_file_path, "wb") as f:
                        f.write(response.content)
                    
                    button.setText("Installed")
                    button.setDisabled(True)
                    QMessageBox.information(self, "Success", f"{file_name} installed successfully!")
                    self._window.load_plugins()
                else:
                    QMessageBox.critical(self, "Error", f"Failed to download: HTTP {response.status_code}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to download: {e}")
        else:
            # Directory-based plugin
            api_url = f"https://api.github.com/repos/{self.username}/{self.repo}/contents/Plugins/{file_name}"
            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    files = response.json()
                    local_dir = os.path.join(self._window.local_app_data, "plugins", file_name)
                    os.makedirs(local_dir, exist_ok=True)
                    
                    for f_info in files:
                        if f_info["type"] == "file":
                            f_name = f_info["name"]
                            f_download_url = f_info["download_url"]
                            f_response = requests.get(f_download_url)
                            if f_response.status_code == 200:
                                with open(os.path.join(local_dir, f_name), "wb") as f:
                                    f.write(f_response.content)
                    
                    button.setText("Installed")
                    button.setDisabled(True)
                    QMessageBox.information(self, "Success", f"{file_name} installed successfully!")
                    self._window.load_plugins()
                else:
                    QMessageBox.critical(self, "Error", f"Failed to fetch directory contents: HTTP {response.status_code}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to download folder: {e}")
