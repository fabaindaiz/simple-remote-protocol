import sys
from internal.memory import MEMORY, NVMDir

with MEMORY as memory:
    root = memory[NVMDir.ROOT].decode()
ROOT = f"root/{root}"

def rootspace():
    sys.path.append(ROOT)
    import firmware
    return firmware.main
