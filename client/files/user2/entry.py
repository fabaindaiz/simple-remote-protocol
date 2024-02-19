import asyncio


async def main(connection):
    while True:
        print("Hello World with updates!")
        await asyncio.sleep(1)
        