from src.connection.base import Handler, SEP
from src.connection.cipher import AESCipher, RSACipher
from src.connection.signer import HMACSigner, HeaderSigner


class SecureHandler(Handler):

    def __init__(self, handler: Handler):
        self.server_aes, self.client_aes, self.hmac = client_handshake(handler)
        self.header = HeaderSigner()
        self.handler = handler

    def receive(self, buffer: int = 1024) -> bytes:
        data: bytes = self.handler.receive(buffer)
        payload, iv, hmac = data.split(SEP, 2)
        self.hmac.verify(payload, hmac)
        decrypted = self.server_aes.decrypt(payload, iv)
        header, message = decrypted.split(SEP, 1)
        self.header.verify(message, header)
        return message
    
    def send(self, message: bytes):
        header = self.header.sign(message)
        encoded = header + SEP + message
        payload, iv = self.client_aes.encrypt(encoded)
        hmac = self.hmac.sign(payload)
        data = payload + SEP + iv + SEP + hmac
        self.handler.send(data)

    def close(self):
        self.handler.close()


def client_handshake(handler: Handler) -> tuple[AESCipher, AESCipher, HMACSigner]:
    client_rsa = RSACipher()
    client_rsa_exp = client_rsa.save_public()
    handler.send(client_rsa_exp)

    server_aes_enc = handler.receive()
    server_aes = AESCipher(client_rsa.decrypt(server_aes_enc))

    client_aes = AESCipher()
    aes_data, aes_iv = server_aes.encrypt(client_aes.key)
    handler.send(aes_data + SEP + aes_iv)

    server_hmac_enc = handler.receive()
    hmac_data, hmac_iv = server_hmac_enc.split(SEP, 1)
    server_hmac = HMACSigner(client_aes.decrypt(hmac_data, hmac_iv))

    return server_aes, client_aes, server_hmac
