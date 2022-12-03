"""
Main file for Aura Notes. Run this file to experience what a TRUE Notepad feels lile.

Functions for the features are split into different files for better readablity for devs. This includes:
- Translator
- Wikipedia
- Hiighlight feature
- Find in Notes
- Search tools
And much more
"""

# system libs
import base64
import re
import webbrowser
from datetime import date
from random import choice

# Tkinter
from tkinter import *
from tkinter import messagebox, filedialog, colorchooser
from tkinter import ttk
import tkinter

# Image Processing
import PIL.Image
from PIL import ImageTk


# Extra Files
import ModuleFile
import Translate
import SearchMod

# main gui window for editor
root = Tk()
root.tk_setPalette('SystemButtonFace')
root.title("Aura Notes")

# Function for 'resize_button'
def resize():
    ModuleFile.resize(root)

# icon files
cmdlist_icon = ImageTk.PhotoImage(PIL.Image.open('cmdlist.png').resize((1170, 950)))

# setting theme (light/dark)
root.tk.call("source", "theme.tcl")

root.tk.call("set_theme", "dark")
# making the window resizable and adjusting its size
root.resizable(True, True)

# Making the window maximized always
root.state('zoomed')

# Declaring the icon file
root.iconbitmap("notepad.ico")

# top frame to accompany menu bar and stuff
topFrame = tkinter.Frame(root, height=50)

# bottom frame for line numbers, cmd, etc
bottomFrame = tkinter.Frame(root, background="#1b1b1b", height=20)

#packing both
bottomFrame.pack(side=BOTTOM, fill=X)
topFrame.pack(side=TOP, fill=X)

# Find in Notes Entry
textfinded = ttk.Entry(topFrame, width=25, foreground="light blue", font=("Arial", 13))

# cmd
cmd_line = Entry(bottomFrame, width=30, foreground="sky blue", borderwidth=0, background="black")
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
            minibuffer.insert(0.0, "It's HEAD")
        else:
            minibuffer.insert(0.0, "It's TAIL")

    def dice_roll():
        choices = [1, 2, 3, 4, 5, 6]
        aa = choice(choices)
        aa = str(aa)
        minibuffer.insert(0.0, aa)

    def stackcmd():
        s = str(cmdget.replace("stack", ""))
        l = "https://stackoverflow.com/search?q=" + s + "&s=ddab4d49-a574-4a62-8794-24ac8a478c20"
        webbrowser.open_new_tab(l)

    def githubcmd():
        s = str(cmdget.replace("git", ""))
        link = "https://github.com/search?q=" + s
        webbrowser.open_new_tab(link)

    cmdget = cmd_line.get()

    def ntp_changr_bg():
        s = str(cmdget.replace("npbg ", ""))
        notepad.config(background=s)
        minibuffer.insert(0.0, "Bg has been changed to: " + s)

    def ntp_changr_fg():
        s = str(cmdget.replace("npfg ", ""))
        notepad.config(foreground=s)
        minibuffer.insert(0.0, "Fg has been changed to: " + s)

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
        minibuffer.insert(0.0, "Syntax Highlighting ON")
    elif "yt" in cmdget:
        ytcmd()
    elif "stack" in cmdget:
        stackcmd()
    elif "git" in cmdget:
        githubcmd()
    elif "cal" in cmdget:
        calendar()
        minibuffer.insert(0.0, "Calendar Opened")
    elif "aot" in cmdget:
        alwaysontop()
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
        coin_flip()
    elif "droll" in cmdget:
        dice_roll()
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
        syntax_highlighting()
        minibuffer.insert(0.0, "Coding Mode Turned ON")
    elif "min" in cmdget:
        minimize()
    elif "max" in cmdget:
        maximize()
        minibuffer.insert(0.0, "Window Maximized")
    else:
        messagebox.showerror("Error!", "Command Error!")

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

def SummaryBttn():
    ModuleFile.Summary(notepad)

# label for line numbers
lineLabel = Button(bottomFrame, text="1.0", justify=CENTER, foreground="light blue",
                  font=("Helvetica", 10), borderwidth=0, background="#1b1b1b",
                   activebackground="#1b1b1b", activeforeground="light blue", command=SummaryBttn)
lineLabel.pack(side=LEFT, padx=6)

# updating the line numbers
def line_update(e):
    cindex = str(notepad.index(INSERT))
    lineLabel.config(text=cindex)

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
    tt = Toplevel()
    tt.geometry("1397x1080")
    tt.state('zoomed')
    tt.config(background="#f8f3f3")
    img_label = Label(tt, image=cmdlist_icon, background="#f8f3f3")
    img_label.image = cmdlist_icon
    img_label.pack()
    tt.mainloop()

# new file
def cmd_new():  # file menu New option
    global fileName
    if len(notepad.get('1.0', END + '-1c')) > 0:
        if messagebox.askyesno("Notepad", "Do you want to save changes?"):
            cmd_save_ss()
            minibuffer.insert(0.0, "New file has been created!")
        else:
            notepad.delete(0.0, END)
            minibuffer.insert(0.0, "New file has been created!")

# inserting the current date
def insert_date_up():
    cdate = str(date.today())
    notepad.insert(1.0, cdate)

# to see all the ongoing processes
minibuffer = Text(bottomFrame, background="#1b1b1b", foreground="sky blue", height=1, borderwidth=0, width=30)
minibuffer.pack(side=RIGHT, padx=2)

# save file
def cmd_save_ss():  # file menu Save As option
    fd = filedialog.asksaveasfile(mode='w', defaultextension='.txt', initialfile="textfile")
    t = notepad.get(0.0, END)  # t stands for the text gotten from notepad
    try:
        fd.write(t.rstrip())
        minibuffer.insert(0.0, "File Saved Successfully!")
    except ValueError:
        messagebox.showinfo(title="Error", message="Not able to save file!")

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
    Translate.rightTranslateEng(notepad)

# text box for entry
notepad = Text(root, font=("Consolas", 13), height=48, foreground="white",
               insertbackground="light blue", borderwidth=0, undo=True)

notepad.bind('<KeyPress>', line_update)
notepad.bind('<KeyRelease>', line_update)

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
    tabnumber = int(tabnumberget)
    # Insert the 4 spaces
    notepad.insert("insert", " " * tabnumber)
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
scrollbar = ttk.Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
notepad.config(yscrollcommand=scrollbar.set, background="#151718")
scrollbar.config(command=notepad.yview, )

notepad.focus_set()

notepad.pack(fill=BOTH, side=TOP)

# always on top
def alwaysontop():
    root.attributes('-topmost', 1)
    minibuffer.insert(0.0, "Always On Top Enabled")

def bug_report():
    webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Notes/issues/new")

# open note files
def noteopen():  # file menu Open option
    fd = filedialog.askopenfile(parent=root, mode='r')
    t = fd.read()  # t is the text read through filedialog
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

translate.add_command(label="Translate Selection", command=right_translate)
translate.add_command(label="Translate Full Note", command=full_translate)


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

def font_color():
    color_chooser = colorchooser.askcolor(title="Choose color")
    rgb, hexx = color_chooser
    st_ind = notepad.index("sel.first")
    end_ind = notepad.index("sel.last")

    notepad.tag_add("start", st_ind, end_ind)
    notepad.tag_config("start", foreground=hexx)


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
        cmd_save_ss()
    else:
        root.destroy()

# Transparency Adjustments start #
def Transparent25():
    root.attributes('-alpha', 0.75)

def Transparent20():
    root.attributes('-alpha', 0.75)

def Transparent30():
    root.attributes('-alpha', 0.75)

def Transparent40():
    root.attributes('-alpha', 0.75)

# 50% Transparency
def Transparent50():
    root.attributes('-alpha', 0.5)

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

textfinded.pack()

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

transparency.add_command(label="20%", command=Transparent20)
transparency.add_command(label="25%", command=Transparent25)
transparency.add_command(label="30%", command=Transparent30)
transparency.add_command(label="50%", command=Transparent50)
transparency.add_command(label="75%", command=Transparent75)
transparency.add_command(label="Reset", command=resetTransparent)

helptab.add_command(label="Command List", command=cmd_list)

# current version
def version():
    text_ver = "Current Version: " + "1.0.7" + "\n" + "\n" + "\n" + "What's New:" + "\n" + "\n" + "* Improved Color Science" + "\n" \
               + "* Complete Visual Overhaul with simpler look" + "\n" + "* New Formatting Features such as Bold, Italic, etc" + "\n" + "* Quicker translations" + "\n" + "* More organised menus" + "\n" + "* Improved overall Stability"

    messagebox.showinfo("Version Info", text_ver)

file.add_command(label="New Document", command=cmd_new)
file.add_command(label="Open Document", command=noteopen)
file.add_command(label="Save Document", command=cmd_save_ss)
file.add_command(label="Exit", command=cmdexit)

view.add_command(label="Zoom In", command=lambda: zoomin("plus"))
view.add_command(label="Zoom Out", command=lambda: zoomin("minus"))

edit.add_command(label="Copy", command=cmdcopy)
edit.add_command(label="Paste", command=cmdpaste)
edit.add_command(label="Cut", command=cmdcut)
edit.add_command(label="Select All", command=cmdselectall)
edit.add_command(label="Undo", command=cmd_undo)
edit.add_command(label="Redo", command=cmd_redo)

window.add_command(label="Minimize", command=minimize)
window.add_command(label="Maximize", command=maximize)
window.add_command(label="Resize", command=resize)
window.add_checkbutton(label="Always on Top", command=alwaysontop)
window.add_cascade(label="Window Transparency", menu=transparency)

tools.add_command(label="Calendar", command=calendar)
tools.add_cascade(label="Mail Tools", menu=mail_tools)

def minibuffer_clear(e):
    def delete():
        minibuffer.delete(0.0, END)

    root.after(4500, delete)

root.bind('<KeyRelease>', minibuffer_clear)
root.bind('<FocusIn>', minibuffer_clear)
root.bind('<MouseWheel>', minibuffer_clear)

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
