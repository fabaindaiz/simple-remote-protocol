from src.connection.base import Handler
from src.protocol.base import SessionError
from src.protocol.mapper import Router


router = Router()

@router.register("exit")
def exit(client: Handler, command: bytes, data: bytes):
    print("sending exit command, closing session...")
    raise SessionError("Session closed")
