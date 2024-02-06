import asyncio
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket

from firmware.connection.base import Connection, Handler, EOF


class SocketConnection(Connection):

    def __init__(self, ethernet: str) -> None:
        self.ethernet = ethernet
        self._callback = None

    @property
    def callback(self):
        if not self._callback:
            raise ValueError("Callback not set")
        return self._callback
    
    @callback.setter
    def callback(self, value):
        self._callback = value

    def start(self):
        socket.set_interface(self.ethernet)
        self.server = socket.socket()

        self.server.bind((None, 8080))
        self.server.setblocking(False)
        self.server.settimeout(0.04)
        self.server.listen(1)
        print("Socket listening en 8080")

    async def listen(self):
        while True:
            try:
                client, address = self.server.accept()
                print("Conexión desde", address)

                handler = SocketHandler(client, address)
                self.callback(handler)

            except TimeoutError:
                await asyncio.sleep(0.01)


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
