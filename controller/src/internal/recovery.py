import storage
import supervisor
import usb_cdc
from internal.memory import NVMController, NVM

def secure_mode():
    try:
        with open("internal/secure", "r") as file:
            storage.disable_usb_drive()
            usb_cdc.disable()
    except:
        print("Secure mode disabled. USB drive access allowed.")

def system_recovery(exception: Exception):
    print("Exception:", exception)
    print("\nFirmware recovery mode activated.")

    with NVMController() as memory:
        memory[NVM.ROOT] = b"main"
        memory[NVM.USER] = b"test"
    supervisor.reload()
