# File for vm management
import os
import settings
from safebox.cmd_utils import execute, createScreen, destroyScreen, getPath

class VMmanager:
    
    vm_assosiations = {}
    user_assosiations = {}
    channel_assosiations = {}
    
    def __init__(self, max_vm_number, mount_dir_info, other_dirs):
        self.destroyAllScreens()

        self.max_vm = max_vm_number
        self.mount_dirs = mount_dir_info
        self.other_dirs = other_dirs
        
    # Fixa un usuari a un discord channel
    def setUserToDcChannel(self, user, channel):
        self.channel_assosiations[user] = channel

    def freeUserFromDcChannel(self, user):
        self.channel_assosiations.pop(user, None)
    
    # Assigna una screen i una VM a un usuari
    def assignVm(self, user):
        # Busquem en totes les vm i ens quedem amb la primera None
        if len(self.vm_assosiations) >= self.max_vm:
            return -1
        for i in range(len(self.vm_assosiations) + 1):
            if not i in self.vm_assosiations:
                self.createVm(str(i))
                createScreen(str(i))

                self.vm_assosiations[i] = user
                self.user_assosiations[user] = i

                return i
        return -1
    

    def createVm(self, n):
        vmPath = getPath() + 'root' + str(n)
        self.destroyVm(n)
        execute('mkdir ' + vmPath)
        for d in self.mount_dirs.keys():
            execute('mkdir ' + vmPath + "/" + d)
            execute("sudo mount --bind " + self.mount_dirs[d] + " " + vmPath + "/" + d)
        for d in self.other_dirs:
            execute('mkdir ' + vmPath + "/" + d)
            execute('sudo chown ' + settings.js["chroot_username"] + ' ' + vmPath + "/" + d)
            execute('sudo chmod ug=rwx ' + vmPath +"/" + d)

    # Borra la VM i la screen a un usuari
    def removeVm(self, user):
        if user in self.user_assosiations:
            i = self.user_assosiations[user]
            destroyScreen(str(i))
            self.destroyVm(str(i))

            self.vm_assosiations.pop(i, None)
            self.user_assosiations.pop(user, None)
    
    def destroyAllScreens(self):
        execute("screen -ls | grep '" + settings.js["screen_prefix"] + "' | awk '{print $1}' | xargs -I % -t screen -X -S % quit")

    def destroyVm(self, n):
        vmPath = getPath() + 'root' + str(n)
        if os.path.isdir(vmPath):
            # Umount and remove
            for d in settings.js["mount_dirs"].keys():
                execute('sudo umount ' + vmPath + "/" + d)
            execute('sudo rm -R ' + vmPath)

    
