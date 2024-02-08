import os
import asyncio

from firmware.connection.base import Handler, ConnectionError
from firmware.connection.secure import SecureHandler
from firmware.connection.socket import SocketHandler
from firmware.protocol.auth import Authentication
from firmware.protocol.base import Context, ProtocolError, CommandError, response
from firmware.protocol.mapper import CommandMapper


class RemoteSession:

    def __init__(self, command: CommandMapper):
        self.command = command

    async def start(self, client, address):
        client.settimeout(5)

        try:
            try:
                socket = SocketHandler(client, address)
                secure = SecureHandler(socket)
                print("Secure connection established")

                context = Authentication.authenticate(secure)
                print("Authentification success")
                
                await self.loop(secure, context)
            
            except ConnectionError as e:
                response(secure, f"Connection error: {e}")
            except ProtocolError as e:
                response(secure, f"Connection error: {e}")
            finally:
                client.close()

        except RuntimeError:
            print("Connection closed: Client disconnected")
        except TimeoutError:
            print("Connection closed: Session start timeout")
    
    async def loop(self, client: Handler, context: Context):
        client.settimeout(0.1)
        os.chdir("/")

        while True:
            try:
                self.command.process(client, context)
            
            except CommandError as e:
                response(client, f"Command error: {e}")
            except TimeoutError:
                await asyncio.sleep(0.5)
