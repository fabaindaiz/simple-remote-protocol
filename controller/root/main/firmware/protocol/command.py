from firmware.connection.base import Handler, SEP


class Command:

    def __init__(self) -> None:
        self.commands = {}

    def register(self, command: bytes):
        def wrapper(func):
            if command in self.commands:
                raise ValueError(f"Command {command} already exists")
            self.commands[command] = func
            return func
        return wrapper
    
    def process(self, client: Handler):
        data = client.receive()
        command, content = data.split(SEP, 1)
        
        func = self.commands.get(command, not_found)
        func(client, command, content)


def not_found(client: Handler, command: bytes, content: bytes):
    print(f"Command {command.decode()} not found")
    client.send(b"Command not found")
