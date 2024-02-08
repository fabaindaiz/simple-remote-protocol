import adafruit_hashlib as hashlib

from internal.filesystem import ROOT
from firmware.protocol.base import AuthError


class Auth:

    @staticmethod
    def hash(key: bytes) -> str:
        u = hashlib.sha512()
        u.update(key)
        return u.hexdigest()

    @staticmethod
    def generate(key: bytes):
        value = Auth.hash(key)
        with open(f"{ROOT}/authkey", "wb") as file:
            file.write(value.encode())

    @staticmethod
    def check(client) -> bool:
        key = client.receive()
        value = Auth.hash(key)
        with open(f"{ROOT}/authkey", "rb") as file:
            auth = file.read()
        if auth != value.encode():
            raise AuthError("Invalid key")
        client.send(b"AUTH OK")
