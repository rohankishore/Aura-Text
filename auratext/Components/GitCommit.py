import subprocess
import os
import json
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import (QListWidget, QVBoxLayout, QWidget, QDockWidget, QPushButton, 
                             QListWidgetItem, QCheckBox, QMessageBox, QTextEdit, QLabel, 
                             QHBoxLayout, QFrame, QScrollArea)
import platform


if platform.system() == "Windows":
    local_app_data = os.getenv('LOCALAPPDATA')
elif platform.system() == "Linux":
    local_app_data = os.path.expanduser("~/.config")
elif platform.system() == "Darwin":
    local_app_data = os.path.expanduser("~/Library/Application Support")
else:
    print("Unsupported operating system")
    sys.exit(1)
local_app_data = os.path.join(local_app_data, "AuraText")
cpath = open(f"{local_app_data}/data/CPath_Project.txt", "r+").read()

# Load theme
with open(f"{local_app_data}/data/theme.json", "r") as f:
    theme_data = json.load(f)
    theme_color = theme_data.get("theme", "#007acc")
    bg_color = theme_data.get("sidebar_bg", "#1e1e1e")
    editor_bg = theme_data.get("editor_theme", "#121212")
    fg_color = theme_data.get("editor_fg", "#ffffff")

class GitCommitDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__('Source Control', parent)
        self.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        changed_files = self.list_changed_files()

        self.visibilityChanged.connect(
            lambda visible: parent.onCommitDockVisibilityChanged(visible)
        )

        if changed_files != []:
            # Header
            header = QLabel("SOURCE CONTROL")
            header.setStyleSheet(f"""
                QLabel {{
                    background-color: {bg_color};
                    color: {fg_color};
                    padding: 8px 12px;
                    font-size: 11px;
                    font-weight: normal;
                    letter-spacing: 0.5px;
                }}
            """)
            self.main_layout.addWidget(header)

            # Commit message section
            commit_container = QWidget()
            commit_container.setStyleSheet(f"background-color: {editor_bg};")
            commit_layout = QVBoxLayout(commit_container)
            commit_layout.setContentsMargins(8, 8, 8, 8)
            commit_layout.setSpacing(8)

            self.commit_entry = QTextEdit()
            self.commit_entry.setPlaceholderText("Message (Ctrl+Enter to commit)")
            self.commit_entry.setMaximumHeight(80)
            self.commit_entry.setStyleSheet(f"""
                QTextEdit {{
                    background-color: {bg_color};
                    color: {fg_color};
                    border: 1px solid #3c3c3c;
                    border-radius: 2px;
                    padding: 6px;
                    font-size: 13px;
                }}
            """)
            
            # Install event filter for Ctrl+Enter
            self.commit_entry.installEventFilter(self)

            # Commit button (VS Code style)
            self.commit_button = QPushButton('✓ Commit')
            self.commit_button.clicked.connect(self.commit_changes)
            self.commit_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme_color};
                    color: #ffffff;
                    border: none;
                    border-radius: 2px;
                    padding: 8px 16px;
                    font-size: 13px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: {self.adjust_color_brightness(theme_color, 1.1)};
                }}
                QPushButton:pressed {{
                    background-color: {self.adjust_color_brightness(theme_color, 0.9)};
                }}
            """)

            commit_layout.addWidget(self.commit_entry)
            commit_layout.addWidget(self.commit_button)
            self.main_layout.addWidget(commit_container)

            # Changes section header
            changes_header = QWidget()
            changes_header.setStyleSheet(f"background-color: {bg_color};")
            changes_header_layout = QHBoxLayout(changes_header)
            changes_header_layout.setContentsMargins(12, 6, 12, 6)
            
            changes_label = QLabel(f"CHANGES ({len(changed_files)})")
            changes_label.setStyleSheet(f"""
                QLabel {{
                    color: {fg_color};
                    font-size: 11px;
                    font-weight: bold;
                    letter-spacing: 0.5px;
                }}
            """)
            changes_header_layout.addWidget(changes_label)
            changes_header_layout.addStretch()
            
            self.main_layout.addWidget(changes_header)

            # File list
            self.file_list_widget = QListWidget()
            self.file_list_widget.setStyleSheet(f"""
                QListWidget {{
                    background-color: {editor_bg};
                    border: none;
                    outline: none;
                }}
                QListWidget::item {{
                    padding: 4px 12px;
                    border: none;
                }}
                QListWidget::item:hover {{
                    background-color: {self.adjust_color_brightness(editor_bg, 1.2)};
                }}
                QCheckBox {{
                    color: {fg_color};
                    spacing: 8px;
                }}
            """)
            self.populate_file_list()
            self.main_layout.addWidget(self.file_list_widget)
        else:
            # Empty state
            empty_container = QWidget()
            empty_layout = QVBoxLayout(empty_container)
            empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.pic_label = QLabel()
            photo = QPixmap(f"{local_app_data}/icons/no_commits.png")
            self.pic_label.setPixmap(photo)
            self.pic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_layout.addWidget(self.pic_label)
            
            self.main_layout.addWidget(empty_container)
            self.main_layout.addStretch(1)

        self.setWidget(self.main_widget)

    def eventFilter(self, obj, event):
        """Handle Ctrl+Enter to commit"""
        if obj == self.commit_entry and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                self.commit_changes()
                return True
        return super().eventFilter(obj, event)

    def adjust_color_brightness(self, hex_color, factor):
        """Adjust color brightness by factor"""
        try:
            hex_color = hex_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            r = min(255, int(r * factor))
            g = min(255, int(g * factor))
            b = min(255, int(b * factor))
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return hex_color

    def get_file_status(self, status_line):
        """Parse git status code to readable format"""
        if not status_line:
            return ""
        code = status_line[:2]
        status_map = {
            " M": "M",  # Modified
            "M ": "M",  # Modified (staged)
            "MM": "M",  # Modified (staged and unstaged)
            "A ": "A",  # Added
            "D ": "D",  # Deleted
            " D": "D",  # Deleted (unstaged)
            "R ": "R",  # Renamed
            "C ": "C",  # Copied
            "??": "U",  # Untracked
        }
        return status_map.get(code.strip() or code, "M")

    def populate_file_list(self):
        self.file_list_widget.clear()
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  cwd=cpath, text=True)
            if result.returncode != 0:
                return
                
            files = result.stdout.strip().split('\n')
            for line in files:
                if not line:
                    continue
                    
                status = self.get_file_status(line)
                file_path = line[3:]  # Skip status codes
                file_name = os.path.basename(file_path)
                full_path = os.path.abspath(os.path.join(cpath, file_path))
                
                item = QListWidgetItem(self.file_list_widget)
                
                # Create checkbox with file status indicator
                checkbox = QCheckBox(f"{status}  {file_name}")
                checkbox.setProperty("full_path", full_path)
                checkbox.setStyleSheet(f"""
                    QCheckBox {{
                        color: {fg_color};
                        font-size: 13px;
                    }}
                    QCheckBox::indicator {{
                        width: 16px;
                        height: 16px;
                    }}
                """)
                
                self.file_list_widget.addItem(item)
                self.file_list_widget.setItemWidget(item, checkbox)
        except Exception as e:
            print(f"Error populating file list: {e}")

    def list_changed_files(self):
        try:
            result = subprocess.run(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                raise FileNotFoundError("Git command not found. Ensure that Git is installed and added to the PATH.")

            result = subprocess.run(['git', 'status', '--porcelain'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    cwd=cpath)
            if result.returncode != 0:
                raise FileNotFoundError(f"Git status command failed with error: {result.stderr.decode('utf-8')}")

            files = result.stdout.decode('utf-8').split('\n')
            changed_files = [os.path.abspath(os.path.join(cpath, line[3:])) for line in files if line]
            return changed_files
        except FileNotFoundError as e:
            QMessageBox.critical(self, "Error", str(e))
            return []
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", str(e))
            return []

    def commit_changes(self):
        selected_files = []
        for index in range(self.file_list_widget.count()):
            item = self.file_list_widget.item(index)
            checkbox = self.file_list_widget.itemWidget(item)
            if checkbox.isChecked():
                selected_files.append(checkbox.property("full_path"))

        if not selected_files:
            QMessageBox.warning(self, 'No Files Selected', 
                              'Please select at least one file to commit.')
            return

        # Get commit message
        commit_msg = self.commit_entry.toPlainText().strip()
        if not commit_msg:
            QMessageBox.warning(self, 'No Commit Message', 
                              'Please enter a commit message.')
            return

        # Remove leading path from file paths to make them relative to repo
        relative_files = [os.path.relpath(file, cpath) for file in selected_files]

        try:
            # Stage selected files for commit
            subprocess.run(['git', 'add'] + relative_files, cwd=cpath, check=True)

            # Commit the changes
            result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                                  cwd=cpath, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                # Clear commit message and refresh file list
                self.commit_entry.clear()
                self.populate_file_list()
                
                # Show success message (VS Code-style)
                file_count = len(selected_files)
                QMessageBox.information(self, 'Commit Successful', 
                                      f'Successfully committed {file_count} file(s).')
            else:
                QMessageBox.warning(self, 'Commit Failed', 
                                  f"Git returned an error:\n{result.stderr}")

        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, 'Error', 
                               f"Failed to execute git command:\n{e}")
        except Exception as e:
            QMessageBox.critical(self, 'Error', 
                               f"An unexpected error occurred:\n{e}")
