from src.connection.base import Handler, EOF


class SocketHandler(Handler):

    def __init__(self, client, address: tuple) -> None:
        self.client = client
        self.address = address
        self.next = b''
    
    def receive(self, buffer: int = 1024) -> bytes:
        data = self.next
        while True:
            chunk: bytes = self.client.recv(buffer)
            if EOF in chunk:
                end, self.next = chunk.split(EOF, 1)
                data += end
                break
            data += chunk
        return data
    
    def send(self, data: bytes):
        self.client.send(data + EOF)

    def close(self):
        self.client.close()
