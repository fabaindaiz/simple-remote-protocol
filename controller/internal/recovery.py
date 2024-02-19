import storage
import supervisor
import usb_cdc


def secure_mode():
    try:
        with open("internal/secure", "r") as file:
            storage.disable_usb_drive()
            usb_cdc.disable()
    except:
        print("Secure mode disabled. USB drive access allowed.")

def system_recovery():
    print("\nFirmware recovery mode activated.")

    try:
        with open("root/boot", "w") as file:
            file.write("main")
        with open("user/boot", "w") as file:
            file.write("main")
        supervisor.reload()
    except:
        print("Critical exception: firmware recovery failed.")
        print("If you are connected via USB, please disconnect and try again.")
