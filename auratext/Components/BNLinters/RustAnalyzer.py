from pathlib import Path
import subprocess
import os

from PyQt6.QtCore import QObject, QTimer, pyqtSignal

from ..NonBlockingIO import NonBlockingIO
from sansio_lsp_client import Client, Initialized, TextDocumentItem,VersionedTextDocumentIdentifier, TextDocumentContentChangeEvent, PublishDiagnostics

class LangServerNoExistError(Exception):
    pass

class RustAnalyzer(QObject):
    diagnosticsReceived = pyqtSignal(list)
    def __init__(self, parent=None, binaryPath="", file_path=""):
        super().__init__(parent=parent)
        self.parent = parent
        if not binaryPath:
            raise LangServerNoExistError("Language server path cannot be empty")
        if not os.path.exists(binaryPath):
            raise LangServerNoExistError(f"Language server does not exist at {binaryPath}")
        self.rootpath = self.parent.parent.cpath
        self.file_path = file_path
        self.rootURI = self.resolveFileURIFromPath(self.rootpath)
        self.fileURI = self.resolveFileURIFromPath(self.file_path)
        self.process = subprocess.Popen(
            [binaryPath],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        self.io = NonBlockingIO(self.process)
        self.lsp = Client(trace="verbose", root_uri=self.rootURI)
        self.io.write(self.lsp.send())
        self.initialized = False
        self.version = 1

        QTimer.singleShot(0, self.IOPump)

    def resolveFileURIFromPath(self, path):
        pathobj = Path(path).resolve()
        return pathobj.as_uri()

    def handle_event(self, event):
        if isinstance(event, PublishDiagnostics):
            self.diagnosticsReceived.emit(event.diagnostics)
            self.parent.lsp_in_editor.display(event.diagnostics)

    def onFileOpen(self):
        text = self.parent.text()
        self.lsp.did_open(
            TextDocumentItem(
                uri=self.fileURI,
                languageId="rust",
                version=self.version,
                text=text
            )
        )
        self.io.write(self.lsp.send())

    def onFileChange(self):
        text = self.parent.text()
        self.version += 1
        self.lsp.did_change(
            text_document=VersionedTextDocumentIdentifier(
                uri=self.fileURI,
                version=self.version
            ),
            content_changes=[
                TextDocumentContentChangeEvent(
                    text=text
                )
            ]
        )
        self.io.write(self.lsp.send())

    def IOPump(self):
        outgoing = self.lsp.send()
        if outgoing:
            self.io.write(outgoing)

        incoming = self.io.read()
        if incoming:
            for event in self.lsp.recv(incoming):
                if isinstance(event, Initialized):
                    # self.lsp.is_initialized()
                    # self.io.write(self.lsp.send())
                    self.initialized = True
                    self.onFileOpen()
                self.handle_event(event)
        elif incoming == b"":
            print("ERROR: Rust Analyzer exited early")
            return
        if self.process.poll() is not None:
            print("Process died")
            return

        QTimer.singleShot(20, self.IOPump)