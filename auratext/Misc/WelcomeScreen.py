from __future__ import annotations
from typing import TYPE_CHECKING
import json
import webbrowser

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QCursor
from PyQt6.QtWidgets import (QPushButton, QWidget, QVBoxLayout, QLabel, 
                             QHBoxLayout, QScrollArea, QFrame)


if TYPE_CHECKING:
    from auratext.Core.window import Window


class ActionButton(QPushButton):
    """VS Code-style action button"""
    def __init__(self, icon_text, label_text, theme_color, parent=None):
        super().__init__(parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setText(f"{icon_text}  {label_text}")
        self.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 8px 12px;
                border: none;
                background: transparent;
                color: {theme_color};
                font-size: 13px;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.05);
            }}
        """)


class WalkthroughCard(QFrame):
    """VS Code-style walkthrough card"""
    def __init__(self, title, description, theme_color, badge=None, progress=None, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # Title row with badge
        title_row = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: #cccccc;
                font-size: 13px;
                font-weight: 500;
            }}
        """)
        title_row.addWidget(title_label)
        
        if badge:
            badge_label = QLabel(badge)
            badge_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {theme_color};
                    color: white;
                    padding: 2px 8px;
                    border-radius: 10px;
                    font-size: 10px;
                    font-weight: bold;
                }}
            """)
            title_row.addWidget(badge_label)
        
        title_row.addStretch()
        layout.addLayout(title_row)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 12px;
            }
        """)
        layout.addWidget(desc_label)
        
        # Progress bar if provided
        if progress is not None:
            progress_container = QWidget()
            progress_layout = QHBoxLayout(progress_container)
            progress_layout.setContentsMargins(0, 4, 0, 0)
            
            progress_bar = QFrame()
            progress_bar.setFixedHeight(3)
            progress_bar.setStyleSheet(f"""
                QFrame {{
                    background-color: #333333;
                    border-radius: 2px;
                }}
            """)
            
            filled_bar = QFrame(progress_bar)
            filled_bar.setFixedSize(int(progress_bar.width() * progress / 100), 3)
            filled_bar.setStyleSheet(f"""
                QFrame {{
                    background-color: {theme_color};
                    border-radius: 2px;
                }}
            """)
            
            progress_layout.addWidget(progress_bar)
            layout.addWidget(progress_container)
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #252526;
                border: 1px solid #333333;
                border-radius: 6px;
            }}
            QFrame:hover {{
                background-color: #2a2a2b;
                border-color: {theme_color};
            }}
        """)


class RecentProjectItem(QPushButton):
    """VS Code-style recent project item"""
    def __init__(self, name, path, theme_color, parent=None):
        super().__init__(parent)
        self.project_path = path
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        self.setText(f"{name}     {path}")
        self.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 6px 0px;
                border: none;
                background: transparent;
                color: {theme_color};
                font-size: 13px;
            }}
            QPushButton:hover {{
                text-decoration: underline;
            }}
        """)


class WelcomeWidget(QWidget):
    def __init__(self, window: Window):
        super().__init__()
        self.window = window
        
        # Load theme
        with open(f"{window.local_app_data}/data/theme.json", "r") as f:
            theme_data = json.load(f)
            theme_color = theme_data.get("theme", "#007ACC")
            bg_color = theme_data.get("editor_theme", "#1e1e1e")
        
        # Main scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        # Container widget
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(60, 40, 60, 40)
        main_layout.setSpacing(30)
        
        # Title Section
        title_label = QLabel("Aura Text")
        title_label.setFont(QFont("Segoe UI", 48, QFont.Weight.Light))
        title_label.setStyleSheet("color: #cccccc;")
        
        subtitle_label = QLabel("Like any text editor. Unlike any text editor")
        subtitle_label.setFont(QFont("Segoe UI", 16))
        subtitle_label.setStyleSheet("color: #888888; margin-bottom: 20px;")
        
        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        
        # Content Layout (Start + Walkthroughs side by side)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(60)
        
        # Left Column - Start Section
        start_column = QVBoxLayout()
        start_column.setSpacing(15)
        
        start_header = QLabel("Start")
        start_header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        start_header.setStyleSheet("color: #cccccc; margin-bottom: 5px;")
        start_column.addWidget(start_header)
        
        # Start actions
        new_file_btn = ActionButton("📄", "New File...", theme_color)
        new_file_btn.clicked.connect(window.cs_new_document)
        start_column.addWidget(new_file_btn)
        
        open_file_btn = ActionButton("📂", "Open File...", theme_color)
        open_file_btn.clicked.connect(window.open_document)
        start_column.addWidget(open_file_btn)
        
        open_folder_btn = ActionButton("📁", "Open Folder...", theme_color)
        open_folder_btn.clicked.connect(window.open_project)
        start_column.addWidget(open_folder_btn)
        
        clone_repo_btn = ActionButton("🔗", "Clone Git Repository...", theme_color)
        clone_repo_btn.clicked.connect(window.gitClone)
        start_column.addWidget(clone_repo_btn)
        
        new_project_btn = ActionButton("✨", "Create New Project...", theme_color)
        new_project_btn.clicked.connect(window.new_project)
        start_column.addWidget(new_project_btn)
        
        manage_projects_btn = ActionButton("📊", "Manage Projects...", theme_color)
        manage_projects_btn.clicked.connect(window.manageProjects)
        start_column.addWidget(manage_projects_btn)
        
        website_btn = ActionButton("🌐", "Visit Website", theme_color)
        website_btn.clicked.connect(lambda: webbrowser.open_new_tab("https://aura-text.netlify.app"))
        start_column.addWidget(website_btn)
        
        start_column.addStretch()
        content_layout.addLayout(start_column, 1)
        
        # Right Column - Walkthroughs
        walkthrough_column = QVBoxLayout()
        walkthrough_column.setSpacing(15)
        
        walkthrough_header = QLabel("Walkthroughs")
        walkthrough_header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        walkthrough_header.setStyleSheet("color: #cccccc; margin-bottom: 5px;")
        walkthrough_column.addWidget(walkthrough_header)
        
        # Walkthrough cards
        card1 = WalkthroughCard(
            "⭐ Get started with Aura Text",
            "Customize your editor, learn the basics, and start coding",
            theme_color,
            progress=60
        )
        card1.mousePressEvent = lambda e: window.getting_started()
        walkthrough_column.addWidget(card1)
        
        card2 = WalkthroughCard(
            "💡 Learn the Fundamentals",
            "Master keyboard shortcuts and essential features",
            theme_color
        )
        card2.mousePressEvent = lambda e: window.shortcuts()
        walkthrough_column.addWidget(card2)
        
        card3 = WalkthroughCard(
            "🐍 Get Started with Python Development",
            "Set up your Python environment and start coding",
            theme_color,
            badge="Popular"
        )
        card3.mousePressEvent = lambda e: webbrowser.open_new_tab("https://aura-text.netlify.app/docs.html")
        walkthrough_column.addWidget(card3)
        
        more_link = QPushButton("More...")
        more_link.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        more_link.clicked.connect(window.getting_started)
        more_link.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 8px 0px;
                border: none;
                background: transparent;
                color: {theme_color};
                font-size: 13px;
            }}
            QPushButton:hover {{
                text-decoration: underline;
            }}
        """)
        walkthrough_column.addWidget(more_link)
        
        walkthrough_column.addStretch()
        content_layout.addLayout(walkthrough_column, 1)
        
        main_layout.addLayout(content_layout)
        
        # Recent Projects Section
        recent_header = QLabel("Recent")
        recent_header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        recent_header.setStyleSheet("color: #cccccc; margin-top: 10px; margin-bottom: 5px;")
        main_layout.addWidget(recent_header)
        
        # Get recent projects from database
        recent_layout = QVBoxLayout()
        recent_layout.setSpacing(5)
        
        try:
            cursor = window.dbcursor
            cursor.execute('SELECT name, path FROM projects ORDER BY id DESC LIMIT 5')
            projects = cursor.fetchall()
            
            if projects:
                for name, path in projects:
                    project_item = RecentProjectItem(name, path, theme_color)
                    project_item.clicked.connect(lambda checked, p=path: self.open_recent_project(p))
                    recent_layout.addWidget(project_item)
            else:
                no_recent = QLabel("No recent projects")
                no_recent.setStyleSheet("color: #888888; font-size: 13px; padding: 6px 0px;")
                recent_layout.addWidget(no_recent)
        except Exception as e:
            print(f"Error loading recent projects: {e}")
        
        more_recent = QPushButton("More...")
        more_recent.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        more_recent.clicked.connect(window.manageProjects)
        more_recent.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 6px 0px;
                border: none;
                background: transparent;
                color: {theme_color};
                font-size: 13px;
            }}
            QPushButton:hover {{
                text-decoration: underline;
            }}
        """)
        recent_layout.addWidget(more_recent)
        
        main_layout.addLayout(recent_layout)
        main_layout.addStretch()
        
        # Set container to scroll area
        scroll.setWidget(container)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)
        
        self.setStyleSheet(f"QWidget {{ background-color: {bg_color}; }}")
    
    def open_recent_project(self, path):
        """Open a recent project"""
        import os
        with open(f"{self.window.local_app_data}/data/CPath_Project.txt", "w") as file:
            file.write(path)
        self.window.treeview_project(path)
        
        # Close welcome tab
        for i in range(self.window.tab_widget.count()):
            if self.window.tab_widget.tabText(i) == "Welcome":
                self.window.tab_widget.removeTab(i)
                break
