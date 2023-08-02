import subprocess
import sys
from art import text2art

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QWidget, QLineEdit, QTextEdit, QVBoxLayout
from pyjokes import pyjokes

from AuraText import json_data
from datetime import datetime

now = datetime.now()

class AuraTextTerminalWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.script_edit = QLineEdit()
        self.setStyleSheet("QWidget {background-color: #000000;}")
        self.script_edit.setStyleSheet(
            "QLineEdit {"
            "   border-radius: 5px;"
            "   padding: 5px;"
            "background-color: #000000;"
            "color: green;"
            "}"
        )
        self.script_edit.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.text = QTextEdit()
        self.text.setStyleSheet("QTextEdit {background-color: #000000;color: white; border:none;}")


        layout1 = QVBoxLayout()
        layout1.addWidget(self.text)
        layout1.addWidget(self.script_edit)

        self.setLayout(layout1)

        self.quitSc = QShortcut(QKeySequence('Return'), self)
        self.quitSc.activated.connect(self.run_script)

    def run_script(self):
        script = self.script_edit.text()
        self.script_edit.clear()

        if script == "ctheme":
            self.text.setPlainText(json_data["theme"])

        elif script == "ctime":
            current_time = now.strftime("%H:%M:%S")
            self.text.setPlainText(current_time)

        elif script == "cdate":
            self.text.setPlainText(str(now))

        elif script == "joke":
            a =  pyjokes.get_joke(language='en', category='neutral')
            self.text.setPlainText(a)

        elif "ascii" in script or "ASCII" in script:
            a = str(script.replace("ascii", ""))
            ascii_art = text2art(a)
            self.text.setPlainText(ascii_art)

        elif "birthday" in script or "BIRTHDAY" in script:
            self.text.setPlainText("Aura Text's GitHub Repo was created on 2022-10-05.")

        elif script == "cproject" or script == "cpath":
            with open('Data/CPath_Project.txt', 'r') as file:
                a = file.readline()

                if a != "" or a!=" ":
                    self.text.setPlainText(a)
                else:
                    self.text.setPlainText("No folder opened!")

        elif script == "exitAT":
            sys.exit()

        else:
            try:
                result = subprocess.run(["powershell", script], capture_output=True)
                res = result.stdout.decode('utf-8')
                res = res.replace('\r\n', '\n').replace('\r', '\n')  # Normalize line endings
                self.text.setPlainText(res)
            except Exception as e:
                print(e)


