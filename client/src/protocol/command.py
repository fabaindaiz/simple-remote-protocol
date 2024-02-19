from src.connection.base import Handler
from src.protocol.encode import Encoder


class Command:

    @staticmethod
    def update(space: bytes, build: bytes):
        def wrapper(handler: Handler):
            command = b"upload "
            content = Encoder.encode_files(space, build)
            print("Uploading files...")
            data = command + content

            handler.send(data)
            response = handler.receive()
            print(response.decode())
        return wrapper
    
    @staticmethod
    def shell(loop: bool = True):
        def wrapper(handler: Handler):
            while loop:
                command = input("> ")
                if command == "exit":
                    break
                elif command.startswith("upload"):
                    try:
                        _, space, build = command.split(" ", 2)
                        Command.update(space.encode(), build.encode())(handler)
                    except Exception as e:
                        print(f"Upload command failed with error:\n{e}")
                else:
                    handler.send(command.encode())
                    response = handler.receive()
                    print(response.decode())
        return wrapper
