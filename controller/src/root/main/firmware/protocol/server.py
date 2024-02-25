import gc
import asyncio
import microcontroller
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
from adafruit_httpserver import Server, Request, JSONResponse
from firmware.protocol.mapper import CommandMapper
from firmware.protocol.sesion import RemoteSession


class RemoteServer:

    def __init__(self, connection, command: CommandMapper):
        self.connection = connection
        self.command = command
    
    async def start(self, host: tuple = (None, 8080), listen: int = 1):
        #socket.set_interface(self.connection.ethernet)
        #self.socket = socket.socket()

        #self.socket.bind(host)
        #self.socket.setblocking(False)
        #self.socket.settimeout(0.1)
        #self.socket.listen(listen)
        print("Socket listening en 8080")
        print(self.connection.ethernet.pretty_ip(self.connection.ethernet.ip_address))

        server = Server(socket)
        @server.route("/")#, append_slash=True)
        def cpu_information_handler(request: Request):
            data = {
                "frequency": f"{round(microcontroller.cpu.frequency/1000000, 2)} MKz",
                "temperature": f"{round(microcontroller.cpu.temperature, 4)} °C",
            }
            return JSONResponse(request, data)
        server.start(str(self.connection.ethernet.pretty_ip(self.connection.ethernet.ip_address)))
        while True:
            server.poll()
            await asyncio.sleep(0.1)

    async def loop(self):
        while True:
            try:
                client, address = self.socket.accept()
                print("Connection from", address)

                sesion = RemoteSession(self.command)
                asyncio.create_task(sesion.start(client, address))
            
            except TimeoutError:
                gc.collect()
                await asyncio.sleep(2)
