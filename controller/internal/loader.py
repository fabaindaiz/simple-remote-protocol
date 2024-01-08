import asyncio

from internal.connection import Connection
from internal.recovery import system_recovery
from internal.filesystem import remount, rootspace, userspace


def main():
    try:
        connection = Connection()
        connection.connect()

        print("Starting controller...")
        remount()

        root = rootspace()
        asyncio.create_task(root(connection))
        print("Firmware loaded!")

        user = userspace()
        asyncio.create_task(user(connection))
        print("Entrypoint loaded!")

        print("Controller started successfully!\n")
        asyncio.run(connection.supervisor())

    except Exception as exception:
        print("Exception:", exception)
        system_recovery()
