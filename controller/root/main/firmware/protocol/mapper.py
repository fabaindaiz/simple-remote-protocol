from firmware.connection.base import SEP, Handler
from firmware.protocol.base import Context, CommandError


class Router:

    def __init__(self) -> None:
        self.commands = {}

    def register(self, command: bytes):
        def wrapper(func):
            if command in self.commands:
                raise ValueError(f"Command {command} already exists")
            self.commands[command] = func
            return func
        return wrapper


class CommandMapper:

    def __init__(self) -> None:
        self.commands = {}

    def register(self, command: bytes):
        def wrapper(func):
            if command in self.commands:
                raise ValueError(f"Command {command} already exists")
            self.commands[command] = func
            return func
        return wrapper
    
    def add_router(self, router: Router):
        for command, function in router.commands.items():
            self.register(command)(function)

    def process(self, client: Handler, context: Context):
        data = client.receive()
        args = data.split(b" ")

        if len(args) == 1:
            command = data
            content = b""
        else:
            command, content = data.split(b" ", 1)
        
        if command not in self.commands:
            raise CommandError(f"Command {command.decode()} not found")

        func = self.commands.get(command)
        func(client, command, content)
