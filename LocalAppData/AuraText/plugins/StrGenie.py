import sys
import threading

import pyttsx3
from PyQt6.QtGui import QKeySequence, QShortcut, QAction, QFont, QPainter, QPen, QIcon
from PyQt6.QtWidgets import QMenu, QDialog, QLabel, QDockWidget, QWidget, QVBoxLayout, QComboBox, QPushButton
from PyQt6.QtCore import QTimer, Qt

from auratext import Plugin
from auratext.Core.AuraText import CodeEditor
from auratext.Core.window import Window


class StringManipulation(Plugin):
    def __init__(self, window: Window) -> None:
        super().__init__(window)

        self.window = window

        self.sm_menu = QMenu("&String Manipulation", self.window)
        self.case_menu = QMenu("&Case      ", self.window)
        self.order_menu = QMenu("&Order     ", self.window)

        self.capitalize = QAction("Capitalize", self.window)
        self.capitalize.triggered.connect(self.toUpper)

        self.lowercase = QAction("Lowercase", self.window)
        self.lowercase.triggered.connect(self.toLower)

        self.title = QAction("Title", self.window)
        self.title.triggered.connect(self.toTitle)

        self.reverse = QAction("Reverse", self.window)
        self.reverse.triggered.connect(self.reverse_str)

        self.sort = QAction("Sort", self.window)
        self.sort.triggered.connect(self.sort_str)

        self.snake_case = QAction("Snake Case", self.window)
        self.snake_case.triggered.connect(self.snake_str)

        self.rev_pc = QAction("Reverse (Preserve Case)", self.window)
        self.rev_pc.triggered.connect(self.reverse_str_preserve_case)

        self.case_menu.addAction(self.capitalize)
        self.case_menu.addAction(self.lowercase)
        self.case_menu.addAction(self.title)

        self.order_menu.addAction(self.reverse)
        self.order_menu.addAction(self.sort)
        self.order_menu.addAction(self.snake_case)
        self.order_menu.addAction(self.rev_pc)

        self.sm_menu.addMenu(self.case_menu)
        self.sm_menu.addMenu(self.order_menu)

        button = QPushButton("Pomodoro Timer")
        button.clicked.connect(self.run_rm)

        try:
            self.window.current_editor.context_menu.addMenu(self.sm_menu)
        except AttributeError:
            pass

    def toUpper(self):
        try:
            text = str(self.window.current_editor.selectedText())
            cap_text = text.upper()
            self.window.current_editor.replaceSelectedText(cap_text)
        except Exception as e:
            print(e)

    def toTitle(self):
        try:
            text = str(self.window.current_editor.selectedText())
            cap_text = text.title()
            self.window.current_editor.replaceSelectedText(cap_text)
        except Exception as e:
            print(e)

    def toLower(self):
        try:
            text = str(self.window.current_editor.selectedText())
            cap_text = text.lower()
            self.window.current_editor.replaceSelectedText(cap_text)
        except Exception as e:
            print(e)

    def reverse_str(self):
        try:
            text = str(self.window.current_editor.selectedText())
            cap_text = text[::-1]
            self.window.current_editor.replaceSelectedText(cap_text)
        except Exception as e:
            print(e)

    def reverse_str_preserve_case(self):
        try:
            text = str(self.window.current_editor.selectedText())
            reversed_text = text[::-1]
            reversed_preserved = ''.join(
                char.upper() if original.isupper() else char.lower()
                for char, original in zip(reversed_text, text)
            )
            self.window.current_editor.replaceSelectedText(reversed_preserved)
        except Exception as e:
            print(e)

    def sort_str(self):
        try:
            text = str(self.window.current_editor.selectedText())
            cap_text = ''.join(sorted(text))
            self.window.current_editor.replaceSelectedText(cap_text)
        except Exception as e:
            print(e)

    def snake_str(self):
        try:
            text = str(self.window.current_editor.selectedText())
            cap_text = '_'.join(text.lower().split())
            self.window.current_editor.replaceSelectedText(cap_text)
        except Exception as e:
            print(e)

    def run_rm(self):
        try:
            pass
        except Exception as e:
            print(e)
