import datetime
import os
import webbrowser
from tkinter import *
import tkinter
from tkinter import messagebox, filedialog, simpledialog
import wikipedia
from tkinter.ttk import Combobox, Notebook
import pyperclip
import pyttsx3
from PIL import ImageTk, Image
from googletrans import Translator
from datetime import date
from cryptography.fernet import Fernet
from tkinter import ttk

# main gui window for editor
editor = Tk()
editor.title("Aura Notes")

# deciding which theme to use
editor.config(background="#141414")

# making the window resizable and adjusting its size
editor.resizable(True, True)
editor.state('zoomed')
editor.iconbitmap("notes.ico")

# top frame to accompany menu bar and stuff
# topFrame = tkinter.Frame(editor, background="#212121", width=1550, height=45).place(x=2, y=8)

clear_icon = ImageTk.PhotoImage(Image.open('clear.png').resize((27, 27)))
plus_icon = ImageTk.PhotoImage(Image.open('add-button.png').resize((15, 15)))
minus_icon = ImageTk.PhotoImage(Image.open('minus.png').resize((15, 15)))
ig_icon = ImageTk.PhotoImage(Image.open('instagram.png').resize((27, 27)))


def rightSpeak():
    v = notepad.selection_get()
    engine = pyttsx3.init()
    engine.say(v)
    engine.runAndWait()


menu_number = ""


def toolPage():
    h = tkinter.Tk()
    h.geometry("700x600"), h.config(background="#1b1b1b"), h.title("Tools Page - Aura Notes")

    tc = ttk.Notebook(h)

    calc = Frame(tc, background="#1b1b1b")
    enc = Frame(tc, background="#1b1b1b")

    tc.add(enc, text="Encryption")

    ttk.Label(enc, text="Normal Text", background="#1b1b1b", foreground="white").place(x=87, y=27)
    ttk.Label(enc, text="Encrypted Text", background="#1b1b1b", foreground="white").place(x=500, y=27)

    T = Text(enc, foreground="white", background="#1b1b1b", borderwidth=0.8, height=8, width=29,
             insertbackground="white")
    En = Text(enc, foreground="white", background="#1b1b1b", borderwidth=0.8, height=8, width=29)
    T.place(x=20, y=50)
    En.place(x=430, y=50)

    T.focus_set()

    def ec():
        msg = T.get(1.0, END)
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encMessage = fernet.encrypt(msg.encode())
        enc = str(encMessage)

        En.delete(1.0, END)
        En.insert(0.1, enc)
        En.config(state=DISABLED)

    def copy():
        t = En.get(1.0, END)
        pyperclip.copy(t)

    Button(enc, text="Encrypt", background="#1b1b1b", foreground="white", borderwidth=0, command=ec,
           cursor="hand2").place(x=320, y=300)

    Button(enc, text="Copy Encrypted Text", background="#1b1b1b", foreground="white", borderwidth=0, command=copy,
           cursor="hand2").place(x=288, y=340)

    tc.pack(side=TOP, fill=BOTH, expand=10)

    h.mainloop()


def speak(e):
    v = notepad.get(1.0, END)

    if v is None:
        messagebox.showerror("Error", "Type any text to speak")

    engine = pyttsx3.init()
    engine.say(v)
    engine.runAndWait()


def speakUp():
    v = notepad.get(1.0, END)

    if v is None:
        messagebox.showerror("Error", "Type any text to speak")

    engine = pyttsx3.init()
    engine.say(v)
    engine.runAndWait()


# useful datas
af = os.listdir(r'C:\Windows\fonts')
availFonts = list(af)
fontSizes = list(range(1, 31))


def cmdNew(e):  # file menu New option
    global fileName
    if len(notepad.get('1.0', END + '-1c')) > 0:
        if messagebox.askyesno("Notepad", "Do you want to save changes?"):
            cmdSave()
        else:
            notepad.delete(0.0, END)
    editor.title("Notepad")


def cmdSave(e):  # file menu Save option
    fd = filedialog.asksaveasfile(mode='w', defaultextension='.txt', initialfile="textfile")
    if fd is not None:
        data = notepad.get('1.0', END)
    try:
        fd.write(data)
    except:
        messagebox.showerror(title="Error", message="Not able to save file!")


def cmdOpen():  # file menu Open option
    fd = filedialog.askopenfile(parent=editor, mode='r')
    t = fd.read()  # t is the text read through filedialog
    notepad.delete(0.0, END)
    notepad.insert(0.0, t)


def about():
    messagebox.showinfo("About",
                        "Aura Notes Stable Build (Orchid v1.0.1)" + "\n" + "\n" +
                        "Version: 1.0.1 (Orchid)" + "\n" + "\n" + "\n" + "Developed with love by Rohan. See Whats new below!" + "\n" + "\n" + "\n" +
                        "* Added shortcut for inserting the current date" + "\n" +
                        "* Stability Improvements" + "\n" +
                        "* Fixed a bug where the app closes itself when calculating math expressions" + "\n" + "\n" +
                        "* Improved the speed of Wikipedia search")


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
    notepad.insert(0.0, cdate)


def cmdSaveAs():  # file menu Save As option
    fd = filedialog.asksaveasfile(mode='w', defaultextension='.txt', initialfile="textfile")
    t = notepad.get(0.0, END)  # t stands for the text gotten from notepad
    try:
        fd.write(t.rstrip())
    except:
        messagebox.showinfo(title="Error", message="Not able to save file!")


def cmdExit():  # file menu Exit option
    if messagebox.askyesno("Notepad", "Are you sure you want to exit?"):
        editor.destroy()


def cmdExitUp(e):  # file menu Exit option
    if messagebox.askyesno("Notepad", "Are you sure you want to exit?"):
        editor.destroy()


def cmdCut():  # edit menu Cut option
    notepad.event_generate("<<Cut>>")


def cmdCopy():  # edit menu Copy option
    notepad.event_generate("<<Copy>>")


def cmdCopyUp(e):  # edit menu Copy option

    notepad.event_generate("<<Copy>>")


def translate():
    tpage = Tk()
    tpage.title('Langauge Translator - Aura Notes')
    tpage.geometry('530x330')
    tpage.config(background="#212121")
    tpage.maxsize(530, 330)
    tpage.minsize(530, 330)

    def translate():
        language_1 = t1.get("1.0", "end-1c")
        cl = choose_langauge.get()

        if language_1 == '':
            messagebox.showerror('Language Translator', 'please fill the box')
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

    t1 = Text(tpage, width=30, height=10, borderwidth=2, relief=RIDGE, background="#1b1b1b", insertbackground="white",
              foreground="white")
    t1.focus_set()
    t1.place(x=10, y=100)

    t2 = Text(tpage, width=30, height=10, borderwidth=2, relief=RIDGE, background="#1b1b1b", insertbackground="white",
              foreground="white")
    t2.place(x=260, y=100)

    button = Button(tpage, text="Translate", relief=RIDGE, borderwidth=1, background="#1b1b1b", foreground="white",
                    font=('verdana', 10, 'bold'), cursor="hand2",
                    command=translate)
    button.place(x=150, y=280)

    clear = Button(tpage, text="Clear", relief=RIDGE, borderwidth=1, font=('verdana', 10, 'bold'), cursor="hand2",
                   command=clear, background="#1b1b1b", foreground="white")
    clear.place(x=280, y=280)

    tpage.mainloop()


def search():
    query = notepad.selection_get()
    link = str(
        "https://www.google.com/search?q=" + query + "&oq=hi&aqs=chrome..69i57j69i59j0i67l2j46i67j69i60j69i61l2.422j0j4&sourceid=chrome&ie=UTF-8")
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

    t1 = Text(tpage, width=30, height=10, borderwidth=2, relief=RIDGE, background="#1b1b1b", insertbackground="white",
              foreground="white")
    t1.focus_set()
    t1.place(x=10, y=100)
    t1.insert(1.0, v)

    t2 = Text(tpage, width=30, height=10, borderwidth=2, relief=RIDGE, background="#1b1b1b", insertbackground="white",
              foreground="white")
    t2.place(x=260, y=100)

    button = Button(tpage, text="Translate", relief=RIDGE, borderwidth=0, font=('verdana', 10, 'bold'), cursor="hand2",
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

    def popup(event):
        try:
            rightclickevent.tk_popup(event.x_root, event.y_root)

        finally:
            rightclickevent.grab_release()

    t1.bind("<Button-3>", popup)

    tpage.mainloop()


def aboutPage():
    ab = Tk()
    ab.geometry("700x700"), ab.config(background="#1b1b1b"), ab.resizable(False, False)
    ab.title("About - Aura Notes")

    Label(ab, text="ABOUT", font=("Didot", 13, "bold"), background="#1b1b1b", foreground="white").pack(pady=7)
    Label(ab, text="Aura Notes is a notepad app for Windows. It is completely free with no ads.",
          font=("Didot", 12, "italic"),
          background="#1b1b1b", foreground="white").place(x=100, y=45)

    Label(ab, text="Version:", font=("Didot", 12, "bold"),
          background="#1b1b1b", foreground="white").place(x=5, y=125)

    Label(ab, text="1.0.0 (Orchid Build)", font=("Didot", 12, "italic"),
          background="#1b1b1b", foreground="white").place(x=160, y=125)

    Label(ab, text="What's new in this version:", font=("Didot", 12, "bold"),
          background="#1b1b1b", foreground="white").place(x=5, y=195)

    Label(ab, text="* Added Shortcut for adding current date", font=("Didot", 11, "italic"),
          background="#1b1b1b", foreground="white").place(x=5, y=235)

    Label(ab, text="* Fixed an issue where app crashes while trying to search Wikipedia", font=("Didot", 11, "italic"),
          background="#1b1b1b", foreground="white").place(x=5, y=260)

    Label(ab, text="* Overall Stability Improvements", font=("Didot", 11, "italic"),
          background="#1b1b1b", foreground="white").place(x=5, y=285)

    Label(ab, text="Icon Credits:", font=("Didot", 12, "bold"),
          background="#1b1b1b", foreground="white").place(x=5, y=355)

    Label(ab, text="* Feen (Zoom in Button)", font=("Didot", 11, "italic"),
          background="#1b1b1b", foreground="white").place(x=5, y=395)

    Label(ab, text="* Pixel Perfect (Zoom out Button)", font=("Didot", 11, "italic"),
          background="#1b1b1b", foreground="white").place(x=5, y=420)

    Label(ab, text="* Iconproject45 (Close Button)", font=("Didot", 11, "italic"),
          background="#1b1b1b", foreground="white").place(x=5, y=445)

    Label(ab, text="* Freepik (Menu Button)", font=("Didot", 11, "italic"),
          background="#1b1b1b", foreground="white").place(x=5, y=470)

    def icon_collection_link():
        link = "https://www.flaticon.com/collections/27372811"
        webbrowser.open_new_tab(link)

    def childHelp():
        webbrowser.open_new_tab("https://www.unicef.org/india/take-action/donate-to-unicef")

    def insta():
        webbrowser.open_new_tab("www.instagram.com/jops.rekt/")

    def gitSource():
        webbrowser.open_new_tab()

    Button(ab, text="Get the Icon Collection", background="#1b1b1b", borderwidth=0, foreground="red",
           activeforeground="white", activebackground="#1b1b1b",
           width=19, height=4, command=icon_collection_link, cursor="hand2").place(x=340, y=412)

    img = ig_icon

    insta = Button(ab, text="Follow Developer on Instagram", background="#1b1b1b", borderwidth=1,
                   activeforeground="white", activebackground="#1b1b1b", foreground="white",
                   width=35, height=3, command=insta, cursor="hand2")

    ch = Button(ab, text="Help a child by donating to UNICEF", background="#1b1b1b", borderwidth=1,
                activeforeground="white", activebackground="#1b1b1b", foreground="white",
                width=35, height=3, command=childHelp, cursor="hand2")

    ch = Button(ab, text="Get Source", background="#1b1b1b", borderwidth=1,
                activeforeground="white", activebackground="#1b1b1b", foreground="white",
                width=35, height=3, command=childHelp, cursor="hand2")

    insta.place(x=25, y=572)
    ch.place(x=350, y=572)


def cmdPaste():  # edit menu Paste option
    notepad.event_generate("<<Paste>>")


def cmdClear():  # edit menu Clear option
    notepad.event_generate("<<Clear>>")


def toggle_win():
    global f1
    f1 = Frame(editor, width=300, height=885, bg='black')
    f1.place(x=0, y=0)

    # buttons
    def bttn(x, y, text, bcolor, fcolor, cmd):
        def on_entera(e):
            myButton1['background'] = 'black'  # ffcc66
            myButton1['foreground'] = 'red'  # 000d33

        def on_leavea(e):
            myButton1['background'] = "black"
            myButton1['foreground'] = 'white'

        myButton1 = Button(f1, text=text,
                           width=42,
                           height=2,
                           fg='white',
                           border=0,
                           bg=fcolor,
                           activeforeground='pink',
                           activebackground="black",
                           command=cmd)

        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x, y=y)

    bttn(0, 117, 'T R A N S L A T E', "black", 'black', translate)
    bttn(0, 174, 'S P E A K', 'black', 'black', speakUp)
    bttn(0, 231, 'O P E N', 'black', 'black', cmdOpen)
    bttn(0, 288, 'S A V E', 'black', 'black', cmdSaveAs)
    bttn(0, 345, 'E X I T', '#1B1B1B', 'black', cmdExit)
    bttn(0, 402, 'T O O L S', '#1B1B1B', 'black', toolPage)
    bttn(0, 459, 'A B O U T', '#1B1B1B', 'black', aboutPage)

    def dele():
        f1.destroy()
        b2 = Button(editor, image=img1,
                    command=toggle_win,
                    border=0, background="#141414",
                    activebackground='#262626', cursor="hand2")
        b2.place(x=5, y=8)

    global img2
    img2 = ImageTk.PhotoImage(Image.open("close.png").resize((30, 30)))

    Button(f1,
           image=img2,
           borderwidth=0,
           command=dele,
           border=0,
           bg='black',
           activebackground='black', cursor="hand2", activeforeground="black").place(x=5, y=10)


img1 = ImageTk.PhotoImage(Image.open("menu.png").resize((40, 40)))

global b2
b2 = tkinter.Button(editor, image=img1,
                    command=toggle_win,
                    border=0,
                    borderwidth=0,
                    bg='#141414',
                    activebackground='#141414', activeforeground="#141414", cursor="hand2", background="#141414")
b2.place(x=8, y=8)


def click(event):  # handling click event
    notepad.tag_config('Found', background='white', foreground='black')


def cmdSelectAllUp(e):  # edit menu Select All option
    notepad.event_generate("<<SelectAll>>")


def cmdSelectAll():  # edit menu Select All option
    notepad.event_generate("<<SelectAll>>")


def cmdTimeDate():  # edit menu Time/Date option
    now = datetime.now()
    # dd/mm/YY H:M:S
    dtString = now.strftime("%d/%m/%Y %H:%M:%S")
    label = messagebox.showinfo("Time/Date", dtString)


def copyFull():
    n = notepad.get(1.0, END)
    pyperclip.copy(n)


def wikiUp(e):
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

    Button(w, background="#1b1b1b", foreground="white", text="Copy Article", activebackground="#1b1b1b",
           activeforeground="white", borderwidth=0, command=copy).place(x=295, y=460)

    result = wikipedia.summary(query, auto_suggest=False, sentences=6)

    text.insert(1.0, result)
    text.config(state=DISABLED)


def wiki():
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

    Button(w, background="#1b1b1b", foreground="white", text="Copy Article", activebackground="#1b1b1b",
           activeforeground="white", borderwidth=0, command=copy).place(x=295, y=460)

    result = wikipedia.summary(query, auto_suggest=False, sentences=6)

    text.insert(1.0, result)
    text.config(state=DISABLED)


# text box for entry
notepad = Text(editor, font=("Helvetica", 13), height=42, width=169, background="#1b1b1b", foreground="white",
               insertbackground="white", borderwidth=0.5)

notepad.focus_set()
notepad.place(x=5, y=54)

font1 = ['Helvetica', 13]


def zoomin(str1):
    if str1 == 'plus':
        font1[1] = font1[1] + 2
    else:
        font1[1] = font1[1] - 2
    notepad.config(font=font1)


def mathExp():
    exp = notepad.selection_get()
    try:
        res = str(eval(exp))
        res_txt = str("Expression Result: " + res)
    except:
        messagebox.showerror("Error", "Given input isn't an math expression!")
    a = Label(editor, text=res_txt, font=("ds-digital", 12), background="#141414", foreground="cyan").place(x=30, y=860)


def mathExpUp(e):
    exp = notepad.selection_get()
    try:
        res = str(eval(exp))
        res_txt = str("Expression Result: " + res)
    except:
        messagebox.showerror("Error", "Given input isn't an math expression!")
    Label(editor, text=res_txt, font=("ds-digital", 12), background="#1b1b1b", foreground="cyan").place(x=30, y=860)


gg = StringVar()

right_click_event = Menu(notepad, tearoff=0)
right_click_event.config(borderwidth=0)
right_click_event.add_command(label="Copy                                                                     Ctrl + C",
                              command=cmdCopy)
right_click_event.add_command(
    label="Paste                                                                     Ctrl + V", command=cmdPaste)
right_click_event.add_command(label="Select All                                                              Ctrl + A",
                              command=cmdSelectAll)
right_click_event.add_command(
    label="Cut                                                                        Ctrl + X", command=cmdCut)
right_click_event.add_command(label="Speak", command=rightSpeak)
right_click_event.add_command(label="Translate                                                              Ctrl + T",
                              command=rightTranslate)
right_click_event.add_command(label="Copy Full Note", command=copyFull)
right_click_event.add_command(label="Add Today's Date                                               Ctrl + D",
                              command=insertDate)
right_click_event.add_command(label="Calculate Math Expression                               Ctrl + M", command=mathExp)
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
    MsgBox = messagebox.askquestion('Exit Application', 'Do you want to save the file?', icon='warning')
    if MsgBox == 'yes':
        cmdSaveAs()
    else:
        editor.destroy()


# keyboard shortcuts
editor.bind('<Control-o>', cmdOpenUp)
editor.bind('<Control-c>', cmdCopyUp)
editor.bind('<Control-s>', cmdSave)
editor.bind('<Control-b>', rightSpeak)
editor.bind('<Control-t>', translate)
editor.bind('<Control-m>', mathExpUp)
editor.bind('<Control-w>', wikiUp)
editor.bind('<Control-d>', insertDateUp)

editor.protocol("WM_DELETE_WINDOW", ExitApplication)

Button(editor, image=plus_icon, command=lambda: zoomin('plus'), background="#141414", activebackground="#141414",
       activeforeground="#141414", borderwidth=0, cursor="hand2").place(x=1470, y=860)

Button(editor, image=minus_icon, command=lambda: zoomin('minus'), background="#141414", activebackground="#141414",
       activeforeground="#141414", borderwidth=0, cursor="hand2").place(x=1500, y=860)

# main loop
editor.mainloop()
