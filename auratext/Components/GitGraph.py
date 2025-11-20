import subprocess
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QRadioButton, QHBoxLayout, QGroupBox, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

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

        self.refresh_graph()

    def refresh_graph(self):
        try:
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
