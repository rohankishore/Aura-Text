import datetime
import importlib
import json
import os
import random
import shutil
import sys
import sqlite3
import time
import webbrowser
import subprocess
import git
import pyjokes
import qdarktheme
import markdown
import platform
from pyqtconsole.console import PythonConsole
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QColor, QFont, QActionGroup, QFileSystemModel, QPixmap, QIcon, QShortcut, QKeySequence, QCursor
from PyQt6.Qsci import QsciScintilla
from PyQt6.QtWidgets import (
    QMainWindow,
    QInputDialog,
    QDockWidget,
    QTextEdit,
    QTreeView,
    QFileDialog,
    QSplashScreen,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStatusBar,
    QMenu,
    QSplitter)
from . import Lexers
from ..Misc import shortcuts, WelcomeScreen, boilerplates, file_templates
from . import MenuConfig
from . import additional_prefs
from . import Modules as ModuleFile
from . import PluginDownload
from . import ThemeDownload
from . import config_page
from .CommandPalette import CommandPalette
from ..Components import powershell, terminal, statusBar, ProjectManager, About, ToDo, GitGraph
from ..Components import powershell, terminal, statusBar, ProjectManager, About, ToDo, GitGraph, GitRebase, Performance, DBViewer
from ..Components.CommandPalette import CommandPalette
from ..Components.NewProjectDialog import NewProjectDialog
from ..Components.Linter import CodeLinter
from .MiniMapWidget import MiniMapWidget
from .svg_icon_manager import SVGIconManager

from .AuraText import CodeEditor
from auratext.Components.TabWidget import TabWidget
from .plugin_interface import Plugin

if platform.system() == "Windows":
    local_app_data = os.getenv('LOCALAPPDATA')
elif platform.system() == "Linux":
    local_app_data = os.path.expanduser("~/.config")
elif platform.system() == "Darwin":
    local_app_data = os.path.expanduser("~/Library/Application Support")
else:
    print("Unsupported operating system")
    sys.exit(1)

local_app_data = os.path.join(local_app_data, "AuraText")

script_dir = os.path.dirname(os.path.abspath(__file__))
# Check dev path first: ../../LocalAppData/AuraText
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
copytolocalappdata = os.path.join(project_root, "LocalAppData", "AuraText")

if not os.path.exists(copytolocalappdata):
    import sys
    exedir = os.path.dirname(sys.executable)
    copytolocalappdata = os.path.join(exedir, "LocalAppData", "AuraText")

if os.path.exists(copytolocalappdata):
    if not os.path.exists(local_app_data):
        os.makedirs(local_app_data)

    for item in os.listdir(copytolocalappdata):
        s = os.path.join(copytolocalappdata, item)
        d = os.path.join(local_app_data, item)

        if item == "data":
            if not os.path.exists(d):
                os.makedirs(d)
            for data_item in os.listdir(s):
                ds = os.path.join(s, data_item)
                dd = os.path.join(d, data_item)
                if not os.path.exists(dd):
                    if os.path.isdir(ds):
                        shutil.copytree(ds, dd)
                    else:
                        shutil.copy2(ds, dd)
        else:
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
else:
    print(f"Warning: Could not find LocalAppData/AuraText to copy. Checked: {copytolocalappdata}")

cpath = open(f"{local_app_data}/data/CPath_Project.txt", "r+").read().strip()
cfile = open(f"{local_app_data}/data/CPath_File.txt", "r+").read().strip()
if not cpath:
    cpath = ""
if not cfile:
    cfile = ""

def is_git_repo():
    return os.path.isdir(os.path.join(cpath, '.git'))


if is_git_repo():
    from ..Components import GitCommit, GitPush
else:
    pass


class Sidebar(QDockWidget):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setFixedWidth(60)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

# noinspection PyUnresolvedReferences
# no inspection for unresolved references as pylance flags inaccurately sometimes
class Window(QMainWindow):
    def __init__(self, greeting=None):
        super().__init__()
        self.local_app_data = local_app_data
        # self._terminal_history = ""

        # project manager db init
        self.conn = sqlite3.connect(f"{self.local_app_data}/data/ProjectManager.db")
        self.dbcursor = self.conn.cursor()

        self.dbcursor.execute('''
            CREATE TABLE IF NOT EXISTS projects(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                path TEXT
            )
        ''')

        # theme file
        with open(f"{local_app_data}/data/theme.json", "r") as themes_file:
            self._themes = json.load(themes_file)

        # config file
        with open(f"{local_app_data}/data/config.json", "r") as config_file:
            self._config = json.load(config_file)

        # terminal history file
        with open(f"{local_app_data}/data/terminal_history.txt", "r+") as thfile:
            self.terminal_history = thfile.readlines()

        # keymap file
        with open(f"{local_app_data}/data/shortcuts.json", "r+") as kmfile:
            self._shortcuts = json.load(kmfile)

        if self._themes["theming"] == "flat":
            # pywinstyles.apply_style(self, "dark")
            qdarktheme.setup_theme(
                self._themes["theme_type"], custom_colors={"primary": self._themes["theme"]}
            )
            if platform.system() == "Windows":
                import pywinstyles
                pywinstyles.apply_style(self, (self._themes["titlebar"]))
        else:
            pass

        self._config["show_setup_info"] = "False"

        def splashScreen():
            # Splash Screen
            splash_pix = ""
            current_time = datetime.datetime.now().time()
            sunrise_time = current_time.replace(hour=6, minute=0, second=0, microsecond=0)
            sunset_time = current_time.replace(hour=18, minute=0, second=0, microsecond=0)

            # Check which time interval the current time falls into
            if sunrise_time <= current_time < sunrise_time.replace(hour=12):
                splash_pix = QPixmap(f"{local_app_data}/icons/splash_morning.png")
            elif sunrise_time.replace(hour=12) <= current_time < sunset_time:
                splash_pix = QPixmap(f"{local_app_data}/icons/splash_afternoon.png")
            else:
                splash_pix = QPixmap(f"{local_app_data}/icons/splash_night.png")

            splash = QSplashScreen(splash_pix)
            splash.show()
            time.sleep(1)
            splash.hide()

        if self._config["splash"] == "True":
            splashScreen()
        else:
            pass

        self.tab_widget = TabWidget()
        self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                padding: 8px;
            }
        """)

        # Create splitter for split view
        self.editor_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.editor_splitter.addWidget(self.tab_widget)
        self.split_tab_widget = None
        self.is_split = False

        self.current_editor = ""

        if self._config["explorer_default_open"] == "True":
            self.expandSidebar__Explorer()
        else:
            pass

        if cpath == "" or cpath == " ":
            welcome_widget = WelcomeScreen.WelcomeWidget(self)
            self.tab_widget.addTab(welcome_widget, "Welcome")
        else:
            self.treeview_project(cpath)

        self.tab_widget.setTabsClosable(True)

        self.md_dock = QDockWidget("Markdown Preview")
        self.mdnew = QDockWidget("Markdown Preview")
        self.ps_dock = QDockWidget("Powershell")

        # Sidebar
        self.sidebar_main = Sidebar("", self)
        self.sidebar_main.setTitleBarWidget(QWidget())
        self.sidebar_widget = QWidget(self.sidebar_main)
        self.sidebar_widget.setStyleSheet(f"QWidget{{background-color: {self._themes['sidebar_bg']};}}")
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.sidebar_main.setWidget(self.sidebar_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar_main)

        self.leftBar = Sidebar("", self)
        self.leftBar.setTitleBarWidget(QWidget())
        self.leftBar_widget = QWidget(self.leftBar)
        self.leftBar_widget.setStyleSheet(f"QWidget{{background-color: {self._themes['sidebar_bg']};}}")
        self.leftBar_layout = QVBoxLayout(self.leftBar_widget)
        self.leftBar_layout.addStretch()
        self.leftBar_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.leftBar.setWidget(self.leftBar_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.leftBar)

        self.statusBar = statusBar.StatusBar(self, greeting=greeting)
        self.setStatusBar(self.statusBar)

        # Track currently selected sidebar button
        self.selected_sidebar_button = None
        
        # Theme color for selected icons
        theme_color = self._themes.get("theme", "#007ACC")
        
        # Create Explorer button with SVG icons
        explorer_svg = f"{local_app_data}/icons/explorer.svg"
        explorer_unselected, explorer_selected = SVGIconManager.create_stateful_icon(
            explorer_svg, None, theme_color, (23, 23)
        )
        
        self.explorer_button = QPushButton(self)
        self.explorer_button.setIcon(explorer_unselected)
        self.explorer_button.setIconSize(QSize(23, 23))
        self.explorer_button.setFixedSize(36, 36)
        self.explorer_button.setStyleSheet(
            """
            QPushButton {
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            """
        )
        self.explorer_button.unselected_icon = explorer_unselected
        self.explorer_button.selected_icon = explorer_selected

        # Create Plugin/Extensions button with SVG icons
        extensions_svg = f"{local_app_data}/icons/extensions.svg"
        plugin_unselected, plugin_selected = SVGIconManager.create_stateful_icon(
            extensions_svg, None, theme_color, (23, 23)
        )
        
        self.plugin_button = QPushButton(self)
        self.plugin_button.setIcon(plugin_unselected)
        self.plugin_button.setIconSize(QSize(23, 23))
        self.plugin_button.setFixedSize(36, 36)
        self.plugin_button.setStyleSheet(
            """
            QPushButton {
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            """
        )
        self.plugin_button.unselected_icon = plugin_unselected
        self.plugin_button.selected_icon = plugin_selected

        # Create Git/Commit button with SVG icons
        git_svg = f"{local_app_data}/icons/git.svg"
        commit_unselected, commit_selected = SVGIconManager.create_stateful_icon(
            git_svg, None, theme_color, (23, 23)
        )
        
        self.commit_button = QPushButton(self)
        self.commit_button.setIcon(commit_unselected)
        self.commit_button.clicked.connect(self.gitCommit)
        self.commit_button.setIconSize(QSize(23, 23))
        self.commit_button.setFixedSize(36, 36)
        self.commit_button.setStyleSheet(
            """
            QPushButton {
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            """
        )
        self.commit_button.unselected_icon = commit_unselected
        self.commit_button.selected_icon = commit_selected

        git_graph_icon = QIcon(f"{local_app_data}/icons/search.png")
        self.git_graph_button = QPushButton(self)
        self.git_graph_button.setIcon(git_graph_icon)
        self.git_graph_button.clicked.connect(self.gitGraph)
        self.git_graph_button.setIconSize(QSize(25, 25))
        self.git_graph_button.setFixedSize(30, 30)
        self.git_graph_button.setStyleSheet(
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

        if self.is_git_repo():
            self.sidebar_layout.insertWidget(2, self.commit_button)
        else:
            pass

        self.sidebar_layout.addStretch()
        self.leftBar_layout.addStretch()
        self.leftBar_layout.addSpacing(45)

        # Connect the button's clicked signal to the slot
        self.explorer_button.clicked.connect(lambda: self.handle_sidebar_button_click(self.explorer_button, self.expandSidebar__Explorer))
        self.plugin_button.clicked.connect(lambda: self.handle_sidebar_button_click(self.plugin_button, self.expandSidebar__Plugins))

        # Create Run button for Python files
        run_svg = f"{local_app_data}/icons/run.svg"
        run_icon, _ = SVGIconManager.create_stateful_icon(
            run_svg, None, theme_color, (20, 20)
        )
        self.run_button = QPushButton(self)
        self.run_button.setIcon(run_icon)
        self.run_button.clicked.connect(self.run_python_file)
        self.run_button.setIconSize(QSize(20, 20))
        self.run_button.setFixedSize(32, 32)
        self.run_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {theme_color};
            }}
            QPushButton:pressed {{
                background-color: {theme_color}bb;
            }}
            """
        )
        self.run_button.setToolTip("Run Python File")
        self.run_button.hide()  # Hidden by default
        
        # Create Split button
        split_svg = f"{local_app_data}/icons/split.svg"
        split_icon, _ = SVGIconManager.create_stateful_icon(
            split_svg, None, theme_color, (20, 20)
        )
        self.split_button = QPushButton(self)
        self.split_button.setIcon(split_icon)
        self.split_button.clicked.connect(self.toggle_split_editor)
        self.split_button.setIconSize(QSize(20, 20))
        self.split_button.setFixedSize(32, 32)
        self.split_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {theme_color};
            }}
            QPushButton:pressed {{
                background-color: {theme_color}bb;
            }}
            """
        )
        self.split_button.setToolTip("Toggle Split Editor")
        
        # Add buttons as corner widget
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(4)
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.split_button)
        self.tab_widget.setCornerWidget(button_container, Qt.Corner.TopRightCorner)

        self.setCentralWidget(self.editor_splitter)
        self.statusBar.hide()
        self.editors = []
        self.linters = {}  # Dictionary to store linters for each editor
        self.tab_file_paths = {}  # Dictionary to store file paths for each tab index

        self.about_dialog = None

        if self._config["open_last_file"] == "True":
            if cfile != "" or cfile != " ":
                self.open_last_file()
                self.statusBar.show()
            else:
                pass
        else:
            pass

        self.action_group = QActionGroup(self)
        self.action_group.setExclusive(True)

        self.tab_widget.setStyleSheet("QTabWidget {border: 10px;}")

        self.tab_widget.currentChanged.connect(self.change_text_editor)
        self.tab_widget.tabCloseRequested.connect(self.remove_editor)
        # self.new_document()
        self.setWindowTitle("Aura Text")
        self.setWindowIcon(QIcon(f"{local_app_data}/icons/icon.ico"))
        self.configure_menuBar()
        sys.path.append(f"{local_app_data}/plugins")
        self.load_plugins()

        # Setup autosave timer (saves every 30 seconds)
        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.start(30000)  # 30 seconds

        self.commands = [
            {"name": "File: New", "action": self.cs_new_document},
            {"name": "File: New from Template - HTML", "action": self.html_temp},
            {"name": "File: New from Template - Python", "action": self.py_temp},
            {"name": "File: New from Template - C++", "action": self.cpp_temp},
            {"name": "File: New from Template - PHP", "action": self.php_temp},
            {"name": "File: New from Template - TeX", "action": self.tex_temp},
            {"name": "File: New from Template - Java", "action": self.java_temp},
            {"name": "File: Open", "action": self.open_document},
            {"name": "File: New Project", "action": self.new_project},
            {"name": "File: New Project from VCS", "action": self.gitClone},
            {"name": "File: Open Project", "action": self.open_project},
            {"name": "File: Open Project as Treeview", "action": self.open_project_as_treeview},
            {"name": "File: Manage Projects", "action": self.manageProjects},
            {"name": "File: Save As", "action": self.save_document},
            {"name": "File: Summary", "action": self.summary},
            {"name": "File: Extensions", "action": self.expandSidebar__Plugins},
            {"name": "File: Settings", "action": self.expandSidebar__Settings},
            {"name": "File: Exit", "action": sys.exit},
            {"name": "File: Performance", "action": self.show_performance},
            {"name": "Edit: Cut", "action": self.cut_document},
            {"name": "Edit: Copy", "action": self.copy_document},
            {"name": "Edit: Paste", "action": self.paste_document},
            {"name": "Edit: Undo", "action": self.undo_document},
            {"name": "Edit: Redo", "action": self.redo_document},
            {"name": "Edit: Find", "action": self.find_in_editor},
            {"name": "View: Full Screen", "action": self.fullscreen},
            {"name": "View: Project Directory", "action": self.expandSidebar__Explorer},
            {"name": "View: AT Terminal", "action": self.terminal_widget},
            {"name": "View: Powershell", "action": self.setupPowershell},
            {"name": "View: Python Console", "action": self.python_console},
            {"name": "View: Read-Only", "action": self.toggle_read_only},
            {"name": "Code: Code Formatting", "action": self.code_formatting},
            {"name": "Code: Boilerplates", "action": self.boilerplates},
            {"name": "Code: Create Snippet", "action": self.create_snippet},
            {"name": "Code: Import Snippet", "action": self.import_snippet},
            {"name": "Tools: Upload to Pastebin", "action": self.pastebin},
            {"name": "Tools: Notes", "action": self.notes},
            {"name": "Tools: To-Do", "action": self.todo},
            {"name": "Tools: Convert to HTML", "action": self.toHTML},
            {"name": "Git: Commit", "action": self.gitCommit},
            {"name": "Git: Push", "action": self.gitPush},
            {"name": "Git: Graph", "action": self.gitGraph},
            {"name": "Git: Interactive Rebase", "action": self.gitRebase},
            {"name": "Preferences: Additional Preferences", "action": self.additional_prefs},
            {"name": "Preferences: Import Theme", "action": self.import_theme},
            {"name": "Help: Keyboard Shortcuts", "action": self.shortcuts},
            {"name": "Help: Getting Started", "action": self.getting_started},
            {"name": "Help: Submit a Bug Report", "action": self.bug_report},
            {"name": "Help: A Byte of Humour!", "action": self.code_jokes},
            {"name": "Help: GitHub", "action": self.about_github},
            {"name": "Help: About", "action": self.version},
        ]

        self.command_palette = CommandPalette(self.commands)
        
        # Setup language button click handler
        self.statusBar.setLanguageClickHandler(self.show_language_menu)
        self.command_palette.hide()
        
        # Keyboard shortcuts
        # Command palette
        shortcut = QShortcut(QKeySequence("Ctrl+Shift+P"), self)
        shortcut.activated.connect(self.show_command_palette)
        
        # File operations
        new_file_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        new_file_shortcut.activated.connect(self.cs_new_document)
        
        open_file_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        open_file_shortcut.activated.connect(self.open_document)
        
        save_file_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_file_shortcut.activated.connect(self.save_document)
        
        close_tab_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        close_tab_shortcut.activated.connect(lambda: self.remove_editor(self.tab_widget.currentIndex()) if self.tab_widget.currentIndex() >= 0 else None)
        
        # Edit operations
        undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        undo_shortcut.activated.connect(self.undo_document)
        
        redo_shortcut = QShortcut(QKeySequence("Ctrl+Y"), self)
        redo_shortcut.activated.connect(self.redo_document)
        
        cut_shortcut = QShortcut(QKeySequence("Ctrl+X"), self)
        cut_shortcut.activated.connect(self.cut_document)
        
        copy_shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        copy_shortcut.activated.connect(self.copy_document)
        
        paste_shortcut = QShortcut(QKeySequence("Ctrl+V"), self)
        paste_shortcut.activated.connect(self.paste_document)
        
        select_all_shortcut = QShortcut(QKeySequence("Ctrl+A"), self)
        select_all_shortcut.activated.connect(lambda: self.current_editor.selectAll() if self.current_editor and self.current_editor != "" else None)
        
        # View operations
        terminal_shortcut = QShortcut(QKeySequence("Ctrl+`"), self)
        terminal_shortcut.activated.connect(self.setupPowershell)
        
        split_shortcut = QShortcut(QKeySequence("Ctrl+\\"), self)
        split_shortcut.activated.connect(self.toggle_split_editor)
        
        fullscreen_shortcut = QShortcut(QKeySequence("F11"), self)
        fullscreen_shortcut.activated.connect(self.fullscreen)
        
        # Code operations
        run_shortcut = QShortcut(QKeySequence("Shift+F5"), self)
        run_shortcut.activated.connect(self.run_python_file)
        
        find_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        find_shortcut.activated.connect(self.find_in_editor)
        
        format_shortcut = QShortcut(QKeySequence("Shift+Alt+F"), self)
        format_shortcut.activated.connect(self.code_formatting)
        
        settings_shortcut = QShortcut(QKeySequence("Ctrl+,"), self)
        settings_shortcut.activated.connect(self.expandSidebar__Settings)

        self.showMaximized()

    def show_command_palette(self):
        self.command_palette.exec()

    def create_editor(self, file_path=""):
        # Create container widget for editor + minimap
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create editor
        self.text_editor = CodeEditor(self)
        
        # Create minimap
        minimap = MiniMapWidget(self.text_editor, container)
        
        # Add to layout
        layout.addWidget(self.text_editor)
        layout.addWidget(minimap)
        
        # Store minimap reference on editor
        self.text_editor.minimap = minimap
        
        # Check if minimap should be visible (default to True)
        if not hasattr(self, 'minimap_visible'):
            self.minimap_visible = True
        minimap.setVisible(self.minimap_visible)
        
        # Initialize linter for Python files if enabled
        if self._config.get("enable_linter", "True") == "True":
            if file_path.endswith('.py') or not file_path:
                linter_types = self._config.get("linter_types", "flake8").split(",")
                linter = CodeLinter(self.text_editor, file_path, linter_types)
                self.linters[id(self.text_editor)] = linter
        
        return container

    def getTextStats(self, widget):
        if isinstance(widget, QTextEdit):
            cursor = widget.textCursor()
            text = widget.toPlainText()
            return (
                cursor.blockNumber() + 1,
                cursor.columnNumber() + 1,
                widget.document().blockCount(),
                len(text.split()),
            )
        elif isinstance(widget, QsciScintilla):
            lineNumber, columnNumber = widget.getCursorPosition()
            text = widget.text()
            return (
                lineNumber + 1,
                columnNumber + 1,
                widget.lines(),
                len(text.split()),
            )

    def updateStatusBar(self):
        currentWidget = self.tab_widget.currentWidget()
        
        # Get the actual editor from the container
        editor = None
        if currentWidget and hasattr(currentWidget, 'layout') and currentWidget.layout():
            for i in range(currentWidget.layout().count()):
                item = currentWidget.layout().itemAt(i)
                if item and isinstance(item.widget(), (QTextEdit, QsciScintilla, CodeEditor)):
                    editor = item.widget()
                    break
        
        # Fall back to checking if currentWidget itself is an editor
        if not editor and isinstance(currentWidget, (QTextEdit, QsciScintilla)):
            editor = currentWidget
        
        if editor:
            lineNumber, columnNumber, totalLines, words = self.getTextStats(editor)
            self.statusBar.updateStats(lineNumber, columnNumber, totalLines, words)

            if self.current_editor == "":
                editMode = "Edit" if not currentWidget.isReadOnly() else "ReadOnly"
                if self.current_editor != "":
                    self.statusBar.updateEditMode(editMode)
                else:
                    pass
            else:
                editMode = "Edit" if not self.current_editor.isReadOnly() else "ReadOnly"
                if self.current_editor != "":
                    self.statusBar.updateEditMode(editMode)
                else:
                    pass

    def load_plugins(self):
        self.plugins = []
        plugin_files = [
            f.split(".")[0] for f in os.listdir(f"{local_app_data}/plugins") if f.endswith(".py")
        ]
        print("Plugins Found: ", plugin_files)
        sys.path.append(f"{local_app_data}/plugins")
        for plugin_file in plugin_files:
            print(f"Loading plugin: {plugin_file}")
            if not plugin_file.isidentifier():
                print(f"Skipping plugin with invalid name: {plugin_file}")
                continue
            try:
                module = importlib.import_module(plugin_file)
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type) and issubclass(obj, Plugin) and obj is not Plugin:
                        try:
                            self.plugins.append(obj(self))
                        except Exception as e:
                            print(f"Error initializing plugin {plugin_file}: {e}")
            except Exception as e:
                print(f"Error loading plugin {plugin_file}: {e}")

    def onPluginDockVisibilityChanged(self, visible):
        if visible:
            if hasattr(self.plugin_button, 'selected_icon'):
                self.plugin_button.setIcon(self.plugin_button.selected_icon)
        else:
            if hasattr(self.plugin_button, 'unselected_icon'):
                self.plugin_button.setIcon(self.plugin_button.unselected_icon)

    def onExplorerDockVisibilityChanged(self, visible):
        if visible:
            if hasattr(self.explorer_button, 'selected_icon'):
                self.explorer_button.setIcon(self.explorer_button.selected_icon)
        else:
            if hasattr(self.explorer_button, 'unselected_icon'):
                self.explorer_button.setIcon(self.explorer_button.unselected_icon)

    def onCommitDockVisibilityChanged(self, visible):
        if visible:
            if hasattr(self.commit_button, 'selected_icon'):
                self.commit_button.setIcon(self.commit_button.selected_icon)
        else:
            if hasattr(self.commit_button, 'unselected_icon'):
                self.commit_button.setIcon(self.commit_button.unselected_icon)

    def treeview_project(self, path):
        self.dock = QDockWidget("Explorer", self)
        self.dock.visibilityChanged.connect(
            lambda visible: self.onExplorerDockVisibilityChanged(visible)
        )
        # dock.setStyleSheet("QDockWidget { background-color: #191a1b; color: white;}")
        self.dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        tree_view = QTreeView()
        self.model = QFileSystemModel()
        bg = self._themes["sidebar_bg"]
        tree_view.setStyleSheet(
            f"QTreeView {{background-color: {bg}; color: white; border: none; }}"
        )
        tree_view.setModel(self.model)
        tree_view.setRootIndex(self.model.index(path))
        self.model.setRootPath(path)
        self.dock.setWidget(tree_view)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        tree_view.setFont(QFont("Consolas"))

        tree_view.setColumnHidden(1, True)  # File type column
        tree_view.setColumnHidden(2, True)  # Size column
        tree_view.setColumnHidden(3, True)  # Date modified column

        tree_view.doubleClicked.connect(self.open_file)
    
    def handle_sidebar_button_click(self, button, action):
        """Handle sidebar button clicks and update icon states"""
        # Reset previous selected button if exists
        if self.selected_sidebar_button and hasattr(self.selected_sidebar_button, 'unselected_icon'):
            self.selected_sidebar_button.setIcon(self.selected_sidebar_button.unselected_icon)
        
        # Set new selected button
        self.selected_sidebar_button = button
        if hasattr(button, 'selected_icon'):
            button.setIcon(button.selected_icon)
        
        # Execute the original action
        action()

    def expandSidebar__Explorer(self):
        self.dock = QDockWidget("Explorer", self)
        self.dock.setMinimumWidth(200)
        self.dock.visibilityChanged.connect(
            lambda visible: self.onExplorerDockVisibilityChanged(visible)
        )
        self.dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        tree_view = QTreeView()

        self.model = QFileSystemModel()
        bg = self._themes["sidebar_bg"]
        tree_view.setStyleSheet(
            f"QTreeView {{background-color: {bg}; color: white; border: none; }}"
        )
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

    def create_snippet(self):
        ModuleFile.CodeSnippets.snippets_gen(self.current_editor)

    def import_snippet(self):
        ModuleFile.CodeSnippets.snippets_open(self.current_editor)

    def expandSidebar__Settings(self):
        # Check if settings tab is already open
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == "Settings":
                self.tab_widget.setCurrentIndex(i)
                return
        
        # Create and add settings tab
        self.settings_widget = config_page.ConfigPage(self)
        settings_icon = QIcon(f"{self.local_app_data}/icons/settings.png")
        self.tab_widget.addTab(self.settings_widget, settings_icon, "Settings")
        self.tab_widget.setCurrentWidget(self.settings_widget)
        self.statusBar.show()

    def expandSidebar__Plugins(self):
        # Remove existing docks if they exist
        if hasattr(self, 'plugin_dock') and self.plugin_dock:
            self.removeDockWidget(self.plugin_dock)
            self.plugin_dock.close()
            self.plugin_dock.deleteLater()
        
        if hasattr(self, 'theme_dock') and self.theme_dock:
            self.removeDockWidget(self.theme_dock)
            self.theme_dock.close()
            self.theme_dock.deleteLater()
        
        # Create new docks with updated design
        self.plugin_dock = QDockWidget("Extensions", self)
        self.theme_dock = QDockWidget("Themes", self)
        self.plugin_dock.setMinimumWidth(300)
        
        # Connect visibility tracking
        self.plugin_dock.visibilityChanged.connect(
            lambda visible: self.onPluginDockVisibilityChanged(visible)
        )
        
        self.plugin_widget = PluginDownload.FileDownloader(self)
        self.plugin_layout = QVBoxLayout()
        self.plugin_layout.addStretch(1)
        self.plugin_layout.addWidget(self.plugin_widget)
        self.plugin_dock.setWidget(self.plugin_widget)

        self.theme_widget = ThemeDownload.ThemeDownloader(self)
        self.theme_layout = QVBoxLayout()
        self.theme_layout.addStretch(1)
        self.theme_layout.addWidget(self.theme_widget)
        self.theme_dock.setWidget(self.theme_widget)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.plugin_dock)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.theme_dock)
        self.tabifyDockWidget(self.theme_dock, self.plugin_dock)

    def addWidget_toPlugin(self, widget):
        self.plugin_layout.addWidget(widget)

    def new_project(self):
        dialog = NewProjectDialog(self)
        if dialog.exec():
            project_details = dialog.get_project_details()
            project_name = project_details["name"]
            project_path = os.path.join(project_details["path"], project_name)

            if not os.path.exists(project_path):
                os.makedirs(project_path)

            if project_details["create_readme"]:
                with open(os.path.join(project_path, "README.md"), "w") as f:
                    f.write(f"# {project_name}")

            with open(f"{self.local_app_data}/data/CPath_Project.txt", "w") as file:
                file.write(project_path)

            messagebox = QMessageBox()
            messagebox.setWindowTitle("New Project"), messagebox.setText(
                f"New project created at {project_path}"
            )
            messagebox.exec()

            self.treeview_project(project_path)
            self.addProjectsToDB(name=project_name, project_path=project_path)

    def code_jokes(self):
        a = pyjokes.get_joke(language="en", category="neutral")
        QMessageBox.information(self, "A Byte of Humour!", a)

    def terminal_widget(self):
        self.terminal_dock = QDockWidget("AT Terminal", self)
        terminal_widget = terminal.AuraTextTerminalWidget(self)
        self.terminal_dock.setWidget(terminal_widget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.terminal_dock)

    def hideTerminal(self):
        self.terminal_dock.hide()

    def setupPowershell(self):
        self.ps_dock = QDockWidget("Powershell")
        self.terminal = powershell.TerminalEmulator()
        self.terminal.setMinimumHeight(100)
        self.ps_dock.setWidget(self.terminal)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.ps_dock)

    def python_console(self):
        self.console_dock = QDockWidget("Python Console", self)
        console_widget = PythonConsole()
        console_widget.eval_in_thread()
        # self.sidebar_layout_Terminal = QVBoxLayout()
        self.console_dock.setWidget(console_widget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.console_dock)

    def hide_pyconsole(self):
        self.console_dock.hide()

    def closeEvent(self, event):
        if self.tab_widget.count() > 0:
            reply = QMessageBox.question(
                self,
                "Save File",
                random.choice(ModuleFile.emsg_save_list),
                QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Save,
            )
            if reply == QMessageBox.StandardButton.Save:
                self.save_document()
                event.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def gitClone(self):
        messagebox = QMessageBox()
        global path
        try:
            from git import Repo

            repo_url, ok = QInputDialog.getText(self, "Git Repo", "URL of the Repository")
            try:
                path = QFileDialog.getExistingDirectory(self, caption="Repo Path")
            except:
                messagebox.setWindowTitle("Path Error"), messagebox.setText(
                    "The folder should be EMPTY! Please try again with an EMPTY folder"
                )
                messagebox.exec()

            try:
                Repo.clone_from(repo_url, path)
                with open(f"{self.local_app_data}/data/CPath_Project.txt", "w") as file:
                    file.write(path)
                messagebox.setWindowTitle("Success!"), messagebox.setText(
                    "The repository has been cloned successfully!"
                )
                messagebox.exec()
                self.treeview_project(path)
            except git.GitCommandError:
                pass

        except ImportError:
            messagebox = QMessageBox()
            messagebox.setWindowTitle("Git Import Error"), messagebox.setText(
                "Aura Text can't find Git in your PC. Make sure Git is installed and has been added to PATH."
            )
            messagebox.exec()

    def markdown_open(self, path_data, file_path=None):
        ModuleFile.markdown_open(self, path_data, file_path)

    def markdown_new(self):
        ModuleFile.markdown_new(self)

    def gitCommit(self):
        # Remove existing dock if it exists
        if hasattr(self, 'gitCommitDock') and self.gitCommitDock:
            self.removeDockWidget(self.gitCommitDock)
            self.gitCommitDock.close()
            self.gitCommitDock.deleteLater()
        
        # Create new dock with updated design
        self.gitCommitDock = GitCommit.GitCommitDock(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.gitCommitDock)

    def run_python_file(self):
        """Run the current Python file"""
        current_index = self.tab_widget.currentIndex()
        
        # Get file path for current tab
        file_path = self.tab_file_paths.get(current_index)
        
        if not file_path:
            QMessageBox.warning(self, "No File", "Please save the file first before running.")
            return
        
        if not file_path.endswith('.py'):
            QMessageBox.warning(self, "Not a Python File", "This is not a Python file.")
            return
        
        # Save the current file before running
        if self.current_editor and self.current_editor != "":
            try:
                with open(file_path, 'w') as f:
                    f.write(self.current_editor.text())
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Failed to save file: {e}")
                return
        
        # Run the Python file in PowerShell
        try:
            subprocess.Popen(
                ['powershell', '-Command', f'python "{file_path}"'],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        except Exception as e:
            QMessageBox.critical(self, "Run Error", f"Failed to run file: {e}")

    def update_run_button_visibility(self):
        """Show/hide run button based on whether current tab is a Python file"""
        current_index = self.tab_widget.currentIndex()
        file_path = self.tab_file_paths.get(current_index, "")
        
        if file_path and file_path.endswith('.py'):
            self.run_button.show()
        else:
            self.run_button.hide()

    def autosave(self):
        """Autosave all open files that have file paths"""
        for tab_index, file_path in self.tab_file_paths.items():
            if file_path and tab_index < self.tab_widget.count():
                widget = self.tab_widget.widget(tab_index)
                if widget and hasattr(widget, 'layout') and widget.layout():
                    for i in range(widget.layout().count()):
                        item = widget.layout().itemAt(i)
                        if item and isinstance(item.widget(), CodeEditor):
                            editor = item.widget()
                            try:
                                with open(file_path, 'w') as f:
                                    f.write(editor.text())
                            except Exception:
                                pass
                            break

    def toggle_split_editor(self):
        """Toggle split editor view"""
        if not self.is_split:
            # Enable split view - check if there's an active editor
            current_index = self.tab_widget.currentIndex()
            if current_index < 0:
                QMessageBox.warning(self, "No File", "Open a file first to use split view.")
                return
            
            current_widget = self.tab_widget.widget(current_index)
            current_title = self.tab_widget.tabText(current_index)
            
            # Get the current editor
            current_editor = None
            if current_widget and hasattr(current_widget, 'layout') and current_widget.layout():
                for i in range(current_widget.layout().count()):
                    item = current_widget.layout().itemAt(i)
                    if item and isinstance(item.widget(), CodeEditor):
                        current_editor = item.widget()
                        break
            
            if not current_editor:
                QMessageBox.warning(self, "No Editor", "Current tab is not a text editor.")
                return
            
            # Create split tab widget
            self.split_tab_widget = TabWidget()
            self.split_tab_widget.setStyleSheet("""
                QTabBar::tab {
                    padding: 8px;
                }
            """)
            self.split_tab_widget.setTabsClosable(True)
            
            # Create a new editor container with same content
            split_container = QWidget()
            split_layout = QHBoxLayout(split_container)
            split_layout.setContentsMargins(0, 0, 0, 0)
            split_layout.setSpacing(0)
            
            # Create split editor
            split_editor = CodeEditor(self)
            split_editor.setText(current_editor.text())
            
            # Create minimap for split editor
            split_minimap = MiniMapWidget(split_editor, split_container)
            split_editor.minimap = split_minimap
            
            # Add to layout
            split_layout.addWidget(split_editor)
            split_layout.addWidget(split_minimap)
            
            # Add to split tab widget
            icon = self.get_icon(current_title)
            self.split_tab_widget.addTab(split_container, icon, current_title)
            
            # Set up bidirectional sync
            def sync_to_split():
                if split_editor and not getattr(sync_to_split, 'syncing', False):
                    sync_from_main.syncing = True
                    split_editor.setText(current_editor.text())
                    sync_from_main.syncing = False
            
            def sync_from_main():
                if current_editor and not getattr(sync_from_main, 'syncing', False):
                    sync_to_split.syncing = True
                    current_editor.setText(split_editor.text())
                    sync_to_split.syncing = False
            
            current_editor.textChanged.connect(sync_to_split)
            split_editor.textChanged.connect(sync_from_main)
            
            # Store sync references to prevent garbage collection
            self.split_sync_handlers = (sync_to_split, sync_from_main, split_editor, current_editor)
            
            # Add to splitter
            self.editor_splitter.addWidget(self.split_tab_widget)
            self.editor_splitter.setSizes([self.width() // 2, self.width() // 2])
            self.is_split = True
        else:
            # Disable split view
            if self.split_tab_widget:
                # Disconnect sync handlers
                if hasattr(self, 'split_sync_handlers'):
                    sync_to_split, sync_from_main, split_editor, current_editor = self.split_sync_handlers
                    try:
                        current_editor.textChanged.disconnect(sync_to_split)
                        split_editor.textChanged.disconnect(sync_from_main)
                    except:
                        pass
                    self.split_sync_handlers = None
                
                self.editor_splitter.widget(1).deleteLater()
                self.split_tab_widget = None
                self.is_split = False

    def toggle_minimap(self):
        """Toggle minimap visibility for all editors"""
        self.minimap_visible = not getattr(self, 'minimap_visible', True)
        
        # Toggle minimap in main tab widget
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if widget and hasattr(widget, 'layout') and widget.layout():
                for j in range(widget.layout().count()):
                    item = widget.layout().itemAt(j)
                    if item and isinstance(item.widget(), CodeEditor):
                        editor = item.widget()
                        if hasattr(editor, 'minimap'):
                            editor.minimap.setVisible(self.minimap_visible)
                        break
        
        # Toggle minimap in split tab widget if active
        if self.is_split and self.split_tab_widget:
            for i in range(self.split_tab_widget.count()):
                widget = self.split_tab_widget.widget(i)
                if widget and hasattr(widget, 'layout') and widget.layout():
                    for j in range(widget.layout().count()):
                        item = widget.layout().itemAt(j)
                        if item and isinstance(item.widget(), CodeEditor):
                            editor = item.widget()
                            if hasattr(editor, 'minimap'):
                                editor.minimap.setVisible(self.minimap_visible)
                            break

    def gitPush(self):
        self.gitPushDialog = GitPush.GitPushDialog(self)
        self.gitPushDialog.exec()

    def gitGraph(self):
        self.git_graph_widget = GitGraph(cpath)
        self.git_graph_widget.show()

    def gitRebase(self):
        self.git_rebase_dialog = GitRebase.GitRebaseDialog(cpath)
        self.git_rebase_dialog.exec()

    def is_git_repo(self):
        return os.path.isdir(os.path.join(cpath, '.git'))

    def open_file(self, index):
        path = self.model.filePath(index)
        image_extensions = ["png", "jpg", "jpeg", "ico", "gif", "bmp"]
        ext = path.split(".")[-1]

        if ext.lower() == "db":
            self.db_viewer = DBViewer(path)
            self.tab_widget.addTab(self.db_viewer, os.path.basename(path))
            self.tab_widget.setCurrentWidget(self.db_viewer)
            return

        if ext.lower() in image_extensions:
            ModuleFile.add_image_tab(self, self.tab_widget, path, os.path.basename(path))
            return

        try:
            f = open(path, "r", encoding='utf-8', errors='ignore')
            filedata = f.read()
            f.close()
            self.new_document(title=os.path.basename(path), file_path=path)
            self.current_editor.insert(filedata)
            if ext.lower() == "md":
                self.markdown_open(filedata, path)

        except UnicodeDecodeError:
            messagebox = QMessageBox()
            messagebox.setWindowTitle("Wrong Filetype!"), messagebox.setText(
                "This file type is not supported!"
            )
            messagebox.exec()
        except FileNotFoundError:
            return
        except Exception as e:
            print(e)
            messagebox = QMessageBox()
            messagebox.setWindowTitle("Error"), messagebox.setText(
                f"An error occurred while opening the file: {e}"
            )
            messagebox.exec()

    def configure_menuBar(self):
        MenuConfig.configure_menuBar(self)

    def addProjectsToDB(self, name, project_path):
        # Check if exists
        self.dbcursor.execute('SELECT id FROM projects WHERE path = ?', (project_path,))
        data = self.dbcursor.fetchone()
        if data:
            # Delete existing to re-insert at top (since we order by ID DESC)
            self.dbcursor.execute('DELETE FROM projects WHERE id = ?', (data[0],))
        
        self.dbcursor.execute('INSERT INTO projects (name, path) VALUES (?, ?)',
                              (name, project_path))
        self.conn.commit()

    def close_project(self):
        self.tab_widget.clear()
        self.editors = []
        self.current_editor = None
        if hasattr(self, 'dock') and self.dock:
            self.removeDockWidget(self.dock)
            self.dock.close()
        
        # Clear current project path
        with open(f"{self.local_app_data}/data/CPath_Project.txt", "w") as file:
            file.write("")
            
        # Show Welcome Screen
        welcome_widget = WelcomeScreen.WelcomeWidget(self)
        self.tab_widget.addTab(welcome_widget, "Welcome")

    def python(self):
        Lexers.python(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def csharp(self):
        Lexers.csharp(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def json(self):
        Lexers.json(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def duplicate_line(self):
        ModuleFile.duplicate_line(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def yaml(self):
        Lexers.yaml(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def xml(self):
        Lexers.xml(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def html(self):
        Lexers.html(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def toggle_read_only(self):
        self.current_editor.setReadOnly(True)
        self.statusBar.editModeLabel.setText("ReadOnly")

    def read_only_reset(self):
        self.current_editor.setReadOnly(False)
        self.statusBar.editModeLabel.setText("Edit")

    def cpp(self):
        Lexers.cpp(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def ruby(self):
        Lexers.ruby(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def perl(self):
        Lexers.perl(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def pascal(self):
        Lexers.pascal(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def css(self):
        Lexers.css(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def sql(self):
        Lexers.sql(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def lua(self):
        Lexers.lua(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def cmake(self):
        Lexers.cmake(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def postscript(self):
        Lexers.postscript(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def asm(self):
        Lexers.asm(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def avs(self):
        Lexers.avs(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def coffeescript(self):
        Lexers.coffeescript(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def batch(self):
        Lexers.bat(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def bash(self):
        Lexers.bash(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def srec(self):
        Lexers.srec(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def idl(self):
        Lexers.idl(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def matlab(self):
        Lexers.matlab(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def tcl(self):
        Lexers.tcl(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def verilog(self):
        Lexers.verilog(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def spice(self):
        Lexers.spice(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def vhdl(self):
        Lexers.vhdl(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def octave(self):
        Lexers.octave(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def fortran77(self):
        Lexers.fortran77(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))
    
    def get_current_language(self):
        """Get the current language/lexer name from the editor"""
        if not self.current_editor or self.current_editor == "":
            return "Plain Text"
        
        try:
            lexer = self.current_editor.lexer()
            if lexer is None:
                return "Plain Text"
            
            # Get the language name from the lexer
            lang = lexer.language()
            if lang:
                return lang
            return "Plain Text"
        except:
            return "Plain Text"
    
    def show_language_menu(self):
        """Show a menu to select a different language"""
        if not self.current_editor or self.current_editor == "":
            QMessageBox.warning(self, "No Editor", "Please open a file first.")
            return
        
        # Create menu with all available languages
        menu = QMenu(self)
        
        # Define all available languages in alphabetical order
        languages = {
            "Assembly": self.asm,
            "AVS": self.avs,
            "Bash": self.bash,
            "Batch": self.batch,
            "C/C++": self.cpp,
            "C#": self.csharp,
            "CMake": self.cmake,
            "CoffeeScript": self.coffeescript,
            "CSS": self.css,
            "Fortran": self.fortran,
            "Fortran77": self.fortran77,
            "HTML": self.html,
            "IDL": self.idl,
            "Java": self.java,
            "JavaScript": self.js,
            "JSON": self.json,
            "Lua": self.lua,
            "Makefile": self.makefile,
            "Markdown": self.markdown,
            "Matlab": self.matlab,
            "Octave": self.octave,
            "Pascal": self.pascal,
            "Perl": self.perl,
            "Plain Text": self.set_plain_text,
            "PostScript": self.postscript,
            "Python": self.python,
            "Ruby": self.ruby,
            "SPICE": self.spice,
            "SQL": self.sql,
            "SREC": self.srec,
            "TCL": self.tcl,
            "TeX": self.tex,
            "Verilog": self.verilog,
            "VHDL": self.vhdl,
            "XML": self.xml,
            "YAML": self.yaml,
        }
        
        # Add actions to menu
        for lang_name in sorted(languages.keys()):
            action = menu.addAction(lang_name)
            action.triggered.connect(lambda checked, ln=lang_name: self.change_language(ln, languages[ln]))
        
        # Show menu at cursor position
        menu.exec(QCursor.pos())
    
    def change_language(self, language_name, language_func):
        """Change the current editor's language"""
        try:
            language_func()
            self.statusBar.updateLanguage(language_name)
        except Exception as e:
            print(f"Error changing language: {e}")
    
    def set_plain_text(self):
        """Remove lexer to set plain text mode"""
        if self.current_editor and self.current_editor != "":
            self.current_editor.setLexer(None)
            self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
            self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))
    
    def update_language_display(self):
        """Update the language display in the status bar"""
        lang = self.get_current_language()
        self.statusBar.updateLanguage(lang)
    
    def auto_detect_language(self, filename):
        """Auto-detect and apply language/lexer based on file extension"""
        if not self.current_editor or self.current_editor == "":
            return
        
        # Get file extension
        ext = filename.split(".")[-1].lower() if "." in filename else ""
        filename_lower = filename.lower()
        
        # Map extensions to language methods
        extension_map = {
            "py": self.python,
            "pyw": self.python,
            "cs": self.csharp,
            "json": self.json,
            "js": self.js,
            "mjs": self.js,
            "yaml": self.yaml,
            "yml": self.yaml,
            "xml": self.xml,
            "html": self.html,
            "htm": self.html,
            "cpp": self.cpp,
            "cc": self.cpp,
            "cxx": self.cpp,
            "c": self.cpp,
            "h": self.cpp,
            "hpp": self.cpp,
            "rb": self.ruby,
            "pl": self.perl,
            "pm": self.perl,
            "pas": self.pascal,
            "css": self.css,
            "sql": self.sql,
            "lua": self.lua,
            "cmake": self.cmake,
            "ps": self.postscript,
            "asm": self.asm,
            "s": self.asm,
            "avs": self.avs,
            "coffee": self.coffeescript,
            "bat": self.batch,
            "cmd": self.batch,
            "sh": self.bash,
            "bash": self.bash,
            "srec": self.srec,
            "idl": self.idl,
            "m": self.matlab,
            "tcl": self.tcl,
            "v": self.verilog,
            "vhdl": self.vhdl,
            "vhd": self.vhdl,
            "sp": self.spice,
            "f": self.fortran,
            "f90": self.fortran,
            "f77": self.fortran77,
            "for": self.fortran77,
            "tex": self.tex,
            "md": self.markdown,
            "markdown": self.markdown,
            "java": self.java,
        }
        
        # Special case for Makefile
        if "makefile" in filename_lower:
            self.makefile()
            return
        
        # Apply language based on extension
        if ext in extension_map:
            extension_map[ext]()

    def tex(self):
        Lexers.tex(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def makefile(self):
        Lexers.makefile(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def markdown(self):
        Lexers.markdown(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def js(self):
        Lexers.js(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def fortran(self):
        Lexers.fortran(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def java(self):
        Lexers.java(self)
        self.current_editor.setMarginsBackgroundColor(QColor(self._themes["margin_theme"]))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def toggle_linter(self, checked):
        """Toggle linter on/off for all editors"""
        self._config["enable_linter"] = "True" if checked else "False"
        
        # Save to config file
        with open(f"{local_app_data}/data/config.json", "w") as config_file:
            json.dump(self._config, config_file, indent=4)
        
        # Apply to all existing linters
        if checked:
            # Enable linters for existing editors
            for editor_id, linter in self.linters.items():
                linter.run_lint()
            QMessageBox.information(self, "Linter Enabled", 
                "Linter is now enabled. Error and warning indicators will appear in Python files.")
        else:
            # Clear markers from all editors
            for editor_id, linter in self.linters.items():
                linter.clear_markers()
            QMessageBox.information(self, "Linter Disabled", 
                "Linter is now disabled. No error/warning indicators will be shown.")


    def pastebin(self):
        ModuleFile.pastebin(self)

    def code_formatting(self):
        ModuleFile.code_formatting(self)

    def goto_line(self):
        line_number, ok = QInputDialog.getInt(self, "Goto Line", "Line:")
        if ok:
            self.setCursorPosition(line_number - 1, 0)

    def manageProjects(self):
        dialog = ProjectManager.ProjectManager(self)
        dialog.exec()

    def toHTML(self):
        index = self.tab_widget.currentIndex()
        tabText = str(self.tab_widget.tabText(index))
        print(tabText)
        if ".md" in tabText:
            mdText = self.current_editor.text()
            HTMLText = markdown.markdown(mdText)
            fileName, _ = QFileDialog.getSaveFileName(self,
                                                      "Save File", "", "All Files(*);;HTML Files(*.html)")
            if fileName:
                with open(fileName, 'w') as f:
                    f.write(HTMLText)
                    QMessageBox.information(self, 'Success!', 'File successfully converted to HTML')

            else:
                pass
        else:
            QMessageBox.warning(self, 'Filetype Error!', 'Please select a Markdown file to convert.')

    def import_theme(self):
        theme_open, _ = QFileDialog.getOpenFileName(self,
                                                    "Open JSON File",
                                                    "",
                                                    "JSON Files (*.json);;All Files (*)",
                                                    "JSON Files (*.json)"
                                                    )
        if theme_open:
            theme_path = os.path.abspath(theme_open)

            import shutil

            shutil.copyfile(theme_path, f'{local_app_data}/data/theme.json')
        else:
            pass

    def show_welcome(self):
        welcome_widget = WelcomeScreen.WelcomeWidget(self)
        self.tab_widget.addTab(welcome_widget, "Welcome")
        self.tab_widget.setCurrentWidget(welcome_widget)

    def shortcuts(self):
        shortcut_dock = shortcuts.Shortcuts()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, shortcut_dock)

    def find_in_editor(self):
        self.current_editor.show_search_dialog()

    def open_project(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        if dialog.exec():
            project_path = dialog.selectedFiles()[0]
            pathh = str(project_path)
            with open(f"{self.local_app_data}/data/CPath_Project.txt", "w") as file:
                file.write(pathh)
            messagebox = QMessageBox()
            messagebox.setWindowTitle("New Project"), messagebox.setText(
                f"New project created at {project_path}"
            )
            if is_git_repo():
                self.commit_button.hide()
                self.sidebar_layout.insertWidget(2, self.commit_button)
                self.commit_button.show()
            else:
                self.commit_button.hide()
            messagebox.exec()
            self.treeview_project(project_path)
            self.addProjectsToDB(name=(os.path.basename(project_path)), project_path=pathh)
        else:
            pass

    def open_project_as_treeview(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        if dialog.exec():
            project_path = dialog.selectedFiles()[0]
            pathh = str(project_path)
            with open(f"{self.local_app_data}/data/CPath_Project.txt", "w") as file:
                file.write(pathh)
            self.treeview_project(project_path)

    def additional_prefs(self):
        settings = additional_prefs.SettingsWindow()
        settings.exec()

    def new_document(self, checked=False, title="Scratch 1", file_path=""):
        container = self.create_editor(file_path)
        self.current_editor = self.text_editor  # text_editor is set in create_editor
        self.current_editor.textChanged.connect(self.updateStatusBar)
        self.current_editor.cursorPositionChanged.connect(self.updateStatusBar)
        self.load_plugins()

        self.editors.append(self.current_editor)
        icon = self.get_icon(title)
        self.tab_widget.addTab(container, icon, title)
        tab_index = self.tab_widget.indexOf(container)
        # Store file path for this tab
        if file_path:
            self.tab_file_paths[tab_index] = file_path
        self.tab_widget.setCurrentWidget(container)
        # Auto-detect and set language based on file extension
        self.auto_detect_language(file_path if file_path else title)
        self.update_language_display()
        self.update_run_button_visibility()
        # Update status bar to show initial stats
        self.updateStatusBar()

    def custom_new_document(self, title, checked=False):
        container = self.create_editor()
        self.current_editor = self.text_editor
        self.current_editor.textChanged.connect(self.updateStatusBar)
        self.current_editor.cursorPositionChanged.connect(self.updateStatusBar)
        self.editors.append(self.current_editor)
        self.tab_widget.addTab(container, title)
        if ".html" in title:
            self.html_temp()
        self.tab_widget.setCurrentWidget(container)

    def boilerplates(self):
        self.boilerplate_dialog = boilerplates.BoilerPlate(current_editor=self.current_editor)
        self.boilerplate_dialog.show()

    def cs_new_document(self, checked=False):
        text, ok = QInputDialog.getText(None, "New File", "Filename:")
        if text != "":
            ext = text.split(".")[-1]
            container = self.create_editor(text)
            self.current_editor = self.text_editor
            self.current_editor.cursorPositionChanged.connect(self.updateStatusBar)
            self.current_editor.textChanged.connect(self.updateStatusBar)
            self.editors.append(self.current_editor)
            self.tab_widget.addTab(container, text)
            if ".html" in text:
                self.html_temp()
                self.html()
            if ".py" in text:
                self.py_temp()
                self.python()
            if ".css" in text:
                self.css_temp()
                self.css()
            if ".php" in text:
                self.php_temp()
            if ".tex" in text:
                self.tex_temp()
                self.tex()
            if ".java" in text:
                self.java_temp()
                self.java()
            self.load_plugins()
            if os.path.isfile(f"{local_app_data}/plugins/Markdown.py"):
                self.markdown_new()
            else:
                pass
            self.tab_widget.setCurrentWidget(container)
            # Update language display
            self.update_language_display()
        else:
            pass

    def change_text_editor(self, index):
        widget = self.tab_widget.widget(index)
        
        # Check if this is a non-editor tab (like Welcome screen, DB viewer, etc.)
        from auratext.Misc import WelcomeScreen
        from auratext.Components.DBViewer import DBViewer
        
        if isinstance(widget, (WelcomeScreen.WelcomeWidget, DBViewer)):
            self.statusBar.hide()
            self.run_button.hide()
            return
        
        # Get the actual editor from the container
        if widget and hasattr(widget, 'layout') and widget.layout():
            # The editor is the first item in the layout
            editor_found = False
            for i in range(widget.layout().count()):
                item = widget.layout().itemAt(i)
                if item and isinstance(item.widget(), CodeEditor):
                    editor = item.widget()
                    editor_found = True
                    self.statusBar.show()
                    # Set the previous editor as read-only
                    if self.current_editor and self.current_editor != "":
                        try:
                            self.current_editor.setReadOnly(True)
                        except:
                            pass
                    
                    self.current_editor = editor
                    self.current_editor.setReadOnly(False)
                    # Update language display
                    self.update_language_display()
                    # Update run button visibility
                    self.update_run_button_visibility()
                    # Update status bar
                    self.updateStatusBar()
                    break
            
            # If no editor found in the layout, hide status bar
            if not editor_found:
                self.statusBar.hide()
                self.run_button.hide()

        if self.tab_widget.count() == 0:
            self.statusBar.hide()
            self.run_button.hide()

    def undo_document(self):
        self.current_editor.undo()

    def html_temp(self):
        text = file_templates.generate_html_template()
        self.current_editor.append(text)

    def py_temp(self):
        text = file_templates.generate_python_template()
        self.current_editor.append(text)

    def php_temp(self):
        text = file_templates.generate_php_template()
        self.current_editor.append(text)

    def tex_temp(self):
        text = file_templates.generate_tex_template()
        self.current_editor.append(text)

    def java_temp(self):
        text = file_templates.generate_java_template("Welcome")
        self.current_editor.append(text)

    def cpp_temp(self):
        text = file_templates.generate_cpp_template()
        self.current_editor.append(text)

    def notes(self):
        note_dock = QDockWidget("Notes", self)
        note_widget = QPlainTextEdit(note_dock)
        note_widget.setFont(QFont(self._themes["font"]))
        note_dock.setWidget(note_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, note_dock)
        note_dock.show()

    def todo(self):
        todo_dialog = ToDo.ToDoApp()
        todo_dialog.exec()

    def redo_document(self):
        self.current_editor.redo()

    def cut_document(self):
        self.current_editor.cut()

    def copy_document(self):
        self.current_editor.copy()

    def summary(self):
        text = self.current_editor.text()
        lines = text.count('\n') + 1 if text else 0
        words = len(text.split())
        chars_with_spaces = len(text)
        chars_no_spaces = len(text.replace(' ', '').replace('\n', '').replace('\r', ''))
        try:
            bytes_count = len(text.encode('utf-8'))
        except Exception:
            bytes_count = chars_with_spaces

        summary = (
            f"Lines: {lines}\n"
            f"Words: {words}\n"
            f"Characters (with spaces): {chars_with_spaces}\n"
            f"Characters (no spaces): {chars_no_spaces}\n"
            f"Bytes: {bytes_count}"
        )
        msg = QMessageBox()
        msg.setWindowTitle("Document Statistics")
        msg.setText(summary)
        msg.exec()

    def paste_document(self):
        self.current_editor.paste()

    def remove_editor(self, index):
        # Remove file path from tracking
        if index in self.tab_file_paths:
            del self.tab_file_paths[index]
        
        # Update indices for remaining tabs
        new_paths = {}
        for tab_index, path in self.tab_file_paths.items():
            if tab_index > index:
                new_paths[tab_index - 1] = path
            else:
                new_paths[tab_index] = path
        self.tab_file_paths = new_paths
        
        # Remove the tab
        self.tab_widget.removeTab(index)
        
        # Update run button visibility after tab removal
        self.update_run_button_visibility()
        if index < len(self.editors):
            del self.editors[index]
            self.statusBar.hide()

        if self.tab_widget.count() == 0:
            self.statusBar.hide()

    def open_document(self):
        a = ModuleFile.open_document(self)
        self.load_plugins()

    def open_last_file(self, title=os.path.basename(cfile)):
        try:
            file = open(cfile, "r+")
            container = self.create_editor(cfile)
            self.current_editor = self.text_editor
            self.current_editor.textChanged.connect(self.updateStatusBar)
            self.current_editor.cursorPositionChanged.connect(self.updateStatusBar)
            text = file.read()
            self.editors.append(self.current_editor)
            self.current_editor.setText(text)
            self.tab_widget.addTab(container, title)
            tab_index = self.tab_widget.indexOf(container)
            # Store file path for this tab
            self.tab_file_paths[tab_index] = cfile
            self.tab_widget.setCurrentWidget(container)
            self.update_run_button_visibility()
            self.updateStatusBar()
        except FileNotFoundError and OSError:
            pass

    def save_document(self):
        ModuleFile.save_document(self)

    @staticmethod
    def about_github():
        webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Notes")

    def version(self):
        try:
            if not self.about_dialog:
                self.about_dialog = About.AboutAppDialog()
            self.about_dialog.exec()
            self.about_dialog.raise_()
        except Exception as e:
            print(e)

    @staticmethod
    def getting_started():
        webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Text/wiki")

    @staticmethod
    def buymeacoffee():
        webbrowser.open_new_tab("https://ko-fi.com/rohankishore")

    def fullscreen(self):
        if not self.isFullScreen():
            self.showFullScreen()
        else:
            self.showMaximized()

    def show_command_palette(self):
        self.command_palette.show()
        # Center the palette
        geo = self.geometry()
        x = geo.x() + (geo.width() - self.command_palette.width()) // 2
        y = geo.y() + 50  # Show near top
        self.command_palette.move(x, y)
        self.command_palette.command_input.setFocus()
        self.command_palette.command_input.clear()

    @staticmethod
    def bug_report():
        webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Text/issues/new/choose")

    def show_performance(self):
        self.performance_dock = QDockWidget("Performance", self)
        self.performance_widget = Performance.PerformanceWidget(self)
        self.performance_dock.setWidget(self.performance_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.performance_dock)
        self.performance_dock.show()

    def get_icon(self, title):
        extension = os.path.splitext(title)[1].lower()
        icon_name = None

        mapping = {
            ".ada": "logo_ada.png",
            ".awk": "logo_awk.png",
            ".sh": "logo_bash.png",
            ".bash": "logo_bash.png",
            ".bat": "logo_batch.png",
            ".c": "logo_c.png",
            ".h": "logo_c.png",
            ".cmake": "logo_cmake.png",
            ".coffee": "logo_coffeescript.png",
            ".cpp": "logo_cpp.png",
            ".hpp": "logo_cpp.png",
            ".cs": "logo_csharp.png",
            ".css": "logo_css.png",
            ".pyx": "logo_cython.png",
            ".d": "logo_d.png",
            ".f": "logo_fortran.png",
            ".f90": "logo_fortran.png",
            ".f77": "logo_fortran77.png",
            ".html": "logo_html.png",
            ".htm": "logo_html.png",
            ".idl": "logo_idl.png",
            ".java": "logo_java.png",
            ".js": "logo_javascript.png",
            ".json": "logo_json.png",
            ".lua": "logo_lua.png",
            "makefile": "logo_makefile.png",
            ".m": "logo_matlab.png",
            ".nim": "logo_nim.png",
            ".pas": "logo_pascal.png",
            ".pl": "logo_perl.png",
            ".php": "logo_php.png",
            ".ps": "logo_postscript.png",
            ".py": "logo_python.png",
            ".pyw": "logo_python.png",
            ".rb": "logo_ruby.png",
            ".sql": "logo_sql.png",
            ".tcl": "logo_tcl.png",
            ".tex": "logo_tex.png",
            ".v": "logo_verilog.png",
            ".vhdl": "logo_vhdl.png",
            ".xml": "logo_xml.png",
            ".yaml": "logo_yaml.png",
            ".yml": "logo_yaml.png",
        }

        if title.lower() == "makefile":
            icon_name = mapping["makefile"]
        elif extension in mapping:
            icon_name = mapping[extension]

        if icon_name:
            icon_path = os.path.join(os.path.dirname(__file__), "Resources", "language_icons", icon_name)
            if os.path.exists(icon_path):
                return QIcon(icon_path)

        return QIcon()
