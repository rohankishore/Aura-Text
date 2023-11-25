from PyQt6.Qsci import (
    QsciLexerCPP,
    QsciLexerVerilog,
    QsciLexerAVS,
    QsciLexerAsm,
    QsciLexerBash,
    QsciLexerBatch,
    QsciLexerJavaScript,
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
    lexer.setFont(QFont(self._config["font"]))


class PythonLexer(QsciLexerPython):
    def __init__(self, window: "Window"):
        super().__init__()
        self.setDefaultColor(QColor("white"))
        self.setPaper(QColor(window._config["editor_theme"]))
        self.setColor(QColor("#ffffff"), self.ClassName)
        self.setFont(QFont(window._config["font"]))


def csharp(self):
    lexer = QsciLexerCSharp()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def avs(self):
    lexer = QsciLexerAVS()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def asm(self):
    lexer = QsciLexerAsm()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setFont(QFont(self._config["font"]))


def coffeescript(self):
    lexer = QsciLexerCoffeeScript()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def ma(self):
    lexer = QsciLexerCSharp()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def json(self):
    lexer = QsciLexerJSON()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def js(self):
    lexer = QsciLexerJavaScript()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setColor(QColor("#ffffff"), lexer.Default)
    lexer.setFont(QFont(self._config["font"]))


def fortran(self):
    lexer = QsciLexerFortran()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def java(self):
    lexer = QsciLexerJava()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def bash(self):
    lexer = QsciLexerBash()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def yaml(self):
    lexer = QsciLexerYAML()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def xml(self):
    lexer = QsciLexerXML()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setFont(QFont(self._config["font"]))


def html(self):
    lexer = QsciLexerHTML()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Tag)
    lexer.setFont(QFont(self._config["font"]))


def cpp(self):
    lexer = QsciLexerCPP()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setColor(QColor("#ffffff"), lexer.Identifier)
    lexer.setFont(QFont(self._config["font"]))


def srec(self):
    lexer = QsciLexerSRec()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setFont(QFont(self._config["font"]))


def ruby(self):
    lexer = QsciLexerRuby()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setColor(QColor("#ffffff"), lexer.ClassName)
    lexer.setFont(QFont(self._config["font"]))


def perl(self):
    lexer = QsciLexerPerl()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def css(self):
    lexer = QsciLexerCSS()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setFont(QFont(self._config["font"]))


def lua(self):
    lexer = QsciLexerLua()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def sql(self):
    lexer = QsciLexerSQL()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def tex(self):
    lexer = QsciLexerTeX()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setFont(QFont(self._config["font"]))


def bat(self):
    lexer = QsciLexerBatch()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def cmake(self):
    lexer = QsciLexerCMake()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setFont(QFont(self._config["font"]))


def postscript(self):
    lexer = QsciLexerPostScript()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def markdown(self):
    lexer = QsciLexerMarkdown()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Header1)
    lexer.setColor(QColor("#FFA500"), lexer.Header2)
    lexer.setColor(QColor("#ffffff"), lexer.Header3)
    lexer.setFont(QFont(self._config["font"]))


def makefile(self):
    lexer = QsciLexerMakefile()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setFont(QFont(self._config["font"]))


def pascal(self):
    lexer = QsciLexerPascal()
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def tcl(self):
    lexer = QsciLexerTCL()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setFont(QFont(self._config["font"]))


def verilog(self):
    lexer = QsciLexerVerilog()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor(self._config["editor_theme"]), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def spice(self):
    lexer = QsciLexerSpice()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setFont(QFont(self._config["font"]))


def vhdl(self):
    lexer = QsciLexerVHDL()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def octave(self):
    lexer = QsciLexerOctave()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))


def fortran77(self):
    lexer = QsciLexerFortran77()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(self._config["editor_theme"]))
    lexer.setColor(QColor("#808080"), lexer.Comment)
    lexer.setColor(QColor("#FFA500"), lexer.Keyword)
    lexer.setFont(QFont(self._config["font"]))
