import asyncio

from internal.connection import WiznetConnection
from firmware.protocol.mapper import CommandMapper
from firmware.protocol.server import Server

import firmware.routers.storage as storage
import firmware.routers.system as system
import firmware.routers.update as update


command = CommandMapper()
command.add_router(storage.router)
command.add_router(system.router)
command.add_router(update.router)


async def main(connection: WiznetConnection):
    server = Server(connection, command)

    while True:
        await server.loop()
        await asyncio.sleep(1)
