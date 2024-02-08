from getpass import getpass
import socket

from src.connection.base import SEP, Handler, SecurityError
from src.connection.secure import SecureHandler
from src.connection.socket import SocketHandler
from src.protocol.base import SessionError
from src.protocol.encode import Encoder


class Connection:
    
    @staticmethod
    def connect(host: tuple):
        password = getpass()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(host)
        print("Connection established")

        client = SocketHandler(client, host)
        client = SecureHandler(client)
        print("Secure connection established")

        client.send(password.encode())
        if client.receive() != b"AUTH OK":
            raise SecurityError("Invalid authentication")
        print("Authentication successful")

        return client


class Request:

    @staticmethod
    def update(client: Handler, space: str, build: str):
        try:
            command = b"upload "
            content = Encoder.encode_files(space, build)
            print("Uploading files...")
            data = command + content

            client.send(data)
            response = client.receive()
            print(response.decode())
        
        finally:
            client.send(b"exit")
            print("Connection closed")

    @staticmethod
    def shell(client: Handler):
        try:
            while True:
                command = input("> ")
                if command == "exit":
                    break
                client.send(command.encode())
                response = client.receive().decode()
                print(response)
        
        finally:
            client.send(b"exit")
            print("Connection closed")
