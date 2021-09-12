from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication, QProcess, QSize, Qt
from settings.theme import *
from settings.font import *
from settings.settings import *
from terminalFunc import *
from data.stylesheets import *
import os
import json
import methods


class Terminal(QWidget):
      """Console widget"""
      def __init__(self, parent=None):
          super(Terminal, self).__init__(parent)
          self.commandArea = QLineEdit()
          self.commandArea.setObjectName("commandArea")
          self.commandArea.setPlaceholderText("Type your command here...")
          self.commandArea.returnPressed.connect(self.push)
          self.outputArea  = QPlainTextEdit()
          self.outputArea.moveCursor(QTextCursor.EndOfLine)
          self.outputArea.setReadOnly(True)
          self.outputArea.setObjectName("outputArea")
          self.tell("FastEdit Terminal")
          font = QFont()
          font.setFamily(FontFamily.Console)
          font.setPointSizeF(FontSize.FontSizeTerminal)
          self.outputArea.setFont(font)
          layout = QVBoxLayout(self)
          layout.addWidget(self.outputArea)
          layout.addWidget(self.commandArea)
          layout.setContentsMargins(0,0,0,0)
          layout.setSpacing(0)
          self.outputArea.verticalScrollBar().setContextMenuPolicy(Qt.NoContextMenu)
          self.commandArea.setContextMenuPolicy(Qt.NoContextMenu)
          self._console = Console()
      def push(self):
            command = self.commandArea.text()
      def tell(self, text):
            self.outputArea.appendHtml(f"{text}")
      def reply(self, text):
            self.outputArea.appendHtml(f"<span style='color: #158cee;'>>></span> {text}")