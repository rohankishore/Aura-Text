import subprocess
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QListWidget, QVBoxLayout, QWidget, QDockWidget, QPushButton, QListWidgetItem, QCheckBox, \
    QMessageBox, QLineEdit, QLabel

local_app_data = os.path.join(os.getenv("LocalAppData"), "AuraText")
cpath = open(f"{local_app_data}/data/CPath_Project.txt", "r+").read()


class GitCommitDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__('Git Commit', parent)
        self.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)

        self.main_widget = QWidget()
        self.layout = QVBoxLayout(self.main_widget)

        changed_files = self.list_changed_files()

        self.visibilityChanged.connect(
            lambda visible: parent.onCommitDockVisibilityChanged(visible)
        )

        if changed_files != []:
            self.file_list_widget = QListWidget()
            self.populate_file_list()
            self.layout.addWidget(self.file_list_widget)

            self.commit_entry = QLineEdit()
            self.commit_entry.setPlaceholderText("Commit message")

            self.commit_button = QPushButton('Commit')
            self.commit_button.clicked.connect(self.commit_changes)

            self.layout.addWidget(self.commit_entry)
            self.layout.addWidget(self.commit_button)
        else:
            self.pic_label = QLabel()
            photo = QPixmap(f"{local_app_data}/icons/no_commits.png")
            self.pic_label.setPixmap(photo)
            self.pic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(self.pic_label)

        self.setWidget(self.main_widget)

    def populate_file_list(self):
        self.file_list_widget.clear()
        changed_files = self.list_changed_files()
        print(changed_files)
        for file in changed_files:
            item = QListWidgetItem(self.file_list_widget)
            checkbox = QCheckBox(file)
            self.file_list_widget.addItem(item)
            self.file_list_widget.setItemWidget(item, checkbox)

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
                selected_files.append(checkbox.text())

        if selected_files:
            # Remove leading path from file paths to make them relative to repo
            relative_files = [os.path.relpath(file, cpath) for file in selected_files]

            try:
                # Stage selected files for commit
                if relative_files:
                    subprocess.run(['git', 'add'] + relative_files, cwd=cpath, check=True)

                    # Get commit message
                    commit_msg = self.commit_entry.text() or "No message"

                    # Commit the changes
                    result = subprocess.run(['git', 'commit', '-m', commit_msg], cwd=cpath, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, text=True)

                    if result.returncode == 0:
                        QMessageBox.information(self, 'Commit Successful', 'Changes have been committed.')
                        print(f"Committing changes for: {relative_files}")
                    else:
                        QMessageBox.warning(self, 'Commit Failed', f"Error: {result.stderr}")
                        print(f"Commit failed: {result.stderr}")

                else:
                    QMessageBox.warning(self, 'No Files Selected', 'Please select files to commit.')

            except subprocess.CalledProcessError as e:
                QMessageBox.warning(self, 'Error', f"Command failed: {e}")
                print(f"Command failed: {e}")
            except Exception as e:
                QMessageBox.warning(self, 'Error', f"Can't commit. Try again.\n{e}")
                print(f"Unexpected error: {e}")
        else:
            QMessageBox.warning(self, 'No Files Selected', 'Please select files to commit.')
