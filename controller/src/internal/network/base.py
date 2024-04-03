import asyncio

class NetworkController:
    @property
    def link_status(self) -> bool:
        return NotImplementedError
    
    @property
    def socket(self) -> tuple:
        return NotImplementedError
    
    def connect(self, ifconfig: tuple, mac_address: bytes):
        return NotImplementedError
    
    async def supervisor(self):
        return NotImplementedError
    
    def start_supervisor(self):
        asyncio.create_task(self.supervisor())
