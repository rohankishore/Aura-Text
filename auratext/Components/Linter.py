"""
Integrated Linter for Aura Text
Provides real-time error/warning indicators using pylint and flake8
"""
import os
import sys
import subprocess
import threading
import platform
import tempfile
import time
import hashlib
import atexit
import shutil
import getpass
from typing import List, Dict, Tuple, Optional

from PyQt6.QtCore import QObject, pyqtSignal, QTimer, Qt, QThread
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QPushButton, QMessageBox
from PyQt6.Qsci import QsciScintilla, QsciScintillaBase

from io import StringIO
from pylint.lint import Run
from pylint.reporters import BaseReporter
from pylint.reporters.json_reporter import JSONReporter
import json

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
class LintMessage:
    """Represents a single lint message"""
    def __init__(self, line: int, column: int, severity: str, message: str, linter: str, code: str = ""):
        self.line = line
        self.column = column
        self.severity = severity  # 'error', 'warning', 'info', 'convention'
        self.message = message
        self.linter = linter
        self.code = code

    def __repr__(self):
        return f"LintMessage(line={self.line}, severity={self.severity}, message={self.message})"


class LinterWorker(QObject):
    """Background worker for running linters"""
    finished = pyqtSignal(list)  # Emits list of LintMessage
    
    def __init__(self, file_path: str, content: str, linters: List[str]):
        super().__init__()
        self.file_path = file_path
        self.content = content
        self.linters = linters
        self.temp_file = None

    def run(self):
        """Run linters and collect messages"""
        messages = []
        
        # Create temporary file for linting
        import tempfile
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tf:
                self.temp_file = tf.name
                tf.write(self.content)
            
            for linter in self.linters:
                # if linter == 'pylint':
                #     messages.extend(self._run_pylint())
                # elif linter == 'flake8':
                #     messages.extend(self._run_flake8())
                # elif linter == 'pyflakes':
                #     messages.extend(self._run_pyflakes())
                messages.extend(self._run_pylint())
            
        except Exception as e:
            print(f"Linter error: {e}")
        finally:
            # Clean up temp file
            if self.temp_file and os.path.exists(self.temp_file):
                try:
                    os.unlink(self.temp_file)
                except:
                    pass
        
        self.finished.emit(messages)

    def _run_pylint(self) -> List[LintMessage]:
        messages = []
    
        try:
            output = StringIO()
            reporter = JSONReporter(output)
    
            Run(
                [self.temp_file],
                reporter=reporter
            )

            data = json.loads(output.getvalue())

            for item in data:
                severity = self._map_pylint_severity(item.get('type', 'info'))

                messages.append(LintMessage(
                    line=item.get('line', 0),
                    column=item.get('column', 0),
                    severity=severity,
                    message=item.get('message', ''),
                    linter='pylint',
                    code=item.get('message-id', '')
                ))
    
        except Exception as e:
            print(f"Pylint error: {e}")
        print(f"Pylint messages: {messages}")
        return messages

    def _run_flake8(self) -> List[LintMessage]:
        """Run flake8 and parse output"""
        messages = []
        if platform.system() == "Windows":
            print("WARNING: Windows does not like Python's forking, so we cannot run subprocesses like flake8 here.")
            return messages
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'flake8', '--format=%(row)d:%(col)d:%(code)s:%(text)s', self.temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                try:
                    parts = line.split(':', 3)
                    if len(parts) == 4:
                        row, col, code, text = parts
                        severity = self._map_flake8_severity(code)
                        messages.append(LintMessage(
                            line=int(row),
                            column=int(col),
                            severity=severity,
                            message=text.strip(),
                            linter='flake8',
                            code=code
                        ))
                except ValueError:
                    continue
        except subprocess.TimeoutExpired:
            print("Flake8 timed out")
        except FileNotFoundError:
            pass  # Flake8 not installed
        except Exception as e:
            print(f"Flake8 error: {e}")
        
        return messages

    def _run_pyflakes(self) -> List[LintMessage]:
        """Run pyflakes and parse output"""
        messages = []
        if platform.system() == "Windows":
            print("WARNING: Windows does not like Python's forking, so we cannot run subprocesses like pyflakes here.")
            return messages
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pyflakes', self.temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                try:
                    # Format: filename:line:col: message
                    if ':' in line:
                        parts = line.split(':', 3)
                        if len(parts) >= 3:
                            line_num = int(parts[1])
                            message = parts[-1].strip()
                            messages.append(LintMessage(
                                line=line_num,
                                column=0,
                                severity='warning',
                                message=message,
                                linter='pyflakes',
                                code=''
                            ))
                except (ValueError, IndexError):
                    continue
        except subprocess.TimeoutExpired:
            print("Pyflakes timed out")
        except FileNotFoundError:
            pass  # Pyflakes not installed
        except Exception as e:
            print(f"Pyflakes error: {e}")
        
        return messages

    @staticmethod
    def _map_pylint_severity(pylint_type: str) -> str:
        """Map pylint message types to severity levels"""
        mapping = {
            'error': 'error',
            'warning': 'warning',
            'convention': 'info',
            'refactor': 'info',
            'info': 'info'
        }
        return mapping.get(pylint_type.lower(), 'info')

    @staticmethod
    def _map_flake8_severity(code: str) -> str:
        """Map flake8 error codes to severity levels"""
        if code.startswith('E9') or code.startswith('F'):
            return 'error'
        elif code.startswith('E') or code.startswith('W'):
            return 'warning'
        else:
            return 'info'


class CodeLinter(QObject):
    """Main linter class for integrating with the editor"""
    lint_complete = pyqtSignal(list)
    
    # Marker symbols for different severity levels
    ERROR_MARKER = 0
    WARNING_MARKER = 1
    INFO_MARKER = 2
    
    def __init__(self, editor: QsciScintilla, file_path: str = "", enabled_linters: Optional[List[str]] = None):
        super().__init__()
        self.editor = editor
        self.file_path = file_path or "untitled.py"
        self.enabled_linters = enabled_linters or ['flake8']  # Default to flake8
        self.messages: List[LintMessage] = []
        self.lint_timer = QTimer()
        self.lint_timer.setSingleShot(True)
        self.lint_timer.timeout.connect(self.run_lint)
        self.is_linting = False
        
        # Configure markers
        self._setup_markers()
        
        # Connect editor signals
        self.editor.textChanged.connect(self.on_text_changed)
        
    def _setup_markers(self):
        """Setup visual markers for errors and warnings"""
        # Error marker (red circle with X)
        self.editor.markerDefine(QsciScintilla.MarkerSymbol.Circle, self.ERROR_MARKER)
        self.editor.setMarkerBackgroundColor(QColor("#FF0000"), self.ERROR_MARKER)
        self.editor.setMarkerForegroundColor(QColor("#FFFFFF"), self.ERROR_MARKER)
        
        # Warning marker (yellow triangle)
        self.editor.markerDefine(QsciScintilla.MarkerSymbol.RightTriangle, self.WARNING_MARKER)
        self.editor.setMarkerBackgroundColor(QColor("#FFA500"), self.WARNING_MARKER)
        self.editor.setMarkerForegroundColor(QColor("#000000"), self.WARNING_MARKER)
        
        # Info marker (blue circle)
        self.editor.markerDefine(QsciScintilla.MarkerSymbol.Circle, self.INFO_MARKER)
        self.editor.setMarkerBackgroundColor(QColor("#0080FF"), self.INFO_MARKER)
        self.editor.setMarkerForegroundColor(QColor("#FFFFFF"), self.INFO_MARKER)
        
        # Enable annotations
        self.editor.setAnnotationDisplay(QsciScintilla.AnnotationDisplay.AnnotationBoxed)
    
    def on_text_changed(self):
        """Handle text changes with debouncing"""
        # Restart timer on each change (debounce)
        self.lint_timer.stop()
        self.lint_timer.start(1500)  # Run lint 1.5 seconds after last change
    
    def run_lint(self):
        """Run linting in background thread"""
        if self.is_linting:
            return
        
        # Only lint Python files
        if not self.file_path.endswith('.py'):
            return
        
        self.is_linting = True
        content = self.editor.text()
        
        # Clear previous markers
        self.clear_markers()
        
        # Run linter in thread
        worker = LinterWorker(self.file_path, content, self.enabled_linters)
        worker.finished.connect(self.on_lint_finished)
        
        # Use thread to avoid blocking
        thread = threading.Thread(target=worker.run)
        thread.daemon = True
        thread.start()
    
    def on_lint_finished(self, messages: List[LintMessage]):
        """Handle lint results"""
        self.is_linting = False
        self.messages = messages
        self.display_messages()
        self.lint_complete.emit(messages)
    
    def display_messages(self):
        """Display lint messages in the editor"""
        # Clear old markers and annotations
        self.clear_markers()
        
        # Group messages by line
        lines_with_messages: Dict[int, List[LintMessage]] = {}
        for msg in self.messages:
            line = msg.line - 1  # Convert to 0-based
            if line not in lines_with_messages:
                lines_with_messages[line] = []
            lines_with_messages[line].append(msg)
        
        # Add markers and annotations
        for line, msgs in lines_with_messages.items():
            # Determine highest severity
            has_error = any(m.severity == 'error' for m in msgs)
            has_warning = any(m.severity == 'warning' for m in msgs)
            
            # Add marker
            if has_error:
                self.editor.markerAdd(line, self.ERROR_MARKER)
            elif has_warning:
                self.editor.markerAdd(line, self.WARNING_MARKER)
            else:
                self.editor.markerAdd(line, self.INFO_MARKER)
            
            # Add annotation with all messages for this line
            annotation = '\n'.join([f"[{m.linter}] {m.message}" for m in msgs])
            self.editor.annotate(line, annotation, 0)
    
    def clear_markers(self):
        """Clear all markers and annotations"""
        self.editor.markerDeleteAll(self.ERROR_MARKER)
        self.editor.markerDeleteAll(self.WARNING_MARKER)
        self.editor.markerDeleteAll(self.INFO_MARKER)
        self.editor.clearAnnotations()
    
    def set_enabled_linters(self, linters: List[str]):
        """Update enabled linters and re-run"""
        self.enabled_linters = linters
        self.run_lint()
    
    def get_messages_for_line(self, line: int) -> List[LintMessage]:
        """Get all messages for a specific line"""
        return [m for m in self.messages if m.line == line + 1]  # Convert to 1-based
