import storage
import supervisor
import usb_cdc

from internal.memory import MEMORY, NVMDir


def secure_mode():
    try:
        with open("internal/secure", "r") as file:
            storage.disable_usb_drive()
            usb_cdc.disable()
    except:
        print("Secure mode disabled. USB drive access allowed.")

def system_recovery(exception: Exception):
    print("Exception:", exception.with_traceback())
    print("\nFirmware recovery mode activated.")

    try:
        with MEMORY as memory:
            memory[NVMDir.CONFIG] = b"main.json"
            memory[NVMDir.ROOT] = b"main"
            memory[NVMDir.USER] = b"test"
        supervisor.reload()
    except:
        print("Critical exception: firmware recovery failed.")
