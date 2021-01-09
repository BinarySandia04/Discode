import discord

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

client.run(getToken())
