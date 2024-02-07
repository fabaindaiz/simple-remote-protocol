import asyncio
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket

from internal.connection import WiznetConnection
from firmware.connection.secure import SecureHandler, SecurityException
from firmware.connection.socket import SocketHandler
from firmware.protocol.auth import Auth
from firmware.protocol.command import Command, SessionEnd


class Updater:

    def __init__(self, connection: WiznetConnection, command: Command):
        self.connection = connection
        self.command = command
    
    def start(self, host: tuple = (None, 8080), blocking: bool = False, listen: int = 1):
        socket.set_interface(self.connection.ethernet)
        self.server = socket.socket()

        self.server.bind(host)
        self.server.setblocking(blocking)
        self.server.settimeout(0.05)
        self.server.listen(listen)
        print("Socket listening en 8080")

    async def loop(self):
        while True:
            try:
                socket, address = self.server.accept()
                print("Connection from", address)

                asyncio.create_task(self.process(socket, address))
            
            except TimeoutError:
                await asyncio.sleep(0.01)
    
    async def process(self, connection, address):
        try:
            try:
                socket = SocketHandler(connection, address)
                client = SecureHandler(socket)
                print("Secure connection established")

                authkey = client.receive()
                if Auth.check(authkey):
                    client.send(b"AUTH OK")
                    print("Authentification success")
                else:
                    client.send(b"AUTH ERROR")
                    raise SecurityException("Invalid authkey")
                
                self.command.process(client)
            
            except SessionEnd:
                print("Connection closed: Session ended")
            except SecurityException as e:
                print("Connection closed:", e)
            finally:
                client.close()
        
        except RuntimeError:
            print("Connection closed: Client disconnected")
        