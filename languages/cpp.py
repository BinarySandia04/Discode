from .base import Base

class Cpp(Base):
    async def run(self, code, discode, author, channel):
        self.saveFile(code, "home/main.cc")

        self.enterChroot()

        self.vmExecute("cd home && g++ main.cc -o main && ./main")
        
        await discode.sendMessage("Running...", channel)

        print(self.startRecording())
        await self.wait(5)
        print(self.stopRecording())

        log = self.getLog()
     
        print(len(log))
        
        await discode.sendMessage("**CODE OUTPUT:**", channel)
        await discode.sendMessage("```" + log + "```", channel)

        self.destroySession()
