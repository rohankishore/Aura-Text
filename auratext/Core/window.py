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
import git
import pyjokes
import qdarktheme
import markdown
import platform
from pyqtconsole.console import PythonConsole
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont, QActionGroup, QFileSystemModel, QPixmap, QIcon, QShortcut, QKeySequence
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
    QStatusBar)
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
    shutil.copytree(copytolocalappdata, local_app_data, dirs_exist_ok=True)
else:
    print(f"Warning: Could not find LocalAppData/AuraText to copy. Checked: {copytolocalappdata}")

cpath = open(f"{local_app_data}/data/CPath_Project.txt", "r+").read()
cfile = open(f"{local_app_data}/data/CPath_File.txt", "r+").read()
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
        self.setFixedWidth(40)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

class PluginActions(QDockWidget):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)

        self.plugin_widget = QWidget()

        self.plugin_layout = QVBoxLayout(self.plugin_widget)
        self.plugin_layout.addStretch(1)

        # Set the widget with the layout as the dock's central widget
        self.setWidget(self.plugin_widget)

    def addPluginAction(self, widget):
        """
        Add a plugin action to the sidebar.

        :param widget: The Widget object to add.
        :return: None
        :param widget:
        :return:
        """

        self.plugin_layout.addWidget(widget)

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

        self.plugin_actions_dock = PluginActions("Plugin Actions", self)

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

        self.current_editor = ""

        if self._config["explorer_default_open"] == "True":
            self.expandSidebar__Explorer()
        else:
            pass

        if cpath == "" or cpath == " ":
            welcome_widget = WelcomeScreen.WelcomeWidget(self)
            self.tab_widget.addTab(welcome_widget, "Welcome")
        else:
            pass

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

        explorer_icon = QIcon(f"{local_app_data}/icons/explorer_unfilled.png")
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

        plugin_icon = QIcon(f"{local_app_data}/icons/extension_unfilled.png")
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

        commit_icon = QIcon(f"{local_app_data}/icons/commit_unselected.png")
        self.commit_button = QPushButton(self)
        self.commit_button.setIcon(commit_icon)
        self.commit_button.clicked.connect(self.gitCommit)
        self.commit_button.setIconSize(QSize(25, 25))
        self.commit_button.setFixedSize(30, 30)
        self.commit_button.setStyleSheet(
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
        self.explorer_button.clicked.connect(self.expandSidebar__Explorer)
        self.plugin_button.clicked.connect(self.expandSidebar__Plugins)

        self.setCentralWidget(self.tab_widget)
        self.statusBar.hide()
        self.editors = []

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
        self.command_palette.hide()
        shortcut = QShortcut(QKeySequence("Ctrl+Shift+P"), self)
        shortcut.activated.connect(self.show_command_palette)

        self.showMaximized()

    def show_command_palette(self):
        self.command_palette.exec()

    def create_editor(self):
        self.text_editor = CodeEditor(self)
        return self.text_editor

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
        if isinstance(currentWidget, (QTextEdit, QsciScintilla)):
            lineNumber, columnNumber, totalLines, words = self.getTextStats(
                currentWidget
            )
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
            self.plugin_button.setIcon(QIcon(f"{local_app_data}/icons/extension_filled.png"))
        else:
            self.plugin_button.setIcon(QIcon(f"{local_app_data}/icons/extension_unfilled.png"))

    def onExplorerDockVisibilityChanged(self, visible):
        if visible:
            self.explorer_button.setIcon(QIcon(f"{local_app_data}/icons/explorer_filled.png"))
        else:
            self.explorer_button.setIcon(QIcon(f"{local_app_data}/icons/explorer_unfilled.png"))

    def onCommitDockVisibilityChanged(self, visible):
        if visible:
            self.commit_button.setIcon(QIcon(f"{local_app_data}/icons/commit_selected.png"))
        else:
            self.commit_button.setIcon(QIcon(f"{local_app_data}/icons/commit_unselected.png"))

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

        self.settings_widget = config_page.ConfigPage(self)
        self.settings_widget.exec()

    def expandSidebar__Plugins(self):
        self.plugin_dock = QDockWidget("Extensions", self)
        self.theme_dock = QDockWidget("Themes", self)
        self.plugin_dock.setMinimumWidth(300)
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

    def expandSidebar__PluginActions(self):
        self.plugin_actions_dock = PluginActions("Plugin Actions")
        background_color = (
            self.plugin_button.palette().color(self.plugin_button.backgroundRole()).name()
        )
        if background_color == "#3574f0":
            self.plugin_actions_dock.destroy()
        else:
            self.plugin_actions_dock.visibilityChanged.connect(
                lambda visible: self.onPluginDockVisibilityChanged(visible)
            )

            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.plugin_actions_dock)

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
        self.gitCommitDock = GitCommit.GitCommitDock(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.gitCommitDock)

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
            f = open(path, "r")
            filedata = f.read()
            f.close()
            self.new_document(title=os.path.basename(path))
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
            self.treeview_project(project_path)

    def additional_prefs(self):
        settings = additional_prefs.SettingsWindow()
        settings.exec()

    def new_document(self, checked=False, title="Scratch 1"):
        self.current_editor = self.create_editor()
        self.current_editor.textChanged.connect(self.updateStatusBar)
        self.current_editor.cursorPositionChanged.connect(self.updateStatusBar)
        self.load_plugins()

        self.editors.append(self.current_editor)
        icon = self.get_icon(title)
        self.tab_widget.addTab(self.current_editor, icon, title)
        self.tab_widget.setCurrentWidget(self.current_editor)

    def custom_new_document(self, title, checked=False):
        self.current_editor = self.create_editor()
        self.current_editor.textChanged.connect(self.updateStatusBar)
        self.current_editor.cursorPositionChanged.connect(self.updateStatusBar)
        self.editors.append(self.current_editor)
        self.tab_widget.addTab(self.current_editor, title)
        if ".html" in title:
            self.html_temp()
        self.tab_widget.setCurrentWidget(self.current_editor)

    def boilerplates(self):
        self.boilerplate_dialog = boilerplates.BoilerPlate(current_editor=self.current_editor)
        self.boilerplate_dialog.show()

    def cs_new_document(self, checked=False):
        text, ok = QInputDialog.getText(None, "New File", "Filename:")
        if text != "":
            ext = text.split(".")[-1]
            self.current_editor = self.create_editor()
            self.current_editor.cursorPositionChanged.connect(self.updateStatusBar)
            self.current_editor.textChanged.connect(self.updateStatusBar)
            self.editors.append(self.current_editor)
            self.tab_widget.addTab(self.current_editor, text)
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
            self.tab_widget.setCurrentWidget(self.current_editor)
        else:
            pass

    def change_text_editor(self, index):
        widget = self.tab_widget.widget(index)
        if index < len(self.editors):
            self.statusBar.show()
            # Set the previous editor as read-only
            if self.current_editor:
                self.current_editor.setReadOnly(True)

            self.current_editor = self.editors[index]

            self.current_editor.setReadOnly(False)

        if self.tab_widget.count() == 0:
            self.statusBar.hide()

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
            self.statusBar.hide()

        if self.tab_widget.count() == 0:
            self.statusBar.hide()

    def open_document(self):
        a = ModuleFile.open_document(self)
        self.load_plugins()

    def open_last_file(self, title=os.path.basename(cfile)):
        try:
            file = open(cfile, "r+")
            self.current_editor = self.create_editor()
            self.current_editor.textChanged.connect(self.updateStatusBar)
            self.current_editor.cursorPositionChanged.connect(self.updateStatusBar)
            text = file.read()
            self.editors.append(self.current_editor)
            self.current_editor.setText(text)
            self.tab_widget.addTab(self.current_editor, title)
            self.tab_widget.setCurrentWidget(self.current_editor)
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
        self.command_palette.search_input.setFocus()
        self.command_palette.search_input.clear()

    @staticmethod
    def bug_report():
        webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Text/issues/new/choose")

    def show_performance(self):
        self.performance_dock = QDockWidget("Performance", self)
        self.performance_widget = Performance.PerformanceWidget(self)
        self.performance_dock.setWidget(self.performance_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.performance_dock)
        self.performance_dock.show()
