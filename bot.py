import discord
import os

# PARAMS
VM_NUMBER = 8
########


client = discord.Client()

async def sendMessage(textFormatted, channel):
    await channel.send(textFormatted)

@client.event
async def on_message(msg):
    content = msg.content
    await sendMessage(content, msg.channel)

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
    os.system(s)

# Removes instances of mounted Vms
def removeVms(n):
    for i in range(n):
        vmPath = './root' + srt(i)
        if os.path.isdir(vmPath):
            # Umount and remove
            execute('sudo umount ' vmPath)
            execute('rm -R ' + vmPath)
    return

# Creates mounted Vms
def createVms(n):
    for i in range(n):
        vmPath = './root' + srt(i)
        if os.path.isdir(vmPath):
            execute('mkdir ' + vmPath)
            execute('sudo mount --bind ./root ' + vmPath)
    return

def restartVMs(n):
    removeVms(n)
    createVms(n)
    print("Successfully restarted VMs!")
    return

restartVMs(n)
client.run(getToken())
