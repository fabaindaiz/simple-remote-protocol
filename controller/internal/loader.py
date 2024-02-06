import asyncio

from internal.connection import WiznetConnection
import internal.filesystem as filesystem
import internal.recovery as recovery


def main():
    try:
        connection = WiznetConnection()
        connection.connect()

        print("Starting controller...")
        filesystem.remount()

        root = filesystem.rootspace()
        asyncio.create_task(root(connection))
        print("Firmware loaded!")

        user = filesystem.userspace()
        asyncio.create_task(user(connection))
        print("Entrypoint loaded!")

        print("Controller started successfully!\n")
        asyncio.run(connection.supervisor())

    except Exception as exception:
        print("Exception:", exception)
        recovery.system_recovery()
