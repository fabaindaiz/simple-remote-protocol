import asyncio


class Singleton(type):
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @staticmethod
    def init(func):
        def wrapper(self, *args, **kwargs):
            if not self._initialized:
                self._initialized = True
                func(self, *args, **kwargs)
        return wrapper

class Supervisor:

    async def supervisor(self):
        raise NotImplementedError

    def register(self):
        asyncio.create_task(self.supervisor())
