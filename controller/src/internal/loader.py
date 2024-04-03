import asyncio
from internal.filesystem import Filesystem

async def loop():
    while True:
        asyncio.sleep(1)

def main():
    try:
        print("Starting controller...")

        root = Filesystem().root()
        asyncio.create_task(root)
        print("Root loaded!")

        user = Filesystem().user()
        asyncio.create_task(user)
        print("User loaded!")

        asyncio.run(loop)
        print("Controller started successfully!\n")
    except Exception as exception:
        import internal.recovery as recovery
        recovery.system_recovery(exception)
