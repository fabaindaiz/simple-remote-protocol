import os
import zlib

from src.connection.base import SEP, Handler
from src.protocol.base import CommandError, handleException
from src.protocol.mapper import Router, split_args


router = Router()

@router.register("update")
@handleException(OSError, CommandError)
def update(client: Handler, command: str, data: str):
    args = split_args(data)
    if len(args) == 2:
        space, build = args
        command = b"update "
        content = Encoder.encode_files(space.encode(), build.encode())
        data = command + content
        print("Uploading files...")

        client.send(data)
        response = client.receive()
        print(response.decode())
        return

    raise CommandError("Invalid upload command")


class Encoder:

    @staticmethod
    def encode_file(path: str, name: str, file: bytes):
        data = path.encode() + SEP + name.encode() + SEP + file
        return zlib.compress(data)

    @staticmethod
    def encode_files(space: bytes, build: bytes):
        filedata = []

        for path, name in Encoder.list_files(build.decode(), recursive=True):
            if name == ".":
                data = b""
            else:
                with open(os.path.join("files", path, name), "rb") as f:
                    data = f.read()
            encoded = Encoder.encode_file(path, name, data)
            filedata.append(encoded)

        bindata = SEP.join(filedata)
        return space + SEP + build + SEP + bindata
    
    @staticmethod
    def list_files(path: str, recursive: bool = False):
        location = os.path.join("files", path)
        listdir = os.listdir(location)
        
        yield (path, ".")
        yield from ((path, file) for file in listdir if os.path.isfile(os.path.join(location, file)))

        if recursive:
            folders = (folder for folder in listdir if os.path.isdir(os.path.join(location, folder)))
            for folder in folders:
                yield from Encoder.list_files(f"{path}/{folder}", recursive)
