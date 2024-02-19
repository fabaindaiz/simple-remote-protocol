import socket

from src.connection.base import Handler, ConnectionError
from src.connection.secure import SecureHandler
from src.connection.socket import SocketHandler
from src.protocol.auth import Authentication
from src.protocol.base import CommandError, ProtocolError


class Manager:

    def process(self, handler: Handler):
        raise NotImplementedError


class Client:

    def __init__(self, manager: Manager):
        self.manager = manager

    def start(self, host: tuple):
        try:
            auth = Authentication.password_prompt()
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(host)

            handler: Handler
            handler = SocketHandler(client, host)
            handler = SecureHandler(handler)
            auth.autenticate(handler)
            print("Connection established")

            self.loop(handler)
        
        except ConnectionError as e:
            handler.missing_message()
            print(f"Connection error: {e}")
        except ProtocolError as e:
            print(f"Connection error: {e}")
        finally:
            handler.send(b"exit")

    def loop(self, client: Handler):
        while True:
            try:
                self.manager.process(client)
            
            except CommandError as e:
                print(f"Command error: {e}")
