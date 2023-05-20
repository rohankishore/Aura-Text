from PyQt6.Qsci import *
from PyQt6.QtGui import QColor, QFont


def python(self):
    lexer = QsciLexerPython()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setColor(QColor('#ffffff'), lexer.ClassName)
    lexer.setFont(QFont('Consolas'))

class PythonLexer(QsciLexerPython):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDefaultColor(QColor('white'))
        self.setPaper(QColor("#d3d3d3"))

def csharp(self):
    lexer = QsciLexerCSharp()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont('Consolas'))


def json(self):
    lexer = QsciLexerJSON()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont('Consolas'))

def js(self):
    lexer = QsciLexerJavaScript()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setColor(QColor('#ffffff'), lexer.Default)
    lexer.setFont(QFont('Consolas'))

def fortran(self):
    lexer = QsciLexerFortran()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont('Consolas'))

def java(self):
    lexer = QsciLexerJava()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont('Consolas'))

def yaml(self):
    lexer = QsciLexerYAML()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont('Consolas'))

def xml(self):
    lexer = QsciLexerXML()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setFont(QFont('Consolas'))

def html(self):
    lexer = QsciLexerHTML()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Tag)
    lexer.setColor(QColor('#FFA500'), lexer.Script)
    lexer.setColor(QColor('#ffffff'), lexer.Attribute)
    lexer.setFont(QFont('Consolas'))


def cpp(self):
    lexer = QsciLexerCPP()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    #self.setMarginsBackgroundColor(QColor("#1e1f22"))
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setColor(QColor('#ffffff'), lexer.Identifier)
    lexer.setFont(QFont('Consolas'))

def ruby(self):
    lexer = QsciLexerRuby()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setColor(QColor('#ffffff'), lexer.ClassName)
    lexer.setFont(QFont('Consolas'))

def perl(self):
    lexer = QsciLexerPerl()
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont('Consolas'))

def pascal(self):
    lexer = QsciLexerPascal()
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont('Consolas'))

def css(self):
    lexer = QsciLexerCSS()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setFont(QFont('Consolas'))

# Slot for SQL action
def sql(self):
    lexer = QsciLexerSQL()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont('Consolas'))

# Slot for Lua action
def lua(self):
    lexer = QsciLexerLua()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont('Consolas'))

# Slot for IDL action
def idl(self):
    lexer = QsciLexerIDL()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont('Consolas'))

# Slot for MATLAB action
def matlab(self):
    lexer = QsciLexerMatlab()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont('Consolas'))

# Slot for Tcl action
def tcl(self):
    lexer = QsciLexerTCL()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setFont(QFont('Consolas'))

# Slot for VB action
def verilog(self):
    lexer = QsciLexerVerilog()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont('Consolas'))

# Slot for Scala action
def spice(self):
    lexer = QsciLexerSpice()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setFont(QFont('Consolas'))

# Slot for VHDL action
def vhdl(self):
    lexer = QsciLexerVHDL()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont('Consolas'))

# Slot for Octave action
def octave(self):
    lexer = QsciLexerOctave()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont('Consolas'))

# Slot for Forth action
def fortran77(self):
    lexer = QsciLexerFortran77()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setColor(QColor('#FFA500'), lexer.Keyword)
    lexer.setFont(QFont('Consolas'))

# Slot for TeX action
def tex(self):
    lexer = QsciLexerTeX()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setFont(QFont('Consolas'))

def makefile(self):
    lexer = QsciLexerMakefile()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Comment)
    lexer.setFont(QFont('Consolas'))

def markdown(self):
    lexer = QsciLexerMarkdown()
    lexer.setDefaultColor(QColor("#FFFFFF"))
    self.current_editor.setLexer(lexer)
    lexer.setPaper(QColor("#1e1f22"))
    lexer.setColor(QColor('#808080'), lexer.Header1)
    lexer.setColor(QColor('#FFA500'), lexer.Header2)
    lexer.setColor(QColor('#ffffff'), lexer.Header3)
    lexer.setFont(QFont('Consolas'))