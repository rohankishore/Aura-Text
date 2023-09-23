from PyQt6.QtWidgets import QApplication
import sys

from auratext.Core.window import Window


def main():
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
