import os
from internal.utils import Singleton, Supervisor


class NetworkController(Singleton):
    @Singleton.init
    def __init__(self):
        self._network = None

        network = os.getenv("NETWORK", "w5x00")
        if network is "w5x00":
            from internal.network.w5x00 import W5x00Controller
            self._network = W5x00Controller()
        else:
            raise RuntimeError(f"Unsupported network controller: {network}")