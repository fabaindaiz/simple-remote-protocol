import microcontroller
from internal.base import Singleton

class NVM:
    ROOT = 4
    USER = 5

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
        return data[1:size+1]

class NVMController(Singleton):
    @Singleton.init
    def __init__(self, padding: int = 32) -> None:
        if microcontroller.nvm is None:
            raise ImportError("NVM not supported")
        self._mem_size = len(microcontroller.nvm)
        self._gap_num = self._mem_size // padding
        self._gap_size = padding
        
        self._memory = None
        self._changed = False

    @property
    def memory(self):
        if self._memory is None:
            raise ValueError("Use NVMController as a context manager to access the memory")
        return self._memory

    def _get_slice(self, index: int) -> slice:
        if not isinstance(index, int):
            raise ValueError("Only integer index supported")
        if index >= self._gap_num:
            raise ValueError("Index out of range")
        start = index * self._gap_size
        end = start + self._gap_size
        return slice(start, end)

    def __enter__(self) -> 'NVMController':
        self._memory = microcontroller.nvm[:self._mem_size]
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self._changed:
            microcontroller.nvm[:self._mem_size] = self._memory
        self._memory = None
        self._changed = False

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
        self._changed = True

    def clear(self):
        self.memory = b"\x00" * self._mem_size
        self._changed = True
