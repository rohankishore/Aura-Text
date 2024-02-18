from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import (
    QDockWidget,
    QWidget,
    QVBoxLayout,)

class Shortcuts(QDockWidget):
    def __init__(self, title="Keyboard Shortcuts", parent=None):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setMinimumWidth(300)

        # Create a widget to hold the labels
        dock_widget_contents = QWidget()
        self.setWidget(dock_widget_contents)

        # Create a layout for the dock widget contents
        dock_layout = QVBoxLayout()
        # dock_layout.addStretch()
        dock_widget_contents.setLayout(dock_layout)

        # Add Heading Label
        heading_label = QLabel("Editor Shortcuts")
        heading_label.setStyleSheet("font-weight: bold; font-size: 25px;")
        dock_layout.addWidget(heading_label)

        placeholder = QLabel("")
        dock_layout.addWidget(placeholder)


        # Create labels with shortcuts
        label1 = QLabel("Magnify Text Size:  Ctrl + '+' ")
        dock_layout.addWidget(label1)

        label2 = QLabel("Minimize Text Size:  Ctrl + '-' ")
        dock_layout.addWidget(label2)

        label3 = QLabel("Delete to start of word:	Ctrl + Backspace")
        dock_layout.addWidget(label3)

        label4 = QLabel("Delete to end of word:  Ctrl + Delete")
        dock_layout.addWidget(label4)

        label5 = QLabel("Delete to start of line:	Ctrl + Shift + Backspace")
        dock_layout.addWidget(label5)

        label6 = QLabel("Delete to end of line:     Ctrl + Shift + Delete")
        dock_layout.addWidget(label6)

        label7 = QLabel("Go to start of document:	Ctrl + Home")
        dock_layout.addWidget(label7)

        label8 = QLabel("Extend selection to start of document:	   Ctrl + Shift + Home")
        dock_layout.addWidget(label8)

        label9 = QLabel("Extend selection to end of document:	   Ctrl + Shift + End")
        dock_layout.addWidget(label9)

        label10 = QLabel("Go to start of display line:   Alt + Home")
        dock_layout.addWidget(label10)

        # Create label 11
        label11 = QLabel("Go to end of document:    Ctrl + End")
        dock_layout.addWidget(label11)

        # Create label 12
        label12 = QLabel("Line delete:	Ctrl+Shift+L")
        dock_layout.addWidget(label12)

        # Create label 13
        label13 = QLabel("Line transpose with previous:	Ctrl+T")
        dock_layout.addWidget(label13)

        # Create label 14
        label14 = QLabel("Previous paragraph. Shift extends selection: 	Ctrl+ [	")
        dock_layout.addWidget(label14)

        # Create label 15
        label15 = QLabel("Next paragraph. Shift extends selection: 	Ctrl+ ]	")
        dock_layout.addWidget(label15)

        # Create label 16
        label16 = QLabel("Previous word. Shift extends selection:	Ctrl + Left")
        dock_layout.addWidget(label16)

        # Create label 17
        label17 = QLabel("Next word. Shift extends selection:	Ctrl + Right")
        dock_layout.addWidget(label17)

        # Create label 18
        label18 = QLabel("Extend rectangular selection to start of line:	Alt+Shift+Home")
        dock_layout.addWidget(label18)

        # Create label 19
        label19 = QLabel("Extend rectangular selection to end of line:	Alt+Shift+Home")
        dock_layout.addWidget(label19)

