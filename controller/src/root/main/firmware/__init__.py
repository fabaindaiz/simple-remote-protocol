import asyncio
from internal.network.w5x00 import W5x00Controller
from firmware.protocol.mapper import CommandMapper
from firmware.protocol.server import RemoteServer
import firmware.routers.storage as storage
import firmware.routers.system as system
import firmware.routers.update as update


command = CommandMapper()
command.add_router(storage.router)
command.add_router(system.router)
command.add_router(update.router)

config = ((192, 168, 100, 120), (255, 255, 255, 0), (192, 168, 100, 1), (8, 8, 8, 8))
connection = W5x00Controller()
connection.connect(config)
server = RemoteServer(connection, command)

async def main(): 
    await server.start()

    while True:
        await server.loop()
        await asyncio.sleep(1)
