import gc
import microcontroller
import supervisor

from firmware.connection.base import Handler, SEP
from firmware.protocol.base import SessionError
from firmware.protocol.mapper import Router


router = Router()

@router.register(b"metrics")
def metrics(client: Handler, command: bytes, data: bytes):
    gc.collect()
    metrics = [
        "METRICS",
        f"cpu uid: {str(microcontroller.cpu.uid)}",
        f"cpu frec: {microcontroller.cpu.frequency} Hz",
        f"cpu temp: {microcontroller.cpu.temperature} C",
        f"mem free: {gc.mem_free()} bytes",
    ]
    client.send("\n".join(metrics).encode())

@router.register(b"reboot")
def reboot(client: Handler, command: bytes, data: bytes):
    print("reboot command received, rebooting device...")
    client.send(b"Rebooting...")
    supervisor.reload()

@router.register(b"exit")
def exit(client: Handler, command: bytes, data: bytes):
    print("exit command received, closing session...")
    raise SessionError("Session closed")
