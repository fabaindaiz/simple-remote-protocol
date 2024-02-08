import asyncio
import gc

from internal.connection import WiznetConnection


async def main(connection: WiznetConnection):
    print("Hello, world!")
    
    while True:
        gc.collect()
        print(f"free: {round(gc.mem_free() / 1000, 4)} kB")
        await asyncio.sleep(0.2)
        