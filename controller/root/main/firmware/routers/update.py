import os
import zlib

from internal.filesystem import change_rootspace, change_userspace
from firmware.connection.base import SEP, Handler
from firmware.protocol.base import CommandError, response
from firmware.protocol.mapper import Router


router = Router()

@router.register(b"rootspace")
def rootspace(client: Handler, command: bytes, data: bytes):
    args = data.split(b" ")
    if len(args) == 1:
        inst = args[0]
        if inst == b"list":
            folders = os.listdir("/root")
            client.send(b" ".join(folders))
        else:
            raise CommandError("Invalid rootspace command")
    
    elif len(args) == 2:
        inst, path = args
        if inst == b"upload":
            upload(client, command, path)
        elif inst == b"change":
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
def userspace(client: Handler, command: bytes, data: bytes):
    args = data.split(b" ")
    if len(args) == 1:
        inst = args[0]
        if inst == b"list":
            folders = os.listdir("/user")
            client.send(b" ".join(folders))
        else:
            raise CommandError("Invalid userspace command")
    
    elif len(args) == 2:
        inst, path = args
        if inst == b"upload":
            upload(client, command, path)
        elif inst == b"change":
            change_userspace(path.decode())
            client.send(b"userspace changed")
        elif inst == b"delete":
            if path in os.listdir("/user") and path not in ["boot", "main"]:
                os.rmdir(f"/user/{path}")
                client.send(b"userspace deleted")
            else:
                client.send(b"userspace not found")
        else:
            raise CommandError("Invalid userspace command")
    
    else:
        raise CommandError("Invalid userspace command")


def upload(client: Handler, command: bytes, data: bytes):
    try:
        folder, content = data.split(SEP, 1)
        files = content.split(SEP)

        for file in files:
            decoded = FileData.decode_files(folder, file)
            decoded.save_file()
        
        client.send(b"files uploaded")
    except:
        raise CommandError("upload bad format")


class FileData:

    def __init__(self, name: bytes, path: bytes, content: bytes):
        self.name = name.decode()
        self.path = path.decode()
        self.content = content

    @staticmethod
    def decode_files(path: bytes, file: bytes):
        data = bytes(zlib.decompress(file))
        name, content = data.split(b"\r\n", 1)
        return FileData(name, path, content)

    def save_file(self):
        try:
            with open(f"{self.path}/{self.name}", "wb") as file:
                file.write(self.content)
        except:
            pass
        print("file", self.path, self.name, len(self.content))
