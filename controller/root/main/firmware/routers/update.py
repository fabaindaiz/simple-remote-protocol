import os
import zlib

from internal.filesystem import change_rootspace, change_userspace
from firmware.connection.base import SEP, Handler
from firmware.protocol.base import CommandError, handleException
from firmware.protocol.mapper import Router


router = Router()

@router.register(b"rootspace")
@handleException(OSError, CommandError)
def rootspace(client: Handler, command: bytes, data: bytes):
    args = Router.split_args(data)
    if len(args) == 1:
        inst = args[0]
        if inst == b"list":
            folders = [folder.encode() for folder in os.listdir("/root") if folder != "boot"]
            client.send(b" ".join(folders))
            return
    
    elif len(args) == 2:
        inst, path = args
        space = path.decode()
        if inst == b"change":
            if space in os.listdir("/root") and space not in ["boot"]:
                change_rootspace(space)
                client.send(b"rootspace changed")
                return

        elif inst == b"delete":
            if path in os.listdir("/root") and path not in ["boot", "main"]:
                os.rmdir(f"/root/{path}")
                client.send(b"Rootspace deleted")
                return

    raise CommandError("Invalid rootspace command")

@router.register(b"userspace")
@handleException(OSError, CommandError)
def userspace(client: Handler, command: bytes, data: bytes):
    args = Router.split_args(data)
    if len(args) == 1:
        inst = args[0]
        if inst == b"list":
            folders = [folder.encode() for folder in os.listdir("/user") if folder != "boot"]
            client.send(b" ".join(folders))
            return
    
    elif len(args) == 2:
        inst, path = args
        space = path.decode()
        if inst == b"change":
            if space in os.listdir("/user") and space not in ["boot"]:
                change_userspace(space)
                client.send(b"Userspace changed")
                return

        if inst == b"delete":
            if space in os.listdir("/user") and space not in ["boot", "main"]:
                os.rmdir(f"/user/{path}")
                client.send(b"Userspace deleted")
                return
    
    raise CommandError("Invalid userspace command")

@router.register(b"update")
def update(client: Handler, command: bytes, data: bytes):
    space, build, content = data.split(SEP, 2)

    if not space in [b"root", b"user"]:
        raise CommandError("Not a valid space")
    if build.decode() in os.listdir(f"/{space.decode()}"):
        raise CommandError("Build already exists")
    print("uploading files to", space.decode())

    sucess = True
    while content:
        if SEP in content:
            file, content = content.split(SEP, 1)
        else:
            file = content
            content = None

        decoded = FileData.decode_files(file)
        response = decoded.save_file(space.decode())
        sucess = sucess and response
    
    if not sucess:
        raise CommandError("Upload completed but filesystem was in readonly mode")
    client.send(b"Upload completed successfully")


class FileData:

    def __init__(self, path: bytes, name: bytes, content: bytes):
        self.path = path.decode()
        self.name = name.decode()
        self.content = content

    @staticmethod
    def decode_files(file: bytes):
        try:
            data = bytes(zlib.decompress(file))
            path, name, content = data.split(SEP, 2)
            return FileData(path, name, content)
        except Exception as e:
            print(e)
            raise CommandError("File data is corrupted")

    def save_file(self, space: str):
        try:
            if self.name == ".":
                print("mkdir", self.path, self.name)
                os.mkdir(f"/{space}/{self.path}")
                return True
            else:
                print("file", self.path, self.name, len(self.content))
                with open(f"/{space}/{self.path}/{self.name}", "wb") as file:
                    file.write(self.content)
                return True
        except Exception as e:
            print(e)
            return False
