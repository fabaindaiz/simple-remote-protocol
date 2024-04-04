import asyncio

async def main():
    while True:
        print("Hello World")
        await asyncio.sleep(1)

asyncio.run(main())
