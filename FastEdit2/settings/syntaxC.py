import os
import json

loc = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
path = os.path.join(loc, "settings/editorTheme.json")
with open(path, "r") as file:
      _text = file.read()
data = json.loads(_text)

DefaultColor      = data["Color"]
DefaultBackground = data["Background"]
FoldArea          = data["FoldArea"]

Keyword           = data["SyntaxColouring"]["keyword"]
String            = data["SyntaxColouring"]["string"]
Comment           = data["SyntaxColouring"]["comment"]
Number            = data["SyntaxColouring"]["number"]
UnclosedString    = data["SyntaxColouring"]["unclosedString"]

HtmlString        = data["SyntaxColouring"]["html.string"]
HtmlTag           = data["SyntaxColouring"]["html.tag"]
HtmlValue         = data["SyntaxColouring"]["html.value"]
HtmlAtr           = data["SyntaxColouring"]["html.attribute"]
HtmlEntity        = data["SyntaxColouring"]["html.entity"]

cssTag            = data["SyntaxColouring"]["css.tag"]
cssValue          = data["SyntaxColouring"]["css.value"]
cssAtr            = data["SyntaxColouring"]["css.attribute"]
cssPseudoElement  = data["SyntaxColouring"]["css.pseudoElement"]
cssProperty  = data["SyntaxColouring"]["css.property"]
cssExtendPseoudoEl= data["SyntaxColouring"]["css.extendedPseudoElement"]
cssExtendPseoudoCl= data["SyntaxColouring"]["css.extendedPseudoClass"]
cssPseudoCl       = data["SyntaxColouring"]["css.pseudoClass"]
cssVar            = data["SyntaxColouring"]["css.variables"]
cssClassSelector  = data["SyntaxColouring"]["css.classSelector"]
cssIdSelector     = data["SyntaxColouring"]["css.idSelector"]
cssMediaRule      = data["SyntaxColouring"]["css.mediaRule"]

pyFString         = data["SyntaxColouring"]["python.fString"]
pyClassName         = data["SyntaxColouring"]["python.className"]
pyFunName        = data["SyntaxColouring"]["python.methodName"]
pyDec         = data["SyntaxColouring"]["python.decorator"]

jsonProperty = data["SyntaxColouring"]["json.property"]
jsonIri = data["SyntaxColouring"]["json.iri"]