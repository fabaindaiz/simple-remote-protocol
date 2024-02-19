from src.protocol.client import Client
from src.protocol.mapper import CommandMapper
from src.protocol.manager import ShellManager

import src.routers.update as update
import src.routers.system as system

HOST = ("192.168.1.220", 8080)


if __name__ == "__main__":
    command = CommandMapper()
    command.add_router(system.router)
    command.add_router(update.router)

    manager = ShellManager(command)
    
    client = Client(manager)
    client.start(HOST)
