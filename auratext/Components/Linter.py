"""
Integrated Linter for Aura Text
Provides real-time error/warning indicators using pylint
"""
import os
import sys
import tempfile
import time
import hashlib
import atexit
import shutil
import getpass

from PyQt6.QtCore import QObject, pyqtSignal, QTimer, Qt, QThread
from PyQt6.QtGui import QColor
from PyQt6.Qsci import QsciScintilla, QsciScintillaBase

from pylint.lint import Run
from pylint.reporters import BaseReporter

from auratext.Misc.boilerplates import get_appdata_dirs
from auratext.Misc.import_res import notepadequalequalComponentImportPathAppend
sys.path.append(notepadequalequalComponentImportPathAppend)

local_app_data, script_dir = get_appdata_dirs()


class CollectingReporter(BaseReporter):
    """Collects pylint messages without outputting them"""
    def __init__(self):
        super().__init__()
        self.messages = []

    def handle_message(self, msg):
        self.messages.append(msg)

    def display_messages(self, layout):
        pass

    def _display(self, layout):
        pass


class Linter(QObject):
    """Pylint runner with persistent temp directory for an editor instance"""
    def __init__(self):
        super().__init__()
        self.sysTempDir = tempfile.gettempdir()
        dir_string = hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]
        user_string = getpass.getuser()
        self.tempdir = os.path.join(self.sysTempDir, f"pylint-run-{user_string}-{dir_string}")
        if not os.path.exists(self.tempdir):
            os.makedirs(self.tempdir)
        self._destroyed = False
        atexit.register(self.destroy)

    def destroy(self):
        if self._destroyed:
            return
        if os.path.exists(self.tempdir):
            try:
                shutil.rmtree(self.tempdir)
                print("Cleaned up code linter temp directory successfully.")
                self._destroyed = True
            except Exception as e:
                print(f"Error cleaning up temp directory: {e}")

    def __del__(self):
        self.destroy()

    def generate_timehash(self):
        return hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]

    def run(self, content):
        return self.run_pylint(content)

    def run_pylint(self, content):
        reporter = CollectingReporter()
        timehash = self.generate_timehash()
        filename = os.path.join(self.tempdir, f"{timehash}.py")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        try:
            Run([filename], reporter=reporter, exit=False)
        except Exception as e:
            print(f"Error running pylint: {e}")
            return []
        return reporter.messages


class LinterForEditor(QObject):
    """Attaches to a QsciScintilla editor and shows lint markers inline"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = parent
        if not isinstance(parent, QsciScintilla):
            raise TypeError("LinterForEditor must be attached to a QsciScintilla or CodeEditor")

        self.ERROR_MARKER = 0
        self.WARNING_MARKER = 1
        self.INFO_MARKER = 2
        self._setup_markers()

        self.lint_timer = QTimer(self)
        self.lint_timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.lint_timer.setSingleShot(True)
        self.lint_timer.timeout.connect(lambda: QTimer.singleShot(0, self.reanalyze))
        self.editor.textChanged.connect(self.live)

    def _setup_markers(self):
        # Error marker (red circle)
        self.editor.markerDefine(QsciScintilla.MarkerSymbol.Circle, self.ERROR_MARKER)
        self.editor.setMarkerBackgroundColor(QColor("#FF0000"), self.ERROR_MARKER)
        self.editor.setMarkerForegroundColor(QColor("#FFFFFF"), self.ERROR_MARKER)
        # Warning marker (orange circle)
        self.editor.markerDefine(QsciScintilla.MarkerSymbol.Circle, self.WARNING_MARKER)
        self.editor.setMarkerBackgroundColor(QColor("#FFA500"), self.WARNING_MARKER)
        self.editor.setMarkerForegroundColor(QColor("#000000"), self.WARNING_MARKER)
        # Info marker (blue triangle)
        self.editor.markerDefine(QsciScintilla.MarkerSymbol.RightTriangle, self.INFO_MARKER)
        self.editor.setMarkerBackgroundColor(QColor("#0080FF"), self.INFO_MARKER)
        self.editor.setMarkerForegroundColor(QColor("#FFFFFF"), self.INFO_MARKER)
        # Enable boxed annotations
        self.editor.setAnnotationDisplay(QsciScintilla.AnnotationDisplay.AnnotationBoxed)

    def display(self, messages):
        self.clearMarkers()
        for msg in messages:
            severity = msg.msg_id[0].upper()
            annotation = f"{msg.msg} ({msg.msg_id}:{msg.symbol})"
            line = msg.line - 1
            if severity == "E":
                self.editor.markerAdd(line, self.ERROR_MARKER)
            elif severity == "W":
                self.editor.markerAdd(line, self.WARNING_MARKER)
            else:
                self.editor.markerAdd(line, self.INFO_MARKER)
            self.editor.annotate(line, annotation, 0)

    def clearMarkers(self):
        self.editor.markerDeleteAll(self.ERROR_MARKER)
        self.editor.markerDeleteAll(self.WARNING_MARKER)
        self.editor.markerDeleteAll(self.INFO_MARKER)
        self.editor.SendScintilla(QsciScintillaBase.SCI_ANNOTATIONCLEARALL)

    class LintWorker(QObject):
        finished = pyqtSignal(list)

        def __init__(self, linter, text):
            super().__init__()
            self.linter = linter
            self.text = text

        def run(self):
            messages = self.linter.run(self.text)
            self.finished.emit(messages)

    def reanalyze(self):
        text = self.editor.text()
        self.thread = QThread()
        self.worker = self.LintWorker(self.editor.linter, text)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.display)
        self.worker.finished.connect(self.thread.quit)
        self.thread.start()

    def live(self):
        self.lint_timer.stop()
        self.lint_timer.start(500)

class LSPInEditor(QObject):
    """Attaches to a QsciScintilla editor and shows lint markers inline for LSP"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = parent
        if not isinstance(parent, QsciScintilla):
            raise TypeError("LSPInEditor must be attached to a QsciScintilla or CodeEditor")

        self.ERROR_MARKER = 0
        self.WARNING_MARKER = 1
        self.INFO_MARKER = 2
        self._setup_markers()

        self.lint_timer = QTimer(self)
        self.lint_timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.lint_timer.setSingleShot(True)
        self.lint_timer.timeout.connect(lambda: QTimer.singleShot(0, self.reanalyze))
        self.editor.textChanged.connect(self.live)

    def _setup_markers(self):
        # Error marker (red circle)
        self.editor.markerDefine(QsciScintilla.MarkerSymbol.Circle, self.ERROR_MARKER)
        self.editor.setMarkerBackgroundColor(QColor("#FF0000"), self.ERROR_MARKER)
        self.editor.setMarkerForegroundColor(QColor("#FFFFFF"), self.ERROR_MARKER)
        # Warning marker (orange circle)
        self.editor.markerDefine(QsciScintilla.MarkerSymbol.Circle, self.WARNING_MARKER)
        self.editor.setMarkerBackgroundColor(QColor("#FFA500"), self.WARNING_MARKER)
        self.editor.setMarkerForegroundColor(QColor("#000000"), self.WARNING_MARKER)
        # Info marker (blue triangle)
        self.editor.markerDefine(QsciScintilla.MarkerSymbol.RightTriangle, self.INFO_MARKER)
        self.editor.setMarkerBackgroundColor(QColor("#0080FF"), self.INFO_MARKER)
        self.editor.setMarkerForegroundColor(QColor("#FFFFFF"), self.INFO_MARKER)
        # Enable boxed annotations
        self.editor.setAnnotationDisplay(QsciScintilla.AnnotationDisplay.AnnotationBoxed)

    def display(self, messages):
        self.clearMarkers()
        for msg in messages:
            severity = msg.msg_id[0].upper()
            annotation = f"{msg.msg} ({msg.msg_id}:{msg.symbol})"
            line = msg.line - 1
            if severity == "E":
                self.editor.markerAdd(line, self.ERROR_MARKER)
            elif severity == "W":
                self.editor.markerAdd(line, self.WARNING_MARKER)
            else:
                self.editor.markerAdd(line, self.INFO_MARKER)
            self.editor.annotate(line, annotation, 0)

    def displayDiagnostics(self, diagnostics):
        self.clearMarkers()

        for d in diagnostics:
            line = d.range.start.line
            message = d.message

            severity = d.severity if hasattr(d, "severity") else 3

            if severity == 1:
                marker = self.ERROR_MARKER
            elif severity == 2:
                marker = self.WARNING_MARKER
            else:
                marker = self.INFO_MARKER

            self.editor.markerAdd(line, marker)
            self.editor.annotate(line, message, 0)

    def clearMarkers(self):
        self.editor.markerDeleteAll(self.ERROR_MARKER)
        self.editor.markerDeleteAll(self.WARNING_MARKER)
        self.editor.markerDeleteAll(self.INFO_MARKER)
        self.editor.SendScintilla(QsciScintillaBase.SCI_ANNOTATIONCLEARALL)

    def reanalyze(self):
        self.editor.linter.onFileChange()

    def live(self):
        self.lint_timer.stop()
        self.lint_timer.start(500)
