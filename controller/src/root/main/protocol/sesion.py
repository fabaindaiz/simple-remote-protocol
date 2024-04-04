import asyncio
import gc
import os
from ..connection.base import Handler, ConnectionError
from ..connection.secure import SecureHandler
from ..connection.socket import SocketHandler
from ..protocol.auth import Authentication
from ..protocol.base import Context, CommandError, ProtocolError, response
from ..protocol.mapper import CommandMapper

class RemoteSession:
    def __init__(self, command: CommandMapper):
        self.command = command

    async def start(self, client, address):
        client.settimeout(5)

        try:
            try:
                handler: Handler
                handler = SocketHandler(client, address)
                handler = SecureHandler(handler)
                context = Authentication.authenticate(handler)
                print("Connection established")

                await self.loop(handler, context)
            
            except ConnectionError as e:
                handler.missing_message()
                response(handler, f"Connection error: {e}")
            except ProtocolError as e:
                response(handler, f"Connection error: {e}")
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
                gc.collect()
                await asyncio.sleep(0.5)
