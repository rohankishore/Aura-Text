from PyQt6.Qsci import *
from PyQt6.QtGui import QColor, QFont
import json

with open("Data/config.json", "r") as json_file:
    json_data = json.load(json_file)

editor_bg = str(json_data["editor_theme"])
font = str(json_data["font"])

def python(self):
    lexer = QsciLexerPython()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setColor(QColor('#ffffff'), lexer.ClassName)
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
    lexer.setColor(QColor('#808080'), lexer.Tag)
    lexer.setFont(QFont(font))

def cpp(self):
    lexer = QsciLexerCPP()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor(editor_bg))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setColor(QColor('#ffffff'), lexer.Identifier)
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