"""
ModuleFile
This file contains all the functions for the features of Aura Notes. This makes the code better accessible and easy to contribute
for the devs
Translate feature isn't included in this file as the number of lines increases dramatically. That's in a different .py file.
"""
import json
import os
import tkinter
import webbrowser
from difflib import get_close_matches
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator
from tkinter import *
from tkinter import messagebox, ttk
import pyttsx3
import wikipedia
import pywhatkit as kit
import cv2
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
        gui.configure(background='#303030')
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
        new.configure(background="#1b1b1b")
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

    tk.configure(background="black")

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
    notepad.configure(background="black", foreground="#44ad88")
    cmd_line.configure(background="grey")
    topFrame.configure(background="black")

def darkmode(notepad, topFrame, cmd_line):
    notepad.configure(background="#1d1d1d", foreground="white")
    topFrame.configure(background="#1d1d1d")
    #cmd_line.configure(background="#313335") #this line give error ('background' is a invalid argument something)

def lightmode(notepad, topFrame, cmd_line):
    notepad.configure(background="#d3d3d3", foreground="black")
    topFrame.configure(background="white")
    cmd_line.configure(background="white")

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
    notepad.tag_configure("start", background="gold", foreground="black")

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
        notepad.tag_configure('found', foreground='red')

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


def get_meaning(notepad):
    data = json.load(open('data.json'))
    word = notepad.selection_get()

    word = word.lower()

    if word in data:
        meaning = data[word]

        for item in meaning:
            messagebox.showinfo('Meaning',  item)

    elif len(get_close_matches(word, data.keys())) > 0:

        close_match = get_close_matches(word, data.keys())[0]

        res = messagebox.askyesno('Confirm', 'Did you mean ' + close_match + ' instead?')

        if res:
            meaning = data[close_match]

            for item in meaning:
                messagebox.showinfo('Meaning', item)

    else:
        messagebox.showerror('Error', 'The word doesnt exist.Please double check it.')

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def talk_meaning(notepad):
    data = json.load(open('data.json'))
    word = notepad.selection_get()

    word = word.lower()

    if word in data:
        meaning = data[word]

        for item in meaning:
            speak(item)

    elif len(get_close_matches(word, data.keys())) > 0:

        close_match = get_close_matches(word, data.keys())[0]

        res = messagebox.askyesno('Confirm', 'Did you mean ' + close_match + ' instead?')

        if res:
            meaning = data[close_match]

            for item in meaning:
                speak(item)

    else:
        messagebox.showerror('Error', 'The word doesnt exist.Please double check it.')


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
    text_w.configure(state=DISABLED)

def find_replace(notepad):
    #find function
    def finnd():
        word = find_input.get()                         #take input from find_input
        notepad.tag_remove("match",'1.0',END)
        matches = 0
        if word:
            start_pos = "1.0"
            while True:
                start_pos = notepad.search(word,start_pos,stopindex=END) #searching for the word
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(word)}c"
                notepad.tag_add("match",start_pos,end_pos)
                matches += 1
                start_pos = end_pos
                notepad.tag_config("match",foreground = "yellow",background = "#1d1d1d")
    def replace():
        word = find_input.get()                 #getting input from variable
        replace_text = replace_input.get()
        content = notepad.get(1.0,END)
        new_content = content.replace(word,replace_text)
        notepad.delete(1.0,END)
        notepad.insert(1.0,new_content)

    find_dialogue = Toplevel()   #inside find windows
    find_dialogue.config(background="#1d1d1d")
    find_dialogue.geometry("450x200")
    find_dialogue.title("Find/replace")
    find_dialogue.resizable(0,0)
    find_frame = LabelFrame(find_dialogue,text = "Find/replace", background="#1d1d1d", foreground="white")
    find_frame.pack(pady = 20)

    text_find_label = ttk.Label(find_frame, text='Find : ', background="#1d1d1d", foreground="cyan")
    text_replace_label = ttk.Label(find_frame, text= 'Replace', background="#1d1d1d", foreground="cyan")

    find_input = ttk.Entry(find_frame, width=30, background="grey")
    replace_input = ttk.Entry(find_frame, width=30)

    find_button = ttk.Button(find_frame, text='Find',command = finnd)
    replace_button = ttk.Button(find_frame, text= 'Replace',command = replace)

    text_find_label.grid(row=0, column=0, padx=4, pady=4)
    text_replace_label.grid(row=1, column=0, padx=4, pady=4)

    find_input.grid(row=0, column=1, padx=4, pady=4)
    replace_input.grid(row=1, column=1, padx=4, pady=4)

    find_button.grid(row=2, column=0, padx=8, pady=20)
    replace_button.grid(row=2, column=1, padx=8, pady=20)

    find_dialogue.mainloop()


