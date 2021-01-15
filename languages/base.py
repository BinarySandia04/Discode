import safebox.vm as vm
import safebox.cmd_utils as box
import asyncio
import settings

class Base:
    def __init__(self, vm_index, discode):
        self.vm_index = vm_index
        self._recordStart = -1
        self._recordEnd = -1
        self.discode = discode
    
    async def run(self, code, author, channel):
        # Run the code!
        pass

    async def wait(self, i):
        await asyncio.sleep(i)
    
    def enterChroot(self):
        box.executeScreen(str(self.vm_index), "sudo chroot --userspec=" + settings.js["chroot_username"] + " root" + str(self.vm_index))
    
    def execute(self, code):
        box.execute(code)
   
    def isScreenExecuting(self):
        return box.isScreenExecuting(self.vm_index)

    def vmExecute(self, code):
        box.executeScreen(str(self.vm_index), code)
    
    def getCompleteLog(self):
        return box.getScreenLog(str(self.vm_index))
    
    def startRecording(self):
        self._recordStart = len(self.getCompleteLog().split("\n"))
        return self._recordStart
    
    def stopRecording(self):
        self._recordEnd = len(self.getCompleteLog().split("\n"))
        return self._recordEnd
    
    def destroySession(self):
        box.destroyScreen(self.vm_index)
    
    def getLog(self):
        log = self.getCompleteLog().split("\n")
        res = ""
        for i in range(self._recordStart, self._recordEnd):
            res += log[i] + "\n"
        return res
    
    def saveFile(self, content, path):
        with open("root" + str(self.vm_index) + "/" + path, "w") as f:
            f.write(content)

    
