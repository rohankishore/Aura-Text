from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QHeaderView, QMessageBox
import subprocess
import tempfile
import os

class GitRebaseDialog(QDialog):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.setWindowTitle("Interactive Rebase")
        self.setGeometry(100, 100, 700, 500)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Rebase from (commit hash, branch, or tag):")
        self.layout.addWidget(self.label)

        self.commit_input = QLineEdit()
        self.commit_input.setPlaceholderText("e.g., HEAD~5 or a commit hash")
        self.layout.addWidget(self.commit_input)

        self.load_commits_button = QPushButton("Load Commits")
        self.load_commits_button.clicked.connect(self.load_commits)
        self.layout.addWidget(self.load_commits_button)

        self.commit_table = QTableWidget()
        self.commit_table.setColumnCount(3)
        self.commit_table.setHorizontalHeaderLabels(["Action", "Commit", "Message"])
        self.commit_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.commit_table)

        self.start_rebase_button = QPushButton("Start Rebase")
        self.start_rebase_button.clicked.connect(self.start_rebase)
        self.start_rebase_button.setEnabled(False)
        self.layout.addWidget(self.start_rebase_button)

    def load_commits(self):
        rebase_from = self.commit_input.text()
        if not rebase_from:
            return

        try:
            # Get the list of commits from the specified point to HEAD
            command = ["git", "log", f"{rebase_from}..HEAD", "--pretty=format:%h|%s"]
            process = subprocess.run(
                command,
                cwd=self.path,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )

            if process.returncode != 0:
                self.commit_table.setRowCount(1)
                error_item = QTableWidgetItem(f"Error loading commits: {process.stderr}")
                self.commit_table.setSpan(0, 0, 1, 3)
                self.commit_table.setItem(0, 0, error_item)
                self.start_rebase_button.setEnabled(False)
                return

            commits = process.stdout.strip().split('\n')
            if commits == ['']:
                commits = []
            commits.reverse() # Show oldest first, as it appears in rebase file

            self.commit_table.setRowCount(len(commits))

            for i, commit in enumerate(commits):
                sha, message = commit.split('|', 1)
                
                # Action dropdown
                action_combo = QComboBox()
                actions = ["pick", "reword", "edit", "squash", "fixup", "drop"]
                action_combo.addItems(actions)
                self.commit_table.setCellWidget(i, 0, action_combo)

                # Commit SHA
                sha_item = QTableWidgetItem(sha)
                sha_item.setFlags(sha_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.commit_table.setItem(i, 1, sha_item)

                # Commit Message
                message_item = QTableWidgetItem(message)
                self.commit_table.setItem(i, 2, message_item)

            self.start_rebase_button.setEnabled(True)

        except Exception as e:
            self.commit_table.setRowCount(1)
            error_item = QTableWidgetItem(f"An error occurred: {e}")
            self.commit_table.setSpan(0, 0, 1, 3)
            self.commit_table.setItem(0, 0, error_item)
            self.start_rebase_button.setEnabled(False)

    def start_rebase(self):
        rebase_from = self.commit_input.text()
        if not rebase_from:
            return

        # Generate the rebase script
        script_lines = []
        for i in range(self.commit_table.rowCount()):
            action = self.commit_table.cellWidget(i, 0).currentText()
            sha = self.commit_table.item(i, 1).text()
            message = self.commit_table.item(i, 2).text()
            script_lines.append(f"{action} {sha} {message}")
        
        rebase_script = "\n".join(script_lines)

        try:
            # Write the script to a temporary file
            script_path = os.path.join(tempfile.gettempdir(), 'auratext-rebase-script.txt')
            with open(script_path, 'w') as f:
                f.write(rebase_script)

            # For Windows, we need to create a simple batch file to act as the editor
            editor_script_path = os.path.join(tempfile.gettempdir(), 'auratext-rebase-editor.bat')
            with open(editor_script_path, 'w') as f:
                # The batch script will be called by git with the path to the git-rebase-todo file
                # We overwrite that file with our generated script.
                f.write(f'copy "{script_path}" %1 > NUL')

            env = os.environ.copy()
            env["GIT_SEQUENCE_EDITOR"] = f'"{editor_script_path}"'

            command = ["git", "rebase", "-i", rebase_from]
            process = subprocess.run(
                command,
                cwd=self.path,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                env=env,
                shell=True # shell=True is needed for GIT_SEQUENCE_EDITOR to be interpreted correctly
            )

            if process.returncode == 0:
                QMessageBox.information(self, "Rebase Successful", f"Successfully rebased onto {rebase_from}.")
                self.accept()
            else:
                error_message = process.stderr
                if not error_message:
                    error_message = process.stdout
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Critical)
                msg_box.setText("Rebase Failed")
                msg_box.setInformativeText(error_message)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.exec()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
