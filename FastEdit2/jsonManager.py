"""
---------------
SM FastEdit   |
---------------
This file is a part of SM FastEdit 2.0.0!

COPYRIGHT SM 2021:
    AS YOU KNOW SM FASTEDIT 2.0.0 IS A OPEN SOURCE APPLICATION SO YOU CAN MODIFY IT AND CAN TELL ISSUES YOU NOTICED
    IN THIS APPLICATION. BUT IT WILL BE VERY WRONG IF YOU COPIED SOURCE AND THEN PUBLISHED IT. THANK YOU!
"""
import json

def update(filePath, key, value):
    jsonFile = open(filePath, "r")
    data = json.load(jsonFile) 
    jsonFile.close()
    tmp = data[key] 
    data[key] = value
    jsonFile = open(filePath, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()