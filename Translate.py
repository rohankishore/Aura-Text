"""
This files enables Translate feature for Aura Notes. These functions were moved to a different .py file for reducing the size of
main app and to improve experience for contributors. As of now, this feature uses googletrans api.
Translation has two options: 1. To translate only selection and 2. To translate the entire note
"""

from tkinter import *
from tkinter import messagebox, ttk
from tkinter.ttk import Combobox
from googletrans import Translator

def rightTranslate(text_selection):
    v = text_selection.selection_get()
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
                        command=translateFull)
    button.place(x=150, y=280)

    clear = ttk.Button(tpage, text="Clear", cursor="hand2",
                       command=clear)
    clear.place(x=280, y=280)

    tpage.mainloop()

def fullTranslate(textwidget):
    v = textwidget.get(0.0, END)
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

    button = Button(tpage, text="Translate", relief=RIDGE, borderwidth=0, font=('verdana', 10, 'bold'),
                    cursor="hand2",
                    command=translateNow, background="#1b1b1b", foreground="white",
                    activebackground="#1b1b1b",
                    activeforeground="white")
    button.place(x=150, y=280)

    clear = Button(tpage, text="Clear", relief=RIDGE, borderwidth=0, font=('verdana', 10, 'bold',), cursor="hand2",
                   command=clear, background="#1b1b1b", foreground="white", activebackground="#1b1b1b",
                   activeforeground="white")
    clear.place(x=280, y=280)

    tpage.mainloop()

def rightTranslateEng(notepad):
    v = notepad.selection_get()
    language_1 = v
    cindex = notepad.index(INSERT)
    translator = Translator()
    output = translator.translate(language_1, dest='en')
    notepad.insert(cindex, output.text)