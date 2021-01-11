import json

js = {}

r = ""
with open("settings.json", "r") as jsFile:
    js = jsFile.read()
del r
