import os
import aesio
import adafruit_rsa
import circuitpython_hmac as hmac

from firmware.connection.base import SEP


class AESCipher:

    def __init__(self, key: bytes = None):
        self._key = key or self.generate_key()

    @property
    def key(self) -> bytes:
        return self._key

    @staticmethod
    def generate_key(len: int = 32) -> bytes:
        return os.urandom(len)

    def encrypt(self, message: bytes) -> tuple[bytes, bytes]:
        iv = self.generate_key(16)
        output = bytearray(len(message))
        cipher = aesio.AES(self.key, aesio.MODE_CTR, iv)
        cipher.encrypt_into(message, output)
        return bytes(output), iv

    def decrypt(self, message: bytes, iv: bytes) -> bytes:
        output = bytearray(len(message))
        cipher = aesio.AES(self.key, aesio.MODE_CTR, iv)
        cipher.decrypt_into(message, output)
        return bytes(output)


class RSACipher:

    def __init__(self, public: adafruit_rsa.PublicKey):
            self._public = public
    
    @property
    def public(self):
        return self._public
    
    @staticmethod
    def load_private(private_exp: bytes) -> adafruit_rsa.PrivateKey:
        n, e, d, p, q = private_exp.split(SEP, 4)
        return adafruit_rsa.PrivateKey(
            int.from_bytes(n, 'big'),
            int.from_bytes(e, 'big'),
            int.from_bytes(d, 'big'),
            int.from_bytes(p, 'big'),
            int.from_bytes(q, 'big')
        )
    
    @staticmethod
    def load_public(public_exp: bytes) -> adafruit_rsa.PublicKey:
        n, e = public_exp.split(SEP, 1)
        return adafruit_rsa.PublicKey(int.from_bytes(n, 'big'), int.from_bytes(e, 'big'))
    
    def encrypt(self, message: bytes) -> bytes:
        return adafruit_rsa.encrypt(message, self.public)


class HMACCipher:

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

    def verify(self, message: bytes, signature: bytes) -> bool:
        return signature == self.sign(message)
    