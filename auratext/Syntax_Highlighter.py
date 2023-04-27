from PySide6.QtCore import *
from PySide6.QtGui import *


py_words = ["from", "to", "get", 'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
                 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if',
                 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
                 'while', 'with', 'yield', "print", "__name__ = '__main__'","self", "__init__",
            "new", "nullptr", "operator", "return", "main()", "int", "super"]

cpp_words = ['alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto', 'bitand', 'bitor', 'bool', 'break', 'case', 'catch', 'char',
             'char16_t', 'char32_t', 'class', 'compl', 'const', 'constexpr', 'const_cast', 'continue', 'decltype', 'default', 'delete',
             'do', 'double', 'dynamic_cast', 'else', 'enum', 'explicit', 'export', 'extern', 'false', 'float', 'for', 'friend', 'goto', 'if',
             'inline', 'int', 'long', 'mutable', 'namespace', 'new', 'noexcept', 'not', 'not_eq', 'nullptr', 'operator', 'or', 'or_eq',
             'private', 'protected', 'public', 'register', 'reinterpret_cast', 'return', 'short', 'signed', 'sizeof', 'static',
             'static_assert', 'static_cast', 'struct', 'switch', 'template', 'this', 'thread_local', 'throw', 'true', 'try', 'typedef',
             'typeid', 'typename', 'union', 'unsigned', 'using', 'virtual', 'void', 'volatile', 'wchar_t', 'while', 'xor', 'xor_eq']

js_words = ['abstract', 'arguments', 'await', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue', 'debugger',
            'default', 'delete', 'do', 'double', 'else', 'enum', 'eval', 'export', 'extends', 'false', 'final', 'finally', 'float', 'for',
            'function', 'goto', 'if', 'implements', 'import', 'in', 'instanceof', 'int', 'interface', 'let', 'long', 'native', 'new', 'null',
            'package', 'private', 'protected', 'public', 'return', 'short', 'static', 'super', 'switch', 'synchronized', 'this', 'throw',
            'throws', 'transient', 'true', 'try', 'typeof', 'var', 'void', 'volatile', 'while', 'with', 'yield']



class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, lexer, parent=None):
        super().__init__(parent)
        self.highlight_rules = []
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FFA500"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords_py = py_words

        keywords = []

        if lexer == "python":
            keywords = py_words
        elif lexer == "c++":
            keywords = cpp_words
        elif lexer == "javascript":
            keywords = js_words

        for word in keywords:
            pattern = QRegularExpression(r'\b{}\b'.format(word))
            self.highlight_rules.append((pattern, keyword_format))

        quotation_format = QTextCharFormat()
        quotation_format.setForeground(QColor("#00FF00"))
        pattern = QRegularExpression(r'\".*\"|\'.*\'')
        self.highlight_rules.append((pattern, quotation_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#d3d3d3"))
        pattern = QRegularExpression(r'#.*')
        self.highlight_rules.append((pattern, comment_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlight_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
