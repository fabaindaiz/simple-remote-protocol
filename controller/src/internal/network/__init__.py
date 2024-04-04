import os
import asyncio
import supervisor
from internal.base import Singleton
from internal.network.base import NetworkController

class NetworkLoader(Singleton):
    @Singleton.init
    def __init__(self):
        self._network = None

        network = os.getenv("NETWORK", "WIZNET5K")
        if network == "WIZNET5K":
            from internal.network.w5x00 import W5x00Controller
            self._network = W5x00Controller()
            self.start_supervisor()
            
            ifconfig = ((192, 168, 1, 220), (255, 255, 255, 0), (192, 168, 1, 1), (8, 8, 8, 8))
            self._network.connect(ifconfig, is_dhcp=False)
        else:
            raise RuntimeError(f"Unsupported network controller: {network}")
    
    @property
    def network(self) -> NetworkController:
        return self._network

    def start_supervisor(self):
        async def _supervisor():
            print("Starting network supervisor...")
            while True:
                if not self._network.link_status:
                    print("Ethernet disconnected!")
                    supervisor.reload()
                await asyncio.sleep(0.5)
        asyncio.create_task(_supervisor())
