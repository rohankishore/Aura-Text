from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QCheckBox, QFileDialog

class NewProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Project")

        self.layout = QVBoxLayout(self)

        # Project Name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Project Name")
        self.layout.addWidget(self.name_edit)

        # Project Path
        self.path_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Project Location")
        self.path_button = QPushButton("Browse...")
        self.path_button.clicked.connect(self.browse_path)
        self.path_layout.addWidget(self.path_edit)
        self.path_layout.addWidget(self.path_button)
        self.layout.addLayout(self.path_layout)

        # Create README
        self.readme_checkbox = QCheckBox("Create README.md")
        self.layout.addWidget(self.readme_checkbox)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.button_layout)

    def browse_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Project Location")
        if path:
            self.path_edit.setText(path)

    def get_project_details(self):
        return {
            "name": self.name_edit.text(),
            "path": self.path_edit.text(),
            "create_readme": self.readme_checkbox.isChecked()
        }
