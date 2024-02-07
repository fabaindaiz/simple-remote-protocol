from src.connection.base import Handler, SEP
from src.connection.cipher import AESCipher, RSACipher, HMACCipher


class SecurityException(Exception): ...

class SecureHandler(Handler):

    def __init__(self, handler: Handler):
        self.server_aes, self.client_aes, self.server_hmac = client_handshake(handler)
        self.handler = handler
        self.counter = 0

    def receive(self, buffer: int = 1024) -> bytes:
        data: bytes = self.handler.receive(buffer)
        payload, iv, hmac = data.split(SEP, 2)
        if not self.server_hmac.verify(payload, hmac):
            raise SecurityException("Invalid HMAC")
        decoded = self.server_aes.decrypt(payload, iv)
        header, message = decoded.split(SEP, 1)
        if int.from_bytes(header, "big") != self.counter:
            raise SecurityException("Invalid counter")
        self.counter += 1
        return message
    
    def send(self, message: bytes):
        header = b"" + self.counter.to_bytes(4, "big")
        self.counter += 1
        payload, iv = self.client_aes.encrypt(header + SEP + message)
        hmac = self.server_hmac.sign(payload)
        self.handler.send(payload + SEP + iv + SEP + hmac)

    def close(self):
        self.handler.close()


def client_handshake(handler: Handler) -> tuple[AESCipher, AESCipher]:
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
    server_hmac = HMACCipher(client_aes.decrypt(hmac_data, hmac_iv))

    return server_aes, client_aes, server_hmac
