import asyncio

from internal.connection import Connection
from firmware.protocol.command import Command
from firmware.protocol.encode import Decoder
from firmware.protocol.updater import Updater


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

    updater = Updater(connection)
    updater.command = command

    while True:
        await updater.loop()
        await asyncio.sleep(1)
