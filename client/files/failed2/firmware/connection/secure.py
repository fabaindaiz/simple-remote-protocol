from firmware.connection.base import SEP, Handler, SecurityError, handleException
from firmware.connection.cipher import AESCipher, RSACipher
from firmware.connection.signer import HMACSigner, HeaderSigner


class SecureHandler(Handler):

    def __init__(self, handler: Handler):
        self.server_aes, self.client_aes, self.hmac, self.header = server_handshake(handler)
        self.handler = handler
    
    def settimeout(self, timeout: float):
        self.handler.settimeout(timeout)

    def missing_message(self):
        self.header.missing_message()

    def receive(self, buffer: int = 1024) -> bytes:
        data: bytes = self.handler.receive(buffer)
        payload, iv, hmac = data.split(SEP, 2)
        self.hmac.verify(payload, hmac)
        decrypted = self.client_aes.decrypt(payload, iv)
        header, message = decrypted.split(SEP, 1)
        self.header.verify(message, header)
        return message
    
    def send(self, message: bytes):
        header = self.header.sign(message)
        encoded = header + SEP + message
        payload, iv = self.server_aes.encrypt(encoded)
        hmac = self.hmac.sign(payload)
        data = payload + SEP + iv + SEP + hmac
        self.handler.send(data)

    def close(self):
        self.handler.close()


@handleException(SecurityError("Handshake failed"))
def server_handshake(handler: Handler) -> tuple[AESCipher, AESCipher, HMACSigner, HeaderSigner]:
    client_rsa_exp = handler.receive()
    client_rsa_key = RSACipher.load_public(client_rsa_exp)
    client_rsa = RSACipher(client_rsa_key)

    server_aes = AESCipher()
    handler.send(client_rsa.encrypt(server_aes.key))

    client_aes_enc = handler.receive()
    aes_data, aes_iv = client_aes_enc.split(SEP, 1)
    client_aes = AESCipher(server_aes.decrypt(aes_data, aes_iv))

    server_hmac = HMACSigner()
    hmac_data, hmac_iv = client_aes.encrypt(server_hmac.key)
    handler.send(hmac_data + SEP + hmac_iv)

    server_header = HeaderSigner()
    return server_aes, client_aes, server_hmac, server_header
