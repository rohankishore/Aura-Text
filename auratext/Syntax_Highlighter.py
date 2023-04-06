from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QColor
from PySide6.QtGui import QFont
from PySide6.QtGui import QSyntaxHighlighter
from PySide6.QtGui import QTextCharFormat

py_words = [
    "from",
    "to",
    "get",
    "False",
    "None",
    "True",
    "and",
    "as",
    "assert",
    "async",
    "await",
    "break",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "except",
    "finally",
    "for",
    "from",
    "global",
    "if",
    "import",
    "in",
    "is",
    "lambda",
    "nonlocal",
    "not",
    "or",
    "pass",
    "raise",
    "return",
    "try",
    "while",
    "with",
    "yield",
    "print",
    "__name__ = '__main__'",
    "self",
    "__init__",
    "new",
    "nullptr",
    "operator",
    "return",
    "main()",
    "int",
]


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.highlight_rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#ffd466"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = py_words
        for word in keywords:
            pattern = QRegularExpression(rf"\b{word}\b")
            self.highlight_rules.append((pattern, keyword_format))

        quotation_format = QTextCharFormat()
        quotation_format.setForeground(QColor("#90ee90"))
        pattern = QRegularExpression(r"\".*\"|\'.*\'")
        self.highlight_rules.append((pattern, quotation_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#d2d2d2"))
        pattern = QRegularExpression(r"#.*")
        self.highlight_rules.append((pattern, comment_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlight_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
