import os
import zlib

from src.connection.base import SEP


class Encoder:

    @staticmethod
    def encode_file(name: str, file: bytes):
        data = name.encode() + SEP + file
        return zlib.compress(data)

    @staticmethod
    def encode_files(space: str, build: str):
        filedata = []

        path, files = Encoder.list_files(build, recursive=True)
        for file in files:
            with open(os.path.join("files", path, file), "rb") as f:
                data = f.read()
            encoded = Encoder.encode_file(f"{file}/{path}", data)
            filedata.append(encoded)

        space = space.encode()
        build = build.encode()
        bindata = SEP.join(filedata)
        return space + SEP + build + SEP + bindata
    
    @staticmethod
    def list_files(path: str, recursive: bool = False):
        location = os.path.join("files", path)
        listdir = os.listdir(location)
        yield from ((path, file) for file in listdir if os.path.isfile(os.path.join(location, file)))

        if recursive:
            folders = (folder for folder in listdir if os.path.isdir(os.path.join(location, folder)))
            for folder in folders:
                yield from Encoder.list_files(f"{path}/{folder}", recursive)
