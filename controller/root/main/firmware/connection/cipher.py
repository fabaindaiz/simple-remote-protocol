import os
import aesio
import adafruit_rsa
from firmware.connection.base import SEP, SecurityError, handleException


class AESCipher:

    def __init__(self, key: bytes = None):
        self._key = key or self.generate_key()

    @property
    def key(self) -> bytes:
        return self._key

    @staticmethod
    def generate_key(len: int = 32) -> bytes:
        return os.urandom(len)

    @handleException(SecurityError("AES encryption failed"))
    def encrypt(self, message: bytes) -> tuple[bytes, bytes]:
        iv = self.generate_key(16)
        output = bytearray(len(message))
        cipher = aesio.AES(self.key, aesio.MODE_CTR, iv)
        cipher.encrypt_into(message, output)
        return bytes(output), iv

    @handleException(SecurityError("AES decryption failed"))
    def decrypt(self, message: bytes, iv: bytes) -> bytes:
        output = bytearray(len(message))
        cipher = aesio.AES(self.key, aesio.MODE_CTR, iv)
        cipher.decrypt_into(message, output)
        return bytes(output)


class RSACipher:

    def __init__(self, public: adafruit_rsa.PublicKey, private: adafruit_rsa.PrivateKey = None):
            self._public = public
            self._private = private
    
    @property
    def public(self):
        return self._public
    
    @property
    def private(self):
        if self._private is None:
            raise SecurityError("Private key not available")
        return self._private
    
    @staticmethod
    def load_public(public_exp: bytes) -> adafruit_rsa.PublicKey:
        n, e = public_exp.split(SEP, 1)
        return adafruit_rsa.PublicKey(int.from_bytes(n, 'big'), int.from_bytes(e, 'big'))
    
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
    
    @handleException(SecurityError("RSA encryption failed"))
    def encrypt(self, message: bytes) -> bytes:
        return adafruit_rsa.encrypt(message, self.public)
    
    @handleException(SecurityError("RSA decryption failed"))
    def decrypt(self, message: bytes) -> bytes:
        return adafruit_rsa.decrypt(message, self.private)
