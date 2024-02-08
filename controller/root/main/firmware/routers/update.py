import os
import zlib

from internal.filesystem import change_rootspace, change_userspace
from firmware.connection.base import Handler, SEP
from firmware.protocol.base import ProtocolError
from firmware.protocol.mapper import Router


router = Router()

@router.register(b"rootspace")
def rootspace(client: Handler, command: bytes, data: bytes):
    args = data.split(SEP)
    if len(args) == 1:
        inst = args[0]
        if inst == b"list":
            folders = os.listdir("/root")
            client.send(b" ".join(folders))
    elif len(args) == 2:
        inst, path = args
        if inst == b"change":
            change_rootspace(path.decode())
            client.send(b"ROOTSPACE CHANGED")
        if inst == b"delete":
            if path in os.listdir("/root") and path not in ["boot", "main"]:
                os.rmdir(f"/root/{path}")
                client.send(b"ROOTSPACE DELETED")
            else:
                client.send(b"ROOTSPACE NOT FOUND")
    else:
        raise ProtocolError("Invalid ROOTSPACE command")

@router.register(b"userspace")
def userspace(client: Handler, command: bytes, data: bytes):
    args = data.split(SEP)
    if len(args) == 1:
        inst = args[0]
        if inst == b"list":
            folders = os.listdir("/user")
            client.send(b" ".join(folders))
    elif len(args) == 2:
        inst, path = args
        if inst == b"change":
            change_userspace(path.decode())
            client.send(b"USERSPACE CHANGED")
        if inst == b"delete":
            if path in os.listdir("/user") and path not in ["boot", "main"]:
                os.rmdir(f"/user/{path}")
                client.send(b"USERSPACE DELETED")
            else:
                client.send(b"USERSPACE NOT FOUND")
    else:
        raise ProtocolError("Invalid USERSPACE command")

@router.register(b"upload")
def upload(client: Handler, command: bytes, data: bytes):
    folder, content = data.split(SEP, 1)
    files = content.split(SEP)
    for file in files:
        decoded = FileData.decode_files(folder, file)
        decoded.save_file()
    
    client.send(b"OK")


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
        print("FILE", self.path, self.name, len(self.content))
