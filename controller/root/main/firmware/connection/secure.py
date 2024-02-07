from firmware.connection.base import Handler, SEP
from firmware.connection.cipher import AESCipher, RSACipher


class SecureHandler(Handler):

    def __init__(self, handler: Handler):
        self.server_aes = server_handshake(handler)
        self.handler = handler

    def receive(self, buffer: int = 1024) -> bytes:
        data: bytes = self.handler.receive(buffer)
        message, iv = data.split(SEP, 1)
        return self.server_aes.decrypt(message, iv)
    
    def send(self, data: bytes):
        message, iv = self.server_aes.encrypt(data)
        self.handler.send(message + SEP + iv)

    def close(self):
        self.handler.close()


def server_handshake(handler: Handler) -> tuple[AESCipher, AESCipher]:
    client_rsa_exp = handler.receive()
    client_rsa_key = RSACipher.load_public(client_rsa_exp)
    client_rsa = RSACipher(client_rsa_key)

    server_aes = AESCipher()
    handler.send(client_rsa.encrypt(server_aes.key))

    #client_aes_enc = handler.receive()
    #data, iv = client_aes_enc.split(SEP, 1)
    #client_aes = AESCipher(server_aes.decrypt(data, iv))
    return server_aes
