import os
import subprocess
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QMessageBox, QLineEdit, QDialog, QLabel, QComboBox, QSpacerItem

local_app_data = os.path.join(os.getenv("LocalAppData"), "AuraText")
cpath = open(f"{local_app_data}/data/CPath_Project.txt", "r+").read().strip()

class GitPushDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(400, 300, 0, 0)
        self.setWindowTitle("Git Push")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addStretch()
        self.branches = ""

        spacer_item = QSpacerItem(10, 5)
        spacer_item_large = QSpacerItem(20, 20)

        label1 = QLabel("Branch:")
        self.main_layout.addWidget(label1)

        self.branch_list = QComboBox()
        self.main_layout.addWidget(self.branch_list)

        label2 = QLabel("Remote:")
        self.remote_list = QComboBox()
        self.main_layout.addWidget(label2)
        self.main_layout.addWidget(self.remote_list)

        self.command = QLineEdit()
        self.command.setPlaceholderText("git push origin main")

        self.main_layout.addSpacerItem(spacer_item)

        self.main_layout.addWidget(self.command)

        self.main_layout.addSpacerItem(spacer_item_large)

        push_button = QPushButton("Push")
        self.main_layout.addWidget(push_button)
        push_button.clicked.connect(self.push)

        if not self.is_git_repo():
            print(self, "Error", "Not a Git repository. Please initialize a Git repository.")
            self.reject()
            return

        try:
            result = subprocess.run(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                raise FileNotFoundError("Git command not found. Ensure that Git is installed and added to the PATH.")

            self.branches = self.get_all_branches()
            self.c_branch = self.get_current_branch()
            self.remotes = self.get_all_remotes()

            if not self.remotes:
                self.remotes = ["origin"]

            self.branch_list.addItems(self.branches)
            self.remote_list.addItems(self.remotes)

            print("Branches:", self.branches)
            print("Current Branch:", self.c_branch)
            print("Remotes:", self.remotes)

        except Exception as e:
            print("Error initializing GitPushDialog:", e)
            QMessageBox.critical(self, "Initialization Error", str(e))

    def is_git_repo(self):
        return os.path.isdir(os.path.join(cpath, '.git'))

    def get_current_branch(self):
        try:
            result = subprocess.run(['git', 'branch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cpath, text=True)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.startswith('*'):
                        return line[2:].strip()
            else:
                raise Exception(f"Failed to get current branch: {result.stderr}")
        except Exception as e:
            print("Error getting current branch:", e)
            return ""

    def get_all_branches(self):
        try:
            result = subprocess.run(['git', 'branch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cpath, text=True)
            if result.returncode != 0:
                raise Exception(f"Error getting branches: {result.stderr}")

            branches = result.stdout.split('\n')
            branches = [branch[2:] if branch.startswith('*') else branch.strip() for branch in branches if branch.strip()]
            return branches
        except Exception as e:
            print("Error getting branches:", e)
            return []

    def get_all_remotes(self):
        try:
            result = subprocess.run(['git', 'remote', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cpath, text=True)
            if result.returncode != 0:
                raise Exception(f"Error getting remotes: {result.stderr}")

            remotes = result.stdout.strip().split('\n')

            remote_list = []
            for line in remotes:
                parts = line.split()
                if len(parts) >= 2:
                    remote_name = parts[0]
                    remote_url = parts[1]
                    remote_list.append((remote_name, remote_url))

            seen = set()
            unique_remotes = []
            for remote in remote_list:
                if remote[0] not in seen:
                    unique_remotes.append(remote[0])
                    seen.add(remote[0])

            return unique_remotes
        except Exception as e:
            print("Error getting remotes:", e)
            return []

    def push(self):
        try:
            if not self.is_git_repo():
                print(self, "Error", "Not a Git repository. Please initialize a Git repository.")
                return

            command_text = self.command.text().strip()
            if not command_text:
                QMessageBox.warning(self, 'Error', 'Command is empty')
                return

            result = subprocess.run(command_text.split(), cwd=cpath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                QMessageBox.information(self, 'Push Successful', 'Changes have been pushed.')
            else:
                QMessageBox.warning(self, 'Push Failed', f"Error: {result.stderr}")
                print(f"Push failed: {result.stderr}")
        except Exception as e:
            print("Error executing push command:", e)
            QMessageBox.critical(self, 'Error', f"Failed to execute push command: {e}")
