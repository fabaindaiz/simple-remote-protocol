from firmware.connection.base import Handler, SEP
from firmware.connection.cipher import AESCipher, RSACipher, HMACCipher


class SecurityException(Exception): ...

class SecureHandler(Handler):

    def __init__(self, handler: Handler):
        self.server_aes, self.client_aes, self.server_hmac = server_handshake(handler)
        self.handler = handler
        self.counter = 0

    def receive(self, buffer: int = 1024) -> bytes:
        data: bytes = self.handler.receive(buffer)
        payload, iv, hmac = data.split(SEP, 2)
        if not self.server_hmac.verify(payload, hmac):
            raise SecurityException("Invalid HMAC")
        decoded = self.client_aes.decrypt(payload, iv)
        header, message = decoded.split(SEP, 1)
        if int.from_bytes(header, "big") != self.counter:
            raise SecurityException("Invalid counter")
        self.counter += 1
        return message
    
    def send(self, message: bytes):
        header = b"" + self.counter.to_bytes(4, "big")
        self.counter += 1
        payload, iv = self.server_aes.encrypt(header + SEP + message)
        hmac = self.server_hmac.sign(payload)
        self.handler.send(payload + SEP + iv + SEP + hmac)

    def close(self):
        self.handler.close()


def server_handshake(handler: Handler) -> tuple[AESCipher, AESCipher, HMACCipher]:
    client_rsa_exp = handler.receive()
    client_rsa_key = RSACipher.load_public(client_rsa_exp)
    client_rsa = RSACipher(client_rsa_key)

    server_aes = AESCipher()
    handler.send(client_rsa.encrypt(server_aes.key))

    client_aes_enc = handler.receive()
    aes_data, aes_iv = client_aes_enc.split(SEP, 1)
    client_aes = AESCipher(server_aes.decrypt(aes_data, aes_iv))

    server_hmac = HMACCipher()
    hmac_data, hmac_iv = client_aes.encrypt(server_hmac.key)
    handler.send(hmac_data + SEP + hmac_iv)

    return server_aes, client_aes, server_hmac
