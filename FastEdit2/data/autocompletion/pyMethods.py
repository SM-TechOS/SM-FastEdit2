import json
import os
import json

loc = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\"
path = os.path.join(loc, "autocompletion\\addMore.json")
with open(path, "r") as file:
	_text = file.read()
data = json.loads(_text)
Methods = [
	"__init__","__name__","__main__","self","exec_","parent",
	"connect","triggered","clicked","toggled"
]

PyOthers = data["Python"]["Others"]