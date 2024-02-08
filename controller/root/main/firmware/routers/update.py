import os
import zlib

from internal.filesystem import change_rootspace, change_userspace
from firmware.connection.base import SEP, Handler
from firmware.protocol.base import CommandError, response
from firmware.protocol.mapper import Router


router = Router()

@router.register(b"rootspace")
def rootspace(client: Handler, command: bytes, args: list[bytes]):
    if len(args) == 1:
        inst = args[0]
        if inst == b"list":
            folders = os.listdir("/root")
            client.send(b" ".join(folders))
        else:
            raise CommandError("Invalid rootspace command")
    
    elif len(args) == 2:
        inst, path = args
        if inst == b"change":
            change_rootspace(path.decode())
            client.send(b"rootspace changed")
        elif inst == b"delete":
            if path in os.listdir("/root") and path not in ["boot", "main"]:
                os.rmdir(f"/root/{path}")
                client.send(b"rootspace deleted")
            else:
                client.send(b"rootspace not found")
        else:
            raise CommandError("Invalid rootspace command")
    else:
        raise CommandError("Invalid rootspace command")

@router.register(b"userspace")
def userspace(client: Handler, command: bytes, args: list[bytes]):
    if len(args) == 1:
        inst = args[0]
        if inst == b"list":
            folders = os.listdir("/user")
            client.send(b" ".join(folders))
        else:
            raise CommandError("Invalid userspace command")
    
    elif len(args) == 2:
        inst, path = args
        if inst == b"change":
            change_userspace(path.decode())
            client.send(b"userspace changed")
        if inst == b"delete":
            if path in os.listdir("/user") and path not in ["boot", "main"]:
                os.rmdir(f"/user/{path}")
                client.send(b"userspace deleted")
            else:
                client.send(b"userspace not found")
        else:
            raise CommandError("Invalid userspace command")
    
    else:
        raise CommandError("Invalid userspace command")

@router.register(b"upload")
def upload(client: Handler, command: bytes, args: list[bytes]):
    if len(args) == 3:
        space, build, content = args
        files = content.split(SEP)

        if not space in [b"root", b"user"]:
            raise CommandError("Invalid file format")

        for file in files:
            decoded = FileData.decode_files(file)
            decoded.save_file(space)
        
        client.send(b"files uploaded")
    else:
        raise CommandError("Invalid parameters")


class FileData:

    def __init__(self, path: bytes, name: bytes, content: bytes):
        self.path = path.decode()
        self.name = name.decode()
        self.content = content

    @staticmethod
    def decode_files(file: bytes):
        try:
            data = bytes(zlib.decompress(file))
            path, name, content = data.split(b"\r\n", 2)
            return FileData(path, name, content)
        except Exception as e:
            raise CommandError("Invalid file format")

    def save_file(self, space: str):
        try:
            with open(f"/{space}/{self.name}", "wb") as file:
                file.write(self.content)
        except Exception as e:
            print(e)
        print("file", self.name, len(self.content))
