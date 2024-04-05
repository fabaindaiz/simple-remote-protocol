import asyncio
from internal.network import NetworkLoader
from .protocol.mapper import CommandMapper
from .protocol.server import RemoteServer
from .routers import storage
from .routers import system
from .routers import update

command = CommandMapper()
command.add_router(storage.router)
command.add_router(system.router)
command.add_router(update.router)

connection = NetworkLoader().network
server = RemoteServer(connection, command)

async def main(): 
    await server.start()

    while True:
        await server.loop()
        await asyncio.sleep(1)
