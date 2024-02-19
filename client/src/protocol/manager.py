from src.connection.base import Handler
from src.protocol.base import ResolveError, SessionError
from src.protocol.mapper import CommandMapper
from src.routers.update import Encoder


class Update:

    def __init__(self, space: str, build: str):
        self.space = space.encode()
        self.build = build.encode()

    def process(self, handler: Handler):
        command = b"update "
        content = Encoder.encode_files(self.space, self.build)
        data = command + content
        print("Uploading files...")

        handler.send(data)
        response = handler.receive()
        print(response.decode())
        raise SessionError("Manager closed connection")


class ShellManager:

    def __init__(self, command: CommandMapper) -> None:
        self.command = command

    def process(self, handler: Handler):
        while True:
            data = input("> ")
            try:
                self.command.process(handler, data)

            except ResolveError:
                handler.send(data.encode())
                response = handler.receive()
                print(response.decode())
