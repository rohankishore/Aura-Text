"""
This file is used for the breadcrumbs bar. It can be either turned on/off, and change positions to either on status bar at bottom or 
at the top of the editor.
"""

import os
import subprocess
import platform
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QCursor, QAction
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QMenu, QApplication

class BreadcrumbBar(QWidget):
    def __init__(self, parent_window, file_path="", is_status_bar=False):
        super().__init__(parent_window)
        self.window = parent_window
        self.file_path = file_path
        self.is_status_bar = is_status_bar
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 2, 5, 2)
        self.layout.setSpacing(4)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        self.update_theme()
        self.refresh()

    def update_theme(self):
        # Retrieve themes from parent window
        themes = getattr(self.window, "_themes", {})
        theme_type = themes.get("theme_type", "dark")
        
        if self.is_status_bar:
            self.bg_color = "transparent"
            self.text_color = "#FFFFFF"
            self.hover_bg = "rgba(255, 255, 255, 0.15)"
        else:
            if theme_type == "light":
                self.bg_color = "#f5f5f5"
                self.text_color = "#333333"
                self.hover_bg = "rgba(0, 0, 0, 0.08)"
            else:
                self.bg_color = "#252526"
                self.text_color = "#cccccc"
                self.hover_bg = "rgba(255, 255, 255, 0.08)"
                
        if not self.is_status_bar:
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: {self.bg_color};
                    border-bottom: 1px solid {themes.get('sidebar_bg', '#3c3c3c')};
                }}
            """)

    def set_file_path(self, file_path):
        self.file_path = file_path
        self.refresh()

    def refresh(self):
        # Clear existing layout items
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
                
        if not self.file_path:
            label = QLabel("Scratch")
            label.setStyleSheet(f"color: {self.text_color}; font-size: 11px; padding: 2px;")
            self.layout.addWidget(label)
            return

        # Determine segments
        project_path = getattr(self.window, "cpath", "")
        abs_path = os.path.abspath(self.file_path)
        normalized_abs = os.path.normpath(abs_path)
        
        segments = []
        paths_mapping = {}  # segment_index -> path up to that segment
        
        if project_path and normalized_abs.startswith(os.path.normpath(project_path)):
            proj_norm = os.path.normpath(project_path)
            relative = os.path.relpath(normalized_abs, proj_norm)
            proj_name = os.path.basename(proj_norm)
            
            segments.append(proj_name)
            paths_mapping[0] = proj_norm
            
            if relative != ".":
                parts = relative.split(os.sep)
                current_accumulated = proj_norm
                for idx, part in enumerate(parts):
                    current_accumulated = os.path.join(current_accumulated, part)
                    segments.append(part)
                    paths_mapping[len(segments) - 1] = current_accumulated
        else:
            # Absolute path split
            drive, path_tail = os.path.splitdrive(normalized_abs)
            parts = []
            if drive:
                parts.append(drive)
            parts.extend([p for p in path_tail.split(os.sep) if p])
            
            current_accumulated = drive + os.sep if drive else ""
            for idx, part in enumerate(parts):
                if idx == 0 and drive:
                    segments.append(part)
                    paths_mapping[0] = part + os.sep
                else:
                    current_accumulated = os.path.join(current_accumulated, part)
                    segments.append(part)
                    paths_mapping[len(segments) - 1] = current_accumulated

        for i, segment in enumerate(segments):
            # Create a button for each path segment
            btn = QPushButton(segment)
            btn.setFlat(True)
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            
            target_path = paths_mapping.get(i, self.file_path)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {self.text_color};
                    border: none;
                    border-radius: 3px;
                    padding: 2px 4px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: {self.hover_bg};
                }}
            """)
            
            # Left-click reveals in file explorer
            btn.clicked.connect(lambda checked=False, p=target_path: self.reveal_in_explorer(p))
            
            # Right-click context menu
            btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            btn.customContextMenuRequested.connect(lambda pos, p=target_path: self.show_context_menu(pos, p))
            
            self.layout.addWidget(btn)
            
            # Add chevron separator if not the last segment
            if i < len(segments) - 1:
                sep = QLabel("›")
                sep.setStyleSheet(f"color: {self.text_color}; font-size: 11px; font-weight: bold;")
                self.layout.addWidget(sep)
                
        self.layout.addStretch()

    def reveal_in_explorer(self, target_path):
        if not target_path:
            return
        
        target_path = os.path.normpath(target_path)
        system = platform.system()
        
        try:
            if system == "Windows":
                if os.path.isdir(target_path):
                    os.startfile(target_path)
                else:
                    subprocess.run(["explorer", "/select,", target_path])
            elif system == "Darwin":  # macOS
                if os.path.isdir(target_path):
                    subprocess.run(["open", target_path])
                else:
                    subprocess.run(["open", "-R", target_path])
            else:  # Linux
                parent_dir = target_path if os.path.isdir(target_path) else os.path.dirname(target_path)
                subprocess.run(["xdg-open", parent_dir])
        except Exception as e:
            print(f"Error revealing in explorer: {e}")

    def show_context_menu(self, pos, target_path):
        menu = QMenu(self)
        
        reveal_action = QAction("Reveal in File Explorer", self)
        reveal_action.triggered.connect(lambda: self.reveal_in_explorer(target_path))
        menu.addAction(reveal_action)
        
        copy_abs_action = QAction("Copy Absolute Path", self)
        copy_abs_action.triggered.connect(lambda: self.copy_to_clipboard(os.path.abspath(target_path)))
        menu.addAction(copy_abs_action)
        
        project_path = getattr(self.window, "cpath", "")
        if project_path:
            copy_rel_action = QAction("Copy Relative Path", self)
            rel_path = os.path.relpath(target_path, project_path)
            copy_rel_action.triggered.connect(lambda: self.copy_to_clipboard(rel_path))
            menu.addAction(copy_rel_action)
            
        menu.exec(QCursor.pos())

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
