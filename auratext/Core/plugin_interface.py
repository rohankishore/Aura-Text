# plugin_interface.py
from __future__ import annotations
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMenu
from PyQt6.QtCore import QObject

if TYPE_CHECKING:
    from .window import Window


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


class Plugin(QObject):
    def __init__(self, window: Window) -> None:
        super().__init__(window)
        self.window = window


#############################################
