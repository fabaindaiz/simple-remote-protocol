import gc
import os
import microcontroller
import supervisor

from firmware.connection.base import Handler
from firmware.protocol.base import SessionError
from firmware.protocol.mapper import Router


router = Router()

@router.register(b"metrics")
def metrics(client: Handler, command: bytes, data: bytes):
    gc.collect()
    mem_free = gc.mem_free() / 1000
    mem_alloc = gc.mem_alloc() / 1000
    mem_total = mem_free + mem_alloc
    block_size = os.statvfs('/')[0] / 1000
    disk_free = os.statvfs('/')[3] * block_size
    disk_total = os.statvfs('/')[2] * block_size
    disk_used = disk_total - disk_free

    response = [
        f"frec: {round(microcontroller.cpu.frequency/1000000, 2)} MKz",
        f"temp: {round(microcontroller.cpu.temperature, 4)} °C",
        f"mem: {round(mem_free, 2)} / {round(mem_total, 2)} kB",
        f"disk: {round(disk_free, 2)} / {round(disk_total, 2)} kB",
    ]
    client.send("\n".join(response).encode())

@router.register(b"reboot")
def reboot(client: Handler, command: bytes, data: bytes):
    print("reboot command received, rebooting device...")
    client.send(b"Rebooting...")
    supervisor.reload()

@router.register(b"exit")
def exit(client: Handler, command: bytes, data: bytes):
    print("exit command received, closing session...")
    raise SessionError("Session closed")
