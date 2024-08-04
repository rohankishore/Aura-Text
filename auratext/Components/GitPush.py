import os
import subprocess

from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QMessageBox, QLineEdit, QDialog, QLabel, QComboBox, QSpacerItem

local_app_data = os.path.join(os.getenv("LocalAppData"), "AuraText")
cpath = open(f"{local_app_data}/data/CPath_Project.txt", "r+").read()


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
        branch = self.branch_list.currentText()
        if self.remote_list.currentText() == "":
            remote = "origin"
        else:
            remote = self.remote_list.currentText()
        cmd = "git push " + remote + "" + branch
        self.command.setText(cmd)

        self.main_layout.addSpacerItem(spacer_item)

        self.main_layout.addWidget(self.command)

        self.main_layout.addSpacerItem(spacer_item_large)

        push_button = QPushButton("Push")
        self.main_layout.addWidget(push_button)
        push_button.clicked.connect(self.push)

        try:
            result = subprocess.run(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                raise FileNotFoundError("Git command not found. Ensure that Git is installed and added to the PATH.")

            self.branches = self.get_all_branches()
            self.c_branch = self.get_current_branch()
            self.remotes = self.get_all_remotes()
            self.remotes[0] = "origin"

            self.branch_list.addItems(self.branches)
            self.remote_list.addItems(self.remotes)

            print(self.branches)

        except Exception as e:
            print(e)

    def get_current_branch(self):
        result = subprocess.run(['git', 'branch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cpath, text=True)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('*'):
                    return line[2:].strip()
        else:
            raise Exception(f"Failed to get current branch: {result.stderr}")

    def get_all_branches(self):
        result = subprocess.run(['git', 'branch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise Exception(f"Error getting branches: {result.stderr}")

        branches = result.stdout.split('\n')
        # Strip whitespace, remove empty lines, and remove the '*' from the current branch
        branches = [branch[2:] if branch.startswith('*') else branch.strip() for branch in branches if branch.strip()]
        return branches

    def get_all_remotes(self):
        result = subprocess.run(['git', 'remote', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise Exception(f"Error getting remotes: {result.stderr}")

        remotes = result.stdout.strip().split('\n')

        remote_list = []
        for line in remotes:
            parts = line.split()
            if len(parts) >= 2:  # Ensure there are enough parts in the line
                remote_name = parts[0]
                remote_url = parts[1]
                remote_list.append((remote_name, remote_url))

        # Remove duplicate remotes keeping only one instance
        seen = set()
        unique_remotes = []
        for remote in remote_list:
            if remote[0] not in seen:
                unique_remotes.append(remote)
                seen.add(remote[0])

        return unique_remotes

    def push(self):
        result = subprocess.run((self.command.text()), cwd=cpath, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            QMessageBox.information(self, 'Push Successful', 'Changes have been pushed.')
        else:
            QMessageBox.warning(self, 'Push Failed', f"Error: {result.stderr}")
            print(f"Push failed: {result.stderr}")
