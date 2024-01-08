import asyncio

from internal.connection import Connection
from firmware.command import Command
from firmware.encode import Decoder
from firmware.remote import Remote


command = Command()

@command.register(b"UPLOAD")
def upload(client, data):
    try:
        for folder, name, file in Decoder.decode_files(data):
            print("UPLOAD", folder, name, len(file))
        client.send(b"OK")
    except:
        client.send(b"ERROR")
    
    client.close()


async def main(connection: Connection):
    remote = Remote(connection)
    remote.set_command(command)

    while True:
        await remote.updater()
        await asyncio.sleep(1)
