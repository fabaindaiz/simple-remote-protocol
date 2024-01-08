import os
import zlib

EOF = b"\r\n\r\n"
SEP = b"\r\n"


class Encoder:

    @staticmethod
    def encode_file(name: str, file: bytes):
        data = name.encode() + SEP + file
        return zlib.compress(data)

    @staticmethod
    def encode_files(build: str):
        path = f"files/{build}"
        files = os.listdir(path)
        filedata = []

        for file in files:
            with open(os.path.join(path, file), "rb") as f:
                data = f.read()
            encoded = Encoder.encode_file(file, data)
            filedata.append(encoded)

        start = b"FILES\r\n"
        folder = build.encode() + SEP
        bindata = SEP.join(filedata)
        return start + folder + bindata + EOF
