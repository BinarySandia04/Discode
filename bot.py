# Main file of the bot
import discord
import string
import asyncio
import time
import os

from sys import executable

from safebox import vm
from safebox.cmd_utils import readFile, execute
import languages

import settings

class Discode(discord.Client):
    def __init__(self):
        """
        Starts the bot
        """
        super().__init__()

        self.vm = vm.VMmanager(settings.js["max_vm_instances"], settings.js["mount_dirs"], settings.js["other_dirs"])

        self.run(self.getToken())

        self.lastMessages = {}
    
    def getToken(self):
        """
        Reads the token provided in the .token file
        """
        return readFile(".token")
    
    def getLastCommitInfo(self):
        """
        Gets the last commit info
        """

        execute('git log --pretty=format:"%h - %an, %ar : %s" | head -n 1 > .lastcommit')
        execute('git log --pretty=format:"%H" >> .lastcommit')
        r = readFile(".lastcommit")
        os.remove(".lastcommit")
        return r.split("\n")

    async def restartServer(self):
        """
        Updates with remote and restarts the server
        """
        execute("git fetch && git pull")
        await self.close()
        os.execv(executable, [executable, __file__])
        exit()

    async def sendMessage(self, textFormatted, channel):
        """
        Quick function to send a message through a channel
        """
        return await channel.send(textFormatted)
    
    async def react(self, msg, emoji):
        """
        Reacts to a message with an emoji (it doesn't work lol)
        """
        await msg.add_reaction(emoji)

    async def sendHelpMessage(self, channel):
        """
        Sends the help message
        """
        await sendMessage(readFile(settings.js["help_file"]), channel)

    async def formatCode(self, msg, code):
        """
        Deletes and modifies the user's code message to add numbered line support
        TODO: Add user info
        """

        channel = msg.channel
        author  = msg.author

        trimmed = self.addLineNumber(code)

        await msg.delete()

        await sendMessage("**Your Code:**", channel)
        await sendMessage(trimmed, channel)

    def getCodeModule(self, code):
        """
        Gets in which language should the code be ran depending on the prefix
        """

        prefixes = settings.js["prefixes"]
        prefix = code.split("\n")[0]
        for l in prefixes.keys():
            for i in prefixes[l]:
                if prefix == i:
                    return l
        return None


    def getLastMessageContent(self, author):
        return lastMessages[author]

    def getRawCode(self, text):
        l = text.split("\n")
        l = l[1:len(l)-2]
        r = ""
        for line in l:
            r += line + "\n"
        return r

    def addLineNumber(self, text):
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
    
    # Gets guild stats for the bot
    def getGuilds(self):
        users = 0

        n = len(self.guilds)
        s = "I AM AT **" + str(n) + "** SERVERS:\n"
        
        for guild in self.guilds:
            s += "**" + guild.name + "** " + str(guild.id) + " " + str(guild.member_count) + "\n"
            users += guild.member_count
        s += "In total there are " + str(users) + " users"

        return s

    async def on_message(self, msg):
        """
        Function for handling bot's messages
        """
        content = msg.content
        author = msg.author.id
        channel = msg.channel

        if author == self.user.id:
            return
        
        lastMessages[msg.author.id] = msg.content # Cache the content!
        
        if content == "!dc servers":
            if author == settings.js["admin_id"]:
                await sendMessage(getGuilds(), channel)
        
        if content == "!dc":
            await sendHelpMessage(channel)
        
        if content == "!dc r":
            if author == settings.js["admin_id"]:
                await sendMessage("Restart!", channel)
                await restartServer()
        
        if content == "!dc c":
            l = getLastCommitInfo()
            res = l[0]
            com = l[1]
            await sendMessage("**LAST COMMIT INFO:**\n```" + res + "```", channel)
            await sendMessage(settings.js["github_repo"] + "/commit/" + com, channel)

        if content == "!dc run":
            if author in vm.user_assosiations:
                await sendMessage("**You are already running a code!**")
                return

            lcontent = getLastMessageContent(author) # Contains the content of the raw message
            codemodule = getCodeModule(lcontent)
            
            if codemodule == None:
                await sendMessage("This code is not valid or there is no language specified")
                return
            
            # Now we know that we should run cpp for example,
            # let's start a instance of a vm for the user and run the module,
            # but first let's format his code

            formatCode(msg, lcontent)

            # Now let's create the vm

            vm.setUserToDcChannel(author, channel)
            vm_index = vm.assignVm(author)

            # Check if that ran successfully

            if vm_index == -1:
                await sendMessage("Sorry, there are no VMs free right now. Maybe the bot is oversaturated", channel)
                return
            
            # Instance the class!
            #TODO: GET CODE WITHOUT PREFIX
            run = eval("languages." + codemodule)(vm_index)
            await run.run(getRawCode(lcontent), self, author, channel)

            # Now remove the author
            vm.removeVm(author)

            vm.freeUserFromDcChannel(author)

    async def on_ready(self):
        """
        Executes when the bot starts
        """

        print('Logged in!')

        # Set custom status
        await self.change_presence(activity=discord.Game(name="Code"))

def discordTrim(text):
    if len(text) < 1994:
        return "```" + text + "```"
    msgFinal = "\n... and many more"
    return "```" + text[:(1990 - len(msgFinal))] + msgFinal + "```"

# Main function
if __name__ == "__main__":
    discode = Discode()
