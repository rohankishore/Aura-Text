import webbrowser, sys, ModuleFile, time, Preferences, random
from tkinter import messagebox
from PySide6 import QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import QShortcut, QPixmap, QKeySequence, QFont
from Syntax_Highlighter import PythonHighlighter
from TabWidget import TabWidget
from CodeEditor import CodeEditor

__author__ = "Rohan Kishore (@rohankishore on GitHub)"
__copyright__ = "Copyright (C) 2023 Rohan Kishore"
__license__ = "MIT License"
__version__ = "2.1"

#config_data
nfs = Preferences.new_file_shortcut
ofs = Preferences.open_file_shortcut
sfs = Preferences.save_file_shortcut
cfs = Preferences.close_file_shortcut
font = Preferences.font
font_size = Preferences.font_size

tab_stylesheet = """ ......5..0 
    QTabBar::tab:selected {background: white;}
    QTabWidget::pane{ border: 0;}
    QTabBar::tab:hover {background-color: #d5d5d5; color: black;}
    """

class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__()

        splash_pix = QPixmap("Icons/splash.png")
        splash = QSplashScreen(splash_pix)
        splash.show()
        time.sleep(0.5)
        splash.hide()

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

        menubar_items = {
            "&File": [
                ("New File       ", "Ctrl+N", self.new_document),
                ("Open File", "Ctrl+O", self.open_document),
                ("Save As", "Ctrl+S", self.save_document),
                None,
                ("Summary", None, self.summary),
                None,
                ("Exit", "Alt+F4", self.quit),
            ],
            "&Edit": [
                ("Cut Selection    ", "Ctrl+X", self.cut_document),
                ("Copy Selection", "Ctrl+C", self.copy_document),
                ("Paste", "Ctrl+V", self.paste_document),
                ("Undo", "Ctrl+Z", self.undo_document),
                ("Redo", "Ctrl+Y", self.redo_document),
                None,
                ("Duplicate Line", None, self.duplicate_line),
            ],
            "&Code": [
                ("Code Formatting", None, self.code_formatting),
                None,
            ],
            "&View": [("&Fullscreen       ", "F11", self.fullscreen), None],
            "&Tools": [
                ("Read Aloud     ", None, self.speak),
                ("Upload to Pastebin", None, self.pastebin),
            ],

            "&Prefernces": [
                ("Settings     ", None, self.settings_at),
                ("Themeing", None, self.settings_at),
            ],

            "&Help": [
                ("Getting Started", None, self.getting_started),
                ("Submit a Bug Report", None, self.bug_report),
                None,
                ("GitHub", None, self.about_github),
                ("Contribute to Aura Text", None, self.contrib),
                ("Join Discord Server", None, self.discord),
                ("Buy Me A Coffee", None, self.buymeacoffee),
                ("About", None, self.version),
            ],
        }

        for menuitem, actions in menubar_items.items():
            menu = menubar.addMenu(menuitem)
            for act in actions:
                if act:
                    text, shorcut, callback = act
                    action = QtGui.QAction(text, self)
                    action.triggered.connect(callback)
                    menu.addAction(action)
                else:
                    menu.addSeparator()

    def remove_editor(self, index):
        self.tab_widget.removeTab(index)
        if index < len(self.editors):
            del self.editors[index]

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Save File',random.choice(ModuleFile.emsg_save_list),
            QMessageBox.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel, QMessageBox.Save)

        if reply == QMessageBox.Save:
            self.save_document()
            event.accept()
        elif reply == QMessageBox.StandardButton.Discard:
            event.accept()
        else:
            event.ignore()

    def create_editor(self):
        self.text_editor = CodeEditor()
        self.text_editor.setFont(QFont(font, font_size))
        if Preferences.syntax_highlighting == "on":
            highlighter = PythonHighlighter(Preferences.programming_language, self.text_editor.document())
        else:
            pass

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
        ModuleFile.open_document(self)

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
            + "2.1"
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

    def settings_at(self):
        ModuleFile.open_custom_document(self, file_dir="Preferences.py")

    def themeing_at(self):
        ModuleFile.open_custom_document(self, file_dir="themeing.py")

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
