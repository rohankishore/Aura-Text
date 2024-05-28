import os

from PyQt6.QtWidgets import (
    QMainWindow,
    QInputDialog,
    QDockWidget,
    QTreeView,
    QFileDialog,
    QSplashScreen,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QStatusBar,
    QListWidget,
    QLabel,
    QDialog)

local_app_data = os.path.join(os.getenv("LocalAppData"), "AuraText")

class BoilerPlate(QDialog):
    def __init__(self, current_editor):
        super().__init__()
        self.setWindowTitle("Boilerplates")

        self.current_editor = current_editor

        # Create a layout for the dock widget
        dock_layout = QVBoxLayout()
        self.setLayout(dock_layout)
        # self.boilerplate_dock.setLayout(dock_layout)

        # Add a header label to the dock widget
        header_label = QLabel("Boilerplates")
        header_label.setStyleSheet("QLabel{font-size: 20px; font : Arial;}")
        dock_layout.addWidget(header_label)

        # Create a QListWidget for displaying file names
        self.boilerplate_list = QListWidget()
        dock_layout.addWidget(self.boilerplate_list)

        # Populate the QListWidget with file names
        directory = f"{local_app_data}/boilerplates"
        if os.path.exists(directory):
            try:
                for file_name in os.listdir(directory):
                    if os.path.isfile(os.path.join(directory, file_name)):
                        name, extension = os.path.splitext(file_name)
                        self.boilerplate_list.addItem(name)
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f"The directory '{directory}' does not exist.")

            # Connect the clicked signal to a custom slot method
            self.boilerplate_list.clicked.connect(self.on_item_clicked)

    def on_item_clicked(self, item):
        print("Function reached")
        selected_file = item.text()

        # Read the contents of the selected file
        file_path = os.path.join(local_app_data, "boilerplates", f"{selected_file}.txt")
        try:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                print(file_contents)
                self.current_editor.append(file_contents)
        except Exception as e:
            print(f"Error reading file: {e}")