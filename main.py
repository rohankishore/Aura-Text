# system libs
import base64
from random import choice
import re
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
from tkinter.ttk import Combobox
import PIL.Image

# Extras
import pyperclip
import pyttsx3
import sv_ttk
import wikipedia
from PIL import ImageTk
from googletrans import Translator

# main gui window for editor
root = tkinter.Tk()
root.tk_setPalette('SystemButtonFace')
root.title("Aura Notes")


def resize():
    root.geometry("500x500")
    root.state("normal")
    root.attributes('-topmost', 1)


resize_icon = ImageTk.PhotoImage(PIL.Image.open('resize.png').resize((13, 13)))
cmdlist_icon = ImageTk.PhotoImage(PIL.Image.open('cmdlist.png').resize((1170, 950)))

# deciding which theme to use
sv_ttk.set_theme("dark")

# making the window resizable and adjusting its size
root.resizable(True, True)

root.config(background="#121212")

# Set a minsize for the window, and place it in the middle
root.state('zoomed')
root.iconbitmap("notepad.ico")

# top frame to accompany menu bar and stuff
topFrame = tkinter.Frame(root, background="#1b1b1b", height=50)
bottomFrame = tkinter.Frame(root, background="#1b1b1b", height=20)
bottomFrame.pack(side=BOTTOM, fill=X)
topFrame.pack(side=TOP, fill=X)

resize = Button(topFrame, image=resize_icon, background="#1b1b1b", activebackground="#1b1b1b", borderwidth=0,
                command=resize)
resize.image = resize_icon
resize.pack(side=LEFT, padx=5)

textfinded = ttk.Entry(topFrame, width=25, foreground="light blue", font=("Arial", 13))

cmd_line = Entry(bottomFrame, width=30, foreground="dark orange", borderwidth=0, background="black")
cmd_line.pack(side=RIGHT)


def manual():
    f = open("Manual.txt", "r")
    c = f.readlines()

    cindex = notepad.index(INSERT)

    notepad.insert(cindex, c)


def cmdline(e):
    def ytcmd():
        s = str(cmdget.replace("yt", ""))
        link = "https://www.youtube.com/results?search_query=" + s
        webbrowser.open_new_tab(link)

    def coinFlip():
        choices = ["Heads", "Tails", "Heads", "Tails"]

        aa = choice(choices)

        if aa == "Heads":
            minibuffer.insert(0.0, "It's HEAD")
        else:
            minibuffer.insert(0.0, "It's TAIL")

    def diceRoll():
        choices = [1, 2, 3, 4, 5, 6]
        aa = choice(choices)
        aa = str(aa)
        minibuffer.insert(0.0, aa)

    def Stackcmd():
        s = str(cmdget.replace("stack", ""))
        l = "https://stackoverflow.com/search?q=" + s + "&s=ddab4d49-a574-4a62-8794-24ac8a478c20"
        webbrowser.open_new_tab(l)

    def Githubcmd():
        s = str(cmdget.replace("git", ""))
        link = "https://github.com/search?q=" + s
        webbrowser.open_new_tab(link)

    cmdget = cmd_line.get()

    if "save" in cmdget:
        cmdSaveAs()
    elif "open" in cmdget:
        noteOpen()
    elif "new" in cmdget:
        cmdNew()
    elif "dateinsert" in cmdget:
        insertDateUp()
    elif "exit" in cmdget:
        cmdExit()

    elif "ftrans" in cmdget:
        fullTranslate()

    elif "yt" in cmdget:
        ytcmd()

    elif "stack" in cmdget:
        Stackcmd()

    elif "git" in cmdget:
        Githubcmd()

    elif "cal" in cmdget:
        calendar()
        minibuffer.insert(0.0, "Calendar Opened")

    elif "aot" in cmdget:
        alwaysOnTop()
        minibuffer.insert(0.0, "Always On Top Enabled")

    elif "mailff" in cmdget:
        add_full_format()
        minibuffer.insert(0.0, "Added full mail format")

    elif "ain" in cmdget:
        auto_intend()
        minibuffer.insert(0.0, "Turned on Auto Intend")

    elif "mailfooter" in cmdget:
        add_footer()
        minibuffer.insert(0.0, "Added footer of the mail")

    elif "mailtf" in cmdget:
        to_and_from()
        minibuffer.insert(0.0, "Added to and from mail")

    elif "cflip" in cmdget:
        coinFlip()

    elif "droll" in cmdget:
        diceRoll()

    elif "ltk" in cmdget:
        lightmode()
        minibuffer.insert(0.0, "Light Mode")

    elif "dtk" in cmdget:
        darkmode()
        minibuffer.insert(0.0, "Dark Mode")

    elif "htk" in cmdget:
        highContrastMode()
        minibuffer.insert(0.0, "High Contrast")

    elif "cdm" in cmdget:
        syntaxHighlighting()
        minibuffer.insert(0.0, "Coding Mode Turned ON")

    elif "min" in cmdget:
        minimize()

    elif "max" in cmdget:
        maximize()
        minibuffer.insert(0.0, "Window Maximized")

    else:
        messagebox.showerror("Error!", "Command Error!")


cmd_line.bind('<Return>', cmdline)


def rightSpeak():
    v = notepad.selection_get()
    engine = pyttsx3.init()
    engine.say(v)
    engine.runAndWait()


def fullSpeak():
    v = notepad.get(0.0, END)
    engine = pyttsx3.init()
    engine.say(v)
    engine.runAndWait()


def ytSearch():
    queryyt = notepad.selection_get()
    link = "https://www.youtube.com/results?search_query=" + queryyt
    webbrowser.open_new_tab(link)


lineLabel = Label(bottomFrame, text="1.0", justify=CENTER, foreground="orange",
                  font=("Helvetica", 10), borderwidth=0, background="#1b1b1b", activebackground="#1b1b1b")
lineLabel.pack(side=LEFT, padx=6)


def lineUpdate(e):
    cindex = str(notepad.index(INSERT))
    lineLabel.config(text=cindex)


def encypt():
    import base64
    cindex = notepad.index(INSERT)
    sample_string = notepad.selection_get()
    sample_string_bytes = sample_string.encode("ascii")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_encoded = base64_bytes.decode("ascii")

    notepad.insert(cindex, base64_encoded)


def decode():
    base64_string = notepad.selection_get()
    base64_bytes = base64_string.encode("ascii")

    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")

    notepad.insert(notepad.index(INSERT), sample_string)


def cmdList():
    tt = Toplevel()
    tt.geometry("1397x1080")
    tt.state('zoomed')
    tt.config(background="#f8f3f3")
    img_label = Label(tt, image=cmdlist_icon, background="#f8f3f3")
    img_label.image = cmdlist_icon
    img_label.pack()
    tt.mainloop()


def cmdNew():  # file menu New option
    global fileName
    if len(notepad.get('1.0', END + '-1c')) > 0:
        if messagebox.askyesno("Notepad", "Do you want to save changes?"):
            cmdSaveAs()
            minibuffer.insert(0.0, "New file has been created!")
        else:
            notepad.delete(0.0, END)
            minibuffer.insert(0.0, "New file has been created!")


def cmdOpenUp(e):  # file menu Open option
    fd = filedialog.askopenfile(parent=root, mode='r')
    t = fd.read()  # t is the text read through filedialog
    notepad.delete(0.0, END)
    notepad.insert(0.0, t)
    minibuffer.delete(0.0, END)
    minibuffer.insert(0.0, "File opened Successfully!")


def insertDateUp():
    cdate = str(date.today())
    notepad.insert(1.0, cdate)


minibuffer = Text(bottomFrame, background="#1b1b1b", foreground="orange", height=1, borderwidth=0, width=30)
minibuffer.pack(side=RIGHT, padx=2)


def cmdSaveAs():  # file menu Save As option
    fd = filedialog.asksaveasfile(mode='w', defaultextension='.txt', initialfile="textfile")
    t = notepad.get(0.0, END)  # t stands for the text gotten from notepad
    try:
        fd.write(t.rstrip())
        minibuffer.insert(0.0, "File Saved Successfully!")
    except ValueError:
        messagebox.showinfo(title="Error", message="Not able to save file!")


def cmdExit():  # file menu Exit option
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


def checkEvenOdd():
    aa = int(notepad.selection_get())

    if aa % 2 == 0:
        messagebox.showinfo("Even!", "Even Number Found")
    else:
        messagebox.showinfo("Odd!", "Odd Number Found")


def checkPrime():
    num = int(notepad.selection_get())

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

    def translateFull():
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

    aa = StringVar()
    auto_detect = ttk.Combobox(tpage, width=20, textvariable=aa, state='readonly', font=('verdana', 10, 'bold'),
                               background="#1b1b1b")

    auto_detect['values'] = (
        'Auto Detect',
    )

    auto_detect.place(x=30, y=70)
    auto_detect.current(0)

    l = StringVar()
    choose_langauge = ttk.Combobox(tpage, width=20, textvariable=l, state='readonly', font=('verdana', 10, 'bold'),
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

    button = ttk.Button(tpage, text="Translate",
                        cursor="hand2",
                        command=translate)
    button.place(x=150, y=280)

    clear = ttk.Button(tpage, text="Clear", cursor="hand2",
                       command=clear)
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


def fullTranslate():
    v = notepad.get(0.0, END)
    tpage = Tk()
    tpage.title('Translator - Aura Notes')
    tpage.geometry('530x330')
    tpage.config(background="#212121")
    tpage.maxsize(530, 330)
    tpage.minsize(530, 330)

    def translateNow():
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

    aa = StringVar()
    auto_detect = Combobox(tpage, width=20, textvariable=aa, state='readonly', font=('verdana', 10, 'bold'),
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
                            command=translateNow, background="#1b1b1b", foreground="white",
                            activebackground="#1b1b1b",
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


def cmdPaste():  # edit menu Paste option
    notepad.event_generate("<<Paste>>")


def cmdSelectAll():  # edit menu Select All option
    notepad.event_generate("<<SelectAll>>")


def wiki():
    global query
    w = Tk()

    try:
        query = notepad.selection_get()
    except ValueError:
        messagebox.showerror("Error!", "Select any text or word to continue")
        w.destroy()

    w.configure(background="#1b1b1b"), w.title("Wikipedia"), w.resizable(False, False)

    text = Text(w, background="#1b1b1b", foreground="white", font=("Helvetica", 12))
    text.pack(pady=10)

    def copy():
        aa = text.get(1.0, END)
        pyperclip.copy(aa)

    ttk.Button(w, text="Copy Article", command=copy).place(x=295, y=460)

    result = wikipedia.page(query).content

    text.insert(1.0, result)
    text.config(state=DISABLED)


def cmdUndo():
    notepad.edit_undo()


def cmdRedo():
    notepad.edit_redo()


# text box for entry
notepad = Text(root, font=("Arial 15", 13), height=48, foreground="white",
               insertbackground="light blue", borderwidth=0, undo=True)

notepad.bind('<KeyPress>', lineUpdate)
notepad.bind('<KeyRelease>', lineUpdate)

with open("synhig.txt", 'r+') as syn:
    synhigh = syn.readline()

with open("theme.txt", 'r+') as thm:
    themeget = thm.readline()

with open("auto_intend.txt", 'r+') as ain:
    autointendget = ain.readline()

with open("tabnumber.txt", 'r+') as tbn:
    tabnumberget = tbn.readline()


def auto_indent(event):
    text = event.widget

    # get leading whitespace from current line
    line = text.get("insert linestart", "insert")
    match = re.match(r'^(\s+)', line)
    whitespace = match.group(0) if match else ""

    # insert the newline and the whitespace
    text.insert("insert", f"\n{whitespace}")

    # return "break" to inhibit default insertion of newline
    return "break"


def tab_pressed(event: Event) -> str:
    tabnumber = int(tabnumberget)
    # Insert the 4 spaces
    notepad.insert("insert", " " * tabnumber)
    # Prevent the default tkinter behaviour
    return "break"


def syntaxHighlighting():
    cdg = ColorDelegator()
    cdg.tagdefs['COMMENT'] = {'foreground': 'grey', 'background': '#151718'}
    cdg.tagdefs['KEYWORD'] = {'foreground': 'orange', 'background': '#151718'}
    cdg.tagdefs['BUILTIN'] = {'foreground': 'gold', 'background': '#151718'}
    cdg.tagdefs['STRING'] = {'foreground': 'light green', 'background': '#151718'}
    cdg.tagdefs['DEFINITION'] = {'foreground': 'gold', 'background': '#151718'}
    cdg.tagdefs['BRACKETS'] = {'foreground': '#007F7F', 'background': '#151718'}
    Percolator(notepad).insertfilter(cdg)


def auto_intend():
    notepad.bind("<Return>", auto_indent)
    notepad.bind("<Tab>", tab_pressed)


if synhigh == "stx":
    syntaxHighlighting()


def searchStack():
    cquery = notepad.selection_get()
    l = "https://stackoverflow.com/search?q=" + cquery + "&s=ddab4d49-a574-4a62-8794-24ac8a478c20"
    webbrowser.open_new_tab(l)


notepad.tag_configure("tag_name", justify='center')

scrollbar = ttk.Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
notepad.config(yscrollcommand=scrollbar.set, background="#151718")
scrollbar.config(command=notepad.yview, )

notepad.focus_set()

notepad.pack(fill=BOTH, side=TOP)


def mathSolver():
    sel = (notepad.selection_get())
    import wolframalpha
    app_id = 'WRWRJG-VKEWL3TXXA'
    client = wolframalpha.Client(app_id)
    res = client.query(sel)
    answer = next(res.results).text
    messagebox.showinfo("Result", answer)


def alwaysOnTop():
    root.attributes('-topmost', 1)


def noteOpen():  # file menu Open option
    fd = filedialog.askopenfile(parent=root, mode='r')
    t = fd.read()  # t is the text read through filedialog
    notepad.delete(0.0, END)
    notepad.insert(0.0, t)


# Calendar
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


def find(e):
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
    edit.focus_set()


def mathExpUp():
    global res_txt
    exp = notepad.selection_get()
    res = str(eval(exp))
    res_txt = str("Expression Result: " + res)
    messagebox.showinfo("Result", res_txt)


notepad_right_click_event = Menu(notepad, tearoff=0)
notepad_right_click_event.config(borderwidth=0, background='#2c2f33', foreground="orange")

cmenubar = Menu(notepad_right_click_event, background='blue', fg='orange')
web_tools = Menu(cmenubar, tearoff=False, background="#2c2f33", foreground="orange")
numericals = Menu(cmenubar, tearoff=False, background="#2c2f33", foreground="orange")
mail_tools = Menu(cmenubar, tearoff=False, background="#2c2f33", foreground="orange")
highlight_text = Menu(cmenubar, tearoff=False, background="#2c2f33", foreground="orange")
translate = Menu(cmenubar, tearoff=False, background="#2c2f33", foreground="orange")
encode = Menu(cmenubar, tearoff=False, background="#2c2f33", foreground="orange")
speak = Menu(cmenubar, tearoff=False, background="#2c2f33", foreground="orange")


def searchGithub():
    gquery = notepad.selection_get()
    link = "https://github.com/search?q=" + gquery
    webbrowser.open_new_tab(link)


def highlightText():
    st_ind = notepad.index("sel.first")
    end_ind = notepad.index("sel.last")

    notepad.tag_add("start", st_ind, end_ind)
    notepad.tag_config("start", background="gold", foreground="black")


web_tools.add_command(label="Google", command=search)
web_tools.add_command(label="Wikipedia for article", command=wiki)
web_tools.add_command(label="Youtube                              Ctrl + Y", command=ytSearch)
web_tools.add_command(label="StackOverflow", command=searchStack)
web_tools.add_command(label="GitHub", command=searchGithub)

encode.add_command(label="Encode Base64", command=encypt)
encode.add_command(label="Decode Base64", command=decode)

speak.add_command(label="Speak Selection", command=rightSpeak)
speak.add_command(label="Speak Full Note", command=fullSpeak)

translate.add_command(label="Translate Selection", command=rightTranslate)
translate.add_command(label="Translate Full Note", command=fullTranslate)


def clearHighlight():
    st_ind = notepad.index("sel.first")
    end_ind = notepad.index("sel.last")

    notepad.tag_remove("start", st_ind, end_ind)


highlight_text.add_command(label="Highlight", command=highlightText)
highlight_text.add_command(label="Remove Highlight", command=clearHighlight)


def to_and_from():
    global a
    a = notepad.index(tkinter.INSERT)

    text = "To: " + "\n" + "\n" + "\n" + "From: "

    notepad.insert(a, text)


def add_footer():
    cindex = notepad.index(tkinter.INSERT)

    text = "Your Sincerely," + "\n" + "<Your Name>"

    notepad.insert(cindex, text)


fontList = ["Arial", "Helvetica", "Futura"]


def add_full_format():
    from datetime import date

    cind = notepad.index(tkinter.INSERT)

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

    notepad.insert(cind, text)


mail_tools.add_command(label="Add full mail format", command=add_full_format)
mail_tools.add_command(label="Add 'To' and 'From' formatting", command=to_and_from)
mail_tools.add_command(label="Add footer", command=add_footer)

numericals.add_command(label="Calculate Expression", command=mathExpUp)
numericals.add_command(label="Check EVEN or ODD", command=checkEvenOdd)
numericals.add_command(label="Check if PRIME", command=checkPrime)

notepad_right_click_event.add_command(label="Copy                               Ctrl + C", command=cmdCopy)
notepad_right_click_event.add_command(label="Paste                               Ctrl + V", command=cmdPaste)
notepad_right_click_event.add_command(label="Select All                          Ctrl + A", command=cmdSelectAll)
notepad_right_click_event.add_command(label="Cut                                  Ctrl + X", command=cmdCut)

# keyboard shortcuts for notepad
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

notepad_right_click_event.add_separator()

notepad_right_click_event.add_cascade(label="Speak", menu=speak)
notepad_right_click_event.add_cascade(label="Translate", menu=translate)
notepad_right_click_event.add_cascade(label="Highlight", menu=highlight_text)
notepad_right_click_event.add_cascade(label="Search In", menu=web_tools)
notepad_right_click_event.add_cascade(label="Numericals", menu=numericals)
notepad_right_click_event.add_cascade(label="Encrypt", menu=encode)


def notes_popup(event):
    try:
        notepad_right_click_event.tk_popup(event.x_root, event.y_root)

    finally:
        notepad_right_click_event.grab_release()


notepad.bind("<Button-3>", notes_popup)


# Prompt while exiting the app
def ExitApplication():
    MsgBox = messagebox.askquestion('Close Document',
                                    'The app is about to close. Do you want to save this document?',
                                    icon='warning')
    if MsgBox == 'yes':
        cmdSaveAs()
    else:
        root.destroy()


# 25% Transparency
def Transparent25():
    root.attributes('-alpha', 0.75)


def Transparent20():
    root.attributes('-alpha', 0.75)


def Calculator():
    from Calculator import calc
    calc.run()


def Transparent30():
    root.attributes('-alpha', 0.75)


def Transparent40():
    root.attributes('-alpha', 0.75)


def highContrastMode():
    notepad.config(background="black", foreground="#44ad88")
    cmd_line.config(background="grey")
    resize.config(background="black")
    topFrame.config(background="black")


def darkmode():
    notepad.config(background="#151718", foreground="white")
    topFrame.config(background="#1b1b1b")
    cmd_line.config(background="black")
    resize.config(background="#1b1b1b")


def lightmode():
    notepad.config(background="#d3d3d3", foreground="black")
    topFrame.config(background="white")
    cmd_line.config(background="white")
    resize.config(background="white")


if themeget == "dark":
    darkmode()
elif themeget == "light":
    lightmode()
else:
    highContrastMode()

if autointendget == "on":
    auto_intend()

mails = Menubutton(topFrame, text="Mail", background="#1b1b1b", activebackground="#1b1b1b", borderwidth=0)
translate = Menubutton(topFrame, text="Translate", background="#1b1b1b", activebackground="#1b1b1b", borderwidth=0)

textfinded.pack(side=RIGHT, padx=20)

mails.menu = Menu(mails, tearoff=0, background="#303030", foreground="cyan", borderwidth=0)
mails["menu"] = mails.menu

translate.menu = Menu(translate, tearoff=0, background="#303030", foreground="cyan", borderwidth=0)
translate["menu"] = translate.menu

mails.menu.add_command(label="Full Format", command=add_full_format)
mails.menu.add_command(label="To & From", command=to_and_from)
mails.menu.add_command(label="Footer", command=add_footer)
mails.menu.add_separator()

translate.menu.add_command(label="Translate Selection", command=rightTranslate)
translate.menu.add_command(label="Translate Full Note", command=fullTranslate)


# 50% Transparency
def Transparent50():
    root.attributes('-alpha', 0.5)


# 75% Transparency
def Transparent75():
    root.attributes('-alpha', 0.25)


# Reset transparency to default (0%)
def resetTransparent():
    root.attributes('-alpha', 1)


# Summary function. Returns char and line counts
def Summary():
    note_lines = str(notepad.index('end-1c').split('.')[0])
    note_char_count = str(len(notepad.get("1.0", 'end-1c')))
    note_cindex = notepad.index(INSERT)

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


menubar = Menu(root, background='blue', fg='white')

font1 = ['Arial', 13]


def zoomin(str1):
    if str1 == 'plus':
        font1[1] = font1[1] + 2
    else:
        font1[1] = font1[1] - 2

    notepad.config(font=font1)


# Declare file and edit for showing in menubar
file = Menu(menubar, tearoff=False, background='#2c2f33', foreground="orange")
edit = Menu(menubar, tearoff=False, background='#2c2f33', foreground="orange")
window = Menu(menubar, tearoff=False, background='#2c2f33', foreground="orange")
tools = Menu(menubar, tearoff=False, background="#2c2f33", foreground="orange")
abb = Menu(menubar, tearoff=False, background="#2c2f33", foreground="orange")
accessiblity = Menu(menubar, tearoff=False, background="#2c2f33", foreground="orange")
view = Menu(menubar, tearoff=False, background="#2c2f33", foreground="orange")
helptab = Menu(menubar, tearoff=False, background="#2c2f33", foreground="orange")

transparency = Menu(window, tearoff=False, background="#2c2f33", foreground="orange")

transparency.add_command(label="20%", command=Transparent20)
transparency.add_command(label="25%", command=Transparent25)
transparency.add_command(label="30%", command=Transparent30)
transparency.add_command(label="50%", command=Transparent50)
transparency.add_command(label="75%", command=Transparent75)
transparency.add_command(label="Reset", command=resetTransparent)

helptab.add_command(label="Manual", command=manual)
helptab.add_command(label="Command List", command=cmdList)


def version():
    text = "Current Version: " + "1.0.6" + "\n" + "\n" + "\n" + "What's New:" + "\n" + "\n" + "* Improved Color Science" + "\n" \
           + "* Complete Visual Overhaul with simpler look" + "\n" + "* New Mailing templates" + "\n" + "* Scheduled Writing Feature" + "\n" + "* More organised menus" + "\n" + "* Improved overall Stability"

    messagebox.showinfo("Version Info", text)


# Add commands in file menu
file.add_command(label="New Document", command=cmdNew)
file.add_command(label="Open Document", command=noteOpen)
file.add_command(label="Save Document", command=cmdSaveAs)
file.add_command(label="Summary", command=Summary)
file.add_command(label="Exit", command=cmdExit)

view.add_command(label="Zoom In", command=lambda: zoomin("plus"))
view.add_command(label="Zoom Out", command=lambda: zoomin("minus"))

edit.add_command(label="Copy", command=cmdCopy)
edit.add_command(label="Paste", command=cmdPaste)
edit.add_command(label="Cut", command=cmdCut)
edit.add_command(label="Select All", command=cmdSelectAll)
edit.add_command(label="Undo", command=cmdUndo)
edit.add_command(label="Redo", command=cmdRedo)

# Add commands in window menu
window.add_command(label="Minimize", command=minimize)
window.add_command(label="Maximize", command=maximize)
window.add_checkbutton(label="Always on Top", command=mathSolver)
window.add_cascade(label="Window Transparency", menu=transparency)

# Add commands in tools menu
# tools.add_command(label="Universal Search", command=mathSolver)
tools.add_command(label="Calendar", command=calendar)
tools.add_command(label="Calculator", command=Calculator)
tools.add_cascade(label="Mail Tools", menu=mail_tools)


def minibufferClear(e):
    def delete():
        minibuffer.delete(0.0, END)

    root.after(3500, delete)


root.bind('<KeyRelease>', minibufferClear)
root.bind('<FocusIn>', minibufferClear)
root.bind('<MouseWheel>', minibufferClear)

# Add commands in about menu
abb.add_command(label="Current Version", command=version)


def settings():
    import settingsNotes
    settingsNotes.settings()


# Display the file and edit declared in previous step
menubar.add_cascade(label="File", menu=file)
menubar.add_cascade(label="Edit", menu=edit)
menubar.add_cascade(label="Window", menu=window)
menubar.add_cascade(label="View", menu=view)
menubar.add_cascade(label="Tools", menu=tools)
menubar.add_cascade(label="Help", menu=helptab)
menubar.add_command(label="Settings", command=settings)
menubar.add_cascade(label="About", menu=abb)

textfinded.bind('<KeyRelease>', find)
textfinded.bind('<FocusIn>', find)
textfinded.bind('<MouseWheel>', find)

# Displaying of menubar in the app
root.config(menu=menubar)

# Setting the notepad as the main focus point
notepad.focus_set()

root.protocol("WM_DELETE_WINDOW", ExitApplication)

# Redirecting to main screen after specific time

# main loop
mainloop()
