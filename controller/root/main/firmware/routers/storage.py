import os

from firmware.connection.base import Handler, SEP
from firmware.protocol.base import CommandError
from firmware.protocol.mapper import Router


router = Router()

@router.register(b"storage")
def storage(client: Handler, command: bytes, data: bytes):
    try:
        args = data.split(b" ")
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
                raise CommandError("Invalid storage command")
            
        elif len(args) == 2:
            inst, path = args
            if inst == b"cd":
                os.chdir(path.decode())
                client.send(b"OK")
            elif inst == b"mkdir":
                os.mkdir(path.decode())
                client.send(b"OK")
            elif inst == b"rm":
                os.remove(path.decode())
                client.send(b"OK")
            elif inst == b"rmdir":
                os.rmdir(path.decode())
                client.send(b"OK")
            else:
                raise CommandError("Invalid storage command")
        
        elif len(args) == 3:
            inst, old, new = args
            if inst == b"mv":
                os.rename(old.decode(), new.decode())
                client.send(b"OK")
            else:
                raise CommandError("Invalid storage command")

        else:
            raise CommandError("Invalid storage command")

    except OSError:
        raise CommandError("Storage command failed")
