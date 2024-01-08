import storage
import supervisor
import sys

with open("root/boot", "r") as file:
    ROOT = f"root/{file.read()}"

with open("user/boot", "r") as file:
    USER = f"user/{file.read()}"


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
    with open("root/boot", "w") as file:
        file.write(path)
    supervisor.reload()

def change_userspace(path: str):
    with open("user/boot", "w") as file:
        file.write(path)
    supervisor.reload()
