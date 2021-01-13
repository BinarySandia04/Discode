# File for cmd utils
import os
import settings
import re

from pathlib import Path

PYPATH = str(Path(__file__).parent.absolute().parent.absolute()) + "/"

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def getPath():
    return PYPATH

# Executes command
def execute(s):
    if settings.js["debug"]:
        print(s)
    os.system(s)

def screenCommand(name, command):
    execute("screen -X -S " + settings.js["screen_prefix"] + str(name) + " " + command)

def executeScreen(name, command):
    execute("screen -S " + settings.js["screen_prefix"] + str(name) + " -X stuff \"" + command + "\n\"")

# Return true if the file has something
def isScreenExecuting(name):
    # XD
    execute("echo $(ps -el | grep $(ps -el | grep $(ps -el | grep $(ps -el | grep $(screen -ls | grep " + settings.js["screen_prefix"] + str(name) + " | cut -f1 -d'.' | sed 's/\W//g') | grep bash | awk '{print $4}') | grep sudo | awk '{print $4}') | grep bash | awk '{print $4}') | grep -v bash) > .stmp" + str(name))
    s = readFile(".stmp" + str(name))
    if len(s) < 4:
        return False
    else:
        return True

# Creates an screen and restarts if it already exists
def createScreen(name):
    destroyScreen(name)
    execute("screen -dmS " + settings.js["screen_prefix"] + str(name) + " -L -Logfile screen." + str(name) + ".log")
    screenCommand(name, "logfile flush 0")

# Crea una screen con su log file y tambien pone a disposición una vm
def destroyScreen(name):
    execute("rm screen." + str(name) + ".log")
    screenCommand(name, "quit")
   
def getScreenLog(name):
    res = ansi_escape.sub('', readFile("screen." + str(name) + ".log"))
    if(settings.js["debug"]):
        print(res)
    return res

def readFile(fileName):
    r = ""
    with open(PYPATH + fileName, "r") as rfile:
        r = rfile.read()
    return r
