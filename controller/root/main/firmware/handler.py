EOF = b"\r\n\r\n"


class Handler():

    def receive(self):
        raise NotImplementedError
    
    def send(self):
        raise NotImplementedError
    
    def close(self):
        raise NotImplementedError


class SocketHandler(Handler):

    def __init__(self, client, address: tuple) -> None:
        self.client = client
        self.address = address
    
    def receive(self, buffer: int = 1024) -> bytes:
        data = b''
        while True:
            chunk = self.client.recv(buffer)
            data += chunk
            if chunk.endswith(EOF):
                break
        return data[:-len(EOF)]
    
    def send(self, data: bytes):
        self.client.send(data + EOF)

    def close(self):
        self.client.close()
