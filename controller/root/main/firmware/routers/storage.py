import os

from firmware.connection.base import Handler
from firmware.protocol.base import CommandError, handleException
from firmware.protocol.mapper import Router, split_args


router = Router()

@router.register(b"pwd")
@handleException(OSError, CommandError)
def storage_pwd(client: Handler, command: bytes, data: bytes):
    args = split_args(data)
    if len(args) == 0:
        path = os.getcwd()
    else:
        raise CommandError("Invalid parameters")
    client.send(path.encode())

@router.register(b"ls")
@handleException(OSError, CommandError)
def storeage_ls(client: Handler, command: bytes, data: bytes):
    args = split_args(data)
    if len(args) == 0:
        folders = os.listdir()
    elif len(args) == 1:
        folders = os.listdir(args[0].decode())
    else:
        raise CommandError("Invalid parameters")
    client.send(" ".join(folders).encode())

@router.register(b"cd")
@handleException(OSError, CommandError)
def storage_cd(client: Handler, command: bytes, data: bytes):
    args = split_args(data)
    if len(args) == 0:
        os.chdir("/")
    elif len(args) == 1:
        os.chdir(args[0].decode())
    else:
        raise CommandError("Invalid parameters")
    client.send(b"OK")

@router.register(b"cat")
@handleException(OSError, CommandError)
def storage_cat(client: Handler, command: bytes, data: bytes):
    args = split_args(data)
    if len(args) == 1:
        with open(args[0].decode(), "r") as f:
            client.send(f.read().encode())
    else:
        raise CommandError("Invalid parameters")

@router.register(b"stat")
@handleException(OSError, CommandError)
def storage_stat(client: Handler, command: bytes, data: bytes):
    args = split_args(data)
    if len(args) == 0:
        stat = os.stat(os.getcwd())
    elif len(args) == 1:
        stat = os.stat(args[0].decode())
    else:
        raise CommandError("Invalid parameters")
    response = [
        f"mode: {hex(stat[0])}",
        f"size: {stat[6]} B"
    ]
    client.send("\n".join(response).encode())

@router.register(b"mv")
@handleException(OSError, CommandError)
def storage_mv(client: Handler, command: bytes, data: bytes):
    args = split_args(data)
    if len(args) == 2:
        os.rename(args[0].decode(), args[1].decode())
    else:
        raise CommandError("Invalid parameters")
    client.send(b"OK")

@router.register(b"cp")
@handleException(OSError, CommandError)
def storage_cp(client: Handler, command: bytes, data: bytes):
    args = split_args(data)
    if len(args) == 2:
        with open(args[0].decode(), "rb") as f:
            data = f.read()
        with open(args[1].decode(), "wb") as g:
            g.write(data)
    else:
        raise CommandError("Invalid parameters")
    client.send(b"OK")

@router.register(b"rm")
@handleException(OSError, CommandError)
def storage_rm(client: Handler, command: bytes, data: bytes):
    args = split_args(data)
    if len(args) == 1:
        os.remove(args[0].decode())
    else:
        raise CommandError("Invalid parameters")
    client.send(b"OK")

@router.register(b"mkdir")
@handleException(OSError, CommandError)
def storage_mkdir(client: Handler, command: bytes, data: bytes):
    args = split_args(data)
    if len(args) == 1:
        os.mkdir(args[0].decode())
    else:
        raise CommandError("Invalid parameters")
    client.send(b"OK")

@router.register(b"rmdir")
@handleException(OSError, CommandError)
def storage_rmdir(client: Handler, command: bytes, data: bytes):
    args = split_args(data)
    if len(args) == 1:
        os.rmdir(args[0].decode())
    else:
        raise CommandError("Invalid parameters")
    client.send(b"OK")
