import asyncio
import gc

async def main():
    while True:
        print(f"free: {round(gc.mem_free() / 1000, 4)} kB")
        await asyncio.sleep(0.5)
