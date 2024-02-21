import storage
import supervisor
import sys

from internal.memory import MEMORY, NVMDir


with MEMORY as memory:
    root = memory[NVMDir.ROOT].decode()
    user = memory[NVMDir.USER].decode()

ROOT = f"root/{root}"
USER = f"user/{user}"


def remount():
    try:
        storage.remount("/", readonly=False)
    except:
        print("Cannot remount filesystem when visible via USB.")
        print("You can ignore this message if you are developing.")

def rootspace():
    sys.path.append(ROOT)
    import firmware
    return firmware.main

def userspace():
    sys.path.append(USER)
    import entrypoint
    return entrypoint.main

def change_rootspace(path: str):
    with MEMORY as memory:
        memory[NVMDir.ROOT.value] = path.encode()
    supervisor.reload()

def change_userspace(path: str):
    with MEMORY as memory:
        memory[NVMDir.USER.value] = path.encode()
    supervisor.reload()
