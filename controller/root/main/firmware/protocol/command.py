from firmware.protocol.auth import Auth
from firmware.network.handler import Handler

SEP = b"\r\n"


class Command:

    def __init__(self) -> None:
        self.commands = {}

    def process(self, client: Handler):
        data = client.receive()

        authkey, command, content = data.split(SEP, 2)
        if not Auth.check(authkey):
            print(f"Invalid authkey")
            client.send(b"Invalid authkey")
            client.close()
        
        func = self.commands.get(command)
        if not func:
            print(f"Command {command} not found")
            client.send(b"Command not found")
            client.close()
        
        func(client, content)

    def register(self, topic: bytes):
        def wrapper(func):
            if topic in self.commands:
                raise ValueError(f"Command {topic} already exists")
            self.commands[topic] = func
            return func
        return wrapper
