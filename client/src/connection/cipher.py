import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding, rsa


class AESCipher:

    def __init__(self, key: bytes = None):
        self._key = key or self.generate_key()

    @property
    def key(self) -> bytes:
        return self._key

    @staticmethod
    def generate_key(length: int = 16) -> bytes:
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

    def encrypt(self, message: bytes) -> bytes:
        return self.public.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def decrypt(self, ciphertext: bytes) -> bytes:
        return self.private.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )