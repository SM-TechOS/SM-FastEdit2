import os 
import json

loc = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\"
path = os.path.join(loc, "Images\\iconManager.json")
with open(path, "r") as file:
      _text = file.read()
data = json.loads(_text)
IconPy      = data["Icon"]["FileIcon"]["Python"]
IconJS      = data["Icon"]["FileIcon"]["JavaScript"]
IconCSS     = data["Icon"]["FileIcon"]["CSS"]
IconJSON    = data["Icon"]["FileIcon"]["JSON"]
IconHTML    = data["Icon"]["FileIcon"]["HTML"]
IconText    = data["Icon"]["FileIcon"]["PlainText"]