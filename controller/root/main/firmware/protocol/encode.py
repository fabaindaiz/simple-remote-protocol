import zlib

from firmware.connection.base import SEP


class Decoder:

    @staticmethod
    def decode_files(data: bytes):
        try:
            header, folder, content = data.split(SEP, 2)
            if not header == b"FILES":
                raise ValueError("Invalid data")
            
            files = content.split(SEP)
            for file in files:
                data = bytes(zlib.decompress(file))
                name, content = data.split(b"\r\n", 1)
                yield folder.decode(), name.decode(), content
        except Exception as e:
            print("Invalid file format", e)
            raise ValueError("Invalid data")
