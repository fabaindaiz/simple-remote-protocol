
EOF = b"\r\n\r\n"
SEP = b"\r\n"


class ConnectionError(Exception): ...
class SecurityError(ConnectionError): ...
class TransportError(ConnectionError): ...


class Handler():

    def settimeout(self, timeout: float):
        raise NotImplementedError

    def receive(self) -> bytes:
        raise NotImplementedError
    
    def send(self):
        raise NotImplementedError
    
    def close(self):
        raise NotImplementedError


def handleException(exception: ConnectionError):
    def wrapper(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise exception from e
        return inner
    return wrapper
