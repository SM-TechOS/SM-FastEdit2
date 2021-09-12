from sys import call_tracing, flags
from PyQt5.QtGui import QColor
from PyQt5.Qsci import *
from data.stylesheets import *
"""Note: You will need to restart app to apply settings."""

loc = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
path = os.path.join(loc, "settings/editor.json")
with open(path, "r") as file:
	_text = file.read()
data = json.loads(_text)
class Tab:
	TabWidth            = data["TabWidth"]
class Caret:
	CaretWidth          = data["Caret"]["CaretWidth"]
	CaretColor          = data["Caret"]["CaretColor"]
	if data["Caret"]["LineHighlighting"] is True:
		CaretBColorR        = data["Caret"]["LineHighlightColor"]["r"]
		CaretBColorG        = data["Caret"]["LineHighlightColor"]["g"]
		CaretBColorB        = data["Caret"]["LineHighlightColor"]["b"]
		CaretBColorA        = data["Caret"]["LineHighlightColor"]["alpha"]
	elif data["Caret"]["LineHighlighting"] is False:
		CaretBColorR        = 51
		CaretBColorG        = 51
		CaretBColorB        = 51
		CaretBColorA        = 0
	if data["Caret"]["CaretStyle"] == "line":
		CaretStyle = QsciScintilla.CARETSTYLE_LINE
	elif data["Caret"]["CaretStyle"] == "block":
		CaretStyle = QsciScintilla.CARETSTYLE_BLOCK
	elif data["Caret"]["CaretStyle"] == "invisible":
		CaretStyle = QsciScintilla.CARETSTYLE_INVISIBLE
class Indent:
	AutoIndent          = data["Indent"]["AutoIndent"]
	BackSpaceUnIndent   = data["Indent"]["BackSpaceUnindent"]
	IndentuseTabs       = data["Indent"]["IndentUseTabs"]
class Indicator:
	Color               = QColor(data["HighlightMatchesIndicatorColor"]["r"],data["HighlightMatchesIndicatorColor"]["g"],data["HighlightMatchesIndicatorColor"]["b"],data["HighlightMatchesIndicatorColor"]["alpha"])
class Selection:
	ColorBG 		  = QColor(data["SelectionBackgroundColor"]["r"],data["SelectionBackgroundColor"]["g"],data["SelectionBackgroundColor"]["b"],data["SelectionBackgroundColor"]["alpha"])
if data["BraceMatching"] is True:
	BraceMatching = QsciScintilla.BraceMatch.SloppyBraceMatch
elif data["BraceMatching"] is False:
	BraceMatching = QsciScintilla.BraceMatch.NoBraceMatch
if data["LineNumbersVisible"] is True:
	LineNumbersVisible = True
elif data["LineNumbersVisible"] is False:
	LineNumbersVisible = False
if data["CallTipsEnabled"] is True:
	CallTipsEnabled = True
if data["CallTipsEnabled"] is False:
	CallTipsEnabled = False
if data["AutoCloseBrackets"] is True:
	AutoCloseBrackets = True
if data["AutoCloseBrackets"] is False:
	AutoCloseBrackets = False
Encoding = data["Encoding"]