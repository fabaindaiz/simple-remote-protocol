import adafruit_hashlib as hashlib

from internal.filesystem import ROOT


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
    def check(key: bytes) -> bool:
        try:
            value = Auth.hash(key)
            with open(f"{ROOT}/authkey", "rb") as file:
                auth = file.read()
            return auth == value.encode()
        except:
            return False
