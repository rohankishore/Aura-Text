import json
import os
import random
import sys
import time
import tkinter.messagebox
import webbrowser
from tkinter import filedialog, messagebox
import git
import qdarktheme
import pyjokes
import importlib
from PyQt6.Qsci import QsciScintilla, QsciAPIs, QsciScintillaBase
from PyQt6.QtCore import Qt, QSize, QPoint
from PyQt6.QtGui import QColor, QFont, QActionGroup, QFileSystemModel, QKeySequence,  QPixmap, QIcon, QFontMetrics, QAction, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog, QDockWidget, QTreeView, QFileDialog, QSplashScreen, \
    QMessageBox, QMenu, QPlainTextEdit, QPushButton, QWidget, QVBoxLayout, QDialog, QLabel, QStatusBar, QHBoxLayout, QSplitter
from plugin_interface import ContextMenuPluginInterface
import Lexers
import datetime

#import PluginDownload
import Core.file_templates as temp
import config_page
from Core import WelcomeScreen, ApplyTheme
import terminal
import MenuConfig
import Modules as ModuleFile
from Core.TabWidget import TabWidget


path_file = open("Data/CPath_Project.txt", 'r+')
cpath = path_file.read()

with open("Data/theme.json", "r") as json_file_theme:
    json_data_theme = json.load(json_file_theme)

with open("Data/config.json", "r") as json_file_config:
    json_data_config = json.load(json_file_config)

editor_bg = str(json_data_theme["editor_theme"])
margin_bg = str(json_data_theme["margin_theme"])
linenumber_bg = str(json_data_theme["lines_theme"])
margin_fg = str(json_data_theme["margin_fg"])
editor_fg = str(json_data_theme["editor_fg"])
linenumber_fg = str(json_data_theme["lines_fg"])
sidebar_bg = str(json_data_theme["sidebar_bg"])
font = str(json_data_theme["font"])
theme_color = str(json_data_theme["theme"])
theme = str(json_data_theme["theme_type"])
intend_length = int(json_data_config["intend_length"])

class CodeEditor(QsciScintilla):
    def __init__(self):
        super().__init__(parent=None)

        lexer = Lexers.PythonLexer()
        self.setLexer(lexer)
        self.setPaper(QColor(editor_bg))
        self.ensureLineVisible(True)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  # or Qt.ScrollBarAsNeeded
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # or Qt.ScrollBarAsNeeded

        # Autocompletion
        apis = QsciAPIs(self.lexer())
        self.setUtf8(True)
        self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionCaseSensitivity(True)
        #self.setWrapMode(QsciScintilla.WrapMode.WrapNone)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionFillupsEnabled(True)
        # Set up the scrollbar
        self.setWrapMode(QsciScintilla.WrapMode.WrapNone)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setUtf8(True)

        # Setting up lexers
        lexer.setPaper(QColor(editor_bg))
        lexer.setColor(QColor('#808080'), lexer.Comment)
        lexer.setColor(QColor('#FFA500'), lexer.Keyword)
        lexer.setColor(QColor('#FFFFFF'), lexer.ClassName)
        lexer.setColor(QColor("#59ff00"), lexer.TripleSingleQuotedString)
        lexer.setColor(QColor("#59ff00"), lexer.TripleDoubleQuotedString)
        lexer.setColor(QColor("#3ba800"), lexer.SingleQuotedString)
        lexer.setColor(QColor("#3ba800"), lexer.DoubleQuotedString)
        lexer.setColor(QColor(editor_fg), lexer.Default)
        lexer.setFont(QFont(font))

        self.setTabWidth(intend_length)
        self.setMarginLineNumbers(1, True)
        self.setAutoIndent(True)
        self.SendScintilla(QsciScintilla.SCI_SETMULTIPLESELECTION, 1)
        self.setMarginWidth(1, "#0000")
        left_margin_index = 0
        left_margin_width = 7
        self.setEolMode(QsciScintilla.EolMode.EolUnix)
        self.setEolVisibility(False)
        self.setMarginsForegroundColor(QColor(linenumber_fg))
        self.setMarginsBackgroundColor(QColor(linenumber_bg))
        font_metrics = QFontMetrics(self.font())
        left_margin_width_pixels = font_metrics.horizontalAdvance(' ') * left_margin_width
        self.SendScintilla(self.SCI_SETMARGINLEFT, left_margin_index, left_margin_width_pixels)
        self.setFolding(QsciScintilla.FoldStyle.BoxedTreeFoldStyle)
        self.setMarginSensitivity(2, True)
        self.setFoldMarginColors(QColor(margin_bg), QColor(margin_bg))
        self.setBraceMatching(QsciScintilla.BraceMatch.StrictBraceMatch)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#20d3d3d3"))
        self.setAutoCompletionThreshold(1)
        self.setBackspaceUnindents(True)
        self.setIndentationGuides(True)

        self.context_menu = QMenu(self)

        plugin_dir = os.path.abspath("Plugins")
        sys.path.append(plugin_dir)

        for file_name in os.listdir(plugin_dir):
            if file_name.endswith(".py"):
                plugin_module_name = os.path.splitext(file_name)[0]
                try:
                    plugin_module = importlib.import_module(plugin_module_name)
                    for obj_name in dir(plugin_module):
                        obj = getattr(plugin_module, obj_name)
                        if isinstance(obj, type) and (
                                issubclass(obj, ContextMenuPluginInterface)
                        ) and obj != ContextMenuPluginInterface:
                            plugin = obj()
                            plugin.add_menu_items(self.context_menu)
                            print(f"Loaded plugin: {plugin_module_name}")
                except Exception as e:
                    print(f"Error loading plugin {plugin_module_name}: {e}")


        self.encrypt_menu = QMenu("Encryption", self.context_menu)
        self.context_menu.addAction("Cut        ").triggered.connect(self.cut)
        self.context_menu.addAction("Copy").triggered.connect(self.copy)
        self.context_menu.addAction("Paste").triggered.connect(self.paste)
        self.context_menu.addAction("Select All").triggered.connect(self.selectAll)
        self.context_menu.addSeparator()
        self.context_menu.addAction("Calculate", self.calculate)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.keyPressEvent = self.handleKeyPress

    def handleKeyPress(self, event):
        if event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key.Key_A:  # Example: Use Ctrl + A to add cursors
                self.addCursorAtCaret()

        else:
            QsciScintilla.keyPressEvent(self, event)

    def addCursorAtCaret(self):
        position = self.SendScintilla(QsciScintilla.SCI_GETCURRENTPOS)
        line = self.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, position)
        index = self.SendScintilla(QsciScintilla.SCI_GETCOLUMN, position)

        self.SendScintilla(QsciScintilla.SCI_MULTIPLESELECTADDNEXT, line, index)

    def show_context_menu(self, point):
        self.context_menu.popup(self.mapToGlobal(point))

    def calculate(self):
        ModuleFile.calculate(self)


class Sidebar(QDockWidget):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setFixedWidth(40)
        style_sheet = "background : {}".format(sidebar_bg)
        self.setStyleSheet(style_sheet)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

class ContextMenuButton(QPushButton):
    def __init__(self, text, menu_items=None, parent=None):
        super().__init__(text, parent)
        self.setMenu(QMenu(self))
        if menu_items:
            for item_text, callback in menu_items:
                action = QAction(item_text, self)
                action.triggered.connect(callback)
                self.menu().addAction(action)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Splash Screen
        splash_pix = QPixmap("Core/Icons/splash_morning.png")
        current_time = datetime.datetime.now().time()
        sunrise_time = current_time.replace(hour=6, minute=0, second=0, microsecond=0)
        sunset_time = current_time.replace(hour=18, minute=0, second=0, microsecond=0)


        # Check which time interval the current time falls into
        if sunrise_time <= current_time < sunrise_time.replace(hour=12):
            splash_pix = QPixmap("Core/Icons/splash_morning.png")
        elif sunrise_time.replace(hour=12) <= current_time < sunset_time:
            splash_pix = QPixmap("Core/Icons/splash_afternoon.png")
        else:
            splash_pix = QPixmap("Core/Icons/splash_night.png")

        splash = QSplashScreen(splash_pix)
        #splash.show()
        #time.sleep(1)
        splash.hide()


        self.tab_widget = TabWidget()
        self.current_editor = CodeEditor()

        self.tab_widget.setTabsClosable(True)

        # Shortcuts
        toggleCase = QAction('Toggle Case', self, triggered=self.toggleCase)
        toggleCase.setShortcut(QKeySequence(Qt.Key.Key_Control ,Qt.Key.Key_Shift, Qt.Key.Key_U))

        self.md_dock = QDockWidget("Markdown Preview")
        self.mdnew = QDockWidget("Markdown Preview")


        # Sidebar
        self.sidebar_main = Sidebar("", self)
        self.sidebar_main.setTitleBarWidget(QWidget())
        self.sidebar_widget = QWidget(self.sidebar_main)
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_main.setWidget(self.sidebar_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar_main)

        self.bottom_bar = QStatusBar()
        style_sheet = "background : {}".format(sidebar_bg)
        self.bottom_bar.setStyleSheet(style_sheet)
        self.setStatusBar(self.bottom_bar)

        self.cfpath = ""

        context_menu_items = [
            ("Change Intend Length", self.jumpToIndent),
        ]

        context_menu_button = ContextMenuButton(str(intend_length) + " spaces", context_menu_items, self)

        self.read_only_icon = QIcon('Core/Icons/read_only.png')
        self.write_button_icon = QIcon('Core/Icons/write_allowed.png')

        self.directory_linear = QLabel(self.get_linear_path(cpath), self.bottom_bar)
        self.read_only_button = QPushButton(self.bottom_bar)
        self.read_only_button.setToolTip("Make the current file read only")
        self.read_only_button.setIcon(self.write_button_icon)
        self.read_only_button.clicked.connect(self.read_only_func_for_button)

        self.line_label = QPushButton(self.bottom_bar)
        self.line_label.clicked.connect(self.go_to_line_column)
        self.line_label.setText("0:0")

        context_menu_dir = QMenu(self)
        copy_action = QAction("Open in File Explorer", self)
        copy_action.triggered.connect(lambda : self.open_in_file_explorer())
        context_menu_dir.addAction(copy_action)
        self.directory_linear.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.directory_linear.customContextMenuRequested.connect(lambda pos: self.show_context_menu(context_menu_dir, pos, self.directory_linear))

        self.bottom_bar.addWidget(self.directory_linear)
        self.bottom_bar.addPermanentWidget(context_menu_button)
        self.bottom_bar.addPermanentWidget(self.line_label)
        self.bottom_bar.addPermanentWidget(self.read_only_button)

        self.statusbar = Sidebar("", self)
        self.statusbar.setTitleBarWidget(QWidget())
        self.statusbar_widget = QWidget(self.statusbar)
        self.statusbar_layout = QVBoxLayout(self.statusbar_widget)
        self.statusbar_layout.addStretch()
        self.statusbar_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.statusbar.setWidget(self.statusbar_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.statusbar)

        explorer_icon = QIcon('Core/Icons/explorer_unfilled.png')
        self.explorer_button = QPushButton(self)
        self.explorer_button.setIcon(explorer_icon)
        self.explorer_button.setIconSize(QSize(23, 23))
        self.explorer_button.setFixedSize(28, 28)
        self.explorer_button.setStyleSheet(
            """
            QPushButton {
                border: none;
                border-radius:10;
                align: left;
            }
            QPushButton:hover {
                background-color: #4e5157;
            }
            """
        )

        self.note_dock = QDockWidget("Notes", self)
        self.note_widget = QPlainTextEdit(self.note_dock)

        plugin_icon = QIcon('Core/Icons/extension_unfilled.png')
        self.plugin_button = QPushButton(self)
        self.plugin_button.setIcon(plugin_icon)
        self.plugin_button.setIconSize(QSize(21, 21))
        self.plugin_button.setFixedSize(30, 30)
        self.plugin_button.setStyleSheet(
            """
            QPushButton {
                border: none;
                border-radius:10;
                align: botton;
            }
            QPushButton:hover {
                background-color: #4e5157;
            }
            """
        )

        self.sidebar_layout.insertWidget(0, self.explorer_button)
        self.sidebar_layout.insertWidget(1, self.plugin_button)

        self.sidebar_layout.addStretch()
        self.statusbar_layout.addStretch()
        self.statusbar_layout.addSpacing(45)

        # Connect the button's clicked signal to the slot
        self.explorer_button.clicked.connect(self.expandSidebar__Explorer)
        self.plugin_button.clicked.connect(self.expandSidebar__Plugins)

        self.setCentralWidget(self.tab_widget)

        self.splitter = QSplitter(Qt.Orientation.Vertical)

        self.editors = []

        self.action_group = QActionGroup(self)
        self.action_group.setExclusive(True)

        self.tab_widget.setStyleSheet("""
        QTabWidget {border: none;}
        QTabBar {qproperty-drawBase: 0;}
        """)

        if cpath == "" or cpath == " ":
            self.explorer_button.setDisabled(True)
            welcome_widget = WelcomeScreen.WelcomeWidget(self)
            self.tab_widget.addTab(welcome_widget, "Welcome")
        else:
            pass

        self.tab_widget.currentChanged.connect(self.change_text_editor)
        self.tab_widget.tabCloseRequested.connect(self.remove_editor)
        #self.new_document()
        self.setWindowTitle('Aura Text')
        self.setWindowIcon(QIcon("Core/Icons/icon.ico"))
        self.configure_menuBar()
        self.showMaximized()

    def create_editor(self):
        self.text_editor = CodeEditor()
        return self.text_editor

    def load_plugins(self, plugins_directory):
        plugin_files = [f for f in os.listdir(plugins_directory) if f.endswith(".py")]
        for plugin_file in plugin_files:
            module_name = os.path.splitext(plugin_file)[0]
            module_path = os.path.join(plugins_directory, plugin_file)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, PluginBase) and obj is not PluginBase:
                    self.plugins.append(obj())

    def onPluginDockVisibilityChanged(self, visible):
        if visible:
            self.plugin_button.setIcon(QIcon('Core/Icons/extension_filled.png'))
        else:
            self.plugin_button.setIcon(QIcon('Core/Icons/extension_unfilled.png'))

    def terminal_widget(self):
        from pyqtconsole.console import PythonConsole
        self.terminal_dock = QDockWidget("Terminal", self)
        terminal_widget = terminal.AuraTextTerminalWidget()
        self.sidebar_layout_Terminal = QVBoxLayout(terminal_widget)
        self.terminal_dock.setWidget(terminal_widget)
        self.python_dock = QDockWidget("Python Shell", self)
        python_widget = terminal.PythonShell()
        self.sidebar_layout_python = QVBoxLayout(python_widget)
        self.python_dock.setWidget(python_widget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.terminal_dock)

    def read_only_func_for_button(self):
        try:
            if self.current_editor.isReadOnly():
                self.current_editor.setReadOnly(False)
                self.read_only_button.setIcon(self.write_button_icon)
            else:
                self.current_editor.setReadOnly(True)
                self.read_only_button.setIcon(self.read_only_icon)
        except AttributeError:
            QMessageBox.warning(self, "Open a file first", "Open a file to make the editor read only!")

    def go_to_line_column(self):
        text, ok = QInputDialog.getText(
            self, "Go to", "[LINE] : [COLUMN]"
        )
        line_column_text = text
        try:
            line, column = map(int, line_column_text.split(":"))
            if line > 0 and column > 0:
                self.current_editor.ensureLineVisible(line - 1)
                self.current_editor.setCursorPosition(line - 1, column - 1)
                self.current_editor.setFocus()  # Set focus on the editor
        except (ValueError, IndexError):
            pass

    def onExplorerDockVisibilityChanged(self, visible):
        if visible:
            self.explorer_button.setIcon(QIcon('Core/Icons/explorer_filled.png'))
        else:
            self.explorer_button.setIcon(QIcon('Core/Icons/explorer_unfilled.png'))

    def encode(self):
        ModuleFile.encypt(self)

    def jumpToIndent(self):
        intend, ok = QInputDialog.getText(
            self, "Intend Length", "Intend:"
        )
        try:
            json_data_config["intend_length"] = int(intend)
        except ValueError:
            messagebox = QMessageBox()
            messagebox.setWindowTitle("Length Error"), messagebox.setText(
                "No Input Found! Please type in correct intend length")
            messagebox.exec()

    def decode(self):
        ModuleFile.decode(self)

    def treeview_project(self, path):
        self.dock = QDockWidget("Explorer", self)
        self.dock.visibilityChanged.connect(lambda visible: self.onExplorerDockVisibilityChanged(visible))
        #dock.setStyleSheet("QDockWidget { background-color: #191a1b; color: white;}")
        self.dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        tree_view = QTreeView()
        self.model = QFileSystemModel()
        #tree_view.setStyleSheet("QTreeView { background-color: #191a1b; color: white; border: none; }")
        tree_view.setModel(self.model)
        tree_view.setRootIndex(self.model.index(path))
        self.model.setRootPath(path)
        self.dock.setWidget(tree_view)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
        self.splitDockWidget(self.sidebar_main, self.dock, Qt.Orientation.Horizontal)
        tree_view.doubleClicked.connect(self.open_file)

    def expandSidebar__Explorer(self):
        self.dock = QDockWidget("Explorer", self)
        self.dock.setMinimumWidth(200)
        self.dock.visibilityChanged.connect(
            lambda visible: self.onExplorerDockVisibilityChanged(visible))
        #self.dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        tree_view = QTreeView()

        self.model = QFileSystemModel()
        style_sheet = "background : {}".format(sidebar_bg)
        tree_view.setStyleSheet(style_sheet)
        tree_view.setModel(self.model)
        tree_view.setRootIndex(self.model.index(cpath))
        self.model.setRootPath(cpath)
        self.dock.setWidget(tree_view)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)
        tree_view.setFont(QFont("Consolas"))

        tree_view.setColumnHidden(1, True)  # File type column
        tree_view.setColumnHidden(2, True)  # Size column
        tree_view.setColumnHidden(3, True)  # Date modified column
        tree_view.doubleClicked.connect(self.open_file)

    def splitView(self):
        self.split_dock = QDockWidget("Split View", self)
        self.split_dock.setMinimumWidth(550)

        currentEditorText = self.current_editor.text()

        splitWidget = CodeEditor()
        splitWidget.setText(currentEditorText)

        self.split_dock.setWidget(splitWidget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.split_dock)

    def create_snippet(self):
        ModuleFile.CodeSnippets.snippets_gen(self.current_editor)

    def import_snippet(self):
        ModuleFile.CodeSnippets.snippets_open(self.current_editor)

    def expandSidebar__Settings(self):
        self.settings_dock = QDockWidget("Settings", self)
        self.settings_dock.setStyleSheet("QDockWidget {background-color : #1b1b1b; color : white;}")
        self.settings_dock.setFixedWidth(200)
        self.settings_widget = config_page.ConfigPage()
        self.settings_layout = QVBoxLayout(self.settings_widget)
        self.settings_layout.addWidget(self.settings_widget)
        self.settings_dock.setWidget(self.settings_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.settings_dock)

    def expandSidebar__Plugins(self):
        self.plugin_dock = QDockWidget("Extensions", self)
        background_color = self.plugin_button.palette().color(self.plugin_button.backgroundRole()).name()
        if background_color == "#3574f0":
            self.plugin_dock.destroy()
        else:
            self.plugin_dock.visibilityChanged.connect(lambda visible: self.onPluginDockVisibilityChanged(visible))
            self.plugin_dock.setMinimumWidth(300)
            self.plugin_widget = PluginDownload.FileDownloader()
            self.plugin_layout = QVBoxLayout(self.plugin_widget)
            self.plugin_layout.addStretch(1)
            self.plugin_layout.addWidget(self.plugin_widget)
            self.plugin_dock.setWidget(self.plugin_widget)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.plugin_dock)

    def new_project(self):
        new_folder_path = filedialog.askdirectory(title="Create New Folder", initialdir="./",
                                                  mustexist=False)
        with open('Data/CPath_Project.txt', 'w') as file:
            file.write(new_folder_path)

    def code_jokes(self):
        a =  pyjokes.get_joke(language='en', category='neutral')
        QMessageBox.information(self, "A Byte of Humour!", a)

    def commit_changes(self):
        commit_message, ok = QInputDialog.getText(
            self, "Commit", "Enter commit message:"
        )
        if ok and commit_message:
            try:
                repo = git.Repo(os.getcwd())
                repo.git.add("--all")
                repo.index.commit(commit_message)
                QMessageBox.information(self, "Commit", "Changes committed successfully.")
            except git.exc.GitCommandError as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"An error occurred while committing: {e}",
                    QMessageBox.StandardButton.Ok,
                )

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


    def show_context_menu(self, context_menu, pos, label):
        adjusted_pos = label.mapToGlobal(pos)
        adjusted_pos.setY(adjusted_pos.y() + (label.height()-1))  # Position the menu below the label
        context_menu.exec(adjusted_pos)

    def lintCode(self):
        self.statusBar().clearMessage()
        code = self.current_editor.text()
        try:
            compile(code, '<string>', 'exec')
            self.statusBar().showMessage("No errors were found!", 5000)
        except SyntaxError as e:
            # Display the syntax error message in the status bar
            self.statusBar().showMessage(f'Syntax Error: {str(e)}', 5000)

    def gitClone(self):
        try:
            from git import Repo
            repo_url, ok = QInputDialog.getText(self, "Git Repo", "URL of the Repository")
            try:
                path = filedialog.askdirectory(title="Repo Path", initialdir="./",
                                                          mustexist=False)
            except:
                messagebox = QMessageBox()
                messagebox.setWindowTitle("Path Error"), messagebox.setText(
                    "The folder should be EMPTY! Please try again with an EMPTY folder")
                messagebox.exec()

            try:
                Repo.clone_from(repo_url, path)
                with open('Data/CPath_Project.txt', 'w') as file:
                    file.write(path)
                messagebox = QMessageBox()
                messagebox.setWindowTitle("Success!"), messagebox.setText(
                    "The repository has been cloned successfully!")
                messagebox.exec()
                self.treeview_project(path)
            except git.GitCommandError:
                pass


        except ImportError:
            messagebox = QMessageBox()
            messagebox.setWindowTitle("Git Import Error"), messagebox.setText("Aura Text can't find Git in your PC. Make sure Git is installed and has been added to PATH.")
            messagebox.exec()

    def markdown_open(self, path_data):
        ModuleFile.markdown_open(self, path_data)

    def markdown_new(self):
        ModuleFile.markdown_new(self)

    # TREEVIEW
    def open_file(self, index):
        path = self.model.filePath(index)
        image_extensions = ["png", "jpg", "jpeg", "ico", "gif", "bmp"]
        ext = path.split(".")[-1]

        def add_image_tab():
            ModuleFile.add_image_tab(self, self.tab_widget, path, os.path.basename(path))

        if path:

            try:
                if ext in image_extensions:
                    add_image_tab()
                    return

            except UnicodeDecodeError:
                messagebox = QMessageBox()
                messagebox.setWindowTitle("Wrong Filetype!"), messagebox.setText("This file type is not supported!")
                messagebox.exec()

            try:
                f = open(path, "r")
                try:
                    filedata = f.read()
                    self.new_document(title=os.path.basename(path))
                    self.current_editor.insert(filedata)
                    if ext == "md" or ext == "MD":
                        self.markdown_open(filedata)
                    elif ext == "png" or ext == "PNG":
                        add_image_tab()
                    f.close()
                except UnicodeDecodeError:
                    messagebox = QMessageBox()
                    messagebox.setWindowTitle("Wrong Filetype!"), messagebox.setText("This file type is not supported!")
                    messagebox.exec()
            except FileNotFoundError:
                return

    def configure_menuBar(self):
        MenuConfig.configure_menuBar(self)

    def python(self):
        Lexers.python(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def csharp(self):
        Lexers.csharp(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def import_theme(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select JSON Theme File", "", "JSON Files (*.json)")

        if file_path:
            try:
                # Read the new theme contents from the selected JSON file
                with open(file_path, "r") as json_file:
                    new_theme = json.load(json_file)

                # Write the new theme contents to the existing config JSON file
                config_file_path = "Data/theme.json"
                with open(config_file_path, "w") as config_file:
                    json.dump(new_theme, config_file, indent=4)
                    messagebox = QMessageBox(self)
                    messagebox.setText("The selected theme has been applied!"), messagebox.setWindowTitle("Theme Applied!")
                    messagebox.show()

            except PermissionError:
                messagebox = QMessageBox(self)
                messagebox.setText("Failed to Apply the selected theme. Try again or submit an Issue in GitHub"), messagebox.setWindowTitle("Uh-Oh!!")
                messagebox.show()

    def json(self):
        Lexers.json(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def duplicate_line(self):
        ModuleFile.duplicate_line(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def yaml(self):
        Lexers.yaml(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def xml(self):
        Lexers.xml(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def html(self):
        Lexers.html(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def toggle_read_only(self):
        self.current_editor.setReadOnly(True)
        self.read_only_button.setIcon(self.read_only_icon)

    def read_only_reset(self):
        self.current_editor.setReadOnly(False)
        self.read_only_button.setIcon(self.write_button_icon)

    def cpp(self):
        Lexers.cpp(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def ruby(self):
        Lexers.ruby(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def perl(self):
        Lexers.perl(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def pascal(self):
        Lexers.pascal(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def css(self):
        Lexers.css(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def sql(self):
        Lexers.sql(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def lua(self):
        Lexers.lua(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def get_current_line_number(self):
        current_position = self.current_editor.SendScintilla(QsciScintilla.SCI_GETCURRENTPOS)
        line_number = self.current_editor.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, current_position)
        column = current_position - self.current_editor.SendScintilla(QsciScintilla.SCI_POSITIONFROMLINE, line_number)
        return f"{line_number + 1}:{column}"

    def update_line_label(self):
        a = self.get_current_line_number()
        self.line_label.setText(a)

    def cmake(self):
        Lexers.cmake(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def postscript(self):
        Lexers.postscript(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def asm(self):
        Lexers.asm(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def avs(self):
        Lexers.avs(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def coffeescript(self):
        Lexers.coffeescript(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def batch(self):
        Lexers.bat(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def update_linear_dir(self, text):
        self.directory_linear.setText(self.cfpath)

    def open_in_file_explorer(self):
        import subprocess
        subprocess.Popen(['explorer', '/select,', self.cfpath])

    def insert_py(self):
        a = temp.generate_python_template()
        self.new_document(title="main.py")
        self.current_editor.setText(a)
        self.python()

    def insert_html(self):
        a = temp.generate_html_template()
        self.new_document(title="file.html")
        self.current_editor.setText(a)
        self.html()

    def insert_tex(self):
        a = temp.generate_tex_template()
        self.new_document(title="main.tex")
        self.current_editor.setText(a)
        self.tex()

    def insert_cpp(self):
        a = temp.generate_cpp_template()
        self.new_document(title="main.cpp")
        self.current_editor.setText(a)
        self.cpp()

    def toggleCase(self):
        selected_text = self.current_editor.selectedText()
        if selected_text:
            toggled_text = selected_text.swapcase()
            self.current_editor.replaceSelectedText(toggled_text)
        else:
            pass


    def insert_php(self):
            a = temp.generate_php_template()
            self.new_document(title="file.php")
            self.current_editor.setText(a)

    def insert_java(self):
        a = temp.generate_java_template("Main")
        self.new_document(title="main.java")
        self.current_editor.setText(a)
        self.java()

    def bash(self):
        Lexers.bash(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def srec(self):
        Lexers.srec(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def idl(self):
        Lexers.idl(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def matlab(self):
        Lexers.matlab(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def tcl(self):
        Lexers.tcl(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def verilog(self):
        Lexers.verilog(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def spice(self):
        Lexers.spice(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def vhdl(self):
        Lexers.vhdl(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def octave(self):
        Lexers.octave(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def fortran77(self):
        Lexers.fortran77(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def tex(self):
        Lexers.tex(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def makefile(self):
        Lexers.makefile(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def markdown(self):
        Lexers.markdown(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def js(self):
        Lexers.js(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def fortran(self):
        Lexers.fortran(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def java(self):
        Lexers.java(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def pastebin(self):
        ModuleFile.pastebin(self)

    def code_formatting(self):
        ModuleFile.code_formatting(self)

    def goto_line(self):
        line_number, ok = QInputDialog.getInt(self, "Goto Line", "Line:")
        if ok:
            self.setCursorPosition(line_number - 1, 0)

    def get_linear_path(self, directory_path):
        components = directory_path.split("/")
        linear_path = " > ".join(components)
        return linear_path

    # ENCODINGS #
    def utf_8(self):
        self.current_editor.setUtf8(True)
    def utf_16(self):
        self.current_editor.SendScintilla(QsciScintilla.SCI_SETCODEPAGE, QsciScintilla.SC_CP_UTF16LE)


    def open_project(self):
        ModuleFile.open_project(self)

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
        ext = text.split(".")[-1]
        self.current_editor = self.create_editor()
        self.editors.append(self.current_editor)
        self.tab_widget.addTab(self.current_editor, text)
        if ext == "md" or ext == "MD":
            self.markdown_new()
        else:
            pass
        self.tab_widget.setCurrentWidget(self.current_editor)
        self.update_linear_dir(text)

    def save(self):
        text_to_save = self.current_editor.text()

        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, "w") as file:
                file.write(text_to_save)
        else:
            self.save_document()

    def change_text_editor(self, index):
        if index < len(self.editors):
            # Set the previous editor as read-only
            if self.current_editor:
                self.current_editor.setReadOnly(True)

            self.current_editor = self.editors[index]
            self.current_editor.cursorPositionChanged.connect(self.update_line_label)

            self.current_editor.setReadOnly(False)

    def undo_document(self):
        self.current_editor.undo()

    def notes(self):
        self.note_dock = QDockWidget("Notes", self)
        self.note_widget = QPlainTextEdit(self.note_dock)
        note_dock.setWidget(self.note_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.note_dock)
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
        messagebox = QMessageBox()
        messagebox.setText(text), messagebox.setWindowTitle("Summary")
        messagebox.exec()

    def paste_document(self):
        self.current_editor.paste()

    def remove_editor(self, index):
        self.tab_widget.removeTab(index)
        if index < len(self.editors):
            del self.editors[index]

    def open_document(self):
        a = ModuleFile.open_document(self)
        text = self.get_linear_path(self.cfpath)
        self.update_linear_dir(text)

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
                + "4.2"
                + "\n"
                + "\n"
                + "Copyright © 2023 Rohan Kishore."
        )
        msg_box = QMessageBox()
        msg_box.setWindowTitle("About")
        msg_box.setText(text_ver)
        msg_box.exec()

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
    qdarktheme.setup_theme(theme, custom_colors={"primary" : theme_color})
    ex = Window()
    ex.setStyleSheet(f'''
           QScrollBar:vertical {{
               border: none;
               background: {editor_bg};
               width:14px;
               margin: 15px 0 15px 0;
               border-radius: 0px;
           }}

           /* HANDLE BAR VERTICAL */
           QScrollBar::handle:vertical {{
               background-color: {theme_color};
               min-height: 30px;
               border-radius: 7px;
           }}

           QScrollBar::handle:vertical:hover {{
               background-color: #d2d2d2;
           }}

           QScrollBar::handle:vertical:pressed {{
               background-color: #d3d3d3;
           }}

       ''')
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
