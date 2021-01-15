from .base import Base

class Cpp(Base):
    async def run(self, code, author, channel):
        self.saveFile(code, "home/main.cc")

        self.enterChroot()

        self.vmExecute("cd home && g++ main.cc -o main")

        await self.discode.sendMessage("Compiling...", channel)
        while self.isScreenExecuting():
            await self.wait(0.05)
        
        self.discode.sendMessage("Compiled!", channel)
        self.vmExecute("./main")
        
        await self.discode.sendMessage("**Running...**", channel)

        firstLine = len(self.getCompleteLog().split("\n"))
        
        await self.wait(0.1)

        while self.isScreenExecuting():
            if author in self.discode.messageHistory:
                while len(self.discode.messageHistory[author]) > 0:
                    self.vmExecute(self.discode.messageHistory[author][0])
                    self.discode.messageHistory[author].pop(0)

            await self.wait(0.1)

            completeLog = self.getCompleteLog()
            
            currentLine = len(completeLog.split("\n"))

            log = "\n".join(completeLog.split("\n")[firstLine:currentLine-1])
            
            firstLine = currentLine

            if len(log) != 0:
                await self.discode.sendMessage("```" + log + "```", channel)

        await self.discode.sendMessage("**End of the program**", channel)

        self.destroySession()
