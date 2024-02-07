import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from src.connection.base import SEP


class AESCipher:

    def __init__(self, key: bytes = None):
        self._key = key or self.generate_key()

    @property
    def key(self) -> bytes:
        return self._key

    @staticmethod
    def generate_key(length: int = 32) -> bytes:
        return os.urandom(length)

    def encrypt(self, message: bytes) -> tuple[bytes, bytes]:
        iv = self.generate_key(16)  # Para AES, IV siempre debe ser de 16 bytes para CTR.
        cipher = Cipher(algorithms.AES(self.key), modes.CTR(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(message) + encryptor.finalize()
        return ct, iv

    def decrypt(self, ciphertext: bytes, iv: bytes) -> bytes:
        cipher = Cipher(algorithms.AES(self.key), modes.CTR(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()


class RSACipher:

    def __init__(self, public = None):
        if public is None:
            self._private = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            self._public = self._private.public_key()
        else:
            self._public = public
            self._private = None

    @property
    def public(self):
        return self._public

    @property
    def private(self):
        if not self._private:
            raise ValueError("No private key available.")
        return self._private
    
    def save_public(self) -> bytes:
        # get public numbers
        public_numbers = self.public.public_numbers()
        n = public_numbers.n
        e = public_numbers.e
        return n.to_bytes(256, 'big') + SEP + e.to_bytes(4, 'big')
    
    def save_private(self, password: bytes) -> bytes:
        values = self.private.private_numbers()
        sizes = [256, 4, 256, 128, 128]
        return SEP.join(value.to_bytes(size, 'big') for value, size in zip(values, sizes))

    def encrypt(self, message: bytes) -> bytes:
        return self.public.encrypt(message, padding.PKCS1v15())

    def decrypt(self, ciphertext: bytes) -> bytes:
        return self.private.decrypt(ciphertext, padding.PKCS1v15())


class HMACCipher:

    def __init__(self, key: bytes = None):
        self._key = key or self.generate_key()

    @property
    def key(self) -> bytes:
        return self._key

    @staticmethod
    def generate_key(length: int = 32) -> bytes:
        return os.urandom(length)
    
    def sign(self, message: bytes) -> bytes:
        h = hmac.HMAC(self.key, hashes.SHA256())
        h.update(message)
        return h.finalize()

    def verify(self, message: bytes, signature: bytes) -> bool:
        h = hmac.HMAC(self.key, hashes.SHA256())
        h.update(message)
        try:
            h.verify(signature)
            return True
        except:
            return False
