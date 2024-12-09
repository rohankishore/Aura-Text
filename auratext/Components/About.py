import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QSpacerItem, QHBoxLayout, QLabel, QSizePolicy, QDialog)

local_app_data = os.path.join(os.getenv("LocalAppData"), "AuraText")

class AboutAppDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About App")
        self.setMinimumSize(400, 300)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Image at the top
        image_label = QLabel()
        pixmap = QPixmap(f"{local_app_data}/icons/banner.png")
        pixmap = pixmap.scaled(200, 200, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # App description
        description = QLabel("Aura Text is a versatile and powerful text editor powered by QScintilla that provides all the necessary tools for developers. It is build using PyQt6 and Python."
                             "\n" + "\n" 
                             "Version: v5.1.0" + "\n" + "\n" + "\n" + "Made with ❣️ by Rohan Kishore")
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Buttons at the bottom
        button_layout = QHBoxLayout()

        close_button = QPushButton("Close")
        learn_more_button = QPushButton("Learn More")

        # Add spacers for better layout
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        button_layout.addItem(spacer)
        button_layout.addWidget(learn_more_button)
        button_layout.addWidget(close_button)
        button_layout.addItem(spacer)

        # Connect button signals
        close_button.clicked.connect(self.close)
        learn_more_button.clicked.connect(self.learn_more)

        # Add widgets to the layout
        layout.addWidget(image_label)
        layout.addWidget(description)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def learn_more(self):
        print("Learn More button clicked!")

