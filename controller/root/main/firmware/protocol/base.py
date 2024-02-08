from firmware.connection.base import Handler


EOF = b"\r\n\r\n"
SEP = b"\r\n"


class ProtocolError(Exception): ...
class AuthError(ProtocolError): ...
class CommandError(ProtocolError): ...
class SessionError(ProtocolError): ...


class Context:
    pass


def response(client: Handler, message: str):
    client.send(message.encode())
    print(message)
