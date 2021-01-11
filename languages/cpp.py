class Cpp:
    async def run(self, code, discode, author, channel):
        self.saveFile(code, "home/main.cc")

        self.enterChroot()

        self.startRecording()
        self.vmExecute("cd home && g++ main.cc -o main && ./main")
        self.stopRecording()

        log = self.getLog()

        self.destroySession()

        await self.wait(4)
        
        await discode.sendMessage(log, channel)