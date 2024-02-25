import asyncio


class Singleton(type):
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, *args, **kwargs):
        if not self._initialized:
            self._initialized = True

class Supervisor:

    async def supervisor(self):
        raise NotImplementedError

    async def register(self):
        asyncio.create_task(self.supervisor())