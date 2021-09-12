"""
---------------
SM FastEdit   |
---------------
This file is a part of SM FastEdit 2.0.0!

COPYRIGHT SM 2021:
      AS YOU KNOW SM FASTEDIT 2.0.0 IS A OPEN SOURCE APPLICATION SO YOU CAN MODIFY IT AND CAN TELL ISSUES YOU NOTICED
      IN THIS APPLICATION. BUT IT WILL BE VERY WRONG IF YOU COPIED SOURCE AND THEN PUBLISHED IT. THANK YOU!
"""

import os
import re
from settings.font import *
from PyQt5.QtNetwork import *
import jsonManager
import importlib
import sys
import urllib.request
import json

def checkPyQt5():
      exists = importlib.util.find_spec("PyQt5") is not None
      return exists
def checkPythonVersion():
      version = sys.version_info.major
      return version
def checkQSci():
      exists = importlib.util.find_spec("PyQt5.Qsci") is not None
      return exists
def requirementsSatisfied():
      if checkPythonVersion() == 3:
            if checkPyQt5() is True:
                  if checkQSci() is True:
                        return True
                  else: 
                        return False
            else: 
                  return False
      else:
            return False
def getFileSize(path):
      fileSize_byts = os.path.getsize(path)
      fileSize = fileSize_byts/(1024*1024) 
      return fileSize
def getWriterName() -> str:
      name = "Shaurya Mishra"
      return name
def getOrganisationName() -> str:
      name = "SM Technology"
      return name
def getApplName() -> str:
      name = "SM FastEdit"
      return name
def getFullAppName() -> str:
      name = f"SM FastEdit {getAppVersion}"
      return name
def getAppVersion():
      path = urllib.request.urlopen("https://codeguru-eng.github.io/SM-FastEdit2/version.json")
      _text = path.read()
      data = json.loads(_text)
      Version = data["version"]
      return Version
def getAppType():
      AppType = "Code editor"
      return AppType
def getFontSize():
      fontSize = FontSize.FontSizeF
      return fontSize
def getFontFamily() -> str:
      family = FontFamily.Family
      return family
def getFileExt(filePath) -> str:
      split = os.path.splitext(filePath)
      extensionName = split[1]
      return extensionName
def getLocation(a1):
      loc = os.path.dirname(os.path.dirname(a1)) + "/"
      loc2 = loc.replace("\\", "/")
      return loc2
def getFileInfo(filePath) -> str:
      fileInfo = f"""
      <b>Name     : </b>{os.path.basename((filePath))}<br>
      <b>Extension: </b>{os.path.splitext(filePath)[1]}<br>
      <b>Size     : </b>{os.path.getsize(filePath)} bytes<br>
      """
      return fileInfo
def index_strings_in_text(search_text, text, case_sensitive=True, regular_expression=False, text_to_bytes=False,whole_words=False):
      if whole_words == True:
            search_text = r"\b(" + search_text + r")\b"
      if text_to_bytes == True:
            search_text = bytes(search_text, "utf-8")
            text = bytes(text, "utf-8")
      if regular_expression == False:
            search_text = re.escape(search_text)
      if case_sensitive == True:
            compiled_search_re = re.compile(search_text)
      else:
            compiled_search_re = re.compile(search_text, re.IGNORECASE)
      list_of_matches = [(0, match.start(), 0, match.end()) for match in re.finditer(compiled_search_re, text)]
      return list_of_matches
def updateJson(jsonFilePath, pro, value):
      """Updates given json file's key value.
      * jsonFilePath: here you have to give json file path
      * pro: here you have to give a key
      * value: here you have to give a value for key
      """
      jsonManager.update(jsonFilePath, pro, value)
def updateApp():
      ...