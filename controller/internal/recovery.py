from internal.filesystem import change_rootspace


def system_recovery():
    print("\nFirmware recovery mode activated.")

    try:
        change_rootspace("main")
    except:
        print("Critical exception: firmware recovery failed.")
        print("If you are connected via USB, please disconnect and try again.")
