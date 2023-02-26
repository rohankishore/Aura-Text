from datetime import datetime
from tkinter import *
import webbrowser, re, ModuleFile, SearchMod, os, config
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator
from customtkinter import  CTk, CTkCanvas, CTkScrollbar, CTkEntry, CTkToplevel
from tkinter import messagebox, ttk
from hashlib import md5

python_wd = ModuleFile.words

theme_get = "dark" #config.config_json["theme"]
lang_get = "python"  #config.config_json["language"]
fg_get = "white" #config.config_json["foreground"]
bg_get = "#1d1d1d"#config.config_json["background"]
tc_get = "cyan" #config.config_json["txt_cursor"]
font = "Consolas" #config.config_json["font"]
fontsize = 12 #config.config_json["font_size"]


class Document:
    def __init__(self, tkFrame, TextWidget, FileDir=''):
        self.file_dir = FileDir; self.file_name = 'Scratch' if not FileDir else os.path.basename(FileDir); self.textbox = TextWidget; self.status = md5(self.textbox.get(1.0, 'end').encode('utf-8'))

class AuraTextWidget(Text):
    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop("autocomplete", None); super().__init__(*args, **kwargs); self.bind("<Any-KeyRelease>", self._autocomplete)

    def _handle_tab(self, event):
        tag_ranges= self.tag_ranges("autocomplete")
        if tag_ranges:
            self.mark_set("insert", tag_ranges[1]); self.tag_remove("sel", "1.0", "end"); self.tag_remove("autocomplete", "1.0", "end") ; return "break"

    def _autocomplete(self, event):
        if event.char and self.callback:
            word = self.get("insert-1c wordstart", "insert-1c wordend"); matches = self.callback(word)
            if matches:
                remainder = matches[0][len(word):]; insert = self.index("insert"); self.insert(insert, remainder, ("sel", "autocomplete")); self.mark_set("insert", insert)

class Editor:
    def __init__(self, master):
        self.master = master
        self.master.set_appearance_mode(theme_get); self.master.geometry("1250x700"); self.master.iconbitmap("icon.ico"); self.master.title("Aura Text"); self.frame = Frame(self.master); self.frame.pack()

        self.lineNumber = CTkCanvas(self.master, background="#212325", width=80, highlightthickness=0)
        self.lineNumber.pack(side=LEFT, fill=Y, pady=25)
 
        self.wordCount = StringVar()
        self.wordCount.set("Word Count -> 0")

        self.init_dir = os.path.join(os.path.expanduser('~'), 'Desktop')

        self.tabs = {}

        self.nb = ttk.Notebook(master); self.nb.bind("<Button-2>", self.close_tab); self.nb.bind("<B1-Motion>", self.move_tab); self.nb.pack(expand=10, fill="both"); self.nb.enable_traversal(); style = ttk.Style()
        style.theme_use("default"); style.configure('TNotebook', background='#1d1d1d', borderwidth=0.4); style.configure('TNotebook.Tab', background='black', foreground='white'); style.map('TNotebook.Tab', background=[("selected", '#1d1d1d')], foreground=[("selected", "light blue")]); style.configure('Red.TNotebook.Tab', foreground='red')
        self.master.protocol('WM_DELETE_WINDOW', self.exit)

        menubar = Menu(self.master)

        filemenu = Menu(menubar, tearoff=0, background="#2c2f33", foreground="light blue")
        new_file_menu = Menu(filemenu, tearoff=0, background="#2c2f33", foreground="light blue")
        new_file_menu.add_command(label="Python File            ", command=self.python_add); new_file_menu.add_command(label="C++ File", command=self.cpp_add); new_file_menu.add_command(label="Text File", command=self.txt_add)

        filemenu.add_cascade(label="New", menu=new_file_menu)
        filemenu.add_command(label="Open", command=self.open_file, accelerator="Ctrl + O")
        filemenu.add_command(label="Open from Directory", command=self.open_in_dir)
        filemenu.add_command(label="Save", command=self.save_file, accelerator="Ctrl + S"); filemenu.add_command(label="Save As...", command=self.save_as, accelerator="Ctrl + S")
        filemenu.add_command(label="Close Tab", command=self.close_tab, accelerator="Ctrl + W"); filemenu.add_command(label="Summary", command=self.summary)
        filemenu.add_command(label="Exit", command=self.exit, accelerator="Alt + F4")

        toolsmenu = Menu(menubar, tearoff=0, background="#2c2f33", foreground="light blue")
        toolsmenu_txt = Menu(toolsmenu, tearoff=0, background="#2c2f33", foreground="light blue")
        toolsmenu.add_cascade(label="Text Editing", menu=toolsmenu_txt)

        editmenu = Menu(menubar, tearoff=0, background="#2c2f33", foreground="light blue")
        editmenu.add_command(label="Undo", command=self.undo)
        editmenu.add_command(label="Redo", command=self.cmd_redo)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command=self.cut, accelerator="Ctrl + X"); editmenu.add_command(label="Copy", command=self.copy, accelerator="Ctrl + C"); editmenu.add_command(label="Paste", command=self.paste, accelerator="Ctrl + V"); editmenu.add_command(label="Delete", command=self.delete, accelerator="Del"); editmenu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl + A")
        editmenu.add_separator()
        editmenu.add_command(label="Convert Selection to UPPERCASE", command=self.to_Upper); editmenu.add_command(label="Convert Selection to lowercase", command=self.to_Lower)
        editmenu.add_separator()
        editmenu.add_command(label="Date & Time", accelerator="F5", command=self.time); editmenu.add_command(label="Duplicate Line", command=self.duplicate_line); editmenu.add_command(label="Goto Line", command=self.goto)
        editmenu.add_separator()
        editmenu.add_command(label="Find & Replace", command=self.find_replace)
        editmenu.add_separator()

        windowmenu = Menu(menubar, tearoff=0, background="#2c2f33", foreground="light blue")
        transparency = Menu(windowmenu, tearoff=False, background="#2c2f33", foreground="light blue")
        windowmenu.add_command(label="Always On Top", command=self.alwaysontop)

        transparency.add_command(label="5%", command=self.Transparent5); transparency.add_command(label="10%", command=self.Transparent10); transparency.add_command(label="20%", command=self.Transparent20); transparency.add_command(label="25%", command=self.Transparent25); transparency.add_command(label="30%", command=self.Transparent30); transparency.add_command(label="40%", command=self.Transparent40); transparency.add_command(label="50%", command=self.Transparent50); transparency.add_command(label="75%", command=self.Transparent75); transparency.add_command(label="Reset", command=self.resetTransparent)
        windowmenu.add_cascade(label="Transparency", menu=transparency)

        abb = Menu(menubar, tearoff=False, background="#2c2f33", foreground="light blue")
        abb.add_command(label="Learn IDE Features", command=self.learn_features); abb.add_command(label="Submit a Bug Report", command=self.bug_report); abb.add_separator(); abb.add_command(label="Current Version", command=self.version); abb.add_command(label="GitHub", command=self.about_github)

        self.word_wrap = BooleanVar()
        editmenu.add_checkbutton(label="Word Wrap", onvalue=True, offvalue=False, variable=self.word_wrap,
                                   command=self.wrap)

        menubar.add_cascade(label="File", menu=filemenu) ;menubar.add_cascade(label="Edit", menu=editmenu);
        menubar.add_cascade(label="Tools", menu=toolsmenu); menubar.add_cascade(label="Window", menu=windowmenu);
        menubar.add_cascade(label="Help", menu=abb)
        self.master.config(menu=menubar)

        self.right_click_menu = Menu(self.master, tearoff=0, foreground="light blue", background="#2c2f33")
        self.searchmenu = Menu(self.right_click_menu, tearoff=0, foreground="light blue", background="#2c2f33")
        self.speakmenu = Menu(self.right_click_menu, tearoff=0, foreground="light blue", background="#2c2f33")
        self.encodemenu = Menu(self.right_click_menu, tearoff=0, foreground="light blue", background="#2c2f33")
        self.highlightmenu = Menu(self.right_click_menu, tearoff=0, foreground="light blue", background="#2c2f33")

        self.right_click_menu.add_command(label="Cut                                     ", command=self.cut, accelerator="Ctrl + X"); self.right_click_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl + C"); self.right_click_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl + V"); self.right_click_menu.add_command(label="Delete", command=self.delete, accelerator="Del"); self.right_click_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl + A"); self.right_click_menu.add_separator(); self.right_click_menu.add_command(label="Refractor", command=self.refractoring)
        self.right_click_menu.add_separator(); self.speakmenu.add_command(label="Speak", command=self.right_speak); self.searchmenu.add_command(label="Wikipedia", command=self.wiki); self.searchmenu.add_command(label="StackOverflow", command=self.search_stack); self.encodemenu.add_command(label="Encode", command=self.encypt); self.encodemenu.add_command(label="Decode", command=self.decode); self.highlightmenu.add_command(label="Highlight", command=self.highlight_note); self.highlightmenu.add_command(label="Remove Highlight", command=self.clear_highlight)

        self.right_click_menu.add_cascade(label="Highlighting", menu=self.highlightmenu); self.right_click_menu.add_cascade(label="Speak", menu=self.speakmenu); self.right_click_menu.add_cascade(label="Search In", menu=self.searchmenu); self.right_click_menu.add_cascade(label="Encryption", menu=self.encodemenu)

        self.tab_right_click_menu = Menu(self.master, tearoff=0)
        self.tab_right_click_menu.add_command(label="New Tab", command=self.new_file)
        self.nb.bind('<Button-3>', self.right_click_tab)

        first_tab = ttk.Frame(self.nb)
        self.tabs[first_tab] = Document(first_tab, self.create_text_widget(first_tab))
        self.nb.add(first_tab, text='Scratch')

    def get_matches(self, word):
        wordd = self.tabs[self.get_tab()].textbox.get("1.0", "end-1c").split()
        words = python_wd + list(wordd)
        matches = [x for x in words if x.startswith(word)]
        return matches

    def create_text_widget(self, frame):
        textbox = AuraTextWidget(frame, autocomplete=self.get_matches, relief='sunken', borderwidth=0, wrap='none', background=bg_get, foreground=fg_get
                                 , insertbackground=tc_get, font=(font, fontsize))
        yscrollbar = CTkScrollbar(frame, command=textbox.yview); yscrollbar.pack(side='right', fill='y')

        def auto_indent(event):
            text_ai = event.widget
            line = text_ai.get("insert linestart", "insert")
            match = re.match(r'^(\s+)', line)
            whitespace = match.group(0) if match else ""
            text_ai.insert("insert", f"\n{whitespace}")
            return "break"

        def tab_pressed(event: Event) -> str:
            self.tabs[self.get_tab()].textbox.insert("insert", " " * 4)
            return "break"

        textbox.bind("<Return>", auto_indent)
        textbox.bind("<Tab>", tab_pressed)

        xscrollbar = CTkScrollbar(frame, command=textbox.xview,orientation='horizontal'); xscrollbar.pack(side='bottom', fill='x'); textbox.config(yscrollcommand=yscrollbar.set, undo=True, autoseparators=True)
        textbox.config(xscrollcommand=xscrollbar.set)

        textbox.bind('<Control-s>', self.save_file); textbox.bind('<Control-s>', self.save_file); textbox.bind('<Control-o>', self.open_file); textbox.bind('<Control-O>', self.open_file); textbox.bind('<Control-n>', self.new_file); textbox.bind('<Control-N>', self.new_file); textbox.bind('<Control-w>', self.close_tab); textbox.bind('<Control-W>', self.close_tab); textbox.bind('<Button-3>', self.right_click); textbox.bind('<Control-F>', self.finder); textbox.bind_all('<Return>', self.redraw); textbox.bind_all('<BackSpace>', self.redraw); textbox.bind_all('<KeyPress>', self.redraw); textbox.bind_all('<KeyRelease>', self.redraw); textbox.bind_all('<Key>', self.redraw); textbox.bind_all('<Button-4>', self.redraw)
        textbox.bind_all('<Button-5>', self.redraw); textbox.bind_all('<Configure>', self.redraw); textbox.bind_all('<Motion>', self.redraw); textbox.bind('<Control-f>', self.finder)

        cdg = ColorDelegator()
        cdg.tagdefs['COMMENT'] = {'foreground': 'grey', 'background': '#1d1d1d'}; cdg.tagdefs['KEYWORD'] = {'foreground': 'orange', 'background': '#1d1d1d'}; cdg.tagdefs['BUILTIN'] = {'foreground': 'gold', 'background': '#1d1d1d'}; cdg.tagdefs['STRING'] = {'foreground': '#95e7ad', 'background': '#1d1d1d'}; cdg.tagdefs['DEFINITION'] = {'foreground': '#bb6733', 'background': '#1d1d1d'}; cdg.tagdefs['BRACKETS'] = {'foreground': '#007F7F', 'background': '#1d1d1d'}
        Percolator(textbox).insertfilter(cdg)

        textbox.pack(fill='both', expand=True)
        return textbox

    def open_file(self, *args):
        ModuleFile.open_file(self, self, Document=Document)
    def save_as(self):
        ModuleFile.save_as(self)
    def goto(self):
        ModuleFile.goto(self)
    def save_file(self, *args):
        ModuleFile.save_file(self, self)
    def open_in_dir(self):
        ModuleFile.open_in_dir(self)
    def new_file(self, *args):
        new_tab = ttk.Frame(self.nb); self.tabs[new_tab] = Document(new_tab, self.create_text_widget(new_tab)); self.tabs[new_tab].textbox.config(wrap='word' if self.word_wrap.get() else 'none'); self.nb.add(new_tab, text='Scratch'); self.nb.select(new_tab)
    def copy(self):
        try:
            sel = self.tabs[self.get_tab()].textbox.get(SEL_FIRST, SEL_LAST); self.master.clipboard_clear(); self.master.clipboard_append(sel)
        except TclError:
            pass
    def delete(self):
        try:
            self.tabs[self.get_tab()].textbox.delete(SEL_FIRST, SEL_LAST)
        except TclError:
            pass
    def cut(self):
        try:
            sel = self.tabs[self.get_tab()].textbox.get(SEL_FIRST, SEL_LAST); self.master.clipboard_clear(); self.master.clipboard_append(sel); self.tabs[self.get_tab()].textbox.delete(SEL_FIRST, SEL_LAST)
        except TclError:
            pass

    def finder(self, e):
        finde = CTkToplevel()
        finde.title("Find")
        textfindedd = CTkEntry(finde, width=200, text_color="light blue", text_font=("Arial", 12), height=32)
        textfindedd.pack()
        textfindedd.focus_set()
        finde.attributes('-topmost', 1)

        def finded(v):
            ModuleFile.find(self.tabs[self.get_tab()].textbox, textfindedd)

        textfindedd.bind('<KeyPress>', finded)
        textfindedd.bind('KeyRelease', finded)
        textfindedd.bind('<FocusIn>', finded)
        textfindedd.bind('<MouseWheel>', finded)

    def encypt(self):
        ModuleFile.encypt(self.tabs[self.get_tab()].textbox)
    def clear_highlight(self):
        st_ind = self.tabs[self.get_tab()].textbox.index("sel.first"); end_ind = self.tabs[self.get_tab()].textbox.index("sel.last"); self.tabs[self.get_tab()].textbox.tag_remove("start", st_ind, end_ind)
    def decode(self):
        ModuleFile.decode(self.tabs[self.get_tab()].textbox)
    def redraw(self, event=NONE):
        self.update_count(event); self.lineNumber.delete("all"); self.objectIds = []
        si = self.tabs[self.get_tab()].textbox.index("@0,0")
        while True:
            dline = self.tabs[self.get_tab()].textbox.dlineinfo(si)
            if dline is None:
                break
            y = dline[1]
            liNum = str(si).split(".")[0]
            self.lineNumber.create_text(
                2, y, anchor="nw", text=liNum, fill="#d3d3d3", font=("Consolas", 12))
            si = self.tabs[self.get_tab()].textbox.index(f"{si}+1line")

    def update_count(self, event):
        count = self.tabs[self.get_tab()].textbox.get('1.0', END)
        self.wordCount.set(f"Word Count -> {len(count) - 1}")
    def python_add(self):
        self.new_file()
        ModuleFile.python_temp(self.tabs[self.get_tab()].textbox)
    def cpp_add(self):
        self.new_file()
        ModuleFile.cpp_temp(self.tabs[self.get_tab()].textbox)
    def txt_add(self):
        self.new_file()
    def wrap(self):
        if self.word_wrap.get():
            for index in self.tabs:
                self.tabs[index].textbox.config(wrap="word")
        else:
            for index in self.tabs:
                self.tabs[index].textbox.config(wrap="none")
    def find_replace(self):
        ModuleFile.find_replace(self)
    def to_Upper(self):
        ModuleFile.to_Upper(self)
    def to_Lower(self):
        ModuleFile.to_Lower(self)
    def refractoring(self):
        ModuleFile.refractor(self.tabs[self.get_tab()].textbox)
    def highlight_note(self):
        ModuleFile.highlightText(self.tabs[self.get_tab()].textbox)
    def summary(self):
        ModuleFile.Summary(self.tabs[self.get_tab()].textbox)
    def paste(self):
        try:
            self.tabs[self.get_tab()].textbox.insert(INSERT, self.master.clipboard_get())
        except TclError:
            pass

    def duplicate_line(self):
        line = (self.tabs[self.get_tab()].textbox.index("insert")); line_start = line + " linestart"; line_end = line + " lineend"; line_contents = self.tabs[self.get_tab()].textbox.get(line_start, line_end); line_contents = "\n" + line_contents; self.tabs[self.get_tab()].textbox.insert(line, line_contents)
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
        self.tabs[curr_tab].textbox.tag_add(SEL, "1.0", END)
        self.tabs[curr_tab].textbox.mark_set(INSERT, END)
        self.tabs[curr_tab].textbox.see(INSERT)
    def time(self):
        d = datetime.now()
        self.tabs[self.get_tab()].textbox.insert('end', d)
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
    def bug_report(self):
        webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Text/issues/new/choose")
    def version(self):
        text_ver = "Current Version: " + "1.2" + "\n" + "Codename: " + "Hi Speed!"
        messagebox.showinfo("Version Info", text_ver)
    def about_github(self):
        webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Notes")
    def close_tab(self, event=None):
        if event is None or event.type == str(2):
            selected_tab = self.get_tab()
        else:
            try:
                index = event.widget.index('@%d,%d' % (event.x, event.y))
                selected_tab = self.nb._nametowidget(self.nb.tabs()[index])
            except TclError:
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
            m = messagebox.askyesnocancel('Aura Notes', "Hold up, cowboy! Do uou want to save your masterpiece " +
                                           ('Scratch' if not file_dir else file_dir) + ' before riding off into the sunset?')
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
            except TclError:
                return
 
def main():
    root = CTk()
    app = Editor(root)
    root.mainloop()
if __name__ == '__main__':
    main()
