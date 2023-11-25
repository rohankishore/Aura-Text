from auratext import Plugin
from auratext.Core.window import Window, QPlainTextEdit
import sys


class LogsPlugin(Plugin):
    def __init__(self, window: Window) -> None:
        super().__init__(window)
        self.widget = QPlainTextEdit()

        sys.stdout.write = sys.stderr.write = self.log
        action = self.window.addAction("Show Logs")
        action.setShortcut("Alt+Shift+C")
        action.triggered.connect(
            lambda: self.widget.show() if self.widget.isHidden() else self.widget.hide()
        )

        print("hello")
        print("how")
        a = window.current_editor.text()
        print(a)

    def log(self, msg: str):
        self.widget.setPlainText(f"{self.widget.toPlainText()}{msg}")

