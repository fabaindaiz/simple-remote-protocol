
EOF = b"\r\n\r\n"
SEP = b"\r\n"


class Handler():

    def receive(self) -> bytes:
        raise NotImplementedError
    
    def send(self):
        raise NotImplementedError
    
    def close(self):
        raise NotImplementedError
