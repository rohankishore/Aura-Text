from tkinter import *
from tkinter import ttk, messagebox

with open("synhig.txt", 'r+') as syn:
    synhigh = syn.readline()

with open("theme.txt", 'r+') as thm:
    themeget = thm.readline()

with open("auto_intend.txt", 'r+') as ain:
    autointendget = ain.readline()

with open("tabnumber.txt", 'r+') as tbn:
    tabnumberget = tbn.readline()


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