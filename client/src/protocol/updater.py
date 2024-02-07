import socket

from src.connection.base import Handler, SEP
from src.connection.socket import SocketHandler
from src.connection.secure import SecureHandler
from src.protocol.encode import Encoder


def connection(host: tuple, auth: str):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(host)

    client = SocketHandler(client, host)
    client = SecureHandler(client)
    print("Secure connection established")

    client.send(auth.encode())
    if client.receive() != b"AUTH OK":
        raise ValueError("Invalid authentication")
    print("Authentication successful")

    return client

def update_request(client: Handler, build: str):
    try:
        command = b"UPLOAD"
        content = Encoder.encode_files(build)
        data = command + SEP + content

        client.send(data)
        response = client.receive()
        if response != b"UPLOAD OK":
            raise ValueError("Upload failed")
        print("Upload successful")
    
    finally:
        client.close()
