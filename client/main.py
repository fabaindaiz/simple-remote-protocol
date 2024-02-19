from src.protocol.client import Client
from src.protocol.command import Command

SPACE = b"user"
BUILD = b"main2"
HOST = ("192.168.1.220", 8080)


if __name__ == "__main__":
    client = Client.connect(HOST)

    #command = Command.update(SPACE, BUILD)
    command = Command.shell()

    client.command(command)
