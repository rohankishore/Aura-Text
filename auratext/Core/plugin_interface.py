# plugin_interface.py
from PyQt6.QtWidgets import QMenu

class ContextMenuPluginInterface:
    def add_menu_items(self, context_menu: QMenu):
        pass

    def add_context_menu_items(self, context_menu: QMenu):
        pass

class MenuPluginInterface:
    def __init__(self, text_widget):
        super().__init__()

    section = ""

    def add_menu_items(self, context_menu: QMenu):
        pass

    def add_context_menu_items(self, context_menu: QMenu):
        pass

#############################################