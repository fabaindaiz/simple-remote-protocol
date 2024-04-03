import storage
import supervisor
import sys
from internal.base import Singleton
from internal.service.memory import NVMController, NVM

class StorageController(Singleton):
    @Singleton.init
    def __init__(self) -> None:
        with NVMController() as memory:
            self.root = f"root/{memory[NVM.ROOT].decode()}"
            self.user = f"user/{memory[NVM.USER].decode()}"
        self.remount()

    @staticmethod
    def remount():
        try:
            storage.remount("/", readonly=False)
        except:
            print("Cannot remount filesystem when visible via USB.")
            print("You can ignore this message if you are developing.")

    @property
    def root(self):
        sys.path.append(self.root)
        import firmware
        return firmware.main

    @property
    def user(self):
        sys.path.append(self.user)
        import entrypoint
        return entrypoint.main
    
    @root.setter
    def root(path: str):
        with NVMController() as memory:
            memory[NVM.ROOT] = path.encode()
        supervisor.reload()

    @user.setter
    def user(path: str):
        with NVMController() as memory:
            memory[NVM.USER] = path.encode()
        supervisor.reload()
