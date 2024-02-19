
EOF = b"\r\n\r\n"
SEP = b"\r\n"


class ProtocolError(Exception): ...
class AuthError(ProtocolError): ...
class CommandError(ProtocolError): ...
class ResolveError(ProtocolError): ...
class SessionError(ProtocolError): ...


def handleException(exception, throw):
    def wrapper(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception as e:
                raise throw(e)
        return inner
    return wrapper
