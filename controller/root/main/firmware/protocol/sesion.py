from firmware.protocol.auth import Auth
from firmware.protocol.base import AuthError, ProtocolError, SessionEnd
from firmware.connection.base import ConnectionError, SecurityError
from firmware.connection.secure import SecureHandler
from firmware.connection.socket import SocketHandler


class Sesion:

    def __init__(self, command):
        self.command = command

    def loop(self, client):
        while True:
            try:
                self.command.process(client)
            
            except ProtocolError as e:
                client.send(b"Command error")

    async def start(self, connection, address):
        try:
            try:
                socket = SocketHandler(connection, address)
                client = SecureHandler(socket)
                print("Secure connection established")

                Auth.check(client)
                print("Authentification success")
                
                self.loop(client)
            
            except AuthError:
                client.send(b"AUTH ERROR")
                print("Connection closed: Auth error")
            except SessionEnd:
                client.send(b"SESSION END")
                print("Connection closed: Session ended")
            
            except ConnectionError as e:
                print("Connection closed:", e)
            except SecurityError as e:
                print("Connection closed:", e)
            finally:
                client.close()
        
        except RuntimeError:
            print("Connection closed: Client disconnected")
