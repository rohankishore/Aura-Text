import random
from tkinter import messagebox, filedialog
import requests
import os
import webbrowser
import base64
import pyttsx3
import win32clipboard
from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor

api_key_pastebin = '_L_ZkBp7K3aZMY7z4ombPIztLxITOOpD'

emsg_save_list = [
    "Hey there! Hold on a sec... Are you really sure you wanna quit without saving? I mean, you put a lot of effort into that file. Don't you wanna give it a chance to live its best life?",
    "Warning: Unsaved work detected! If you leave now, you'll make the computer cry. Do you really want to make the computer cry?",
    "Whoa there! You're about to exit without saving. Are you sure you want to risk angering the computer gods? Save your work, mortal!",
    "Stop! Hammer time! You can't touch this app until you save your work",
    "Whoa there! Hold your horses, partner! You can't just ride off into the sunset without saving your work. Y'all gotta hit that save button before you hit the road.",
    "Are you sure you want to quit without saving? Your file is like a newborn baby - it needs to be saved before it can make its way in the world!",
    "Looks like you're trying to exit without saving. That's like leaving the grocery store without paying.",
    "Did you forget to save? Your work is about to disappear like a magician's bunny.",]

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
    "Whoops! Looks like you divided by the imaginary number i...nfinity.",]


def rightSpeak(text):
    if text != "":
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    else:
        messagebox.showerror(
            "Text not found!",
            "Did you forget to bring your words to the party? Don't worry, just type something "
            "and let's get this conversation started!")


def encypt(self):
    cursor = QTextCursor(self.document())
    sample_string = self.textCursor().selectedText()
    if sample_string != "":
        sample_string_bytes = sample_string.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_encoded = base64_bytes.decode("ascii") + "   "
        self.setTextCursor(cursor)
        self.insertPlainText(base64_encoded)
    else:
        messagebox.showerror(
            "No Selection!",
            "Looks like you're taking the non-selective approach today. Select any text to encrypt.")


def decode(self):
    cursor = QTextCursor(self.document())
    base64_string = self.textCursor().selectedText()
    if base64_string != "":
        base64_bytes = base64_string.encode("ascii")
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii") + "   "
        self.setTextCursor(cursor)
        self.insertPlainText(sample_string)
    else:
        messagebox.showerror(
            "No Selection!",
            "Looks like you're taking the non-selective approach today. Select any text to decrypt.")


def calculate(self):
    stringg = self.textCursor().selectedText()
    try:
        try:
            res = int(eval(stringg))
            res = str(res)
            messagebox.showinfo("Result", res)
        except ZeroDivisionError:
            messagebox.showerror(
                "Can't divide by zero!",
                random.choice(emsg_zerodivision))
    except TypeError and NameError:
        messagebox.showerror(
            "Numeric Expression Where??",
            "Oops! Looks like you forgot to select a numeric expression. "
            "Are you trying to give me a break? Come on, give me something to calculate here!")


def pastebin(self):
    text_pb = self.current_editor.toPlainText()
    data = {
        'api_dev_key': api_key_pastebin,
        'api_option': 'paste',
        'api_paste_code': text_pb}
    response = (
        requests.post(
            'https://pastebin.com/api/api_post.php',
            data=data)).text
    text = "Your Pastebin link has been copied to the clipboard!"
    messagebox.showinfo("Success!", text)
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(response)
    win32clipboard.CloseClipboard()

def goToLine(self, line):
    # Get the QTextDocument object
    doc = self.current_editor.document()

    # Get the QTextBlock object corresponding to the line number
    block = doc.findBlockByLineNumber(line - 1)

    # Set the cursor position to the beginning of the block
    cursor = self.current_editor.textCursor()
    cursor.setPosition(block.position())

    # Set the cursor in the text edit and ensure it's visible
    self.current_editor.setTextCursor(cursor)
    self.current_editor.ensureCursorVisible()

def summary(self):
    doc = self.current_editor.document()
    # char_count = self.current_editor.split(QRegularExpression("(\\s|\\n|\\r)+").QString.SkipEmptyParts).count()
    line_count = str(doc.blockCount())
   # word_count = doc.wordCount()
    text = "Total Number of Lines: " + line_count + "\n" + "Total Character Count: " \
           + "char_count" + "\n" + "Total Word Count: " + "word_count"
    messagebox.showinfo("Summary", text)


def save_document(self):
    try:
        name = str(
            filedialog.asksaveasfilename(
                title="Select file",
                defaultextension='.py'))
        file = open(name, 'w')
        text = self.current_editor.toPlainText()
        file.write(text)
        title = os.path.basename(file.name) + "   ~ Aura Text"
        active_tab_index = self.tab_widget.currentIndex()
        self.tab_widget.setTabText(
            active_tab_index,
            os.path.basename(
                file.name))
        self.setWindowTitle(title)
        file.close()
    except FileNotFoundError:
        messagebox.showerror(
            "Don't wanna save your file?",
            "You can run, but you can't hide from your unsaved changes."
            " Please come back and save your work before it's too late!")


def duplicate_line(self):
    cursor = self.current_editor.textCursor()
    line_number = cursor.blockNumber()
    line_text = cursor.block().text()
    cursor.movePosition(QTextCursor.MoveOperation.EndOfLine)
    cursor.insertText("\n" + line_text)
    self.current_editor.setTextCursor(cursor)
    self.current_editor.ensureCursorVisible()


def reverse_line(self):
    cursor = self.current_editor.textCursor()
    line_number = cursor.blockNumber()
    line_text = str(cursor.block().text())
    line_text_reversed = line_text[::-1]
    cursor.movePosition(QTextCursor.MoveOperation.EndOfLine)
    cursor.insertText("\n" + line_text_reversed)
    self.current_editor.setTextCursor(cursor)
    self.current_editor.ensureCursorVisible()


def search_google(self):
    cursor = QTextCursor(self.document())
    sample_string = self.textCursor().selectedText()
    if sample_string != "":
        link = str(
            "https://www.google.com/search?q=" +
            sample_string +
            "&oq=hi&aqs=chrome..69i57j69i59j0i67l2j46i67j69i60j69i61l2.422j0j4&sourceid=chrome&ie=UTF-8")
        webbrowser.open_new_tab(link)
    else:
        messagebox.showerror(
            "No Selection!",
            "Looks like you're taking the non-selective approach today. Select any text to search in Google.")


def open_document(self):
    file_dir = filedialog.askopenfilename(
        title="Select file",
    )
    if file_dir:
        try:
            f = open(file_dir, "r")
            try:
                filedata = f.read()
                self.new_document(title=os.path.basename(file_dir))
                self.current_editor.setPlainText(filedata)
                f.close()
            except UnicodeDecodeError:
                messagebox.showerror("Wrong Filetype!", "This file type is not supported!")
        except FileNotFoundError:
            return


def open_custom_document(self, file_dir):
    if file_dir:
        try:
            f = open(file_dir, "r")
            filedata = f.read()
            self.new_document(title=os.path.basename(file_dir))
            self.current_editor.setPlainText(filedata)
            f.close()
        except FileNotFoundError:
            return


def new_document(self, title, checked=False):
    self.current_editor = self.create_editor()
    self.editors.append(self.current_editor)
    self.tab_widget.addTab(self.current_editor, title)
    self.tab_widget.setCurrentWidget(self.current_editor)


def code_formatting(self):
    import autopep8
    og_code = str(self.current_editor.toPlainText())
    if og_code != "":
        options = {
            "aggressive": 2,
            "experimental": True,
        }
        clean_code = autopep8.fix_code(og_code, options=options)
        self.custom_new_document(title="Code Formatting")
        self.current_editor.setPlainText(clean_code)
    else:
        messagebox.showerror(
            "Error: No Code Found!",
            random.choice(emsg_nocode_list)
        )


def find_first_match(self, word):
    cursor = self.current_editor.textCursor()
    selection = QTextEdit.ExtraSelection()
    format = QTextCharFormat()
    format.setBackground(QColor("yellow"))
    format.setForeground(QColor("red"))
    selection.format = format
    while cursor.hasSelection() is False:
        cursor = self.current_editor.document().find(word, cursor)
        if cursor is None:
            break
        selection.cursor = cursor
        selection.cursor.movePosition(QTextCursor.WordRight, QTextCursor.KeepAnchor)
        self.current_editor.setExtraSelections([selection])

def searcch_and_highlight_word(self, word):
    cursor = self.current_editor.textCursor()
    format = QTextCharFormat()
    format.setBackground(QColor("yellow"))
    format.setForeground(QColor("red"))
    while cursor.hasSelection() is False:
        cursor = self.current_editor.document().find(word, cursor)
        if cursor is None:
            break
        selection = QTextEdit.ExtraSelection()
        selection.format = format
        selection.cursor = cursor
        selection.cursor.movePosition(QTextCursor.WordRight, QTextCursor.KeepAnchor)
        self.current_editor.setExtraSelections([selection])
        cursor = selection.cursor