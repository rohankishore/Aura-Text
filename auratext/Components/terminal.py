from __future__ import annotations

import os
import random
import subprocess
import sys
from datetime import datetime
from typing import TYPE_CHECKING

import pyautogui
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QShortcut, QKeySequence, QFont, QIcon, QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QWidget, QLineEdit, QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout, QDialog, QListView
from art import text2art
from pyjokes import pyjokes

now = datetime.now()

if TYPE_CHECKING:
    from auratext.Core.window import Window

example_cmds = ["'ascii Hello'", "'joke' for some byte sized humour", "'pip'",
                "'cpath' to view the current project path", "'ctheme' to view the current theme", "'ipconfig'",
                "'key' and type combinations of keyboard keys to emulate them. [key Win + Shift + C]"]


class TerminalHistoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.local_app_data = os.path.join(os.getenv("LocalAppData"), "AuraText")

        self.setWindowTitle("Terminal History")
        self.setMinimumSize(400, 300)

        # Create a list view and set it as the main widget for the dialog
        self.list_view = QListView()
        self.list_model = QStandardItemModel()
        self.list_view.setModel(self.list_model)

        layout = QVBoxLayout(self)
        layout.addWidget(self.list_view)

        close_button = QPushButton("Clear All")
        close_button.clicked.connect(self.clear_all)
        layout.addWidget(close_button)

        self.fill_data()

    def fill_data(self):
        with open(f'{self.local_app_data}/data/terminal_history.txt', 'r') as thistory_file:
            for line in thistory_file:
                item = QStandardItem(line.strip())
                self.list_model.appendRow(item)

    def clear_all(self):
        with open(f'{self.local_app_data}/data/terminal_history.txt', 'r+') as thistory_file:
            thistory_file.truncate(0)


class AuraTextTerminalWidget(QWidget):
    def __init__(self, window: Window):
        super().__init__(window)
        self._window = window

        self.dialog = QDialog()
        self.list_view = QListView()
        self.list_view.doubleClicked.connect(self.item_clicked)
        self.list_model = QStandardItemModel()

        with open(f'{self._window.local_app_data}/data/terminal_history.txt', 'r+') as self.thistory_file:
            self.commands = list(self.thistory_file.readlines())

        self.strcmds = str(self.commands)

        self.script_edit = QLineEdit()
        self.script_edit.setFont(QFont("Consolas"))
        self.setStyleSheet("QWidget {background-color: #FFFFFF;}")
        self.script_edit.setStyleSheet(
            "QLineEdit {"
            "   border-radius: 5px;"
            "   padding: 5px;"
            "   background-color: #000000;"
            "   color: #21FC0D;"  # Color name: Electric Green
            "}"
        )

        terminal_history_icon = QIcon(f"{self._window.local_app_data}/icons/terminal_history.png")
        self.terminal_history_button = QPushButton()
        self.terminal_history_button.setStyleSheet(
            "QPushButton {"
            "background-color: #202124;"
            "border : 0;"
            "}"
        )
        self.terminal_history_button.setIcon(terminal_history_icon)
        self.terminal_history_button.setIconSize(QSize(21, 21))
        self.terminal_history_button.setToolTip("Terminal History")
        self.terminal_history_button.setFixedSize(32, 28)
        self.terminal_history_button.clicked.connect(self.terminal_history_run)

        self.text = QTextEdit()
        self.text.setFont(QFont("Consolas"))
        self.text.setReadOnly(True)
        self.text.setStyleSheet("QTextEdit {background-color: #000000;color: white; border:none;}")

        # Set up a layout for the script_edit and button
        layout = QHBoxLayout()
        layout.addWidget(self.script_edit)
        layout.addWidget(self.terminal_history_button)  # Add the button to the layout
        layout.setContentsMargins(0, 0, 0, 0)  # Remove any margins

        # Set up the main layout that includes the QTextEdit and the layout with script_edit and button
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.text)
        main_layout.addLayout(layout)  # Add the layout with script_edit and button to the main layout

        self.setLayout(main_layout)

        self.quitSc = QShortcut(QKeySequence("Return"), self)
        self.quitSc.activated.connect(self.run_script)

    def update_placeholders(self):
        self.script_edit.setPlaceholderText(("Try " + random.choice(example_cmds)))

    def terminal_history(self):
        self.dialog.setWindowTitle("Terminal History")
        self.dialog.setMinimumSize(400, 300)

        self.list_view.setModel(self.list_model)

        layout = QVBoxLayout(self)

        self.dialog.setLayout(layout)
        layout.addWidget(self.list_view)

    def clear_all(self):
        with open(f'{self._window.local_app_data}/data/terminal_history.txt', 'r+') as thistory_file:
            thistory_file.truncate(0)
        self.list_model.clear()

    def item_clicked(self, index):
        item = self.list_model.itemFromIndex(index)
        if item is not None:
            selected_text = item.text()
            self.script_edit.insert(selected_text)

    def terminal_history_run(self):
        self.terminal_history()
        self.fill_data()
        self.dialog.exec()

    def fill_data(self):
        self.list_model.clear()
        with open(f'{self._window.local_app_data}/data/terminal_history.txt', 'r') as thistory_file:
            for line in thistory_file:
                item = QStandardItem(line.strip())
                self.list_model.appendRow(item)

    def run_script(self):
        print("hi")
        script = self.script_edit.text()

        self.commands.append(script)
        with open(f'{self._window.local_app_data}/data/terminal_history.txt', 'a') as self.thistory_file:
            self.thistory_file.write("\n")
            self.thistory_file.write(script)
            self.fill_data()


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

        elif "flush history" in script or "flush_history" in script:
            self.clear_all()
            self.text.append("Terminal History has been successfully cleared")

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
