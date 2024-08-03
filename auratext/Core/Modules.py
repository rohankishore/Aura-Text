import random
from tkinter import messagebox, filedialog
import requests
import os
import base64
import pyttsx3
import win32clipboard
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QLabel, QDockWidget, QVBoxLayout, QTextEdit, QTextBrowser

api_key_pastebin = "_L_ZkBp7K3aZMY7z4ombPIztLxITOOpD"

emsg_save_list = [
    "Hey there! Hold on a sec... Are you really sure you wanna quit without saving? I mean, you put a lot of effort into that file. Don't you wanna give it a chance to live its best life?",
    "Warning: Unsaved work detected! If you leave now, you'll make the computer cry. Do you really want to make the computer cry?",
    "Whoa there! You're about to exit without saving. Are you sure you want to risk angering the computer gods? Save your work, mortal!",
    "Stop! Hammer time! You can't touch this app until you save your work",
    "Whoa there! Hold your horses, partner! You can't just ride off into the sunset without saving your work. Y'all gotta hit that save button before you hit the road.",
    "Are you sure you want to quit without saving? Your file is like a newborn baby - it needs to be saved before it can make its way in the world!",
    "Looks like you're trying to exit without saving. That's like leaving the grocery store without paying.",
    "Did you forget to save? Your work is about to disappear like a magician's bunny.",
]

emsg_nocode_list = [
    "Whoa, slow down! It looks like you're trying to use a feature that requires some code to be written. You can't just wing it like a chicken trying to fly without feathers.",
    "It looks like your keyboard is on vacation. Please wake it up and start typing some code so we can work our magic.",
    "Whoops! It seems like you're trying to use a feature that requires some code. Don't worry, I won't tell anyone that you were trying to cheat your way to success. Just write some code and we'll be on our way!",
]

emsg_zerodivision = [
    "Error 404: Reality not found. You can't divide by zero, that's just crazy talk.",
    "Congratulations! You broke math. Dividing by zero is undefined.",
    "Warning: Attempting to divide by zero may cause a rift in the space-time continuum. Please don't.",
    "Sorry, can't divide by zero. It's like trying to split an atom with a spoon.",
    "Whoops! Looks like you divided by the imaginary number i...nfinity.",
]

local_app_data = os.path.join(os.getenv("LocalAppData"), "AuraText")
cfile_path = f"{local_app_data}/data/Cpath_File.txt"

class CodeSnippets:
    def __init__(self):
        super().__init__()

    @staticmethod
    def snippets_gen(editor):
        snippet_text = editor.selectedText()
        name = str(filedialog.asksaveasfilename(title="Select file", defaultextension=".py"))
        file = open(name, "w")
        file.write(snippet_text)

    @staticmethod
    def snippets_open(editor):
        file_dir = filedialog.askopenfilename(
            title="Select file",
        )
        ext = file_dir.split(".")[-1]
        if file_dir:
            try:
                f = open(file_dir, "r")
                try:
                    filedata = f.read()
                    editor.append(filedata)
                    f.close()
                except UnicodeDecodeError:
                    messagebox.showerror("Wrong Filetype!", "This file type is not supported!")
            except FileNotFoundError:
                return


def rightSpeak(text):
    if text != "":
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    else:
        messagebox.showerror(
            "Text not found!",
            "Did you forget to bring your words to the party? Don't worry, just type something "
            "and let's get this conversation started!",
        )


def encypt(self):
    sample_string = self.selectedText()
    if sample_string != "":
        sample_string_bytes = sample_string.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_encoded = base64_bytes.decode("ascii") + "   "
        self.replaceSelectedText(base64_encoded)
    else:
        messagebox.showerror(
            "No Selection!",
            "Looks like you're taking the non-selective approach today. Select any text to encrypt.",
        )


def decode(self):
    base64_string = self.selectedText()
    if base64_string != "":
        base64_bytes = base64_string.encode("ascii")
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii") + "   "
        self.replaceSelectedText(sample_string)
    else:
        messagebox.showerror(
            "No Selection!",
            "Looks like you're taking the non-selective approach today. Select any text to decrypt.",
        )


def markdown_new(self):
    self.mdnew.setStyleSheet("QDockWidget {background-color : #1b1b1b; color : white;}")
    self.mdnew.setMinimumWidth(400)
    self.md_widget = QTextEdit()
    self.md_widget.setReadOnly(True)
    self.md_layout = QVBoxLayout(self.md_widget)
    self.md_layout.addWidget(self.md_widget)
    self.mdnew.setWidget(self.md_widget)
    self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.mdnew)

    def update():
        a = self.current_editor.text()
        self.md_widget.setMarkdown(a)

    self.current_editor.textChanged.connect(update)


def markdown_open(self, path_data):
    try:
        self.md_dock = QDockWidget("Markdown Preview")
        self.md_dock.setStyleSheet("QDockWidget {background-color : #1b1b1b; color : white;}")
        self.md_dock.setMinimumWidth(400)
        self.md_widget = QTextBrowser()
        self.md_widget.setMarkdown(path_data)
        #text = self.current_editor.text()
        #self.md_widget.setMarkdown(text)
        self.md_widget.setReadOnly(True)
        self.md_layout = QVBoxLayout(self.md_widget)
        self.md_layout.addWidget(self.md_widget)
        self.md_dock.setWidget(self.md_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.md_dock)

        def update():
            a = self.current_editor.text()
            self.md_widget.setMarkdown(a)

        self.current_editor.textChanged.connect(update)
    except AttributeError:
        messagebox.showerror("Uh Oh!", "An unknown error is stopping Aura Text from rendering this file. Please try again later. If it's still not fixed, then please open an Issue in the repo")


def calculate(self):
    stringg = self.selectedText()
    try:
        try:
            res = int(eval(stringg))
            res = str(res)
            messagebox.showinfo("Result", res)
        except ZeroDivisionError:
            messagebox.showerror("Can't divide by zero!", random.choice(emsg_zerodivision))
    except TypeError and NameError:
        messagebox.showerror(
            "Numeric Expression Where??",
            "Oops! Looks like you forgot to select a numeric expression. "
            "Are you trying to give me a break? Come on, give me something to calculate here!",
        )


def pastebin(self):
    text_pb = self.current_editor.text()
    if text_pb != "":
        data = {"api_dev_key": api_key_pastebin, "api_option": "paste", "api_paste_code": text_pb}
        response = (requests.post("https://pastebin.com/api/api_post.php", data=data)).text
        text = "Your Pastebin link has been copied to the clipboard!"
        messagebox.showinfo("Success!", text)
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(response)
        win32clipboard.CloseClipboard()
    else:
        messagebox.showerror("No Code Found!", random.choice(emsg_nocode_list))


def summary(self):
    doc = self.current_editor.document()
    # char_count = self.current_editor.split(QRegularExpression("(\\s|\\n|\\r)+").QString.SkipEmptyParts).count()
    line_count = str(doc.blockCount())
    # word_count = doc.wordCount()
    text = (
            "Total Number of Lines: "
            + line_count
            + "\n"
            + "Total Character Count: "
            + "char_count"
            + "\n"
            + "Total Word Count: "
            + "word_count"
    )
    messagebox.showinfo("Summary", text)


def save_document(self):
    try:
        # a = self.tab_widget.
        name = str(filedialog.asksaveasfilename(title="Select file", defaultextension=".py"))
        file = open(name, "w")
        text = self.current_editor.text()
        file.write(text)
        title = os.path.basename(file.name) + "   ~ Aura Text"
        active_tab_index = self.tab_widget.currentIndex()
        self.tab_widget.setTabText(active_tab_index, os.path.basename(file.name))
        self.setWindowTitle(title)
        file.close()
        return
    except FileNotFoundError:
        messagebox.showerror(
            "Don't wanna save your file?",
            "You can run, but you can't hide from your unsaved changes."
            " Please come back and save your work before it's too late!",
        )


def add_image_tab(self, tab, image_path, tab_name):
    label = QLabel()
    pixmap = QPixmap(image_path)
    label.setPixmap(pixmap)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    tab.addTab(label, tab_name)


def open_document(self):
    file_dir = filedialog.askopenfilename(
        title="Select file",
    )
    ext = file_dir.split(".")[-1]
    image_extensions = ["png", "jpg", "jpeg", "ico", "gif", "bmp"]

    if file_dir:
        try:
            if ext in image_extensions:
                add_image_tab(self, self.tab_widget, file_dir, os.path.basename(file_dir))
                return

        except UnicodeDecodeError:
            messagebox.showerror("Wrong Filetype!", "This file type is not supported!")

        try:
            f = open(file_dir, "r")
            c = open(cfile_path, "r+")
            try:
                filedata = f.read()
                if ext == "md" or ext == "MD":
                    self.markdown_open(filedata)
                self.new_document(title=os.path.basename(file_dir))
                self.current_editor.insert(filedata)
                c.truncate(0)
                c.write(file_dir)
                f.close()
            except UnicodeDecodeError:
                messagebox.showerror("Wrong Filetype!", "This file type is not supported!")
        except FileNotFoundError:
            return


def code_formatting(self):
    import autopep8

    og_code = str(self.current_editor.text())
    if og_code != "":
        options = {
            "aggressive": 2,
            "experimental": True,
        }
        clean_code = autopep8.fix_code(og_code, options=options)
        self.custom_new_document(title="Code Formatting")
        self.current_editor.insert(clean_code)
    else:
        messagebox.showerror("Error: No Code Found!", random.choice(emsg_nocode_list))
