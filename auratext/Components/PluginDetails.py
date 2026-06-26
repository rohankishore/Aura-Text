import os
import ast
import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTextBrowser, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap, QIcon, QPainter, QColor, QPen, QBrush
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class PluginDetailsWidget(QWidget):
    def __init__(self, plugin_name, plugin_type, window):
        super().__init__()
        self.plugin_name = plugin_name
        self.plugin_type = plugin_type
        self._window = window
        
        self.metadata = {
            "__name__": plugin_name,
            "__author__": "Unknown",
            "__readme__": "No readme details available."
        }
        
        self.init_ui()
        self.load_details()

    def init_ui(self):
        # Base style and background
        self.setStyleSheet("background-color: #1e1e1e;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header area frame
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #252526; 
                border-radius: 6px; 
                border: 1px solid #3e3e3e;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(15, 15, 15, 15)
        header_layout.setSpacing(15)
        
        # Icon label
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(64, 64)
        self.icon_label.setStyleSheet("background: transparent; border: none;")
        self.set_default_icon()
        header_layout.addWidget(self.icon_label)
        
        # Name and Author Layout
        info_layout = QVBoxLayout()
        self.name_label = QLabel(self.plugin_name)
        self.name_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff; background: transparent; border: none;")
        
        self.author_label = QLabel("By: Loading...")
        self.author_label.setStyleSheet("font-size: 13px; color: #888888; background: transparent; border: none;")
        
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.author_label)
        info_layout.addStretch()
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        
        # Action button
        self.action_btn = QPushButton("Install")
        self.action_btn.setFixedSize(120, 32)
        self.action_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.action_btn.clicked.connect(self.handle_action)
        header_layout.addWidget(self.action_btn)
        
        layout.addWidget(header_frame)
        
        # Separator Line
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #3e3e3e; max-height: 1px; border: none;")
        layout.addWidget(sep)
        
        # Markdown Browser (README)
        self.readme_browser = QTextBrowser()
        self.readme_browser.setStyleSheet("""
            QTextBrowser {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: none;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                line-height: 1.6;
            }
        """)
        layout.addWidget(self.readme_browser)
        
        self.update_action_button_style()

    def set_default_icon(self):
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        color = QColor("#007acc")
        painter.setPen(QPen(color, 2))
        painter.setBrush(QBrush(QColor(0, 122, 204, 30)))
        painter.drawRoundedRect(4, 4, 56, 56, 12, 12)
        
        painter.setBrush(QBrush(color))
        painter.drawRoundedRect(22, 22, 20, 20, 4, 4)
        
        painter.end()
        self.icon_label.setPixmap(pixmap)

    def is_installed(self):
        if self.plugin_type == "file":
            local_file = os.path.join(self._window.local_app_data, "plugins", f"{self.plugin_name}.py")
            return os.path.exists(local_file)
        else:
            local_dir = os.path.join(self._window.local_app_data, "plugins", self.plugin_name)
            return os.path.isdir(local_dir)

    def update_action_button_style(self):
        if self.is_installed():
            self.action_btn.setText("Uninstall")
            self.action_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3e3e3e;
                    color: #cccccc;
                    border: 1px solid #5e5e5e;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #4e4e4e;
                    color: white;
                }
            """)
        else:
            self.action_btn.setText("Install")
            self.action_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0e639c;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1177bb;
                }
            """)

    def handle_action(self):
        if self.is_installed():
            # Uninstall logic
            try:
                if self.plugin_type == "file":
                    local_file = os.path.join(self._window.local_app_data, "plugins", f"{self.plugin_name}.py")
                    if os.path.exists(local_file):
                        os.remove(local_file)
                else:
                    local_dir = os.path.join(self._window.local_app_data, "plugins", self.plugin_name)
                    if os.path.isdir(local_dir):
                        import shutil
                        shutil.rmtree(local_dir)
                
                self._window.load_plugins()
                self.update_action_button_style()
                
                # Update sidebar install buttons if open
                if hasattr(self._window, "plugin_widget") and self._window.plugin_widget:
                    self._window.plugin_widget.update_install_buttons()
                    
                QMessageBox.information(self, "Success", f"{self.plugin_name} uninstalled successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to uninstall plugin: {e}")
        else:
            # Install logic
            if hasattr(self._window, "plugin_widget") and self._window.plugin_widget:
                downloader = self._window.plugin_widget
                self.action_btn.setText("Installing...")
                self.action_btn.setDisabled(True)
                
                # Download plugin using downloader logic
                downloader.download_plugin(self.plugin_name, self.plugin_type, self.action_btn)
                
                self.action_btn.setDisabled(False)
                self.update_action_button_style()
                downloader.update_install_buttons()
            else:
                QMessageBox.critical(self, "Error", "Extensions manager is not initialized.")

    def load_details(self):
        if self.is_installed():
            self.load_local_details()
        else:
            self.load_remote_details()

    def load_local_details(self):
        local_plugins_dir = os.path.join(self._window.local_app_data, "plugins")
        
        py_file_path = None
        icon_path = None
        
        if self.plugin_type == "file":
            py_file_path = os.path.join(local_plugins_dir, f"{self.plugin_name}.py")
        else:
            local_dir = os.path.join(local_plugins_dir, self.plugin_name)
            if os.path.isdir(local_dir):
                # Search for icon
                for ext in [".png", ".jpg", ".jpeg", ".svg"]:
                    p = os.path.join(local_dir, f"icon{ext}")
                    if os.path.exists(p):
                        icon_path = p
                        break
                
                # Search for .py file inside folder
                py_files = [f for f in os.listdir(local_dir) if f.endswith(".py") and f != "__init__.py"]
                if py_files:
                    best_match = None
                    for py in py_files:
                        if py.lower() == f"{self.plugin_name.lower()}.py":
                            best_match = py
                            break
                    if not best_match:
                        best_match = py_files[0]
                    py_file_path = os.path.join(local_dir, best_match)

        if py_file_path and os.path.exists(py_file_path):
            try:
                with open(py_file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                meta = self.extract_metadata_from_code(content)
                self.metadata.update(meta)
            except Exception as e:
                print(f"Error reading local plugin details: {e}")
        
        self.apply_metadata_to_ui()
        
        if icon_path:
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                self.icon_label.setPixmap(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def load_remote_details(self):
        username = "rohankishore"
        repo = "AuraText-Plugins"
        
        self.author_label.setText("By: Loading from GitHub...")
        self.readme_browser.setHtml("<p style='color: #888888;'>Loading plugin details...</p>")
        
        if self.plugin_type == "file":
            download_url = f"https://raw.githubusercontent.com/{username}/{repo}/main/Plugins/{self.plugin_name}.py"
            self.fetch_py_and_parse(download_url)
        else:
            api_url = f"https://api.github.com/repos/{username}/{repo}/contents/Plugins/{self.plugin_name}"
            
            self.manager = QNetworkAccessManager(self)
            self.manager.finished.connect(self.on_dir_contents_fetched)
            self.manager.get(QNetworkRequest(QUrl(api_url)))

    def on_dir_contents_fetched(self, reply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            import json
            try:
                files = json.loads(reply.readAll().data().decode("utf-8"))
                py_url = None
                icon_url = None
                
                for f in files:
                    if f["type"] == "file":
                        name = f["name"]
                        if name.endswith(".py") and name != "__init__.py":
                            if not py_url or name.lower() == f"{self.plugin_name.lower()}.py":
                                py_url = f["download_url"]
                        elif name.lower() in ("icon.png", "icon.jpg", "icon.jpeg", "icon.svg"):
                            icon_url = f["download_url"]
                
                if py_url:
                    self.fetch_py_and_parse(py_url)
                else:
                    self.author_label.setText("By: Unknown")
                    self.readme_browser.setMarkdown("No Python code file found in this plugin folder.")
                
                if icon_url:
                    self.fetch_and_set_icon(icon_url)
            except Exception as e:
                self.author_label.setText("By: Unknown")
                self.readme_browser.setMarkdown(f"Failed to parse directory contents: {e}")
        else:
            self.author_label.setText("By: Unknown")
            self.readme_browser.setMarkdown("Failed to fetch folder contents from GitHub API. Please check your internet connection.")
        reply.deleteLater()

    def fetch_py_and_parse(self, url):
        self.py_manager = QNetworkAccessManager(self)
        self.py_manager.finished.connect(self.on_py_fetched)
        self.py_manager.get(QNetworkRequest(QUrl(url)))

    def on_py_fetched(self, reply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            try:
                content = reply.readAll().data().decode("utf-8")
                meta = self.extract_metadata_from_code(content)
                self.metadata.update(meta)
                self.apply_metadata_to_ui()
            except Exception as e:
                print(f"Error parsing fetched py content: {e}")
        reply.deleteLater()

    def fetch_and_set_icon(self, url):
        self.icon_manager = QNetworkAccessManager(self)
        self.icon_manager.finished.connect(self.on_icon_fetched)
        self.icon_manager.get(QNetworkRequest(QUrl(url)))

    def on_icon_fetched(self, reply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            data = reply.readAll()
            pixmap = QPixmap()
            if pixmap.loadFromData(data):
                self.icon_label.setPixmap(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        reply.deleteLater()

    def extract_metadata_from_code(self, content):
        meta = {}
        try:
            tree = ast.parse(content)
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id in ("__name__", "__author__", "__readme__"):
                            value = node.value
                            if isinstance(value, ast.Constant):
                                meta[target.id] = value.value
                            elif isinstance(value, ast.Str):
                                meta[target.id] = value.s
        except Exception as e:
            print(f"AST parsing failed: {e}")
        return meta

    def apply_metadata_to_ui(self):
        name = self.metadata.get("__name__", self.plugin_name)
        self.name_label.setText(name)
        
        author = self.metadata.get("__author__", "Unknown")
        self.author_label.setText(f"By: {author}")
        
        readme = self.metadata.get("__readme__", "No description available.")
        self.readme_browser.setMarkdown(readme)
