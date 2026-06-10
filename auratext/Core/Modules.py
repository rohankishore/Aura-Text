from PyQt6.QtCore import QRegularExpression
import base64
import os
import random
import markdown
import sys
import pyttsx3
import requests
import pyperclip
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QLabel, QDockWidget, QMessageBox, QVBoxLayout, QTextEdit, QTextBrowser
import platform

from auratext.Misc.import_res import notepadequalequalComponentImportPathAppend
sys.path.append(notepadequalequalComponentImportPathAppend)
from notepadequalequal.fileio import retrieve_file

GITHUB_CSS = """
<style>
body {
    font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
    font-size: 16px;
    line-height: 1.5;
    word-wrap: break-word;
    color: #c9d1d9;
    background-color: #0d1117;
    padding: 20px;
}
h1, h2, h3, h4, h5, h6 {
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
    color: #e6edf3;
}
h1 { font-size: 2em; border-bottom: 1px solid #21262d; padding-bottom: 0.3em; }
h2 { font-size: 1.5em; border-bottom: 1px solid #21262d; padding-bottom: 0.3em; }
h3 { font-size: 1.25em; }
h4 { font-size: 1em; }
h5 { font-size: 0.875em; }
h6 { font-size: 0.85em; color: #8b949e; }
p { margin-top: 0; margin-bottom: 16px; }
code {
    font-family: ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace;
    font-size: 85%;
    padding: 0.2em 0.4em;
    margin: 0;
    background-color: rgba(110,118,129,0.4);
    border-radius: 6px;
}
pre {
    padding: 16px;
    overflow: auto;
    font-size: 85%;
    line-height: 1.45;
    background-color: #161b22;
    border-radius: 6px;
}
pre code {
    background-color: transparent;
    padding: 0;
}
blockquote {
    padding: 0 1em;
    color: #8b949e;
    border-left: 0.25em solid #30363d;
    margin: 0 0 16px 0;
}
ul, ol {
    padding-left: 2em;
    margin-top: 0;
    margin-bottom: 16px;
}
table {
    border-spacing: 0;
    border-collapse: collapse;
    margin-top: 0;
    margin-bottom: 16px;
    width: 100%;
}
table th, table td {
    padding: 6px 13px;
    border: 1px solid #30363d;
}
table th {
    font-weight: 600;
    background-color: #161b22;
}
table tr {
    background-color: #0d1117;
    border-top: 1px solid #21262d;
}
table tr:nth-child(2n) {
    background-color: #161b22;
}
img {
    max-width: 100%;
    box-sizing: content-box;
    background-color: #0d1117;
}
hr {
    height: 0.25em;
    padding: 0;
    margin: 24px 0;
    background-color: #30363d;
    border: 0;
}
a {
    color: #58a6ff;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
</style>
"""

api_key_pastebin = "_L_ZkBp7K3aZMY7z4ombPIztLxITOOpD"

emsg_save = "The current file is not saved. Changes may be lost if they are not saved. Do you want to save before exiting?"
emsg_save_list = []
#     "Hey there! Hold on a sec... Are you really sure you wanna quit without saving? I mean, you put a lot of effort into that file. Don't you wanna give it a chance to live its best life?",
#     "Warning: Unsaved work detected! If you leave now, you'll make the computer cry. Do you really want to make the computer cry?",
#     "Whoa there! You're about to exit without saving. Are you sure you want to risk angering the computer gods? Save your work, mortal!",
#     "Stop! Hammer time! You can't touch this app until you save your work",
#     "Whoa there! Hold your horses, partner! You can't just ride off into the sunset without saving your work. Y'all gotta hit that save button before you hit the road.",
#     "Are you sure you want to quit without saving? Your file is like a newborn baby - it needs to be saved before it can make its way in the world!",
#     "Looks like you're trying to exit without saving. That's like leaving the grocery store without paying.",
#     "Did you forget to save? Your work is about to disappear like a magician's bunny.",
# ]
for i in range(8):
    emsg_save_list.append(emsg_save)

emsg_nocode = "The current file is empty or contains no code. Please write some code to use this feature."
emsg_nocode_list = []
#     "Whoa, slow down! It looks like you're trying to use a feature that requires some code to be written. You can't just wing it like a chicken trying to fly without feathers.",
#     "It looks like your keyboard is on vacation. Please wake it up and start typing some code so we can work our magic.",
#     "Whoops! It seems like you're trying to use a feature that requires some code. Don't worry, I won't tell anyone that you were trying to cheat your way to success. Just write some code and we'll be on our way!",
# ]
for i in range(3):
    emsg_nocode_list.append(emsg_nocode)

emsg_zerodivision_str = "This operation is apparently attempting to divide by zero. This is infinity, which is mathematically undefined. Please change your operation to be mathematically valid to continue."
emsg_zerodivision = []
#     "Error 404: Reality not found. You can't divide by zero, that's just crazy talk.",
#     "Congratulations! You broke math. Dividing by zero is undefined.",
#     "Warning: Attempting to divide by zero may cause a rift in the space-time continuum. Please don't.",
#     "Sorry, can't divide by zero. It's like trying to split an atom with a spoon.",
#     "Whoops! Looks like you divided by the imaginary number i...nfinity.",
# ]
for i in range(5):
    emsg_zerodivision.append(emsg_zerodivision_str)

if platform.system() == "Windows":
    local_app_data = os.getenv('LOCALAPPDATA')
    newline = "\r\n"
elif platform.system() == "Linux":
    local_app_data = os.path.expanduser("~/.config")
    newline = "\n"
elif platform.system() == "Darwin":
    local_app_data = os.path.expanduser("~/Library/Application Support")
    newline = "\n"
else:
    print("Unsupported operating system")
    sys.exit(1)
local_app_data = os.path.join(local_app_data, "AuraText")
cfile_path = f"{local_app_data}/data/Cpath_File.txt"

class CodeSnippets:
    def __init__(self):
        super().__init__()

    @staticmethod
    def snippets_gen(editor):
        try:
            snippet_text = editor.selectedText()
        except AttributeError:
            QMessageBox.warning(editor, "No Editor Open", "The current widget is not an editor.")
            return
        filename, ok = QFileDialog.getSaveFileName(None, "Select file", "", "Python Files (*.py);;All Files (*)")[0]
        if not ok:
            return
        name = str(filename)
        file = open(name, "w")
        file.write(snippet_text)

    @staticmethod
    def snippets_open(editor):
        filedirPath, ok = QFileDialog.getOpenFileName(None, "Select file", "", "All Files (*)")
        if not ok:
            return
        file_dir = filedirPath
        ext = file_dir.split(".")[-1]
        if file_dir:
            try:
                try:
                    filedata = retrieve_file(file_dir)
                    editor.append(filedata)
                except UnicodeDecodeError:
                    QMessageBox.warning(None, "Wrong Filetype", "This file type is not supported")
            except FileNotFoundError:
                return


def rightSpeak(text):
    if text != "":
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    else:
        QMessageBox.warning(None, "Text not found", "Please enter something in the text box to convert it to speech.")


def encypt(self):
    sample_string = self.selectedText()
    if sample_string != "":
        sample_string_bytes = sample_string.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_encoded = base64_bytes.decode("ascii") + "   "
        self.replaceSelectedText(base64_encoded)
    else:
        QMessageBox.warning(self, "No Selection", "Please select something to encrypt.")


def decode(self):
    base64_string = self.selectedText()
    if base64_string != "":
        base64_bytes = base64_string.encode("ascii")
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii") + "   "
        self.replaceSelectedText(sample_string)
    else:
        QMessageBox.warning(self, "No Selection", "Please select a base64 string to decrypt.")


def markdown_new(self):
    self.mdnew.setStyleSheet("QDockWidget {background-color : #1b1b1b; color : white;}")
    self.mdnew.setMinimumWidth(400)
    self.md_widget = QTextBrowser()
    self.md_widget.setOpenExternalLinks(True)
    self.md_widget.setStyleSheet("background-color: #0d1117;")
    self.mdnew.setWidget(self.md_widget)
    self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.mdnew)

    def update():
        text = self.current_editor.text()
        html = markdown.markdown(text, extensions=['extra', 'codehilite'])
        full_html = GITHUB_CSS + html
        self.md_widget.setHtml(full_html)

    self.current_editor.textChanged.connect(update)
    update()


def markdown_open(self, path_data, file_path=None):
    try:
        self.md_dock = QDockWidget("Markdown Preview")
        self.md_dock.setStyleSheet("QDockWidget {background-color : #1b1b1b; color : white;}")
        self.md_dock.setMinimumWidth(400)
        self.md_widget = QTextBrowser()
        self.md_widget.setOpenExternalLinks(True)
        self.md_widget.setStyleSheet("background-color: #0d1117;")

        if file_path:
            self.md_widget.setSearchPaths([os.path.dirname(file_path)])

        self.md_dock.setWidget(self.md_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.md_dock)

        def update():
            text = self.current_editor.text()
            html = markdown.markdown(text, extensions=['extra', 'codehilite'])
            full_html = GITHUB_CSS + html
            self.md_widget.setHtml(full_html)

        self.current_editor.textChanged.connect(update)
        update()
    except AttributeError:
        QMessageBox.warning(self, "Not an Editor", "The current widget is not an editor, or no editor is open. Please open one to continue.")


def calculate(self):
    stringg = self.selectedText()
    try:
        try:
            res = int(eval(stringg))
            res = str(res)
            QMessageBox.information(self, "Result", res)
        except ZeroDivisionError:
            QMessageBox.warning(self, "Zero Division Error", random.choice(emsg_zerodivision))
    except TypeError and NameError:
        QMessageBox.warning(self, "Invalid Expression", "Either the expression you entered is not valid, or you have not entered one. Please enter a valid expression to continue.")


def pastebin(self):
    try:
        text_pb = self.current_editor.text()
    except AttributeError:
        QMessageBox.warning(self, "No Editor Open", "The current widget is not an editor.")
        return
    if text_pb != "":
        data = {"api_dev_key": api_key_pastebin, "api_option": "paste", "api_paste_code": text_pb}
        response = (requests.post("https://pastebin.com/api/api_post.php", data=data)).text
        text = "Your Pastebin link has been copied to the clipboard!"
        QMessageBox.information(self, "Success!", text)
        pyperclip.copy(response)
    else:
        QMessageBox.warning(self, "No Code Found!", random.choice(emsg_nocode_list))


def summary(self):
    doc = self.current_editor.document()
    char_count = self.current_editor.split(QRegularExpression("(\\s|\\n|\\r)+").QString.SkipEmptyParts).count()
    line_count = str(doc.blockCount())
    word_count = doc.wordCount()
    text = (
            "Total Number of Lines: "
            + line_count
            + "\n"
            + "Total Character Count: "
            + char_count
            + "\n"
            + "Total Word Count: "
            + word_count
    )
    QMessageBox.information(self, "Summary", text)


def save_document(self, force_dialog=False):
    try:
        active_tab_index = self.tab_widget.currentIndex()
        if active_tab_index < 0:
            return

        existing_path = self.tab_file_paths.get(active_tab_index, "") if hasattr(self, "tab_file_paths") else ""
        current_tab_name = str(self.tab_widget.tabText(active_tab_index)).strip()

        if force_dialog or not existing_path:
            suggested_name = os.path.basename(existing_path) if existing_path else os.path.basename(current_tab_name)
            if not suggested_name:
                suggested_name = "untitled.py"
            filename, ok = QFileDialog.getSaveFileName(None, "Select file", suggested_name, "Python Files (*.py);;All Files (*)")
            if not ok:
                return
            name = filename
            if not name:
                return
        else:
            name = existing_path

        file = open(name, "w", encoding="utf-8", newline=newline)
        text = self.current_editor.text()
        file.write(text)
        title = os.path.basename(file.name) + " ~ Aura Text"
        self.tab_widget.setTabText(active_tab_index, os.path.basename(file.name))
        self.setWindowTitle(title)
        self.current_editor.setModified(False)
        if hasattr(self, "tab_file_paths"):
            self.tab_file_paths[active_tab_index] = name
        if hasattr(self, "update_run_button_visibility"):
            self.update_run_button_visibility()
        file.close()
        return
    except FileNotFoundError:
        QMessageBox.warning(self, "File Not Found", "The file you are trying to save does not exist.")



def add_image_tab(self, tab, image_path, tab_name):
    from PyQt6.QtWidgets import QWidget, QHBoxLayout
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    
    label = QLabel()
    pixmap = QPixmap(image_path)
    label.setPixmap(pixmap)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    layout.addWidget(label)
    tab.addTab(container, tab_name)
    tab.setCurrentWidget(container)



def open_document(self):
    file_dir_path, ok = QFileDialog.getOpenFileName(None, "Select file", "", "All Files (*)")
    if not ok:
        return
    file_dir = file_dir_path
    ext = file_dir.split(".")[-1].lower()
    image_extensions = ["png", "jpg", "jpeg", "ico", "gif", "bmp"]

    if file_dir:
        if ext == "pdf":
            opened = False
            if hasattr(self, "open_pdf_in_app"):
                opened = bool(self.open_pdf_in_app(file_dir))
            pdf_handler = getattr(self, "_latex_pdf_open_handler", None)
            if callable(pdf_handler):
                pdf_handler(file_dir)
            if opened or callable(pdf_handler):
                return

        try:
            if ext in image_extensions:
                add_image_tab(self, self.tab_widget, file_dir, os.path.basename(file_dir))
                return

        except UnicodeDecodeError:
            QMessageBox.warning(self, "Wrong Filetype", "This file type is not supported")

        try:
            try:
                filedata = retrieve_file(file_dir)
                if ext == "md":
                    self.markdown_open(filedata, file_dir)
                self.new_document(title=os.path.basename(file_dir), file_path=file_dir)
                self.current_editor.insert(filedata)
            except UnicodeDecodeError:
                QMessageBox.warning(self, "Wrong Filetype", "This file type is not supported!")
        except FileNotFoundError:
            return


def code_formatting(self):
    import autopep8

    try:
        og_code = str(self.current_editor.text())
    except AttributeError:
        QMessageBox.warning(self, "Not An Editor", "The current widget is not an editor.")
        return
    if og_code != "":
        options = {
            "aggressive": 2,
            "experimental": True,
        }
        clean_code = autopep8.fix_code(og_code, options=options)
        self.custom_new_document(title="Code Formatting")
        self.current_editor.insert(clean_code)
    else:
        QMessageBox.warning(self, "Error: No Code Found!", random.choice(emsg_nocode_list))
