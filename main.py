import re
import tkinter as tk
import webbrowser
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator
from tkinter import ttk
from customtkinter import *
import tkinter.filedialog
from tkinter import messagebox
import os
from hashlib import md5
import ModuleFile, SearchMod

font1 = ['Arial', 13]

class Document:
    def __init__(self, Frame, TextWidget, FileDir=''):
        self.file_dir = FileDir
        self.file_name = 'Untitled' if not FileDir else os.path.basename(FileDir)
        self.textbox = TextWidget
        self.status = md5(self.textbox.get(1.0, 'end').encode('utf-8'))

class AutocompleteText(tk.Text):
    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop("autocomplete", None)
        super().__init__(*args, **kwargs)

        # bind on key release, which will happen after tkinter
        # inserts the typed character
        self.bind("<Any-KeyRelease>", self._autocomplete)

        # special handling for tab, which needs to happen on the
        # key _press_
        self.bind("<Tab>", self._handle_tab)

    def _handle_tab(self, event):
        # see if any text has the "autocomplete" tag
        tag_ranges= self.tag_ranges("autocomplete")
        if tag_ranges:
            # move the insertion cursor to the end of
            # the selected text, and then remove the "sel"
            # and "autocomplete" tags
            self.mark_set("insert", tag_ranges[1])
            self.tag_remove("sel", "1.0", "end")
            self.tag_remove("autocomplete", "1.0", "end")

            # prevent the default behavior of inserting a literal tab
            return "break"

    def _autocomplete(self, event):
        if event.char and self.callback:
            # get word preceeding the insertion cursor
            word = self.get("insert-1c wordstart", "insert-1c wordend")

            # pass word to callback to get possible matches
            matches = self.callback(word)

            if matches:
                # autocomplete on the first match
                remainder = matches[0][len(word):]

                # remember the current insertion cursor
                insert = self.index("insert")

                # insert at the insertion cursor the remainder of
                # the matched word, and apply the tag "sel" so that
                # it is selected. Also, add the "autocomplete" text
                # which will make it easier to find later.
                self.insert(insert, remainder, ("sel", "autocomplete"))

                # move the cursor back to the saved position
                self.mark_set("insert", insert)

class Editor:
    def __init__(self, master):
        self.master = master
        self.master.set_appearance_mode("dark")
        self.master.geometry("1250x700")
        self.master.iconbitmap("icon.ico")
        self.master.title("Aura Text")
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.init_dir = os.path.join(os.path.expanduser('~'), 'Desktop')

        self.tabs = {}  # { index, text widget }

        self.nb = ttk.Notebook(master)
        self.nb.bind("<Button-2>", self.close_tab)
        self.nb.bind("<B1-Motion>", self.move_tab)
        self.nb.pack(expand=10, fill="both")
        self.nb.enable_traversal()

        style = ttk.Style()
        style.theme_use("default")

        # Notebook Style
        style.configure('TNotebook', background='#1d1d1d', borderwidth=0.4)
        style.configure('TNotebook.Tab', background='#2b2b2b', foreground='cyan')
        style.map('TNotebook.Tab', background=[("selected", '#1d1d1d')], foreground=[("selected", "light blue")])
        style.configure('Red.TNotebook.Tab', foreground='red')

        self.master.protocol('WM_DELETE_WINDOW', self.exit)

        menubar = tk.Menu(self.master)

        filemenu = tk.Menu(menubar, tearoff=0, background="#2c2f33", foreground="light blue")
        filemenu.add_command(label="New", command=self.new_file)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_command(label="Save As...", command=self.save_as)
        filemenu.add_command(label="Close Tab", command=self.close_tab)
        filemenu.add_command(label="Summary", command=self.summary)
        filemenu.add_command(label="Exit", command=self.exit)

        editmenu = tk.Menu(menubar, tearoff=0, background="#2c2f33", foreground="light blue")
        editmenu.add_command(label="Undo", command=self.undo)
        editmenu.add_command(label="Redo", command=self.cmd_redo)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command=self.cut)
        editmenu.add_command(label="Copy", command=self.copy)
        editmenu.add_command(label="Paste", command=self.paste)
        editmenu.add_command(label="Delete", command=self.delete)
        editmenu.add_command(label="Select All", command=self.select_all)
        editmenu.add_separator()
        editmenu.add_command(label="Duplicate Line", command=self.duplicate_line)
        editmenu.add_command(label="Find & Replace", command=self.find_replace)

        windowmenu = tk.Menu(menubar, tearoff=0, background="#2c2f33", foreground="light blue")
        transparency = tk.Menu(windowmenu, tearoff=False, background="#2c2f33", foreground="light blue")
        windowmenu.add_command(label="Always On Top", command=self.alwaysontop)

        transparency.add_command(label="5%", command=self.Transparent5)
        transparency.add_command(label="10%", command=self.Transparent10)
        transparency.add_command(label="20%", command=self.Transparent20)
        transparency.add_command(label="25%", command=self.Transparent25)
        transparency.add_command(label="30%", command=self.Transparent30)
        transparency.add_command(label="40%", command=self.Transparent40)
        transparency.add_command(label="50%", command=self.Transparent50)
        transparency.add_command(label="75%", command=self.Transparent75)
        transparency.add_command(label="Reset", command=self.resetTransparent)

        windowmenu.add_cascade(label="Transparency", menu=transparency)

        abb = tk.Menu(menubar, tearoff=False, background="#2c2f33", foreground="light blue")
        abb.add_command(label="Learn About Features", command=self.learn_features)
        abb.add_command(label="Bug Report", command=self.bug_report)
        abb.add_separator()
        abb.add_command(label="Current Version", command=self.version)
        abb.add_command(label="GitHub", command=self.about_github)

        formatmenu = tk.Menu(menubar, tearoff=0, background="#2c2f33", foreground="light blue")
        self.word_wrap = tk.BooleanVar()
        formatmenu.add_checkbutton(label="Word Wrap", onvalue=True, offvalue=False, variable=self.word_wrap,
                                   command=self.wrap)

        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Edit", menu=editmenu)
        menubar.add_cascade(label="Format", menu=formatmenu)
        menubar.add_cascade(label="Window", menu=windowmenu)
        menubar.add_cascade(label="Help", menu=abb)
        self.master.config(menu=menubar)

        self.right_click_menu = tk.Menu(self.master, tearoff=0, foreground="light blue", background="#2c2f33")
        self.searchmenu = tk.Menu(self.right_click_menu, tearoff=0, foreground="light blue", background="#2c2f33")
        self.speakmenu = tk.Menu(self.right_click_menu, tearoff=0, foreground="light blue", background="#2c2f33")
        self.encodemenu = tk.Menu(self.right_click_menu, tearoff=0, foreground="light blue", background="#2c2f33")
        self.highlightmenu = tk.Menu(self.right_click_menu, tearoff=0, foreground="light blue", background="#2c2f33")

        self.right_click_menu.add_command(label="Cut                                           Ctrl-X", command=self.cut)
        self.right_click_menu.add_command(label="Copy                                        Ctrl-C", command=self.copy)
        self.right_click_menu.add_command(label="Paste                                        Ctrl-V", command=self.paste)
        self.right_click_menu.add_command(label="Delete", command=self.delete)
        self.right_click_menu.add_command(label="Select All", command=self.select_all)
        self.right_click_menu.add_separator()
        self.speakmenu.add_command(label="Speak", command=self.right_speak)
        self.searchmenu.add_command(label="Wikipedia", command=self.wiki)
        self.searchmenu.add_command(label="StackOverflow", command=self.search_stack)
        self.searchmenu.add_command(label="YouTube", command=self.yt_search)
        self.encodemenu.add_command(label="Encode", command=self.encypt)
        self.encodemenu.add_command(label="Decode", command=self.decode)
        self.highlightmenu.add_command(label="Highlight", command=self.highlight_note)
        self.highlightmenu.add_command(label="Remove Highlight", command=self.clear_highlight)

        self.right_click_menu.add_cascade(label="Highlighting", menu=self.highlightmenu)
        self.right_click_menu.add_cascade(label="Speak", menu=self.speakmenu)
        self.right_click_menu.add_cascade(label="Search In", menu=self.searchmenu)
        self.right_click_menu.add_cascade(label="Encryption", menu=self.encodemenu)

        self.tab_right_click_menu = tk.Menu(self.master, tearoff=0)
        self.tab_right_click_menu.add_command(label="New Tab", command=self.new_file)
        self.nb.bind('<Button-3>', self.right_click_tab)

        first_tab = ttk.Frame(self.nb)
        self.tabs[first_tab] = Document(first_tab, self.create_text_widget(first_tab))
        self.nb.add(first_tab, text='Untitled')

    def get_matches(self, word):
        # For illustrative purposes, pull possible matches from
        # what has already been typed. You could just as easily
        # return a list of pre-defined keywords.
        wordd = self.tabs[self.get_tab()].textbox.get("1.0", "end-1c").split()
        words = ["from", "to", "get", 'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
                 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if',
                 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
                 'while', 'with', 'yield'] + list(wordd)
        matches = [x for x in words if x.startswith(word)]
        return matches

    def create_text_widget(self, frame):
        textbox = AutocompleteText(frame, autocomplete=self.get_matches ,relief='sunken', borderwidth=0, wrap='none', background="#1d1d1d", foreground="white"
                          , insertbackground="cyan", font=("Consolas", 12))

        yscrollbar = CTkScrollbar(frame, command=textbox.yview)
        yscrollbar.pack(side='right', fill='y')

        def auto_indent(event):
            text_ai = event.widget
            line = text_ai.get("insert linestart", "insert")
            match = re.match(r'^(\s+)', line)
            whitespace = match.group(0) if match else ""
            text_ai.insert("insert", f"\n{whitespace}")
            return "break"

        def tab_pressed(event: tk.Event) -> str:
            # Insert the 4 spaces
            self.tabs[self.get_tab()].textbox.insert("insert", " " * 4)
            # Prevent the default tkinter behaviour
            return "break"

        textbox.bind("<Return>", auto_indent)
        textbox.bind("<Tab>", tab_pressed)

        xscrollbar = CTkScrollbar(frame, command=textbox.xview,orientation='horizontal')
        xscrollbar.pack(side='bottom', fill='x')

        textbox.config(yscrollcommand=yscrollbar.set, undo=True, autoseparators=True)
        textbox.config(xscrollcommand=xscrollbar.set)

        textbox.bind('<Control-s>', self.save_file)
        textbox.bind('<Control-o>', self.open_file)
        textbox.bind('<Control-n>', self.new_file)
        textbox.bind('<Control-a>', self.select_all)
        textbox.bind('<Control-w>', self.close_tab)
        textbox.bind('<Button-3>', self.right_click)

        textbox.bind('<Control-F>', self.finder)
        textbox.bind('<Control-f>', self.finder)

        cdg = ColorDelegator()
        cdg.tagdefs['COMMENT'] = {'foreground': 'grey', 'background': '#1d1d1d'}
        cdg.tagdefs['KEYWORD'] = {'foreground': 'orange', 'background': '#1d1d1d'}
        cdg.tagdefs['BUILTIN'] = {'foreground': 'gold', 'background': '#1d1d1d'}
        cdg.tagdefs['STRING'] = {'foreground': '#95e7ad', 'background': '#1d1d1d'}
        cdg.tagdefs['DEFINITION'] = {'foreground': 'gold', 'background': '#1d1d1d'}
        cdg.tagdefs['BRACKETS'] = {'foreground': '#007F7F', 'background': '#1d1d1d'}
        Percolator(textbox).insertfilter(cdg)

        textbox.pack(fill='both', expand=True)
        return textbox

    def open_file(self, *args):
        file_dir = (tkinter
                    .filedialog
                    .askopenfilename(initialdir=self.init_dir, title="Select file",))
        if file_dir:
            try:
                file = open(file_dir)
                new_tab = ttk.Frame(self.nb, borderwidth=0)
                self.tabs[new_tab] = Document(new_tab, self.create_text_widget(new_tab), file_dir)
                self.nb.add(new_tab, text=os.path.basename(file_dir))
                self.nb.select(new_tab)
                self.tabs[new_tab].textbox.insert('end', file.read())
                self.tabs[new_tab].status = md5(self.tabs[new_tab].textbox.get(1.0, 'end').encode('utf-8'))
            except FileNotFoundError:
                return

    def save_as(self):
        curr_tab = self.get_tab()

        file_dir = (tkinter
                    .filedialog
                    .asksaveasfilename(initialdir=self.init_dir, title="Select file",
                                       defaultextension='.txt'))
        if not file_dir:
            return

        if file_dir[-4:] != '.txt':
            file_dir += '.txt'

        self.tabs[curr_tab].file_dir = file_dir
        self.tabs[curr_tab].file_name = os.path.basename(file_dir)
        self.nb.tab(curr_tab, text=self.tabs[curr_tab].file_name)
        file = open(file_dir, 'w')
        file.write(self.tabs[curr_tab].textbox.get(1.0, 'end'))
        file.close()
        self.tabs[curr_tab].status = md5(self.tabs[curr_tab].textbox.get(1.0, 'end').encode('utf-8'))

    def save_file(self, *args):
        curr_tab = self.get_tab()
        if not self.tabs[curr_tab].file_dir:
            self.save_as()
        else:
            with open(self.tabs[curr_tab].file_dir, 'w') as file:
                file.write(self.tabs[curr_tab].textbox.get(1.0, 'end'))
            self.tabs[curr_tab].status = md5(self.tabs[curr_tab].textbox.get(1.0, 'end').encode('utf-8'))

    def new_file(self, *args):
        new_tab = ttk.Frame(self.nb)
        self.tabs[new_tab] = Document(new_tab, self.create_text_widget(new_tab))
        self.tabs[new_tab].textbox.config(wrap='word' if self.word_wrap.get() else 'none')
        self.nb.add(new_tab, text='Untitled')
        self.nb.select(new_tab)

    def copy(self):
        try:
            sel = self.tabs[self.get_tab()].textbox.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.master.clipboard_clear()
            self.master.clipboard_append(sel)
        except tk.TclError:
            pass

    def delete(self):
        try:
            self.tabs[self.get_tab()].textbox.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass

    def cut(self):
        try:
            sel = self.tabs[self.get_tab()].textbox.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.master.clipboard_clear()
            self.master.clipboard_append(sel)
            self.tabs[self.get_tab()].textbox.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass

    def finder(self, e):
        finde = tk.Toplevel()
        finde.title("Find")
        textfindedd = CTkEntry(finde, width=200, text_color="light blue", text_font=("Arial", 12), height=32)
        textfindedd.pack()
        textfindedd.focus_set()
        finde.attributes('-topmost', 1)
        def finded(ee):
            ModuleFile.find(e, self.tabs[self.get_tab()].textbox, textfindedd)
        textfindedd.bind('<KeyPress>', finded)
        textfindedd.bind('KeyRelease', finded)
        textfindedd.bind('<FocusIn>', finded)
        textfindedd.bind('<MouseWheel>', finded)

    # base64 encode
    def encypt(self):
        ModuleFile.encypt(self.tabs[self.get_tab()].textbox)

    def clear_highlight(self):
        st_ind = self.tabs[self.get_tab()].textbox.index("sel.first")
        end_ind = self.tabs[self.get_tab()].textbox.index("sel.last")

        self.tabs[self.get_tab()].textbox.tag_remove("start", st_ind, end_ind)

    # base64 decode
    def decode(self):
        ModuleFile.decode(self.tabs[self.get_tab()].textbox)

    def wrap(self):
        if self.word_wrap.get():
            for index in self.tabs:
                self.tabs[index].textbox.config(wrap="word")
        else:
            for index in self.tabs:
                self.tabs[index].textbox.config(wrap="none")

    def find_replace(self):
        ModuleFile.find_replace(self.tabs[self.get_tab()].textbox)

    def highlight_note(self):
        ModuleFile.highlightText(self.tabs[self.get_tab()].textbox)

    def summary(self):
        ModuleFile.Summary(self.tabs[self.get_tab()].textbox)

    def yt_search(self):
        SearchMod.yt_search(self.tabs[self.get_tab()].textbox)

    def paste(self):
        try:
            self.tabs[self.get_tab()].textbox.insert(tk.INSERT, self.master.clipboard_get())
        except tk.TclError:
            pass

    def duplicate_line(self):
        line = (self.tabs[self.get_tab()].textbox.index("insert"))
        line_start = line + " linestart"
        line_end = line + " lineend"
        line_contents = self.tabs[self.get_tab()].textbox.get(line_start, line_end)
        line_contents = "\n" + line_contents
        self.tabs[self.get_tab()].textbox.insert(line, line_contents)

    def Transparent25(self):
        self.master.attributes('-alpha', 0.75)
    def Transparent20(self):
        self.master.attributes('-alpha', 0.8)
    def Transparent5(self):
        self.master.attributes('-alpha', 0.95)
    def Transparent10(self):
        self.master.attributes('-alpha', 0.9)
    def Transparent30(self):
        self.master.attributes('-alpha', 0.7)
    def Transparent40(self):
        self.master.attributes('-alpha', 0.6)
    def Transparent50(self):
        self.master.attributes('-alpha', 0.5)
    def Transparent60(self):
        self.master.attributes('-alpha', 0.4)
    def Transparent75(self):
        self.master.attributes('-alpha', 0.25)
    def resetTransparent(self):
        self.master.attributes('-alpha', 1)

    def search_stack(self):
        SearchMod.search_stack(self.tabs[self.get_tab()].textbox)

    def right_speak(self):
        notepad_selection = self.tabs[self.get_tab()].textbox.selection_get()
        ModuleFile.rightSpeak(notepad_selection)

    def select_all(self, *args):
        curr_tab = self.get_tab()

        self.tabs[curr_tab].textbox.tag_add(tk.SEL, "1.0", tk.END)

        self.tabs[curr_tab].textbox.mark_set(tk.INSERT, tk.END)
        self.tabs[curr_tab].textbox.see(tk.INSERT)

    def undo(self):
        self.tabs[self.get_tab()].textbox.edit_undo()

    def wiki(self):
        ModuleFile.wiki(self.tabs[self.get_tab()].textbox)

    def cmd_redo(self):
        self.tabs[self.get_tab()].textbox.edit_redo()

    def right_click(self, event):
        self.right_click_menu.post(event.x_root, event.y_root)

    def right_click_tab(self, event):
        self.tab_right_click_menu.post(event.x_root, event.y_root)

    def learn_features(self):
        webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Notes/wiki")

    @staticmethod
    def bug_report():
        webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Notes/issues/new")

    @staticmethod
    def version():
        text_ver = "Current Version: " + "1.1.0"
        messagebox.showinfo("Version Info", text_ver)

    @staticmethod
    def about_github():
        webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Notes")

    def close_tab(self, event=None):
        if event is None or event.type == str(2):
            selected_tab = self.get_tab()
        else:
            try:
                index = event.widget.index('@%d,%d' % (event.x, event.y))
                selected_tab = self.nb._nametowidget(self.nb.tabs()[index])
            except tk.TclError:
                return

        if self.save_changes():
            self.nb.forget(selected_tab)
            self.tabs.pop(selected_tab)

        if self.nb.index("end") == 0:
            self.master.destroy()

    def exit(self):
        if self.save_changes():
            self.master.destroy()
        else:
            return

    def alwaysontop(self):
        self.master.attributes('-topmost', 1)

    def save_changes(self):
        curr_tab = self.get_tab()
        file_dir = self.tabs[curr_tab].file_dir
        if md5(self.tabs[curr_tab].textbox.get(1.0, 'end').encode('utf-8')).digest() != self.tabs[
            curr_tab].status.digest():
            m = messagebox.askyesnocancel('Aura Notes', 'Do you want to save changes to ' + (
                'Untitled' if not file_dir else file_dir) + '?')

            if m is None:
                return False
            elif m is True:
                self.save_file()
            else:
                pass
        return True

    def get_tab(self):
        return self.nb._nametowidget(self.nb.select())

    def move_tab(self, event):
        if self.nb.index("end") > 1:
            y = self.get_tab().winfo_y() - 5
            try:
                self.nb.insert(event.widget.index('@%d,%d' % (event.x, y)), self.nb.select())
            except tk.TclError:
                return

def main():
    root = CTk()
    app = Editor(root)
    root.mainloop()

if __name__ == '__main__':
    main()
