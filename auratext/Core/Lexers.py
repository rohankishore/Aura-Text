"""
his file includes lexer functions for all the languages supported by Aura Text. The lexer functionalities are implemented using QSciScintilla.
"""
import re

from PyQt6.Qsci import (
    QsciLexerCPP,
    QsciLexerVerilog,
    QsciLexerAVS,
    QsciLexerAsm,
    QsciLexerBash,
    QsciLexerBatch,
    QsciLexerJavaScript, QsciLexerCustom,
)
from PyQt6.Qsci import QsciLexerCSharp, QsciLexerFortran77, QsciLexerOctave, QsciLexerVHDL
from PyQt6.Qsci import (
    QsciLexerJava,
    QsciLexerJSON,
    QsciLexerYAML,
    QsciLexerHTML,
    QsciLexerRuby,
    QsciLexerCMake,
    QsciLexerCoffeeScript,
)
from PyQt6.Qsci import (
    QsciLexerPerl,
    QsciLexerCSS,
    QsciLexerLua,
    QsciLexerSQL,
    QsciLexerPascal,
    QsciLexerPostScript,
    QsciLexerTCL,
    QsciLexerSRec,
    QsciLexerSpice,
)
from PyQt6.Qsci import (
    QsciLexerTeX,
    QsciLexerPython,
    QsciLexerXML,
    QsciLexerMakefile,
    QsciLexerMarkdown,
    QsciLexerFortran,
)
from PyQt6.QtGui import QColor, QFont


class ColorCodeLexer(QsciLexerCustom):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColor(QColor("#000000"), 0)  # Default color
        self.setFont(QFont("Courier", 10))

    def language(self):
        return "ColorCode"

    def styleText(self, start, end):
        editor = self.editor()
        if not editor:
            return

        text = editor.text()[start:end]
        color_pattern = r'#[0-9a-fA-F]{6}\b'  # Regular expression to match hex color codes

        for match in re.finditer(color_pattern, text):
            start_index = match.start()
            end_index = match.end()
            self.startStyling(start + start_index, 0x11)  # Using style 17
            self.setStyling(end_index - start_index, 0)


def python(self):
    lexer = QsciLexerPython(self)
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self.editor_bg))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setColor(QColor("#FFFFFF"), lexer.ClassName)
    lexer.setColor(QColor("#59ff00"), lexer.TripleSingleQuotedString)
    lexer.setColor(QColor("#59ff00"), lexer.TripleDoubleQuotedString)
    lexer.setColor(QColor("#3ba800"), lexer.SingleQuotedString)
    lexer.setColor(QColor("#3ba800"), lexer.DoubleQuotedString)
    lexer.setFont(QFont(self._themes["font"]))


class PythonLexer(QsciLexerPython):
    def __init__(self, window: "Window"):
        super().__init__()
        self.setDefaultColor(QColor("white"))
        self.setPaper(QColor(window._themes["editor_theme"]))
        self.setColor(QColor("#ffffff"), self.ClassName)
        self.setFont(QFont(window._themes["font"]))

def csharp(self):
    lexer = QsciLexerCSharp()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def avs(self):
    lexer = QsciLexerAVS()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def asm(self):
    lexer = QsciLexerAsm()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setFont(QFont(self._themes["font"]))


def coffeescript(self):
    lexer = QsciLexerCoffeeScript()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def ma(self):
    lexer = QsciLexerCSharp()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def json(self):
    lexer = QsciLexerJSON()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def js(self):
    lexer = QsciLexerJavaScript()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setColor(QColor("#ffffff"), lexer.Default)
    lexer.setFont(QFont(self._themes["font"]))


def fortran(self):
    lexer = QsciLexerFortran()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def java(self):
    lexer = QsciLexerJava()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def bash(self):
    lexer = QsciLexerBash()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def yaml(self):
    lexer = QsciLexerYAML()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def xml(self):
    lexer = QsciLexerXML()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setFont(QFont(self._themes["font"]))


def html(self):
    lexer = QsciLexerHTML()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Tag)
    lexer.setFont(QFont(self._themes["font"]))


def cpp(self):
    lexer = QsciLexerCPP()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setColor(QColor("#ffffff"), lexer.Identifier)
    lexer.setFont(QFont(self._themes["font"]))


def srec(self):
    lexer = QsciLexerSRec()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setFont(QFont(self._themes["font"]))


def ruby(self):
    lexer = QsciLexerRuby()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setColor(QColor("#ffffff"), lexer.ClassName)
    lexer.setFont(QFont(self._themes["font"]))


def perl(self):
    lexer = QsciLexerPerl()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def css(self):
    lexer = QsciLexerCSS()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setFont(QFont(self._themes["font"]))


def lua(self):
    lexer = QsciLexerLua()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def sql(self):
    lexer = QsciLexerSQL()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def tex(self):
    lexer = QsciLexerTeX()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setFont(QFont(self._themes["font"]))


def bat(self):
    lexer = QsciLexerBatch()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def cmake(self):
    lexer = QsciLexerCMake()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setFont(QFont(self._themes["font"]))


def postscript(self):
    lexer = QsciLexerPostScript()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def markdown(self):
    lexer = QsciLexerMarkdown()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Header1)
    lexer.setColor(QColor("#FFA500"), lexer.Header2)
    lexer.setColor(QColor("#ffffff"), lexer.Header3)
    lexer.setFont(QFont(self._themes["font"]))


def makefile(self):
    lexer = QsciLexerMakefile()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setFont(QFont(self._themes["font"]))


def pascal(self):
    lexer = QsciLexerPascal()
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def tcl(self):
    lexer = QsciLexerTCL()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setFont(QFont(self._themes["font"]))


def verilog(self):
    lexer = QsciLexerVerilog()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor(self._themes["editor_theme"]), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def spice(self):
    lexer = QsciLexerSpice()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setFont(QFont(self._themes["font"]))


def vhdl(self):
    lexer = QsciLexerVHDL()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def octave(self):
    lexer = QsciLexerOctave()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))


def fortran77(self):
    lexer = QsciLexerFortran77()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._themes["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._themes["font"]))
