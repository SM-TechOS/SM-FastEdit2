from PyQt5 import QtCore
import PyQt5
from PyQt5.Qt import Qt
from PyQt5.Qsci import *
from PyQt5.QtCore import QFileInfo, endl
from PyQt5.QtGui import QClipboard, QColor, QFont, QFontMetrics
from PyQt5.QtWidgets import QApplication, QMenu
from .mainWidgets import *
import platform
from settings.font import *
from settings.shortcuts import *
from settings.theme import *
from settings.syntaxC import *
from data.autocompletion.pyqt5List import Modules, Widgets
from data.autocompletion.pyKeywords import Keywords
from data.autocompletion.jsKeywords import *
from data.autocompletion.pyMethods import *
from data.autocompletion.cssExtra import *
from data.autocompletion.htmlExtra import *
from data.autocompletion.jsonLists import *
from data.calltips.python import *
from settings.editorsettings import *
from methods import *
import json
# Variable
tagsC = QColor(HtmlTag)
commentC = QColor(Comment)
attrC = QColor(HtmlAtr)
strC = QColor(String)
marginC = Theme.EditorBG
keyWordC = QColor(Keyword)

loc = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
path = os.path.join(loc, "data/api/addApi.json")
with open(path, "r") as file:
    _text = file.read()
data = json.loads(_text)
mainText = ""
loc = getLocation(os.path.abspath(__file__))
class LexerJS(QsciLexerJavaScript):
      def __init__(self):
            super().__init__()
            # adding let keyword to lexer
      def keywords(self, index):
            keywords = QsciLexerJavaScript.keywords(self, index) or ''
            if index == 1:
                  return  ' let ' + keywords
                  
class LexerPython(QsciLexerPython):
      def __init__(self):
            super().__init__()
      # adding extra keywords to lexer
      def keywords(self, index):
            keywords = QsciLexerPython.keywords(self, index) or ''
            if index == 1:
                  return  ' input ' + ' len ' + ' __name__ ' + ' str ' + ' int ' + ' float ' + ' self ' + ' __peg_parser__ ' + ' await ' + ' nonlocal ' + ' True ' + ' False ' + keywords
 # editor area
class Editor(QsciScintilla):
      """Editor Widget"""
      selection_lock          = None
      selection_indicator     = 4
      def __init__(self, parent=None):
            """Main components of Editor widget."""
            super(Editor, self).__init__(parent)
            self.setStyleSheet("""
* {
      border: none;
}

            """)
            # editor
            self.setSelectionBackgroundColor(Selection.ColorBG)
            self.textChanged.connect(self.unsaved)
            self.textChanged.connect(self.textChanged_)
            self.selectionChanged.connect(self.onSelection)
            self.selectionChanged.connect(self.getSelectedCharNum)
            # variables
            self.saved              = False # saved file or not
            self.path               = None  # file path or not
            self.selection_lock     = False 
            self.savable            = True  # can be save or not
            # scroll bar
            # font
            self.font = QFont()
        
            system = platform.system().lower()
            if system == 'windows':
                  self.font.setFamily(FontFamily.Editor)
            else:
                  self.font.setFamily(FontFamily.Editor)
        
            self.font.setFixedPitch(True)
            self.font.setPointSizeF(FontSize.FontSizeF)
            self.setFont(self.font)
            self.setMarginsFont(self.font)
            # match braces 
            self.setMatchedBraceBackgroundColor(QColor.fromRgb(10, 82, 190))
            self.setMatchedBraceForegroundColor(Theme.EditorC)
            self.setUnmatchedBraceBackgroundColor(Theme.EditorBG)
            self.setUnmatchedBraceForegroundColor(QColor(UnclosedString))
            self.setBraceMatching(BraceMatching)
            # wrap
            self.setWhitespaceVisibility(QsciScintilla.WsVisible)
            self.setWhitespaceBackgroundColor(Theme.EditorBG)
            self.setWhitespaceForegroundColor(QColor("#666"))
            self.setIndentationGuides(True)
            self.setIndentationGuidesBackgroundColor(QColor("#777"))
            self.setTabDrawMode(QsciScintilla.TabStrikeOut)
            # font
            self.font = QFont()
            self.font.setFixedPitch(True)
            self.font.setFamily(FontFamily.Editor)
            self.font.setPointSizeF(FontSize.FontSizeF)
            self.setFont(self.font)
            self.setMarginsFont(self.font)
            # line number bar
            self.updateMarginWidth()
            self.setMarginLineNumbers(0, LineNumbersVisible)
            self.setMarginsForegroundColor(Theme.LineNumberC)
            self.setMarginsBackgroundColor(Theme.EditorBG)
            # context menu
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.customContextMenu)
            # caret
            self.SendScintilla(QsciScintilla.SCI_SETCARETFORE, QColor('#ffffff'))
            self.setCaretWidth(Caret.CaretWidth)
            self.setCaretLineBackgroundColor(QColor.fromRgbF(Caret.CaretBColorR,Caret.CaretBColorG,Caret.CaretBColorB, Caret.CaretBColorA))
            self.setCaretForegroundColor(QColor(Caret.CaretColor))
            self.setCaretLineVisible(True)
            self.SendScintilla(QsciScintilla.SCI_SETCARETSTYLE, Caret.CaretStyle)
            # Scroll bar
            self.verticalScrollBar().setStyleSheet(Theme.VScrollBar)
            widget = QLabel("")
            widget.setStyleSheet("background: #222;")
            self.setCornerWidget(widget)
            self.horizontalScrollBar().setStyleSheet(Theme.HScrollBar)
            self.verticalScrollBar().setContextMenuPolicy(Qt.NoContextMenu)
            self.horizontalScrollBar().setContextMenuPolicy(Qt.NoContextMenu)
            # tab size
            self.setTabWidth(Tab.TabWidth)
            self.cursorPositionChanged.connect(self.getlineAndCol)
            self.style = None
            ### 
            self.moveToMatchingBrace()
            # parent
            self.setHighlightingFor("text")
            self.setUtf8(True)
            self.setOverwriteMode(False)
            self.setMarginSensitivity(0, False)
            self.setAutoIndent(Indent.AutoIndent)
            self.setIndentationsUseTabs(Indent.IndentuseTabs)
            self.setText(mainText) 
            self.setBackspaceUnindents(Indent.BackSpaceUnIndent)
            self.setAcceptDrops(False)
            self.setEolMode(QsciScintilla.EolUnix)
            self.setPaper(Theme.EditorBG)
            self.setFoldMarginColors(Theme.MarginC, Theme.MarginBG)
            self.setFold()
            self.setAcceptDrops(True)
            if self.hasSelectedText():
                  self.getSelectedCharNum()
      def textChanged_(self):
            self.updateMarginWidth()
      def updateMarginWidth(self):
            """Update margin width if line numbers increased."""
            line_count  = self.lines()
            self.setMarginWidth(0, str(line_count) + "000")
      def reloadFile(self):
            self.parent.reloadFile()
            pass
      def unsaved(self):
            self.saved = False
            self.savable = True
            self.parent.btn2.setText("Unsaved")
      def customContextMenu(self, point):
            self.menu = Menu()
            undo = self.menu.addAction("Undo")
            undo.triggered.connect(self.undo)
            redo = self.menu.addAction("Redo")
            redo.triggered.connect(self.redo)
            self.menu.addSeparator()
            cut = self.menu.addAction("Cut")
            cut.triggered.connect(self.cut)
            copy = self.menu.addAction("Copy")
            copy.triggered.connect(self.copy)
            paste = self.menu.addAction("Paste")
            paste.triggered.connect(self.paste)
            self.menu.addSeparator()
            select_all = self.menu.addAction("Select All")
            select_all.triggered.connect(self.selectAllText)
            copy_all = self.menu.addAction("Copy All")
            copy_all.triggered.connect(self.copyAll)
            self.menu.addSeparator()
            deleteFle = self.menu.addAction("Delete File")
            deleteFle.triggered.connect(self.delete_file)
            ########################################
            undo.setShortcut(ShortcutKeys.Undo)
            redo.setShortcut(ShortcutKeys.Redo)
            cut.setShortcut(ShortcutKeys.Cut)
            copy.setShortcut(ShortcutKeys.Copy)
            paste.setShortcut(ShortcutKeys.Paste)
            select_all.setShortcut(ShortcutKeys.SelectAll)
            copy_all.setShortcut(ShortcutKeys.CopyAll)
            deleteFle.setShortcut(ShortcutKeys.DeleteFile)
            ########################################
            self.menu.exec_(self.mapToGlobal(point))
      def delete_file(self):
            self.parent.delete_file()
            pass
      def selectAllText(self):
            self.selectAll()
      def copyAll(self):
            self.selectAll()
            self.copy()
      def setHighlightingFor(self, lang: str):
            if lang == "text" or lang == "plain text":
                  self.style = None
                  self.setLexer(None)
                  self.setPaper(Theme.EditorBG)
                  self.setColor(Theme.EditorC)
            elif lang == "html" or lang == "HTML":
                  self.setAutoIndent(True)
                  self.style = "HTML"
                  font1 = QFont()
                  font1.setItalic(True)
                  font1.setFamily(FontFamily.Editor)
                  font1.setPointSizeF(FontSize.FontSizeF)
                  font2 = QFont()
                  font2.setFamily(FontFamily.Editor)
                  font2.setPointSizeF(FontSize.FontSizeF)
                  lexer = QsciLexerHTML(self)
                  self.setPaper(Theme.EditorBG)
                  self.setColor(Theme.EditorC)
                  lexer.setDefaultFont(self.font)
                  lexer.setDefaultPaper(Theme.EditorBG)
                  lexer.setDefaultColor(Theme.EditorC)
                  lexer.setColor(QColor(DefaultColor), QsciLexerHTML.Default)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.Default)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.PHPKeyword)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.PHPOperator)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.XMLEnd)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.XMLTagEnd)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.PHPDefault)
                  lexer.setColor(Theme.EditorC, QsciLexerHTML.PHPDefault)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.JavaScriptDefault)
                  lexer.setFont(self.font, QsciLexerHTML.JavaScriptDefault)
                  lexer.setFont(self.font, QsciLexerHTML.JavaScriptCommentLine)
                  lexer.setFont(self.font, QsciLexerHTML.JavaScriptCommentDoc)
                  lexer.setFont(self.font, QsciLexerHTML.JavaScriptComment)
                  lexer.setColor(QColor(Comment), QsciLexerHTML.JavaScriptCommentLine)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.JavaScriptCommentLine)
                  lexer.setColor(QColor(Comment), QsciLexerHTML.JavaScriptCommentDoc)
                  lexer.setColor(QColor(Comment), QsciLexerHTML.JavaScriptUnclosedString)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.JavaScriptCommentDoc)
                  lexer.setColor(QColor("#5eb1ff"), QsciLexerHTML.JavaScriptKeyword)
                  lexer.setFont(font1, QsciLexerHTML.JavaScriptKeyword)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.JavaScriptKeyword)
                  lexer.setColor(Theme.EditorC, QsciLexerHTML.JavaScriptDefault)
                  lexer.setFont(self.font, QsciLexerHTML.JavaScriptDefault)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.JavaScriptDefault)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.JavaScriptDefault)
                  lexer.setColor(QColor(Comment), QsciLexerHTML.JavaScriptCommentDoc)
                  lexer.setColor(QColor(Comment), QsciLexerHTML.JavaScriptComment)
                  lexer.setColor(QColor(Comment), QsciLexerHTML.JavaScriptCommentLine)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.JavaScriptComment)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.JavaScriptDoubleQuotedString)
                  lexer.setFont(self.font, QsciLexerHTML.JavaScriptDoubleQuotedString)
                  lexer.setColor(Theme.EditorC, QsciLexerHTML.JavaScriptDoubleQuotedString)
                  lexer.setColor(Theme.EditorC, QsciLexerHTML.JavaScriptComment)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.JavaScriptDoubleQuotedString)
                  lexer.setFont(self.font, QsciLexerHTML.JavaScriptSingleQuotedString)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.JavaScriptSingleQuotedString)
                  lexer.setColor(Theme.EditorC, QsciLexerHTML.JavaScriptSingleQuotedString)
                  lexer.setFont(self.font, QsciLexerHTML.JavaScriptUnclosedString)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.JavaScriptUnclosedString)
                  lexer.setFont(self.font, QsciLexerHTML.JavaScriptNumber)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.JavaScriptNumber)
                  lexer.setColor(QColor(Number), QsciLexerHTML.JavaScriptNumber)
                  lexer.setColor(QColor(Comment), QsciLexerHTML.JavaScriptSymbol)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.JavaScriptSymbol)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.JavaScriptRegex)
                  lexer.setColor(Theme.EditorC, QsciLexerHTML.JavaScriptRegex)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.JavaScriptStart)
                  lexer.setColor(Theme.EditorC, QsciLexerHTML.JavaScriptStart)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.JavaScriptWord)
                  lexer.setColor(Theme.EditorC, QsciLexerHTML.JavaScriptWord)
                  lexer.setFont(self.font, QsciLexerHTML.JavaScriptWord)
                  lexer.setFont(self.font, QsciLexerHTML.JavaScriptSymbol)
                  lexer.setFont(self.font, QsciLexerHTML.Default)
                  lexer.setColor(tagsC, QsciLexerHTML.Tag)
                  lexer.setColor(commentC, QsciLexerHTML.HTMLComment)
                  lexer.setFont(font1, QsciLexerHTML.HTMLComment)
                  lexer.setFont(font1, QsciLexerHTML.Attribute)
                  lexer.setColor(attrC, QsciLexerHTML.Attribute)
                  lexer.setFont(font1, QsciLexerHTML.UnknownAttribute)
                  lexer.setColor(attrC, QsciLexerHTML.UnknownAttribute)
                  lexer.setColor(QColor(HtmlString), QsciLexerHTML.HTMLDoubleQuotedString)
                  lexer.setColor(QColor(HtmlString), QsciLexerHTML.HTMLSingleQuotedString)
                  lexer.setColor(QColor(HtmlString), QsciLexerHTML.HTMLNumber)
                  lexer.setColor(QColor(HtmlEntity), QsciLexerHTML.Entity)
                  lexer.setFont(font2, QsciLexerHTML.Entity)
                  lexer.setColor(tagsC, QsciLexerHTML.OtherInTag)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.OtherInTag)
                  lexer.setColor(tagsC, QsciLexerHTML.UnknownTag)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.UnknownTag)
                  lexer.setColor(attrC, QsciLexerHTML.UnknownAttribute)
                  lexer.setColor(QColor(HtmlValue), QsciLexerHTML.HTMLValue)
                  lexer.setPaper(Theme.EditorBG, QsciLexerHTML.HTMLValue)
                  lexer.setFoldCompact(False)
                  self.lexerHTML = lexer
                  self.setHtmlAutoComplete()
                  self.setLexer(lexer)
            elif lang == "css" or lang == "CSS":
                  self.setAutoIndent(True)
                  self.style = "CSS"
                  font1 = QFont()
                  font1.setBold(False)
                  font1.setFamily(FontFamily.Editor)
                  font1.setPointSizeF(FontSize.FontSizeF)
                  font2 = QFont()
                  font2.setItalic(True)
                  font2.setFamily(FontFamily.Editor)
                  font2.setPointSizeF(FontSize.FontSizeF)
                  lexerCSS = QsciLexerCSS(self)
                  lexerCSS.setDefaultFont(font1)
                  lexerCSS.setDefaultPaper(Theme.EditorBG)
                  lexerCSS.setDefaultColor(Theme.EditorC)
                  lexerCSS.setColor(Theme.EditorC, QsciLexerCSS.Default)
                  lexerCSS.setColor(QColor(cssTag), QsciLexerCSS.Tag)
                  lexerCSS.setFont(font1, QsciLexerCSS.Tag)
                  lexerCSS.setColor(Theme.EditorC, QsciLexerCSS.Operator)
                  lexerCSS.setPaper(Theme.EditorBG, QsciLexerCSS.Operator)
                  lexerCSS.setColor(QColor(cssAtr), QsciLexerCSS.Attribute)
                  lexerCSS.setColor(QColor(cssProperty), QsciLexerCSS.CSS1Property)
                  lexerCSS.setColor(QColor(cssProperty), QsciLexerCSS.CSS2Property)
                  lexerCSS.setColor(QColor(cssProperty), QsciLexerCSS.CSS3Property)
                  lexerCSS.setColor(QColor(cssProperty), QsciLexerCSS.UnknownProperty)
                  lexerCSS.setColor(QColor(cssValue), QsciLexerCSS.Value)
                  lexerCSS.setColor(strC, QsciLexerCSS.SingleQuotedString)
                  lexerCSS.setColor(strC, QsciLexerCSS.DoubleQuotedString)
                  lexerCSS.setColor(QColor(cssPseudoElement), QsciLexerCSS.PseudoElement)
                  lexerCSS.setColor(QColor(cssExtendPseoudoEl), QsciLexerCSS.ExtendedPseudoElement)
                  lexerCSS.setColor(QColor(cssExtendPseoudoCl), QsciLexerCSS.ExtendedPseudoClass)
                  lexerCSS.setColor(QColor(cssPseudoCl), QsciLexerCSS.PseudoClass)
                  lexerCSS.setColor(QColor(cssPseudoCl), QsciLexerCSS.UnknownPseudoClass)
                  lexerCSS.setColor(QColor(cssVar), QsciLexerCSS.Variable)
                  lexerCSS.setColor(QColor(cssClassSelector), QsciLexerCSS.ClassSelector)
                  lexerCSS.setColor(QColor(cssIdSelector), QsciLexerCSS.IDSelector)
                  lexerCSS.setColor(QColor(cssMediaRule), QsciLexerCSS.MediaRule)
                  lexerCSS.setFont(font2, QsciLexerCSS.MediaRule)
                  lexerCSS.setColor(commentC, QsciLexerCSS.Comment)
                  lexerCSS.setFont(font2, QsciLexerCSS.Comment)
                  lexerCSS.setFont(font2, QsciLexerCSS.IDSelector)
                  self.setFont(font1)
                  lexerCSS.setFont(font1, QsciLexerCSS.Tag)
                  lexerCSS.setFoldCompact(True)
                  self.lexerCSS = lexerCSS
                  self.setCSSAutoComplete()
                  self.setLexer(lexerCSS)
            elif lang == "js" or lang == "javascript" or lang == "JavaScript":
                  self.style = "JavaScript"
                  self.setAutoIndent(True)
                  font2 = QFont()
                  font2.setItalic(True)
                  font2.setFamily(FontFamily.Editor)
                  font2.setPointSizeF(FontSize.FontSizeF)
                  font3 = QFont()
                  font3.setUnderline(True)
                  font3.setPointSizeF(FontSize.FontSizeF)
                  font3.setFamily(FontFamily.Editor)
                  lexerJs = LexerJS()
                  lexerJs.setDefaultFont(self.font)
                  lexerJs.setDefaultPaper(Theme.EditorBG)
                  lexerJs.setDefaultColor(QColor(Theme.EditorC))
                  lexerJs.setColor(Theme.EditorC, QsciLexerJavaScript.Default)
                  lexerJs.setColor(QColor(UnclosedString), QsciLexerJavaScript.UnclosedString)
                  lexerJs.setPaper(Theme.EditorBG, QsciLexerJavaScript.UnclosedString)
                  lexerJs.setFont(font3, QsciLexerJavaScript.UnclosedString)
                  lexerJs.setColor(commentC, QsciLexerJavaScript.Comment)
                  lexerJs.setPaper(Theme.EditorBG, QsciLexerJavaScript.Comment)
                  lexerJs.setFont(font2, QsciLexerJavaScript.Comment)
                  lexerJs.setColor(commentC, QsciLexerJavaScript.CommentLine)
                  lexerJs.setPaper(Theme.EditorBG, QsciLexerJavaScript.CommentLine)
                  lexerJs.setFont(font2, QsciLexerJavaScript.CommentLine)
                  lexerJs.setColor(commentC, QsciLexerJavaScript.CommentDoc)
                  lexerJs.setPaper(Theme.EditorBG, QsciLexerJavaScript.CommentDoc)
                  lexerJs.setFont(font2, QsciLexerJavaScript.CommentDoc)
                  lexerJs.setColor(QColor(Number), QsciLexerJavaScript.Number)
                  lexerJs.setPaper(Theme.EditorBG, QsciLexerJavaScript.HashQuotedString)
                  lexerJs.setColor(keyWordC, QsciLexerJavaScript.Keyword)
                  lexerJs.setFont(font2, QsciLexerJavaScript.Keyword)
                  lexerJs.setColor(keyWordC, QsciLexerJavaScript.KeywordSet2)
                  lexerJs.setFont(font2, QsciLexerJavaScript.KeywordSet2)
                  lexerJs.setColor(Theme.EditorC, QsciLexerJavaScript.Operator)
                  lexerJs.setColor(strC, QsciLexerJavaScript.SingleQuotedString)
                  lexerJs.setFont(self.font, QsciLexerJavaScript.SingleQuotedString)
                  lexerJs.setPaper(Theme.EditorBG, QsciLexerJavaScript.Regex)
                  lexerJs.setFont(self.font, QsciLexerJavaScript.Regex)
                  lexerJs.setColor(strC, QsciLexerJavaScript.DoubleQuotedString)
                  lexerJs.setFont(self.font, QsciLexerJavaScript.DoubleQuotedString)
                  lexerJs.setColor(strC, QsciLexerJavaScript.TripleQuotedVerbatimString)
                  lexerJs.setFont(self.font, QsciLexerJavaScript.TripleQuotedVerbatimString)
                  lexerJs.setColor(keyWordC, QsciLexerJavaScript.GlobalClass)
                  self.lexerJs = lexerJs
                  self.setJsAutoComplete()
                  self.setLexer(lexerJs)
            elif lang == "py" or lang == "python":
                  self.style = "Python"
                  self.setAutoIndent(True)
                  self.lexerPy = LexerPython()
                  font2 = QFont()
                  font2.setItalic(True)
                  font2.setFamily(FontFamily.Editor)
                  font2.setPointSizeF(FontSize.FontSizeF)
                  font3 = QFont()
                  font3.setUnderline(True)
                  font3.setPointSizeF(FontSize.FontSizeF)
                  font3.setFamily(FontFamily.Editor)
                  self.lexerPy.setDefaultColor(Theme.EditorC)
                  self.lexerPy.setDefaultFont(self.font)
                  self.lexerPy.setDefaultPaper(Theme.EditorBG)
                  self.lexerPy.setColor(Theme.EditorC, QsciLexerPython.Default)
                  self.lexerPy.setFont(self.font, QsciLexerPython.Default)
                  self.lexerPy.setPaper(Theme.EditorBG, QsciLexerPython.Default)
                  self.lexerPy.setColor(keyWordC, QsciLexerPython.Keyword)
                  self.lexerPy.setFont(font2, QsciLexerPython.Keyword)
                  self.lexerPy.setColor(QColor(pyClassName), QsciLexerPython.ClassName)
                  self.lexerPy.setFont(self.font, QsciLexerPython.ClassName)
                  self.lexerPy.setColor(Theme.EditorC, QsciLexerPython.Operator)
                  self.lexerPy.setColor(QColor(Number), QsciLexerPython.Number)
                  self.lexerPy.setColor(QColor(pyDec), QsciLexerPython.Decorator)
                  self.lexerPy.setColor(QColor(pyFunName), QsciLexerPython.FunctionMethodName)
                  self.lexerPy.setFont(self.font, QsciLexerPython.FunctionMethodName)
                  self.lexerPy.setColor(QColor(pyFString), QsciLexerPython.SingleQuotedFString)
                  self.lexerPy.setFont(font2, QsciLexerPython.SingleQuotedFString)
                  self.lexerPy.setColor(strC, QsciLexerPython.SingleQuotedString)
                  self.lexerPy.setFont(self.font, QsciLexerPython.SingleQuotedString)
                  self.lexerPy.setColor(QColor(pyFString), QsciLexerPython.DoubleQuotedFString)
                  self.lexerPy.setFont(font2, QsciLexerPython.DoubleQuotedFString)
                  self.lexerPy.setColor(strC, QsciLexerPython.DoubleQuotedString)
                  self.lexerPy.setFont(self.font, QsciLexerPython.DoubleQuotedString)
                  self.lexerPy.setColor(QColor(pyFString), QsciLexerPython.TripleSingleQuotedFString)
                  self.lexerPy.setFont(font2, QsciLexerPython.TripleSingleQuotedFString)
                  self.lexerPy.setColor(QColor(pyFString), QsciLexerPython.TripleDoubleQuotedFString)
                  self.lexerPy.setFont(font2, QsciLexerPython.TripleDoubleQuotedFString)
                  self.lexerPy.setColor(strC, QsciLexerPython.TripleSingleQuotedString)
                  self.lexerPy.setFont(self.font, QsciLexerPython.TripleSingleQuotedString)
                  self.lexerPy.setColor(strC, QsciLexerPython.TripleDoubleQuotedString)
                  self.lexerPy.setFont(self.font, QsciLexerPython.TripleDoubleQuotedString)
                  self.lexerPy.setPaper(Theme.EditorBG, QsciLexerPython.UnclosedString)
                  self.lexerPy.setColor(QColor(UnclosedString), QsciLexerPython.UnclosedString)
                  self.lexerPy.setFont(self.font, QsciLexerPython.UnclosedString)
                  self.lexerPy.setColor(QColor(Comment), QsciLexerPython.Comment)
                  self.lexerPy.setFont(font2, QsciLexerPython.Comment)
                  self.lexerPy.setColor(QColor(Comment), QsciLexerPython.CommentBlock)
                  self.lexerPy.setFont(font2, QsciLexerPython.CommentBlock)
                  self.lexerPy.setHighlightSubidentifiers(True)
                  self.setHotspotUnderline(True)
                  self.lexerPy.setAutoIndentStyle(QsciScintilla.AiClosing)
                  self.setFold()
                  self.setPythonCallTips()
                  self.setPyAutoComplete()
                  self.setLexer(self.lexerPy)
            elif lang == "json":
                  self.style = "JSON"
                  self.lexerJSON = QsciLexerJSON()
                  self.setPaper(Theme.EditorBG)
                  self.setColor(Theme.EditorC)
                  font1 = QFont()
                  font1.setPointSizeF(FontSize.FontSizeF)
                  font1.setFamily(FontFamily.Editor)
                  font1.setItalic(True)
                  self.lexerJSON.setDefaultColor(Theme.EditorC)
                  self.lexerJSON.setDefaultFont(self.font)
                  self.lexerJSON.setDefaultPaper(Theme.EditorBG)
                  self.lexerJSON.setColor(Theme.EditorC, QsciLexerJSON.Default)
                  self.lexerJSON.setColor(keyWordC, QsciLexerJSON.Keyword)
                  self.lexerJSON.setColor(strC, QsciLexerJSON.String)
                  self.lexerJSON.setColor(QColor(jsonIri), QsciLexerJSON.IRI)
                  self.lexerJSON.setFont(font1, QsciLexerJSON.IRI)
                  self.lexerJSON.setColor(QColor(jsonProperty), QsciLexerJSON.Property)
                  self.lexerJSON.setColor(QColor(Number), QsciLexerJSON.Number)
                  self.lexerJSON.setColor(QColor(UnclosedString), QsciLexerJSON.UnclosedString)
                  self.lexerJSON.setPaper(Theme.EditorBG, QsciLexerJSON.UnclosedString)
                  self.lexerJSON.setColor(Theme.EditorC, QsciLexerJSON.Operator)
                  self.lexerJSON.setColor(QColor(Comment), QsciLexerJSON.CommentBlock)
                  self.lexerJSON.setColor(QColor(Comment), QsciLexerJSON.CommentBlock)
                  self.lexerJSON.setColor(QColor(Comment), QsciLexerJSON.CommentLine)
                  self.lexerJSON.setColor(QColor(Comment), QsciLexerJSON.CommentLine)
                  self.setFold()
                  self.setJSONAutoComplete()
                  self.setLexer(self.lexerJSON)
      def setJSONAutoComplete(self):
            self.autocomplete = QsciAPIs(self.lexerJSON)
            for words in Values:
                  self.autocomplete.add(words)
            self.autocomplete.prepare()
            self.setAutoCompletionThreshold(1)
            self.setAutoCompletionSource(QsciScintilla.AcsAll)
            self.setAutoCompletionCaseSensitivity(False)
            self.setAutoCompletionReplaceWord(True)
            self.setAutoCompletionShowSingle(True)
            self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)
            self.autoCompleteFromAll()
      def setPyAutoComplete(self):
            self.autocomplete = QsciAPIs(self.lexerPy)
            for word in Modules:
                  self.autocomplete.add(word)
            for widgets in Widgets:
                  self.autocomplete.add(widgets)
            for words in Methods:
                  self.autocomplete.add(words)
            for keywords in Keywords:
                  self.autocomplete.add(keywords)
            for words in PyOthers:
                  self.autocomplete.add(words)
            for words in builtin:
                  self.autocomplete.add(words)
            for files in data["apiFiles"]:
                  self.autocomplete.load(f"{loc}/{files}")
            self.registerImage(4, QPixmap("Images/Icons/iconFunc.png"))
            self.registerImage(1, QPixmap("Images/Icons/iconClass.png"))
            self.autocomplete.prepare()
            self.setAutoCompletionThreshold(1)
            self.setAutoCompletionSource(QsciScintilla.AcsAll)
            self.setAutoCompletionCaseSensitivity(False)
            self.setAutoCompletionReplaceWord(True)
            self.setAutoCompletionShowSingle(True)
            self.setAutoCompletionFillupsEnabled(True)
            self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)
            self.autoCompleteFromAll()
      def setFold(self):
            x = self.FoldStyle(self.FoldStyle(QsciScintilla.FoldStyle.PlainFoldStyle)) 
            if not x:
                  self.foldAll(False)
            self.setFolding(x)
      def unsetFold(self):
            self.setFolding(0)
      def getlineAndCol(self):
            line = self.getCursorPosition()[0] + 1
            colm = self.getCursorPosition()[1] + 1
            self.parent.btn1.setText(f"Ln: {line}, Col: {colm}")
      def getSelectedCharNum(self):
            if self.hasSelectedText():
                  line = self.getCursorPosition()[0] + 1
                  colm = self.getCursorPosition()[1] + 1
                  start = self.SendScintilla(QsciScintilla.SCI_GETSELECTIONSTART)
                  end = self.SendScintilla(QsciScintilla.SCI_GETSELECTIONEND)
                  self.parent.btn1.setText(f"Ln: {line}, Col: {colm} (Selected: {end-start})")
      def undoAct(self):
            self.undo()
      def redoAct(self):
            self.redo()
      def setJsAutoComplete(self):
            self.setAutoCompletionCaseSensitivity(False)
            self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
            self.setAutoCompletionThreshold(1)
            self.updateAutoCompleteJs()
      def setHtmlAutoComplete(self):
            self.setAutoCompletionCaseSensitivity(False)
            self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
            self.setAutoCompletionThreshold(1)
            self.updateAutoCompleteHTM()
      def updateAutoCompleteJs(self, text=None):
            self.autocomplete = QsciAPIs(self.lexerJs)
            for words in jsKeywords:
                  self.autocomplete.add(words)
            for words in JSOthers:
                  self.autocomplete.add(words)
            if not text:
                  firstList = []   
                  secondList = []  
                  for item in secondList:
                        self.autocomplete.add(item)
                  self.autocomplete.prepare()
      def updateAutoCompleteHTM(self, text=None):
            self.autocomplete = QsciAPIs(self.lexerHTML)
            self.keywords = self.lexerHTML.keywords(1)
            self.keywords = self.keywords.split(' ')
            for word in self.keywords:
                  self.autocomplete.add(word)
            for words in HTMLOtherList:
                  self.autocomplete.add(words)
            for words in HTMLOthers:
                  self.autocomplete.add(words)
            if not text:
                  firstList = []   
                  secondList = []  
                  for item in secondList:
                        self.autocomplete.add(item)
                  self.autocomplete.prepare()
      def setCSSAutoComplete(self):
            self.setAutoCompletionCaseSensitivity(False)
            self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
            self.setAutoCompletionThreshold(1)
            self.updateAutoCompleteCSS()
      def updateAutoCompleteCSS(self, text=None):
            self.autocomplete = QsciAPIs(self.lexerCSS)
            self.keywords = self.lexerCSS.keywords(1)
            self.keywords = self.keywords.split(' ')
            for word in self.keywords:
                  self.autocomplete.add(word)
            for words in CSSOtherList:
                  self.autocomplete.add(words)
            for words2 in CSSOther2:
                  self.autocomplete.add(words2)
            if not text:
                  firstList = []   
                  secondList = []
                  for item in secondList:
                        self.autocomplete.add(item)
                  self.autocomplete.prepare()
      def setPythonCallTips(self):
            self.setCallTipsStyle(QsciScintilla.CallTipsStyle.CallTipsNoContext)
            self.setCallTipsPosition(QsciScintilla.CallTipsAboveText)
            self.setCallTipsBackgroundColor(Theme.CallTipBG)
            self.setCallTipsForegroundColor(Theme.CallTipC)
            self.setCallTipsHighlightColor(Theme.HighlightedCallTip)
            self.setCallTipsVisible(CallTipsEnabled)
      def onSelection(self):
            if self.selection_lock == False:
                  self.selection_lock = True
                  selectedText = self.selectedText()
                  self.clearSelectionHighlights()
                  if selectedText.isidentifier():
                        self.highlightSelectedText(selectedText, case_sensitive=True,regular_expression=True)
                        self.setCaretLineBackgroundColor(Editor_Dark)
                  self.selection_lock = False
      def highlightSelectedText(self, highlight_text, case_sensitive=True, regular_expression=False):
            self.setIndicator("selection")
            matches = self.findAll(
                  highlight_text,
                  case_sensitive,
                  regular_expression,
                  text_to_bytes=True,
                  whole_words=True
            )
            if matches:
                  self.highlight(matches)
      def findAll(self,search_text, case_sensitive=True, regular_expression=False, text_to_bytes=False,whole_words=False):
            matches = index_strings_in_text(
                  search_text, 
                  self.text(), 
                  case_sensitive, 
                  regular_expression, 
                  text_to_bytes,
                  whole_words
                  )
            return matches
      def highlight(self, list):
            """
            Not done by me!
            INFO:This is done using the scintilla "INDICATORS" described in the official
                scintilla API (http://www.scintilla.org/ScintillaDoc.html#Indicators)
            """
            scintilla_command = QsciScintillaBase.SCI_INDICATORFILLRANGE
            for highlight in list:
                  start   = highlight[1]
                  length  = highlight[3] - highlight[1]
                  self.SendScintilla(
                        scintilla_command, 
                        start, 
                        length
                  )
      def clearSelectionHighlights(self):
            self.clearIndicatorRange(0,0,self.lines(),self.lineLength(self.lines()-1),self.selection_indicator)
            self.setCaretLineBackgroundColor(QColor.fromRgbF(Caret.CaretBColorR,Caret.CaretBColorG,Caret.CaretBColorB, Caret.CaretBColorA))
      def setIndicatorStyle(self, indicator,color):
            self.indicatorDefine(QsciScintillaBase.INDIC_STRAIGHTBOX, indicator)
            self.setIndicatorForegroundColor(color, indicator)
            self.SendScintilla(QsciScintillaBase.SCI_SETINDICATORCURRENT, indicator)
      def setIndicator(self, indicator):
            if indicator == "selection":
                  self.setIndicatorStyle(self.selection_indicator, Indicator.Color)
      def keyPressEvent(self, event):
            """Auto complete brackets"""
            super().keyPressEvent(event)
            if AutoCloseBrackets is True:
                  tags = {"[": "]", "'": "'", '"': '"', "{": "}", "(": ")", "<": ">"}
                  tags = tags.get(event.text())
                  if tags is not None:
                        l = self.getCursorPosition()[0]
                        p = self.getCursorPosition()[1]
                        self.insertAt(tags, l, p)
            else:
                  return