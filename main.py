import base64
import math
import os.path
import re
import tkinter
import webbrowser
from datetime import date
from random import choice
from tkinter import *
from tkinter import messagebox, filedialog
import customtkinter
from customtkinter import *
import ModuleFile
import SearchMod
import Translate
import psutil

# main gui window for editor
root = CTk()
root.tk_setPalette('SystemButtonFace')
root.title("Aura Notes")
root.configure(background="#1d1d1d")

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Function for 'resize_button'
def resize():
    ModuleFile.resize(root)

def new_frame():
    ModuleFile.new_frame()

root.resizable(True, True)

# Making the window maximized always
root.geometry("1300x700")

# Declaring the icon file
root.iconbitmap("icon.ico")

# top frame to accompany menu bar and stuff
topFrame = tkinter.Frame(root, height=50)

# bottom frame for line numbers, cmd, etc
bottomFrame = Frame(root, background="#1b1b1b", height=20)

#packing both
bottomFrame.pack(side=BOTTOM, fill=X)
topFrame.pack(side=TOP, fill=X)

# Find in Notes Entry
textfinded = CTkEntry(topFrame, width=250, text_color="light blue", text_font=("Arial", 12), height=32)

# cmd
cmd_line = CTkEntry(bottomFrame, width=200 , borderwidth=0, text_color="light blue")
cmd_line.pack(side=RIGHT)

# cmd main function
def cmdline(e):
    def ytcmd():
        s = str(cmdget.replace("yt", ""))
        link = "https://www.youtube.com/results?search_query=" + s
        webbrowser.open_new_tab(link)

    def coin_flip():
        choices = ["Heads", "Tails", "Heads", "Tails"]

        aa = choice(choices)

        if aa == "Heads":
            messagebox.showinfo("Toss", "HEADS")
        else:
            messagebox.showinfo("Toss", "TAILS")

    def dice_roll():
        choices = [1, 2, 3, 4, 5, 6]
        aa = choice(choices)
        aa = str(aa)
        messagebox.showinfo("Dice Roll", aa)

    def stackcmd():
        s = str(cmdget.replace("stack", ""))
        stack_link = "https://stackoverflow.com/search?q=" + s + "&s=ddab4d49-a574-4a62-8794-24ac8a478c20"
        webbrowser.open_new_tab(stack_link)

    def githubcmd():
        s = str(cmdget.replace("git", ""))
        link = "https://github.com/search?q=" + s
        webbrowser.open_new_tab(link)

    cmdget = cmd_line.get()

    def ntp_changr_bg():
        s = str(cmdget.replace("npbg ", ""))
        notepad.config(background=s)

    def ntp_changr_fg():
        s = str(cmdget.replace("npfg ", ""))
        notepad.config(foreground=s)

    if "save" in cmdget:
        cmd_save_ss()
    elif "open" in cmdget:
        noteopen()
    elif "new" in cmdget:
        cmd_new()
    elif "dateinsert" in cmdget:
        insert_date_up()
    elif "exit" in cmdget:
        cmdexit()
    elif 'npbg' in cmdget:
        ntp_changr_bg()
    elif 'npfg' in cmdget:
        ntp_changr_fg()
    elif "ftrans" in cmdget:
        full_translate()
    elif "stx" in cmdget:
        syntax_highlighting()
        notepad.config(font="Consolas")
    elif "yt" in cmdget:
        ytcmd()
    elif "stack" in cmdget:
        stackcmd()
    elif "git" in cmdget:
        githubcmd()
    elif "cal" in cmdget:
        calendar()
    elif "wordwrap" in cmdget:
        word_wrap()
    elif "aot" in cmdget:
        alwaysontop()
    elif "mailff" in cmdget:
        add_full_format()
    elif "ain" in cmdget:
        auto_intend()
    elif "mailfooter" in cmdget:
        add_footer()
    elif "mailtf" in cmdget:
        to_and_from()
    elif "cflip" in cmdget:
        coin_flip()
    elif "autoin" in cmdget:
        auto_intend()
    elif "droll" in cmdget:
        dice_roll()
    elif "ltk" in cmdget:
        lightmode()
    elif "dtk" in cmdget:
        darkmode()
    elif "htk" in cmdget:
        highContrastMode()
    elif "cdm" in cmdget:
        syntax_highlighting()
    elif "min" in cmdget:
        minimize()
    elif "max" in cmdget:
        maximize()
    else:
        res = eval(cmdget)
        messagebox.showinfo("Result", res)

def findActivate(e):
    textfinded.focus_set()

def notepadAct(e):
    notepad.focus_set()

cmd_line.bind('<Return>', cmdline)

#speak selection
def right_speak():
    notepad_selection = notepad.selection_get()
    full_notepad_get = notepad.get(0.0, END)
    ModuleFile.rightSpeak(notepad_selection)

# full note speak
def full_speak():
    full_notepad_get = notepad.get(0.0, END)
    ModuleFile.fullSpeak(full_notepad_get)

# yt search
def yt_search():
    SearchMod.yt_search(notepad)

def summary():
    ModuleFile.Summary(notepad)

# base64 encode
def encypt():
    import base64
    cindex = notepad.index(INSERT)
    sample_string = notepad.selection_get()
    sample_string_bytes = sample_string.encode("ascii")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_encoded = base64_bytes.decode("ascii")

    notepad.insert(cindex, base64_encoded)

#base64 decode
def decode():
    base64_string = notepad.selection_get()
    base64_bytes = base64_string.encode("ascii")

    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")

    notepad.insert(notepad.index(INSERT), sample_string)

# cmd cheat list func
def cmd_list():
    webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Notes/wiki/Command-Prompt-for-Aura-Notes")

# new file
def cmd_new():  # file menu New option
    global fileName
    if len(notepad.get('1.0', END + '-1c')) > 0:
        if messagebox.askyesno("Notepad", "Do you want to save changes?"):
            cmd_save_ss()
        else:
            notepad.delete(0.0, END)

# inserting the current date
def insert_date_up():
    cdate = str(date.today())
    notepad.insert(1.0, cdate)

# save file
def cmd_save_ss():  # file menu Save As option
    fd = filedialog.asksaveasfile(mode='w', defaultextension='.txt', initialfile="textfile")
    t = notepad.get(0.0, END)  # t stands for the text gotten from notepad
    try:
        fd.write(t.rstrip())
    except AttributeError:
        messagebox.showinfo(title="No, Not Again!", message="I'm currently not able to save this file!")

# exit the app
def cmdexit():  # file menu Exit option
    if messagebox.askyesno("Notepad", "Are you sure you want to exit?"):
        root.destroy()

# minimize
def minimize():
    root.iconify()

# maximize
def maximize():
    root.state('zoomed')

# cut
def cmdcut():  # edit menu Cut option
    notepad.event_generate("<<Cut>>")

# copy
def cmdcopy():  # edit menu Copy option
    notepad.event_generate("<<Copy>>")

# check if number even or odd
def check_even_odd():
    aa = int(notepad.selection_get())

    if aa % 2 == 0:
        messagebox.showinfo("Even!", "Even Number Found")
    else:
        messagebox.showinfo("Odd!", "Odd Number Found")

# check if number is prime
def checkprime():
    num = int(notepad.selection_get())
    ModuleFile.checkPrime(num)

# google search
def search():
    SearchMod.search_google(notepad)

# translate selection
def right_translate():
    Translate.rightTranslate(notepad)

# full note translate
def full_translate():
    Translate.fullTranslate(notepad)

# wikipedia
def wiki():
    ModuleFile.wiki(notepad)

# undo
def cmd_undo():
    notepad.edit_undo()

# redo
def cmd_redo():
    notepad.edit_redo()

def quick_translate_eng(e):
    Translate.quick_translate(notepad)

# text box for entry
notepad = Text(root, font=("Consolas", 12), height=48, foreground="white",
               insertbackground="light blue", borderwidth=0, undo=True)


notepad.focus_set()

notepad.bind('<Control-F>', findActivate)
notepad.bind('<Control-f>', findActivate)

notepad.bind('<Alt-T>', quick_translate_eng)
notepad.bind('<Alt-t>', quick_translate_eng)

textfinded.bind('<Escape>', notepadAct)


# opening configs
with open("synhig.txt", 'r+') as syn:
    synhigh = syn.readline()

with open("theme.txt", 'r+') as thm:
    themeget = thm.readline()

with open("auto_intend.txt", 'r+') as ain:
    autointendget = ain.readline()

with open("tabnumber.txt", 'r+') as tbn:
    tabnumberget = tbn.readline()


# auto indent func
def auto_indent(event):
    text_ai = event.widget

    # get leading whitespace from current line
    line = text_ai.get("insert linestart", "insert")
    match = re.match(r'^(\s+)', line)
    whitespace = match.group(0) if match else ""

    # insert the newline and the whitespace
    text_ai.insert("insert", f"\n{whitespace}")

    # return "break" to inhibit default insertion of newline
    return "break"

# changing number of tabs
def tab_pressed(event: Event) -> str:
    # Insert the 4 spaces
    notepad.insert("insert", " " * 4)
    # Prevent the default tkinter behaviour
    return "break"

# syntax highlighting
def syntax_highlighting():
    ModuleFile.syntaxHighlighting(notepad)

# triggering auto indent
def auto_intend():
    notepad.bind("<Return>", auto_indent)
    notepad.bind("<Tab>", tab_pressed)

if synhigh == "stx":
    syntax_highlighting()

def search_stack():
    SearchMod.search_stack(notepad)

notepad.tag_configure("tag_name", justify='center')

# scrollbar
scrollbar = CTkScrollbar(root, command=notepad.yview)
scrollbar.pack(side=RIGHT, fill=Y)
notepad.config(yscrollcommand=scrollbar.set, background="#1d1d1d")

notepad.focus_set()
notepad.pack(fill=BOTH, side=TOP, padx=3)

# always on top
def alwaysontop():
    root.attributes('-topmost', 1)

def bug_report():
    webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Notes/issues/new")

file_type = Label(bottomFrame, text="Text File", font=("ds-digital", 8), background="#1b1b1b", foreground="light blue")
file_type.pack(side=LEFT, padx=5)

# open note files
def noteopen():  # file menu Open option
    fd = (filedialog.askopenfile(parent=root, mode='r'))
    fd_str = str(fd)
    ext = os.path.splitext(fd_str)
    ext = ext[1]
    ext = ext[0] + ext[1] + ext[2]
    t = fd.read()  # t is the text read through filedialog

    if ext == ".tx":
        file_type.config(text="Text File")
    elif ext == ".py":
        file_type.config(text="Python File")
    elif ext == ".js":
        file_type.config(text="JSON File")
    elif ext == ".cs":
        file_type.config(text="CSV File")
    elif ext == ".sp":
        file_type.config(text="SPEC File")

    notepad.delete(0.0, END)
    notepad.insert(0.0, t)

# Calendar
def calendar():
    ModuleFile.calendar()

# find in notes
def find(e):
    ModuleFile.find(e, notepad, textfinded)

# calc math exp
def math_exp():
    ModuleFile.mathExpUp(notepad)

# right click menu
notepad_right_click_event = Menu(notepad, tearoff=0)
notepad_right_click_event.config(borderwidth=0, background='#2c2f33', foreground="light blue")

cmenubar = Menu(notepad_right_click_event, background='blue', fg='light blue')
web_tools = Menu(cmenubar, tearoff=False, background="#2c2f33", foreground="light blue")
numericals = Menu(cmenubar, tearoff=False, background="#2c2f33", foreground="light blue")
mail_tools = Menu(cmenubar, tearoff=False, background="#2c2f33", foreground="light blue")
highlight_text = Menu(cmenubar, tearoff=False, background="#2c2f33", foreground="light blue")
translate = Menu(cmenubar, tearoff=False, background="#2c2f33", foreground="light blue")
encode = Menu(cmenubar, tearoff=False, background="#2c2f33", foreground="light blue")
speak = Menu(cmenubar, tearoff=False, background="#2c2f33", foreground="light blue")


def search_github():
    SearchMod.search_github(notepad)

# highlighter
def highlight_note():
    ModuleFile.highlightText(notepad)


web_tools.add_command(label="Google", command=search)
web_tools.add_command(label="Wikipedia for article", command=wiki)
web_tools.add_command(label="Youtube                              Ctrl + Y", command=yt_search)
web_tools.add_command(label="StackOverflow", command=search_stack)
web_tools.add_command(label="GitHub", command=search_github)

encode.add_command(label="Encode Base64", command=encypt)
encode.add_command(label="Decode Base64", command=decode)

speak.add_command(label="Speak Selection", command=right_speak)
speak.add_command(label="Speak Full Note", command=full_speak)

translate.add_command(label="Selection", command=right_translate)
translate.add_command(label="Full Note", command=full_translate)


def clear_highlight():
    st_ind = notepad.index("sel.first")
    end_ind = notepad.index("sel.last")

    notepad.tag_remove("start", st_ind, end_ind)

highlight_text.add_command(label="Highlight", command=highlight_note)
highlight_text.add_command(label="Remove Highlight", command=clear_highlight)

# mail tools start #
def to_and_from():
    ModuleFile.to_and_from(notepad)

def add_footer():
    ModuleFile.add_footer(notepad)

def add_full_format():
    ModuleFile.add_full_format(notepad)
# mail tools end #

mail_tools.add_command(label="Add full mail format", command=add_full_format)
mail_tools.add_command(label="Add 'To' and 'From' formatting", command=to_and_from)
mail_tools.add_command(label="Add footer", command=add_footer)

numericals.add_command(label="Calculate Expression", command=math_exp)
numericals.add_command(label="Check EVEN or ODD", command=check_even_odd)
numericals.add_command(label="Check if PRIME", command=checkprime)

# paste
def cmdpaste():  # edit menu Paste option
    notepad.event_generate("<<Paste>>")

# select all
def cmdselectall():  # edit menu Select All option
    notepad.event_generate("<<SelectAll>>")

notepad_right_click_event.add_command(label="Copy                               Ctrl + C", command=cmdcopy)
notepad_right_click_event.add_command(label="Paste                               Ctrl + V", command=cmdpaste)
notepad_right_click_event.add_command(label="Select All                          Ctrl + A", command=cmdselectall)
notepad_right_click_event.add_command(label="Cut                                  Ctrl + X", command=cmdcut)

notepad_right_click_event.add_separator()

notepad.bind('<Control-s>', cmd_save_ss)
notepad.bind('<Control-b>', right_speak)
notepad.bind('<Control-m>', math_exp)
notepad.bind('<Control-d>', insert_date_up)
notepad.bind('<Control-y>', yt_search)
notepad.bind('<Control-S>', cmd_save_ss)
notepad.bind('<Control-B>', right_speak)
notepad.bind('<Control-M>', math_exp)
notepad.bind('<Control-D>', insert_date_up)
notepad.bind('<Control-Y>', yt_search)


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
    MsgBox = messagebox.askquestion('Not this fast! Consider saving the file?',
                                    'Do you want to save this document before leaving?',
                                    icon='warning')
    if MsgBox == 'yes':
        cmd_save_ss()
    else:
        root.destroy()

# Transparency Adjustments start #
def Transparent25():
    root.attributes('-alpha', 0.75)

def Transparent20():
    root.attributes('-alpha', 0.8)

def Transparent5():
    root.attributes('-alpha', 0.95)

def Transparent10():
    root.attributes('-alpha', 0.9)

def Transparent30():
    root.attributes('-alpha', 0.7)

def Transparent40():
    root.attributes('-alpha', 0.6)

# 50% Transparency
def Transparent50():
    root.attributes('-alpha', 0.5)

def Transparent60():
    root.attributes('-alpha', 0.4)

# 75% Transparency
def Transparent75():
    root.attributes('-alpha', 0.25)

# Reset transparency to default (0%)
def resetTransparent():
    root.attributes('-alpha', 1)
# Transparency Adjustments end #

def highContrastMode():
    ModuleFile.highContrastMode(notepad, topFrame, cmd_line)

def darkmode():
    ModuleFile.darkmode(notepad, topFrame, cmd_line)

def lightmode():
    ModuleFile.lightmode(notepad, topFrame, cmd_line)

# adjusting themes
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

textfinded.pack(pady=5)

mails.menu = Menu(mails, tearoff=0, background="#303030", foreground="cyan", borderwidth=0)
mails["menu"] = mails.menu

translate.menu = Menu(translate, tearoff=0, background="#303030", foreground="cyan", borderwidth=0)
translate["menu"] = translate.menu

mails.menu.add_command(label="Full Format", command=add_full_format)
mails.menu.add_command(label="To & From", command=to_and_from)
mails.menu.add_command(label="Footer", command=add_footer)
mails.menu.add_separator()

translate.menu.add_command(label="Translate Selection", command=right_translate)
translate.menu.add_command(label="Translate Full Note", command=full_translate)

menubar = Menu(root, background='blue', fg='light blue')

font1 = ['Arial', 13]

# zoom in and out
def zoomin(str1):
    if str1 == 'plus':
        font1[1] = font1[1] + 2
    else:
        font1[1] = font1[1] - 2

    notepad.config(font=font1)

line_label = Label(bottomFrame, text="1.0", background="#1b1b1b", foreground="light blue")
line_label.pack(side=RIGHT, padx=20)

def update_line_label(e):
    cindex = str(notepad.index(INSERT))
    line_label.config(text=cindex)

notepad.bind('<KeyPress>', update_line_label)
notepad.bind('<KeyRelease>', update_line_label)
notepad.bind('<Button-2>', update_line_label)


# Declare file and edit for showing in menubar
file = Menu(menubar, tearoff=False, background='#2c2f33', foreground="light blue")
edit = Menu(menubar, tearoff=False, background='#2c2f33', foreground="light blue")
window = Menu(menubar, tearoff=False, background='#2c2f33', foreground="light blue")
tools = Menu(menubar, tearoff=False, background="#2c2f33", foreground="light blue")
abb = Menu(menubar, tearoff=False, background="#2c2f33", foreground="light blue")
accessiblity = Menu(menubar, tearoff=False, background="#2c2f33", foreground="light blue")
view = Menu(menubar, tearoff=False, background="#2c2f33", foreground="light blue")
helptab = Menu(menubar, tearoff=False, background="#2c2f33", foreground="light blue")
transparency = Menu(window, tearoff=False, background="#2c2f33", foreground="light blue")

transparency.add_command(label="5%", command=Transparent5)
transparency.add_command(label="10%", command=Transparent10)
transparency.add_command(label="20%", command=Transparent20)
transparency.add_command(label="25%", command=Transparent25)
transparency.add_command(label="30%", command=Transparent30)
transparency.add_command(label="40%", command=Transparent40)
transparency.add_command(label="50%", command=Transparent50)
transparency.add_command(label="75%", command=Transparent75)
transparency.add_command(label="Reset", command=resetTransparent)

helptab.add_command(label="Command List", command=cmd_list)
helptab.add_command(label="Bug Report", command=bug_report)

def open_taskmgr():
    os.system("taskmgr")

ram_button = Button(bottomFrame, text="", background="#1b1b1b", activebackground="#1b1b1b", borderwidth=0, foreground="light blue", activeforeground="cyan", command=open_taskmgr)
ram_button.pack(side=RIGHT, padx=5)

def ram_get(e):
    ram_gb = (psutil.virtual_memory()[3] / 1000000000)
    ram_gb = str(ram_gb) + " GB"
    ram_button.config(text=ram_gb)

notepad.bind('<KeyPress>', ram_get)
notepad.bind('<KeyRelease>', ram_get)

# current version
def version():
    text_ver = "Current Version: " + "1.0.8" + "\n" + "\n" + "\n" + "What's New:" + "\n" + "\n" + "* Improved Color Science" + "\n" \
               + "* Line Numbers" + "\n" + "* New Icon" + "\n" + "* Quicker Translations" + "\n" + "* More Transparency Options" + "\n" + "* Improved overall Stability"
    messagebox.showinfo("Version Info", text_ver)

def find_replace():
    ModuleFile.find_replace(notepad)

def word_wrap():
    notepad.config(wrap=WORD)

file.add_command(label="New Document", command=cmd_new)
file.add_command(label="Open Document", command=noteopen)
file.add_command(label="Save Document", command=cmd_save_ss)
file.add_command(label="New Frame", command=new_frame)
file.add_command(label="Summary", command=summary)
file.add_command(label="Exit", command=cmdexit)

view.add_command(label="Zoom In", command=lambda: zoomin("plus"))
view.add_command(label="Zoom Out", command=lambda: zoomin("minus"))

edit.add_command(label="Copy", command=cmdcopy)
edit.add_command(label="Paste", command=cmdpaste)
edit.add_command(label="Cut", command=cmdcut)
edit.add_command(label="Select All", command=cmdselectall)
edit.add_command(label="Undo", command=cmd_undo)
edit.add_command(label="Redo", command=cmd_redo)
edit.add_command(label="Find & Replace", command=find_replace)

window.add_command(label="Minimize", command=minimize)
window.add_command(label="Maximize", command=maximize)
window.add_command(label="Resize", command=resize)
window.add_checkbutton(label="Always on Top", command=alwaysontop)
window.add_cascade(label="Transparency", menu=transparency)

tools.add_command(label="Calendar", command=calendar)
tools.add_cascade(label="Mail Tools", menu=mail_tools)

def about_github():
    webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Notes")

# Add commands in about menu
abb.add_command(label="Current Version", command=version)
abb.add_command(label="GitHub", command=about_github)

# settings page
def settings():
    ModuleFile.settings()

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

# main loop
root.mainloop()
