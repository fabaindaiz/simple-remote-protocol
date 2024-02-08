import os
import circuitpython_hmac as hmac

from firmware.connection.base import SEP, SecurityError


class HMACSigner:

    def __init__(self, key: bytes = None):
        self.key = key or self.generate_key()

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
        return count + length
    
    def verify(self, message: bytes, signature: bytes):
        count, length = signature[:2], signature[2:]
        if int.from_bytes(count, "big") != self.counter:
            raise SecurityError("Invalid header")
        if int.from_bytes(length, "big") != len(message):
            raise SecurityError("Invalid header")
        self.counter += 1
