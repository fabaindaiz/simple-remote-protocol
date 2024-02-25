import storage
import supervisor
import sys
from internal.memory import NVMController, NVM
from internal.utils import Singleton


with NVMController() as memory:
    ROOT = f"root/{memory[NVM.ROOT].decode()}"
    USER = f"user/{memory[NVM.USER].decode()}"

class Filesystem(Singleton):

    @staticmethod
    def remount():
        try:
            storage.remount("/", readonly=False)
        except:
            print("Cannot remount filesystem when visible via USB.")
            print("You can ignore this message if you are developing.")

    @property
    def root(self):
        sys.path.append(ROOT)
        import firmware
        return firmware.main
    
    @property
    def user(self):
        sys.path.append(USER)
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
