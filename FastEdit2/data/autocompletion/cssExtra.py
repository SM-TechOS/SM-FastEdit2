import json
import os
import json

loc = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\"
path = os.path.join(loc, "autocompletion\\addMore.json")
with open(path, "r") as file:
      _text = file.read()
data = json.loads(_text)
CSSOtherList = [
      "background","color","image","border","px",
	"before","after","selection","hover","focus","active"
]
CSSOther2 = data["CSS"]["Others"]