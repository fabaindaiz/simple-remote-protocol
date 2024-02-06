import os
import aesio
import adafruit_rsa


class AESCipher:

    def __init__(self, key: bytes = None):
        self._key = key or self.generate_key()

    @property
    def key(self) -> bytes:
        return self._key

    @staticmethod
    def generate_key(len: int = 16) -> bytes:
        return os.urandom(len)

    def encrypt(self, message: bytes) -> tuple[bytes, bytes]:
        iv = self.generate_key()
        output = bytearray(len(message))
        cipher = aesio.AES(self.key, aesio.MODE_CTR, iv)
        cipher.encrypt_into(message, output)
        return output, iv

    def decrypt(self, message: bytes, iv: bytes) -> bytes:
        output = bytearray(len(message))
        cipher = aesio.AES(self.key, aesio.MODE_CTR, iv)
        cipher.decrypt_into(message, output)
        return output


class RSACipher:

    def __init__(self, public: adafruit_rsa.PublicKey = None):
        if public is None:
            self._public, self._private = self.generate_key()
        else:
            self._public = public
            self._private = None
    
    @property
    def public(self) -> adafruit_rsa.PublicKey:
        return self._public
    
    @property
    def private(self) -> adafruit_rsa.PrivateKey:
        if not self._private:
            raise ValueError("No private key")
        return self._private
    
    @staticmethod
    def generate_key(len: int = 1024) -> tuple[adafruit_rsa.PublicKey, adafruit_rsa.PrivateKey]:
        return adafruit_rsa.newkeys(len)
    
    def encrypt(self, message: bytes) -> bytes:
        return adafruit_rsa.encrypt(message, self.public)

    def decrypt(self, message: bytes) -> bytes:
        return adafruit_rsa.decrypt(message, self.private)
