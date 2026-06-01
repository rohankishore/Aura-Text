import subprocess
import os
import re
import json
import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import (QListWidget, QVBoxLayout, QWidget, QDockWidget, QPushButton, 
                             QListWidgetItem, QCheckBox, QMessageBox, QTextEdit, QLabel, 
                             QHBoxLayout, QLineEdit, QScrollArea, QSizePolicy, QDialog)

from auratext.Misc.import_res import notepadequalequalComponentImportPathAppend

"""
File used to store the qdialog required for the working of the regular expression playground feature. 
"""

class RegexPlaygroundDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Regex Playground")
        self.setMinimumSize(650, 350)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.text = QTextEdit()
        self.text.setPlaceholderText("Type or paste sample text here")
        self.layout.addWidget(self.text)

        self.regex = QLineEdit()
        self.regex.setPlaceholderText("Enter a regular expression")
        self.regex.textChanged.connect(self.ParseRegex)
        self.layout.addWidget(self.regex)

        self.res = QTextEdit()
        self.res.setReadOnly(True)
        self.layout.addWidget(self.res)

    def ParseRegex(self):
        text = self.text.toPlainText()
        pattern = self.regex.text()

        try:
            if not pattern:
                self.res.clear()
                return

            matches = [match.group(0) for match in re.finditer(pattern, text)]
            if matches:
                self.res.setPlainText("\n".join(matches))
            else:
                self.res.setPlainText("No matches found.")
        except re.error as error:
            self.res.setPlainText(f"Regex error: {error}")
