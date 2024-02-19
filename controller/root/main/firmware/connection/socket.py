from firmware.connection.base import EOF, Handler, TransportError, handleException


class SocketHandler(Handler):

    def __init__(self, client, address: tuple) -> None:
        self.client = client
        self.address = address
        self.next = b''

    def settimeout(self, timeout: float):
        self.client.settimeout(timeout)

    def missing_message(self):
        pass
    
    @handleException(TransportError("Socket receive failed"))
    def receive(self, buffer: int = 1024) -> bytes:
        data = self.next
        while True:
            chunk: bytes = self.client.recv(buffer)
            if EOF in chunk:
                end, next = chunk.split(EOF, 1)
                data += end
                break
            data += chunk
        return data
    
    @handleException(TransportError("Socket send failed"))
    def send(self, data: bytes):
        self.client.send(data + EOF)

    @handleException(TransportError("Socket close failed"))
    def close(self):
        self.client.close()
