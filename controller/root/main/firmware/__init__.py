import asyncio

from internal.connection import WiznetConnection
from firmware.protocol.command import Command
from firmware.protocol.encode import Decoder
from firmware.protocol.updater import Updater


command = Command()

@command.register(b"UPLOAD")
def upload(client, command, data):
    try:
        for folder, name, file in Decoder.decode_files(data):
            print("UPLOAD", folder, name, len(file))
        client.send(b"UPLOAD OK")
    except:
        client.send(b"UPLOAD ERROR")
    
    client.close()


async def main(connection: WiznetConnection):
    updater = Updater(connection, command)
    updater.start()

    while True:
        await updater.loop()
        await asyncio.sleep(1)
