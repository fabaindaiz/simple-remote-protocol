from src.connection.base import Handler, SEP
from src.connection.cipher import AESCipher, RSACipher


class SecureHandler(Handler):

    def __init__(self, handler: Handler):
        self.client_aes, self.server_aes = client_handshake(handler)
        self.handler = handler

    def receive(self, buffer: int = 1024) -> bytes:
        data: bytes = self.handler.receive(buffer)
        message, iv = data.split(SEP, 1)
        return self.client_aes.decrypt(message, iv)
    
    def send(self, data: bytes):
        message, iv = self.server_aes.encrypt(data)
        self.handler.send(message + SEP + iv)

    def close(self):
        self.handler.close()


def client_handshake(handler: Handler) -> tuple[AESCipher, AESCipher]:
    # RSA public key exchange
    server_rsa_key = handler.receive(1024)
    server_rsa = RSACipher(server_rsa_key)

    client_rsa = RSACipher()
    handler.send(client_rsa.public)

    # AES session key exchange
    server_aes_enc = handler.receive()
    server_aes = AESCipher(server_rsa.decrypt(server_aes_enc))

    client_aes = AESCipher()
    handler.send(server_aes.encrypt(client_aes.key))

    return client_aes, server_aes
