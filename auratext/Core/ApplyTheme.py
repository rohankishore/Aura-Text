from PyQt6.QtWidgets import QMainWindow, QPushButton, QFileDialog
import json


class ApplyTheme(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Replace App")

        self.button = QPushButton("Replace JSON File", self)
        self.button.setGeometry(50, 50, 200, 30)
        self.button.clicked.connect(self.replace_file_contents)

    def replace_file_contents(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select JSON File", "", "JSON Files (*.json)")

        if file_path:
            new_contents = {
                "message": "This content has been replaced."
            }

            try:
                with open(file_path, "w") as json_file:
                    json.dump(new_contents, json_file, indent=4)
                print("File contents replaced successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")