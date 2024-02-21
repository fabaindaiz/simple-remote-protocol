import microcontroller

AUTHKEY = None

class NVMDir:
    SECURE = 4
    CONFIG = 5

    ROOT = 7
    USER = 8


class NVMValue:

    @staticmethod
    def encode(data: bytes, padding: int) -> bytes:
        size = len(data)
        if size >= padding:
            raise ValueError("Data too long")
        return size.to_bytes(1, "big") + data + b"\x00" * (padding - size - 1)

    @staticmethod
    def decode(data: bytes) -> bytes:
        size = data[0]
        if size == 0:
            return None
        return data[1:size+1]


class NVMemory(bytearray):
    def __init__(self, padding: int = 32) -> None:
        if microcontroller.nvm is None:
            raise ImportError("NVM not supported")
        self._mem_size = len(microcontroller.nvm)
        self._gap_num = self._mem_size // padding
        self._gap_size = padding

        self.memory: bytearray[self._mem_size]
        self._change = False
        self._initialize()

    def __enter__(self) -> 'NVMemory':
        self.memory = microcontroller.nvm[:self._mem_size]
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self._change:
            microcontroller.nvm[:self._mem_size] = self.memory
        self.memory = None
        self._change = False

    def __len__(self) -> int:
        return self._gap_num

    def __getitem__(self, index: int) -> bytes:
        mem_slice = self._get_slice(index)
        encoded = self.memory[mem_slice]
        return NVMValue.decode(encoded)
    
    def __setitem__(self, index: int, value: bytes):
        mem_slice = self._get_slice(index)
        encoded = NVMValue.encode(value, self._gap_size)
        self.memory[mem_slice] = encoded
        self._change = True
    
    def _get_slice(self, index: int) -> slice:
        if not isinstance(index, int):
            raise ValueError("Slice not supported")
        if index == 0:
            raise ValueError("Index reserved")
        if index >= self._gap_num:
            raise ValueError("Index out of range")
        start = index * self._gap_size
        end = start + self._gap_size
        return slice(start, end)

    def _initialize(self, force: bool = False):
        AUTHKEY = microcontroller.nvm[0:128]
        with open("authkey", "rb") as file:
            authkey = file.read()
        if AUTHKEY != authkey or force:
            print("Initializing memory...")
            memory = authkey + b"\x00" * (self._mem_size - 128)
            microcontroller.nvm[:self._mem_size] = memory


# Use NVMemory as a context manager to access the memory
# This will ensure that the memory is properly updated
MEMORY = NVMemory()
