import storage
from internal.base import Singleton
from internal.memory import NVMController, NVM

class StorageController(Singleton):
    @Singleton.init
    def __init__(self) -> None:
        with NVMController() as memory:
            self.ROOT = f"root/{memory[NVM.ROOT].decode()}"
            self.USER = f"user/{memory[NVM.USER].decode()}"
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
        return __import__(self.ROOT)
    
    @root.setter
    def root(path: str):
        with NVMController() as memory:
            memory[NVM.ROOT] = path.encode()

    @property
    def user(self):
        return __import__(self.USER)
    
    @user.setter
    def user(path: str):
        with NVMController() as memory:
            memory[NVM.USER] = path.encode()
