from internal.connection import WiznetConnection
from firmware.connection.secure import SecureConnection, SecureHandler
from firmware.protocol.auth import Auth


class Updater:

    def __init__(self, connection: WiznetConnection):
        self.connection = SecureConnection(connection, self.process)
        self.connection.callback = self.process
        self.connection.start()
        self._command = None

    @property
    def command(self):
        if not self._command:
            raise ValueError("Command not set")
        return self._command
    
    @command.setter
    def command(self, value):
        self._command = value

    def process(self, client: SecureHandler):
        authkey = client.receive()

        if not Auth.check(authkey):
            print(f"Connection closed: Invalid authkey")
            client.send(b"Connection closed: Invalid authkey")
            client.close()

        self.command.process(client)

    async def loop(self):
        await self.connection.listen()
