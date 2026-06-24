from pathlib import Path
import subprocess
import os

from PyQt6.QtCore import QObject, QTimer, Qt, pyqtSignal

from ..NonBlockingIO import NonBlockingIO
from sansio_lsp_client import Client, Initialized, TextDocumentItem, VersionedTextDocumentIdentifier, TextDocumentContentChangeEvent, PublishDiagnostics, ShowMessage, LogMessage

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
        self.rootpath = self._resolveRootPath(file_path)
        self.file_path = file_path
        self.rootURI = self.resolveFileURIFromPath(self.rootpath)
        self.fileURI = self.resolveFileURIFromPath(self.file_path)
        self.process = subprocess.Popen(
            [binaryPath],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=self.rootpath if os.path.isdir(self.rootpath) else None,
        )
        self.io = NonBlockingIO(self.process)
        self.lsp = Client(trace="verbose", root_uri=self.rootURI)
        self.io.write(self.lsp.send())
        self.initialized = False
        self.opened = False
        self.pending_change = False
        self.version = 1
        self.lint_timer = QTimer(self)
        self.lint_timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.lint_timer.setSingleShot(True)
        self.lint_timer.timeout.connect(self.flushPendingChange)
        if hasattr(self.parent, "textChanged"):
            self.parent.textChanged.connect(self.live)

        QTimer.singleShot(0, self.IOPump)

    def _resolveRootPath(self, file_path):
        if file_path:
            candidate = Path(file_path).resolve()
            search_dir = candidate.parent if candidate.is_file() else candidate
            for directory in (search_dir, *search_dir.parents):
                if (directory / "Cargo.toml").exists():
                    return str(directory)
            return str(search_dir)

        window_root = getattr(getattr(self.parent, "parent", None), "cpath", "")
        if window_root:
            return window_root
        return os.getcwd()

    def resolveFileURIFromPath(self, path):
        pathobj = Path(path).resolve()
        return pathobj.as_uri()

    def handle_event(self, event):
        if isinstance(event, PublishDiagnostics):
            self.diagnosticsReceived.emit(event.diagnostics)
            if hasattr(self.parent, "lsp_in_editor"):
                self.parent.lsp_in_editor.displayDiagnostics(event.diagnostics)
        elif isinstance(event, (ShowMessage, LogMessage)):
            print(f"Rust Analyzer: {event.message}")

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
        self.opened = True
        if self.pending_change:
            QTimer.singleShot(0, self.flushPendingChange)

    def onFileChange(self):
        if not self.initialized or not self.opened:
            self.pending_change = True
            return
        if self.process.poll() is not None:
            return

        text = self.parent.text()
        self.version += 1
        self.lsp.did_change(
            text_document=VersionedTextDocumentIdentifier(
                uri=self.fileURI,
                version=self.version
            ),
            content_changes=[
                TextDocumentContentChangeEvent(
                    text=text,
                    range=None,
                    rangeLength=None,
                )
            ]
        )
        self.io.write(self.lsp.send())

    def live(self):
        self.pending_change = True
        self.lint_timer.stop()
        self.lint_timer.start(500)

    def flushPendingChange(self):
        if not self.pending_change:
            return
        self.pending_change = False
        self.onFileChange()

    def IOPump(self):
        outgoing = self.lsp.send()
        if outgoing:
            self.io.write(outgoing)

        incoming = self.io.read()
        if incoming:
            try:
                for event in self.lsp.recv(incoming):
                    if isinstance(event, Initialized):
                        self.initialized = True
                        self.onFileOpen()
                    self.handle_event(event)
            except Exception as e:
                print(f"ERROR: Rust Analyzer LSP error: {e}")
        elif incoming == b"":
            print(f"ERROR: Rust Analyzer exited early with code {self.process.poll()}")
            return
        if self.process.poll() is not None:
            returncode = self.process.returncode
            hex_code = f"0x{returncode & 0xFFFFFFFF:08X}" if returncode is not None else "unknown"
            print(f"ERROR: Rust Analyzer process died with code {returncode} ({hex_code})")
            return

        QTimer.singleShot(20, self.IOPump)
