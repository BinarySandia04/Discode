# File for cmd utils
import os
import settings
import re

from pathlib import Path

PYPATH = str(Path(__file__).parent.absolute()) + "/"

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

# Executes command
def execute(s):
    print(s)
    os.system(s)

def screenCommand(name, command):
    execute("screen -X -S " + settings.js["screen_prefix"] + str(name) + " " + command)

def executeScreen(name, command):
    execute("screen -S " + settings.js["screen_prefix"] + str(name) + " -X stuff \"" + command + "\n\"")


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
    print(res)
    return res

def readFile(fileName):
    r = ""
    with open(PYPATH + fileName, "r") as rfile:
        r = rfile.read()
    return r
