from src.connection.base import Handler
from src.protocol.base import ResolveError


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

    def process(self, client: Handler, data: str):
        if " " in data:
            command, content = data.split(" ", 1)
        else:
            command = data
            content = b""
        
        if command not in self.commands:
            raise ResolveError

        func = self.commands.get(command)
        func(client, command, content)


def split_args(data: str):
    if data == "":
        return []
    return data.split(" ")
