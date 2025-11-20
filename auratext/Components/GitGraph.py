
import subprocess
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QRadioButton, QHBoxLayout, QGroupBox
from PyQt6.QtGui import QFont

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

        self.refresh_graph()

    def refresh_graph(self):
        try:
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

