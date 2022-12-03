"""
This files contains functions for 'Search In' feature. All these files will only require webbroweser lib
"""

import webbrowser

def search_stack(notepad):
    cquery = notepad.selection_get()
    l = "https://stackoverflow.com/search?q=" + cquery + "&s=ddab4d49-a574-4a62-8794-24ac8a478c20"
    webbrowser.open_new_tab(l)

def search_github(notepad):
    gquery = notepad.selection_get()
    link = "https://github.com/search?q=" + gquery
    webbrowser.open_new_tab(link)

def yt_search(notepad):
    queryyt = notepad.selection_get()
    link = "https://www.youtube.com/results?search_query=" + queryyt
    webbrowser.open_new_tab(link)

def search_google(notepad):
    querysearch = notepad.selection_get()
    link = str(
        "https://www.google.com/search?q=" + querysearch + "&oq=hi&aqs=chrome..69i57j69i59j0i67l2j46i67j69i60j69i61l2.422j0j4&sourceid=chrome&ie=UTF-8")
    webbrowser.open_new_tab(link)