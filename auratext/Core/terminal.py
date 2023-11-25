from __future__ import annotations

import random
from typing import TYPE_CHECKING
import subprocess
from art import text2art

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence, QFont
from PyQt6.QtWidgets import QWidget, QLineEdit, QTextEdit, QVBoxLayout
import sys
from pyjokes import pyjokes
import pyautogui
from datetime import datetime

now = datetime.now()

if TYPE_CHECKING:
    from .window import Window

example_cmds = ["'ascii Hello'", "'joke' for some byte sized humour", "'pip'",
                "'cpath' to view the current project path", "'ctheme' to view the current theme", "'ipconfig'",
                "'key' and type combinations of keyboard keys to emulate them. [key Win + Shift + C]"]


class AuraTextTerminalWidget(QWidget):
    def __init__(self, window: Window):
        super().__init__(window)
        self._window = window

        self.script_edit = QLineEdit()
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

        if self._window._config["terminal_tips"] == "True":
            self.script_edit.setPlaceholderText(("Try " + random.choice(example_cmds)))
            self.script_edit.textChanged.connect(self.update_placeholders)
        else:
            pass

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
        #self.script_edit.clear()

        self._window._terminal_history.append(script)
        print("hi")
        print(self._window._terminal_history)

        if script == "ctheme":
            self.text.append(self._window._themes["theme"])

        elif script == "ctime":
            current_time = now.strftime("%H:%M:%S")
            self.text.append(current_time)

        elif script == "cdate":
            self.text.append(str(now))

        elif script == "joke":
            a = pyjokes.get_joke(language="en", category="neutral")
            self.text.append(a)

        elif "ascii" in script:
            a = str(script.replace("ascii", ""))
            ascii_art = text2art(a)
            self.text.append(ascii_art)

        elif "key" in script:
            # Remove "key" and split the remaining string by '+'
            a = script.replace("key", "")
            a = a.replace(' ', '')  # Remove spaces as well
            keys = a.split('+')

            # Emulate the keypress using pyautogui.hotkey, passing only non-empty strings
            keys_to_press = [key.lower() for key in keys if key]
            if keys_to_press:
                pyautogui.hotkey(*keys_to_press)

            self.text.append(("Triggered: " + str(keys_to_press)))

        elif "birthday" in script:
            self.text.append("Aura Text's GitHub Repo was created on 2022-10-05.")

        elif script == "cproject" or script == "cpath":
            with open(f"{self._window.local_app_data}/data/CPath_Project.txt", "r") as file:
                a = file.readline()

                if a != "" or a != " ":
                    self.text.append(a)
                else:
                    self.text.append("No folder opened!")

        elif script == "exitat":
            sys.exit()
        else:
            try:
                result = subprocess.run(["powershell", script], capture_output=True)
                res = result.stdout.decode("utf-8")
                res = res.replace("\r\n", "\n").replace("\r", "\n")  # Normalize line endings
                self.text.append(res)
            except Exception as e:
                print(e)
