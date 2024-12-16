import os
import sys
import csv
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QListWidget, QPushButton, QHBoxLayout, QMessageBox, QDialog, QLineEdit
)
from PyQt6.QtCore import Qt

local_app_data = os.path.join(os.getenv("LocalAppData"), "AuraText")
cpath = open(f"{local_app_data}/data/CPath_Project.txt", "r+").read()


def check_folder_exists(folder_path):
    """Check if a folder exists in the specified directory."""
    if os.path.isdir(folder_path):
        print(f"The folder '{folder_path}' exists.")
        return True
    else:
        print(f"The folder '{folder_path}' does not exist.")
        return False


def create_folder(folder_path):
    """Create a folder inside a directory if it doesn't already exist."""
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"The folder '{folder_path}' was created (or already exists).")
    except Exception as e:
        print(f"Failed to create folder '{folder_path}': {e}")


if check_folder_exists(f"{cpath}/Aura Text/"):
    pass
else:
    create_folder(f"{cpath}/Aura Text")
# Path to the CSV file
CSV_FILE = f"{cpath}/Aura Text/todo.csv"


class ToDoApp(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("To-Do List")
        self.resize(400, 400)

        # Central widget setup

        # Layouts
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # List widget to display tasks
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        # Buttons for actions
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        self.mark_complete_button = QPushButton("Mark as Complete")
        self.mark_complete_button.clicked.connect(self.mark_as_complete)
        self.button_layout.addWidget(self.mark_complete_button)

        self.refresh_button = QPushButton("Refresh List")
        self.refresh_button.clicked.connect(self.load_tasks)
        self.button_layout.addWidget(self.refresh_button)

        # Input field for adding tasks
        self.add_task_layout = QHBoxLayout()
        self.layout.addLayout(self.add_task_layout)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task")
        self.add_task_layout.addWidget(self.task_input)

        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.add_task)
        self.add_task_layout.addWidget(self.add_task_button)

        # Load tasks from the CSV file
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from the CSV file into the list widget."""
        self.list_widget.clear()
        try:
            with open(CSV_FILE, "r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) != 2:
                        continue
                    task, status = row
                    display_text = f"{task} [{status}]"
                    self.list_widget.addItem(display_text)
        except FileNotFoundError:
            create_folder(f"{cpath}/Aura Text/")
            with open(CSV_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                # Add default rows or leave empty
                writer.writerow(["Task", "Status"])
                writer.writerow(["Sample Task 1", "Incomplete"])
                writer.writerow(["Sample Task 2", "Incomplete"])
            print(f"File created successfully.")

    def mark_as_complete(self):
        """Mark the selected task as complete and update the CSV file."""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a task to mark as complete.")
            return

        selected_task = selected_items[0].text()
        task_name = selected_task.split(" [")[0]  # Extract the task name

        updated_rows = []
        try:
            with open(CSV_FILE, "r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) != 2:
                        continue
                    task, status = row
                    if task == task_name:
                        updated_rows.append([task, "Complete"])
                    else:
                        updated_rows.append(row)

            with open(CSV_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)

            QMessageBox.information(self, "Success", f"Task '{task_name}' marked as complete.")

            # Refresh the list
            self.load_tasks()

        except FileNotFoundError:
            with open(CSV_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                # Add default rows or leave empty
                writer.writerow(["Task", "Status"])
                writer.writerow(["Sample Task 1", "Incomplete"])
                writer.writerow(["Sample Task 2", "Incomplete"])
            print(f"File created successfully.")

    def add_task(self):
        """Add a new task to the to-do list and update the CSV file."""
        task_name = self.task_input.text().strip()
        if not task_name:
            QMessageBox.warning(self, "Warning", "Task name cannot be empty.")
            return

        try:
            with open(CSV_FILE, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([task_name, "Incomplete"])

            QMessageBox.information(self, "Success", f"Task '{task_name}' added successfully.")

            # Clear the input field
            self.task_input.clear()

            # Refresh the list
            self.load_tasks()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add task: {e}")
