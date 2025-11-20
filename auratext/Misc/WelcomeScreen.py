from __future__ import annotations
from typing import TYPE_CHECKING
import os

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon, QColor, QCursor
from PyQt6.QtWidgets import (
    QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QScrollArea, QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect
)

if TYPE_CHECKING:
    from auratext.Core.window import Window

class ModernButton(QPushButton):
    def __init__(self, text, icon_path=None, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(24, 24))
        
        self.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3e3e3e;
                border-radius: 8px;
                padding: 0px 20px;
                text-align: left;
                font-family: "Segoe UI", sans-serif;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3e3e3e;
                border-color: #505050;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #1a1a1a;
            }
        """)

class ProjectButton(QPushButton):
    def __init__(self, name, path, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(2)
        
        name_label = QLabel(name)
        name_label.setStyleSheet("color: #e0e0e0; font-weight: bold; font-size: 14px; background: transparent; border: none;")
        
        path_label = QLabel(path)
        path_label.setStyleSheet("color: #888888; font-size: 12px; background: transparent; border: none;")
        
        layout.addWidget(name_label)
        layout.addWidget(path_label)
        
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #2d2d2d;
            }
            QPushButton:pressed {
                background-color: #1a1a1a;
            }
        """)

class WelcomeWidget(QWidget):
    def __init__(self, window: Window):
        super().__init__()
        self.window = window
        self.setStyleSheet("background-color: #1e1e1e; color: #cccccc; font-family: 'Segoe UI', sans-serif;")
        
        # Main Layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(60, 60, 60, 60)
        main_layout.setSpacing(60)

        # Left Panel (Logo + Actions)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(30)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Logo/Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(15)
        
        logo_label = QLabel()
        pixmap = QPixmap(f"{window.local_app_data}/icons/splash_morning.png")
        if not pixmap.isNull():
            if pixmap.width() > 120:
                pixmap = pixmap.scaledToWidth(120, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        title_label = QLabel("Aura Text")
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #ffffff;")
        
        subtitle_label = QLabel("Code with clarity and speed.")
        subtitle_label.setStyleSheet("font-size: 18px; color: #888888;")

        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        left_layout.addLayout(header_layout)
        
        left_layout.addSpacing(20)

        # Actions
        actions_group = QWidget()
        actions_layout = QVBoxLayout(actions_group)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(15)
        
        start_label = QLabel("Start")
        start_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff; margin-bottom: 5px;")
        actions_layout.addWidget(start_label)

        btn_open = ModernButton("Open Folder...")
        btn_open.clicked.connect(window.open_project)
        
        btn_clone = ModernButton("Clone from Git...")
        btn_clone.clicked.connect(window.gitClone)
        
        actions_layout.addWidget(btn_open)
        actions_layout.addWidget(btn_clone)
        
        left_layout.addWidget(actions_group)
        left_layout.addStretch()
        
        # Right Panel (Recent Projects)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(20)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        recent_label = QLabel("Recent")
        recent_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        right_layout.addWidget(recent_label)
        
        # Scroll Area for projects
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        projects_container = QWidget()
        projects_container.setStyleSheet("background: transparent;")
        projects_layout = QVBoxLayout(projects_container)
        projects_layout.setContentsMargins(0, 0, 0, 0)
        projects_layout.setSpacing(5)
        projects_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Fetch projects
        try:
            window.dbcursor.execute("SELECT name, path FROM projects ORDER BY id DESC LIMIT 10")
            projects = window.dbcursor.fetchall()
            
            if not projects:
                no_projects = QLabel("No recent projects.")
                no_projects.setStyleSheet("color: #666666; font-size: 14px; margin-top: 10px;")
                projects_layout.addWidget(no_projects)
            else:
                for name, path in projects:
                    btn = ProjectButton(name, path)
                    # Use default argument to capture path correctly in the loop
                    btn.clicked.connect(lambda checked, p=path: self.open_recent_project(p))
                    projects_layout.addWidget(btn)
                    
        except Exception as e:
            err_label = QLabel(f"Could not load recent projects.")
            err_label.setStyleSheet("color: #ff5555;")
            projects_layout.addWidget(err_label)

        projects_layout.addStretch()
        scroll.setWidget(projects_container)
        right_layout.addWidget(scroll)

        # Add panels to main layout
        main_layout.addWidget(left_panel, 4)
        
        # Vertical separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setStyleSheet("background-color: #333333; width: 1px;")
        main_layout.addWidget(line)
        
        main_layout.addWidget(right_panel, 6)

    def open_recent_project(self, path):
        if not os.path.exists(path):
            # Maybe show a toast or message that path doesn't exist
            return
            
        with open(f"{self.window.local_app_data}/data/CPath_Project.txt", "w") as file:
            file.write(path)
            
        self.window.treeview_project(path)
        
        # Close this welcome tab
        index = self.window.tab_widget.indexOf(self)
        if index != -1:
            self.window.tab_widget.removeTab(index)
