import safebox.vm as vm
import safebox.cmd_utils as box
import asyncio

class Base:
    def __init__(self, vm_index):
        self.vm_index = vm_index
        self._recordStart = -1
        self._recordEnd = -1
    
    async def run(self, code, discode):
        # Run the code!
        pass

    async def wait(self, i):
        await asyncio.sleep(i)

    def enterChroot(self):
        box.executeScreen(str(self.vm_index), "sudo chroot --userspec=dragoconda root" + str(self.vm_index))
    
    def execute(self, code):
        box.execute(code)
    
    def vmExecute(self, code):
        box.executeScreen(str(self.vm_index), code)
    
    def getCompleteLog(self):
        return box.getScreenLog(str(self.vm_index))
    
    def startRecording(self):
        _recordStart = len(self.getCompleteLog())
    
    def stopRecording(self):
        _recordEnd = len(self.getCompleteLog())
    
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

    
