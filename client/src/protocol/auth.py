from getpass import getpass

from src.connection.base import Handler, SecurityError


class Authentication:

    def __init__(self, password) -> None:
        self._password = password

    @staticmethod
    def password_prompt() -> "Authentication":
        password = getpass().encode()
        return Authentication(password)
    
    def autenticate(self, handler: Handler):
        request = b"AUTH " + self._password
        handler.send(request)
        if handler.receive() != b"AUTH OK":
            raise SecurityError("Invalid authentication")
    
    def setkey(self, handler: Handler):
        request = b"SETKEY " + self._password
        handler.send(request)
        if handler.receive() != b"AUTH OK":
            raise SecurityError("Invalid authentication")
