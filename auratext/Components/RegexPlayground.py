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
        self.layout.addWidget(self.text)

        self.regex = QLineEdit()
        self.regex.textChanged.connect(lambda: self.ParseRegex())
        self.layout.addWidget(self.regex)

        self.res = QTextEdit()
        self.layout.addWidget(self.res)

    def ParseRegex(self):
        text = self.text.toPlainText()
        pattern = self.regex.text()

        result = re.findall(pattern, text)

        try:
            self.res.setText(result)
        except Exception as e:
            pass
