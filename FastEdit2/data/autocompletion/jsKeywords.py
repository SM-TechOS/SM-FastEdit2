import json
import os
import json

loc = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\"
path = os.path.join(loc, "autocompletion\\addMore.json")
with open(path, "r") as file:
	_text = file.read()
data = json.loads(_text)
jsKeywords = [
      "break", "case", "catch", "continue", "debugger", "default", "delete", "do", "else", "finally", "for", "function", 
      "if", "in", "instanceof", "new", "return", "switch", "this", "throw", "try", "typeof", "var", "void", "while", 
      "let","null","true","false","class", "const", "enum", "export", "extends", "import","super","implements", 
      "interface", "package", "private", "protected", "public", "static", "yield","NaN","undefined","Infinity",
      "byte", "char", "goto", "long", "final", "float", "short", "double", "native", "throws", "boolean", "abstract", 
      "volatile", "transient", "synchronized",
]
JSOthers = data["JavaScript"]["Others"]