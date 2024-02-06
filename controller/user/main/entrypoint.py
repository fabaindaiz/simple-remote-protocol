import asyncio

from internal.connection import WiznetConnection


async def main(connection: WiznetConnection):
    while True:
        print("Hello World!")
        await asyncio.sleep(1)
        