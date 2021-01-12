import json

js = {}

r = ""
with open("settings.json", "r") as jsFile:
    js = json.loads(jsFile.read())
del r
