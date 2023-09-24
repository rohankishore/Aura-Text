import json

from PyQt6.Qsci import QsciLexerCPP, QsciLexerVerilog, QsciLexerAVS, QsciLexerAsm, QsciLexerBash, QsciLexerBatch, \
    QsciLexerJavaScript
from PyQt6.Qsci import QsciLexerCSharp, QsciLexerFortran77, QsciLexerOctave, QsciLexerVHDL
from PyQt6.Qsci import QsciLexerJava, QsciLexerJSON, QsciLexerYAML, QsciLexerHTML, QsciLexerRuby, QsciLexerCMake, \
    QsciLexerCoffeeScript
from PyQt6.Qsci import QsciLexerPerl, QsciLexerCSS, QsciLexerLua, QsciLexerSQL, QsciLexerPascal, QsciLexerPostScript, \
    QsciLexerTCL, QsciLexerSRec, QsciLexerSpice
from PyQt6.Qsci import QsciLexerTeX, QsciLexerPython, QsciLexerXML, QsciLexerMakefile, QsciLexerMarkdown, \
    QsciLexerFortran
from PyQt6.QtGui import QColor, QFont

with open("Data/theme.json", "r") as json_file:
    json_data = json.load(json_file)


editor_bg = str(json_data["editor_theme"])
font = str(json_data["font"])
margin_bg = str(json_data["margin_theme"])
linenumber_bg = str(json_data["lines_theme"])
margin_fg = str(json_data["margin_fg"])
editor_fg = str(json_data["editor_fg"])
linenumber_fg = str(json_data["lines_fg"])
sidebar_bg = str(json_data["sidebar_bg"])

def python(self):
    lexer = QsciLexerPython()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setColor(QColor('#FFFFFF'), lexer.ClassName)
    lexer.setColor(QColor("#59ff00"), lexer.TripleSingleQuotedString)
    lexer.setColor(QColor("#59ff00"), lexer.TripleDoubleQuotedString)
    lexer.setColor(QColor("#3ba800"), lexer.SingleQuotedString)
    lexer.setColor(QColor("#3ba800"), lexer.DoubleQuotedString)
    lexer.setFont(QFont(font))

class PythonLexer(QsciLexerPython):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDefaultColor(QColor('white'))
        self.setPaper(QColor(editor_bg))
        self.setColor(QColor('#ffffff'), self.ClassName)
        self.setFont(QFont(font))

def csharp(self):
    lexer = QsciLexerCSharp()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def avs(self):
    lexer = QsciLexerAVS()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def asm(self):
    lexer = QsciLexerAsm()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setFont(QFont(font))

def coffeescript(self):
    lexer = QsciLexerCoffeeScript()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def ma(self):
    lexer = QsciLexerCSharp()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def json(self):
    lexer = QsciLexerJSON()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def js(self):
    lexer = QsciLexerJavaScript()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setColor(QColor('#ffffff'), lexer.Default)
    lexer.setFont(QFont(font))

def fortran(self):
    lexer = QsciLexerFortran()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def java(self):
    lexer = QsciLexerJava()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def bash(self):
    lexer = QsciLexerBash()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def yaml(self):
    lexer = QsciLexerYAML()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def xml(self):
    lexer = QsciLexerXML()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setFont(QFont(font))

def html(self):
    lexer = QsciLexerHTML()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#AB3254'), lexer.Tag)
    lexer.setColor(QColor("#FFFFFF"), lexer.Default)
    lexer.setColor(QColor("#BB8A29"), lexer.Entity)
    lexer.setFont(QFont(font))

def cpp(self):
    lexer = QsciLexerCPP()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setColor(QColor('#ffffff'), lexer.Identifier)
    lexer.setColor(QColor('#ffffff'), lexer.Default)
    lexer.setFont(QFont(font))

def srec(self):
    lexer = QsciLexerSRec()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setFont(QFont(font))

def ruby(self):
    lexer = QsciLexerRuby()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setColor(QColor('#ffffff'), lexer.ClassName)
    lexer.setFont(QFont(font))

def perl(self):
    lexer = QsciLexerPerl()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def css(self):
    lexer = QsciLexerCSS()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setFont(QFont(font))

def lua(self):
    lexer = QsciLexerLua()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def sql(self):
    lexer = QsciLexerSQL()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def tex(self):
    lexer = QsciLexerTeX()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setFont(QFont(font))

def bat(self):
    lexer = QsciLexerBatch()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def cmake(self):
    lexer = QsciLexerCMake()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setFont(QFont(font))

def postscript(self):
    lexer = QsciLexerPostScript()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def markdown(self):
    lexer = QsciLexerMarkdown()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Header1)
    lexer.setColor(QColor('#FFA500'), lexer.Header2)
    lexer.setColor(QColor('#ffffff'), lexer.Header3)
    lexer.setFont(QFont(font))

def makefile(self):
    lexer = QsciLexerMakefile()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setFont(QFont(font))

def pascal(self):
    lexer = QsciLexerPascal()
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def tcl(self):
    lexer = QsciLexerTCL()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setFont(QFont(font))

def verilog(self):
    lexer = QsciLexerVerilog()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor(editor_bg), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def spice(self):
    lexer = QsciLexerSpice()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setFont(QFont(font))

def vhdl(self):
    lexer = QsciLexerVHDL()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def octave(self):
    lexer = QsciLexerOctave()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))

def fortran77(self):
    lexer = QsciLexerFortran77()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont(font))