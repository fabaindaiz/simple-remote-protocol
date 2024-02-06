import socket

from src.connection.base import Handler, SEP
from src.connection.socket import SocketHandler
from src.connection.secure import SecureHandler
from src.protocol.encode import Encoder

HOST = ("192.168.1.220", 8080)


def connection(auth: str):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(HOST)

    socket = SocketHandler(client, HOST)
    client = SecureHandler(socket)

    client.send(auth.encode())
    response = client.receive()
    print("Respuesta recibida:", response.decode())

    return client

def update_request(client: Handler, build: str):
    try:
        command = b"UPLOAD"
        content = Encoder.encode_files(build)
        data = command + SEP + content

        client.send(data)
        response = client.receive()
        print("Respuesta recibida:", response.decode())

    finally:
        client.close()

if __name__ == '__main__':
    auth = input("Ingrese la clave: ")
    client = connection(auth)

    build = "main2"
    update_request(client, build)
