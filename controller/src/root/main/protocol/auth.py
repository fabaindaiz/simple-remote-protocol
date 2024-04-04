import microcontroller
import adafruit_hashlib as hashlib
from ..protocol.base import Context, AuthError
from ..connection.base import Handler

class Authentication:
    @staticmethod
    def hash(key: bytes) -> str:
        u = hashlib.sha512()
        u.update(key)
        return u.hexdigest()

    @staticmethod
    def generate(key: bytes):
        value = Authentication.hash(key)
        microcontroller.nvm[0:128] = value.encode()

    @staticmethod
    def authenticate(client: Handler) -> Context:
        command, content = client.receive().split(b" ", 1)
        if command == b"AUTH":
            value = Authentication.hash(content)
            with open("authkey", "rb") as file:
                if file.read() != value.encode():
                    raise AuthError("Invalid key")
            client.send(b"AUTH OK")
        elif command == b"SETKEY":
            raise AuthError("Not implemented")
        else:
            raise AuthError("Invalid command")
        return Context()
