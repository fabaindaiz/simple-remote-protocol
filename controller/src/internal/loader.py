import asyncio
from internal.memory import NVMController, NVM
from internal.storage import StorageController

def main():
    #try:
        with NVMController() as memory:
            memory[NVM.ROOT] = b"main"
            memory[NVM.USER] = b"test"

        print("Starting controller...")

        root = StorageController().root.main
        asyncio.create_task(root)
        print("Root loaded!")

        user = StorageController().user.main
        asyncio.create_task(user)
        print("User loaded!")

        asyncio.run(loop)
        print("Controller started successfully!\n")
    #except Exception as exception:
    #    import internal.recovery as recovery
    #    recovery.system_recovery(exception)

async def loop():
    while True:
        asyncio.sleep(1)
