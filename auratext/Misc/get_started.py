import json
import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QPushButton, QLabel, \
    QStackedWidget
from PyQt6.QtGui import QMovie
import sys


local_app_data = os.path.join(os.getenv("LocalAppData"), "AuraText")
with open(f"{local_app_data}/data/config.json", "r") as config_file:
    _config = json.load(config_file)


class SetupWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Get Started")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.setup_wizard()

    def setup_wizard(self):
        self.stacked_widget = QStackedWidget(self.central_widget)

        # Slide 1
        slide1 = QLabel("Welcome to Your App!\nThis is the first slide.")
        self.stacked_widget.addWidget(slide1)

        # Slide 2 with GIF
        slide2 = QLabel()
        movie = QMovie("hh.gif")  # Replace with the path to your GIF file
        slide2.setMovie(movie)
        movie.start()
        self.stacked_widget.addWidget(slide2)

        # Slide 3
        slide3 = QLabel("Slide 3:\nExplain the third step of the setup.")
        self.stacked_widget.addWidget(slide3)

        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_slide)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.stacked_widget)
        layout.addWidget(next_button)

        self.current_slide_index = 0

    def next_slide(self):
        self.current_slide_index += 1

        if self.current_slide_index < self.stacked_widget.count():
            self.stacked_widget.setCurrentIndex(self.current_slide_index)
        else:
            self.close()


def show_setup_window():
    _config["show_setup_info"] = "False"
    app = QApplication(sys.argv)
    setup_window = SetupWindow()
    setup_window.show()
    sys.exit(app.exec())
