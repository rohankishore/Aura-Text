from __future__ import annotations

import random
import time
from typing import TYPE_CHECKING
import subprocess
from art import text2art

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence, QFont
from PyQt6.QtWidgets import QWidget, QLineEdit, QTextEdit, QVBoxLayout
import sys
from pyjokes import pyjokes

from datetime import datetime

now = datetime.now()

if TYPE_CHECKING:
    from .window import Window

example_cmds = ["'ascii Hello'", "'joke' for some byte sized humour", "'pip'",
                "'cpath' to view the current project path", "'ctheme' to view the current theme", "'ipconfig'"]

class AuraTextTerminalWidget(QWidget):
    def __init__(self, window: Window):
        super().__init__(window)
        self._window = window

        self.script_edit = QLineEdit()
        self.script_edit.setPlaceholderText(("Try " + random.choice(example_cmds)))
        self.script_edit.setFont(QFont("Consolas"))
        self.setStyleSheet("QWidget {background-color: #FFFFFF;}")
        self.script_edit.setStyleSheet(
            "QLineEdit {"
            "   border-radius: 5px;"
            "   padding: 5px;"
            "background-color: #000000;"
            "color: #21FC0D;"  # Color name: Electric Green
            "}"
        )
        self.script_edit.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.script_edit.textChanged.connect(self.update_placeholders)
        self.text = QTextEdit()
        self.text.setFont(QFont("Consolas"))
        self.text.setReadOnly(True)
        self.text.setStyleSheet("QTextEdit {background-color: #000000;color: white; border:none;}")

        layout1 = QVBoxLayout()
        layout1.addWidget(self.text)
        layout1.addWidget(self.script_edit)

        self.setLayout(layout1)

        self.quitSc = QShortcut(QKeySequence("Return"), self)
        self.quitSc.activated.connect(self.run_script)

    def update_placeholders(self):
        self.script_edit.setPlaceholderText(("Try " + random.choice(example_cmds)))

    def run_script(self):
        print("hi")
        script = self.script_edit.text()
        self.script_edit.clear()

        self._window._terminal_history.append(script)
        print("hi")
        print(self._window._terminal_history)

        if script == "ctheme":
            self.text.setPlainText(self._window._themes["theme"])

        elif script == "ctime":
            current_time = now.strftime("%H:%M:%S")
            self.text.setPlainText(current_time)

        elif script == "cdate":
            self.text.setPlainText(str(now))

        elif script == "joke":
            a = pyjokes.get_joke(language="en", category="neutral")
            self.text.setPlainText(a)

        elif "ascii" in script or "ASCII" in script:
            a = str(script.replace("ascii", ""))
            ascii_art = text2art(a)
            self.text.setPlainText(ascii_art)

        elif "birthday" in script or "BIRTHDAY" in script:
            self.text.setPlainText("Aura Text's GitHub Repo was created on 2022-10-05.")

        elif script == "cproject" or script == "cpath":
            with open(f"{self._window.local_app_data}/data/CPath_Project.txt", "r") as file:
                a = file.readline()

                if a != "" or a != " ":
                    self.text.setPlainText(a)
                else:
                    self.text.setPlainText("No folder opened!")

        elif script == "exitAT":
            sys.exit()
        else:
            try:
                result = subprocess.run(["powershell", script], capture_output=True)
                res = result.stdout.decode("utf-8")
                res = res.replace("\r\n", "\n").replace("\r", "\n")  # Normalize line endings
                self.text.setPlainText(res)
            except Exception as e:
                print(e)

