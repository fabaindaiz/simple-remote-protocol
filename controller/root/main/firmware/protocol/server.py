import asyncio
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket

from internal.connection import WiznetConnection
from firmware.protocol.mapper import CommandMapper
from firmware.protocol.sesion import RemoteSession


class RemoteServer:

    def __init__(self, connection: WiznetConnection, command: CommandMapper):
        self.connection = connection
        self.command = command
    
    async def start(self, host: tuple = (None, 8080), listen: int = 1):
        socket.set_interface(self.connection.ethernet)
        self.socket = socket.socket()

        self.socket.bind(host)
        self.socket.setblocking(False)
        self.socket.settimeout(0.05)
        self.socket.listen(listen)
        print("Socket listening en 8080")

    async def loop(self):
        while True:
            try:
                client, address = self.socket.accept()
                print("Connection from", address)

                sesion = RemoteSession(self.command)
                asyncio.create_task(sesion.start(client, address))
            
            except TimeoutError:
                await asyncio.sleep(0.01)
