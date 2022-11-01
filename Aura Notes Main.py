# system libs
import os
import random
import tkinter
import webbrowser
from datetime import date

# Syntax Highlighting
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator

# Tkinter
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox

# Extras
import pyperclip
import pyttsx3
import sv_ttk
import wikipedia
from PIL import ImageTk
from googletrans import Translator

# files
from Quotes import quotes

# Eline break
splash_screen = Tk()
ws = splash_screen.winfo_screenwidth()  # width of the screen
hs = splash_screen.winfo_screenheight()  # height of the screen

w = 700
h = 394

# calculate x and y coordinates for the Tk root window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

# set the dimensions of the screen
# and where it is placed
splash_screen.geometry('%dx%d+%d+%d' % (w, h, x, y))

splash_icon = tkinter.PhotoImage(file="Aura Notes.png")

splash_screen.overrideredirect(True)
splash_label = Label(splash_screen, image=splash_icon)

quote = str(random.choice(quotes))

ttk.Label(splash_screen, text=quote).pack(side=BOTTOM)
splash_label.pack()


def main():
    splash_screen.destroy()

    # main gui window for editor
    root = Tk()
    root.title("Aura Notes")

    # deciding which theme to use
    sv_ttk.set_theme("dark")

    # making the window resizable and adjusting its size
    root.resizable(True, True)

    # Set a minsize for the window, and place it in the middle
    root.state('zoomed')
    root.iconbitmap("notepad.ico")

    # top frame to accompany menu bar and stuff
    topFrame = tkinter.Frame(root, background="#1b1b1b", width=1550, height=45)
    topFrame.place(x=2, y=8)

    def rightSpeak():
        v = notepad.selection_get()
        engine = pyttsx3.init()
        engine.say(v)
        engine.runAndWait()

    tabController = ttk.Notebook(root)
    tabController.pack(expand=True, fill=BOTH)

    editor = ttk.Frame(tabController)
    coding = ttk.Frame(tabController)
    paint = ttk.Frame(tabController)

    tabController.add(editor, text="Notepad ✎")
    tabController.add(coding, text="Coding </>")

    menu_number = ""

    def ytSearch(e):
        queryyt = notepad.selection_get()

        link = "https://www.youtube.com/results?search_query=" + queryyt
        webbrowser.open_new_tab(link)

    # useful datas
    af = os.listdir(r'C:\Windows\fonts')
    availFonts = list(af)
    fontSizes = list(range(1, 31))

    def cmdNew():  # file menu New option
        global fileName
        if len(notepad.get('1.0', END + '-1c')) > 0:
            if messagebox.askyesno("Notepad", "Do you want to save changes?"):
                cmdSaveAs()
            else:
                notepad.delete(0.0, END)

    def cmdOpen():  # file menu Open option
        fd = filedialog.askopenfile(parent=editor, mode='r')
        t = fd.read()  # t is the text read through filedialog
        notepad.delete(0.0, END)
        notepad.insert(0.0, t)

    def cmdOpenUp(e):  # file menu Open option
        fd = filedialog.askopenfile(parent=editor, mode='r')
        t = fd.read()  # t is the text read through filedialog
        notepad.delete(0.0, END)
        notepad.insert(0.0, t)

    def insertDate():
        cdate = str(date.today())
        notepad.insert(0.0, cdate)

    def insertDateUp(e):
        cdate = str(date.today())
        notepad.insert(1.0, cdate)

    def cmdSaveAs():  # file menu Save As option
        fd = filedialog.asksaveasfile(mode='w', defaultextension='.txt', initialfile="textfile")
        t = notepad.get(0.0, END)  # t stands for the text gotten from notepad
        try:
            fd.write(t.rstrip())
        except:
            messagebox.showinfo(title="Error", message="Not able to save file!")

    def cmdExit():  # file menu Exit option
        if messagebox.askyesno("Notepad", "Are you sure you want to exit?"):
            root.destroy()

    def cmdExitUp(e):  # file menu Exit option
        if messagebox.askyesno("Notepad", "Are you sure you want to exit?"):
            root.destroy()

    def minimize():
        root.iconify()

    def maximize():
        root.state('zoomed')

    def cmdCut():  # edit menu Cut option
        notepad.event_generate("<<Cut>>")

    def cmdCopy():  # edit menu Copy option
        notepad.event_generate("<<Copy>>")

    def cmdCopyUp(e):  # edit menu Copy option

        notepad.event_generate("<<Copy>>")

    def search():
        querysearch = notepad.selection_get()
        link = str(
            "https://www.google.com/search?q=" + querysearch + "&oq=hi&aqs=chrome..69i57j69i59j0i67l2j46i67j69i60j69i61l2.422j0j4&sourceid=chrome&ie=UTF-8")
        webbrowser.open_new_tab(link)

    def rightTranslate():
        v = notepad.selection_get()
        tpage = Tk()
        tpage.title('Translator - Aura Notes')
        tpage.geometry('530x330')
        tpage.config(background="#212121")
        tpage.maxsize(530, 330)
        tpage.minsize(530, 330)

        def translate():
            language_1 = v
            cl = choose_langauge.get()

            if language_1 == '':
                messagebox.showerror('Translator', 'please fill the box')
            else:
                t2.delete(1.0, 'end')
                translator = Translator()
                output = translator.translate(language_1, dest=cl)
                t2.insert('end', output.text)

        def clear():
            t1.delete(1.0, 'end')
            t2.delete(1.0, 'end')

        a = StringVar()
        auto_detect = Combobox(tpage, width=20, textvariable=a, state='readonly', font=('verdana', 10, 'bold'),
                               background="#1b1b1b")

        auto_detect['values'] = (
            'Auto Detect',
        )

        auto_detect.place(x=30, y=70)
        auto_detect.current(0)

        l = StringVar()
        choose_langauge = Combobox(tpage, width=20, textvariable=l, state='readonly', font=('verdana', 10, 'bold'),
                                   background="#1b1b1b")

        choose_langauge['values'] = (
            'Afrikaans',
            'Albanian',
            'Arabic',
            'Armenian',
            ' Azerbaijani',
            'Basque',
            'Belarusian',
            'Bengali',
            'Bosnian',
            'Bulgarian',
            ' Catalan',
            'Cebuano',
            'Chichewa',
            'Chinese',
            'Corsican',
            'Croatian',
            ' Czech',
            'Danish',
            'Dutch',
            'English',
            'Esperanto',
            'Estonian',
            'Filipino',
            'Finnish',
            'French',
            'Frisian',
            'Galician',
            'Georgian',
            'German',
            'Greek',
            'Gujarati',
            'Haitian Creole',
            'Hausa',
            'Hawaiian',
            'Hebrew',
            'Hindi',
            'Hmong',
            'Hungarian',
            'Icelandic',
            'Igbo',
            'Indonesian',
            'Irish',
            'Italian',
            'Japanese',
            'Javanese',
            'Kannada',
            'Kazakh',
            'Khmer',
            'Kinyarwanda',
            'Korean',
            'Kurdish',
            'Kyrgyz',
            'Lao',
            'Latin',
            'Latvian',
            'Lithuanian',
            'Luxembourgish',
            'Macedonian',
            'Malagasy',
            'Malay',
            'Malayalam',
            'Maltese',
            'Maori',
            'Marathi',
            'Mongolian',
            'Myanmar',
            'Nepali',
            'Norwegian'
            'Odia',
            'Pashto',
            'Persian',
            'Polish',
            'Portuguese',
            'Punjabi',
            'Romanian',
            'Russian',
            'Samoan',
            'Scots Gaelic',
            'Serbian',
            'Sesotho',
            'Shona',
            'Sindhi',
            'Sinhala',
            'Slovak',
            'Slovenian',
            'Somali',
            'Spanish',
            'Sundanese',
            'Swahili',
            'Swedish',
            'Tajik',
            'Tamil',
            'Tatar',
            'Telugu',
            'Thai',
            'Turkish',
            'Turkmen',
            'Ukrainian',
            'Urdu',
            'Uyghur',
            'Uzbek',
            'Vietnamese',
            'Welsh',
            'Xhosa'
            'Yiddish',
            'Yoruba',
            'Zulu',
        )

        choose_langauge.place(x=290, y=70)
        choose_langauge.current(0)

        t1 = Text(tpage, width=30, height=10, borderwidth=2, relief=RIDGE, background="#1b1b1b",
                  insertbackground="white",
                  foreground="white")
        t1.focus_set()
        t1.place(x=10, y=100)
        t1.insert(1.0, v)

        t2 = Text(tpage, width=30, height=10, borderwidth=2, relief=RIDGE, background="#1b1b1b",
                  insertbackground="white",
                  foreground="white")
        t2.place(x=260, y=100)

        button = tkinter.Button(tpage, text="Translate", relief=RIDGE, borderwidth=0, font=('verdana', 10, 'bold'),
                                cursor="hand2",
                                command=translate, background="#1b1b1b", foreground="white", activebackground="#1b1b1b",
                                activeforeground="white")
        button.place(x=150, y=280)

        clear = Button(tpage, text="Clear", relief=RIDGE, borderwidth=0, font=('verdana', 10, 'bold',), cursor="hand2",
                       command=clear, background="#1b1b1b", foreground="white", activebackground="#1b1b1b",
                       activeforeground="white")
        clear.place(x=280, y=280)

        rightclickevent = Menu(t1, tearoff=0)
        rightclickevent.add_command(label="Copy", command=cmdCopy)
        rightclickevent.add_command(label="Paste", command=cmdPaste)
        rightclickevent.add_command(label="Select All", command=cmdSelectAll)

        def popup_tk(event):
            try:
                rightclickevent.tk_popup(event.x_root, event.y_root)

            finally:
                rightclickevent.grab_release()

        t1.bind("<Button-3>", popup_tk)

        tpage.mainloop()

    def aboutPage():
        aboutWin = Tk()
        aboutWin.geometry("900x700")

        aboutWin.config(background="#1b1b1b")

        Label(aboutWin, text="ABOUT", font=("Didot", 13, "bold"), background="#1b1b1b", foreground="white").pack(pady=7)
        Label(aboutWin,
              text="Aura Notes is a notepad app for Windows, completely made with Tkinter. It is completely free with no ads or in-app purchases",
              font=("Didot", 12, "italic"),
              background="#1b1b1b", foreground="white").pack(pady=10)

        ttk.Label(aboutWin, text="Version:", font=("Didot", 12, "bold"),
                  background="#1b1b1b", foreground="white").pack(pady=10)

        ttk.Label(aboutWin, text="1.0.5 (Orchid Build)", font=("Didot", 12, "italic"),
                  background="#1b1b1b", foreground="white").pack()

        ttk.Label(aboutWin, text="What's new in this version:\n", font=("Didot", 12, "bold"),
                  background="#1b1b1b", foreground="white").pack()

        ttk.Label(aboutWin, text="* Full redesign of the entire app", font=("Didot", 11, "italic"),
                  background="#1b1b1b", foreground="white").pack()

        Label(aboutWin, text="* New Coding mode with Syntax Highlighting",
              font=("Didot", 11, "italic"),
              background="#1b1b1b", foreground="white").pack()

        Label(aboutWin, text="* New shortcut (Ctrl + Y) to quickly search a word in YouTube",
              font=("Didot", 11, "italic"),
              background="#1b1b1b", foreground="white").pack()

        Label(aboutWin, text="* Overall Stability Improvements", font=("Didot", 11, "italic"),
              background="#1b1b1b", foreground="white").pack()

        def childHelp():
            webbrowser.open_new_tab("https://www.unicef.org/india/take-action/donate-to-unicef")

        def insta():
            webbrowser.open_new_tab("www.instagram.com/jops.breh/")

        def gitSource():
            webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Notes")

        insta = ttk.Button(aboutWin, text="Follow Developer on Instagram", command=insta, cursor="hand2")

        ch = ttk.Button(aboutWin, text="Help a child by donating to UNICEF", command=childHelp, cursor="hand2")

        sr = ttk.Button(aboutWin, text="Get Source Code", command=gitSource, cursor="hand2")

        insta.pack(pady=20)
        ch.pack(pady=20)
        sr.pack(pady=20)

    def cmdPaste():  # edit menu Paste option
        notepad.event_generate("<<Paste>>")

    def cmdSelectAllUp(e):  # edit menu Select All option
        notepad.event_generate("<<SelectAll>>")

    def cmdSelectAll():  # edit menu Select All option
        notepad.event_generate("<<SelectAll>>")

    def wiki():
        global query
        w = Tk()

        try:
            query = notepad.selection_get()
        except:
            messagebox.showerror("Error!", "Select any text or word to continue")
            w.destroy()

        w.geometry("700x500"), w.configure(background="#1b1b1b"), w.title("Wikipedia"), w.resizable(False, False)

        text = Text(w, background="#1b1b1b", foreground="white", font=("Helvetica", 12))
        text.pack(pady=10)

        def copy():
            a = text.get(1.0, END)
            pyperclip.copy(a)

        ttk.Button(w, text="Copy Article", command=copy).place(x=295, y=460)

        result = wikipedia.summary(query, auto_suggest=False, sentences=6)

        text.insert(1.0, result)
        text.config(state=DISABLED)

    # text box for entry
    notepad = Text(editor, font=("Segoe UI", 14,), height=100, foreground="white",
                   insertbackground="white", borderwidth=0, undo=True)

    scrollbar = ttk.Scrollbar(editor)
    scrollbar.pack(side=RIGHT, fill=Y)
    notepad.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=notepad.yview)

    notepad.pack(fill=X)
    notepad.focus_set()

    code_editor = Text(coding, font=("Arial", 13), height=100, background="#141414", foreground="white",
                       insertbackground="white", borderwidth=0, undo=True, wrap=WORD)

    codescrollbar = ttk.Scrollbar(coding)
    codescrollbar.pack(side=RIGHT, fill=Y)
    code_editor.config(yscrollcommand=codescrollbar.set)
    codescrollbar.config(command=code_editor.yview)

    def codeSaveAs(e):  # file menu Save As option
        fd = filedialog.asksaveasfile(mode='w', defaultextension='.py', initialfile="scratch")
        t = code_editor.get(0.0, END)  # t stands for the text gotten from notepad
        try:
            fd.write(t.rstrip())
        except:
            messagebox.showinfo(title="Oh No!", message="Not able to save file!")

    def mathSolver():
        math = Tk()
        math.title("Math Solver"), math.config(background="#1b1b1b")

        # making the window resizable and adjusting its size
        math.resizable(False, False)

        # Set a minsize for the window, and place it in the middle
        math.geometry("350x200")

        exp = ttk.Entry(math, width=50, background="#1b1b1b", foreground="black")
        exp.pack(pady=15)

        def Calc():
            ansSpace.delete(0.0, END)
            gfg = exp.get()
            r = eval(gfg)
            ansSpace.insert(0.0, r)

        ttk.Button(math, text="Calculate", command=Calc).pack()

        ansSpace = Text(math, width=40, height=5, borderwidth=0, foreground="black")
        ansSpace.pack(pady=17)

        math.mainloop()

    def alwaysOnTop():
        root.attributes('-topmost', 1)

    def codeOpen(e):  # file menu Open option
        path = askopenfilename(filetypes=[('Python Files', '*.py')])
        with open(path, 'r') as file_code:
            code = file_code.read()
            code_editor.delete('1.0', END)
            code_editor.insert('1.0', code)

    def lineNumbers():
        output = ""
        row, col = code_editor.index('end').split('.')

        for i in range(1, int(row)):
            output += str(i) + '\n'

        return output

    def updateLineNumbers(event=None):
        lineNumbers_bar = lineNumbers()
        lineNumber.config(state="normal")
        lineNumber.delete(1.0, END)
        lineNumber.insert(1.0, lineNumbers_bar)

    code_editor.focus_set()

    lineNumber = Text(
        coding,
        width=7,
        padx=0,
        state="disabled",
        takefocus=0,
        background="#313335",
        wrap="none", font=("Arial", 13)
    )

    def noteOpen():  # file menu Open option
        fd = filedialog.askopenfile(parent=editor, mode='r')
        t = fd.read()  # t is the text read through filedialog
        notepad.delete(0.0, END)
        notepad.insert(0.0, t)

    lineNumber.pack(side="left", fill=Y)

    code_editor.pack(fill=X)

    def lightTheme():
        sv_ttk.set_theme("light")

    def darkTheme():
        sv_ttk.set_theme("dark")

    def mathExpUp():
        global res_txt
        exp = notepad.selection_get()
        try:
            res = str(eval(exp))
            res_txt = str("Expression Result: " + res)
        except:
            messagebox.showerror("Error", "Given input isn't an math expression!")

        Label(editor, text=res_txt, font=("ds-digital", 11), background="#1b1b1b", foreground="cyan").place(x=15, y=800)

    gg = StringVar()

    right_click_event = Menu(notepad, tearoff=0)
    right_click_event.config(borderwidth=0)
    right_click_event.add_command(
        label="Copy                                                                      Ctrl + C",
        command=cmdCopy)
    right_click_event.add_command(
        label="Paste                                                                     Ctrl + V", command=cmdPaste)
    right_click_event.add_command(
        label="Select All                                                                Ctrl + A",
        command=cmdSelectAll)
    right_click_event.add_command(
        label="Cut                                                                        Ctrl + X", command=cmdCut)

    right_click_event.add_separator()

    right_click_event.add_command(label="Speak", command=rightSpeak)
    right_click_event.add_command(
        label="Translate                                                              Ctrl + T",
        command=rightTranslate)
    right_click_event.add_command(label="Calculate Math Expression                               Ctrl + M",
                                  command=mathExpUp)
    right_click_event.add_command(label="Get Wikipedia Article                                         Ctrl + W",
                                  command=wiki)
    right_click_event.add_command(label="Search in Google", command=search)

    def popup(event):
        try:
            right_click_event.tk_popup(event.x_root, event.y_root)

        finally:
            right_click_event.grab_release()

    notepad.bind("<Button-3>", popup)

    def ExitApplication():
        MsgBox = messagebox.askquestion('Close Document',
                                        'The app is about to close. Do you want to save this document?',
                                        icon='warning')
        if MsgBox == 'yes':
            cmdSaveAs()
        else:
            root.destroy()

    # keyboard shortcuts
    notepad.bind('<Control-o>', cmdOpenUp)
    notepad.bind('<Control-c>', cmdCopyUp)
    notepad.bind('<Control-s>', cmdSaveAs)
    notepad.bind('<Control-b>', rightSpeak)
    notepad.bind('<Control-m>', mathExpUp)
    notepad.bind('<Control-d>', insertDateUp)
    notepad.bind('<Control-y>', ytSearch)

    notepad.bind('<Control-O>', cmdOpenUp)
    notepad.bind('<Control-C>', cmdCopyUp)
    notepad.bind('<Control-S>', cmdSaveAs)
    notepad.bind('<Control-B>', rightSpeak)
    notepad.bind('<Control-M>', mathExpUp)
    notepad.bind('<Control-D>', insertDateUp)
    notepad.bind('<Control-Y>', ytSearch)

    def unitConv():
        import UnitConv
        UnitConv.run()

    code_editor.bind('<Any-KeyPress>', updateLineNumbers)
    code_editor.bind('<Control-S>', codeSaveAs)
    code_editor.bind('<Control-s>', codeSaveAs)
    code_editor.bind('<Control-O>', codeOpen)
    code_editor.bind('<Control-o>', codeOpen)

    root.protocol("WM_DELETE_WINDOW", ExitApplication)

    def Transparent25():
        root.attributes('-alpha', 0.75)

    def Transparent50():
        root.attributes('-alpha', 0.5)

    def Transparent75():
        root.attributes('-alpha', 0.25)

    def resetTransparent():
        root.attributes('-alpha', 1)

    def Summary():
        lines = str(notepad.index('end-1c').split('.')[0])
        char_count = str(len(notepad.get("1.0", 'end-1c')))

        text = "Total Number of Line(s): " + lines , "\n", "Total Character Count: " + char_count

        messagebox.showinfo("Summary", text)

    menubar = Menu(editor, background='blue', fg='white')

    # Declare file and edit for showing in menubar
    file = Menu(menubar, tearoff=False, background='#141414', foreground="white")
    window = Menu(menubar, tearoff=False, background='#141414', foreground="white")
    tools = Menu(menubar, tearoff=False, background="#141414", foreground="white")
    abb = Menu(menubar, tearoff=False, background="#141414", foreground="white")
    theme = Menu(menubar, tearoff=False, background="#141414", foreground="white")

    # Add commands in file menu
    file.add_command(label="New Document", command=cmdNew)
    file.add_command(label="Open Document", command=noteOpen)
    file.add_command(label="Exit", command=cmdExit)
    file.add_command(label="Save Document", command=cmdSaveAs)
    file.add_command(label="Summary", command=Summary)

    # Add commands in window menu
    window.add_command(label="Minimize", command=minimize)
    window.add_command(label="Maximize", command=maximize)
    window.add_command(label="Always on Top", command=alwaysOnTop)
    window.add_command(label="Make Window 25% Transparent", command=Transparent25)
    window.add_command(label="Make Window 50% Transparent", command=Transparent50)
    window.add_command(label="Make Window 75% Transparent", command=Transparent75)
    window.add_command(label="Reset Transparency", command=resetTransparent)

    # Add commands in tools menu
    tools.add_command(label="Math Solver", command=mathSolver)
    tools.add_command(label="Unit Convertor", command=unitConv)

    def whatsNew():
        webbrowser.open_new_tab("https://auranotes-whatsnew.nicepage.io/")

    # Add commands in about menu
    abb.add_command(label="About", command=aboutPage)
    abb.add_command(label="What's New", command=whatsNew)

    # Add commands in view menu
    theme.add_command(label="Dark Mode", command=darkTheme)
    theme.add_command(label="Light Mode", command=lightTheme)

    cdg = ColorDelegator()
    cdg.tagdefs['COMMENT'] = {'foreground': 'grey', 'background': '#141414'}
    cdg.tagdefs['KEYWORD'] = {'foreground': 'orange', 'background': '#141414'}
    cdg.tagdefs['BUILTIN'] = {'foreground': 'orange', 'background': '#141414'}
    cdg.tagdefs['STRING'] = {'foreground': 'light green', 'background': '#141414'}
    cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': '#141414'}
    cdg.tagdefs['BRACKETS'] = {'foreground': '#007F7F', 'background': '#141414'}
    Percolator(code_editor).insertfilter(cdg)

    # Display the file and edit declared in previous step
    menubar.add_cascade(label="File", menu=file)
    menubar.add_cascade(label="Window", menu=window)
    menubar.add_cascade(label="Tools", menu=tools)
    menubar.add_cascade(label="Themes", menu=theme)
    menubar.add_cascade(label="About", menu=abb)

    # Displaying of menubar in the app
    root.config(menu=menubar)

    notepad.focus_set()


splash_screen.after(1800, main)

# main loop
mainloop()
