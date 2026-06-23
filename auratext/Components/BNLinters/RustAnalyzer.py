from pathlib import Path
import subprocess
import os

from PyQt6.QtCore import QObject, QTimer

from ..NonBlockingIO import NonBlockingIO
from sansio_lsp_client import Client, Initialized, TextDocumentItem,VersionedTextDocumentIdentifier, TextDocumentContentChangeEvent

class LangServerNoExistError(Exception):
    pass

class RustAnalyzer(QObject):
    def __init__(self, parent=None, binaryPath=""):
        super().__init__(parent=parent)
        self.parent = parent
        

    def resolveFileURIFromPath(self, path):
        pathobj = Path(path).resolve()
        return pathobj.as_uri()