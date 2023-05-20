import os
import random
import sys
import time
import webbrowser
from tkinter import messagebox, filedialog
from PyQt6.Qsci import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QActionGroup, QFileSystemModel, QPixmap, QIcon, QFontMetrics
from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog, QDockWidget, QTreeView, QFileDialog, QSplashScreen, \
    QMessageBox, QMenu, QPlainTextEdit

import Lexers
import MenuConfig
import Modules as ModuleFile
from TabWidget import TabWidget


path_file = open("Data/CPath_Project.txt", 'r+')
cpath = path_file.read()

class CodeEditor(QsciScintilla):
    def __init__(self):
        super().__init__()
        lexer = Lexers.PythonLexer(self)
        self.setLexer(lexer)
        self.setPaper(QColor("#1e1f22"))

        lexer.setPaper(QColor("#1e1f22"))
        lexer.setColor(QColor('#808080'), lexer.Comment)
        lexer.setColor(QColor('#FFA500'), lexer.Keyword)
        lexer.setColor(QColor('#00000'), lexer.ClassName)
        lexer.setColor(QColor("#FFFFFF"), lexer.Default)
        lexer.setFont(QFont('Consolas'))

        self.setTabWidth(4)
        self.setMarginLineNumbers(1, True)
        self.setAutoIndent(True)
        self.setMarginWidth(1, "#0000")
        left_margin_index = 0
        left_margin_width = 7
        self.setMarginsForegroundColor(QColor("#FFFFFF"))
        self.setMarginsBackgroundColor(QColor("#1e1f22"))
        font_metrics = QFontMetrics(self.font())
        left_margin_width_pixels = font_metrics.horizontalAdvance(' ') * left_margin_width
        self.SendScintilla(self.SCI_SETMARGINLEFT, left_margin_index, left_margin_width_pixels)
        self.setFolding(QsciScintilla.FoldStyle.BoxedTreeFoldStyle)
        self.setMarginSensitivity(2, True)
        self.setFoldMarginColors(QColor("#1e1f22"), QColor("#1e1f22"))
        self.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#80d3d3d3"))
        self.setWrapMode(QsciScintilla.WrapMode.WrapWord)
        self.setAutoCompletionThreshold(1)
        self.setBackspaceUnindents(True)
        self.setIndentationGuides(True)

        self.context_menu = QMenu(self)
        encrypt_menu = QMenu("Encryption", self.context_menu)
        self.context_menu.addAction("Cut        ").triggered.connect(self.cut)
        self.context_menu.addAction("Copy").triggered.connect(self.copy)
        self.context_menu.addAction("Paste").triggered.connect(self.paste)
        self.context_menu.addAction("Select All").triggered.connect(self.selectAll)
        self.context_menu.addSeparator()
        encrypt_menu.addAction("Encrypt Selection", self.encode)
        encrypt_menu.addAction("Decrypt Selection", self.decode)
        self.context_menu.addAction("Calculate", self.calculate)
        self.context_menu.addMenu(encrypt_menu)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)


    def show_context_menu(self, point):
        self.context_menu.popup(self.mapToGlobal(point))

    def calculate(self):
        ModuleFile.calculate(self)

    def encode(self):
        ModuleFile.encypt(self)

    def decode(self):
        ModuleFile.decode(self)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        splash_pix = QPixmap("Icons/splash.png")
        splash = QSplashScreen(splash_pix)
        splash.show()
        time.sleep(0.5)
        splash.hide()

        self.tab_widget = TabWidget()
        self.tab_widget.setTabsClosable(True)

        self.setCentralWidget(self.tab_widget)
        self.editors = []

        self.action_group = QActionGroup(self)
        self.action_group.setExclusive(True)

        self.tab_widget.currentChanged.connect(self.change_text_editor)
        self.tab_widget.tabCloseRequested.connect(self.remove_editor)
        self.new_document()
        self.setWindowTitle('Aura Text')
        self.setWindowIcon(QIcon("Icons/icon.ico"))
        self.configure_menuBar()
        self.showMaximized()

    def create_editor(self):
        self.text_editor = CodeEditor()
        return self.text_editor

    def treeview_viewmenu(self):
        self.treeview_project(cpath)

    def new_project(self):
        new_folder_path = filedialog.askdirectory(title="Create New Folder", initialdir="./",
                                                  mustexist=False)
        with open('Data/CPath_Project.txt', 'w') as file:
            file.write(new_folder_path)

    def treeview_project(self, path):
        dock = QDockWidget(path, self)
        dock.setStyleSheet("QDockWidget { background-color: #d2d2d2;}")
        dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        tree_view = QTreeView()
        self.model = QFileSystemModel()
        tree_view.setStyleSheet("QTreeView { background-color: #1b1b1b; color: white; }")
        tree_view.setModel(self.model)
        tree_view.setRootIndex(self.model.index(path))
        self.model.setRootPath(path)
        dock.setWidget(tree_view)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        tree_view.doubleClicked.connect(self.open_file)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            'Save File',
            random.choice(
                ModuleFile.emsg_save_list),
            QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save)
        if reply == QMessageBox.StandardButton.Save:
            self.save_document()
            event.accept()
        elif reply == QMessageBox.StandardButton.Discard:
            event.accept()
        else:
            event.ignore()

    def open_file(self, index):
        path = self.model.filePath(index)
        if path:
            try:
                f = open(path, "r")
                try:
                    filedata = f.read()
                    self.new_document(title=os.path.basename(path))
                    self.current_editor.insert(filedata)
                    f.close()
                except UnicodeDecodeError:
                    messagebox.showerror("Wrong Filetype!", "This file type is not supported!")
            except FileNotFoundError:
                return

    def configure_menuBar(self):
        MenuConfig.configure_menuBar(self)

    def python(self):
        lexer = Lexers.python(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def csharp(self):
        Lexers.csharp(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def json(self):
        Lexers.json(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def duplicate_line(self):
        ModuleFile.duplicate_line(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def yaml(self):
        Lexers.yaml(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def xml(self):
        Lexers.xml(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def html(self):
        Lexers.html(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def cpp(self):
        Lexers.cpp(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def ruby(self):
        Lexers.ruby(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def perl(self):
        Lexers.perl(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def pascal(self):
        Lexers.pascal(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def css(self):
        Lexers.css(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def sql(self):
        Lexers.sql(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def lua(self):
        Lexers.lua(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def idl(self):
        Lexers.idl(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def matlab(self):
        Lexers.matlab(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def tcl(self):
        Lexers.tcl(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def verilog(self):
        Lexers.verilog(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def spice(self):
        Lexers.spice(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def vhdl(self):
        Lexers.vhdl(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def octave(self):
        Lexers.octave(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def fortran77(self):
        Lexers.fortran77(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def tex(self):
        Lexers.tex(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def makefile(self):
        Lexers.makefile(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def markdown(self):
        Lexers.markdown(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def js(self):
        Lexers.js(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def fortran(self):
        Lexers.fortran(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def java(self):
        Lexers.java(self)
        self.current_editor.setMarginsBackgroundColor(QColor("#1e1f22"))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def pastebin(self):
        ModuleFile.pastebin(self)

    def code_formatting(self):
        ModuleFile.code_formatting(self)

    def jump_to_line(self):
        line_number, ok = QInputDialog.getText(None, "Goto Line", "Line:")
        self.current_editor.setCursorPosition(line_number - 1, 0)

    def open_project(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        if dialog.exec():
            project_path = dialog.selectedFiles()[0]
            pathh = str(project_path)
            with open('Data/CPath_Project.txt', 'w') as file:
                file.write(pathh)
            messagebox.showinfo("New Project", f"New project created at {project_path}")
            self.treeview_project(project_path)

    def open_project_as_treeview(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        if dialog.exec():
            project_path = dialog.selectedFiles()[0]
            self.treeview_project(project_path)

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

    def cs_new_document(self, checked=False):
        text, ok = QInputDialog.getText(None, "New File", "Filename:")
        self.current_editor = self.create_editor()
        self.editors.append(self.current_editor)
        self.tab_widget.addTab(self.current_editor, text)
        self.tab_widget.setCurrentWidget(self.current_editor)

    def change_text_editor(self, index):
        if index < len(self.editors):
            self.current_editor = self.editors[index]

    def undo_document(self):
        self.current_editor.undo()

    def notes(self):
        note_dock = QDockWidget("Notes", self)
        terminal_widget = QPlainTextEdit(note_dock)
        note_dock.setWidget(terminal_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, note_dock)
        note_dock.show()

    def redo_document(self):
        self.current_editor.redo()

    def cut_document(self):
        self.current_editor.cut()

    def copy_document(self):
        self.current_editor.copy()

    def summary(self):
        lines = str(self.current_editor.lines())
        text = self.current_editor.text()
        text = "Number of Lines: " + lines
        messagebox.showinfo("Summary", text)

    def find(self):
        text, ok = QInputDialog.getText(None, "Find", "Enter Word:")
        ModuleFile.find_and_highlight_word(self, text)

    def paste_document(self):
        self.current_editor.paste()


    def remove_editor(self, index):
        self.tab_widget.removeTab(index)
        if index < len(self.editors):
            del self.editors[index]

    def open_document(self):
        ModuleFile.open_document(self)

    def save_document(self):
        ModuleFile.save_document(self)

    @staticmethod
    def about_github():
        webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Notes")

    @staticmethod
    def version():
        text_ver = (
                "Aura Text"
                + "\n"
                + "Current Version: "
                + "3.0"
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

    def fullscreen(self):
        if not self.isFullScreen():
            self.showFullScreen()
        else:
            self.showMaximized()

    @staticmethod
    def bug_report():
        webbrowser.open_new_tab(
            "https://github.com/rohankishore/Aura-Text/issues/new/choose"
        )

    @staticmethod
    def discord():
        webbrowser.open_new_tab("https://discord.gg/4PJfTugn")


def main():
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
