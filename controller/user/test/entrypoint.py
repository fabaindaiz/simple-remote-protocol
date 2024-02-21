import gc
import asyncio

from internal.connection import WiznetConnection


async def main(connection: WiznetConnection):
    
    while True:
        print(f"free: {round(gc.mem_free() / 1000, 4)} kB")
        await asyncio.sleep(0.5)
        