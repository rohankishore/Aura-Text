from tkinter import messagebox, filedialog
import requests, os
from PySide6.QtGui import QTextCursor
import webbrowser, base64, pyttsx3, win32clipboard
from PySide6.QtGui import *

api_key_pb = '_L_ZkBp7K3aZMY7z4ombPIztLxITOOpD'
codesnippet_ext = ".py"

def rightSpeak(text):
    if text != "":
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    else:
        messagebox.showerror("Text not found!",
                             "Did you forget to bring your words to the party? Don't worry, just type something "
                             "and let's get this conversation started!")

def Googlesearch(query_google):
    if query_google != "":
        link = str(
            "https://www.google.com/search?q=" + query_google + "&oq=hi&aqs=chrome..69i57j69i59j0i67l2j46i67j69i60j69i61l2.422j0j4&sourceid=chrome&ie=UTF-8")
        webbrowser.open_new_tab(link)
    else:
        messagebox.showerror("No Text Selected!", "Looks like you forgot to highlight any text. "
                                                  "It's okay, we won't judge you for being a little too eager to click that button.")

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
        messagebox.showerror("No Selection!", "Looks like you're taking the non-selective approach today. Select any text to encrypt.")

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
        messagebox.showerror("No Selection!", "Looks like you're taking the non-selective approach today. Select any text to decrypt.")

def load_snippet(self):
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    f = open(file_path)
    snippet_data = f.read()
    cursor = QTextCursor(self.current_editor.document())
    self.current_editor.setTextCursor(cursor)
    self.current_editor.setPlainText(snippet_data)

py_words = ["from", "to", "get", 'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
                 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if',
                 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
                 'while', 'with', 'yield', "print", "__name__ = '__main__'", "self", "__init__"]

def calculate(self):
    stringg = self.textCursor().selectedText()
    try:
        res = int(eval(stringg))
        res = str(res)
        messagebox.showinfo("Result", res)
    except TypeError and NameError:
        messagebox.showerror("Numeric Expression Where??", "Oops! Looks like you forgot to select a numeric expression. "
                            "Are you trying to give me a break? Come on, give me something to calculate here!")

def pastebin(self):
     text_pb = self.current_editor.toPlainText()
     data = {
         'api_dev_key': api_key_pb,
         'api_option': 'paste',
         'api_paste_code': text_pb}
     response = (requests.post('https://pastebin.com/api/api_post.php', data=data)).text
     text = "Your Pastebin link has been copied to the clipboard!"
     messagebox.showinfo("Success!", text)
     win32clipboard.OpenClipboard()
     win32clipboard.EmptyClipboard()
     win32clipboard.SetClipboardText(response)
     win32clipboard.CloseClipboard()

def summary(self):
    doc = self.current_editor.document()
    #char_count = self.current_editor.split(QRegularExpression("(\\s|\\n|\\r)+").QString.SkipEmptyParts).count()
    line_count = str(doc.blockCount())
   # word_count = doc.wordCount()
    text = "Total Number of Lines: " + line_count + "\n" + "Total Character Count: " \
           + "char_count" + "\n" + "Total Word Count: " + "word_count"
    messagebox.showinfo("Summary", text)

def save_snippet(self):
    sample_string = self.current_editor.textCursor().selectedText()
    if sample_string != "":
        name = str(filedialog.asksaveasfilename(title="Save Code Snippet",defaultextension=codesnippet_ext))
        file = open(name ,'w')
        file.write(sample_string)
        file.close()
    else:
        messagebox.showerror("It's empty here!", "Hey there, mind selecting some text before trying to make changes? We can't read your mind... yet.")

def save_document(self):
    try:
        name = str(filedialog.asksaveasfilename(title="Select file",defaultextension='.py'))
        file = open(name ,'w')
        text = self.current_editor.toPlainText()
        file.write(text)
        file.close()
    except FileNotFoundError:
        messagebox.showerror("Don't wanna save your file?", "You can run, but you can't hide from your unsaved changes."
                                                            " Please come back and save your work before it's too late!")

def open_document(self, file_dir):
    if file_dir:
        try:
            f = open(file_dir)
            filedata = f.read()
            self.new_document(title = os.path.basename(file_dir))
            self.current_editor.setPlainText(filedata)
            f.close()
        except FileNotFoundError:
            return
