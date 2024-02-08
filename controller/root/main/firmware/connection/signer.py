import os
import circuitpython_hmac as hmac

from firmware.connection.base import SecurityError, SEP


class HMACSigner:

    def __init__(self, key: bytes = None):
        self._key = key or self.generate_key()

    @property
    def key(self) -> bytes:
        return self._key

    @staticmethod
    def generate_key(len: int = 32) -> bytes:
        return os.urandom(len)
    
    def sign(self, message: bytes) -> bytes:
        return hmac.new(self.key, message).digest()

    def verify(self, message: bytes, signature: bytes):
        if signature != self.sign(message):
            raise SecurityError("Invalid HMAC")


class HeaderSigner:

    def __init__(self):
        self.counter = 0

    def sign(self, message: bytes) -> bytes:
        count = self.counter.to_bytes(2, "big")
        length = len(message).to_bytes(2, "big")
        self.counter += 1
        return count + SEP + length
    
    def verify(self, message: bytes, signature: bytes):
        count, length = signature.split(SEP, 1)
        if int.from_bytes(count, "big") != self.counter:
            raise SecurityError("Invalid counter")
        if int.from_bytes(length, "big") != len(message):
            raise SecurityError("Invalid length")
        self.counter += 1
