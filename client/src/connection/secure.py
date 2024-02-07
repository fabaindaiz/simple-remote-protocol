from src.connection.base import Handler, SEP
from src.connection.cipher import AESCipher, RSACipher


class SecureHandler(Handler):

    def __init__(self, handler: Handler):
        self.server_aes = client_handshake(handler)
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


def client_handshake(handler: Handler) -> tuple[AESCipher, AESCipher]:
    client_rsa = RSACipher()
    client_rsa_exp = client_rsa.save_public()
    handler.send(client_rsa_exp)

    server_aes_enc = handler.receive()
    server_aes = AESCipher(client_rsa.decrypt(server_aes_enc))

    #client_aes = AESCipher()
    #data, iv = server_aes.encrypt(client_aes.key)
    #handler.send(data + SEP + iv)
    return server_aes
