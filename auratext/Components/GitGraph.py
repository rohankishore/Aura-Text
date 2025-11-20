<<<<<<< HEAD
import subprocess
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QRadioButton, QHBoxLayout, QGroupBox, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
=======

import subprocess
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QRadioButton, QHBoxLayout, QGroupBox
from PyQt6.QtGui import QFont
>>>>>>> 9c5dfeb38d1e23643306a10a1dfa851a280d2d52

class GitGraph(QWidget):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.setWindowTitle("Git History Graph")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create options
        options_group = QGroupBox("Options")
        options_layout = QHBoxLayout()
        self.all_branches_radio = QRadioButton("All Branches")
        self.current_branch_radio = QRadioButton("Current Branch")
        self.current_branch_radio.setChecked(True)
<<<<<<< HEAD
        
        self.all_branches_radio.toggled.connect(self.refresh_graph)
        self.current_branch_radio.toggled.connect(self.refresh_graph)

        options_layout.addWidget(self.all_branches_radio)
        options_layout.addWidget(self.current_branch_radio)
        options_group.setLayout(options_layout)
        self.layout.addWidget(options_group)

        # Graph display
        self.graph_display = QTextEdit()
        self.graph_display.setReadOnly(True)
        self.graph_display.setFont(QFont("Consolas", 10))
        self.graph_display.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4;")
        self.layout.addWidget(self.graph_display)

=======
        options_layout.addWidget(self.current_branch_radio)
        options_layout.addWidget(self.all_branches_radio)
        options_group.setLayout(options_layout)

        # Create text area for graph
        self.graph_display = QTextEdit()
        self.graph_display.setReadOnly(True)
        # Use a monospaced font for better graph alignment
        font = QFont("Courier New", 10)
        self.graph_display.setFont(font)

        self.layout.addWidget(options_group)
        self.layout.addWidget(self.graph_display)

        # Connect signals
        self.current_branch_radio.toggled.connect(self.refresh_graph)
        self.all_branches_radio.toggled.connect(self.refresh_graph)

>>>>>>> 9c5dfeb38d1e23643306a10a1dfa851a280d2d52
        self.refresh_graph()

    def refresh_graph(self):
        try:
<<<<<<< HEAD
            cmd = ["git", "log", "--graph", "--oneline", "--decorate", "--color=never"]
            if self.all_branches_radio.isChecked():
                cmd.append("--all")
            
            result = subprocess.run(
                cmd, 
                cwd=self.path, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode == 0:
                self.graph_display.setText(result.stdout)
            else:
                self.graph_display.setText(f"Error loading git graph:\n{result.stderr}")
        except Exception as e:
            self.graph_display.setText(f"Error executing git command:\n{str(e)}")
=======
            if self.all_branches_radio.isChecked():
                command = [
                    "git", "log", "--graph",
                    "--pretty=format:%C(yellow)%h%C(reset) -%C(auto)%d%C(reset) %s %C(green)(%cr) <%an>%C(reset)",
                    "--abbrev-commit", "--all"
                ]
            else:
                command = [
                    "git", "log", "--graph",
                    "--pretty=format:%C(yellow)%h%C(reset) -%C(auto)%d%C(reset) %s %C(green)(%cr) <%an>%C(reset)",
                    "--abbrev-commit"
                ]

            process = subprocess.run(
                command,
                cwd=self.path,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )

            if process.returncode == 0:
                self.graph_display.setText(process.stdout)
            else:
                self.graph_display.setText(f"Error fetching Git log:\n{process.stderr}")

        except FileNotFoundError:
            self.graph_display.setText("Git not found. Please ensure Git is installed and in your system's PATH.")
        except Exception as e:
            self.graph_display.setText(f"An error occurred: {e}")

>>>>>>> 9c5dfeb38d1e23643306a10a1dfa851a280d2d52
