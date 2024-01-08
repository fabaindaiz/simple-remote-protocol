import asyncio

from internal.connection import Connection


async def main(connection: Connection):
    while True:
        print("Hello World!")
        await asyncio.sleep(1)
        