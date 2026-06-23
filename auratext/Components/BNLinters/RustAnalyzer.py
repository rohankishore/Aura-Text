from pathlib import Path
import subprocess
import os

from .. import NonBlockingIO
from sansio_lsp_client import Client

class RustAnalyzer(QObject):
    def __init__(self, parent=None, binaryPath=""):
        super().__init__(parent=parent)
        self.parent = parent
        

    def resolveFileURIFromPath(self, path):
        pathobj = Path(path).resolve()
        return pathobj.as_uri()