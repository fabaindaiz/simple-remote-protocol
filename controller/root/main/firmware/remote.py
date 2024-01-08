import asyncio
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket

from firmware.command import Command
from firmware.handler import SocketHandler


class Remote:

    def __init__(self, connection):
        self.ethernet = connection.ethernet
        self.command = None

    def set_command(self, command: Command):
        self.command = command

    async def updater(self):
        socket.set_interface(self.ethernet)
        server = socket.socket()

        server.bind((None, 8080))
        server.setblocking(False)
        server.settimeout(0.05)
        server.listen(1)

        print("Socket listening en 8080")

        while True:
            try:
                client, address = server.accept()
                print("Conexión desde", address)

                handler = SocketHandler(client, address)
                self.command.process(handler)

            except TimeoutError:
                await asyncio.sleep(0.01)
