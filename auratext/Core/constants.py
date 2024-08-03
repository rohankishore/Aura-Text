# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import enum

# File extension lists
supported_file_extentions = {
    #"assembly": [".s", ".S", ".Asm"],
    "ada": [".ads", ".adb"],
    "awk": [".awk"],
    "bash": [".sh"],
    "batch": [".bat",  ".batch"],
    "c": [".c", ".h"],
    "c++": [".c++", ".h++", ".cc", ".hh", ".cpp", ".hpp", ".cxx", ".hxx"],
    "cicode": [".ci"],
    "coffeescript": [".coffee"],
    "csharp": [".cs"],
    "css": [".css"],
    "cython": [".pyx", ".pxd", ".pxi"],
    "d": [".d"],
    "fortran": [".f90", ".f95", ".f03"],
    "fortran77": [".f", ".for"],
    "html": [".html", ".htm", ".svelte"],
    "idl": [".idl"],
    "ini": [".ini"],
    "java": [".java"],
    "javascript": [".js", ".jsx", ".mjs", ".ts", ".tsx",],
    "json": [".json"],
    "lua": [".lua"],
    "nim": [".nim", ".nims", ".nimble"],
    "oberon/modula": [".mod", ".ob", ".ob2", ".cp"],
    "octave": [".m"],
    "pascal": [".pas", ".pp", ".lpr", ".cyp"],
    "perl": [".pl", ".pm"],
    "php": [".php"],
    "postscript": [".ps",],
    "python": [".py", ".pyw", ".pyi", ".scons"],
    "routeros": [".rsc"],
    "ruby": [".rb", ".rbw"],
    "spice": [".cir", ".inp"],
    "smallbasic": [".bas", ],
    "skill": [".il", ".ils"],
    "sql": [".sql"],
    "text": [".txt", ".text"],
    "xml": [".xml", ".tpy"],
    "yaml": [".yml", ".yaml"],
}

# Global enumerations
class FileStatus(enum.Enum):
    OK       = 0
    MODIFIED = 1

class FileType(enum.Enum):
    Text = 0
    Hex  = 1

class CanSave:
    YES = 0
    NO  = 1

class SearchResult(enum.Enum):
    NOT_FOUND = None
    FOUND     = 1
    CYCLED    = 2

class WindowMode(enum.Enum):
    THREE = 0
    ONE   = 1

class MainWindowSide(enum.Enum):
    LEFT  = 0
    RIGHT = 1

class ReplType(enum.Enum):
    SINGLE_LINE = 0
    MULTI_LINE  = 1

class ReplLanguage(enum.Enum):
    Python = 0
    Hy = 1

class Direction(enum.Enum):
    LEFT  = 0
    RIGHT = 1

class SpinDirection(enum.Enum):
    CLOCKWISE         = 0
    COUNTER_CLOCKWISE = 1

class MessageType(enum.Enum):
    ERROR         = 0
    WARNING       = 1
    SUCCESS       = 2
    DIFF_UNIQUE_1 = 3
    DIFF_UNIQUE_2 = 4
    DIFF_SIMILAR  = 5

class HexButtonFocus(enum.Enum):
    NONE   = 0
    TAB    = 1
    WINDOW = 2

class NodeDisplayType(enum.Enum):
    DOCUMENT = 0
    TREE     = 1

class TreeDisplayType(enum.Enum):
    NODES            = 0
    FILES            = 1
    FILES_WITH_LINES = 2

class DialogResult(enum.Enum):
    Ok = 0
    Cancel = 1
    Yes = 2
    No = 3
    Quit = 4
    Close = 5
    Restore = 6
    SaveAllAndQuit = 7
    SaveAndClose = 8
    SaveAndRestore = 9
    SwitchToLargestWindow = 10

# Default user configuration file content
default_config_file_content = '''# -*- coding: utf-8 -*-

##  FILE DESCRIPTION:
##      Normal module with a special name that holds custom user functions/variables.
##      To manipulate the editors/windows, take a look at the QScintilla details at:
##      http://pyqt.sourceforge.net/Docs/QScintilla2
##
##  NOTES:
##      Built-in special function escape sequence: "lit#"
##          (prepend it to escape built-ins like: cmain, set_all_text, lines, ...)

\'\'\'
# These imports are optional as they are already imported 
# by the REPL, I added them here for clarity.
import data
import functions
import settings

# Imported for less typing
from gui import *


# Initialization function that gets executed only ONCE at startup
def first_scan():
    pass

# Example of got to customize the menu font and menu font scaling
#data.custom_menu_scale = 25
#data.custom_menu_font = ("Segoe UI", 10, qt.QFont.Weight.Bold)
#data.custom_menu_scale = None
#data.custom_menu_font = None

def trim_whitespace():
    """
    Remove whitespace from back of every line in the main document
    """
    ll = []
    tab = form.get_tab_by_indication()
    for line in tab.line_list:
        ll.append(line.rstrip())
    tab.line_list = ll
trim_whitespace.autocompletion = "trim_whitespace()"

def align_assignments():
    """
    Align any assignments in the selected lines
    """
    tab = form.get_tab_by_indication()
    new_lines = []
    selected_text = tab.selectedText()
    max_left_size = 0
    for line in selected_text.split('\n'):
        if '=' in line and line.count('=') == 1:
            split_line = line.split('=')
            left_size = len(split_line[0].rstrip())
            if left_size > max_left_size:
                max_left_size = left_size
            new_lines.append(split_line)
        else:
            new_lines.append(line)
    for i in range(len(new_lines)):
        if isinstance(new_lines[i], list):
            new_lines[i] = "{} = {}".format(
                new_lines[i][0].rstrip().ljust(max_left_size, ' '),
                new_lines[i][1].strip()
            )
    tab.replaceSelectedText('\n'.join(new_lines))
align_assignments.autocompletion = "align_assignments()"

# Example function definition with defined autocompletion string
def delete_files_in_dir(extension=None, directory=None):
    # Delete all files with the selected file extension from the directory
    if isinstance(extension, str) == False:
        print("File extension argument must be a string!")
        return
    if directory == None:
        directory = os.getcwd()
    elif os.path.isdir(directory) == False:
        return
    print("Deleting '{:s}' files in:".format(extension))
    print(directory)
    for file in os.listdir(directory):
        file_extension = os.path.splitext(file)[1].lower()
        if file_extension == extension or file_extension == "." + extension:
            os.remove(os.path.join(directory, file))
            print(" - deleted file: {:s}".format(file))
    print("DONE")
delete_files_in_dir.autocompletion = "delete_files_in_dir(extension=\"\", directory=None)"
\'\'\'
'''