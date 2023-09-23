from __future__ import annotations
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel


if TYPE_CHECKING:
    from auratext.Core.window import Window


class WelcomeWidget(QWidget):
    def __init__(self, window: Window):
        super().__init__()

        layout = QVBoxLayout()
        # layout.addStretch(102)

        label2 = QLabel()
        label2.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        pixmap = QPixmap(f"{window.local_app_data}/icons/splash_morning.png")
        label2.setPixmap(pixmap)

        label = QLabel("Welcome to Aura Text")
        label3 = QLabel(
            "Aura Text is a versatile and powerful text editor powered by QScintilla that provides all the "
            + "\n"
            + "necessary tools for developers. It is build using PyQt6 and Python."
        )
        label1 = QLabel("Please open a folder or create a new file to start editing.")

        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont("Consolas", 12))

        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label1.setFont(QFont("Consolas", 12))

        label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label3.setFont(QFont("Consolas", 12))

        button = QPushButton("Open Folder")
        button.clicked.connect(window.open_project)

        button1 = QPushButton("Clone from Git")
        button1.clicked.connect(window.gitClone)

        layout.addWidget(label2)
        layout.addWidget(label)
        layout.addWidget(label3)
        layout.addWidget(label1)
        layout.addWidget(button)
        layout.addWidget(button1)

        self.setLayout(layout)
