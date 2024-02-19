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

def handleException(exception, throw):
    def wrapper(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception as e:
                raise throw(e)
        return inner
    return wrapper
