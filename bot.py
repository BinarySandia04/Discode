import discord
import string
import os

# PARAMS
VM_NUMBER = 8
MOUNT_DIRS = ["bin", "usr", "lib"]
AUTH_ID = 
########


client = discord.Client()

async def sendMessage(textFormatted, channel):
    await channel.send(textFormatted)

@client.event
async def on_message(msg):
    content = msg.content
    await sendMessage(msg.author.id, msg.channel)

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

# Removes instances of mounted Vms
def removeVms(n):
    for i in range(n):
        vmPath = './root' + str(i)
        if os.path.isdir(vmPath):
            # Umount and remove
            for d in MOUNT_DIRS:
                execute('sudo umount ' + vmPath + "/" + d)
            execute('sudo rm -R ' + vmPath)
    return

# Creates mounted Vms
def createVms(n):
    for i in range(n):
        vmPath = './root' + str(i)
        if not os.path.isdir(vmPath):
            execute('mkdir ' + vmPath + " " + vmPath + "/home")
            for d in MOUNT_DIRS:
                execute('mkdir ' + vmPath + "/" + d)
                execute('sudo mount --bind ./root/' + d + " " + vmPath + "/" + d)
    return

def restartVMs(n):
    print("Restarting VMs, this could take a while...")
    removeVms(n)
    createVms(n)
    print("Successfully restarted VMs!")
    return

restartVMs(VM_NUMBER)
client.run(getToken())
