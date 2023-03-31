import os, webbrowser, sys, ModuleFile, time, autopep8
from tkinter import filedialog, messagebox
from PySide6 import QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from Syntax_Highlighter import PythonHighlighter
from TabWidget import TabWidget
from CodeEditor import CodeEditor

__author__ = "Rohan Kishore (@rohankishore on GitHub)"
__copyright__ = "Copyright (C) 2023 Rohan Kishore"
__license__ = "MIT License"
__version__ = "2.0"

tab_stylesheet = """ ........0 
    QTabBar::tab:selected {background: white;}
    QTabWidget::pane{ border: 0;}
    QTabBar::tab:hover {background-color: #d5d5d5; color: black;}
    """


class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__()

        splash_pix = QPixmap("splash.png")
        splash = QSplashScreen(splash_pix)
        splash.show()
        time.sleep(0.5)
        splash.hide()

        self.setWindowTitle("Aura Text")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
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

        menubar_items = {
            "&File": [
                ("&New       ", "Ctrl+N", self.new_document),
                ("&Open", "Ctrl+O", self.open_document),
                ("&Save", "Ctrl+S", self.save_document),
                None,
                ("&Summary", None, self.summary),
                None,
                ("&Quit", "Alt+F4", self.quit),
            ],
            "&Edit": [
                ("&Cut    ", "Ctrl+X", self.cut_document),
                ("&Copy", "Ctrl+C", self.copy_document),
                ("&Paste", "Ctrl+V", self.paste_document),
                ("&Undo", "Ctrl+Z", self.undo_document),
                ("&Redo", "Ctrl+Y", self.redo_document),
                None,
            ],
            "&Code": [
                ("&Generate        ", "Alt + Insert", None),
                ("&Code Formatting", None, self.code_formatting),
                None,
                ("&Make Code Snippet", None, self.save_snippet),
                ("&Load Code Snippet", None, self.load_snippet),
                # ("&Redo", "Ctrl+Y", self.redo_document),
                None,
            ],
            "&View": [("&Fullscreen       ", "F11", self.fullscreen), None],
            "&Tools": [
                ("Read Aloud     ", None, self.speak),
                ("Upload to Pastebin", None, self.pastebin),
            ],
            "&Help": [
                ("About", None, self.version),
                ("GitHub", None, self.about_github),
                ("Buy Me A Coffee", None, self.buymeacoffee),
                None,
                ("Getting Started", None, self.getting_started),
                ("Submit a Bug Report", None, self.bug_report),
                None,
                ("Join Discord Server", None, self.discord),
                ("Contribute to Aura Text", None, self.contrib),
            ],
        }

        for menuitem, actions in menubar_items.items():
            menu = menubar.addMenu(menuitem)
            for act in actions:
                if act:
                    text, shorcut, callback = act
                    action = QtGui.QAction(text, self)
                    # action.setShortcut(shorcut)
                    action.triggered.connect(callback)
                    menu.addAction(action)
                else:
                    menu.addSeparator()

    def remove_editor(self, index):
        self.tab_widget.removeTab(index)
        if index < len(self.editors):
            del self.editors[index]

    def create_editor(self):
        self.text_editor = CodeEditor()
        self.text_editor.setFont(QFont("Consolas", 11))
        highlighter = PythonHighlighter(self.text_editor.document())
        self.text_editor.setStyleSheet(
            "QPlainTextEdit {background-color: #1e1f22; color: white;}"
        )
        self.text_editor.setTabStopDistance(12)

        # bindings
        QShortcut(QKeySequence("Ctrl+N"), self.text_editor).activated.connect(
            self.new_document
        )
        QShortcut(QKeySequence("Ctrl+O"), self.text_editor).activated.connect(
            self.open_document
        )
        QShortcut(QKeySequence("Ctrl+S"), self.text_editor).activated.connect(
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

    def custom_new_document(self, title, checked=False):
        self.current_editor = self.create_editor()
        self.editors.append(self.current_editor)
        self.tab_widget.addTab(self.current_editor, title)
        self.tab_widget.setCurrentWidget(self.current_editor)

    def contrib(self):
        webbrowser.open_new_tab(
            "https://github.com/rohankishore/Aura-Text/blob/main/CONTRIBUTING.md"
        )

    def open_document(self):
        file_dir = filedialog.askopenfilename(
            title="Select file",
        )
        if file_dir:
            try:
                f = open(file_dir, "r")
                filedata = f.read()
                self.new_document(title=os.path.basename(file_dir))
                self.current_editor.setPlainText(filedata)
                f.close()
            except FileNotFoundError:
                return

    def save_document(self):
        ModuleFile.save_document(self)

    def load_snippet(self):
        ModuleFile.load_snippet(self)

    def save_snippet(self):
        ModuleFile.save_snippet(self)

    def speak(self):
        sel = self.current_editor.toPlainText()
        ModuleFile.rightSpeak(sel)

    def summary(self):
        ModuleFile.summary(self)

    def code_formatting(self):
        og_code = str(self.current_editor.toPlainText())
        if og_code != "":
            options = {
                "aggressive": 1,
                "experimental": True,
            }
            clean_code = autopep8.fix_code(og_code, options=options)
            self.custom_new_document(title="Code Formatting")
            self.current_editor.setPlainText(clean_code)
        else:
            messagebox.showerror(
                "Error: No Code Found!",
                "It looks like your keyboard is on vacation. Please wake it up and "
                "start typing some code so we can work our magic.",
            )

    def pastebin(self):
        ModuleFile.pastebin(self)

    def quit(self):
        self.close()

    def undo_document(self):
        self.current_editor.undo()

    def redo_document(self):
        self.current_editor.redo()

    def cut_document(self):
        self.current_editor.cut()

    def copy_document(self):
        self.current_editor.copy()

    def paste_document(self):
        self.current_editor.paste()

    def add_indent(self):
        if self.text_editor.toPlainText().endswith(":\n"):
            self.text_editor.insertPlainText("    ")

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
            + "2.0"
            + "\n"
            + "\n"
            + "Hello PySide6!!"
            + "\n"
            + "\n"
            + "Copyright © 2023 Rohan Kishore."
        )
        version = QMessageBox()
        messagebox.showinfo("About", text_ver)

    @staticmethod
    def getting_started():
        webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Text/wiki")

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
    # GUI.showMaximized()
    GUI.setGeometry(200, 100, 1300, 750)
    sys.exit(app.exec())


run()
