import socket

from src.connection.base import Handler
from src.connection.secure import SecureHandler
from src.connection.socket import SocketHandler
from src.protocol.auth import Authentication
from src.protocol.command import Command


class Client:

    def __init__(self, handler: Handler):
        self.handler = handler

    @staticmethod
    def connect(host: tuple) -> "Client":
        auth = Authentication.password_prompt()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(host)
        print("Connection to", host)

        handler: Handler
        handler = SocketHandler(client, host)
        handler = SecureHandler(handler)
        auth.autenticate(handler)
        print("Connection established")

        return Client(handler)

    def command(self, command: Command):
        try:
            command(self.handler)
        finally:
            self.handler.send(b"exit")
            print("Connection closed")
