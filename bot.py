import discord
import string
import asyncio
import time
import os
import re
import subprocess
from sys import executable

# PARAMS
VM_MAX_NUMBER = 128
MOUNT_DIRS = {"bin": "root/bin", "usr": "/usr", "lib": "/lib"}
OTHER_DIRS = ["home"]
ADMIN_ID = 342287101225598987 # Syndria#2417
GITHUB_REPO = "https://github.com/BinarySandia04/Dragoconda"
PREFIX = {"cpp": "```cpp\n//run", "py": "```py\n#run", "python": "```python\n#run"}
########
SCREEN_PREFIX = "dragoconda"
#######

client = discord.Client()
vm_assosiations = {}
user_assosiations = {}

channel_assosiations = {}

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def discordTrim(text):
    if len(text) < 1994:
        return "```" + text + "```"
    msgFinal = "\n... and many more"
    return "```" + text[:(1990 - len(msgFinal))] + msgFinal + "```"

def pythonGetOutput(text, finished):
    a = text.split("\n")
    res = ""
    if finished:
        if len(a) < 9:
            return res
        else:
            for i in range(5, len(a) - 3):
                res += a[i] + '\n'
    else:
        for i in range(5, len(a)):
            res += a[i]
    return res

# Fixa un usuari a un discord channel
def setUserToDcChannel(user, channel):
    channel_assosiations[user] = channel

def freeUserFromDcChannel(user):
    channel_assosiations.pop(user, None)

# Assigna una screen i una VM a un usuari
def assignVm(user):
    # Busquem en totes les vm i ens quedem amb la primera None
    if len(vm_assosiations) >= VM_MAX_NUMBER:
        return -1
    for i in range(len(vm_assosiations) + 1):
        if not i in vm_assosiations:
            createVm(str(i))
            createScreen(str(i))

            vm_assosiations[i] = user
            user_assosiations[user] = i

            return i
    return -1

def getLastCommitInfo():
    execute('git log --pretty=format:"%h - %an, %ar : %s" | head -n 1 > .lastcommit')
    execute('git log --pretty=format:"%H" >> .lastcommit')
    r = "No info"
    with open(".lastcommit", "r") as cfile:
        r = cfile.read()
    os.remove(".lastcommit")
    return r.split("\n")


# Borra la VM i la screen a un usuari
def removeVm(user):
    if user in user_assosiations:
        i = user_assosiations[user]
        destroyScreen(str(i))
        destroyVm(str(i))

        vm_assosiations.pop(i, None)
        user_assosiations.pop(user, None)



# Crea una screen con su log file y tambien pone a disposición una vm
def destroyScreen(name):
    execute("rm screen." + str(name) + ".log")
    screenCommand(name, "quit")
   
def getScreenLog(name):
    f = open("screen." + str(name) + ".log", "r")
    res = f.read()
    f.close()
    res = ansi_escape.sub('', res)
    print(res)
    return res

def createScreen(name):
    destroyScreen(name)
    execute("screen -dmS " + SCREEN_PREFIX + str(name) + " -L -Logfile screen." + str(name) + ".log")
    screenCommand(name, "logfile flush 0")

def screenCommand(name, command):
    execute("screen -X -S " + SCREEN_PREFIX + str(name) + " " + command)

def executeScreen(name, command):
    execute("screen -S " + SCREEN_PREFIX + str(name) + " -X stuff \"" + command + "\n\"")

# Gets guild stats for the bot
def getGuilds():
    global client
    
    users = 0

    n = len(client.guilds)
    s = "I AM AT **" + str(n) + "** SERVERS:\n"
    
    for guild in client.guilds:
        s += "**" + guild.name + "** " + str(guild.id) + " " + str(guild.member_count) + "\n"
        users += guild.member_count
    s += "In total there are " + str(users) + " users"

    return s

async def sendMessage(textFormatted, channel):
    return await channel.send(textFormatted)

async def wait(i):
    await asyncio.sleep(i)

# Funcions core, text és el codi trimmed ja llest per passar-ho
async def startCppProgram(msg, author, text):
    channel = channel_assosiations[author]
    
    # Reservar una sessio per al nostre usuari:
    vm_index = assignVm(author)
    
    if vm_index != -1: 
        # Write python code in the vm
        cppCode = open("root" + str(vm_index) + "/main.cc", "w")
        cppCode.write(text)
        cppCode.close()

        # Enter chroot environment
        executeScreen(str(vm_index), "sudo chroot --userspec=dragoconda root" + str(vm_index))
        # Run python file
        executeScreen(str(vm_index), "cd home && g++ ../main.cc -o main && ./main")
        # Exit chroot environment
        executeScreen(str(vm_index), "exit")
        
        statusMsg = await sendMessage("Running the code...", channel)

        await wait(4)

        # Get the result
        result = discordTrim(pythonGetOutput(getScreenLog(str(vm_index)), True))
        print("RES: " + result)

        removeVm(author)
        await statusMsg.edit(content="Done!")
        await sendMessage(result, channel)
    else:
        await sendMessage("Sorry, there are no VMs free right now. Maybe the bot is oversaturated", channel)
    freeUserFromDcChannel(author)



async def startPythonProgram(msg, author, text):
    channel = channel_assosiations[author]

    # Reservar una sessio per al nostre usuari:
    vm_index = assignVm(author)
    
    if vm_index != -1: 
        # Write python code in the vm
        pythonCode = open("root" + str(vm_index) + "/main.py", "w")
        pythonCode.write(text)
        pythonCode.close()

        # Enter chroot environment
        executeScreen(str(vm_index), "sudo chroot --userspec=dragoconda root" + str(vm_index))
        # Run python file
        executeScreen(str(vm_index), "python3 main.py")
        # Exit chroot environment
        executeScreen(str(vm_index), "exit")
        
        statusMsg = await sendMessage("Running the code...", channel)

        await wait(2)

        # Get the result
        log = getScreenLog(str(vm_index))
        result = discordTrim(pythonGetOutput(log, True))
        print("LOG: " + log)
        print("RES: " + result)

        removeVm(author)
        await statusMsg.edit(content="Done!")
        await sendMessage(result, channel)
    else:
        await sendMessage("Sorry, there are no VMs free right now. Maybe the bot is oversaturated", channel)
    freeUserFromDcChannel(author)

async def restartServer():
    execute("git fetch && git pull")
    await client.close()
    os.execv(executable, [executable, __file__])
    exit()

async def react(msg, emoji):
    await msg.add_reaction(emoji)

async def sendHelpMessage(channel):
    with open("help.txt", "r") as helpfile:
      await sendMessage(helpfile.read(), channel)

def addLineNumber(text):
    l = text.split("\n")
    r = ""
    i = 0
    for p in l:
        if i > 0 and i < len(l) - 1:
            r += str(i) + " " + p + "\n"
        else:
            r += p + "\n"
        i += 1
    return r

async def sendCodeMessage(text, channel):
    trimmed = addLineNumber(text)
    await sendMessage("**Your Code:**", channel)
    await sendMessage(trimmed, channel)

@client.event
async def on_message(msg):
    content = msg.content
    author = msg.author.id
    channel = msg.channel

    if author == client.user.id:
        return
    
    if content == "!a servers":
        if author == ADMIN_ID:
            await sendMessage(getGuilds(), channel)
    
    if content == "!anaconda":
        await sendHelpMessage(channel)
    
    if content == "!a r":
        if author == ADMIN_ID:
            await sendMessage("Restart!", channel)
            await restartServer()
    
    if content == "!a c":
        l = getLastCommitInfo()
        res = l[0]
        com = l[1]
        await sendMessage("**LAST COMMIT INFO:**\n```" + res + "```", channel)
        await sendMessage(GITHUB_REPO + "/commit/" + com, channel)

    elif content.startswith(PREFIX["cpp"]):
        # c++
        if author in user_assosiations:
            return
        
        await sendCodeMessage(content, channel)

        await msg.delete()
        setUserToDcChannel(author, channel)
        await startCppProgram(msg, author, content[len(PREFIX["cpp"]):len(content)-3])
    elif content.startswith(PREFIX["py"]) or content.startswith(PREFIX["python"]):
        # python
        if author in user_assosiations:
            return
        
        await sendCodeMessage(content, channel)

        await msg.delete()
        setUserToDcChannel(author, channel)
        await startPythonProgram(msg, author, content[len(PREFIX["py"]):len(content)-3])

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('---------')

    # Set custom status
    await client.change_presence(activity=discord.Game(name="!help"))

def getToken():
    f = open(".token")
    res = f.read()
    f.close()
    return res

# Executes command as sudo
def execute(s):
    print(s)
    os.system(s)

def destroyVm(n):
    vmPath = './root' + str(n)
    if os.path.isdir(vmPath):
        # Umount and remove
        for d in MOUNT_DIRS:
            execute('sudo umount ' + vmPath + "/" + d)
        execute('sudo rm -R ' + vmPath)


def createVm(n):
    vmPath = './root' + str(n)
    destroyVm(n)
    
    execute('mkdir ' + vmPath + " " + vmPath + "/home")
    for d in MOUNT_DIRS.keys():
        execute('mkdir ' + vmPath + "/" + d)
        execute("sudo mount --bind " + MOUNT_DIRS[d] + " " + vmPath + "/" + d)
    for d in OTHER_DIRS:
        execute('mkdir ' + vmPath + "/" + d)
        execute('sudo chown dragoconda ' + vmPath + "/" + d)
        execute('sudo chmod ug=rwx ' + vmPath +"/" + d)

async def some_function():
    await asyncio.sleep(5)

async def forever():
    while True:
        await some_function()


############################################################
asyncio.get_event_loop().create_task(forever())
client.run(getToken())
