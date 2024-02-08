import adafruit_hashlib as hashlib

from internal.filesystem import ROOT
from firmware.protocol.base import Context, AuthError
from firmware.connection.base import Handler


class Authentication:

    @staticmethod
    def hash(key: bytes) -> str:
        u = hashlib.sha512()
        u.update(key)
        return u.hexdigest()

    @staticmethod
    def generate(key: bytes):
        value = Authentication.hash(key)
        with open(f"{ROOT}/authkey", "wb") as file:
            file.write(value.encode())

    @staticmethod
    def authenticate(client: Handler) -> Context:
        value = Authentication.hash(client.receive())
        with open(f"{ROOT}/authkey", "rb") as file:
            if file.read() != value.encode():
                raise AuthError("Invalid key")
        client.send(b"AUTH OK")
        return Context()
