import json

from internal.memory import MEMORY, NVMDir


with MEMORY as memory:
    config = memory[NVMDir.CONFIG].decode()

def _load_config() -> dict:
    path = f"internal/config/{config}"
    with open(path, "r") as file:
        return json.load(file)


CONFIG = _load_config()
