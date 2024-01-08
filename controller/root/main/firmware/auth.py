import adafruit_hashlib as hashlib

from internal.filesystem import ROOT


class HashAuth:

    @staticmethod
    def generate(key: bytes):
        u = hashlib.sha512()
        u.update(key)
        with open(f"{ROOT}/authkey", "wb") as file:
            file.write(u.hexdigest().encode())

    @staticmethod
    def check(key: bytes) -> bool:
        hash = hashlib.sha512()
        hash.update(key)
        with open(f"{ROOT}/authkey", "r") as file:
            auth = file.read()
        return auth == hash.hexdigest()
