import asyncio
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket

from internal.connection import WiznetConnection
from firmware.command.executor import CommandExecutor
from firmware.protocol.sesion import Sesion


class Server:

    def __init__(self, connection: WiznetConnection, command: CommandExecutor):
        self.connection = connection
        self.command = command
    
    def start(self, host: tuple = (None, 8080), listen: int = 1):
        socket.set_interface(self.connection.ethernet)
        self.server = socket.socket()

        self.server.bind(host)
        self.server.setblocking(False)
        self.server.settimeout(0.05)
        self.server.listen(listen)
        print("Socket listening en 8080")

    async def loop(self):
        while True:
            try:
                socket, address = self.server.accept()
                print("Connection from", address)

                sesion = Sesion(self.command)
                asyncio.create_task(sesion.start(socket, address))
            
            except TimeoutError:
                await asyncio.sleep(0.01)
