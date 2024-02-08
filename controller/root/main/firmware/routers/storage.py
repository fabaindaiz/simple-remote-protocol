import os

from firmware.connection.base import Handler, SEP
from firmware.protocol.base import ProtocolError
from firmware.protocol.mapper import Router


router = Router()

@router.register(b"storage")
def send_metrics(client: Handler, command: bytes, data: bytes):
    os.chdir("/")
    args = data.split(SEP)
    if len(args) == 1:
        inst = args[0]
        if inst == b"cd":
            os.chdir("/")
            client.send(b"OK")
        elif inst == b"ls":
            folders = os.listdir()
            client.send(" ".join(folders).encode())
        elif inst == b"pwd":
            client.send(os.getcwd().encode())
        else:
            raise ProtocolError("Invalid file command")
        
    elif len(args) == 2:
        inst, path = args
        if inst == b"cd":
            os.chdir(path)
            client.send(b"OK")
        elif inst == b"mkdir":
            os.mkdir(path)
            client.send(b"OK")
        elif inst == b"rm":
            os.remove(path)
            client.send(b"OK")
        elif inst == b"rmdir":
            os.rmdir(path)
            client.send(b"OK")
        else:
            raise ProtocolError("Invalid file command")
    
    elif len(args) == 3:
        inst, old, new = args
        if inst == b"mv":
            os.rename(old, new)
            client.send(b"OK")
        else:
            raise ProtocolError("Invalid file command")

    else:
        raise ProtocolError("Invalid file command")
