import subprocess
import os
import json
import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import (QListWidget, QVBoxLayout, QWidget, QDockWidget, QPushButton, 
                             QListWidgetItem, QCheckBox, QMessageBox, QTextEdit, QLabel, 
                             QHBoxLayout, QFrame, QScrollArea, QSizePolicy, QDialog)
import platform

from auratext.Misc.import_res import notepadequalequalComponentImportPathAppend
from auratext.Misc.boilerplates import get_appdata_dirs
sys.path.append(notepadequalequalComponentImportPathAppend)
from notepadequalequal.fileio import retrieve_file

class RegexPlaygroundDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Regex Playground")
        self.setMinimumSize(650, 350)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.text = QTextEdit()
        self.layout.addWidget(self.text)
