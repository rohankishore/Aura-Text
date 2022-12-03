"""
ModuleFile

This file contains all the functions for the features of Aura Notes. This makes the code better accessible and easy to contribute
for the devs

Translate feature isnt included in this file as the number of lines increases dramatically. That's in an different .py file.
"""
import os
import tkinter
import webbrowser
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilename
import pyttsx3
import wikipedia
import pyperclip


def resize(root):
    root.geometry("500x500")
    root.state('normal')
    root.attributes('-topmost', 1)

def rightSpeak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def fullSpeak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def checkPrime(num):
    if num > 1:
        # check for factors
        for i in range(2, num):
            if (num % i) == 0:
                messagebox.showinfo("Not Prime!", "NOT A PRIME NUMBER")
                break
        else:
            messagebox.showinfo("Prime!", "PRIME NUMBER FOUND")

    else:
        messagebox.showinfo("Not Prime!", "NOT A PRIME NUMBER")

def Googlesearch(query_google):
    link = str(
        "https://www.google.com/search?q=" + query_google + "&oq=hi&aqs=chrome..69i57j69i59j0i67l2j46i67j69i60j69i61l2.422j0j4&sourceid=chrome&ie=UTF-8")
    webbrowser.open_new_tab(link)

def calendar():
    import calendar

    def showCalender():
        global gui
        gui = Tk()
        gui.config(background='#303030')
        gui.title("Calender for the year")
        yearr = int(year_field.get())
        gui_content = calendar.calendar(yearr)
        calYear = Label(gui, text=gui_content, font="Consolas 10 bold")
        calYear.pack(fill=BOTH)
        gui.mainloop()

    def run():
        global year_field
        new = Tk()
        new.title("Calender"), new.geometry("300x200")
        new.config(background="#1b1b1b")
        cal = ttk.Label(new, text="Calender", font=("times", 28, "bold"), background="#1b1b1b", foreground="white")
        year = ttk.Label(new, text="Enter year", background="#1b1b1b", foreground="white")
        year_field = ttk.Entry(new)
        button = ttk.Button(new, text='Show Calender', command=showCalender)

        def close():
            new.destroy()
            gui.destroy()

        Exit = ttk.Button(new, text='Exit', command=close)
        cal.pack()
        year.pack()
        year_field.pack(pady=5)
        button.pack(pady=5)
        Exit.pack(pady=10)

        new.mainloop()

    run()

def Summary(textwidget):
    note_lines = str(textwidget.index('end-1c').split('.')[0])
    note_char_count = str(len(textwidget.get("1.0", 'end-1c')))
    note_cindex = textwidget.index(INSERT)

    text = "Total Number of Lines: " + note_lines + "\n" + "Total Character Count: " + note_char_count + "\n" + "Current Index: " + note_cindex

    tk = Toplevel()
    tk.overrideredirect(True)

    tk.config(background="black")

    w = 300  # width for the Tk root
    h = 100  # height for the Tk root

    # get screen width and height
    ws = tk.winfo_screenwidth()  # width of the screen
    hs = tk.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # set the dimensions of the screen
    # and where it is placed
    tk.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def close():
        tk.destroy()

    Label(tk, text=text, background="black", foreground="orange").pack()

    ttk.Button(tk, text="OK", command=close).pack(side=BOTTOM)

def highContrastMode(notepad, topFrame, cmd_line):
    notepad.config(background="black", foreground="#44ad88")
    cmd_line.config(background="grey")
    topFrame.config(background="black")

def darkmode(notepad, topFrame, cmd_line):
    notepad.config(background="#1d1d1d", foreground="white")
    topFrame.config(background="#1d1d1d")
    cmd_line.config(background="#313335")

def lightmode(notepad, topFrame, cmd_line):
    notepad.config(background="#d3d3d3", foreground="black")
    topFrame.config(background="white")
    cmd_line.config(background="white")

def add_full_format(textwidget):
    from datetime import date

    cind = textwidget.index(INSERT)

    dt = str(date.today())

    yn = "Sender's Name: " + "\n" + "\n"
    ya = "Sender's Address: " + "\n" + "\n" + "\n"
    d = "Date: " + dt + "\n" + "\n" + "\n"

    sn = "Recipient's Name: " + "\n" + "\n"
    sa = "Recipient's Address: " + "\n" + "\n" + "\n"

    salutation = "Dear Sir/Madam" + "\n" + "\n"
    subject = "Subject: " + "\n" + "\n"

    mail_body = "<Mail Body>" + "\n" + "\n" + "\n" + "\n"

    footer = "Your Sincerely," + "\n" + "<Your Name>"

    text = yn + ya + d + sn + sa + salutation + subject + mail_body + footer

    textwidget.insert(cind, text)

def to_and_from(notepad):
    global a
    a = notepad.index(tkinter.INSERT)

    text = "To: " + "\n" + "\n" + "\n" + "From: "

    notepad.insert(a, text)

def add_footer(notepad):
    cindex = notepad.index(tkinter.INSERT)

    text = "Your Sincerely," + "\n" + "<Your Name>"

    notepad.insert(cindex, text)

def highlightText(notepad):
    st_ind = notepad.index("sel.first")
    end_ind = notepad.index("sel.last")

    notepad.tag_add("start", st_ind, end_ind)
    notepad.tag_config("start", background="gold", foreground="black")

def mathExpUp(notepad):
    global res_txt
    exp = notepad.selection_get()
    res = str(eval(exp))
    res_txt = str("Expression Result: " + res)
    messagebox.showinfo("Result", res_txt)

def find(e, notepad, textfinded):
    # remove tag 'found' from index 1 to END
    notepad.tag_remove('found', '1.0', END)

    # returns to widget currently in focus
    s = textfinded.get()
    if s:
        idx = '1.0'
        while 1:
            # searches for desired string from index 1
            idx = notepad.search(s, idx, nocase=1,
                                        stopindex=END)
            if not idx:
                break

            # last index sum of current index and
            # length of text
            lastidx = '%s+%dc' % (idx, len(s))

            # overwrite 'Found' at idx
            notepad.tag_add('found', idx, lastidx)
            idx = lastidx

        # mark located string as red
        notepad.tag_config('found', foreground='red')

# func for syntax highlighting
def syntaxHighlighting(notepad):
    cdg = ColorDelegator()
    cdg.tagdefs['COMMENT'] = {'foreground': 'grey', 'background': '#1d1d1d'}
    cdg.tagdefs['KEYWORD'] = {'foreground': 'orange', 'background': '#1d1d1d'}
    cdg.tagdefs['BUILTIN'] = {'foreground': 'gold', 'background': '#1d1d1d'}
    cdg.tagdefs['STRING'] = {'foreground': '#95e7ad', 'background': '#1d1d1d'}
    cdg.tagdefs['DEFINITION'] = {'foreground': 'gold', 'background': '#1d1d1d'}
    cdg.tagdefs['BRACKETS'] = {'foreground': '#007F7F', 'background': '#1d1d1d'}
    Percolator(notepad).insertfilter(cdg)

# essential files for settings page
with open("synhig.txt", 'r+') as syn:
    synhigh = syn.readline()

with open("theme.txt", 'r+') as thm:
    themeget = thm.readline()

with open("auto_intend.txt", 'r+') as ain:
    autointendget = ain.readline()

with open("tabnumber.txt", 'r+') as tbn:
    tabnumberget = tbn.readline()

# settings page
def settings():
    f = open("synhig.txt", 'r+')
    t = open("theme.txt", 'r+')
    auto = open("auto_intend.txt", 'r+')
    tab = open("tabnumber.txt", 'r+')

    # main gui window for editor
    settings_page = Tk()
    settings_page.title("Settings")
    settings_page.geometry("350x400")
    settings_page.resizable(True, True)
    settings_page.state('zoomed')
    settings_page.config(background="black")

    syvar = StringVar()
    themevar = StringVar()
    autoindvar = StringVar()
    tabnovar = StringVar()
    synval = ["On", "Off"]
    aival = ["On", "Off"]
    themeval = ["Dark", "Light", "High Contrast"]
    synt = OptionMenu(settings_page, syvar, *synval)
    theme = OptionMenu(settings_page, themevar, *themeval)
    tabnumber = ttk.Entry(settings_page, width=18, textvariable=tabnovar)
    ait = OptionMenu(settings_page, autoindvar, *aival)
    synt.config(width=15, borderwidth=0, activebackground="#1b1b1b")
    theme.config(width=15, borderwidth=0, activebackground="#1b1b1b")
    ait.config(width=15, borderwidth=0, activebackground="#1b1b1b")
    ttk.Label(settings_page, text="Syntax Highlighting", background="#121212", foreground="white").place(x=10, y=50)
    ttk.Label(settings_page, text="Theme", background="#121212", foreground="white").place(x=10, y=120)
    ttk.Label(settings_page, text="Auto Intend", background="#121212", foreground="white").place(x=10, y=190)
    ttk.Label(settings_page, text="Tab Length", background="#121212", foreground="white").place(x=10, y=260)
    synt.place(x=160, y=47)
    theme.place(x=160, y=120)
    ait.place(x=160, y=183)
    tabnumber.place(x=160, y=243)

    def apply():
        syntax_value = syvar.get()
        theme_value = themevar.get()
        autointend_value = autoindvar.get()
        tabnumber_value = tabnovar.get()

        if syntax_value != "":
            f.truncate(0)

            if syntax_value == "On":
                f.write("stx")
            else:
                f.write("")

        if syntax_value == "":
            f.write(synhigh)

        if theme_value != "":
            t.truncate(0)

            if theme_value == "Dark":
                t.write("dark")
            elif theme_value == "Light":
                t.write("light")
            elif theme_value == "High Contrast":
                t.write("hct")

        if theme_value == "":
            t.write(themeget)

        if tabnumber_value != "":
            tab.truncate(0)
            tab.write(tabnumber_value)

        if autointend_value is not None:
            auto.truncate(0)

            if autointend_value == "On":
                auto.write("on")
            else:
                auto.write("off")

        if autointend_value == "":
            auto.write(autointendget)

        messagebox.showinfo("RESTART", "RESTART the app to enable the changes made")

        settings_page.destroy()

    ttk.Button(settings_page, text="Apply", command=apply).pack(side=BOTTOM, pady=20, padx=10)

    settings_page.mainloop()

# wikipedia
def wiki(notepad):
    global query
    w = Tk()

    try:
        query = notepad.selection_get()
    except ValueError:
        messagebox.showerror("Error!", "Select any text or word to continue")
        w.destroy()

    w.configure(background="#1b1b1b"), w.title("Wikipedia"), w.resizable(False, False)

    text_w = Text(w, background="#1b1b1b", foreground="white", font=("Helvetica", 12))
    text_w.pack(pady=10)

    def copy():
        aa = text_w.get(1.0, END)
        pyperclip.copy(aa)

    ttk.Button(w, text="Copy Article", command=copy).place(x=295, y=460)

    result = wikipedia.page(query).content

    text_w.insert(1.0, result)
    text_w.config(state=DISABLED)

def txt_analyze():
    filepath = str(askopenfilename(filetypes=[("Text files", "*.txt")]))

    with open(filepath, 'r+') as f:
        lines = str(len(f.readlines()))
        chars = str(len(f.read()))

    text = "Total Number of Lines: " + lines + "\n" + "Total Character Count: " + chars + "\n"

    tk = Toplevel()
    tk.overrideredirect(True)

    tk.config(background="black")

    w = 300  # width for the Tk root
    h = 100  # height for the Tk root

    # get screen width and height
    ws = tk.winfo_screenwidth()  # width of the screen
    hs = tk.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # set the dimensions of the screen
    # and where it is placed
    tk.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def close():
        tk.destroy()

    Label(tk, text=text, background="black", foreground="orange").pack()

    ttk.Button(tk, text="OK", command=close).pack(side=BOTTOM)