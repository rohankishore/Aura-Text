import webbrowser
import sys
import time
import random
import Modules as ModuleFile
from tkinter import messagebox
from PySide6 import QtGui
from PySide6.QtWidgets import QSplashScreen, QMainWindow, QMenu, QMessageBox, QInputDialog, QApplication
from PySide6.QtGui import QShortcut, QPixmap, QKeySequence, QFont, QAction, QActionGroup

import Syntax_Highlighter
from Syntax_Highlighter import PythonHighlighter
from TabWidget import TabWidget
from CodeEditor import CodeEditor

__author__ = "Rohan Kishore (@rohankishore on GitHub)"
__copyright__ = "Copyright (C) 2023 Rohan Kishore"
__license__ = "MIT License"
__version__ = "2.5"

listt = list(set(
    list(
        Syntax_Highlighter.py_words + Syntax_Highlighter.cpp_words +
                 Syntax_Highlighter.js_words + Syntax_Highlighter.go_keywords +
                 Syntax_Highlighter.java_keywords)))

with open('Data/Dictionary.txt', 'r') as file:
    content = file.read()
words = content.split(',')
words = set(list(listt + list([word.strip() for word in words])))

# config_data
nfs = "Ctrl + N"
ofs = "Ctrl + O"
sfs = "Ctrl + S"
cfs = "Control + W"
font = "Consolas"
font_size = 11

tab_stylesheet = """ ......5..0
    QTabBar::tab:selected {background: white;}
    QTabWidget::pane{ border: 0;}

    QTabBar::tab:hover {background-color: #d5d5d5; color: black;}
    """

lang = "Python"

class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__()

        splash_pix = QPixmap("Icons/splash.png")
        splash = QSplashScreen(splash_pix)
        splash.show()
        time.sleep(0.5)
        splash.hide()

        self.action_group = QActionGroup(self)
        self.action_group.setExclusive(True)

        self.setWindowTitle("Aura Text")
        self.setWindowIcon(QtGui.QIcon("Icons/icon.ico"))
        self.current_editor = self.create_editor()
        self.editors = []
        self.tab_widget = TabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setStyleSheet(tab_stylesheet)
        self.tab_widget.currentChanged.connect(self.change_text_editor)
        self.tab_widget.tabCloseRequested.connect(self.remove_editor)
        self.new_document()
        self.setCentralWidget(self.tab_widget)
        self.configure_menuBar()
        self.show()

    def configure_menuBar(self):
        menubar = self.menuBar()

        self.setStyleSheet(
            """
                QMenuBar {
                    background-color: #1d1d1d;
                    border: 1px solid #000;
                }
                QMenuBar::item {
                    background-color: #1d1d1d;
                    color: rgb(255,255,255);
                }
                QMenuBar::item::selected {
                    background-color: #1b1b1b;
                }
                QMenu {
                    background-color: rgb(49,49,49);
                    color: rgb(255,255,255);
                    border: 1px solid #000;
                }
                QMenu::item::selected {
                    background-color: rgb(30,30,30);
                }
            """
        )

        file_menu = QMenu("&File", self)
        file_menu.addAction("New File", self.cs_new_document)
        file_menu.addAction("Open File", self.open_document)
        file_menu.addAction("Save As", self.save_document)
        file_menu.addSeparator()
        file_menu.addAction("Summary", self.summary)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.quit)
        menubar.addMenu(file_menu)

        edit_menu = QMenu("&Edit", self)
        edit_menu.addAction("Cut               ", self.cut_document)
        edit_menu.addAction("Copy", self.copy_document)
        edit_menu.addAction("Paste", self.paste_document)
        edit_menu.addAction("Undo Changes", self.undo_document)
        edit_menu.addAction("Redo Changes", self.redo_document)
        edit_menu.addSeparator()
        edit_menu.addAction("Duplicate Line", self.duplicate_line)
        edit_menu.addAction("Reverse Line", self.reverse_line)
        edit_menu.addSeparator()
        edit_menu.addAction("Find First Match", self.find_first_match)
        menubar.addMenu(edit_menu)

        view_menu = QMenu("&View",  self)
        view_menu.addAction("Full Screen", self.fullscreen)
        menubar.addMenu(view_menu)

        nav_menu = QMenu("&Navigate", self)
        nav_menu.addAction("Goto Line", self.gotoLine)
        menubar.addMenu(nav_menu)

        code_menu = QMenu("&Code", self)
        code_menu.addAction("Code Formatting", self.code_formatting)
        menubar.addMenu(code_menu)

        tools_menu = QMenu("&Tools", self)
        tools_menu.addAction("Read Aloud", self.speak)
        tools_menu.addAction("Upload to Pastebin", self.pastebin)
        menubar.addMenu(tools_menu)

        prefernces_menu = QMenu("&Preferences", self)
        language_menu = QMenu("&Languages", prefernces_menu)

        action_text = QAction("Text File", self, checkable=True)
        action_text.triggered.connect(self.textfile)
        self.action_group.addAction(action_text)

        action_py = QAction("Python", self, checkable=True)
        action_py.triggered.connect(self.python)
        self.action_group.addAction(action_py)

        action_cpp = QAction("C++", self, checkable=True)
        action_cpp.triggered.connect(self.cpp())
        self.action_group.addAction(action_cpp)

        action_java = QAction("Java", self, checkable=True)
        action_cpp.triggered.connect(self.java())
        self.action_group.addAction(action_java)

        action_go = QAction("Go", self, checkable=True)
        action_cpp.triggered.connect(self.golang())
        self.action_group.addAction(action_go)

        action_js = QAction("JavaScript", self, checkable=True)
        action_js.triggered.connect(self.js())
        self.action_group.addAction(action_js)
        action_py.setChecked(True)

        language_menu.addAction(action_cpp)
        language_menu.addAction(action_go)
        language_menu.addAction(action_js)
        language_menu.addAction(action_java)
        language_menu.addAction(action_py)
        language_menu.addAction(action_text)
        prefernces_menu.addMenu(language_menu)
        prefernces_menu.addAction("Autocomplete Dictionary", self.dictionary_open)
        menubar.addMenu(prefernces_menu)

        help_menu = QMenu("&Help", self)
        help_menu.addAction("Getting Started", self.getting_started),
        help_menu.addAction("Submit a Bug Report", self.bug_report),
        help_menu.addSeparator()
        help_menu.addAction("GitHub", self.about_github),
        help_menu.addAction("Contribute to Aura Text", self.contrib),
        help_menu.addAction("Join Discord Server", self.discord),
        help_menu.addAction("Buy Me A Coffee", self.buymeacoffee),
        help_menu.addAction("About",  self.version),
        menubar.addMenu(help_menu)

    def remove_editor(self, index):
        self.tab_widget.removeTab(index)
        if index < len(self.editors):
            del self.editors[index]

    def textfile(self):
        highlighter = PythonHighlighter("Text", self.text_editor.document())

    def python(self):
        global lang
        lang = "Python"
        highlighter = PythonHighlighter("Python", self.text_editor.document())

    def cpp(self):
        global lang
        lang = "C++"
        highlighter = PythonHighlighter("C++", self.text_editor.document())

    def js(self):
        global lang
        lang = "JavaScript"
        highlighter = PythonHighlighter(
            "JavaScript", self.text_editor.document())

    def golang(self):
        global lang
        lang = "Go"
        highlighter = PythonHighlighter("Go", self.text_editor.document())

    def java(self):
        global lang
        lang = "Java"
        highlighter = PythonHighlighter("Java", self.text_editor.document())

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            'Save File',
            random.choice(
                ModuleFile.emsg_save_list),
            QMessageBox.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
            QMessageBox.Save)
        if reply == QMessageBox.Save:
            self.save_document()
            event.accept()
        elif reply == QMessageBox.StandardButton.Discard:
            event.accept()
        else:
            event.ignore()

    def create_editor(self):
        self.text_editor = CodeEditor(words)
        self.text_editor.setFont(QFont(font, font_size))
        highlighter = PythonHighlighter("Python", self.text_editor.document())

        self.text_editor.setStyleSheet(
            "QPlainTextEdit {background-color: #1e1f22; color: white;}"
        )
        self.text_editor.setTabStopDistance(12)

        # bindings
        QShortcut(QKeySequence(nfs), self.text_editor).activated.connect(
            self.new_document
        )
        QShortcut(QKeySequence(ofs), self.text_editor).activated.connect(
            self.open_document
        )
        QShortcut(QKeySequence(sfs), self.text_editor).activated.connect(
            self.save_document
        )
        return self.text_editor

    def change_text_editor(self, index):
        if index < len(self.editors):
            self.current_editor = self.editors[index]

    def new_document(self, checked=False, title="Scratch 1"):
        self.current_editor = self.create_editor()
        self.editors.append(self.current_editor)
        self.tab_widget.addTab(self.current_editor, title)
        self.tab_widget.setCurrentWidget(self.current_editor)

    def custom_new_doc(self, title, checked=False):
        self.current_editor = self.create_editor()
        self.editors.append(self.current_editor)
        self.tab_widget.addTab(self.current_editor, title)
        self.tab_widget.setCurrentWidget(self.current_editor)

    def cs_new_document(self, checked=False):
        text, ok = QInputDialog.getText(None, "New File", "Filename:")
        self.current_editor = self.create_editor()
        self.editors.append(self.current_editor)
        self.tab_widget.addTab(self.current_editor, text)
        self.tab_widget.setCurrentWidget(self.current_editor)

    def contrib(self):
        webbrowser.open_new_tab(
            "https://github.com/rohankishore/Aura-Text/blob/main/CONTRIBUTING.md"
        )

    def open_document(self):
        ModuleFile.open_document(self)

    def find_first_match(self):
        word, ok = QInputDialog.getText(None, "Find First Match", "Word:")
        if ok:
            ModuleFile.find_first_match(self, word)

    def dictionary_open(self):
        messagebox.showinfo("READ THIS, HUMAN!", "Save and Replace this file with the existing 'Dictionary.txt' file and restart the app to "
                                                 "see the changes. The file can be found at 'Data' folder.")
        ModuleFile.open_custom_document(self, "Data/Dictionary.txt")

    def save_document(self):
        ModuleFile.save_document(self)

    def speak(self):
        sel = self.current_editor.toPlainText()
        ModuleFile.rightSpeak(sel)

    def summary(self):
        ModuleFile.summary(self)

    def code_formatting(self):
        ModuleFile.code_formatting(self)

    def pastebin(self):
        ModuleFile.pastebin(self)

    def quit(self):
        self.close()

    def gotoLine(self):
        text, ok = QInputDialog.getText(None, "Goto Line", "Line Number:")
        line = int(text)
        ModuleFile.goToLine(self, line)

    def undo_document(self):
        self.current_editor.undo()

    def redo_document(self):
        self.current_editor.redo()

    def cut_document(self):
        self.current_editor.cut()

    def copy_document(self):
        self.current_editor.copy()

    def duplicate_line(self):
        ModuleFile.duplicate_line(self)

    def reverse_line(self):
        ModuleFile.reverse_line(self)

    def paste_document(self):
        self.current_editor.paste()

    def fullscreen(self):
        if not self.isFullScreen():
            self.showFullScreen()
        else:
            self.showMaximized()

    @staticmethod
    def about_github():
        webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Notes")

    @staticmethod
    def version():
        text_ver = (
            "Aura Text"
            + "\n"
            + "Current Version: "
            + "2.5"
            + "\n"
            + "\n"
            + "Copyright © 2023 Rohan Kishore."
        )
        messagebox.showinfo("About", text_ver)

    @staticmethod
    def getting_started():
        webbrowser.open_new_tab(
            "https://github.com/rohankishore/Aura-Text/wiki")

    @staticmethod
    def buymeacoffee():
        webbrowser.open_new_tab("https://www.buymeacoffee.com/auratext")

    @staticmethod
    def bug_report():
        webbrowser.open_new_tab(
            "https://github.com/rohankishore/Aura-Text/issues/new/choose"
        )

    @staticmethod
    def discord():
        webbrowser.open_new_tab("https://discord.gg/4PJfTugn")


def run():
    app = QApplication(sys.argv)
    GUI = Window()
    GUI.setGeometry(200, 100, 1300, 750)
    sys.exit(app.exec())


run()
