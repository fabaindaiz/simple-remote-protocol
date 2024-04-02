import asyncio


def main():
    try:
        from internal.filesystem import Filesystem

        print("Starting controller...")
        Filesystem.remount()

        root = Filesystem().root()
        asyncio.create_task(root)
        print("Root loaded!")

        user = Filesystem().user()
        asyncio.run(user)
        asyncio.create_task(user)
        print("User loaded!")

        asyncio.run()
        print("Controller started successfully!\n")
    except Exception as exception:
        import internal.recovery as recovery
        recovery.system_recovery(exception)
