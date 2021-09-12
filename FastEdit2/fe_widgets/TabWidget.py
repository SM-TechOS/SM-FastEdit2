import os
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import *
from .Editor import Editor
from settings.theme import *
from settings.settings import *

class TabWidget(QTabWidget):
      def __init__(self, parent=None):
          super(TabWidget, self).__init__(parent)
          self.setMovable(Settings.TabMovable)
          self.setTabsClosable(Settings.TabClosable)
          self.setTabShape(QTabWidget.TabShape.Rounded)
          self.setLayoutDirection(Qt.LeftToRight)
          self.tabCloseRequested.connect(self.remove_tab)
          self.setUsesScrollButtons(Settings.TabScrollButtonsVisible)
          self.setIconSize(QtCore.QSize(Settings.TabIconWidth, Settings.TabIconHeight))
          self.currentChanged.connect(self.actionSaveunsave)
          self.currentChanged.connect(self.update_lineCol)
          self.currentChanged.connect(self.updateFileType)
          self.setAcceptDrops(True)
      def updateFileType(self):
          self.parent.updateFileType()
          pass
      def update_lineCol(self):
          self.parent.update_lineCol()
          pass
      def actionSaveunsave(self):
          self.parent.update_saveUnsave()
          pass
      def add_tab(self):
            a = self.addTab(Editor(), QIcon("Images/Icons/iconText"), "untitled")
            self.setCurrentIndex(a)
      def remove_tab(self, indx):
            z = self.currentIndex()
            if self.widget(indx):
                if self.widget(indx).saved is False:
                    if self.widget(indx).path is None:
                        if self.widget(indx).text() == "" or self.widget(indx).text() == None:
                            self.removeTab(indx)
                            return
                        else:
                            q = QMessageBox()
                            ans = q.question(None, "Warning!", f"Document {self.tabText(indx)} is not saved.\nClose file anyway?"\
                                                        ,QMessageBox.Yes | QMessageBox.No)
                            if (ans== QMessageBox.Yes):
                              self.removeTab(indx)
                            else:
                                return
                    elif self.widget(indx).saved is False:
                        q = QMessageBox()
                        ans = q.question(None, "Warning!", f"Document {self.tabText(indx)} is not saved.\nClose file anyway?"\
                                                        ,QMessageBox.Yes | QMessageBox.No)
                        if (ans== QMessageBox.Yes):
                            self.removeTab(indx)
                        else:
                            return
                else:
                    self.removeTab(indx)
            else:
                return
      def newTab(self, widget: QWidget, txt: str):
            self.addTab(widget, txt)